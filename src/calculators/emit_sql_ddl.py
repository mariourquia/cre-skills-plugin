#!/usr/bin/env python3
"""
Document-to-Database: SQL DDL Emitter
=====================================
Emits reviewable CREATE TABLE DDL for a target-model profile. This is
target-WAREHOUSE DDL (Postgres dialect): it carries primary keys and, for the
normalized / star / vault profiles, FOREIGN KEY constraints and a topological
load order. It is NOT the amos-prototype staging schema -- AMOS staging
(migration 005) is deliberately FK-free and session-scoped because the Neon
HTTP driver runs one statement per round-trip.

The emitter NEVER produces DML: no INSERT/UPDATE/DELETE/DROP/TRUNCATE. It is a
specification artifact a human reviews and applies; it does not execute.

Pure calculate_emit_sql_ddl(dict)->dict; profile travels in --json.

Used by: document-to-database

Usage:
    python3 src/calculators/emit_sql_ddl.py --json '{"profile": "star_schema", "dialect": "postgres"}'

Output: JSON {profile, dialect, statements, ddl}.
"""
from __future__ import annotations

import argparse
import json
import sys

from ingest import profiles


def calculate_emit_sql_ddl(inputs: dict) -> dict:
    profile = (inputs.get("profile") or "normalized_relational").strip()
    dialect = (inputs.get("dialect") or "postgres").strip().lower()
    if profile not in profiles.TARGET_PROFILES:
        return {"error": "unknown profile '%s'" % profile, "known_profiles": list(profiles.TARGET_PROFILES)}
    if dialect != "postgres":
        return {"error": "only the 'postgres' dialect is supported", "requested": dialect}

    catalog = profiles.profile_tables(profile)
    # Order so FK targets are created before referrers.
    ordered = sorted(catalog.items(), key=lambda kv: (kv[1]["load_order"], kv[0]))

    statements = [_ddl_for_table(name, spec) for name, spec in ordered]
    ddl = "\n\n".join(statements)
    return {
        "profile": profile,
        "dialect": dialect,
        "table_count": len(statements),
        "statements": statements,
        "ddl": ddl,
        "note": "Target-warehouse DDL. Not executed by amos-prototype; AMOS staging is FK-free (migration 005).",
    }


def _ddl_for_table(name: str, spec: dict) -> str:
    parts = []
    for (col, sqltype, nullable) in spec["columns"]:
        parts.append("  %s %s%s" % (col, sqltype, "" if nullable else " not null"))
    pk = spec.get("primary_key") or []
    if pk:
        parts.append("  primary key (%s)" % ", ".join(pk))
    for (col, ref_table, ref_col) in spec.get("foreign_keys", []):
        parts.append("  foreign key (%s) references %s (%s)" % (col, ref_table, ref_col))
    return "create table if not exists %s (\n%s\n);" % (name, ",\n".join(parts))


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database SQL DDL Emitter")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_emit_sql_ddl(inputs), indent=2))


if __name__ == "__main__":
    main()
