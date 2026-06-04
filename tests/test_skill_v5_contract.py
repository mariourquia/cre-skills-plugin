"""v5 skill-contract enforcement (see CONTRIBUTING.md "v5 Skill Standard").

Enforces the extended skill contract on every ``src/skills/**/SKILL.md`` that
opts in with ``v5_contract: true``. Conformance is keyed on that explicit flag
rather than the version number, because a handful of skills already sit at
``0.2.0`` (and the residential_multifamily subsystem at ``1.0.0-rc1``) for
unrelated reasons. Skills that have not opted in are migrated incrementally,
but ANY skill that carries one of the new frontmatter fields has that field's
grammar checked (so partial adoption cannot smuggle in a malformed field).

Enumerates the filesystem directly (NOT registry.yaml / catalog), so a stale
catalog cannot mask a violation. The conformance test is allowed to find zero
opted-in skills during the incremental migration; the grammar test always runs.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import List

try:
    import yaml
    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "src" / "skills"

_CONFIDENCE = {"confirmed", "estimated", "illustrative"}
_REQUIRED_FIELDS = ("stale_data", "confidence_default", "refusal_trigger")
_REQUIRED_SECTIONS = (
    "## Refusal Behavior",
    "## Confidence and Provenance",
    "## Known Limitations",
)
_WORKSPACE_REQUIRED_SECTIONS = ("## Known Limitations",)
_STATUTE_HORIZON_DAYS = 730  # re-verify regime-encoding skills within 24 months


def _split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return "", text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return "", text
    return text[4:end], text[end + 5:]


def _parse_front(front: str) -> dict:
    if not HAS_YAML:
        return {}
    data = yaml.safe_load(front) or {}
    return data if isinstance(data, dict) else {}


def _skills() -> List[Path]:
    return sorted(SKILLS_ROOT.rglob("SKILL.md"))


def _is_workspace(front: dict) -> bool:
    return front.get("category") == "workspace" or front.get("pack_type") in {"router", "workspace"}


def test_yaml_available():
    assert HAS_YAML, "PyYAML required to validate skill frontmatter"


def test_v5_skills_conform():
    """Every skill that opts in with v5_contract: true satisfies the contract."""
    failures: List[str] = []
    for skill in _skills():
        front_raw, body = _split_frontmatter(skill.read_text(encoding="utf-8"))
        front = _parse_front(front_raw)
        rel = skill.relative_to(REPO_ROOT)
        if front.get("v5_contract") is not True:
            continue
        for f in _REQUIRED_FIELDS:
            if f not in front:
                failures.append(f"{rel}: v5_contract skill missing frontmatter '{f}'")
        sections = _WORKSPACE_REQUIRED_SECTIONS if _is_workspace(front) else _REQUIRED_SECTIONS
        for s in sections:
            if s not in body:
                failures.append(f"{rel}: v5_contract skill missing section '{s}'")
        if front.get("calculator_bridge") and "## Calculator / Tool Bridge" not in body:
            failures.append(f"{rel}: declares calculator_bridge but missing '## Calculator / Tool Bridge'")
    assert not failures, "v5 skill-contract violations:\n  " + "\n  ".join(failures)


def test_new_field_grammar():
    """Grammar of the new fields is checked on ANY skill that carries them."""
    failures: List[str] = []
    for skill in _skills():
        front_raw, _ = _split_frontmatter(skill.read_text(encoding="utf-8"))
        front = _parse_front(front_raw)
        rel = skill.relative_to(REPO_ROOT)
        if "v5_contract" in front and not isinstance(front["v5_contract"], bool):
            failures.append(f"{rel}: v5_contract must be bool")
        # stale_data is the existing corpus convention: a non-empty freshness string.
        if "stale_data" in front and not (isinstance(front["stale_data"], str) and front["stale_data"].strip()):
            failures.append(f"{rel}: stale_data must be a non-empty string")
        if "final_marked" in front and not isinstance(front["final_marked"], bool):
            failures.append(f"{rel}: final_marked must be bool")
        if "confidence_default" in front and front["confidence_default"] not in _CONFIDENCE:
            failures.append(f"{rel}: confidence_default must be one of {sorted(_CONFIDENCE)}")
        cb = front.get("calculator_bridge")
        if cb is not None and not (isinstance(cb, list) and all(isinstance(x, str) for x in cb)):
            failures.append(f"{rel}: calculator_bridge must be a list of strings")
        sr = front.get("statute_review")
        if sr is not None:
            if not isinstance(sr, list) or not sr:
                failures.append(f"{rel}: statute_review must be a non-empty list")
            else:
                for entry in sr:
                    if not isinstance(entry, dict) or "code" not in entry or "last_verified" not in entry:
                        failures.append(f"{rel}: statute_review entry needs 'code' and 'last_verified'")
                        continue
                    try:
                        d = _dt.date.fromisoformat(str(entry["last_verified"]))
                    except ValueError:
                        failures.append(
                            f"{rel}: statute_review last_verified not ISO date: {entry['last_verified']!r}"
                        )
                        continue
                    age = (_dt.date.today() - d).days
                    if age > _STATUTE_HORIZON_DAYS:
                        failures.append(
                            f"{rel}: statute_review '{entry['code']}' last_verified "
                            f"{entry['last_verified']} is {age}d old (> {_STATUTE_HORIZON_DAYS}); re-verify"
                        )
    assert not failures, "v5 field-grammar violations:\n  " + "\n  ".join(failures)
