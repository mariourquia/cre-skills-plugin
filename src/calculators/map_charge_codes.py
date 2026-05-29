#!/usr/bin/env python3
"""
Document-to-Database: Charge-Code / Account Mapper
==================================================
Maps rent-roll charge codes (or, when codes are absent, charge descriptions) to
the canonical chart of accounts, and T-12 account lines to canonical account
slugs. Reuses the residential-multifamily GL crosswalk (no parallel taxonomy).

When a charge code maps directly: high confidence. When only a description
matches: medium confidence + human-review flag. When nothing matches: the row
is NOT guessed -- it is routed to human review (mapped to None / "unmapped").

Selectors travel in --json (run_id optional; no as_of required since this
emits no timestamps). Pure calculate_map_charge_codes(dict)->dict.

Used by: document-to-database, rent-roll-to-database, t12-to-database

Usage:
    python3 src/calculators/map_charge_codes.py --json '{
        "charges": [{"charge_code": "cam", "description": "CAM Recovery"},
                    {"charge_code": null, "description": "Parking - monthly"}],
        "accounts": [{"account_code": "6100", "account_name": "Repairs and Maintenance"}]
    }'

Output: JSON {charge_mappings, account_mappings, summary, human_review_items}.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from ingest import accounts


def calculate_map_charge_codes(inputs: dict) -> dict:
    charges = inputs.get("charges") or []
    accts = inputs.get("accounts") or []

    charge_mappings: list = []
    account_mappings: list = []
    review: list = []

    mapped_charge_dollars = 0.0
    total_charge_dollars = 0.0

    for i, ch in enumerate(charges):
        m = accounts.map_charge_code(ch.get("charge_code"), ch.get("description"))
        m["index"] = i
        charge_mappings.append(m)
        amt = _num(ch.get("monthly_amount")) or _num(ch.get("annual_amount")) or 0.0
        total_charge_dollars += amt
        if m["canonical_account"] is not None:
            mapped_charge_dollars += amt
        if m["needs_review"]:
            review.append({
                "kind": "charge_code", "index": i, "charge_code": m["charge_code"],
                "reason": "unmapped" if m["charge_category"] is None else "inferred_from_description",
                "confidence": m["confidence"],
            })

    mapped_accounts = 0
    for i, a in enumerate(accts):
        m = accounts.map_account(a.get("account_code"), a.get("account_name"))
        m["index"] = i
        account_mappings.append(m)
        if m["canonical_account"] != "unmapped":
            mapped_accounts += 1
        if m["needs_review"]:
            review.append({
                "kind": "account", "index": i, "account_code": m["account_code"],
                "reason": "unmapped" if m["canonical_account"] == "unmapped" else "inferred_from_name",
                "confidence": m["confidence"],
            })

    # Dollar-weighted coverage is the gate-relevant number; code-count is secondary.
    dollar_cov = (mapped_charge_dollars / total_charge_dollars) if total_charge_dollars else 1.0
    code_cov = (sum(1 for m in charge_mappings if m["canonical_account"]) / len(charge_mappings)) if charge_mappings else 1.0
    acct_cov = (mapped_accounts / len(account_mappings)) if account_mappings else 1.0

    return {
        "charge_mappings": charge_mappings,
        "account_mappings": account_mappings,
        "summary": {
            "charge_count": len(charge_mappings),
            "account_count": len(account_mappings),
            "charge_mapping_coverage_by_dollars": round(dollar_cov, 4),
            "charge_mapping_coverage_by_code": round(code_cov, 4),
            "account_mapping_coverage": round(acct_cov, 4),
            "human_review_count": len(review),
        },
        "human_review_items": review,
    }


def _num(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace("$", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Charge-Code / Account Mapper")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_map_charge_codes(inputs), indent=2))


if __name__ == "__main__":
    main()
