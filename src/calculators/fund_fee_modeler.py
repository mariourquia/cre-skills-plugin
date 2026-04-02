#!/usr/bin/env python3
"""
Fund Fee Modeler
================
Models blended management fee economics for institutional fund raises.
Calculates weighted-average fee rates, MFN cascade impacts, GP promote
sensitivity, and breakeven fund sizes across multi-close LP pipelines.

Used by: fund-raise-negotiation-engine skill

Commands:
    dashboard    -- Full fund raise dashboard (default)
    scenario     -- What-if analysis for a proposed LP concession
    mfn-audit    -- Full MFN cascade analysis
    export-csv   -- Export LP ledger to CSV
    import-csv   -- Import LP data from CSV and merge with state

Usage:
    # Full dashboard
    python3 scripts/calculators/fund_fee_modeler.py --command dashboard \\
        --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

    # Scenario: what if CalPERS gets 1.10%?
    python3 scripts/calculators/fund_fee_modeler.py --command scenario \\
        --lp-id calpers-001 --proposed-fee 0.011 \\
        --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

    # Scenario with full proposed terms
    python3 scripts/calculators/fund_fee_modeler.py --command scenario \\
        --lp-id calpers-001 \\
        --proposed-terms '{"managementFee": 0.011, "feeHoliday": {"months": 6}}' \\
        --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

    # MFN audit
    python3 scripts/calculators/fund_fee_modeler.py --command mfn-audit \\
        --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

    # Export to CSV
    python3 scripts/calculators/fund_fee_modeler.py --command export-csv \\
        --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

    # Import from CSV (merge into existing state)
    python3 scripts/calculators/fund_fee_modeler.py --command import-csv \\
        --csv fund-v-ledger.csv \\
        --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

    # JSON output instead of formatted text
    python3 scripts/calculators/fund_fee_modeler.py --command dashboard \\
        --format json --json "$(cat state.json)"

Input: Full fund state file JSON via --json argument or stdin.
Output: Structured JSON (--format json) or formatted text (default).
"""

import argparse
import csv
import io
import json
import math
import sys
from datetime import datetime
from typing import Any


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt_dollars(amount: float) -> str:
    """Format a dollar amount with commas and no decimals for large values."""
    if abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:,.1f}M"
    if abs(amount) >= 1_000:
        return f"${amount:,.0f}"
    return f"${amount:,.2f}"


def _fmt_pct(rate: float) -> str:
    """Format a decimal rate as a percentage with two decimal places."""
    return f"{rate * 100:.2f}%"


def _fmt_bps(rate: float) -> str:
    """Format a decimal rate as basis points."""
    return f"{rate * 10000:.0f} bps"


def _safe_get(d: dict, *keys: str, default: Any = None) -> Any:
    """Safely traverse nested dict keys."""
    current = d
    for k in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(k, default)
        if current is None:
            return default
    return current


def _get_standard_fee(state: dict) -> float:
    """Return the standard management fee rate from fund terms."""
    return _safe_get(state, "standardTerms", "managementFee", default=0.015)


def _get_fund_term(state: dict) -> int:
    """Return fund term in years."""
    return _safe_get(state, "standardTerms", "fundTerm", default=10)


def _get_investment_period(state: dict) -> int:
    """Return investment period in years."""
    return _safe_get(state, "standardTerms", "investmentPeriod", default=5)


def _get_pref_return(state: dict) -> float:
    """Return the preferred return (hurdle rate)."""
    return _safe_get(state, "standardTerms", "preferredReturn", default=0.08)


def _get_carry(state: dict) -> float:
    """Return GP carry rate."""
    return _safe_get(state, "standardTerms", "carry", default=0.20)


# ---------------------------------------------------------------------------
# Core: Effective fee rate per LP
# ---------------------------------------------------------------------------

def _effective_fee_rate(investor: dict, state: dict) -> float:
    """
    Compute the effective annual management fee rate for a single LP.

    Accounts for:
      - Negotiated flat rate vs standard
      - Management fee tiers (weighted by commitment)
      - Fee holiday amortization over fund term
      - Early closer discount from assigned close
      - Blended rate across fund family
      - Fee waiver (full or partial)
    """
    terms = investor.get("negotiatedTerms") or {}
    commitment = investor.get("commitment", 0)
    fund_term_months = _get_fund_term(state) * 12

    # Fee waiver overrides everything
    waiver = terms.get("feeWaiver")
    if waiver:
        if waiver.get("type") == "full":
            return 0.0
        if waiver.get("type") == "partial" and waiver.get("rate") is not None:
            return waiver["rate"]

    # Blended rate across fund family overrides per-fund rate
    blended_family = terms.get("blendedRateAcrossFunds")
    if blended_family and blended_family.get("enabled") and blended_family.get("blendedRate") is not None:
        base_rate = blended_family["blendedRate"]
    elif terms.get("managementFeeTiers") and commitment > 0:
        # Tiered fee schedule: compute commitment-weighted effective rate
        tiers = sorted(terms["managementFeeTiers"], key=lambda t: t.get("upTo", float("inf")))
        remaining = commitment
        weighted_fee = 0.0
        prev_boundary = 0
        for tier in tiers:
            boundary = tier.get("upTo", float("inf"))
            tranche = min(remaining, boundary - prev_boundary)
            if tranche <= 0:
                break
            weighted_fee += tranche * tier["rate"]
            remaining -= tranche
            prev_boundary = boundary
        # Any commitment above the highest tier boundary uses the last tier rate
        if remaining > 0 and tiers:
            weighted_fee += remaining * tiers[-1]["rate"]
        base_rate = weighted_fee / commitment if commitment > 0 else _get_standard_fee(state)
    elif terms.get("managementFee") is not None:
        base_rate = terms["managementFee"]
    else:
        base_rate = _get_standard_fee(state)

    # Fee holiday amortization
    holiday = terms.get("feeHoliday")
    if holiday and holiday.get("months", 0) > 0 and fund_term_months > 0:
        holiday_months = holiday["months"]
        base_rate = base_rate * (fund_term_months - holiday_months) / fund_term_months

    # Early closer discount
    target_close_id = investor.get("targetClose")
    if target_close_id:
        closes = state.get("closes", [])
        for close in closes:
            if close.get("closeId") == target_close_id:
                discount = close.get("earlyCloserDiscount", 0)
                if discount > 0:
                    base_rate -= discount
                break

    return max(base_rate, 0.0)


# ---------------------------------------------------------------------------
# Core: Blended fee
# ---------------------------------------------------------------------------

COMMITTED_STATUSES = {"signed", "funded"}
PIPELINE_STATUSES = {"signed", "funded", "verbal_commit"}
ALL_ACTIVE_STATUSES = {"signed", "funded", "verbal_commit", "in_negotiation", "prospect", "re_opened"}


