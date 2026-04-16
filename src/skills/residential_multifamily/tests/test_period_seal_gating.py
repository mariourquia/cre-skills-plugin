"""Period-seal gating for period-grade workflows.

A period-grade workflow is one whose output represents a period-level
financial picture (monthly operating review, reforecast, quarterly LP
letter, executive summary, budget build). These workflows MUST declare a
`required_period_seal` block in their reference_manifest.yaml that pins
the minimum acceptable close_status of the underlying GL.

Contract surfaces enforced here:

  1. Every slug in `_core/final_marked_workflows.yaml#period_grade_workflows`
     has a canonical workflow directory on disk with a reference_manifest.
  2. That manifest declares `required_period_seal` with minimum_close_status
     no less permissive than the floor declared in the registry, and with
     as_of_required: true.
  3. When the registry requires close_lock_timestamp, the manifest says so.
  4. When the registry declares required_version_fields (e.g. budget_version
     for reforecast), the manifest carries the same field list.
  5. Nothing outside period_grade_workflows declares required_period_seal by
     accident — that would silently impose a gate on non-period workflows
     and hide the declaration from reviewers.

Failing this test means a period-grade workflow could accept draft-GL
data and silently produce variance numbers that misrepresent operating
reality to the audience.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from conftest import SUBSYS


_FM_PATH = SUBSYS / "_core" / "final_marked_workflows.yaml"
_SCHEMA_PATH = SUBSYS / "_core" / "schemas" / "period_seal.yaml"

_CLOSE_STATUS_ORDER = ("draft", "soft_close", "hard_close", "locked")


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _close_status_rank(status: str) -> int:
    return _CLOSE_STATUS_ORDER.index(status)


def _period_registry() -> Dict[str, Dict[str, Any]]:
    return _load_yaml(_FM_PATH).get("period_grade_workflows") or {}


def _workflow_manifest(slug: str) -> Dict[str, Any]:
    return _load_yaml(SUBSYS / "workflows" / slug / "reference_manifest.yaml")


def test_period_grade_registry_non_empty() -> None:
    registry = _period_registry()
    assert registry, (
        "final_marked_workflows.yaml#period_grade_workflows is empty — "
        "monthly and quarterly review flows must be enumerated so the "
        "period-seal gate has something to enforce."
    )


def test_schema_defines_close_status_order() -> None:
    schema = _load_yaml(_SCHEMA_PATH)
    order = schema.get("close_status_order")
    assert order == list(_CLOSE_STATUS_ORDER), (
        "period_seal.yaml#close_status_order must match the test harness "
        f"ordering {_CLOSE_STATUS_ORDER}; got {order!r}."
    )


def test_every_period_grade_workflow_has_required_period_seal() -> None:
    registry = _period_registry()
    failures: List[str] = []
    for slug, rules in registry.items():
        wf_dir = SUBSYS / "workflows" / slug
        manifest_path = wf_dir / "reference_manifest.yaml"
        if not manifest_path.exists():
            failures.append(f"{slug}: workflow directory or manifest missing")
            continue
        manifest = _workflow_manifest(slug)
        seal = manifest.get("required_period_seal")
        if not seal:
            failures.append(f"{slug}: manifest has no required_period_seal block")
            continue
        min_status = seal.get("minimum_close_status")
        if min_status not in _CLOSE_STATUS_ORDER:
            failures.append(
                f"{slug}: minimum_close_status {min_status!r} is not a valid "
                f"close state"
            )
            continue
        floor = rules["minimum_close_status"]
        if _close_status_rank(min_status) < _close_status_rank(floor):
            failures.append(
                f"{slug}: manifest floor {min_status!r} is below registry "
                f"floor {floor!r}"
            )
        if not seal.get("as_of_required"):
            failures.append(f"{slug}: as_of_required must be true")
        if rules.get("requires_close_lock_timestamp") and not seal.get(
            "requires_close_lock_timestamp"
        ):
            failures.append(
                f"{slug}: registry requires close_lock_timestamp; manifest does not"
            )
        reg_versions = rules.get("required_version_fields") or []
        man_versions = seal.get("required_version_fields") or []
        missing_versions = [v for v in reg_versions if v not in man_versions]
        if missing_versions:
            failures.append(
                f"{slug}: manifest missing required_version_fields "
                f"{missing_versions}"
            )
    assert not failures, (
        "Period-seal gating violations:\n  " + "\n  ".join(failures)
    )


def test_no_required_period_seal_outside_registry() -> None:
    registry = set(_period_registry().keys())
    strays: List[str] = []
    for wf_dir in sorted((SUBSYS / "workflows").iterdir()):
        if not wf_dir.is_dir() or wf_dir.name.startswith("_"):
            continue
        manifest = wf_dir / "reference_manifest.yaml"
        if not manifest.exists():
            continue
        data = _load_yaml(manifest)
        if data.get("required_period_seal") and wf_dir.name not in registry:
            strays.append(wf_dir.name)
    assert not strays, (
        "Workflows declare required_period_seal but are not in the "
        "period_grade_workflows registry — add them to the registry so the "
        "gate is visible to reviewers:\n  " + "\n  ".join(strays)
    )


def test_hard_close_workflows_require_close_lock_timestamp() -> None:
    """Consistency: hard_close or stricter implies close_lock_timestamp."""
    registry = _period_registry()
    failures: List[str] = []
    for slug, rules in registry.items():
        floor = rules["minimum_close_status"]
        if _close_status_rank(floor) >= _close_status_rank("hard_close"):
            if not rules.get("requires_close_lock_timestamp"):
                failures.append(
                    f"{slug}: minimum_close_status {floor!r} >= hard_close but "
                    f"requires_close_lock_timestamp is not set — every "
                    f"hard-close gate must tie to an audit timestamp."
                )
    assert not failures, "\n".join(failures)
