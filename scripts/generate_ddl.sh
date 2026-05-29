#!/usr/bin/env bash
# generate_ddl.sh -- emit target-model CREATE TABLE DDL (and the load plan).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
usage() {
  cat <<'EOF'
Usage: scripts/generate_ddl.sh [PROFILE]
  Emit reviewable, DML-free Postgres DDL + an FK-ordered load plan for a
  target-model profile. PROFILE in: raw_landing | normalized_relational |
  star_schema | data_vault | hybrid_recommended (default: normalized_relational).
  Output: JSON {ddl, load_plan} to stdout. Target-warehouse DDL; not executed.
EOF
}
case "${1:-}" in -h|--help) usage; exit 0 ;; esac
PROFILE="${1:-normalized_relational}"
cd "$ROOT"
INGEST_PROFILE="$PROFILE" python3 - <<'PY'
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src", "calculators"))
import emit_sql_ddl as D, emit_load_plan as L
profile = os.environ["INGEST_PROFILE"]
ddl = D.calculate_emit_sql_ddl({"profile": profile})
if "error" in ddl:
    print(json.dumps(ddl, indent=2)); sys.exit(2)
plan = L.calculate_emit_load_plan({"profile": profile})
print(json.dumps({"ddl": ddl, "load_plan": plan}, indent=2))
PY
