"""Wave-4 stack-specific conformance tests.

Validates that every wave-4 vendor adapter is present, conforms to required
file structure, and is registered in the master source_registry.yaml. Also
validates the cross-cutting wave-4 documents are present and well-formed.

These tests do NOT cover canonical regression — those live in
test_canonical_regression.py (skill-level) and dedicated wave-3 tests.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
ADAPTERS_DIR = SKILL_ROOT / "reference" / "connectors" / "adapters"
SOURCE_REGISTRY = (
    SKILL_ROOT
    / "reference"
    / "connectors"
    / "source_registry"
    / "source_registry.yaml"
)
STACK_WAVE4_DIR = SKILL_ROOT / "reference" / "connectors" / "_core" / "stack_wave4"
MASTER_DATA_DIR = SKILL_ROOT / "reference" / "connectors" / "master_data"


WAVE_4_ADAPTERS = [
    "appfolio_pms",
    "sage_intacct_gl",
    "procore_construction",
    "dealpath_deal_pipeline",
    "excel_market_surveys",
    "manual_sources_expanded",
    "graysail_placeholder",
]


WAVE_4_SOURCE_IDS = [
    "appfolio_prod",
    "sage_intacct_prod",
    "procore_prod",
    "dealpath_prod",
    "excel_rent_comp_weekly",
    "excel_concession_tracker_monthly",
    "excel_capex_cost_library",
    "excel_staffing_benchmark_quarterly",
    "excel_labor_rate_quarterly",
    "operator_monthly_report_inbox",
    "tpm_data_submission_drive",
    "bid_tab_workbook_drive",
    "approval_matrix_workbook",
    "graysail_pending_classification",
]


@pytest.fixture(scope="module")
def source_registry():
    return yaml.safe_load(SOURCE_REGISTRY.read_text())


@pytest.mark.parametrize("adapter", WAVE_4_ADAPTERS)
def test_wave4_adapter_directory_exists(adapter):
    adapter_dir = ADAPTERS_DIR / adapter
    assert adapter_dir.is_dir(), f"adapter directory missing: {adapter}"


@pytest.mark.parametrize("adapter", WAVE_4_ADAPTERS)
def test_wave4_adapter_has_manifest(adapter):
    manifest = ADAPTERS_DIR / adapter / "manifest.yaml"
    assert manifest.exists(), f"manifest.yaml missing: {adapter}"
    data = yaml.safe_load(manifest.read_text())
    assert data.get("rollout_wave", "").startswith("wave_4")


@pytest.mark.parametrize("adapter", WAVE_4_ADAPTERS)
def test_wave4_adapter_has_readme(adapter):
    readme = ADAPTERS_DIR / adapter / "README.md"
    assert readme.exists(), f"README.md missing: {adapter}"


@pytest.mark.parametrize("adapter", WAVE_4_ADAPTERS)
def test_wave4_adapter_has_source_registry_entry(adapter):
    fragment = ADAPTERS_DIR / adapter / "source_registry_entry.yaml"
    assert fragment.exists(), f"source_registry_entry.yaml missing: {adapter}"
    data = yaml.safe_load(fragment.read_text())
    assert "records" in data and len(data["records"]) >= 1


@pytest.mark.parametrize("adapter", WAVE_4_ADAPTERS)
def test_wave4_adapter_has_tests_dir(adapter):
    tests_dir = ADAPTERS_DIR / adapter / "tests"
    assert tests_dir.is_dir(), f"tests/ missing: {adapter}"
    test_files = list(tests_dir.glob("test_*.py"))
    assert test_files, f"no test_*.py files in: {adapter}/tests/"


@pytest.mark.parametrize("source_id", WAVE_4_SOURCE_IDS)
def test_wave4_source_in_master_registry(source_id, source_registry):
    ids = {r["source_id"] for r in source_registry["records"]}
    assert source_id in ids, f"wave-4 source not merged into master registry: {source_id}"


@pytest.mark.parametrize("source_id", WAVE_4_SOURCE_IDS)
def test_wave4_source_carries_wave4_tag(source_id, source_registry):
    rec = next(r for r in source_registry["records"] if r["source_id"] == source_id)
    assert rec["rollout_wave"] == "wave_4"


def test_wave4_cross_cutting_docs_present():
    expected = [
        "source_of_truth_matrix.md",
        "lifecycle_handoffs.md",
        "stack_reconciliation_matrix.md",
        "stack_rollout_wave4.md",
        "third_party_manager_oversight.md",
        "stack_test_taxonomy.md",
        "open_questions_and_risks.md",
    ]
    for name in expected:
        assert (STACK_WAVE4_DIR / name).exists(), f"missing cross-cutting doc: {name}"


def test_wave4_new_crosswalk_files_present():
    expected = [
        "asset_crosswalk.yaml",
        "market_crosswalk.yaml",
        "submarket_crosswalk.yaml",
    ]
    for name in expected:
        path = MASTER_DATA_DIR / name
        assert path.exists(), f"missing wave-4 crosswalk file: {name}"
        data = yaml.safe_load(path.read_text())
        assert "rows" in data, f"{name} missing 'rows' key"


def test_graysail_status_remains_planned(source_registry):
    rec = next(
        r for r in source_registry["records"] if r["source_id"] == "graysail_pending_classification"
    )
    assert rec["status"] == "planned", "GraySail must remain planned until classified"


def test_wave4_pii_classifications_valid(source_registry):
    valid = {"none", "low", "moderate", "high", "restricted"}
    for source_id in WAVE_4_SOURCE_IDS:
        rec = next(r for r in source_registry["records"] if r["source_id"] == source_id)
        assert rec["pii_classification"] in valid
        assert rec["financial_sensitivity"] in valid
        assert rec["legal_sensitivity"] in valid


def test_wave4_no_credential_strings(source_registry):
    """No actual credential values in wave-4 entries."""
    forbidden_substrings = ["password", "secret", "api_key=", "bearer "]
    for source_id in WAVE_4_SOURCE_IDS:
        rec = next(r for r in source_registry["records"] if r["source_id"] == source_id)
        notes = rec.get("notes", "") or ""
        for sub in forbidden_substrings:
            assert sub.lower() not in notes.lower(), f"forbidden substring in {source_id}: {sub}"


def test_deal_pipeline_domain_exists():
    domain_dir = SKILL_ROOT / "reference" / "connectors" / "deal_pipeline"
    assert domain_dir.is_dir(), "deal_pipeline source domain missing"
    assert (domain_dir / "manifest.yaml").exists()
    assert (domain_dir / "schema.yaml").exists()
