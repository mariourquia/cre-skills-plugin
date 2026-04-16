"""Tests for the runtime fallback resolver (Obj 2b).

Covers the six fallback_behavior enum values declared in
_core/schemas/reference_manifest.yaml:
  ask_user, use_portfolio_average, use_prior_period, refuse, escalate,
  proceed_with_default.

Also asserts the executive-output-contract shape:
- Non-refuse fallback paths attach source_class [overlay:fallback].
- Refuse / escalate / ask_user set refused=True and return value=None.
- Primary hits attach source_class [operator] and do not trigger
  fallback paths.
- Every call produces an audit entry with the minimum set of fields.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Locate the runtime module by walking up to SUBSYS.
_HERE = Path(__file__).resolve()
_SUBSYS = _HERE.parent.parent
sys.path.insert(0, str(_SUBSYS / "_core"))

from runtime.fallback_resolver import (  # noqa: E402
    ReadOutcome,
    format_cell,
    resolve,
)


def _audit_fields():
    return {
        "timestamp",
        "event",
        "workflow_slug",
        "ref_path",
        "declared_fallback_behavior",
        "actor",
        "outcome",
        "source_class",
    }


def test_primary_hit_returns_operator_tag() -> None:
    outcome = ReadOutcome(found=True, value={"x": 1}, primary_path="reference/a.csv")
    r = resolve(
        "refuse",
        outcome,
        workflow_slug="executive_operating_summary_generation",
        ref_path="reference/a.csv",
    )
    assert r.value == {"x": 1}
    assert r.source_class == "operator"
    assert r.refused is False
    assert _audit_fields() <= set(r.audit_entry.keys())
    assert r.audit_entry["outcome"] == "primary_hit"


def test_refuse_returns_placeholder_and_halts() -> None:
    outcome = ReadOutcome(found=False)
    r = resolve(
        "refuse",
        outcome,
        workflow_slug="quarterly_portfolio_review",
        ref_path="reference/normalized/watchlist_scoring.yaml",
    )
    assert r.value is None
    assert r.source_class == "placeholder"
    assert r.refused is True
    assert r.audit_entry["outcome"] == "refused_missing_required_ref"
    assert r.notes and "must halt" in r.notes[0]


def test_use_prior_period_returns_overlay_fallback_tag() -> None:
    outcome = ReadOutcome(
        found=False,
        fallback_value=0.92,
        fallback_source="prior_period_2026-03-31",
    )
    r = resolve(
        "use_prior_period",
        outcome,
        workflow_slug="monthly_property_operating_review",
        ref_path="reference/normalized/market_rents__atlanta_mf.csv",
    )
    assert r.value == 0.92
    assert r.source_class == "overlay:fallback"
    assert r.refused is False
    assert r.audit_entry["outcome"] == "fallback_use_prior_period"
    assert r.audit_entry["source_class"] == "overlay:fallback"
    assert "prior_period_2026-03-31" in r.audit_entry["fallback_source"]


def test_use_portfolio_average_tags_overlay_fallback() -> None:
    outcome = ReadOutcome(found=False, fallback_value=0.045, fallback_source="portfolio_mean")
    r = resolve(
        "use_portfolio_average",
        outcome,
        workflow_slug="monthly_asset_management_review",
        ref_path="reference/normalized/collections_benchmarks__southeast_mf.csv",
    )
    assert r.value == 0.045
    assert r.source_class == "overlay:fallback"
    assert r.refused is False


def test_proceed_with_default_without_value_still_tags_overlay() -> None:
    outcome = ReadOutcome(found=False)  # no fallback value prepared
    r = resolve(
        "proceed_with_default",
        outcome,
        workflow_slug="vendor_dispatch_sla_review",
        ref_path="reference/normalized/vendor_sla_defaults.csv",
    )
    assert r.value is None  # caller will substitute a default
    assert r.source_class == "overlay:fallback"
    assert r.refused is False
    assert "overlay:fallback" in r.notes[0]


def test_escalate_is_a_refusal_at_resolver_layer() -> None:
    outcome = ReadOutcome(found=False)
    r = resolve(
        "escalate",
        outcome,
        workflow_slug="executive_pipeline_summary",
        ref_path="reference/normalized/board_packet_template__acme.md",
    )
    assert r.value is None
    assert r.refused is True
    assert r.source_class == "placeholder"
    assert r.audit_entry["outcome"] == "refused_for_escalate"


def test_ask_user_is_a_refusal_at_resolver_layer() -> None:
    outcome = ReadOutcome(found=False)
    r = resolve(
        "ask_user",
        outcome,
        workflow_slug="tailoring_interview",
        ref_path="reference/derived/same_store_set__acme.yaml",
    )
    assert r.value is None
    assert r.refused is True
    assert r.source_class == "placeholder"
    assert r.audit_entry["outcome"] == "refused_for_ask_user"


def test_format_cell_applies_tag() -> None:
    assert format_cell(0.92, "overlay:fallback") == "0.92 [overlay:fallback]"
    assert format_cell(None, "placeholder") == "REFUSED [placeholder]"
    assert format_cell(1.18, "operator") == "1.18 [operator]"
