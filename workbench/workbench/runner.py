"""The stage engine.

Each stage is a separate `query()` call carrying only that stage's skills. Order
is decided here, in code, not by the model. A stage cannot reach a skill from a
later stage, so a gate cannot be stepped over.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from .config import Pipeline, Stage, stage_applies
from .session import run_turn

STAGE_PROMPT = """{instruction}

The brief collected at intake:
```json
{brief}
```

{prior}

Skills available to you in this step: {skills}
Use them. If the work needs a skill that is not on that list, stop and say which one and why, rather than working around it.
"""


@dataclass
class StageOutcome:
    stage: str
    title: str
    skills: list[str]
    status: str
    text: str = ""
    note: str = ""


@dataclass
class RunRecord:
    root: Path
    pipeline: str
    brief: dict[str, Any]
    outcomes: list[StageOutcome] = field(default_factory=list)

    def write(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "brief.json").write_text(
            json.dumps(self.brief, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        for index, outcome in enumerate(self.outcomes, start=1):
            if outcome.status != "ran":
                continue
            name = f"{index:02d}-{outcome.stage}.md"
            body = f"# {outcome.title}\n\nSkills: {', '.join(outcome.skills) or 'none'}\n\n{outcome.text}\n"
            (self.root / name).write_text(body, encoding="utf-8")
        (self.root / "run.json").write_text(
            json.dumps(
                {
                    "pipeline": self.pipeline,
                    "stages": [
                        {
                            "stage": o.stage,
                            "status": o.status,
                            "skills": o.skills,
                            "note": o.note,
                        }
                        for o in self.outcomes
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )


def new_run_dir(base: Path, pipeline: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return base / f"{stamp}-{pipeline}"


async def execute(
    pipeline: Pipeline,
    brief: dict[str, Any],
    cwd: Path,
    run_dir: Path,
    on_stage: Callable[[Stage, str], None] = lambda s, m: None,
    confirm: Callable[[Stage], bool] = lambda _: True,
) -> RunRecord:
    record = RunRecord(root=run_dir, pipeline=pipeline.name, brief=brief)
    session_id: str | None = None
    prior_summaries: list[str] = []

    for stage in pipeline.stages:
        if not stage_applies(stage.when, brief):
            record.outcomes.append(
                StageOutcome(
                    stage=stage.name,
                    title=stage.title,
                    skills=stage.skills,
                    status="skipped",
                    note=f"condition not met: {stage.when}",
                )
            )
            on_stage(stage, "skipped")
            continue

        if not confirm(stage):
            record.outcomes.append(
                StageOutcome(
                    stage=stage.name,
                    title=stage.title,
                    skills=stage.skills,
                    status="declined",
                    note="declined at the confirmation prompt",
                )
            )
            on_stage(stage, "declined")
            if stage.required:
                break
            continue

        on_stage(stage, "running")
        prior = ""
        if prior_summaries:
            prior = "What earlier steps produced:\n\n" + "\n\n---\n\n".join(prior_summaries)

        prompt = STAGE_PROMPT.format(
            instruction=stage.prompt,
            brief=json.dumps({k: v for k, v in brief.items() if not k.startswith("_")}, indent=2),
            prior=prior,
            skills=", ".join(stage.skills) or "none",
        )

        result = await run_turn(
            prompt,
            cwd=cwd,
            skills=stage.skills,
            allowed_tools=stage.allowed_tools,
            resume=session_id,
        )
        session_id = result.session_id

        outcome = StageOutcome(
            stage=stage.name,
            title=stage.title,
            skills=stage.skills,
            status="ran" if not result.is_error else "error",
            text=result.text,
        )
        record.outcomes.append(outcome)
        on_stage(stage, outcome.status)

        if result.is_error and stage.required:
            outcome.note = "required stage errored; run halted"
            break

        if stage.writes:
            brief[stage.writes] = result.text
        prior_summaries.append(f"## {stage.title}\n\n{result.text}")

    record.write()
    return record
