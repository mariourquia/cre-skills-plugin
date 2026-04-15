"""Runbook structural tests.

Every operational runbook under reference/connectors/runbooks/ must include
the canonical 9 sections so on-call operators have predictable structure.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

import pytest


RUNBOOKS_ROOT = Path(__file__).resolve().parents[1] / "reference" / "connectors" / "runbooks"
SUBSYS = RUNBOOKS_ROOT.parents[2]

REQUIRED_SECTIONS = [
    "Trigger",
    "Symptoms",
    "Likely causes",
    "Immediate actions",
    "Escalation path",
    "Affected workflows",
    "Recovery steps",
    "Verification steps",
    "Post-incident review",
]

EXPECTED_RUNBOOKS = [
    "new_source_onboarding.md",
    "source_schema_change.md",
    "missing_file_handling.md",
    "stale_feed_handling.md",
    "property_crosswalk_issue.md",
    "unmapped_account_handling.md",
    "benchmark_refresh.md",
    "failed_normalization_triage.md",
    "exception_queue_review.md",
    "manual_override_approval.md",
    "cutover_manual_to_system.md",
    "connector_deprecation.md",
    "fair_housing_sensitive_flag.md",
    "financial_control_gate_breach.md",
    "schema_drift_escalation.md",
    "reference_rollback.md",
]


def test_runbooks_family_present():
    missing = [
        str((RUNBOOKS_ROOT / name).relative_to(SUBSYS))
        for name in ["README.md"] + EXPECTED_RUNBOOKS
        if not (RUNBOOKS_ROOT / name).exists()
    ]
    assert not missing, "runbook family missing files:\n  - " + "\n  - ".join(missing)


def test_runbooks_have_canonical_sections():
    failures: List[str] = []
    for name in EXPECTED_RUNBOOKS:
        path = RUNBOOKS_ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        missing = [s for s in REQUIRED_SECTIONS if s.lower() not in text]
        if missing:
            failures.append(f"{path.relative_to(SUBSYS)}: missing sections {missing}")
    assert not failures, "runbook structure validation failed:\n  - " + "\n  - ".join(failures)


def test_runbooks_are_nonempty():
    failures: List[str] = []
    for name in EXPECTED_RUNBOOKS:
        path = RUNBOOKS_ROOT / name
        if not path.exists():
            continue
        size = path.stat().st_size
        if size < 800:
            failures.append(f"{path.relative_to(SUBSYS)}: suspiciously short ({size} bytes)")
    assert not failures, "runbook length check failed:\n  - " + "\n  - ".join(failures)
