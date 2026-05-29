"""Executable realization of the rent-roll data-quality rubric.

This is NOT a parallel grader. It mirrors
``src/skills/rent-roll-analyzer/references/data-quality-rubric.yaml`` (version,
the 10 dimensions and their weights, the weakest-link semantics, and the
A=3/B=2/C=1 weighted score) so ``grade_ingestion`` emits the SAME A/B/C verdict
the YAML defines, alongside a 0-100 readout. Parity with the YAML is enforced
by ``tests/test_ingestion_canonical_sources.py``.

t12 and tie-out add their own dimension blocks here (the YAML covers rent roll
only); they follow the identical weakest-link contract.
"""
from __future__ import annotations

from typing import Any

RUBRIC_PATH = "src/skills/rent-roll-analyzer/references/data-quality-rubric.yaml"
RUBRIC_VERSION = "1.0"

GRADE_POINTS = {"A": 3, "B": 2, "C": 1}

# Rent-roll dimensions mirrored from data-quality-rubric.yaml: (key, name, weight).
RENT_ROLL_DIMENSIONS = (
    ("1_completeness", "Field Completeness", 15),
    ("2_date_consistency", "Date Consistency", 10),
    ("3_sf_reconciliation", "Square Footage Reconciliation", 15),
    ("4_rent_arithmetic", "Rent Arithmetic Accuracy", 10),
    ("5_escalation_documentation", "Rent Escalation Documentation", 10),
    ("6_vacancy_identification", "Vacancy Identification", 10),
    ("7_lease_type_clarity", "Lease Type Clarity", 5),
    ("8_tenant_creditworthiness", "Tenant Credit Information", 5),
    ("9_option_documentation", "Lease Option Documentation", 10),
    ("10_historical_consistency", "Historical Consistency", 10),
)

# Operating-statement dimensions (new; same contract).
T12_DIMENSIONS = (
    ("t12_1_period_integrity", "Period Integrity", 20),
    ("t12_2_account_mapping", "Account Mapping Coverage", 20),
    ("t12_3_sign_convention", "Sign Convention Consistency", 15),
    ("t12_4_noi_consistency", "NOI Classification Consistency", 20),
    ("t12_5_duplicate_detection", "Duplicate / Subtotal Detection", 10),
    ("t12_6_provenance", "Provenance Coverage", 15),
)

# Reconciliation dimensions (new; same contract).
TIEOUT_DIMENSIONS = (
    ("tie_1_base_rent", "Base Rent Tie-Out", 25),
    ("tie_2_recoveries", "Recoveries Tie-Out", 15),
    ("tie_3_other_income", "Other Income Tie-Out", 10),
    ("tie_4_occupancy", "Occupancy Tie-Out", 15),
    ("tie_5_egi_bridge", "EGI / NOI-Revenue Bridge", 25),
    ("tie_6_residual", "Residual Unexplained", 10),
)

DIMENSION_SETS = {
    "rent_roll": RENT_ROLL_DIMENSIONS,
    "t12": T12_DIMENSIONS,
    "operating_statement": T12_DIMENSIONS,
    "rent_roll_t12_tieout": TIEOUT_DIMENSIONS,
}

# Numeric gates (0-100, secondary to the weakest-link letter grade).
MERGE_GATE = 85
PROD_GATE = 92

# Critical validation failures. Any of these forces a hard block regardless of
# the numeric score. A PII-redaction breach is NON-OVERRIDABLE: it cannot be
# waived even as a documented fixture limitation.
CRITICAL_FAILURES = (
    "pii_redaction_breach",          # non-overridable
    "rent_arithmetic_contradiction",
    "negative_or_zero_rent_occupied",
    "t12_period_count_invalid",
    "vacant_unit_active_lease",
    "lease_expiry_before_start",
    "forced_tie_out",
    "confidence_below_floor",
    "noi_includes_below_the_line",
)
NON_OVERRIDABLE_CRITICAL = ("pii_redaction_breach",)


def weakest_link(grades: dict) -> str:
    """Overall letter = the lowest grade across all scored dimensions."""
    if not grades:
        return "C"
    order = {"A": 3, "B": 2, "C": 1}
    worst = min(order.get(g, 1) for g in grades.values())
    for letter, rank in order.items():
        if rank == worst:
            return letter
    return "C"


def weighted_score(grades: dict, dimensions: tuple) -> float:
    """A=3/B=2/C=1 weighted by dimension weight, normalized to /3 like the
    YAML's ``weighted_score`` example. Re-weights to only the dimensions
    actually graded, so an N/A dimension (e.g. reconciliation with no paired
    rent roll) is excluded rather than scored zero."""
    weights = {k: w for (k, _name, w) in dimensions}
    present = [k for k in grades if k in weights]
    total_w = sum(weights[k] for k in present) or 1
    acc = sum(GRADE_POINTS.get(grades[k], 1) * weights[k] for k in present)
    return round(acc / total_w, 4)


def score_100(grades: dict, dimensions: tuple) -> float:
    """The /3 weighted score expressed on a 0-100 scale for the merge gate."""
    return round(weighted_score(grades, dimensions) / 3.0 * 100.0, 2)


def gate(letter: str, numeric: float, criticals: list) -> dict:
    """Resolve the merge/prod gate. Weakest-link letter is primary; the 0-100
    score is secondary; any critical failure blocks; a PII breach is a hard,
    non-overridable block."""
    crit = [c for c in (criticals or []) if c]
    pii_breach = any(c in NON_OVERRIDABLE_CRITICAL for c in crit)
    merge_ok = (letter in ("A", "B")) and (numeric >= MERGE_GATE) and not crit
    prod_ok = (letter == "A") and (numeric >= PROD_GATE) and not crit
    return {
        "weakest_link_grade": letter,
        "score_100": numeric,
        "critical_failures": crit,
        "pii_redaction_breach": pii_breach,
        "merge_ready": bool(merge_ok),
        "production_ready": bool(prod_ok),
        "blocked": bool(crit),
        "merge_gate": MERGE_GATE,
        "prod_gate": PROD_GATE,
        "rubric_version": RUBRIC_VERSION,
    }


def grade_from_pass_rate(pass_rate: float) -> str:
    """Helper to letter-grade a 0..1 pass rate when a dimension has no bespoke
    rule (>=0.97 -> A, >=0.85 -> B, else C)."""
    if pass_rate >= 0.97:
        return "A"
    if pass_rate >= 0.85:
        return "B"
    return "C"
