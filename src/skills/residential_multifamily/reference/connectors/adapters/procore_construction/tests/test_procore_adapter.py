"""Procore construction adapter: wave-5 fill tests.

Covers the wave-5 artifacts produced under procore_construction/:
  - sample_raw JSONL files (7 entities)
  - sample_normalized JSONL mirrors
  - dq_rules.yaml (>=18 rules, pc_ prefix)
  - reconciliation_rules.md (prose spec)
  - reconciliation_checks.yaml (>=12 checks, pc_recon_ prefix)
  - edge_cases.md
  - crosswalk_additions.yaml (5 crosswalk tables)
  - workflow_activation_additions.yaml
  - runbooks/procore_onboarding.md, procore_common_issues.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))


# ----------------------------------------------------------------------
# sample_raw and sample_normalized — presence and shape
# ----------------------------------------------------------------------

SAMPLE_RAW_FILES = {
    "projects.jsonl",
    "commitments.jsonl",
    "change_orders.jsonl",
    "draw_requests.jsonl",
    "schedule_milestones.jsonl",
    "vendors.jsonl",
    "cost_codes.jsonl",
}

SAMPLE_NORMALIZED_FILES = SAMPLE_RAW_FILES


def _load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def test_sample_raw_files_present():
    d = ADAPTER_DIR / "sample_raw"
    assert d.exists(), "sample_raw directory missing"
    actual = {p.name for p in d.iterdir() if p.is_file()}
    missing = SAMPLE_RAW_FILES - actual
    assert not missing, f"sample_raw missing: {missing}"


def test_sample_normalized_files_present():
    d = ADAPTER_DIR / "sample_normalized"
    assert d.exists(), "sample_normalized directory missing"
    actual = {p.name for p in d.iterdir() if p.is_file()}
    missing = SAMPLE_NORMALIZED_FILES - actual
    assert not missing, f"sample_normalized missing: {missing}"


def test_sample_raw_row_counts():
    expected_min = {
        "projects.jsonl": 5,
        "commitments.jsonl": 5,
        "change_orders.jsonl": 6,
        "draw_requests.jsonl": 4,
        "schedule_milestones.jsonl": 6,
        "vendors.jsonl": 4,
        "cost_codes.jsonl": 6,
    }
    for fname, min_rows in expected_min.items():
        rows = _load_jsonl(ADAPTER_DIR / "sample_raw" / fname)
        assert len(rows) >= min_rows, (
            f"sample_raw/{fname}: expected >= {min_rows} rows, got {len(rows)}"
        )
        for idx, row in enumerate(rows):
            assert row.get("status") in {"sample", "stub", "template"}, (
                f"sample_raw/{fname} row {idx} missing status tag"
            )
            assert row.get("source_name") == "procore_prod", (
                f"sample_raw/{fname} row {idx} source_name must be procore_prod"
            )


def test_sample_normalized_row_status_tags():
    d = ADAPTER_DIR / "sample_normalized"
    for fname in SAMPLE_NORMALIZED_FILES:
        rows = _load_jsonl(d / fname)
        assert rows, f"sample_normalized/{fname} is empty"
        for idx, row in enumerate(rows):
            assert row.get("status") in {"sample", "stub", "template"}, (
                f"sample_normalized/{fname} row {idx} missing status tag"
            )


def test_sample_data_is_synthetic_pii_free():
    """Guard that sample_raw does not contain obvious unredacted PII patterns."""
    pii_patterns = [
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN
        re.compile(r"\b\d{10,}\b"),  # raw phone / tax id
        re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b@\w+\.\w+"),  # first last @ domain
    ]
    for fname in SAMPLE_RAW_FILES:
        path = ADAPTER_DIR / "sample_raw" / fname
        text = path.read_text()
        for pat in pii_patterns:
            m = pat.search(text)
            assert not m, f"sample_raw/{fname} contains pattern matching PII: {m.group()}"


# ----------------------------------------------------------------------
# dq_rules.yaml — rule count, prefix, severity, required fields
# ----------------------------------------------------------------------

def test_dq_rules_load_and_prefix():
    data = yaml.safe_load((ADAPTER_DIR / "dq_rules.yaml").read_text())
    rules = data.get("rules", [])
    assert len(rules) >= 18, f"dq_rules expected >= 18, got {len(rules)}"
    rule_ids = [r["rule_id"] for r in rules]
    assert len(set(rule_ids)) == len(rule_ids), "dq_rules rule_ids must be unique"
    for r in rules:
        assert r["rule_id"].startswith("pc_"), f"rule {r['rule_id']} missing pc_ prefix"
        assert r["dimension"] in {"freshness", "completeness", "conformance", "uniqueness", "consistency"}
        assert r["severity"] in {"blocker", "warning", "info"}
        assert r.get("description"), f"rule {r['rule_id']} missing description"
        assert r.get("expected"), f"rule {r['rule_id']} missing expected"
        assert r.get("remediation"), f"rule {r['rule_id']} missing remediation"


def test_dq_rules_cover_required_dimensions():
    data = yaml.safe_load((ADAPTER_DIR / "dq_rules.yaml").read_text())
    dims = {r["dimension"] for r in data["rules"]}
    required_dims = {"freshness", "completeness", "conformance", "uniqueness", "consistency"}
    missing = required_dims - dims
    assert not missing, f"dq_rules missing dimensions: {missing}"


# ----------------------------------------------------------------------
# reconciliation_rules.md and reconciliation_checks.yaml
# ----------------------------------------------------------------------

def test_reconciliation_rules_md_present():
    path = ADAPTER_DIR / "reconciliation_rules.md"
    assert path.exists(), "reconciliation_rules.md missing"
    text = path.read_text()
    # Must reference each of the 5 cross-system reconciliations.
    for expected in [
        "Procore x Intacct",
        "Procore x Dealpath",
        "Procore x Excel",
        "Procore x AppFolio",
        "Procore x Yardi",
    ]:
        assert expected in text, f"reconciliation_rules.md missing section: {expected}"
    # Must cite tolerance band file and never hardcode thresholds.
    assert "reconciliation_tolerance_band.yaml" in text


def test_reconciliation_checks_load_and_prefix():
    data = yaml.safe_load((ADAPTER_DIR / "reconciliation_checks.yaml").read_text())
    checks = data.get("checks", [])
    assert len(checks) >= 12, f"reconciliation_checks expected >= 12, got {len(checks)}"
    ids = [c["check_id"] for c in checks]
    assert len(set(ids)) == len(ids), "reconciliation_checks check_ids must be unique"
    for c in checks:
        assert c["check_id"].startswith("pc_recon_"), (
            f"check {c['check_id']} missing pc_recon_ prefix"
        )
        assert c["severity"] in {"blocker", "warning", "info"}
        assert c.get("description"), f"check {c['check_id']} missing description"
        assert c.get("expected_invariant"), f"check {c['check_id']} missing expected_invariant"
        assert c.get("remediation"), f"check {c['check_id']} missing remediation"
        assert c.get("inputs") and len(c["inputs"]) >= 1, (
            f"check {c['check_id']} must have >= 1 input"
        )


def test_reconciliation_checks_cite_tolerance_band():
    """At least half the checks reference the tolerance band file in inputs or invariant."""
    data = yaml.safe_load((ADAPTER_DIR / "reconciliation_checks.yaml").read_text())
    checks = data["checks"]
    cite_count = 0
    for c in checks:
        corpus = " ".join(c.get("inputs", [])) + " " + c.get("expected_invariant", "")
        if "reconciliation_tolerance_band" in corpus or "_band" in corpus:
            cite_count += 1
    assert cite_count >= len(checks) // 2, (
        f"reconciliation_checks: only {cite_count}/{len(checks)} reference tolerance bands"
    )


# ----------------------------------------------------------------------
# edge_cases.md
# ----------------------------------------------------------------------

def test_edge_cases_md_present_and_has_12():
    path = ADAPTER_DIR / "edge_cases.md"
    assert path.exists(), "edge_cases.md missing"
    text = path.read_text()
    # Count top-level "## " headers that look like numbered edges.
    numbered = re.findall(r"^##\s+\d+\.\s+", text, flags=re.MULTILINE)
    assert len(numbered) >= 12, f"edge_cases.md expected >= 12 cases, got {len(numbered)}"


# ----------------------------------------------------------------------
# crosswalk_additions.yaml
# ----------------------------------------------------------------------

def test_crosswalk_additions_present_and_covers_five_tables():
    data = yaml.safe_load((ADAPTER_DIR / "crosswalk_additions.yaml").read_text())
    expected = {
        "capex_project_crosswalk",
        "dev_project_crosswalk",
        "vendor_master_crosswalk",
        "change_order_crosswalk",
        "draw_request_crosswalk",
    }
    actual = set(data.keys()) - {"status_tag"}
    missing = expected - actual
    assert not missing, f"crosswalk_additions missing tables: {missing}"
    for table_name in expected:
        rows = data[table_name].get("rows", [])
        assert rows, f"{table_name} has no rows"
        for r in rows:
            assert r.get("canonical_id"), f"{table_name} row missing canonical_id"
            assert r.get("source_system"), f"{table_name} row missing source_system"
            assert r.get("source_id"), f"{table_name} row missing source_id"


def test_crosswalk_additions_procore_rows_reference_sample_ids():
    data = yaml.safe_load((ADAPTER_DIR / "crosswalk_additions.yaml").read_text())
    # Every Procore-side row's source_id should appear in one of our sample_raw files.
    all_sample_ids = set()
    for fname in SAMPLE_RAW_FILES:
        rows = _load_jsonl(ADAPTER_DIR / "sample_raw" / fname)
        for r in rows:
            for key in ("project_id", "commitment_id", "vendor_id", "change_order_id", "draw_request_id"):
                v = r.get(key)
                if v:
                    all_sample_ids.add(v)
    for table_name, table in data.items():
        if table_name == "status_tag":
            continue
        for row in table.get("rows", []):
            if row.get("source_system") == "procore_prod":
                assert row["source_id"] in all_sample_ids, (
                    f"{table_name}: procore_prod source_id {row['source_id']} not in sample_raw"
                )


# ----------------------------------------------------------------------
# workflow_activation_additions.yaml
# ----------------------------------------------------------------------

def test_workflow_activation_covers_required_workflows():
    data = yaml.safe_load((ADAPTER_DIR / "workflow_activation_additions.yaml").read_text())

    activates = data.get("activates_existing_workflows", [])
    proposed = data.get("proposes_new_workflows", [])
    all_workflows = activates + proposed

    required_primary = {
        "bid_leveling_procurement_review",
        "change_order_review",
        "construction_meeting_prep_and_action_tracking",
        "cost_to_complete_review",
        "draw_package_review",
        "schedule_risk_review",
        "development_pipeline_tracking",
        "delivery_handoff",
    }
    required_contributing = {
        "capex_estimate_generation",
        "capital_project_intake_and_prioritization",
    }

    workflow_roles = {w["workflow"]: w["role"] for w in all_workflows}

    for wf in required_primary:
        assert wf in workflow_roles, f"missing primary workflow: {wf}"
        assert workflow_roles[wf] == "primary", f"workflow {wf} must be primary; got {workflow_roles[wf]}"

    for wf in required_contributing:
        assert wf in workflow_roles, f"missing contributing workflow: {wf}"
        assert workflow_roles[wf] == "contributing", (
            f"workflow {wf} must be contributing; got {workflow_roles[wf]}"
        )

    # Every workflow entry must have the contract fields.
    for w in all_workflows:
        assert w.get("objects_supplied"), f"{w['workflow']} missing objects_supplied"
        # blocking_issues and partial_mode_behavior and human_approvals_required
        # fields are required for primary workflows per task brief.
        if w["role"] == "primary":
            assert "blocking_issues" in w, f"{w['workflow']} missing blocking_issues"
            assert "partial_mode_behavior" in w, f"{w['workflow']} missing partial_mode_behavior"
            assert "human_approvals_required" in w, (
                f"{w['workflow']} missing human_approvals_required"
            )


# ----------------------------------------------------------------------
# runbooks presence
# ----------------------------------------------------------------------

def test_runbooks_present():
    for name in ("procore_onboarding.md", "procore_common_issues.md"):
        path = ADAPTER_DIR / "runbooks" / name
        assert path.exists(), f"runbook missing: {name}"
        text = path.read_text()
        assert len(text) > 500, f"runbook {name} suspiciously short"


# ----------------------------------------------------------------------
# YAML file leading comment requirement per task brief
# ----------------------------------------------------------------------

def test_every_yaml_file_leads_with_purpose_comment():
    yaml_files = [
        "dq_rules.yaml",
        "reconciliation_checks.yaml",
        "crosswalk_additions.yaml",
        "workflow_activation_additions.yaml",
    ]
    for fname in yaml_files:
        path = ADAPTER_DIR / fname
        with path.open("r", encoding="utf-8") as f:
            first = f.readline()
        assert first.startswith("#"), f"{fname} must lead with # purpose comment"


# ----------------------------------------------------------------------
# DQ rule remediation pointers resolve to runbook headers (best-effort)
# ----------------------------------------------------------------------

def test_dq_rules_remediation_runbook_pointers_resolve():
    """Every remediation pointing at a runbook anchor should match some header."""
    data = yaml.safe_load((ADAPTER_DIR / "dq_rules.yaml").read_text())
    runbook_text = (ADAPTER_DIR / "runbooks" / "procore_common_issues.md").read_text()
    # Gather all `## <slug>` headers.
    anchors = set(re.findall(r"^##\s+([a-z0-9_]+)\s*$", runbook_text, flags=re.MULTILINE))
    for r in data["rules"]:
        rem = r.get("remediation", "")
        m = re.search(r"procore_common_issues\.md::(\w+)", rem)
        if m:
            assert m.group(1) in anchors, (
                f"dq rule {r['rule_id']} remediation anchor '{m.group(1)}' not in runbook"
            )
