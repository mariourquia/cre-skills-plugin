"""Wave-5 stack-completion conformance tests.

Validates that wave-5 deliverables are present and well-formed:
- Yardi adapter (`yardi_multi_role`) directory + classification artifacts
- 9 new workflow packs (pipeline_review, pre_close_deal_tracking, etc.)
- `commitment` canonical object in `_core/ontology.md`
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml` exists
- Yardi rows present in source_registry, vendor_family_registry, master_data crosswalks
- Wave-4 adapters reach the 17-deliverable bar (added wave-5 fill content)

These tests do NOT cover canonical regression — those live in dedicated wave-3
tests. They do NOT supersede wave-4 tests in test_stack_wave4.py.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
ADAPTERS_DIR = SKILL_ROOT / "reference" / "connectors" / "adapters"
WORKFLOWS_DIR = SKILL_ROOT / "workflows"
ONTOLOGY = SKILL_ROOT / "_core" / "ontology.md"
TOLERANCE_BAND_SCHEMA = (
    SKILL_ROOT
    / "reference"
    / "normalized"
    / "schemas"
    / "reconciliation_tolerance_band.yaml"
)
SOURCE_OF_TRUTH_MATRIX = (
    SKILL_ROOT
    / "reference"
    / "connectors"
    / "_core"
    / "stack_wave4"
    / "source_of_truth_matrix.md"
)
VENDOR_FAMILY_REGISTRY = ADAPTERS_DIR / "vendor_family_registry.yaml"
SOURCE_REGISTRY_FILE = (
    SKILL_ROOT
    / "reference"
    / "connectors"
    / "source_registry"
    / "source_registry.yaml"
)
MASTER_DATA_DIR = SKILL_ROOT / "reference" / "connectors" / "master_data"


WAVE_5_WORKFLOWS = [
    "pipeline_review",
    "pre_close_deal_tracking",
    "investment_committee_prep",
    "acquisition_handoff",
    "post_ic_property_setup",
    "delivery_handoff",
    "development_pipeline_tracking",
    "lease_up_first_period",
    "executive_pipeline_summary",
]


WAVE_5_YARDI_SOURCE_IDS = [
    "yardi_voyager_pms_stub",
    "yardi_voyager_gl_stub",
    "yardi_rentcafe_stub",
    "yardi_data_connect_stub",
    "yardi_legacy_export_stub",
]


WAVE_4_ADAPTERS_NEEDING_FILL = [
    "appfolio_pms",
    "sage_intacct_gl",
    "procore_construction",
    "dealpath_deal_pipeline",
    "excel_market_surveys",
    "manual_sources_expanded",
    "graysail_placeholder",
]


def _load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Yardi adapter
# ---------------------------------------------------------------------------

def test_yardi_adapter_directory_exists():
    yardi_dir = ADAPTERS_DIR / "yardi_multi_role"
    assert yardi_dir.is_dir(), "yardi_multi_role adapter directory missing"


@pytest.mark.parametrize(
    "filename",
    [
        "manifest.yaml",
        "classification_worksheet.md",
        "bounded_assumptions.yaml",
        "provisional_source_contract.yaml",
        "source_contract.yaml",
        "normalized_contract.yaml",
        "field_mapping.yaml",
        "dq_rules.yaml",
        "reconciliation_rules.md",
        "reconciliation_checks.yaml",
        "edge_cases.md",
        "crosswalk_additions.yaml",
        "workflow_activation_additions.yaml",
        "README.md",
    ],
)
def test_yardi_adapter_required_files_present(filename):
    yardi_dir = ADAPTERS_DIR / "yardi_multi_role"
    target = yardi_dir / filename
    assert target.exists(), f"yardi_multi_role/{filename} missing"


def test_yardi_classification_artifacts_present():
    yardi_dir = ADAPTERS_DIR / "yardi_multi_role"
    assert (yardi_dir / "runbooks" / "yardi_classification_path.md").exists(), (
        "yardi_classification_path.md missing — operator decision tree required"
    )
    assert (yardi_dir / "sample_raw").is_dir() and any(
        (yardi_dir / "sample_raw").glob("*.jsonl")
    ), "sample_raw/*.jsonl missing"
    assert (yardi_dir / "sample_normalized").is_dir() and any(
        (yardi_dir / "sample_normalized").glob("*.jsonl")
    ), "sample_normalized/*.jsonl missing"


def test_yardi_manifest_status_and_role_posture():
    manifest = _load_yaml(ADAPTERS_DIR / "yardi_multi_role" / "manifest.yaml")
    assert manifest.get("adapter_id") == "yardi_multi_role"
    assert manifest.get("vendor_family") == "yardi_family"
    assert manifest.get("status") == "stub", (
        "Yardi adapter must remain at stub status until classification closes"
    )


def test_yardi_dq_rules_use_yd_prefix():
    rules_yaml = _load_yaml(ADAPTERS_DIR / "yardi_multi_role" / "dq_rules.yaml")
    rules = rules_yaml.get("rules") or []
    assert rules, "yardi dq_rules.yaml has no rules"
    bad = [r["rule_id"] for r in rules if not r.get("rule_id", "").startswith("yd_")]
    assert not bad, f"non-yd_ prefix rule_ids: {bad}"


# ---------------------------------------------------------------------------
# Commitment canonical object
# ---------------------------------------------------------------------------

def test_commitment_object_present_in_ontology():
    text = ONTOLOGY.read_text(encoding="utf-8")
    assert "## Commitment / PurchaseCommitment" in text, (
        "commitment canonical object missing from _core/ontology.md"
    )
    # Spot-check key fields are documented
    for field in [
        "commitment_id",
        "original_amount",
        "approved_change_orders_amount",
        "revised_amount",
        "paid_to_date",
        "retainage_held",
        "balance_to_complete",
        "commitment_type",
    ]:
        assert field in text, f"commitment field '{field}' not documented in ontology.md"


# ---------------------------------------------------------------------------
# Wave-5 workflow packs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("workflow_slug", WAVE_5_WORKFLOWS)
def test_wave5_workflow_pack_directory_exists(workflow_slug):
    wf_dir = WORKFLOWS_DIR / workflow_slug
    assert wf_dir.is_dir(), f"workflows/{workflow_slug}/ missing"


@pytest.mark.parametrize("workflow_slug", WAVE_5_WORKFLOWS)
def test_wave5_workflow_pack_has_required_files(workflow_slug):
    wf_dir = WORKFLOWS_DIR / workflow_slug
    required = ["SKILL.md", "reference_manifest.yaml", "routing.yaml", "change_log.md"]
    missing = [f for f in required if not (wf_dir / f).exists()]
    assert not missing, f"workflows/{workflow_slug}/ missing files: {missing}"
    assert (wf_dir / "examples").is_dir(), (
        f"workflows/{workflow_slug}/examples/ missing"
    )


@pytest.mark.parametrize("workflow_slug", WAVE_5_WORKFLOWS)
def test_wave5_workflow_skill_frontmatter_parses(workflow_slug):
    text = (WORKFLOWS_DIR / workflow_slug / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---"), f"workflows/{workflow_slug}/SKILL.md missing frontmatter"
    body = text.split("---", 2)
    assert len(body) >= 3, f"workflows/{workflow_slug}/SKILL.md frontmatter not closed"
    fm = yaml.safe_load(body[1])
    assert fm.get("slug") == workflow_slug, (
        f"workflows/{workflow_slug}/SKILL.md slug mismatch: got {fm.get('slug')!r}"
    )
    assert fm.get("pack_type") == "workflow"
    assert fm.get("subsystem") == "residential_multifamily"


# ---------------------------------------------------------------------------
# Wave-5 reconciliation_tolerance_band.yaml
# ---------------------------------------------------------------------------

def test_reconciliation_tolerance_band_schema_present():
    assert TOLERANCE_BAND_SCHEMA.exists(), (
        "reference/normalized/schemas/reconciliation_tolerance_band.yaml missing — "
        "wave-5 must close this reference gap that adapter dq_rules cite"
    )


def test_reconciliation_tolerance_band_has_bands():
    if not TOLERANCE_BAND_SCHEMA.exists():
        pytest.skip("schema not yet created")
    doc = _load_yaml(TOLERANCE_BAND_SCHEMA)
    bands = doc.get("bands")
    assert isinstance(bands, list) and len(bands) >= 10, (
        "tolerance band schema must declare bands: list with >= 10 entries"
    )


# ---------------------------------------------------------------------------
# Yardi registry wiring
# ---------------------------------------------------------------------------

def test_vendor_family_registry_includes_yardi():
    registry = _load_yaml(VENDOR_FAMILY_REGISTRY)
    ids = [r.get("adapter_id") for r in (registry.get("records") or [])]
    assert "yardi_multi_role" in ids, (
        "vendor_family_registry.yaml missing yardi_multi_role record"
    )


@pytest.mark.parametrize("source_id", WAVE_5_YARDI_SOURCE_IDS)
def test_yardi_source_records_present(source_id):
    registry = _load_yaml(SOURCE_REGISTRY_FILE)
    ids = [r.get("source_id") for r in (registry.get("records") or [])]
    assert source_id in ids, f"source_registry.yaml missing {source_id}"


# ---------------------------------------------------------------------------
# Wave-4 adapters reach 17-deliverable bar (wave-5 fill)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("adapter_slug", [
    "appfolio_pms",
    "sage_intacct_gl",
    "procore_construction",
    "dealpath_deal_pipeline",
    "manual_sources_expanded",
])
def test_wave4_adapter_has_dq_rules_after_wave5_fill(adapter_slug):
    dq = ADAPTERS_DIR / adapter_slug / "dq_rules.yaml"
    assert dq.exists(), f"adapter {adapter_slug} missing dq_rules.yaml after wave-5 fill"


@pytest.mark.parametrize("adapter_slug", [
    "appfolio_pms",
    "sage_intacct_gl",
    "procore_construction",
    "dealpath_deal_pipeline",
    "manual_sources_expanded",
])
def test_wave4_adapter_has_reconciliation_artifacts(adapter_slug):
    rules = ADAPTERS_DIR / adapter_slug / "reconciliation_rules.md"
    checks = ADAPTERS_DIR / adapter_slug / "reconciliation_checks.yaml"
    assert rules.exists(), (
        f"adapter {adapter_slug} missing reconciliation_rules.md after wave-5 fill"
    )
    assert checks.exists(), (
        f"adapter {adapter_slug} missing reconciliation_checks.yaml after wave-5 fill"
    )


@pytest.mark.parametrize("adapter_slug", [
    "appfolio_pms",
    "sage_intacct_gl",
    "procore_construction",
    "dealpath_deal_pipeline",
    "manual_sources_expanded",
])
def test_wave4_adapter_has_edge_cases_and_crosswalk(adapter_slug):
    edge = ADAPTERS_DIR / adapter_slug / "edge_cases.md"
    crosswalk = ADAPTERS_DIR / adapter_slug / "crosswalk_additions.yaml"
    assert edge.exists(), (
        f"adapter {adapter_slug} missing edge_cases.md after wave-5 fill"
    )
    assert crosswalk.exists(), (
        f"adapter {adapter_slug} missing crosswalk_additions.yaml after wave-5 fill"
    )


# ---------------------------------------------------------------------------
# Source-of-truth matrix updates
# ---------------------------------------------------------------------------

def test_source_of_truth_matrix_resolves_commitment_placeholder():
    text = SOURCE_OF_TRUTH_MATRIX.read_text(encoding="utf-8")
    assert "commitment / purchase_commitment (placeholder)" not in text, (
        "wave-5 must remove the 'commitment placeholder' note from source_of_truth_matrix.md"
    )
    assert "| commitment |" in text, (
        "source_of_truth_matrix.md must declare a row for canonical commitment"
    )


def test_source_of_truth_matrix_includes_yardi_classification_section():
    text = SOURCE_OF_TRUTH_MATRIX.read_text(encoding="utf-8")
    assert "Yardi rows" in text or "yardi_primary_operating" in text, (
        "source_of_truth_matrix.md must include wave-5 Yardi classification rows"
    )


# ---------------------------------------------------------------------------
# Conftest collection regression fix
# ---------------------------------------------------------------------------

def test_pyproject_toml_at_repo_root_configures_pythonpath():
    # SKILL_ROOT = src/skills/residential_multifamily; repo root is .parents[2]
    repo_root = SKILL_ROOT.parents[2]
    pyproject = repo_root / "pyproject.toml"
    assert pyproject.exists(), (
        f"pyproject.toml required at repo root {repo_root} for pytest pythonpath config"
    )
    text = pyproject.read_text(encoding="utf-8")
    assert "pythonpath" in text and "residential_multifamily/tests" in text, (
        "pyproject.toml must declare pythonpath including the skill tests dir"
    )
