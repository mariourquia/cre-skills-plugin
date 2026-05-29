#!/usr/bin/env python3
"""
Document-to-Database: Target-Model Mapper
=========================================
Maps a canonical payload into a chosen target-model profile (raw_landing,
normalized_relational, star_schema, data_vault, hybrid_recommended) and reports
the row counts and representative rows per table. This proves the payload maps
cleanly to the selected profile before any DDL / load plan is emitted.

These are TARGET-WAREHOUSE shapes; they are not the amos-prototype staging
tables (those are a flatter, FK-free, session-scoped subset -- see migration
005 + the AMOS integration doc).

Pure calculate_map_to_target_model(dict)->dict; profile travels in --json.

Used by: document-to-database

Usage:
    python3 src/calculators/map_to_target_model.py --json '{
        "profile": "normalized_relational",
        "payload": { ...normalize_tokens output... },
        "validation": { ...optional... },
        "reconciliation": { ...optional... }
    }'

Output: JSON {profile, tables:{name:{row_count, sample_row}}, summary}.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from ingest import profiles


def calculate_map_to_target_model(inputs: dict) -> dict:
    profile = (inputs.get("profile") or "hybrid_recommended").strip()
    if profile not in profiles.TARGET_PROFILES:
        return {"error": "unknown profile '%s'" % profile, "known_profiles": list(profiles.TARGET_PROFILES)}

    payload = inputs.get("payload") or {}
    validation = inputs.get("validation") or {}
    reconciliation = inputs.get("reconciliation") or {}
    if not payload:
        return {"error": "missing 'payload' (output of normalize_tokens)"}

    catalog = profiles.profile_tables(profile)
    rows = _build_rows(payload, validation, reconciliation)

    tables: dict = {}
    total_rows = 0
    for tname in catalog:
        trows = rows.get(tname, [])
        tables[tname] = {
            "row_count": len(trows),
            "sample_row": trows[0] if trows else None,
        }
        total_rows += len(trows)

    return {
        "profile": profile,
        "tables": tables,
        "summary": {
            "table_count": len(catalog),
            "tables_populated": sum(1 for t in tables.values() if t["row_count"] > 0),
            "total_rows_mapped": total_rows,
        },
    }


def _build_rows(payload: dict, validation: dict, reconciliation: dict) -> dict:
    """Produce mapped rows keyed by target table name. Fills the tables that
    every profile shares names for; profile_tables() then selects which apply."""
    out: dict = {}
    doc_type = payload.get("doc_type", "rent_roll")
    prop = payload.get("property", {})
    run_id = payload.get("run_id")
    prop_id = prop.get("property_id")

    # raw landing
    out["cre_raw_extraction_record"] = [
        {"raw_id": "%s-%d" % (run_id, i), "doc_type": doc_type,
         "document_hash": payload.get("document_hash", "n/a"), "source_ref": "data-room/%s" % doc_type}
        for i, _r in enumerate(payload.get("records", []))
    ]

    # normalized / star shared dimensions
    if prop_id:
        out["cre_property"] = [{"property_id": prop_id, "property_name": prop.get("property_name"),
                                "market": prop.get("market"), "property_type": prop.get("property_type"),
                                "rentable_sf": prop.get("rentable_sf")}]
        out["dim_property"] = [{"property_key": "PK-%s" % prop_id, "property_id": prop_id,
                                "property_name": prop.get("property_name")}]

    out["cre_account"] = [{"canonical_account": s, **m} for s, m in _used_accounts(payload).items()]
    out["dim_account"] = [{"account_key": "AK-%s" % s, "canonical_account": s, "account_type": m["account_type"]}
                          for s, m in _used_accounts(payload).items()]

    if doc_type == "rent_roll":
        out["cre_unit"] = [{"unit_id": u["unit_id"], "property_id": prop_id, **{k: u.get(k) for k in ("suite", "unit_type", "rentable_sf", "unit_status")}}
                           for u in payload.get("units", [])]
        out["cre_lease"] = [{"lease_id": l["lease_id"], **{k: l.get(k) for k in ("unit_id", "lease_status", "lease_type", "lease_start", "lease_expire", "recovery_method", "base_year")}}
                            for l in payload.get("leases", [])]
        out["cre_charge_schedule"] = [{"charge_line_id": "%s-c%d" % (cl.get("lease_id"), i), **{k: cl.get(k) for k in ("lease_id", "charge_code", "charge_category", "canonical_account", "monthly_amount", "annual_amount", "frequency", "is_recoverable")}}
                                      for i, cl in enumerate(payload.get("records", []))]
        out["fact_lease_charge"] = [{"lease_charge_fact_id": "%s-f%d" % (cl.get("lease_id"), i),
                                     "lease_key": "LK-%s" % cl.get("lease_id"), "monthly_amount": cl.get("monthly_amount")}
                                    for i, cl in enumerate(payload.get("records", []))]
    else:
        out["cre_operating_statement_line"] = [{"os_line_id": "%s-o%d" % (prop_id, i), "property_id": prop_id,
                                                **{k: r.get(k) for k in ("canonical_account", "statement_section", "line_type", "fiscal_period", "amount")}}
                                               for i, r in enumerate(payload.get("records", []))]
        out["fact_operating_statement"] = [{"os_fact_id": "%s-of%d" % (prop_id, i), "property_key": "PK-%s" % prop_id,
                                            "account_key": "AK-%s" % r.get("canonical_account"), "line_type": r.get("line_type"), "amount": r.get("amount")}
                                           for i, r in enumerate(payload.get("records", []))]

    # ingestion run + issues + reconciliation
    out["cre_ingestion_run"] = [{"ingestion_run_id": run_id, "doc_type": doc_type, "as_of": payload.get("as_of"), "status": "normalized"}]
    out["cre_validation_issue"] = [{"issue_id": "%s-v%d" % (run_id, i), "ingestion_run_id": run_id,
                                    "code": c.get("code"), "severity": c.get("status"), "field_path": c.get("field_path")}
                                   for i, c in enumerate(validation.get("checks", [])) if c.get("status") in ("warn", "fail", "critical")]
    out["cre_reconciliation_result"] = [{"recon_id": "%s-r%d" % (run_id, i), "ingestion_run_id": run_id,
                                         **{k: d.get(k) for k in ("dimension", "rent_roll_value", "t12_value", "variance", "variance_pct", "difference_type", "tie_status", "residual_unexplained")}}
                                        for i, d in enumerate(reconciliation.get("dimensions", []))]
    out["fact_reconciliation_variance"] = [{"recon_fact_id": "%s-rf%d" % (run_id, i), "property_key": "PK-%s" % prop_id,
                                            "dimension": d.get("dimension"), "variance": d.get("variance"), "difference_type": d.get("difference_type")}
                                           for i, d in enumerate(reconciliation.get("dimensions", []))]

    # data vault hubs from business keys
    out["hub_property"] = [{"property_hk": "HK-%s" % prop_id, "property_bk": prop_id}] if prop_id else []
    return out


def _used_accounts(payload: dict) -> dict:
    from ingest import accounts as acc
    used: dict = {}
    for r in payload.get("records", []):
        slug = r.get("canonical_account")
        if slug and slug in acc.CANONICAL_ACCOUNTS:
            used[slug] = acc.CANONICAL_ACCOUNTS[slug]
    return used


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Target-Model Mapper")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_map_to_target_model(inputs), indent=2))


if __name__ == "__main__":
    main()
