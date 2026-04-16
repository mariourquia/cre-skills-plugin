"""Integration-layer presence tests.

Top-level smoke coverage that the integration layer exposes the documented
subdirectories and key files. Guards against accidental deletion or rename
during refactoring.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

import pytest


SUBSYS = Path(__file__).resolve().parents[1]
ROOT = SUBSYS / "reference" / "connectors"


EXPECTED_SUBDIRS = [
    "_core",
    "_core/security",
    "_schema",
    "adapters",
    "ap",
    "construction",
    "crm",
    "gl",
    "hr_payroll",
    "manual_uploads",
    "market_data",
    "master_data",
    "monitoring",
    "pms",
    "qa",
    "rollout",
    "runbooks",
    "source_registry",
]

EXPECTED_CORE_FILES = [
    "_core/layer_design.md",
    "_core/lineage.md",
    "_core/normalization_patterns.md",
    "_core/field_mapping_template.md",
    "_core/raw_to_normalized_design.md",
    "_core/derived_dependencies.md",
    "_core/workflow_activation_map.yaml",
    "_core/workflow_activation_map.md",
    "_core/third_party_manager_oversight.md",
    "_core/exception_taxonomy.md",
    "_core/lineage_manifest.schema.yaml",
    "_core/mapping_override_log.schema.yaml",
    "_core/benchmark_update_log.schema.yaml",
    "_core/config_overlay_interaction.md",
]

EXPECTED_MONITORING_FILES = [
    "monitoring/alert_policies.yaml",
    "monitoring/exception_routing.yaml",
    "monitoring/observability_events.yaml",
    "monitoring/slo_definitions.md",
    "monitoring/alert_channel_design.md",
    "monitoring/escalation_matrix.md",
]

EXPECTED_ROLLOUT_FILES = [
    "rollout/rollout_waves.md",
    "rollout/minimum_viable_data.md",
    "rollout/pilot_property_guidance.md",
    "rollout/go_live_checklist.md",
    "rollout/rollback_plan.md",
    "rollout/success_metrics.md",
    "rollout/post_launch_monitoring_cadence.md",
    "rollout/cutover_procedures.md",
    "rollout/pilot_to_production_gate.md",
]


def test_integration_subdirs_present():
    missing = [
        s for s in EXPECTED_SUBDIRS
        if not (ROOT / s).is_dir()
    ]
    assert not missing, "integration-layer subdirs missing:\n  - " + "\n  - ".join(missing)


def test_integration_core_files_present():
    missing = [
        f for f in EXPECTED_CORE_FILES
        if not (ROOT / f).exists()
    ]
    assert not missing, "integration-layer _core files missing:\n  - " + "\n  - ".join(missing)


def test_integration_monitoring_files_present():
    missing = [
        f for f in EXPECTED_MONITORING_FILES
        if not (ROOT / f).exists()
    ]
    assert not missing, "monitoring files missing:\n  - " + "\n  - ".join(missing)


def test_integration_rollout_files_present():
    missing = [
        f for f in EXPECTED_ROLLOUT_FILES
        if not (ROOT / f).exists()
    ]
    assert not missing, "rollout files missing:\n  - " + "\n  - ".join(missing)


def test_alert_policies_nonempty_list():
    import yaml
    doc = yaml.safe_load((ROOT / "monitoring" / "alert_policies.yaml").read_text())
    assert isinstance(doc, dict), "alert_policies.yaml must parse to mapping"
    policies = doc.get("policies") or doc.get("alerts") or doc.get("alert_policies") or []
    if isinstance(policies, dict):
        policies = list(policies.values())
    assert isinstance(policies, list) and policies, "alert_policies.yaml must declare policies"
