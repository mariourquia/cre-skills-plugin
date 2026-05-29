#!/usr/bin/env python3
"""
Document-to-Database: Token Normalizer
======================================
Transforms a tokenized/extracted CRE document (rent roll, T-12, or operating
statement) into canonical, typed, provenance-stamped records that downstream
ingestion calculators consume.

Behavioral selectors travel INSIDE the --json payload (doc_type, run_id, as_of,
tenant_id), never as argv flags, so the calculator is fully driveable through
the orchestrator bridge / calculator-invoker (which pass only --json) and is
unit-testable as a pure calculate_normalize_tokens(dict)->dict.

Reuses the shared ingest/ package: canonical charge categories + account
mapping, the PII boundary (tenant identity pseudonymized; natural-person names
never emitted), and the provenance bundle (superset of the 8-column warehouse
contract). Pure + deterministic: same input dict -> byte-identical JSON.

Used by: document-to-database, rent-roll-to-database, t12-to-database,
         operating-statement-to-database

Usage:
    python3 src/calculators/normalize_tokens.py --json '{
        "doc_type": "rent_roll",
        "run_id": "RUN-1", "as_of": "2026-05-29", "tenant_id": "demo-fund",
        "source": {"document_id": "RR-001", "document_type": "rent_roll"},
        "property": {"property_id": "P1", "rentable_sf": 100000},
        "rows": [{"row_number": 1, "unit": "101", "rentable_sf": 850,
                  "unit_status": "occupied", "lease_status": "active",
                  "lease_start": "2024-01-01", "lease_expire": "2026-12-31",
                  "charges": [{"charge_code": "base_rent", "monthly_amount": 1700,
                               "annual_amount": 20400, "frequency": "monthly"}]}]
    }'

Output: JSON canonical payload {doc_type, records, leases, units, aggregates,
        periods, issues, skill, skill_version}.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from ingest import accounts, determinism as det, pii, provenance as prov, schema

SKILL_VERSION = "0.1.0"


# --------------------------------------------------------------------------
# Dispatch
# --------------------------------------------------------------------------
def detect_doc_type(inputs: dict) -> str:
    dt = (inputs.get("doc_type") or "auto").strip().lower()
    if dt in ("rent_roll", "t12", "operating_statement"):
        return dt
    # auto: rows with charges -> rent roll; lines with amounts -> t12.
    if inputs.get("rows"):
        return "rent_roll"
    if inputs.get("lines"):
        return "t12"
    return "rent_roll"


def calculate_normalize_tokens(inputs: dict) -> dict:
    ctx = det.resolve_context(inputs)
    errs = det.require_context(ctx)
    errs += pii.assert_safe_tenant_id(ctx["tenant_id"])
    if errs:
        return det.error_result("invalid run context", details=errs)

    doc_type = detect_doc_type(inputs)
    if doc_type == "rent_roll":
        return normalize_rent_roll(inputs, ctx)
    return normalize_operating_statement(inputs, ctx, doc_type)


# --------------------------------------------------------------------------
# Rent roll
# --------------------------------------------------------------------------
def normalize_rent_roll(inputs: dict, ctx: dict) -> dict:
    source = inputs.get("source") or {}
    doc_id = source.get("document_id", "RR-UNKNOWN")
    prop = inputs.get("property") or {}
    rows = inputs.get("rows") or []

    units: list = []
    leases: list = []
    charge_lines: list = []
    issues: list = []

    gpr_in_place = 0.0
    gpr_market = 0.0
    occupied_units = 0
    revenue_units = 0
    total_units = 0

    for row in rows:
        rn = row.get("row_number")
        unit_id = str(row.get("unit") or row.get("suite") or ("row-%s" % rn))
        unit_status = (row.get("unit_status") or "occupied").strip().lower()
        lease_status = (row.get("lease_status") or "active").strip().lower()
        rsf = _num(row.get("rentable_sf"))

        if unit_status not in schema.UNIT_STATUS:
            issues.append(_issue("unit_status_unknown", "warn", "rows[%s].unit_status" % rn,
                                 "Unknown unit_status '%s'; routed to review." % unit_status))
        if rsf is not None and rsf < 0:
            issues.append(_issue("negative_sf", "critical", "rows[%s].rentable_sf" % rn,
                                 "Rentable SF is negative."))

        is_revenue_unit = unit_status not in schema.NON_REVENUE_UNIT_STATUS
        if is_revenue_unit:
            total_units += 1
        if unit_status == "occupied":
            occupied_units += 1
            revenue_units += 1
        elif unit_status == "leased_not_occupied":
            revenue_units += 1

        # Tenant identity is pseudonymized; the raw name is NEVER emitted.
        raw_name = row.get("tenant_name")
        tenant_code = (
            pii.pseudonymize(raw_name, ctx["run_id"]) if raw_name else None
        )

        # Structural lease validations.
        ls, le = row.get("lease_start"), row.get("lease_expire")
        if ls and le and str(le) < str(ls):
            issues.append(_issue("lease_expiry_before_start", "critical",
                                 "rows[%s]" % rn, "Lease expiry precedes start."))
        if unit_status == "occupied" and lease_status not in ("active", "mtm", "holdover", "in_default"):
            issues.append(_issue("occupied_without_active_lease", "warn", "rows[%s]" % rn,
                                 "Occupied unit without an active lease status."))
        # vacant_available must not carry an active lease / in-place charges.
        active_charges = [c for c in (row.get("charges") or []) if _num(c.get("monthly_amount"))]
        if unit_status == "vacant_available" and (lease_status == "active" or active_charges):
            issues.append(_issue("vacant_unit_active_lease", "critical", "rows[%s]" % rn,
                                 "vacant_available unit carries an active lease or in-place charges."))

        lease_id = str(row.get("lease_id") or ("L-%s" % unit_id))
        free_rent = _num(row.get("free_rent_months")) or 0

        units.append({
            "unit_id": unit_id, "property_id": prop.get("property_id"),
            "building": row.get("building"), "floor": row.get("floor"),
            "suite": row.get("suite"), "unit_type": row.get("unit_type"),
            "rentable_sf": rsf, "unit_status": unit_status,
        })
        leases.append({
            "lease_id": lease_id, "unit_id": unit_id, "tenant_code": tenant_code,
            "lease_status": lease_status, "lease_type": row.get("lease_type"),
            "lease_start": ls, "lease_expire": le,
            "recovery_method": row.get("recovery_method"),
            "base_year": row.get("base_year"), "expense_stop_psf": _num(row.get("expense_stop_psf")),
            "free_rent_months": free_rent, "security_deposit": _num(row.get("security_deposit")),
            "escalation": row.get("escalation"),
            # Only free rent / abatement (or an in-period step) breaks the
            # current-period annual==monthly*12 identity. A future-dated
            # escalation does NOT, so it must not skip the arithmetic check.
            "has_step_or_abatement": bool(free_rent) or bool(row.get("in_period_step")),
        })

        # Charge schedule lines (multi-line, by category).
        for ci, ch in enumerate(row.get("charges") or []):
            mapping = accounts.map_charge_code(ch.get("charge_code"), ch.get("description"))
            if mapping["needs_review"]:
                issues.append(_issue("charge_code_unmapped" if mapping["charge_category"] is None
                                     else "charge_code_inferred",
                                     "warn", "rows[%s].charges[%s]" % (rn, ci),
                                     "Charge mapped via %s (confidence %s)." % (mapping["method"], mapping["confidence"])))
            monthly = _num(ch.get("monthly_amount"))
            annual = _num(ch.get("annual_amount"))
            line = schema.charge_schedule_line(
                lease_id=lease_id, charge_code=ch.get("charge_code"),
                charge_category=mapping["charge_category"] or "other_recurring",
                monthly_amount=monthly, annual_amount=annual,
                period_start=ch.get("effective_start"), period_end=ch.get("effective_end"),
                frequency=(ch.get("frequency") or "monthly"),
                is_recoverable=bool(ch.get("is_recoverable")),
                is_estimate=bool(ch.get("is_estimate")),
                psf_basis=det.safe_div(annual, rsf) if (annual and rsf) else None,
            )
            line["canonical_account"] = mapping["canonical_account"]
            line["map_confidence"] = mapping["confidence"]
            line["provenance"] = prov.build_provenance(
                field_name="charge_%s" % (mapping["charge_category"] or "other"),
                source_document_id=doc_id, source_ref_anchor="charge",
                skill_name="rent-roll-to-database", skill_version=SKILL_VERSION,
                run_id=ctx["run_id"], as_of=ctx["as_of"],
                classification="source-fact",
                confidence=mapping["confidence"], review_status="needs-review" if mapping["needs_review"] else "accepted",
                tenant_id=ctx["tenant_id"], source_document_type="rent_roll",
                source_row_number=rn, source_table_id=(source.get("table_id")),
            )
            charge_lines.append(line)

            # in-place GPR from base rent charge lines on occupied/lno units.
            if mapping["charge_category"] == "base_rent" and is_revenue_unit and monthly:
                gpr_in_place += monthly * 12
            mkt = _num(ch.get("market_monthly_amount"))
            if mapping["charge_category"] == "base_rent" and mkt:
                gpr_market += mkt * 12

    aggregates = {
        "total_units": total_units,
        "occupied_units": occupied_units,
        "revenue_units": revenue_units,
        "physical_occupancy_pct": det.rnd_pct((occupied_units / total_units * 100) if total_units else 0.0),
        "gpr_in_place_annual": det.rnd_money(gpr_in_place),
        "gpr_market_annual": det.rnd_money(gpr_market) if gpr_market else None,
        "as_of": ctx["as_of"],
    }

    return _payload("rent_roll", ctx, prop, issues,
                    records=charge_lines, leases=leases, units=units,
                    aggregates=aggregates, skill="rent-roll-to-database")


# --------------------------------------------------------------------------
# T-12 / operating statement
# --------------------------------------------------------------------------
def normalize_operating_statement(inputs: dict, ctx: dict, doc_type: str) -> dict:
    source = inputs.get("source") or {}
    doc_id = source.get("document_id", "T12-UNKNOWN")
    prop = inputs.get("property") or {}
    lines_in = inputs.get("lines") or []
    declared_periods = inputs.get("periods") or []
    aggregate_cols = set(c.lower() for c in (inputs.get("aggregate_columns") or ["total", "ytd", "annual", "annualized"]))

    # Detect the period set, EXCLUDING Total/YTD/annualized aggregate columns.
    period_set: list = []
    for p in declared_periods:
        if str(p).strip().lower() in aggregate_cols:
            continue
        period_set.append(p)
    if not period_set:
        # derive from the first line's amounts keys, excluding aggregate cols
        for ln in lines_in:
            for k in (ln.get("amounts") or {}).keys():
                if str(k).strip().lower() in aggregate_cols:
                    continue
                if k not in period_set:
                    period_set.append(k)
            if period_set:
                break

    issues: list = []
    expected_periods = inputs.get("periods_expected", 12 if doc_type == "t12" else None)
    if doc_type == "t12":
        if len(period_set) < 12:
            issues.append(_issue("partial_year", "warn", "periods",
                                 "Only %d monthly periods present (expected 12); partial-year/lease-up. "
                                 "Annualization carried as a gap, not synthesized." % len(period_set)))
        elif len(period_set) > 12:
            issues.append(_issue("t12_period_count_invalid", "critical", "periods",
                                 "%d periods present; >12 suggests an aggregate column was not excluded." % len(period_set)))

    # Sign convention detection.
    sign_conv = (inputs.get("expense_sign_convention") or "positive_magnitude").strip().lower()
    if sign_conv not in schema.EXPENSE_SIGN_CONVENTIONS:
        sign_conv = "positive_magnitude"

    os_lines: list = []
    seen_accounts: dict = {}
    section_totals: dict = {"revenue": 0.0, "operating_expense": 0.0,
                            "below_the_line_noi": 0.0, "capex": 0.0,
                            "debt_service": 0.0, "distribution": 0.0}

    for li, ln in enumerate(lines_in):
        mapping = accounts.map_account(ln.get("account_code"), ln.get("account_name"))
        section = ln.get("statement_section") or mapping["statement_section"] or "operating_expense"
        line_type = (ln.get("line_type") or "actual").strip().lower()
        if line_type not in schema.LINE_TYPES:
            issues.append(_issue("line_type_unknown", "warn", "lines[%s].line_type" % li,
                                 "Unknown line_type '%s'." % line_type))
        if mapping["needs_review"]:
            issues.append(_issue("account_unmapped" if mapping["canonical_account"] == "unmapped" else "account_inferred",
                                 "warn", "lines[%s]" % li,
                                 "Account mapped via %s (confidence %s)." % (mapping["method"], mapping["confidence"])))

        amounts = ln.get("amounts") or {}
        # Duplicate / subtotal detection key.
        dkey = (mapping["canonical_account"], line_type)
        seen_accounts.setdefault(dkey, 0)
        seen_accounts[dkey] += 1

        for period in period_set:
            raw_amt = _num(amounts.get(period))
            if raw_amt is None:
                continue
            amt = _normalize_sign(raw_amt, section, sign_conv)
            os_lines.append(schema.operating_statement_line(
                property_id=prop.get("property_id"),
                account_code=ln.get("account_code"),
                raw_account_name=ln.get("account_name", ""),
                canonical_account=mapping["canonical_account"],
                statement_section=section, line_type=line_type,
                fiscal_period=period, amount=det.rnd_money(amt),
            ))
            if line_type == "actual" and section in section_totals:
                section_totals[section] += amt

    # Duplicate account flagging.
    for (acct, lt), count in seen_accounts.items():
        if count > 1 and acct != "unmapped":
            issues.append(_issue("duplicate_account_line", "warn", "lines",
                                 "Account %s (%s) appears %d times; possible subtotal re-count." % (acct, lt, count)))

    noi = section_totals["revenue"] - section_totals["operating_expense"]
    aggregates = {
        "periods_present": len(period_set),
        "periods_expected": expected_periods,
        "expense_sign_convention": sign_conv,
        "revenue_actual": det.rnd_money(section_totals["revenue"]),
        "operating_expense_actual": det.rnd_money(section_totals["operating_expense"]),
        "noi_actual": det.rnd_money(noi),
        "as_of": ctx["as_of"],
    }
    return _payload(doc_type, ctx, prop, issues,
                    records=os_lines, leases=[], units=[],
                    aggregates=aggregates, periods=period_set,
                    skill="t12-to-database" if doc_type == "t12" else "operating-statement-to-database")


def _normalize_sign(amount: float, section: str, convention: str) -> float:
    """Normalize every amount to a canonical convention: revenue positive,
    expense/capex/debt as positive magnitudes (subtracted downstream)."""
    a = float(amount)
    if convention == "signed_negative":
        # expenses arrive negative -> take magnitude
        if section in ("operating_expense", "capex", "debt_service", "distribution"):
            return abs(a)
        return a
    if convention == "debit_credit_normal_balance":
        return abs(a)
    return abs(a) if section in ("operating_expense", "capex", "debt_service", "distribution") else a


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def _num(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        if isinstance(v, str):
            s = v.replace("$", "").replace(",", "").strip()
            if s.startswith("(") and s.endswith(")"):
                s = "-" + s[1:-1]
            return float(s)
        return float(v)
    except (TypeError, ValueError):
        return None


def _issue(code: str, severity: str, field_path: str, detail: str) -> dict:
    return {"code": code, "severity": severity, "field_path": field_path, "detail": detail}


def _payload(doc_type: str, ctx: dict, prop: dict, issues: list, **parts: Any) -> dict:
    out = {
        "doc_type": doc_type,
        "run_id": ctx["run_id"],
        "as_of": ctx["as_of"],
        "tenant_id_or_workspace_id": ctx["tenant_id"],
        "property": prop,
        "issues": issues,
        "skill_version": SKILL_VERSION,
    }
    out.update(parts)
    return out


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Token Normalizer")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_normalize_tokens(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
