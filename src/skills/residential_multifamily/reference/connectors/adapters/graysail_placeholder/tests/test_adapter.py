"""GraySail placeholder: classification-path conformance tests."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))


def test_graysail_required_placeholder_files_present():
    required = [
        "manifest.yaml",
        "README.md",
        "classification_worksheet.md",
        "bounded_assumptions.yaml",
        "provisional_source_contract.yaml",
        "workflow_relevance_map.yaml",
        "source_registry_entry.yaml",
    ]
    for name in required:
        assert (ADAPTER_DIR / name).exists(), f"missing required file: {name}"


def test_graysail_status_is_placeholder():
    src = ADAPTER_DIR / "source_registry_entry.yaml"
    data = yaml.safe_load(src.read_text())
    rec = data["records"][0]
    assert rec["status"] == "planned", "GraySail must remain planned until classified"
    assert rec["credential_method"] == "none"


def test_graysail_bounded_assumptions_carry_required_fields():
    src = ADAPTER_DIR / "bounded_assumptions.yaml"
    data = yaml.safe_load(src.read_text())
    if isinstance(data, dict) and "assumptions" in data:
        for a in data["assumptions"]:
            for key in ("assumption", "confidence"):
                assert key in a, f"bounded_assumption missing {key}"


def test_graysail_no_workflow_treats_it_as_primary():
    src = ADAPTER_DIR / "workflow_relevance_map.yaml"
    data = yaml.safe_load(src.read_text())
    text = src.read_text()
    assert "primary" not in text or "blocked_until_classified" in text, (
        "GraySail must not be primary in any workflow while placeholder"
    )
