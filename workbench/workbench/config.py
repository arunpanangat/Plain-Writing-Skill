"""Pipeline definitions: the stage sequence and the skills each stage may use."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_PIPELINES = Path(__file__).with_name("pipelines.yaml")


@dataclass
class Stage:
    """One enforced step. `skills` is the whole point: nothing else is invokable here."""

    name: str
    title: str
    prompt: str
    skills: list[str] = field(default_factory=list)
    allowed_tools: list[str] = field(default_factory=lambda: ["Read", "Grep", "Glob"])
    when: str | None = None
    writes: str | None = None
    required: bool = True

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Stage":
        return cls(
            name=raw["name"],
            title=raw.get("title", raw["name"]),
            prompt=raw["prompt"].strip(),
            skills=list(raw.get("skills", [])),
            allowed_tools=list(raw.get("allowed_tools", ["Read", "Grep", "Glob"])),
            when=raw.get("when"),
            writes=raw.get("writes"),
            required=bool(raw.get("required", True)),
        )


@dataclass
class Question:
    key: str
    ask: str
    why: str = ""
    required: bool = True

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Question":
        return cls(
            key=raw["key"],
            ask=raw["ask"].strip(),
            why=raw.get("why", "").strip(),
            required=bool(raw.get("required", True)),
        )


@dataclass
class Pipeline:
    name: str
    description: str
    questions: list[Question]
    stages: list[Stage]

    @classmethod
    def from_dict(cls, name: str, raw: dict[str, Any]) -> "Pipeline":
        return cls(
            name=name,
            description=raw["description"].strip(),
            questions=[Question.from_dict(q) for q in raw.get("questions", [])],
            stages=[Stage.from_dict(s) for s in raw["stages"]],
        )

    def skill_names(self) -> list[str]:
        seen: list[str] = []
        for stage in self.stages:
            for skill in stage.skills:
                if skill not in seen:
                    seen.append(skill)
        return seen


def load_pipelines(path: Path | None = None) -> dict[str, Pipeline]:
    source = path or DEFAULT_PIPELINES
    raw = yaml.safe_load(source.read_text(encoding="utf-8"))
    return {name: Pipeline.from_dict(name, body) for name, body in raw["pipelines"].items()}


def stage_applies(when: str | None, brief: dict[str, Any]) -> bool:
    """Tiny, deliberately non-eval condition language.

    Supported forms: `key`, `!key`, `key == value`, `key != value`.
    """
    if not when:
        return True

    expr = when.strip()
    if "!=" in expr:
        key, _, value = expr.partition("!=")
        return _as_text(brief.get(key.strip())) != _normalise(value)
    if "==" in expr:
        key, _, value = expr.partition("==")
        return _as_text(brief.get(key.strip())) == _normalise(value)

    negate = expr.startswith("!")
    key = expr[1:].strip() if negate else expr
    present = _as_text(brief.get(key)) not in ("", "no", "none", "n/a", "not applicable")
    return not present if negate else present


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value).strip().lower()
    return str(value).strip().lower()


def _normalise(value: str) -> str:
    return value.strip().strip("'\"").lower()
