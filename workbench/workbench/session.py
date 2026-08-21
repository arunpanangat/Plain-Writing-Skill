"""Thin wrapper over the Claude Agent SDK.

Every call here is one turn against one stage's skill allowlist. Context carries
across turns through `resume`; the allowlist does not, which is what lets the
runner change what is invokable between stages.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    SystemMessage,
    TextBlock,
    query,
)

_JSON_FENCE = re.compile(r"```json\s*(.*?)```", re.DOTALL | re.IGNORECASE)


@dataclass
class TurnResult:
    text: str
    session_id: str | None
    discovered_skills: list[str] = field(default_factory=list)
    is_error: bool = False

    def json_block(self) -> dict[str, Any] | None:
        """Return the last fenced JSON object in the reply, or None."""
        fences = _JSON_FENCE.findall(self.text)
        for candidate in reversed(fences):
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
        return _scan_for_object(self.text)


async def run_turn(
    prompt: str,
    *,
    cwd: Path,
    skills: list[str] | str,
    allowed_tools: list[str],
    resume: str | None = None,
    max_turns: int | None = None,
    model: str | None = None,
    permission_mode: str = "acceptEdits",
) -> TurnResult:
    options = ClaudeAgentOptions(
        cwd=str(cwd),
        setting_sources=["user", "project"],
        skills=skills,
        allowed_tools=allowed_tools,
        permission_mode=permission_mode,
        resume=resume,
        max_turns=max_turns,
        model=model,
    )

    parts: list[str] = []
    session_id = resume
    discovered: list[str] = []
    is_error = False

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, SystemMessage):
            data = getattr(message, "data", {}) or {}
            if message.subtype == "init":
                discovered = list(data.get("skills") or [])
            session_id = data.get("session_id") or session_id
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    parts.append(block.text)
        elif isinstance(message, ResultMessage):
            session_id = getattr(message, "session_id", None) or session_id
            is_error = message.subtype != "success"
            result_text = getattr(message, "result", None)
            if result_text and not parts:
                parts.append(str(result_text))

    return TurnResult(
        text="\n".join(parts).strip(),
        session_id=session_id,
        discovered_skills=discovered,
        is_error=is_error,
    )


async def discover_skills(cwd: Path) -> list[str]:
    """Ask the SDK what it can actually see on disk. Used by `workbench doctor`."""
    result = await run_turn(
        "Reply with the single word: ready",
        cwd=cwd,
        skills=[],
        allowed_tools=[],
        max_turns=1,
    )
    return result.discovered_skills


def _scan_for_object(text: str) -> dict[str, Any] | None:
    """Fallback for a reply that emitted bare JSON without a fence."""
    depth = 0
    start = -1
    best: dict[str, Any] | None = None
    for index, char in enumerate(text):
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0 and start >= 0:
                try:
                    parsed = json.loads(text[start : index + 1])
                except json.JSONDecodeError:
                    continue
                if isinstance(parsed, dict):
                    best = parsed
    return best
