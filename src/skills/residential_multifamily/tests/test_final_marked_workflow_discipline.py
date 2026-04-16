"""Final-marked workflow discipline.

A final-marked workflow produces a decision-grade deliverable for an audience
outside internal operations (executive committee, investment committee, board,
lender, or LP). These outputs MUST fail closed if a required reference input
is absent — they MUST NOT silently proceed with starter/illustrative data.

This test enforces the invariant at the manifest layer: for every workflow
listed as final-marked in `_core/final_marked_workflows.yaml`, every
`required: true` read in its `reference_manifest.yaml` must declare
`fallback_behavior: refuse`.

If this test fails, either:
  - fix the manifest to declare `refuse` on required reads, or
  - remove the workflow from `final_marked_workflows` (requires change-log
    entry documenting the downgrade), or
  - mark the specific read as `required: false` if it truly is optional.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Set

import yaml

from conftest import SUBSYS


_FM_PATH = SUBSYS / "_core" / "final_marked_workflows.yaml"


def _load_final_marked() -> Dict[str, Any]:
    assert _FM_PATH.exists(), f"missing governance file {_FM_PATH}"
    with _FM_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def test_final_marked_workflows_file_exists_and_validates() -> None:
    data = _load_final_marked()
    assert data.get("schema_version"), "schema_version required"
    fm = data.get("final_marked_workflows") or {}
    assert isinstance(fm, dict) and fm, "final_marked_workflows must be a non-empty mapping"
    for slug, spec in fm.items():
        assert isinstance(spec, dict), f"{slug}: entry must be a mapping"
        audience = spec.get("audience")
        assert isinstance(audience, list) and audience, (
            f"{slug}: audience must be a non-empty list"
        )
        reason = spec.get("downgrade_forbidden_reason")
        assert isinstance(reason, str) and reason.strip(), (
            f"{slug}: downgrade_forbidden_reason must be a non-empty string"
        )


def test_final_marked_workflows_exist_on_disk() -> None:
    data = _load_final_marked()
    fm_slugs: Set[str] = set((data.get("final_marked_workflows") or {}).keys())
    missing: List[str] = []
    for slug in sorted(fm_slugs):
        wf_dir = SUBSYS / "workflows" / slug
        if not (wf_dir / "SKILL.md").exists():
            missing.append(slug)
    assert not missing, (
        f"final-marked workflows have no workflow directory: {missing}"
    )


def test_final_marked_workflows_fail_closed_on_required_reads() -> None:
    data = _load_final_marked()
    fm_slugs: Set[str] = set((data.get("final_marked_workflows") or {}).keys())

    violations: List[str] = []
    for slug in sorted(fm_slugs):
        rm_path = SUBSYS / "workflows" / slug / "reference_manifest.yaml"
        assert rm_path.exists(), f"final-marked workflow {slug!r} has no manifest"
        with rm_path.open("r", encoding="utf-8") as f:
            rm = yaml.safe_load(f) or {}
        for entry in rm.get("reads") or []:
            if not entry.get("required", True):
                continue
            fb = entry.get("fallback_behavior")
            if fb != "refuse":
                violations.append(
                    f"  {slug} -> {entry.get('path')}: required=true but fallback_behavior={fb!r} "
                    f"(must be 'refuse' for final-marked workflows)"
                )

    assert not violations, (
        "Final-marked workflow(s) have required reads that do not fail closed:\n"
        + "\n".join(violations)
        + "\n\nFix: set fallback_behavior: refuse on the entry, or mark it required: false, "
        + "or downgrade the workflow from final_marked_workflows with a change-log entry."
    )


def test_final_marked_and_operating_are_disjoint() -> None:
    data = _load_final_marked()
    fm_slugs: Set[str] = set((data.get("final_marked_workflows") or {}).keys())
    og_slugs: Set[str] = set(data.get("operating_grade_workflows") or [])
    sg_slugs: Set[str] = set(data.get("setup_grade_workflows") or [])

    overlap_fm_og = fm_slugs & og_slugs
    assert not overlap_fm_og, (
        f"workflow appears in both final_marked and operating_grade: {sorted(overlap_fm_og)}"
    )
    overlap_fm_sg = fm_slugs & sg_slugs
    assert not overlap_fm_sg, (
        f"workflow appears in both final_marked and setup_grade: {sorted(overlap_fm_sg)}"
    )
    overlap_og_sg = og_slugs & sg_slugs
    assert not overlap_og_sg, (
        f"workflow appears in both operating_grade and setup_grade: {sorted(overlap_og_sg)}"
    )


def test_classification_covers_all_canonical_workflows() -> None:
    """Every canonical workflow must be classified as exactly one of:
    final_marked, operating_grade, or setup_grade. This prevents a new
    workflow from silently entering the repo without a grade decision.
    """
    data = _load_final_marked()
    classified: Set[str] = set()
    classified.update((data.get("final_marked_workflows") or {}).keys())
    classified.update(data.get("operating_grade_workflows") or [])
    classified.update(data.get("setup_grade_workflows") or [])

    canonical: Set[str] = set()
    wf_dir = SUBSYS / "workflows"
    for child in sorted(wf_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        if (child / "SKILL.md").exists():
            canonical.add(child.name)

    unclassified = sorted(canonical - classified)
    assert not unclassified, (
        f"canonical workflows not classified in final_marked_workflows.yaml: {unclassified}. "
        "Add each to final_marked_workflows, operating_grade_workflows, or setup_grade_workflows."
    )

    extra = sorted(classified - canonical)
    assert not extra, (
        f"final_marked_workflows.yaml lists non-existent workflows: {extra}"
    )
