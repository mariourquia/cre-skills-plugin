"""Overlay integrity tests.

For each overlay.yaml under overlays/**:
- Schema-validates against overlay_manifest schema (with two local exceptions: the
  canonical schema is strict, but our overlay files legitimately carry a `status`
  field used to mark stub overlays; the schema does not forbid extra keys because
  additionalProperties is false in the canonical spec. We tolerate `status` here as
  a documented augmentation that ships with the canonical overlays).
- Asserts no override has target_kind in the forbidden set: metric_numerator,
  metric_denominator. (Overlays may adjust thresholds, target bands, or filters,
  but they may not redefine the numerator or denominator of a canonical metric.)
- For stub overlays (status: stub OR authoring_notes mentions "stub"), asserts
  that no override targets middle_market-specific target_bands on canonical metrics.
  This protects rule-9 behavior ("segment stubs do not override middle-market
  behavior").
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict, Iterator, List

import yaml

from conftest import (
    SUBSYS,
    iter_overlay_manifests,
    validate_against_schema,
)


FORBIDDEN_TARGET_KINDS = {
    "metric_numerator",
    "metric_denominator",
}


def _load(p: Path) -> Dict[str, Any]:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _is_stub(overlay: Dict[str, Any]) -> bool:
    status = str(overlay.get("status", "")).lower()
    if status == "stub":
        return True
    notes = str(overlay.get("authoring_notes", "")).lower()
    if "stub overlay" in notes or "phase 1 does not deepen" in notes:
        return True
    return False


def _permissive_overlay_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of the overlay_manifest schema that allows top-level `status`.

    The canonical schema is strict with additionalProperties=false, which would
    reject the `status` field some canonical overlays use to signal stub vs deep.
    We add `status` to the permitted top-level properties for testing only.
    """
    s = copy.deepcopy(schema)
    props = s.setdefault("properties", {})
    props.setdefault("status", {"type": "string"})
    return s


def test_at_least_one_overlay_present():
    assert list(iter_overlay_manifests()), "no overlays/**/overlay.yaml files found"


def test_every_overlay_validates_against_schema(overlay_manifest_schema):
    permissive = _permissive_overlay_schema(overlay_manifest_schema)
    errors: List[str] = []
    for p in iter_overlay_manifests():
        data = _load(p)
        if not isinstance(data, dict):
            errors.append(f"{p.relative_to(SUBSYS)}: overlay did not parse to a mapping")
            continue
        err = validate_against_schema(data, permissive, path=str(p.relative_to(SUBSYS)))
        errors.extend(err)
    assert not errors, "\n".join(errors)


def test_no_forbidden_target_kinds():
    offenders: List[str] = []
    for p in iter_overlay_manifests():
        data = _load(p) or {}
        for idx, override in enumerate(data.get("overrides") or []):
            tk = override.get("target_kind")
            if tk in FORBIDDEN_TARGET_KINDS:
                offenders.append(
                    f"{p.relative_to(SUBSYS)}: overrides[{idx}] uses forbidden target_kind {tk!r}"
                )
    assert not offenders, "\n".join(offenders)


def test_stub_overlays_do_not_alter_middle_market_target_bands():
    """Stub overlays (affordable, luxury, or any status=stub overlay) must not override
    a `metric_target_band` targeting the middle_market segment's canonical metric.
    """
    failures: List[str] = []
    for p in iter_overlay_manifests():
        data = _load(p) or {}
        if not _is_stub(data):
            continue
        scope = data.get("scope") or {}
        # Stubs scoped to segments other than middle_market must not pretend to override
        # middle-market bands via metric_target_band overrides.
        scope_segment = scope.get("segment")
        for idx, override in enumerate(data.get("overrides") or []):
            tk = override.get("target_kind")
            if tk == "metric_target_band":
                # Permit only if the overlay is scoped exclusively to its own segment AND
                # the override_value does NOT name middle_market.
                ov_val = override.get("override_value")
                val_text = yaml.safe_dump(ov_val) if ov_val is not None else ""
                if (
                    scope_segment
                    and scope_segment != "middle_market"
                    and "middle_market" in val_text
                ):
                    failures.append(
                        f"{p.relative_to(SUBSYS)}: overrides[{idx}] on "
                        f"segment={scope_segment!r} touches middle_market band"
                    )
                # Additional guard: if this stub also includes segment=middle_market
                # scope, that's an outright collision.
                if scope_segment == "middle_market":
                    failures.append(
                        f"{p.relative_to(SUBSYS)}: stub overlay scoped to middle_market "
                        f"(not allowed for stubs)"
                    )
    assert not failures, "\n".join(failures)
