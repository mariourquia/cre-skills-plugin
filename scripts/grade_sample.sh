#!/usr/bin/env bash
# grade_sample.sh -- run the full ingestion chain and print the data-quality grade.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
usage() {
  cat <<'EOF'
Usage: scripts/grade_sample.sh [INPUT_JSON]
  Normalize + validate + grade a sample document (or a {rent_roll, t12} tie-out
  pair) and print the data-quality grade (weakest-link A/B/C + 0-100 + gates).
  Default fixture: tests/fixtures/ingestion/tieout_clean.json
  Output: JSON grade to stdout. Exit 4 if not merge-ready.
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
if "rent_roll" in d and "t12" in d:
    rr = N.calculate_normalize_tokens(d["rent_roll"]); t12 = N.calculate_normalize_tokens(d["t12"])
    as_of = d["rent_roll"].get("as_of"); run_id = d["rent_roll"].get("run_id", "RUN")
    rec = R.calculate_reconcile_rent_roll_t12({"run_id": run_id, "as_of": as_of, "rent_roll": rr, "t12": t12})
    val = V.calculate_validate_payload({"property_type": (d["rent_roll"].get("property") or {}).get("property_type", "multifamily"), "payload": rr})
    grade = G.calculate_grade_ingestion({"run_id": run_id, "as_of": as_of, "payload": rr, "validation": val, "reconciliation": rec})
else:
    payload = N.calculate_normalize_tokens(d)
    if "error" in payload:
        print(json.dumps(payload, indent=2)); sys.exit(2)
    val = V.calculate_validate_payload({"property_type": (d.get("property") or {}).get("property_type", "multifamily"), "payload": payload})
    grade = G.calculate_grade_ingestion({"run_id": d.get("run_id", "RUN"), "as_of": d.get("as_of"), "payload": payload, "validation": val})
print(json.dumps(grade, indent=2))
sys.exit(0 if grade.get("merge_ready") else 4)
PY
