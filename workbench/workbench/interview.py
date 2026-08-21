"""Classification and the one-question-at-a-time intake.

Both run with `skills=[]`. The interviewer's job is to collect, not to work, and
denying it the skill surface keeps it from starting the job early.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from .config import Pipeline
from .session import run_turn

MAX_QUESTIONS = 25

CLASSIFY_PROMPT = """You are routing a piece of work to one of a fixed set of pipelines.

The request:
<request>
{request}
</request>

The pipelines:
{catalogue}

Pick exactly one. Prefer the narrowest pipeline that covers the whole request.
Reply with nothing but a fenced JSON block:

```json
{{"pipeline": "<name>", "reason": "<one sentence>", "confidence": "high|medium|low"}}
```"""

INTERVIEW_SYSTEM = """You are conducting an intake interview. You are not doing the work.

The request:
<request>
{request}
</request>

Pipeline: {pipeline}. {description}

Fields to fill:
{questions}

Rules:
1. Ask ONE question per turn. Never batch.
2. Never ask what the request already answers, or what you can infer with confidence. Fill those fields yourself and say so in `inferred`.
3. Never ask a question whose answer would not change the output.
4. You may add a field beyond the list when the request clearly needs one.
5. When a required field is still empty after two attempts, record the gap and move on.

Reply with nothing but a fenced JSON block, in one of two shapes.

To ask:

```json
{{"status": "ask", "key": "<field>", "question": "<the question>", "why": "<why it changes the output>", "suggestions": ["<optional example answers>"]}}
```

To finish:

```json
{{"status": "done", "brief": {{"<field>": "<value>"}}, "inferred": ["<field: what you assumed and from where>"], "gaps": ["<field: why it is still open>"]}}
```"""


async def classify(
    request: str, pipelines: dict[str, Pipeline], cwd: Path
) -> tuple[str, dict[str, Any]]:
    catalogue = "\n".join(f"- {name}: {p.description}" for name, p in pipelines.items())
    result = await run_turn(
        CLASSIFY_PROMPT.format(request=request, catalogue=catalogue),
        cwd=cwd,
        skills=[],
        allowed_tools=[],
        max_turns=1,
    )
    payload = result.json_block() or {}
    choice = payload.get("pipeline")
    if choice not in pipelines:
        raise ValueError(
            f"Classifier returned {choice!r}, which is not a known pipeline. "
            f"Re-run with --pipeline to choose one of: {', '.join(pipelines)}"
        )
    return choice, payload


async def interview(
    request: str,
    pipeline: Pipeline,
    cwd: Path,
    ask_user: Callable[[dict[str, Any]], str],
    on_note: Callable[[str], None] = lambda _: None,
) -> dict[str, Any]:
    """Drive the intake loop. `ask_user` renders one question and returns the answer."""

    questions = "\n".join(
        f"- {q.key} ({'required' if q.required else 'optional'}): {q.ask}"
        + (f"  [{q.why}]" if q.why else "")
        for q in pipeline.questions
    )
    prompt = INTERVIEW_SYSTEM.format(
        request=request,
        pipeline=pipeline.name,
        description=pipeline.description,
        questions=questions,
    )

    session_id: str | None = None
    answers: dict[str, Any] = {}

    for _ in range(MAX_QUESTIONS):
        result = await run_turn(
            prompt,
            cwd=cwd,
            skills=[],
            allowed_tools=[],
            resume=session_id,
            max_turns=2,
        )
        session_id = result.session_id
        payload = result.json_block()

        if payload is None:
            on_note("Interviewer replied without a JSON block; asking it to restate.")
            prompt = "Reply again with only the fenced JSON control block."
            continue

        if payload.get("status") == "done":
            brief = dict(payload.get("brief") or {})
            brief.update(answers)
            brief["_inferred"] = payload.get("inferred") or []
            brief["_gaps"] = payload.get("gaps") or []
            brief["_request"] = request
            brief["_pipeline"] = pipeline.name
            return brief

        key = payload.get("key") or f"field_{len(answers)}"
        answer = ask_user(payload)
        answers[key] = answer
        prompt = json.dumps({"answered": {key: answer}})

    on_note(f"Hit the {MAX_QUESTIONS}-question ceiling; proceeding with what was collected.")
    return {
        **answers,
        "_inferred": [],
        "_gaps": ["interview hit the question ceiling before the model declared it complete"],
        "_request": request,
        "_pipeline": pipeline.name,
    }
