"""Determinism, rounding, and run-context helpers.

Calculators in the ingestion family are PURE: the same input dict produces
byte-identical JSON. To make that guarantee hold we never read a wall clock
here (no ``datetime``/``time`` import anywhere in this package) -- the caller
supplies ``as_of`` and it flows unchanged into ``created_at``/``updated_at``.
``run_id`` is the only field that legitimately varies a record's identity
between runs; tests assert that two runs differing only in ``run_id`` differ
ONLY in run-id-bearing fields.

Rounding mirrors the existing calculators (quick_screen / debt_sizing):
rates at 4dp, dollars at 2dp, ratios at 3dp.
"""
from __future__ import annotations

import json
from typing import Any

# A stable sentinel used when a caller omits run_id. Graded/payload calculators
# should reject a missing as_of (see require_context); run_id may default.
DEFAULT_RUN_ID = "RUN-UNSET"


def rnd_money(x: float) -> float:
    """Dollars: 2 decimal places."""
    return round(float(x), 2)


def rnd_rate(x: float) -> float:
    """Rates expressed as decimals (e.g. 0.0533): 4 decimal places."""
    return round(float(x), 4)


def rnd_pct(x: float) -> float:
    """Percentage points (e.g. 5.33): 2 decimal places."""
    return round(float(x), 2)


def rnd_ratio(x: float) -> float:
    """Coverage / multiple ratios (e.g. DSCR 1.25): 3 decimal places."""
    return round(float(x), 3)


def rnd_psf(x: float) -> float:
    """Per-square-foot figures: 2 decimal places."""
    return round(float(x), 2)


def safe_div(numerator: float, denominator: float) -> float | None:
    """Division that returns None on a zero/NaN denominator (never raises)."""
    try:
        if not denominator:
            return None
        return float(numerator) / float(denominator)
    except (TypeError, ValueError):
        return None


def stable_dumps(obj: Any) -> str:
    """Canonical JSON for determinism comparisons (sorted keys, compact)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def missing_inputs(inputs: dict, required: list) -> list:
    """Return the required keys that are absent or None (no exception)."""
    return [k for k in required if k not in inputs or inputs[k] is None]


def resolve_context(inputs: dict) -> dict:
    """Extract the run context. ``as_of`` may be None; payload/graded
    calculators must reject that via :func:`require_context`.

    tenant id is read from any of the accepted aliases and is NOT validated
    here -- callers run ``pii.assert_safe_tenant_id`` so a bad id fails closed.
    """
    tenant = (
        inputs.get("tenant_id")
        or inputs.get("workspace_id")
        or inputs.get("tenant_id_or_workspace_id")
    )
    return {
        "run_id": str(inputs.get("run_id") or DEFAULT_RUN_ID),
        "as_of": inputs.get("as_of"),
        "tenant_id": tenant,
    }


def require_context(ctx: dict) -> list:
    """Return error strings if a payload/graded run lacks a deterministic
    ``as_of``. Wall-clock fallback is forbidden, so as_of is mandatory."""
    errs: list = []
    if not ctx.get("as_of"):
        errs.append(
            "as_of is required (ISO date/datetime). Wall-clock timestamps are "
            "forbidden so output stays byte-reproducible."
        )
    return errs


def error_result(message: str, **extra: Any) -> dict:
    """The canonical failure shape. Calculators NEVER raise on bad input;
    they print this dict and (callers) exit non-zero only for unusable input.
    Mirrors fund_fee_modeler / tenant_credit_scorer ``{"error": ...}``."""
    out = {"error": message}
    out.update(extra)
    return out