def blended_fee(investors: list[dict], state: dict, statuses: set[str]) -> dict[str, Any]:
    """
    Compute commitment-weighted blended management fee rate for LPs in the
    given statuses.

    Returns:
        {
            "blended_rate": float,
            "total_commitment": float,
            "lp_count": int,
            "standard_rate": float,
            "delta_bps": float,
            "annual_revenue_standard": float,
            "annual_revenue_blended": float,
            "concession_cost": float,
            "per_lp": [{"lpId", "name", "commitment", "effective_rate", "annual_fee"}]
        }
    """
    standard_rate = _get_standard_fee(state)
    total_commitment = 0.0
    weighted_fee_sum = 0.0
    per_lp: list[dict] = []

    for inv in investors:
        if inv.get("status") not in statuses:
            continue
        commitment = inv.get("commitment", 0)
        if commitment <= 0:
            continue
        eff_rate = _effective_fee_rate(inv, state)
        total_commitment += commitment
        weighted_fee_sum += commitment * eff_rate
        annual_fee = commitment * eff_rate
        per_lp.append({
            "lpId": inv.get("lpId", ""),
            "name": inv.get("name", ""),
            "commitment": commitment,
            "effective_rate": round(eff_rate, 6),
            "annual_fee": round(annual_fee, 2),
        })

    blended_rate = weighted_fee_sum / total_commitment if total_commitment > 0 else standard_rate
    annual_standard = total_commitment * standard_rate
    annual_blended = weighted_fee_sum
    delta_bps = (blended_rate - standard_rate) * 10000

    return {
        "blended_rate": round(blended_rate, 6),
        "total_commitment": round(total_commitment, 2),
        "lp_count": len(per_lp),
        "standard_rate": standard_rate,
        "delta_bps": round(delta_bps, 1),
        "annual_revenue_standard": round(annual_standard, 2),
        "annual_revenue_blended": round(annual_blended, 2),
        "concession_cost": round(annual_blended - annual_standard, 2),
        "per_lp": per_lp,
    }


# ---------------------------------------------------------------------------
# Core: MFN cascade
# ---------------------------------------------------------------------------

def _is_mfn_excluded(investor: dict, mfn_prov: dict) -> bool:
    """Check whether an LP is excluded from MFN scope."""
    tier = investor.get("tier", "standard")
    inv_type = investor.get("type", "")
    commitment = investor.get("commitment", 0)

    if mfn_prov.get("excludeGPAffiliates") and inv_type == "gp_affiliate":
        return True
    if mfn_prov.get("excludeFoundingLPs") and tier == "seed":
        return True
    if mfn_prov.get("excludeAnchorLPs") and tier == "anchor":
        return True

    min_commit = mfn_prov.get("minimumCommitmentForMFN", 0)
    if min_commit > 0 and commitment < min_commit:
        return True

    return False


def mfn_cascade(
    investors: list[dict],
    mfn_provisions: dict,
    state: dict,
    proposed_change: dict | None = None,
) -> dict[str, Any]:
    """
    Compute MFN cascade: current floor, at-risk LPs, and per-LP ratchet cost.

    If proposed_change is provided ({"lpId": str, "proposed_rate": float}),
    simulate the cascade as if that LP received the proposed rate.

    Returns:
        {
            "enabled": bool,
            "floor_rate": float,
            "floor_setter": str,
            "floor_setter_id": str,
            "mfn_eligible_count": int,
            "ratchets": [{"lpId", "name", "current_rate", "ratchet_to", "cost_per_year"}],
            "total_cascade_cost": float,
            "total_ratchet_count": int,
        }
    """
    if not mfn_provisions.get("enabled", False):
        return {
            "enabled": False,
            "floor_rate": 0.0,
            "floor_setter": "",
            "floor_setter_id": "",
            "mfn_eligible_count": 0,
            "ratchets": [],
            "total_cascade_cost": 0.0,
            "total_ratchet_count": 0,
        }

    active_statuses = {"signed", "funded", "verbal_commit", "in_negotiation"}

    # Build rate map, applying proposed change if given
    rate_map: dict[str, float] = {}
    lp_map: dict[str, dict] = {}
    for inv in investors:
        if inv.get("status") not in active_statuses:
            continue
        lp_id = inv.get("lpId", "")
        lp_map[lp_id] = inv
        rate_map[lp_id] = _effective_fee_rate(inv, state)

    # Apply proposed change for simulation
    if proposed_change:
        target_id = proposed_change.get("lpId", "")
        proposed_rate = proposed_change.get("proposed_rate", 0)
        if target_id in rate_map:
            rate_map[target_id] = proposed_rate
        elif target_id:
            # LP may not be in active statuses yet; still model the floor
            rate_map[target_id] = proposed_rate
            # Create a stub for cost calculation
            for inv in investors:
                if inv.get("lpId") == target_id:
                    lp_map[target_id] = inv
                    break

    # Find floor: lowest rate among non-excluded LPs
    floor_rate = float("inf")
    floor_setter_id = ""
    floor_setter_name = ""
    non_excluded_ids: set[str] = set()

    for lp_id, rate in rate_map.items():
        inv = lp_map.get(lp_id)
        if inv is None:
            continue
        if _is_mfn_excluded(inv, mfn_provisions):
            continue
        non_excluded_ids.add(lp_id)
        if rate < floor_rate:
            floor_rate = rate
            floor_setter_id = lp_id
            floor_setter_name = inv.get("name", lp_id)

    if floor_rate == float("inf"):
        floor_rate = _get_standard_fee(state)

    # Determine which MFN-holding LPs ratchet
    ratchets: list[dict] = []
    total_cost = 0.0
    mfn_eligible_count = 0

    for inv in investors:
        lp_id = inv.get("lpId", "")
        if lp_id not in rate_map:
            continue
        terms = inv.get("negotiatedTerms") or {}
        if not terms.get("mfnClause"):
            continue
        mfn_eligible_count += 1

        current_rate = rate_map[lp_id]
        if current_rate > floor_rate:
            commitment = inv.get("commitment", 0)
            cost = commitment * (current_rate - floor_rate)
            ratchets.append({
                "lpId": lp_id,
                "name": inv.get("name", ""),
                "current_rate": round(current_rate, 6),
                "ratchet_to": round(floor_rate, 6),
                "delta_bps": round((current_rate - floor_rate) * 10000, 1),
                "commitment": commitment,
                "cost_per_year": round(cost, 2),
            })
            total_cost += cost

    ratchets.sort(key=lambda r: r["cost_per_year"], reverse=True)

    return {
        "enabled": True,
        "floor_rate": round(floor_rate, 6),
        "floor_setter": floor_setter_name,
        "floor_setter_id": floor_setter_id,
        "mfn_eligible_count": mfn_eligible_count,
        "ratchets": ratchets,
        "total_cascade_cost": round(total_cost, 2),
        "total_ratchet_count": len(ratchets),
    }


# ---------------------------------------------------------------------------
# Core: GP promote sensitivity
# ---------------------------------------------------------------------------

