#!/usr/bin/env bash
# run_rent_roll_t12_tieout.sh -- normalize both sides, reconcile, and grade.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
usage() {
  cat <<'EOF'
Usage: scripts/run_rent_roll_t12_tieout.sh [INPUT_JSON]
  Reconcile a rent roll against a T-12. INPUT_JSON must carry {rent_roll, t12}
  token streams. Default fixture: tests/fixtures/ingestion/tieout_clean.json
  (try tieout_mapping_variance.json / tieout_timing_variance.json /
  tieout_missing_tenant.json). Output: JSON {reconciliation, grade} to stdout.
EOF
}
case "${1:-}" in -h|--help) usage; exit 0 ;; esac
INPUT="${1:-$ROOT/tests/fixtures/ingestion/tieout_clean.json}"
[ -f "$INPUT" ] || { echo "ERROR: input not found: $INPUT" >&2; exit 1; }
cd "$ROOT"
INGEST_INPUT="$INPUT" python3 - <<'PY'
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src", "calculators"))
import normalize_tokens as N, validate_payload as V, reconcile_rent_roll_t12 as R, grade_ingestion as G
d = json.load(open(os.environ["INGEST_INPUT"]))
if "rent_roll" not in d or "t12" not in d:
    print(json.dumps({"error": "input must contain {rent_roll, t12} token streams"}, indent=2)); sys.exit(2)
rr = N.calculate_normalize_tokens(d["rent_roll"])
t12 = N.calculate_normalize_tokens(d["t12"])
for o in (rr, t12):
    if "error" in o:
        print(json.dumps(o, indent=2)); sys.exit(2)
as_of = d["rent_roll"].get("as_of"); run_id = d["rent_roll"].get("run_id", "RUN")
rec = R.calculate_reconcile_rent_roll_t12({"run_id": run_id, "as_of": as_of, "rent_roll": rr, "t12": t12})
val = V.calculate_validate_payload({"property_type": (d["rent_roll"].get("property") or {}).get("property_type", "multifamily"), "payload": rr})
grade = G.calculate_grade_ingestion({"run_id": run_id, "as_of": as_of, "payload": rr, "validation": val, "reconciliation": rec})
print(json.dumps({"reconciliation": rec, "grade": grade}, indent=2))
PY
