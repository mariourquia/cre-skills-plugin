"""Tests for the corpus-wide static governance scanner (scripts/governance-scan.py).

Two halves:
  1. POSITIVE CONTROL — the real generated catalog (dist/catalog.json) passes
     with zero ERROR violations (run scripts/catalog-build.py first).
  2. FAIL-CLOSED FIXTURES — in-memory catalog items (NOT fixture SKILL.md dirs,
     which would pollute the real catalog/counts) prove each ERROR rule fails
     closed and each WARN rule reports without failing.

Plus the two-source_class-vocabulary disjointness invariant: the connector
data-trust enum and the RMF runtime cell-tag enum must never share a value, or a
scanner keyed on the bare token `source_class` would conflate them.
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCANNER_PATH = REPO_ROOT / "scripts" / "governance-scan.py"
CATALOG_JSON = REPO_ROOT / "dist" / "catalog.json"
SOURCE_CLASS_YAML = (
    REPO_ROOT / "src" / "skills" / "residential_multifamily" / "reference"
    / "connectors" / "_schema" / "source_class.yaml"
)


def _load_scanner():
    spec = importlib.util.spec_from_file_location("governance_scan", SCANNER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


GS = _load_scanner()
TODAY = _dt.date(2026, 6, 4)  # fixed so statute fixtures are deterministic

VALID_SRP = {"emits": ["model/*"], "on_unresolvable": "refuse", "forbids_fabricated_model_ref": True}


def _doc_getter(docs):
    """docs: {id: (frontmatter_dict, body_str)} -> get_doc callable."""
    return lambda iid: docs.get(iid, (None, ""))


def _rules(items, docs=None):
    docs = docs or {}
    return {(sev, rule) for sev, _id, rule, _msg in GS.scan(items, _doc_getter(docs), today=TODAY)}


def _error_rules(items, docs=None):
    return {(s, r) for s, r in _rules(items, docs) if s == GS.ERROR}


# ---------------------------------------------------------------------------
# 1. Positive control
# ---------------------------------------------------------------------------
def test_real_catalog_has_no_governance_errors():
    assert CATALOG_JSON.exists(), "run scripts/catalog-build.py first"
    items = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))["items"]
    violations = GS.scan(items, GS._load_doc_from_fs)
    errors = [v for v in violations if v[0] == GS.ERROR]
    assert not errors, "real catalog has governance ERRORs:\n  " + "\n  ".join(
        f"{i} [{r}] {m}" for _s, i, r, m in errors
    )


# ---------------------------------------------------------------------------
# 2. Fail-closed fixtures — one INVALID case per ERROR rule
# ---------------------------------------------------------------------------
def test_decision_grade_requires_gate():
    items = [{"id": "x", "type": "skill", "decision_grade": True, "human_gate": "none",
              "source_ref_policy": VALID_SRP}]
    docs = {"x": ({"refusal_trigger": "refuses on missing input"}, "body")}
    assert (GS.ERROR, "decision_grade_requires_gate") in _rules(items, docs)


def test_decision_grade_requires_source_ref_policy():
    items = [{"id": "x", "type": "skill", "decision_grade": True,
              "human_gate": "approval_required", "source_ref_policy": None}]
    docs = {"x": ({"refusal_trigger": "refuses"}, "body")}
    assert (GS.ERROR, "decision_grade_requires_source_ref_policy") in _rules(items, docs)


def test_decision_grade_requires_refusal_trigger():
    items = [{"id": "x", "type": "skill", "decision_grade": True,
              "human_gate": "approval_required", "source_ref_policy": VALID_SRP}]
    docs = {"x": ({}, "body with no refusal trigger field")}  # frontmatter lacks refusal_trigger
    assert (GS.ERROR, "decision_grade_requires_refusal_trigger") in _rules(items, docs)


def test_source_ref_policy_shape():
    items = [{"id": "x", "type": "skill", "source_ref_policy": {"emits": ["model/*"]}}]
    assert (GS.ERROR, "source_ref_policy_shape") in _error_rules(items)


def test_source_ref_refusal_posture_rejects_warn():
    items = [{"id": "x", "type": "skill", "source_ref_policy": {
        "emits": ["model/*"], "on_unresolvable": "warn", "forbids_fabricated_model_ref": True}}]
    assert (GS.ERROR, "source_ref_refusal_posture") in _error_rules(items)


def test_source_ref_refusal_posture_allows_cite_best_effort():
    # comp-snapshot uses cite_best_effort; it must NOT be flagged (Governance review).
    items = [{"id": "x", "type": "skill", "source_ref_policy": {
        "emits": ["market/*"], "on_unresolvable": "cite_best_effort", "forbids_fabricated_model_ref": True}}]
    assert (GS.ERROR, "source_ref_refusal_posture") not in _error_rules(items)


def test_dangling_decomposition():
    items = [{"id": "x", "type": "skill", "decomposes_to": ["does-not-exist"]}]
    assert (GS.ERROR, "dangling_decomposition") in _error_rules(items)


def test_decomposition_resolves_against_catalog():
    items = [{"id": "orch", "type": "skill", "decomposes_to": ["leaf"]},
             {"id": "leaf", "type": "calculator"}]
    assert (GS.ERROR, "dangling_decomposition") not in _error_rules(items)


def test_pii_removed_posture_value_fails():
    items = [{"id": "x", "type": "skill", "pii_policy": "pseudonymized"}]
    assert (GS.ERROR, "pii_policy_removed_value") in _error_rules(items)


def test_pii_unknown_value_fails():
    items = [{"id": "x", "type": "skill", "pii_policy": "top_secret"}]
    assert (GS.ERROR, "pii_policy_enum") in _error_rules(items)


def test_valuation_requires_not_an_appraisal_stamp():
    items = [{"id": "x", "type": "skill", "produces_artifact_kind": "valuation_support"}]
    docs = {"x": ({}, "A clean valuation with no disclaimer.")}
    assert (GS.ERROR, "valuation_requires_not_an_appraisal") in _rules(items, docs)
    # with the stamp present, it passes
    docs_ok = {"x": ({}, "This is an estimate, not an appraisal.")}
    assert (GS.ERROR, "valuation_requires_not_an_appraisal") not in _error_rules(items, docs_ok)


def test_statute_skill_requires_disclaimer_and_freshness():
    items = [{"id": "x", "type": "skill"}]
    stale = ({"statute_review": [{"code": "IRC-1031", "last_verified": "2020-01-01"}]},
             "Tax analysis with no disclaimer.")
    rules = _rules(items, {"x": stale})
    assert (GS.ERROR, "statute_review_stale") in rules
    assert (GS.ERROR, "statute_requires_disclaimer") in rules
    fresh_ok = ({"statute_review": [{"code": "IRC-1031", "last_verified": "2026-06-03"}]},
                "This is not tax advice; consult a qualified tax professional.")
    assert not any(r.startswith("statute") for _s, r in _rules(items, {"x": fresh_ok}))


def test_calculator_must_be_calculator_result():
    items = [{"id": "c", "type": "calculator", "produces_artifact_kind": "memo"}]
    assert (GS.ERROR, "calculator_artifact_kind") in _error_rules(items)


def test_calculator_file_must_resolve():
    items = [{"id": "x", "type": "skill", "calculator_file": "src/calculators/__nope__.py",
              "produces_artifact_kind": "calculator_result"}]
    assert (GS.ERROR, "calculator_file_unresolved") in _error_rules(items)


# ---------------------------------------------------------------------------
# WARN rules report but do NOT fail closed
# ---------------------------------------------------------------------------
def test_consumer_facing_without_outputs_is_warn_not_error():
    items = [{"id": "x", "type": "skill", "decision_grade": True,
              "human_gate": "approval_required", "source_ref_policy": VALID_SRP, "outputs": []}]
    docs = {"x": ({"refusal_trigger": "refuses"}, "body")}
    rules = _rules(items, docs)
    assert (GS.WARN, "consumer_facing_outputs") in rules
    assert not any(s == GS.ERROR for s, _r in rules)


def test_pii_backfill_candidate_is_warn_not_error():
    items = [{"id": "x", "type": "skill", "workspace_scope": "leasing", "pii_policy": "none"}]
    rules = _rules(items, {"x": ({}, "body")})
    assert (GS.WARN, "pii_backfill_candidate") in rules
    assert not any(s == GS.ERROR for s, _r in rules)


def test_run_exit_codes():
    """A clean item -> exit 0; an ERROR item -> exit 1 (CLI contract). Uses scan
    directly since run() reads the real catalog; here we assert the severity gate."""
    clean = [{"id": "x", "type": "skill", "pii_policy": "none"}]
    assert not [v for v in GS.scan(clean, _doc_getter({}), today=TODAY) if v[0] == GS.ERROR]
    bad = [{"id": "x", "type": "skill", "pii_policy": "pseudonymized"}]
    assert [v for v in GS.scan(bad, _doc_getter({}), today=TODAY) if v[0] == GS.ERROR]


# ---------------------------------------------------------------------------
# Two source_class vocabularies must stay disjoint (no conflation)
# ---------------------------------------------------------------------------
def test_connector_and_runtime_source_class_are_disjoint():
    """The connector data-trust source_class enum (reference/connectors/_schema/
    source_class.yaml) and the RMF runtime cell-tag enum (fallback_resolver.py)
    must never share a value. A scanner keyed on the bare token would otherwise
    conflate two distinct namespaces."""
    import yaml
    connector = set(yaml.safe_load(SOURCE_CLASS_YAML.read_text(encoding="utf-8"))["source_class_values"])
    # RMF runtime cell tags (SoT: residential_multifamily/_core/runtime/fallback_resolver.py
    # + _core/executive_output_contract.md). Pinned here; test_connector_source_class
    # already byte-pins the connector enum to its schema.
    runtime_cell = {"operator", "derived", "benchmark", "overlay", "overlay:fallback", "placeholder"}
    assert connector.isdisjoint(runtime_cell), (
        f"source_class vocabularies overlap: {connector & runtime_cell} — keep connector "
        f"data-trust and RMF runtime cell tags as separate namespaces"
    )
