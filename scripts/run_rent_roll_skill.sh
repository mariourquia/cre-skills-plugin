#!/usr/bin/env bash
# run_rent_roll_skill.sh -- normalize + validate + grade a rent roll.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
usage() {
  cat <<'EOF'
Usage: scripts/run_rent_roll_skill.sh [INPUT_JSON]
  Normalize a tokenized rent roll into database-ready charge-schedule records,
  validate, and self-grade. Default fixture:
  tests/fixtures/ingestion/rent_roll_with_charge_codes.json
  Output: JSON {payload, validation, grade} to stdout.
EOF
}
case "${1:-}" in -h|--help) usage; exit 0 ;; esac
INPUT="${1:-$ROOT/tests/fixtures/ingestion/rent_roll_with_charge_codes.json}"
[ -f "$INPUT" ] || { echo "ERROR: input not found: $INPUT" >&2; exit 1; }
cd "$ROOT"
INGEST_INPUT="$INPUT" python3 - <<'PY'
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src", "calculators"))
import normalize_tokens as N, validate_payload as V, grade_ingestion as G
t = json.load(open(os.environ["INGEST_INPUT"]))
t.setdefault("doc_type", "rent_roll")
payload = N.calculate_normalize_tokens(t)
if "error" in payload:
    print(json.dumps(payload, indent=2)); sys.exit(2)
prop_type = (t.get("property") or {}).get("property_type", "multifamily")
val = V.calculate_validate_payload({"property_type": prop_type, "payload": payload})
grade = G.calculate_grade_ingestion({"run_id": t.get("run_id", "RUN"), "as_of": t.get("as_of"), "payload": payload, "validation": val})
print(json.dumps({"payload": payload, "validation": val, "grade": grade}, indent=2))
PY
