"""Canonical chart of accounts + charge-code / account mapping.

This MIRRORS the existing residential-multifamily GL master data so the
ingestion family does not fork a second chart of accounts:

- canonical slugs and their GL source ids come from
  ``src/skills/residential_multifamily/reference/connectors/master_data/account_crosswalk.yaml``
- ``account_type`` / ``normal_balance`` enums come from
  ``src/skills/residential_multifamily/reference/connectors/gl/schema.yaml``

Parity with those YAML files is enforced by
``tests/test_ingestion_canonical_sources.py`` (a sync test that loads the YAML
and fails if these constants drift). That keeps the single-source-of-truth
posture (ADR-0001) while letting the calculators stay stdlib-only.
"""
from __future__ import annotations

from typing import Any

# Paths (relative to repo root) the sync test reads to enforce parity.
CROSSWALK_PATH = (
    "src/skills/residential_multifamily/reference/connectors/master_data/account_crosswalk.yaml"
)
GL_SCHEMA_PATH = "src/skills/residential_multifamily/reference/connectors/gl/schema.yaml"

ACCOUNT_TYPES = ("asset", "liability", "equity", "revenue", "expense", "capex")
NORMAL_BALANCE = ("debit", "credit")

# Canonical account slugs (corporate_gl set from the crosswalk) with the
# account_type / normal_balance that the GL schema assigns to each type.
CANONICAL_ACCOUNTS: dict = {
    "revenue_base_rent": {"account_type": "revenue", "normal_balance": "credit", "gl_source_id": "4000"},
    "revenue_other_rental": {"account_type": "revenue", "normal_balance": "credit", "gl_source_id": "4100"},
    "revenue_other_non_rental": {"account_type": "revenue", "normal_balance": "credit", "gl_source_id": "4200"},
    "expense_payroll": {"account_type": "expense", "normal_balance": "debit", "gl_source_id": "6000"},
    "expense_contract_labor": {"account_type": "expense", "normal_balance": "debit", "gl_source_id": "6050"},
    "expense_repairs_maintenance": {"account_type": "expense", "normal_balance": "debit", "gl_source_id": "6100"},
    "expense_turn": {"account_type": "expense", "normal_balance": "debit", "gl_source_id": "6150"},
    "capex_component_replacement": {"account_type": "capex", "normal_balance": "debit", "gl_source_id": "7100"},
    "capex_value_add": {"account_type": "capex", "normal_balance": "debit", "gl_source_id": "7200"},
    "capex_compliance_life_safety": {"account_type": "capex", "normal_balance": "debit", "gl_source_id": "7300"},
}

# Which statement section a canonical account belongs to (keeps capex out of NOI).
ACCOUNT_SECTION = {
    "revenue_base_rent": "revenue",
    "revenue_other_rental": "revenue",
    "revenue_other_non_rental": "revenue",
    "expense_payroll": "operating_expense",
    "expense_contract_labor": "operating_expense",
    "expense_repairs_maintenance": "operating_expense",
    "expense_turn": "operating_expense",
    "capex_component_replacement": "capex",
    "capex_value_add": "capex",
    "capex_compliance_life_safety": "capex",
}

# Common real-world rent-roll charge CODES -> canonical charge_category.
# A direct code or alias match is high-confidence; everything else falls to
# description inference (medium) or the human-review queue (unmapped).
CHARGE_CODE_ALIASES = {
    "rent": "base_rent", "base": "base_rent", "base rent": "base_rent", "br": "base_rent",
    "rnt": "base_rent", "min rent": "base_rent", "minimum rent": "base_rent", "fixed rent": "base_rent",
    "cam": "cam_recovery", "oe": "cam_recovery", "opex": "cam_recovery", "cam rec": "cam_recovery",
    "camrec": "cam_recovery", "common area": "cam_recovery",
    "ret": "tax_recovery", "tax": "tax_recovery", "re tax": "tax_recovery", "ret rec": "tax_recovery",
    "tax rec": "tax_recovery",
    "ins": "insurance_recovery", "insurance": "insurance_recovery", "ins rec": "insurance_recovery",
    "pct": "percentage_rent", "percent": "percentage_rent", "overage": "percentage_rent",
    "pct rent": "percentage_rent", "% rent": "percentage_rent",
    "pkg": "parking", "park": "parking", "parking": "parking", "garage": "parking",
    "stor": "storage", "storage": "storage", "locker": "storage",
}

# A rent-roll charge category maps to a canonical revenue account.
CHARGE_CATEGORY_TO_ACCOUNT = {
    "base_rent": "revenue_base_rent",
    "cam_recovery": "revenue_other_rental",
    "tax_recovery": "revenue_other_rental",
    "insurance_recovery": "revenue_other_rental",
    "percentage_rent": "revenue_other_rental",
    "parking": "revenue_other_rental",
    "storage": "revenue_other_rental",
    "other_recurring": "revenue_other_rental",
    "one_time_amortized": "revenue_other_non_rental",
}

