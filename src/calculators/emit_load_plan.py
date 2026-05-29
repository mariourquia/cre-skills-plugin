#!/usr/bin/env python3
"""
Document-to-Database: Load Plan Emitter
=======================================
Emits a reviewable, FK-ordered load plan for a target-model profile: the table
load order (every FK target precedes its referrer), the upsert keys (the
primary key) per table, and each table's dependencies. The plan is a
specification -- it does NOT execute against any database.

Pure calculate_emit_load_plan(dict)->dict; profile travels in --json.

Used by: document-to-database

Usage:
    python3 src/calculators/emit_load_plan.py --json '{"profile": "normalized_relational"}'

Output: JSON {profile, load_order, topologically_valid, note}.
"""
from __future__ import annotations

import argparse
import json
import sys

from ingest import profiles


def calculate_emit_load_plan(inputs: dict) -> dict:
    profile = (inputs.get("profile") or "normalized_relational").strip()
    if profile not in profiles.TARGET_PROFILES:
        return {"error": "unknown profile '%s'" % profile, "known_profiles": list(profiles.TARGET_PROFILES)}

    catalog = profiles.profile_tables(profile)
    ordered = sorted(catalog.items(), key=lambda kv: (kv[1]["load_order"], kv[0]))

    plan = []
    loaded: set = set()
    valid = True
    for name, spec in ordered:
        deps = sorted({ref_table for (_c, ref_table, _rc) in spec.get("foreign_keys", []) if ref_table in catalog})
        # A dependency must already be loaded for the order to be valid.
        unmet = [d for d in deps if d not in loaded]
        if unmet:
            valid = False
        plan.append({
            "table": name,
            "load_order": spec["load_order"],
            "grain": spec["grain"],
            "upsert_keys": spec.get("primary_key", []),
            "depends_on": deps,
            "unmet_dependencies": unmet,
        })
        loaded.add(name)

    return {
        "profile": profile,
        "table_count": len(plan),
        "load_order": plan,
        "topologically_valid": valid,
        "note": "Specification only; not executed. Load tables in the listed order; "
                "upsert on the listed keys. amos-prototype staging is FK-free (migration 005).",
    }


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Load Plan Emitter")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_emit_load_plan(inputs), indent=2))


if __name__ == "__main__":
    main()