def promote_sensitivity(
    blended_rate: float,
    fund_size: float,
    state: dict,
) -> dict[str, Any]:
    """
    Model how blended fee level affects GP promote breakeven.

    At a given blended fee, calculates:
      - Annual fund operating expenses (fee revenue)
      - Net return after fees
      - Gross IRR needed so that net IRR = preferred return
      - Comparison between standard and blended scenarios
      - Promote delta estimate over fund life

    Returns dict with breakeven IRR at standard and blended, promote delta.
    """
    standard_rate = _get_standard_fee(state)
    pref_return = _get_pref_return(state)
    carry = _get_carry(state)
    fund_term = _get_fund_term(state)
    inv_period = _get_investment_period(state)

    org_expense_cap = _safe_get(state, "standardTerms", "orgExpenseCap", default=0)
    annual_org_expense = org_expense_cap / fund_term if org_expense_cap > 0 and fund_term > 0 else 0

    fee_offset_pct = _safe_get(state, "standardTerms", "feeOffsetPercentage", default=1.0)

    def _breakeven_gross_irr(fee_rate: float) -> float:
        """
        Find gross IRR where net IRR equals preferred return after fees.

        Simplified model: annual fee drag on returns during investment period,
        reduced fee post-investment period (step-down). Gross IRR = net IRR + fee drag.
        """
        step_down = _safe_get(state, "standardTerms", "feeStepDown")
        step_rate = step_down.get("rate", fee_rate * 0.75) if step_down else fee_rate * 0.75

        # Weighted average fee drag over fund life
        if fund_term > 0:
            ip_years = min(inv_period, fund_term)
            post_ip_years = fund_term - ip_years
            avg_fee_drag = (ip_years * fee_rate + post_ip_years * step_rate) / fund_term
        else:
            avg_fee_drag = fee_rate

        # Adjust for fee offset (transaction fees offset mgmt fees)
        effective_drag = avg_fee_drag * (1 - fee_offset_pct * 0.1)

        # Add org expense drag
        if fund_size > 0:
            expense_drag = annual_org_expense / fund_size
        else:
            expense_drag = 0

        total_drag = effective_drag + expense_drag
        breakeven = pref_return + total_drag
        return breakeven

    breakeven_standard = _breakeven_gross_irr(standard_rate)
    breakeven_blended = _breakeven_gross_irr(blended_rate)

    # Promote delta estimate over fund life
    # Lower fees -> lower breakeven -> easier to reach promote territory
    # Estimate annual promote-eligible return spread at a target gross return
    target_gross = breakeven_standard + 0.04  # assume 400bps above breakeven
    net_at_standard = target_gross - (standard_rate + annual_org_expense / fund_size if fund_size > 0 else 0)
    net_at_blended = target_gross - (blended_rate + annual_org_expense / fund_size if fund_size > 0 else 0)

    # Promote only applies above pref
    promote_spread_standard = max(net_at_standard - pref_return, 0) * carry
    promote_spread_blended = max(net_at_blended - pref_return, 0) * carry

    annual_promote_standard = fund_size * promote_spread_standard
    annual_promote_blended = fund_size * promote_spread_blended
    promote_delta_annual = annual_promote_blended - annual_promote_standard
    promote_delta_total = promote_delta_annual * fund_term

    return {
        "standard_fee": standard_rate,
        "blended_fee": blended_rate,
        "preferred_return": pref_return,
        "carry": carry,
        "breakeven_irr_standard": round(breakeven_standard, 6),
        "breakeven_irr_blended": round(breakeven_blended, 6),
        "breakeven_delta_bps": round((breakeven_blended - breakeven_standard) * 10000, 1),
        "promote_delta_annual": round(promote_delta_annual, 2),
        "promote_delta_fund_life": round(promote_delta_total, 2),
        "fund_term": fund_term,
        "fund_size": fund_size,
    }


# ---------------------------------------------------------------------------
# Core: Breakeven fund size
# ---------------------------------------------------------------------------

def breakeven_fund_size(concession_cost: float, fund_size: float) -> dict[str, Any]:
    """
    At what fund size does a concession become immaterial (<1 bps impact
    on blended fee)?

    concession_cost: annual dollar cost of the concession
    fund_size: current total commitments

    Breakeven = concession_cost / 0.0001 (1 bps)
    """
    if concession_cost <= 0:
        return {
            "breakeven_size": 0.0,
            "current_size": fund_size,
            "current_pct_of_breakeven": 100.0,
            "is_immaterial": True,
        }

    be_size = abs(concession_cost) / 0.0001
    pct = (fund_size / be_size * 100) if be_size > 0 else 0.0

    return {
        "breakeven_size": round(be_size, 2),
        "current_size": round(fund_size, 2),
        "current_pct_of_breakeven": round(pct, 1),
        "is_immaterial": fund_size >= be_size,
    }


# ---------------------------------------------------------------------------
# Command: dashboard
# ---------------------------------------------------------------------------

def _status_breakdown(investors: list[dict]) -> dict[str, dict]:
    """Group investors by status with counts and commitment totals."""
    status_order = [
        "funded", "signed", "verbal_commit", "in_negotiation",
        "prospect", "re_opened", "stalled", "reduced", "passed",
    ]
    breakdown: dict[str, dict] = {}
    for status in status_order:
        breakdown[status] = {"count": 0, "commitment": 0.0, "names": []}
    for inv in investors:
        s = inv.get("status", "prospect")
        if s not in breakdown:
            breakdown[s] = {"count": 0, "commitment": 0.0, "names": []}
        breakdown[s]["count"] += 1
        breakdown[s]["commitment"] += inv.get("commitment", 0)
        breakdown[s]["names"].append(inv.get("name", inv.get("lpId", "")))
    return breakdown


def _close_schedule(state: dict) -> list[dict]:
    """Build close schedule with per-close amounts and LP assignments."""
    closes = state.get("closes", [])
    investors = state.get("investors", [])
    schedule: list[dict] = []

    for close in closes:
        close_id = close.get("closeId", "")
        assigned: list[dict] = []
        total = 0.0
        for inv in investors:
            if inv.get("targetClose") == close_id and inv.get("status") not in ("passed", "stalled"):
                assigned.append({
                    "lpId": inv.get("lpId", ""),
                    "name": inv.get("name", ""),
                    "commitment": inv.get("commitment", 0),
                    "status": inv.get("status", ""),
                })
                total += inv.get("commitment", 0)

        schedule.append({
            "closeId": close_id,
            "targetDate": close.get("targetDate"),
            "actualDate": close.get("actualDate"),
            "status": close.get("status", "planned"),
            "earlyCloserDiscount": close.get("earlyCloserDiscount", 0),
            "lp_count": len(assigned),
            "total_commitment": round(total, 2),
            "lps": assigned,
        })

    return schedule


