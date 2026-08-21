"""Command line entry point."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from .config import Pipeline, Stage, load_pipelines, stage_applies
from .interview import classify, interview
from .runner import execute, new_run_dir
from .session import discover_skills


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="workbench",
        description="Interview, then execute through a skill sequence enforced in code.",
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="Directory the SDK runs in. Skills load from .claude/skills/ here, in its "
        "parents up to the repo root, and from ~/.claude/skills/.",
    )
    parser.add_argument(
        "--pipelines", type=Path, default=None, help="Alternative pipelines.yaml"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the full interview-then-execute loop")
    run.add_argument("request", nargs="+", help="What you want done, in a sentence or two")
    run.add_argument("--pipeline", help="Skip classification and force this pipeline")
    run.add_argument("--out", type=Path, default=Path("runs"), help="Where run output lands")
    run.add_argument(
        "--plan-only",
        action="store_true",
        help="Interview and print the brief and stage plan, then stop before executing",
    )
    run.add_argument(
        "--yes", action="store_true", help="Do not confirm before each stage"
    )

    sub.add_parser("pipelines", help="List pipelines and their enforced stage order")

    doctor = sub.add_parser(
        "doctor", help="Report which required skills the SDK can actually see on disk"
    )
    doctor.add_argument("--pipeline", help="Check one pipeline instead of all")

    args = parser.parse_args()
    pipelines = load_pipelines(args.pipelines)
    project = args.project.resolve()

    if args.command == "pipelines":
        return _cmd_pipelines(pipelines)
    if args.command == "doctor":
        return asyncio.run(_cmd_doctor(pipelines, project, args.pipeline))
    return asyncio.run(_cmd_run(pipelines, project, args))


def _cmd_pipelines(pipelines: dict[str, Pipeline]) -> int:
    for name, pipeline in pipelines.items():
        print(f"\n{name}")
        print(f"  {pipeline.description.strip()}")
        for index, stage in enumerate(pipeline.stages, start=1):
            condition = f"  (only when: {stage.when})" if stage.when else ""
            skills = ", ".join(stage.skills) or "none"
            print(f"  {index}. {stage.title:<28} skills: {skills}{condition}")
    print()
    return 0


async def _cmd_doctor(
    pipelines: dict[str, Pipeline], project: Path, only: str | None
) -> int:
    print(f"Project directory: {project}")
    print("Asking the SDK what it discovered...\n")
    try:
        found = await discover_skills(project)
    except Exception as error:  # noqa: BLE001 - surface any startup failure plainly
        print(f"Could not start a session: {error}", file=sys.stderr)
        return 2

    print(f"Discovered {len(found)} user-invocable skills.\n")
    selected = {only: pipelines[only]} if only else pipelines
    missing_total: set[str] = set()

    for name, pipeline in selected.items():
        required = pipeline.skill_names()
        missing = [s for s in required if s not in found]
        missing_total.update(missing)
        status = "ok" if not missing else f"missing {len(missing)}"
        print(f"{name}: {status}")
        for skill in required:
            mark = "  ok " if skill in found else "  -- "
            print(f"{mark}{skill}")
        print()

    if missing_total:
        print("Missing skills are not on disk where the SDK looks. Export them to")
        print("~/.claude/skills/<name>/SKILL.md or <project>/.claude/skills/<name>/SKILL.md.")
        print("A stage whose skills are all missing will run with no skill at all.")
        return 1
    return 0


async def _cmd_run(
    pipelines: dict[str, Pipeline], project: Path, args: argparse.Namespace
) -> int:
    request = " ".join(args.request)

    if args.pipeline:
        if args.pipeline not in pipelines:
            print(f"Unknown pipeline {args.pipeline!r}. Known: {', '.join(pipelines)}", file=sys.stderr)
            return 2
        name = args.pipeline
        print(f"Pipeline: {name} (forced)")
    else:
        print("Routing...")
        try:
            name, reason = await classify(request, pipelines, project)
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2
        print(f"Pipeline: {name} ({reason.get('confidence', 'unknown')} confidence)")
        print(f"  {reason.get('reason', '')}")
        if not _confirm("Use this pipeline?"):
            name = _choose_pipeline(pipelines)

    pipeline = pipelines[name]
    print("\nIntake. One question at a time. Blank answer skips a question.\n")

    brief = await interview(
        request,
        pipeline,
        project,
        ask_user=_ask,
        on_note=lambda note: print(f"  [{note}]"),
    )

    print("\nBrief collected:")
    print(json.dumps({k: v for k, v in brief.items() if not k.startswith("_")}, indent=2))
    if brief.get("_inferred"):
        print("\nInferred without asking:")
        for item in brief["_inferred"]:
            print(f"  - {item}")
    if brief.get("_gaps"):
        print("\nStill open:")
        for item in brief["_gaps"]:
            print(f"  - {item}")

    plan = [s for s in pipeline.stages if stage_applies(s.when, brief)]
    print("\nStages that will run:")
    for index, stage in enumerate(plan, start=1):
        print(f"  {index}. {stage.title}: {', '.join(stage.skills) or 'no skills'}")
    skipped = [s for s in pipeline.stages if s not in plan]
    for stage in skipped:
        print(f"  -- {stage.title} (skipped: {stage.when})")

    if args.plan_only:
        print("\nStopped before execution (--plan-only).")
        return 0

    if not _confirm("\nRun it?"):
        return 0

    run_dir = new_run_dir(args.out, pipeline.name)
    record = await execute(
        pipeline,
        brief,
        project,
        run_dir,
        on_stage=_report_stage,
        confirm=(lambda _: True) if args.yes else _confirm_stage,
    )

    print(f"\nOutput written to {record.root}")
    for outcome in record.outcomes:
        print(f"  {outcome.status:<8} {outcome.title}")
    return 0


def _ask(payload: dict[str, Any]) -> str:
    print(f"\n{payload.get('question', '').strip()}")
    if payload.get("why"):
        print(f"  why: {payload['why'].strip()}")
    for suggestion in payload.get("suggestions") or []:
        print(f"  e.g. {suggestion}")
    try:
        return input("> ").strip()
    except EOFError:
        return ""


def _report_stage(stage: Stage, status: str) -> None:
    if status == "running":
        print(f"\n-> {stage.title}  [{', '.join(stage.skills) or 'no skills'}]")
    else:
        print(f"   {status}")


def _confirm_stage(stage: Stage) -> bool:
    return _confirm(f"\nRun '{stage.title}' with {', '.join(stage.skills) or 'no skills'}?")


def _confirm(question: str) -> bool:
    try:
        answer = input(f"{question} [Y/n] ").strip().lower()
    except EOFError:
        return True
    return answer in ("", "y", "yes")


def _choose_pipeline(pipelines: dict[str, Pipeline]) -> str:
    names = list(pipelines)
    for index, name in enumerate(names, start=1):
        print(f"  {index}. {name}: {pipelines[name].description.strip()}")
    while True:
        raw = input("Pipeline number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(names):
            return names[int(raw) - 1]
        print("Pick a number from the list.")


if __name__ == "__main__":
    raise SystemExit(main())
