"""Executive output contract enforcement.

See `_core/executive_output_contract.md`. Every final-marked workflow
must reference the contract in its SKILL.md so implementers can find
the verdict-first + source-class rubric. At least one worked example
must demonstrate the pattern end-to-end so the contract has a
concrete, copyable shape.

Failing this test means a decision-grade workflow could produce
buried-verdict output or unlabeled numeric cells — and the rubric
would be invisible to the next person editing it.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from conftest import SUBSYS


_FM_PATH = SUBSYS / "_core" / "final_marked_workflows.yaml"
_CONTRACT_PATH = SUBSYS / "_core" / "executive_output_contract.md"
_CONTRACT_REF_TOKEN = "_core/executive_output_contract.md"

_SOURCE_CLASS_TAGS = ("[operator]", "[derived]", "[benchmark]", "[overlay]", "[placeholder]")


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _final_marked_slugs() -> List[str]:
    return list((_load_yaml(_FM_PATH).get("final_marked_workflows") or {}).keys())


def test_contract_doc_exists() -> None:
    assert _CONTRACT_PATH.exists(), (
        f"{_CONTRACT_PATH.relative_to(SUBSYS)} is missing; every final-marked "
        f"workflow SKILL.md references it."
    )
    body = _CONTRACT_PATH.read_text(encoding="utf-8")
    for rule_marker in ("Verdict-first", "Source-class", "Refusal"):
        assert rule_marker in body, (
            f"executive_output_contract.md missing expected section marker "
            f"{rule_marker!r} — the contract has three rules and this test "
            f"ensures all three stay present."
        )


def test_final_marked_skill_references_contract() -> None:
    """Every final-marked SKILL.md must reference the contract doc."""
    failures: List[str] = []
    for slug in _final_marked_slugs():
        skill = SUBSYS / "workflows" / slug / "SKILL.md"
        if not skill.exists():
            failures.append(f"{slug}: SKILL.md missing")
            continue
        body = skill.read_text(encoding="utf-8")
        if _CONTRACT_REF_TOKEN not in body:
            failures.append(
                f"{slug}: SKILL.md does not reference {_CONTRACT_REF_TOKEN}"
            )
    assert not failures, "\n  ".join(failures)


def test_at_least_one_example_demonstrates_source_classes() -> None:
    """At least one example file in a final-marked workflow must carry the
    source-class tags so the rubric has a concrete, copyable shape."""
    demonstrated = 0
    for slug in _final_marked_slugs():
        ex_dir = SUBSYS / "workflows" / slug / "examples"
        if not ex_dir.exists():
            continue
        for ex_file in ex_dir.rglob("*.md"):
            body = ex_file.read_text(encoding="utf-8")
            if all(tag in body for tag in _SOURCE_CLASS_TAGS):
                demonstrated += 1
    assert demonstrated >= 1, (
        "No final-marked workflow example demonstrates the full source-class "
        "tag set " + str(_SOURCE_CLASS_TAGS) + ". Executive output contract "
        "requires at least one worked example so the rubric has a concrete "
        "reference shape. See executive_operating_summary_generation/examples/"
        "ex01_*.md for the canonical pattern."
    )


def test_example_demonstrates_verdict_first() -> None:
    """The canonical example must lead with a verdict block."""
    canonical = (
        SUBSYS
        / "workflows"
        / "executive_operating_summary_generation"
        / "examples"
        / "ex01_executive_operating_summary_generation.md"
    )
    body = canonical.read_text(encoding="utf-8")
    # Verdict section, recommendation + confidence + materiality + next action
    required_markers = (
        "Verdict",
        "Recommendation",
        "Confidence",
        "Materiality",
        "Next action",
    )
    missing = [m for m in required_markers if m not in body]
    assert not missing, (
        f"canonical executive output example missing verdict markers: {missing}"
    )
