"""Validates every fenced YAML block in _core/metrics.md against the metric_contract schema.

Also asserts that:
- Every block has a snake_case slug matching the allowed pattern.
- The unit is one of the permitted values.
- `time_basis_window` is present when required.
"""
from __future__ import annotations

from typing import Any, Dict, List

from conftest import (
    SUBSYS,
    extract_yaml_blocks,
    validate_against_schema,
)


PERMITTED_UNITS = {
    "count",
    "percent",
    "dollars",
    "dollars_per_unit",
    "dollars_per_unit_per_month",
    "dollars_per_nrsf",
    "dollars_per_sf",
    "dollars_per_gsf",
    "days",
    "minutes",
    "ratio",
    "months",
    "score",
    "basis_points",
    "pct_points",
    "units_per_fte",
    "index",
    "distribution",
}


def _load_metrics_md_blocks() -> List[Dict[str, Any]]:
    metrics_path = SUBSYS / "_core" / "metrics.md"
    assert metrics_path.exists(), f"missing {metrics_path}"
    text = metrics_path.read_text(encoding="utf-8")
    blocks = extract_yaml_blocks(text)
    assert blocks, "no fenced yaml blocks found in _core/metrics.md"
    return blocks


def test_metric_blocks_nonempty():
    blocks = _load_metrics_md_blocks()
    assert len(blocks) >= 10, f"suspiciously few metric blocks: {len(blocks)}"


def test_each_block_validates_against_contract(metric_contract_schema):
    blocks = _load_metrics_md_blocks()
    errors: List[str] = []
    for block in blocks:
        slug = block.get("slug", "<missing slug>")
        block_errors = validate_against_schema(block, metric_contract_schema, path=f"$.{slug}")
        errors.extend(block_errors)
    assert not errors, "metric contract validation failed:\n" + "\n".join(errors)


def test_time_basis_window_required_when_applicable():
    blocks = _load_metrics_md_blocks()
    bad: List[str] = []
    for block in blocks:
        tb = block.get("time_basis")
        if tb in ("rolling_window", "period_cumulative"):
            if not block.get("time_basis_window"):
                bad.append(f"metric {block.get('slug')!r} has time_basis={tb!r} but no time_basis_window")
    assert not bad, "\n".join(bad)


def test_units_are_permitted():
    blocks = _load_metrics_md_blocks()
    bad: List[str] = []
    for block in blocks:
        unit = block.get("unit")
        if unit not in PERMITTED_UNITS:
            bad.append(f"metric {block.get('slug')!r} has unit {unit!r} not in permitted set")
    assert not bad, "\n".join(bad)


def test_slugs_are_snake_case():
    """Redundant with pattern on slug, but surfaces a nicer error."""
    blocks = _load_metrics_md_blocks()
    import re

    pat = re.compile(r"^[a-z][a-z0-9_]*$")
    bad: List[str] = []
    for block in blocks:
        slug = block.get("slug", "")
        if not pat.match(slug):
            bad.append(f"slug {slug!r} is not snake_case")
    assert not bad, "\n".join(bad)
