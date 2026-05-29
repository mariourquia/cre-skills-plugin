#!/usr/bin/env bash
# validate_sample.sh -- normalize a sample document and print its validation report.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
usage() {
  cat <<'EOF'
Usage: scripts/validate_sample.sh [INPUT_JSON]
  Normalize a tokenized document and print the validation report (type/range/
  nullability + cross-field reconciliations). Default fixture:
  tests/fixtures/ingestion/rent_roll_with_charge_codes.json
  Output: JSON validation report to stdout. Exit 3 if status is fail/critical.
EOF
}
case "${1:-}" in -h|--help) usage; exit 0 ;; esac
INPUT="${1:-$ROOT/tests/fixtures/ingestion/rent_roll_with_charge_codes.json}"
[ -f "$INPUT" ] || { echo "ERROR: input not found: $INPUT" >&2; exit 1; }
cd "$ROOT"
INGEST_INPUT="$INPUT" python3 - <<'PY'
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src", "calculators"))
import normalize_tokens as N, validate_payload as V
t = json.load(open(os.environ["INGEST_INPUT"]))
payload = N.calculate_normalize_tokens(t)
if "error" in payload:
    print(json.dumps(payload, indent=2)); sys.exit(2)
prop_type = (t.get("property") or {}).get("property_type", "multifamily")
rep = V.calculate_validate_payload({"property_type": prop_type, "payload": payload})
print(json.dumps(rep, indent=2))
sys.exit(3 if rep.get("validation_status") in ("fail", "critical") else 0)
PY