def cmd_dashboard(state: dict) -> dict[str, Any]:
    """Produce the full fund raise dashboard."""
    investors = state.get("investors", [])
    target = state.get("targetRaise", 0)
    hard_cap = state.get("hardCap", 0)
    mfn_prov = state.get("mfnProvisions", {})

    # Status breakdown
    breakdown = _status_breakdown(investors)
    committed = sum(
        breakdown[s]["commitment"]
        for s in ("funded", "signed")
        if s in breakdown
    )
    all_pipeline = sum(
        breakdown[s]["commitment"]
        for s in ("funded", "signed", "verbal_commit", "in_negotiation", "prospect", "re_opened")
        if s in breakdown
    )
    progress_pct = (committed / target * 100) if target > 0 else 0

    # Blended fee at three levels
    bf_committed = blended_fee(investors, state, COMMITTED_STATUSES)
    bf_pipeline = blended_fee(investors, state, PIPELINE_STATUSES)
    bf_all = blended_fee(investors, state, ALL_ACTIVE_STATUSES)

    # MFN cascade
    cascade = mfn_cascade(investors, mfn_prov, state)

    # Close schedule
    schedule = _close_schedule(state)

    # GP promote sensitivity using committed blended fee
    total_committed = bf_committed["total_commitment"]
    sensitivity = promote_sensitivity(
        bf_committed["blended_rate"],
        total_committed if total_committed > 0 else target,
        state,
    )

    return {
        "command": "dashboard",
        "fundName": state.get("fundName", ""),
        "fundId": state.get("fundId", ""),
        "targetRaise": target,
        "hardCap": hard_cap,
        "totalCommitted": round(committed, 2),
        "totalPipeline": round(all_pipeline, 2),
        "progressPct": round(progress_pct, 1),
        "statusBreakdown": {
            k: {"count": v["count"], "commitment": round(v["commitment"], 2)}
            for k, v in breakdown.items() if v["count"] > 0
        },
        "blendedFee": {
            "committed": bf_committed,
            "includingVerbal": bf_pipeline,
            "allPipeline": bf_all,
        },
        "mfnCascade": cascade,
        "closeSchedule": schedule,
        "promoteSensitivity": sensitivity,
    }


def _format_dashboard(result: dict) -> str:
    """Render dashboard result as formatted text."""
    lines: list[str] = []
    fund_name = result.get("fundName", "Fund")

    lines.append(f"FUND RAISE DASHBOARD: {fund_name}")
    lines.append(
        f"Target: {_fmt_dollars(result['targetRaise'])} | "
        f"Hard Cap: {_fmt_dollars(result['hardCap'])} | "
        f"Committed: {_fmt_dollars(result['totalCommitted'])} ({result['progressPct']:.1f}%)"
    )
    lines.append("")

    # Status breakdown
    lines.append("STATUS BREAKDOWN:")
    label_map = {
        "funded": "Funded",
        "signed": "Signed",
        "verbal_commit": "Verbal Commit",
        "in_negotiation": "In Negotiation",
        "prospect": "Prospect",
        "re_opened": "Re-Opened",
        "stalled": "Stalled",
        "reduced": "Reduced",
        "passed": "Passed",
    }
    for status_key in label_map:
        entry = result["statusBreakdown"].get(status_key)
        if entry and entry["count"] > 0:
            label = label_map[status_key]
            lines.append(f"  {label:<20s} {_fmt_dollars(entry['commitment']):>12s}  ({entry['count']} LPs)")
    lines.append("")

    # Blended fee analysis
    lines.append("BLENDED FEE ANALYSIS:")
    bf = result["blendedFee"]
    std_rate = bf["committed"]["standard_rate"]
    lines.append(f"  Standard fee rate:                {_fmt_pct(std_rate)}")
    lines.append(
        f"  Blended fee (funded+signed):      {_fmt_pct(bf['committed']['blended_rate'])} "
        f"({bf['committed']['delta_bps']:+.0f} bps)"
    )
    lines.append(
        f"  Blended fee (incl verbal):        {_fmt_pct(bf['includingVerbal']['blended_rate'])} "
        f"({bf['includingVerbal']['delta_bps']:+.0f} bps)"
    )
    lines.append(
        f"  Blended fee (all pipeline):       {_fmt_pct(bf['allPipeline']['blended_rate'])} "
        f"({bf['allPipeline']['delta_bps']:+.0f} bps projected)"
    )
    lines.append("")
    lines.append(f"  Annual fee revenue at standard:   {_fmt_dollars(bf['committed']['annual_revenue_standard'])}")
    lines.append(f"  Annual fee revenue at blended:    {_fmt_dollars(bf['committed']['annual_revenue_blended'])}")
    lines.append(f"  Concession cost:                  {_fmt_dollars(bf['committed']['concession_cost'])}/yr")
    lines.append("")

    # MFN cascade
    mfn = result["mfnCascade"]
    lines.append("MFN CASCADE STATUS:")
    if not mfn["enabled"]:
        lines.append("  MFN provisions not enabled for this fund.")
    else:
        lines.append(f"  {mfn['mfn_eligible_count']} LPs with MFN clauses")
        lines.append(f"  Current MFN floor: {_fmt_pct(mfn['floor_rate'])} (set by {mfn['floor_setter']})")
        lines.append(f"  LPs at risk of ratchet: {mfn['total_ratchet_count']}")
        if mfn["ratchets"]:
            for r in mfn["ratchets"]:
                lines.append(
                    f"    {r['name']}: {_fmt_pct(r['current_rate'])} -> {_fmt_pct(r['ratchet_to'])} "
                    f"(-{r['delta_bps']:.0f} bps) = {_fmt_dollars(r['cost_per_year'])}/yr"
                )
        lines.append(f"  Potential cascade cost: {_fmt_dollars(mfn['total_cascade_cost'])}/yr")
    lines.append("")

    # Close schedule
    lines.append("CLOSE SCHEDULE:")
    schedule = result.get("closeSchedule", [])
    if not schedule:
        lines.append("  No closes configured.")
    else:
        for close in schedule:
            date_str = close.get("actualDate") or close.get("targetDate") or "TBD"
            lines.append(
                f"  {close['closeId']:<12s} {date_str:<12s} "
                f"{close['status']:<8s} {_fmt_dollars(close['total_commitment']):>12s} "
                f"({close['lp_count']} LPs)"
            )
            discount = close.get("earlyCloserDiscount", 0)
            if discount > 0:
                lines.append(f"    Early closer discount: {_fmt_bps(discount)}")
    lines.append("")

    # GP promote sensitivity
    ps = result["promoteSensitivity"]
    lines.append("GP PROMOTE SENSITIVITY:")
    lines.append(f"  At current blended fee: promote breakeven at {_fmt_pct(ps['breakeven_irr_blended'])} gross IRR")
    lines.append(f"  At standard fee:        promote breakeven at {_fmt_pct(ps['breakeven_irr_standard'])} gross IRR")
    lines.append(f"  Breakeven delta: {ps['breakeven_delta_bps']:+.0f} bps")
    lines.append(f"  Promote delta over fund life: {_fmt_dollars(ps['promote_delta_fund_life'])} to GP")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Command: scenario