# Deterministic keyword -> charge_category inference when a charge CODE is
# absent but a DESCRIPTION exists. Ordered most-specific first.
_CHARGE_DESCRIPTION_KEYWORDS = (
    ("base_rent", ("base rent", "minimum rent", "fixed rent", "rent ")),
    ("cam_recovery", ("cam", "common area", "opex recovery", "operating expense recovery")),
    ("tax_recovery", ("tax recovery", "ret recovery", "real estate tax", "property tax recover")),
    ("insurance_recovery", ("insurance recovery", "insurance reimburse")),
    ("percentage_rent", ("percentage rent", "overage", "pct rent", "% rent")),
    ("parking", ("parking", "garage")),
    ("storage", ("storage", "locker")),
    ("one_time_amortized", ("ti repayment", "amortized", "buildout repay", "one-time", "one time")),
    ("other_recurring", ("pet", "utility", "tech package", "valet", "trash", "late fee", "other")),
)

# Deterministic keyword -> canonical account inference for T-12 line names.
_ACCOUNT_NAME_KEYWORDS = (
    ("revenue_base_rent", ("gross potential rent", "base rent", "rental income - base", "minimum rent")),
    ("revenue_other_rental", ("other rental", "parking", "storage", "cam income", "recovery income", "reimbursement")),
    ("revenue_other_non_rental", ("other income", "late fee", "nsf", "application fee", "damage recovery")),
    ("expense_payroll", ("payroll", "salaries", "on-site staff", "wages")),
    ("expense_contract_labor", ("contract labor", "contractor")),
    ("expense_repairs_maintenance", ("repairs", "maintenance", "r&m", "r & m")),
    ("expense_turn", ("turn", "make ready", "make-ready")),
    ("capex_component_replacement", ("component replacement", "roof", "hvac replace", "capital replacement")),
    ("capex_value_add", ("value-add", "value add", "renovation", "unit upgrade")),
    ("capex_compliance_life_safety", ("life safety", "ada", "fire", "compliance capex")),
)


def _match_keywords(text: str, table: tuple) -> str | None:
    low = (text or "").strip().lower()
    if not low:
        return None
    for canonical, needles in table:
        for needle in needles:
            if needle in low:
                return canonical
    return None


def map_charge_code(charge_code: Any, description: Any) -> dict:
    """Map a rent-roll charge to a canonical account.

    Returns a deterministic record. When a charge_code maps directly we report
    high confidence; when only a description matches we infer with medium
    confidence and flag for review; when nothing matches we DO NOT guess --
    the row is routed to human review (``needs_review=True``).
    """
    code = (str(charge_code).strip() if charge_code not in (None, "") else None)
    desc = description or ""

    # 1) Direct charge_category match (the code IS already a known category).
    category = None
    method = None
    confidence = "low"
    code_l = code.lower() if code else None
    if code_l and code_l in CHARGE_CATEGORY_TO_ACCOUNT:
        category = code_l
        method = "direct_code"
        confidence = "high"
    elif code_l and code_l in CHARGE_CODE_ALIASES:
        # 2) Known charge-code alias (e.g. "CAM", "RENT", "RET").
        category = CHARGE_CODE_ALIASES[code_l]
        method = "code_alias"
        confidence = "high"
    else:
        # 3) Description-keyword inference.
        category = _match_keywords(desc, _CHARGE_DESCRIPTION_KEYWORDS)
        if category:
            method = "description_inference"
            confidence = "medium"

    if not category:
        return {
            "charge_code": code,
            "charge_category": None,
            "canonical_account": None,
            "account_type": None,
            "normal_balance": None,
            "method": "unmapped",
            "confidence": "low",
            "needs_review": True,
        }

    account = CHARGE_CATEGORY_TO_ACCOUNT[category]
    meta = CANONICAL_ACCOUNTS[account]
    return {
        "charge_code": code,
        "charge_category": category,
        "canonical_account": account,
        "account_type": meta["account_type"],
        "normal_balance": meta["normal_balance"],
        "method": method,
        "confidence": confidence,
        "needs_review": confidence != "high",
    }


def map_account(account_code: Any, account_name: Any) -> dict:
    """Map a T-12 / operating-statement line to a canonical account.

    Account code (if a known GL id) wins; otherwise infer from the name.
    Unmapped lines accumulate to an ``unmapped`` bucket and are flagged --
    never rejected (mirrors the connectors' unmapped_account_handling runbook).
    """
    code = (str(account_code).strip() if account_code not in (None, "") else None)
    name = account_name or ""

    canonical = None
    method = None
    confidence = "low"

    if code:
        for slug, meta in CANONICAL_ACCOUNTS.items():
            if meta["gl_source_id"] == code:
                canonical = slug
                method = "direct_code"
                confidence = "high"
                break

    if not canonical:
        canonical = _match_keywords(name, _ACCOUNT_NAME_KEYWORDS)
        if canonical:
            method = "name_inference"
            confidence = "medium"

    if not canonical:
        return {
            "account_code": code,
            "canonical_account": "unmapped",
            "account_type": None,
            "normal_balance": None,
            "statement_section": None,
            "method": "unmapped",
            "confidence": "low",
            "needs_review": True,
        }

    meta = CANONICAL_ACCOUNTS[canonical]
    return {
        "account_code": code,
        "canonical_account": canonical,
        "account_type": meta["account_type"],
        "normal_balance": meta["normal_balance"],
        "statement_section": ACCOUNT_SECTION[canonical],
        "method": method,
        "confidence": confidence,
        "needs_review": confidence != "high",
    }
