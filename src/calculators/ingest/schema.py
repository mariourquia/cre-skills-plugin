"""Canonical field vocabulary for the document-to-database cash-flow spine.

The spine the family models (and the grains it preserves) is:

    property -> unit/suite/space -> tenant -> lease -> lease_term
             -> charge_schedule -> charge_code -> account_mapping
             -> monthly contractual cash flow
             -> T-12 / operating-statement account line
             -> NOI / cash-flow reporting

Field names deliberately REUSE the plugin's existing vocabulary so the new
executable layer does not fork the prose layer it sits beneath:

- lease/charge names mirror ``document-to-data-room-extractor``'s
  ``extraction-taxonomy.yaml`` (lease_economics) and the
  ``cam-reconciliation-calculator`` tenant recovery-terms schema.
- line types / sections mirror the GL ``schema.yaml`` actual/budget/forecast
  entities and the AMOS ``monthly-actuals`` below-the-line structure.
"""
from __future__ import annotations

from typing import Any

DOC_TYPES = ("rent_roll", "t12", "operating_statement", "auto")

# --- Charge schedule (rent roll) -------------------------------------------
# A lease carries MULTIPLE concurrent charge lines, not a single rent number.
CHARGE_CATEGORIES = (
    "base_rent",
    "cam_recovery",
    "tax_recovery",
    "insurance_recovery",
    "percentage_rent",
    "parking",
    "storage",
    "other_recurring",
    "one_time_amortized",
)

# Recovery method reuses extraction-taxonomy (nnn|modified_gross|full_service)
# extended with the cam-reconciliation lease_type variants.
RECOVERY_METHODS = (
    "nnn",
    "modified_gross",
    "full_service",
    "base_year_stop",
    "expense_stop",
)

ESCALATION_TYPES = ("fixed_pct", "fixed_dollar", "cpi", "fmv", "none")

BILLING_FREQUENCIES = ("monthly", "quarterly", "annual", "one_time")

# Unit status is NOT a binary vacant flag; institutional rolls distinguish:
UNIT_STATUS = (
    "occupied",
    "vacant_available",
    "leased_not_occupied",  # signed lease, not yet commenced
    "down",
    "model",
    "admin",
    "employee",
    "owner_occupied",
)

LEASE_STATUS = (
    "active",
    "mtm",
    "holdover",
    "in_default",
    "future_commencement",
    "terminated",
)

# Units excluded from occupancy / revenue denominators.
NON_REVENUE_UNIT_STATUS = ("down", "model", "admin", "employee", "owner_occupied")

# --- Operating statement ----------------------------------------------------
# line_type maps to the GL schema actual/budget/forecast entities.
LINE_TYPES = ("actual", "budget", "reforecast", "prior_year", "underwritten")

# statement_section keeps capex / debt service / distributions out of NOI.
STATEMENT_SECTIONS = (
    "revenue",
    "operating_expense",
    "below_the_line_noi",
    "capex",
    "debt_service",
    "distribution",
)

# Sign convention the source statement uses for expenses.
EXPENSE_SIGN_CONVENTIONS = ("positive_magnitude", "signed_negative", "debit_credit_normal_balance")

# --- Reconciliation ---------------------------------------------------------
# Difference buckets. "missing" (present in one source, absent in the other)
# is the most important and is NOT folded into timing.
DIFFERENCE_TYPES = ("mapping", "timing", "missing", "within_tolerance")
TIE_STATUS = ("tied", "untied")  # "forced" is impossible by construction.

# --- Shared classification / confidence ------------------------------------
CLASSIFICATIONS = ("source-fact", "calculated", "modeled-assumption", "requires-review")
CONFIDENCE_BANDS = ("high", "medium", "low")
REVIEW_STATUSES = ("accepted", "needs-review", "flagged")
VALIDATION_STATUSES = ("pass", "warn", "fail", "critical")


def in_enum(value: Any, enum: tuple) -> bool:
    return value in enum


def charge_schedule_line(
    *,
    lease_id: str,
    charge_code: str | None,
    charge_category: str,
    monthly_amount: float,
    annual_amount: float | None = None,
    period_start: str | None = None,
    period_end: str | None = None,
    frequency: str = "monthly",
    is_recoverable: bool = False,
    is_estimate: bool = False,
    psf_basis: float | None = None,
) -> dict:
    """Build one charge-schedule-line record (the charge grain)."""
    return {
        "lease_id": lease_id,
        "charge_code": charge_code,
        "charge_category": charge_category,
        "monthly_amount": monthly_amount,
        "annual_amount": annual_amount,
        "period_start": period_start,
        "period_end": period_end,
        "frequency": frequency,
        "is_recoverable": is_recoverable,
        "is_estimate": is_estimate,
        "psf_basis": psf_basis,
    }


def operating_statement_line(
    *,
    property_id: str,
    account_code: str | None,
    raw_account_name: str,
    canonical_account: str | None,
    statement_section: str,
    line_type: str,
    fiscal_period: str | None,
    amount: float,
) -> dict:
    """Build one operating-statement-line record (account x period grain)."""
    return {
        "property_id": property_id,
        "account_code": account_code,
        "raw_account_name": raw_account_name,
        "canonical_account": canonical_account,
        "statement_section": statement_section,
        "line_type": line_type,
        "fiscal_period": fiscal_period,  # YYYY-MM, reuses monthly-actuals `period`
        "amount": amount,
    }