# ---------------------------------------------------------------------------

def cmd_scenario(
    state: dict,
    lp_id: str,
    proposed_fee: float | None = None,
    proposed_terms: dict | None = None,
) -> dict[str, Any]:
    """
    What-if analysis: model a proposed fee concession for a specific LP.

    Does NOT modify state. Returns direct impact, MFN cascade, blended fee
    shift, promote sensitivity, breakeven analysis, and recommendation.
    """
    investors = state.get("investors", [])
    mfn_prov = state.get("mfnProvisions", {})

    # Find the target LP
    target_lp = None
    for inv in investors:
        if inv.get("lpId") == lp_id:
            target_lp = inv
            break

    if target_lp is None:
        return {"error": f"LP with id '{lp_id}' not found in investor list."}

    # Current effective rate
    current_rate = _effective_fee_rate(target_lp, state)
    commitment = target_lp.get("commitment", 0)
    standard_rate = _get_standard_fee(state)

    # Determine proposed rate
    if proposed_fee is not None:
        new_rate = proposed_fee
    elif proposed_terms:
        # Build a temporary investor with proposed terms applied
        temp_inv = json.loads(json.dumps(target_lp))
        existing_terms = temp_inv.get("negotiatedTerms") or {}
        existing_terms.update(proposed_terms)
        temp_inv["negotiatedTerms"] = existing_terms
        new_rate = _effective_fee_rate(temp_inv, state)
    else:
        return {"error": "Either --proposed-fee or --proposed-terms must be provided."}

    # Direct impact
    annual_current = commitment * current_rate
    annual_proposed = commitment * new_rate
    direct_impact = annual_proposed - annual_current

    # MFN cascade: current vs proposed
    cascade_current = mfn_cascade(investors, mfn_prov, state)
    cascade_proposed = mfn_cascade(
        investors, mfn_prov, state,
        proposed_change={"lpId": lp_id, "proposed_rate": new_rate},
    )

    cascade_incremental_cost = cascade_proposed["total_cascade_cost"] - cascade_current["total_cascade_cost"]
    total_annual_impact = direct_impact + cascade_incremental_cost

    # Blended fee shift: simulate the new blended fee
    # Create a modified investor list for the simulation
    sim_investors = []
    for inv in investors:
        if inv.get("lpId") == lp_id:
            sim_inv = json.loads(json.dumps(inv))
            if proposed_fee is not None:
                sim_terms = sim_inv.get("negotiatedTerms") or {}
                sim_terms["managementFee"] = proposed_fee
                # Clear tiers/holiday/waiver so flat rate takes effect
                sim_terms.pop("managementFeeTiers", None)
                sim_terms.pop("feeHoliday", None)
                sim_terms.pop("feeWaiver", None)
                sim_inv["negotiatedTerms"] = sim_terms
            elif proposed_terms:
                sim_terms = sim_inv.get("negotiatedTerms") or {}
                sim_terms.update(proposed_terms)
                sim_inv["negotiatedTerms"] = sim_terms
            sim_investors.append(sim_inv)
        else:
            sim_investors.append(inv)

    bf_current = blended_fee(investors, state, COMMITTED_STATUSES)
    bf_proposed = blended_fee(sim_investors, state, COMMITTED_STATUSES)

    # If no committed LPs, fall back to pipeline
    if bf_current["lp_count"] == 0:
        bf_current = blended_fee(investors, state, PIPELINE_STATUSES)
        bf_proposed = blended_fee(sim_investors, state, PIPELINE_STATUSES)
    if bf_current["lp_count"] == 0:
        bf_current = blended_fee(investors, state, ALL_ACTIVE_STATUSES)
        bf_proposed = blended_fee(sim_investors, state, ALL_ACTIVE_STATUSES)

    # Promote sensitivity at proposed blended
    fund_size = bf_current["total_commitment"] if bf_current["total_commitment"] > 0 else state.get("targetRaise", 0)
    ps_current = promote_sensitivity(bf_current["blended_rate"], fund_size, state)
    ps_proposed = promote_sensitivity(bf_proposed["blended_rate"], fund_size, state)

    # Breakeven fund size
    be = breakeven_fund_size(abs(direct_impact), fund_size)

    # Counter-offer recommendation
    recommendation = None
    if cascade_incremental_cost > 0 and abs(direct_impact) > 0:
        cascade_ratio = abs(cascade_incremental_cost) / abs(direct_impact)
        if cascade_ratio > 0.20:
            # Suggest a rate that avoids becoming the new MFN floor
            current_floor = cascade_current.get("floor_rate", standard_rate)
            counter_rate = max(current_floor, new_rate + 0.0005)
            recommendation = {
                "trigger": "cascade_cost_exceeds_20pct",
                "message": (
                    f"Cascade cost ({_fmt_dollars(cascade_incremental_cost)}/yr) is "
                    f"{cascade_ratio:.0%} of the direct concession. "
                    f"Consider counter-offering at {_fmt_pct(counter_rate)} "
                    f"(current MFN floor) to avoid triggering ratchets."
                ),
                "counter_rate": round(counter_rate, 6),
                "cascade_ratio": round(cascade_ratio, 4),
            }

    creates_new_floor = (
        mfn_prov.get("enabled", False)
        and new_rate < cascade_current.get("floor_rate", standard_rate)
    )

    return {
        "command": "scenario",
        "lpId": lp_id,
        "lpName": target_lp.get("name", ""),
        "commitment": commitment,
        "directImpact": {
            "current_rate": round(current_rate, 6),
            "proposed_rate": round(new_rate, 6),
            "rate_delta_bps": round((new_rate - current_rate) * 10000, 1),
            "annual_revenue_current": round(annual_current, 2),
            "annual_revenue_proposed": round(annual_proposed, 2),
            "annual_impact": round(direct_impact, 2),
        },
        "mfnCascade": {
            "current": cascade_current,
            "proposed": cascade_proposed,
            "incremental_ratchets": cascade_proposed["total_ratchet_count"] - cascade_current["total_ratchet_count"],
            "incremental_cost": round(cascade_incremental_cost, 2),
            "creates_new_floor": creates_new_floor,
        },
        "totalAnnualImpact": round(total_annual_impact, 2),
        "blendedFeeShift": {
            "current": round(bf_current["blended_rate"], 6),
            "proposed": round(bf_proposed["blended_rate"], 6),
            "delta_bps": round((bf_proposed["blended_rate"] - bf_current["blended_rate"]) * 10000, 1),
        },
        "promoteSensitivity": {
            "current": ps_current,
            "proposed": ps_proposed,
            "breakeven_shift_bps": round(
                (ps_proposed["breakeven_irr_blended"] - ps_current["breakeven_irr_blended"]) * 10000, 1
            ),
            "promote_delta_shift": round(
                ps_proposed["promote_delta_fund_life"] - ps_current["promote_delta_fund_life"], 2
            ),
        },
        "breakeven": be,
        "recommendation": recommendation,
    }


