#!/usr/bin/env bash
# run_document_to_database.sh -- end-to-end document-to-database ingestion.
# Detects the input shape: a tie-out fixture ({rent_roll, t12}) runs the full
# normalize -> reconcile -> grade chain; a single document runs
# normalize -> validate -> grade. Emits one combined JSON report to stdout.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: scripts/run_document_to_database.sh [INPUT_JSON]

  Ingest a tokenized CRE document (or a tie-out pair) into a validated,
  graded, database-ready report.

  INPUT_JSON  Path to a token stream. If it has {rent_roll, t12} keys it is
              reconciled; otherwise it is treated as a single document.
              Default: tests/fixtures/ingestion/tieout_clean.json

  Output: combined JSON to stdout. Deterministic for a fixed as_of/run_id.
EOF
}

case "${1:-}" in -h|--help) usage; exit 0 ;; esac

INPUT="${1:-$ROOT/tests/fixtures/ingestion/tieout_clean.json}"
if [ ! -f "$INPUT" ]; then
  echo "ERROR: input not found: $INPUT" >&2
  exit 1
fi

cd "$ROOT"
INGEST_INPUT="$INPUT" python3 - <<'PY'
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src", "calculators"))
import normalize_tokens as N, validate_payload as V, reconcile_rent_roll_t12 as R, grade_ingestion as G

data = json.load(open(os.environ["INGEST_INPUT"]))

def fail(o):
    print(json.dumps(o, indent=2)); sys.exit(2)

if "rent_roll" in data and "t12" in data:
    rr = N.calculate_normalize_tokens(data["rent_roll"])
    t12 = N.calculate_normalize_tokens(data["t12"])
    if "error" in rr: fail(rr)
    if "error" in t12: fail(t12)
    as_of = data["rent_roll"].get("as_of")
    run_id = data["rent_roll"].get("run_id", "RUN")
    rec = R.calculate_reconcile_rent_roll_t12({"run_id": run_id, "as_of": as_of, "rent_roll": rr, "t12": t12})
    val = V.calculate_validate_payload({"property_type": (data["rent_roll"].get("property") or {}).get("property_type", "multifamily"), "payload": rr})
    grade = G.calculate_grade_ingestion({"run_id": run_id, "as_of": as_of, "payload": rr, "validation": val, "reconciliation": rec})
    print(json.dumps({"rent_roll": rr, "t12": t12, "validation": val, "reconciliation": rec, "grade": grade}, indent=2))
else:
    payload = N.calculate_normalize_tokens(data)
    if "error" in payload: fail(payload)
    prop_type = (data.get("property") or {}).get("property_type", "multifamily")
    val = V.calculate_validate_payload({"property_type": prop_type, "payload": payload})
    grade = G.calculate_grade_ingestion({"run_id": data.get("run_id", "RUN"), "as_of": data.get("as_of"), "payload": payload, "validation": val})
    print(json.dumps({"payload": payload, "validation": val, "grade": grade}, indent=2))
PY
