"""Dimension-specific, basis-aware tolerances.

A single global tolerance is wrong: base rent should tie tight on a
contractual-vs-gross-potential basis, while recoveries legitimately float
because CAM is billed as a monthly estimate and trued-up annually (per
``cam-reconciliation-calculator``). Validation arithmetic (annual == monthly*12)
uses the rent-roll rubric's ``within $1`` rule.

Tolerances are data so a caller may override per dimension via the input dict.
"""
from __future__ import annotations

# Rent-roll arithmetic (rubric dimension 4_rent_arithmetic: "within $1").
RENT_ARITHMETIC_DOLLAR = 1.00

# AMOS coherence vocabulary, reused so staged values reconcile downstream.
DOLLAR_TOL = 10_000.0   # +/- $10K
PCT_TOL = 0.5           # +/- 0.5 percentage points
BPS_TOL = 2.0           # +/- 2 bps
RATIO_TOL = 0.05        # +/- 0.05x
PSF_TOL = 0.50          # +/- $0.50 / SF

# Reconciliation tolerances by dimension (fraction of the larger side).
RECONCILE_TOLERANCE_PCT = {
    "base_rent": 0.01,        # contractual vs gross-potential: tight
    "recoveries": 0.15,       # CAM estimate-vs-trueup float
    "other_income": 0.10,
    "occupancy": 0.01,        # count basis ties tight
    "egi_bridge": 0.03,       # revenue inputs to NOI
}

# Confidence floor below which a record is routed to human review.
CONFIDENCE_FLOOR = "low"  # "low" routes to review; medium/high pass


def reconcile_tolerance(dimension: str, override: dict | None = None) -> float:
    """Return the fractional tolerance for a reconciliation dimension, honoring
    a per-dimension override dict from the input payload."""
    if override and dimension in override:
        try:
            return float(override[dimension])
        except (TypeError, ValueError):
            pass
    return RECONCILE_TOLERANCE_PCT.get(dimension, 0.05)


def within(a: float, b: float, abs_tol: float) -> bool:
    """Absolute-tolerance comparison (never raises on bad input)."""
    try:
        return abs(float(a) - float(b)) <= abs_tol
    except (TypeError, ValueError):
        return False


def within_pct(a: float, b: float, frac_tol: float) -> bool:
    """Relative-tolerance comparison against the larger magnitude."""
    try:
        a_f, b_f = float(a), float(b)
    except (TypeError, ValueError):
        return False
    base = max(abs(a_f), abs(b_f))
    if base == 0:
        return a_f == b_f
    return abs(a_f - b_f) / base <= frac_tol