def _format_scenario(result: dict) -> str:
    """Render scenario result as formatted text."""
    if "error" in result:
        return f"ERROR: {result['error']}"

    lines: list[str] = []
    lp_name = result.get("lpName", result.get("lpId", "LP"))
    di = result["directImpact"]

    lines.append(
        f"SCENARIO ANALYSIS: What if {lp_name} gets {_fmt_pct(di['proposed_rate'])}?"
    )
    lines.append("")

    lines.append("DIRECT IMPACT:")
    lines.append(
        f"  Fee rate change: {_fmt_pct(di['current_rate'])} -> {_fmt_pct(di['proposed_rate'])} "
        f"on {_fmt_dollars(result['commitment'])}"
    )
    lines.append(f"  Annual revenue impact: {_fmt_dollars(di['annual_impact'])}")
    lines.append("")

    # MFN
    mfn = result["mfnCascade"]
    lines.append("MFN CASCADE:")
    if not mfn["proposed"]["enabled"]:
        lines.append("  MFN provisions not enabled.")
    elif mfn["proposed"]["total_ratchet_count"] == 0:
        lines.append("  No MFN ratchets triggered.")
    else:
        lines.append(f"  Triggers {mfn['proposed']['total_ratchet_count']} MFN ratchets:")
        for r in mfn["proposed"]["ratchets"]:
            lines.append(
                f"    {r['name']}: {_fmt_pct(r['current_rate'])} -> {_fmt_pct(r['ratchet_to'])} "
                f"(MFN floor match) = {_fmt_dollars(r['cost_per_year'])}/yr"
            )
        lines.append(f"  Total cascade cost: {_fmt_dollars(mfn['proposed']['total_cascade_cost'])}/yr")
    if mfn.get("creates_new_floor"):
        lines.append(f"  ** Creates new MFN floor at {_fmt_pct(di['proposed_rate'])} **")
    lines.append("")

    lines.append(f"TOTAL ANNUAL IMPACT: {_fmt_dollars(result['totalAnnualImpact'])}/yr")

    bfs = result["blendedFeeShift"]
    lines.append(
        f"BLENDED FEE SHIFT: {_fmt_pct(bfs['current'])} -> {_fmt_pct(bfs['proposed'])} "
        f"({bfs['delta_bps']:+.0f} bps)"
    )
    lines.append("")

    # Promote sensitivity
    ps = result["promoteSensitivity"]
    lines.append("GP PROMOTE SENSITIVITY:")
    lines.append(
        f"  Promote breakeven shifts: "
        f"{_fmt_pct(ps['current']['breakeven_irr_blended'])} -> "
        f"{_fmt_pct(ps['proposed']['breakeven_irr_blended'])} gross IRR"
    )
    lines.append(f"  Promote delta over fund life: {_fmt_dollars(ps['promote_delta_shift'])}")
    lines.append("")

    # Breakeven
    be = result["breakeven"]
    lines.append("BREAKEVEN:")
    lines.append(
        f"  This concession becomes immaterial (<1 bps) at fund size: "
        f"{_fmt_dollars(be['breakeven_size'])}"
    )
    lines.append(
        f"  Current fund size: {_fmt_dollars(be['current_size'])} "
        f"({be['current_pct_of_breakeven']:.1f}% of breakeven)"
    )
    lines.append("")

    # Recommendation
    rec = result.get("recommendation")
    if rec:
        lines.append("RECOMMENDATION:")
        lines.append(f"  {rec['message']}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Command: mfn-audit
# ---------------------------------------------------------------------------

def cmd_mfn_audit(state: dict) -> dict[str, Any]:
    """
    Full MFN cascade audit: current floor, eligible LPs, exposure at
    hypothetical fee levels.
    """
    investors = state.get("investors", [])
    mfn_prov = state.get("mfnProvisions", {})
    standard_rate = _get_standard_fee(state)

    # Current cascade
    current = mfn_cascade(investors, mfn_prov, state)

    # Eligible LP table
    eligible_lps: list[dict] = []
    for inv in investors:
        if inv.get("status") in ("passed", "stalled"):
            continue
        terms = inv.get("negotiatedTerms") or {}
        eff_rate = _effective_fee_rate(inv, state)
        is_excluded = _is_mfn_excluded(inv, mfn_prov)
        has_mfn = terms.get("mfnClause", False)
        would_ratchet = (
            has_mfn
            and not is_excluded
            and current["enabled"]
            and eff_rate > current["floor_rate"]
        )
        cost_if_ratcheted = 0.0
        if would_ratchet:
            cost_if_ratcheted = inv.get("commitment", 0) * (eff_rate - current["floor_rate"])

        eligible_lps.append({
            "lpId": inv.get("lpId", ""),
            "name": inv.get("name", ""),
            "commitment": inv.get("commitment", 0),
            "current_rate": round(eff_rate, 6),
            "has_mfn_clause": has_mfn,
            "is_excluded": is_excluded,
            "would_ratchet": would_ratchet,
            "cost_if_ratcheted": round(cost_if_ratcheted, 2),
        })

    # Exposure table at 3 hypothetical fee levels
    floor = current["floor_rate"] if current["enabled"] else standard_rate
    test_levels = [
        round(floor - 0.0025, 6),  # 25 bps below current floor
        round(floor - 0.0050, 6),  # 50 bps below
        round(floor - 0.0075, 6),  # 75 bps below
    ]
    # Ensure no negative rates
    test_levels = [max(lvl, 0.0) for lvl in test_levels]

    exposure: list[dict] = []
    for level in test_levels:
        sim = mfn_cascade(
            investors, mfn_prov, state,
            proposed_change={"lpId": "__hypothetical__", "proposed_rate": level},
        )
        exposure.append({
            "hypothetical_rate": round(level, 6),
            "ratchet_count": sim["total_ratchet_count"],
            "cascade_cost": round(sim["total_cascade_cost"], 2),
        })

    return {
        "command": "mfn-audit",
        "fundName": state.get("fundName", ""),
        "current": current,
        "eligibleLPs": eligible_lps,
        "exposure": exposure,
    }


def _format_mfn_audit(result: dict) -> str:
    """Render MFN audit result as formatted text."""
    lines: list[str] = []
    fund_name = result.get("fundName", "Fund")
    current = result["current"]

    lines.append(f"MFN AUDIT: {fund_name}")
    lines.append("")

    if not current["enabled"]:
        lines.append("MFN provisions are not enabled for this fund.")
        return "\n".join(lines)

    lines.append(
        f"CURRENT MFN FLOOR: {_fmt_pct(current['floor_rate'])} "
        f"(set by {current['floor_setter']}, "
        f"ID: {current['floor_setter_id']})"
    )
    lines.append("")

    lines.append("MFN-ELIGIBLE LPs:")
    lines.append(
        f"  {'LP Name':<25s} {'Commitment':>12s} {'Rate':>8s} "
        f"{'MFN':>5s} {'Excl':>5s} {'Ratchet':>8s} {'Cost/yr':>12s}"
    )
    lines.append("  " + "-" * 80)
    for lp in result["eligibleLPs"]:
        lines.append(
            f"  {lp['name']:<25s} {_fmt_dollars(lp['commitment']):>12s} "
            f"{_fmt_pct(lp['current_rate']):>8s} "
            f"{'Y' if lp['has_mfn_clause'] else 'N':>5s} "
            f"{'Y' if lp['is_excluded'] else 'N':>5s} "
            f"{'Y' if lp['would_ratchet'] else 'N':>8s} "
            f"{_fmt_dollars(lp['cost_if_ratcheted']):>12s}"
        )
    lines.append("")

    lines.append("EXPOSURE AT HYPOTHETICAL FEE LEVELS:")
    for exp in result["exposure"]:
        lines.append(
            f"  If next LP negotiates {_fmt_pct(exp['hypothetical_rate'])}: "
            f"{exp['ratchet_count']} ratchets, {_fmt_dollars(exp['cascade_cost'])}/yr additional cost"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Command: export-csv
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "lpId", "name", "type", "tier", "status", "targetClose",
    "commitment", "originalCommitment",
    "managementFee", "managementFeeTiers",
    "feeHolidayMonths", "feeHolidayReason",
    "feeWaiverType", "feeWaiverDuration", "feeWaiverRate",
    "coInvestAllocation", "coInvestFee",
    "orgExpenseCap", "feeOffsetPercentage",
    "carry", "preferredReturn",
    "mfnClause",
    "blendedRateEnabled", "blendedRate", "totalFamilyCommitment",
    "customProvisions",
    "primaryContact", "title", "email", "phone",
    "notes",
]


def cmd_export_csv(state: dict) -> str:
    """Export investor ledger to CSV string."""
    investors = state.get("investors", [])
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()

    for inv in investors:
        terms = inv.get("negotiatedTerms") or {}
        contact = inv.get("contactInfo") or {}
        holiday = terms.get("feeHoliday") or {}
        waiver = terms.get("feeWaiver") or {}
        blended = terms.get("blendedRateAcrossFunds") or {}
        tiers = terms.get("managementFeeTiers")

        row = {
            "lpId": inv.get("lpId", ""),
            "name": inv.get("name", ""),
            "type": inv.get("type", ""),
            "tier": inv.get("tier", ""),
            "status": inv.get("status", ""),
            "targetClose": inv.get("targetClose", ""),
            "commitment": inv.get("commitment", 0),
            "originalCommitment": inv.get("originalCommitment", ""),
            "managementFee": terms.get("managementFee", ""),
            "managementFeeTiers": json.dumps(tiers) if tiers else "",
            "feeHolidayMonths": holiday.get("months", ""),
            "feeHolidayReason": holiday.get("reason", ""),
            "feeWaiverType": waiver.get("type", ""),
            "feeWaiverDuration": waiver.get("duration", ""),
            "feeWaiverRate": waiver.get("rate", ""),
            "coInvestAllocation": terms.get("coInvestAllocation", ""),
            "coInvestFee": terms.get("coInvestFee", ""),
            "orgExpenseCap": terms.get("orgExpenseCap", ""),
            "feeOffsetPercentage": terms.get("feeOffsetPercentage", ""),
            "carry": terms.get("carry", ""),
            "preferredReturn": terms.get("preferredReturn", ""),
            "mfnClause": terms.get("mfnClause", ""),
            "blendedRateEnabled": blended.get("enabled", ""),
            "blendedRate": blended.get("blendedRate", ""),
            "totalFamilyCommitment": blended.get("totalFamilyCommitment", ""),
            "customProvisions": json.dumps(terms.get("customProvisions")) if terms.get("customProvisions") else "",
            "primaryContact": contact.get("primaryContact", ""),
            "title": contact.get("title", ""),
            "email": contact.get("email", ""),
            "phone": contact.get("phone", ""),
            "notes": inv.get("notes", ""),
        }
        writer.writerow(row)

    return output.getvalue()


# ---------------------------------------------------------------------------
# Command: import-csv
# ---------------------------------------------------------------------------

def _parse_csv_value(value: str, field: str) -> Any:
    """Parse a CSV cell value into the appropriate Python type."""
    if value == "" or value is None:
        return None

    # Numeric fields
    numeric_fields = {
        "commitment", "originalCommitment", "managementFee",
        "feeHolidayMonths", "feeWaiverRate",
        "coInvestAllocation", "coInvestFee",
        "orgExpenseCap", "feeOffsetPercentage",
        "carry", "preferredReturn",
        "blendedRate", "totalFamilyCommitment",
    }
    if field in numeric_fields:
        try:
            return float(value)
        except ValueError:
            return None

    # Boolean fields
    bool_fields = {"mfnClause", "blendedRateEnabled"}
    if field in bool_fields:
        return value.lower() in ("true", "1", "yes", "y")

    # JSON fields
    json_fields = {"managementFeeTiers", "customProvisions"}
    if field in json_fields:
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None

    return value


def cmd_import_csv(state: dict, csv_path: str) -> dict[str, Any]:
    """
    Import LP data from CSV and merge with existing state.

    Merge logic: if lpId matches an existing investor, update that investor.
    If lpId is new, add it. Returns the updated state as JSON.
    """
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    existing_map: dict[str, int] = {}
    investors = state.get("investors", [])
    for i, inv in enumerate(investors):
        existing_map[inv.get("lpId", "")] = i

    added = 0
    updated = 0

    for row in rows:
        lp_id = row.get("lpId", "").strip()
        if not lp_id:
            continue

        # Build investor dict from CSV row
        terms: dict[str, Any] = {}
        contact: dict[str, Any] = {}

        mf = _parse_csv_value(row.get("managementFee", ""), "managementFee")
        if mf is not None:
            terms["managementFee"] = mf

        tiers = _parse_csv_value(row.get("managementFeeTiers", ""), "managementFeeTiers")
        if tiers:
            terms["managementFeeTiers"] = tiers

        hol_months = _parse_csv_value(row.get("feeHolidayMonths", ""), "feeHolidayMonths")
        hol_reason = row.get("feeHolidayReason", "").strip()
        if hol_months is not None and hol_months > 0:
            terms["feeHoliday"] = {"months": int(hol_months), "reason": hol_reason or "custom"}

        waiver_type = row.get("feeWaiverType", "").strip()
        waiver_dur = row.get("feeWaiverDuration", "").strip()
        waiver_rate = _parse_csv_value(row.get("feeWaiverRate", ""), "feeWaiverRate")
        if waiver_type:
            waiver_obj: dict[str, Any] = {"type": waiver_type}
            if waiver_dur:
                waiver_obj["duration"] = waiver_dur
            if waiver_rate is not None:
                waiver_obj["rate"] = waiver_rate
            terms["feeWaiver"] = waiver_obj

        for field_key in ("coInvestAllocation", "coInvestFee", "orgExpenseCap",
                          "feeOffsetPercentage", "carry", "preferredReturn"):
            val = _parse_csv_value(row.get(field_key, ""), field_key)
            if val is not None:
                terms[field_key] = val

        mfn_val = _parse_csv_value(row.get("mfnClause", ""), "mfnClause")
        if mfn_val is not None:
            terms["mfnClause"] = mfn_val

        ble = _parse_csv_value(row.get("blendedRateEnabled", ""), "blendedRateEnabled")
        blr = _parse_csv_value(row.get("blendedRate", ""), "blendedRate")
        tfc = _parse_csv_value(row.get("totalFamilyCommitment", ""), "totalFamilyCommitment")
        if ble:
            terms["blendedRateAcrossFunds"] = {
                "enabled": True,
                "blendedRate": blr,
                "totalFamilyCommitment": tfc,
            }

        custom = _parse_csv_value(row.get("customProvisions", ""), "customProvisions")
        if custom:
            terms["customProvisions"] = custom

        for ck in ("primaryContact", "title", "email", "phone"):
            cv = row.get(ck, "").strip()
            if cv:
                contact[ck] = cv

        commitment = _parse_csv_value(row.get("commitment", ""), "commitment") or 0
        orig_commit = _parse_csv_value(row.get("originalCommitment", ""), "originalCommitment")

        inv_obj: dict[str, Any] = {
            "lpId": lp_id,
            "name": row.get("name", "").strip() or lp_id,
            "type": row.get("type", "").strip() or "other",
            "tier": row.get("tier", "").strip() or "standard",
            "status": row.get("status", "").strip() or "prospect",
            "targetClose": row.get("targetClose", "").strip() or "",
            "commitment": commitment,
        }
        if orig_commit is not None:
            inv_obj["originalCommitment"] = orig_commit
        if terms:
            inv_obj["negotiatedTerms"] = terms
        if contact:
            inv_obj["contactInfo"] = contact

        notes = row.get("notes", "").strip()
        if notes:
            inv_obj["notes"] = notes

        if lp_id in existing_map:
            idx = existing_map[lp_id]
            # Merge: update existing investor, preserving statusHistory
            existing = investors[idx]
            existing_history = existing.get("statusHistory", [])
            inv_obj["statusHistory"] = existing_history
            # If status changed, log it
            if existing.get("status") != inv_obj.get("status"):
                existing_history.append({
                    "status": inv_obj["status"],
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "amount": commitment,
                    "notes": "Updated via CSV import",
                })
            investors[idx] = inv_obj
            updated += 1
        else:
            inv_obj["statusHistory"] = [{
                "status": inv_obj["status"],
                "date": datetime.now().strftime("%Y-%m-%d"),
                "amount": commitment,
                "notes": "Added via CSV import",
            }]
            investors.append(inv_obj)
            existing_map[lp_id] = len(investors) - 1
            added += 1

    state["investors"] = investors
    state["lastUpdated"] = datetime.now().isoformat()

    return {
        "command": "import-csv",
        "added": added,
        "updated": updated,
        "total_investors": len(investors),
        "state": state,
    }


# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------

def run_command(
    command: str,
    state: dict,
    lp_id: str | None = None,
    proposed_fee: float | None = None,
    proposed_terms: dict | None = None,
    csv_path: str | None = None,
    output_format: str = "text",
) -> str:
    """Dispatch to the appropriate command handler and format output."""

    if command == "dashboard":
        result = cmd_dashboard(state)
        if output_format == "json":
            return json.dumps(result, indent=2)
        return _format_dashboard(result)

    elif command == "scenario":
        if not lp_id:
            return json.dumps({"error": "--lp-id is required for scenario command."})
        result = cmd_scenario(state, lp_id, proposed_fee, proposed_terms)
        if output_format == "json":
            return json.dumps(result, indent=2)
        return _format_scenario(result)

    elif command == "mfn-audit":
        result = cmd_mfn_audit(state)
        if output_format == "json":
            return json.dumps(result, indent=2)
        return _format_mfn_audit(result)

    elif command == "export-csv":
        return cmd_export_csv(state)

    elif command == "import-csv":
        if not csv_path:
            return json.dumps({"error": "--csv is required for import-csv command."})
        result = cmd_import_csv(state, csv_path)
        # Import always outputs JSON (updated state)
        return json.dumps(result, indent=2)

    else:
        return json.dumps({"error": f"Unknown command: {command}"})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fund Fee Modeler -- blended fee, MFN cascade, promote sensitivity calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  # Dashboard\n"
            "  python3 fund_fee_modeler.py --command dashboard --json '{...}'\n\n"
            "  # Scenario analysis\n"
            "  python3 fund_fee_modeler.py --command scenario --lp-id lp-001 "
            "--proposed-fee 0.011 --json '{...}'\n\n"
            "  # MFN audit\n"
            "  python3 fund_fee_modeler.py --command mfn-audit --json '{...}'\n\n"
            "  # Export CSV\n"
            "  python3 fund_fee_modeler.py --command export-csv --json '{...}' > ledger.csv\n\n"
            "  # Import CSV\n"
            "  python3 fund_fee_modeler.py --command import-csv --csv ledger.csv --json '{...}'\n"
        ),
    )

    parser.add_argument(
        "--command",
        type=str,
        default="dashboard",
        choices=["dashboard", "scenario", "mfn-audit", "export-csv", "import-csv"],
        help="Command to run (default: dashboard)",
    )
    parser.add_argument(
        "--json",
        type=str,
        help="Fund state JSON string (or pipe via stdin)",
    )
    parser.add_argument(
        "--lp-id",
        type=str,
        default=None,
        help="LP identifier for scenario command",
    )
    parser.add_argument(
        "--proposed-fee",
        type=float,
        default=None,
        help="Proposed management fee rate as decimal (e.g. 0.011 for 1.10%%)",
    )
    parser.add_argument(
        "--proposed-terms",
        type=str,
        default=None,
        help="Proposed terms as JSON string (e.g. '{\"managementFee\": 0.011}')",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="CSV file path for import-csv command",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="text",
        choices=["text", "json"],
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Read state JSON
    if args.json:
        try:
            state = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        try:
            state = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON from stdin: {e}"}), file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # Parse proposed-terms if provided
    proposed_terms = None
    if args.proposed_terms:
        try:
            proposed_terms = json.loads(args.proposed_terms)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid --proposed-terms JSON: {e}"}), file=sys.stderr)
            sys.exit(1)

    output = run_command(
        command=args.command,
        state=state,
        lp_id=args.lp_id,
        proposed_fee=args.proposed_fee,
        proposed_terms=proposed_terms,
        csv_path=args.csv,
        output_format=args.format,
    )
    print(output)


if __name__ == "__main__":
    main()
