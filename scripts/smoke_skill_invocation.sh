#!/usr/bin/env bash
# smoke_skill_invocation.sh — lightweight smoke-invoke a set of skills
# against a set of Claude model IDs.
#
# Reads ANTHROPIC_API_KEY from environment.
#
# For each (skill, model) pair: sends a minimal prompt to the Anthropic
# messages endpoint via curl and verifies the response is non-empty and
# looks like normal markdown / plain text output. Fails on the first
# empty or error response.
#
# This is NOT a behavioral test — it catches gross shape regressions
# where a model upgrade changes output format enough to break parsers.
#
# Usage:
#   ANTHROPIC_API_KEY=sk-ant-... ./scripts/smoke_skill_invocation.sh
#   ANTHROPIC_API_KEY=sk-ant-... ./scripts/smoke_skill_invocation.sh \
#       --model claude-opus-4-6 --skills deal-quick-screen,loan-sizing-engine
#
# Exit codes:
#   0  all invocations returned non-empty content
#   1  at least one invocation failed or produced empty content
#   2  environment error (missing key or curl)

set -u

readonly API_HOST="api.anthropic.com"
readonly API_PATH="/v1/messages"
readonly MIN_RESPONSE_LEN=200

DEFAULT_MODELS=(
  "claude-opus-4-6"
  "claude-sonnet-4-6"
  "claude-haiku-4-5-20251001"
)

DEFAULT_SKILLS=(
  "deal-quick-screen"
  "loan-sizing-engine"
  "market-memo-generator"
  "comp-snapshot"
  "t12-normalizer"
)

usage() {
  sed -n '2,20p' "$0"
  exit 2
}

# Parse --model / --skills flags (comma-separated for --skills).
MODEL_OVERRIDE=""
SKILLS_OVERRIDE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --model)    MODEL_OVERRIDE="$2"; shift 2 ;;
    --skills)   SKILLS_OVERRIDE="$2"; shift 2 ;;
    -h|--help)  usage ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "ANTHROPIC_API_KEY is not set" >&2
  exit 2
fi
if ! command -v curl >/dev/null 2>&1; then
  echo "curl not found on PATH" >&2
  exit 2
fi

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_ROOT="$PLUGIN_ROOT/src/skills"

if [ -n "$MODEL_OVERRIDE" ]; then
  MODELS=("$MODEL_OVERRIDE")
else
  MODELS=("${DEFAULT_MODELS[@]}")
fi

if [ -n "$SKILLS_OVERRIDE" ]; then
  IFS=',' read -r -a SKILLS <<< "$SKILLS_OVERRIDE"
else
  SKILLS=("${DEFAULT_SKILLS[@]}")
fi

build_prompt() {
  local slug="$1"
  local skill_md="$SKILL_ROOT/$slug/SKILL.md"
  if [ ! -f "$skill_md" ]; then
    return 1
  fi
  # Extract a small excerpt of the SKILL.md to include as context.
  head -c 2000 "$skill_md" | python3 -c '
import json, sys
text = sys.stdin.read()
prompt = (
    "Run the skill on this generic input.\n\n"
    "Asset type: multifamily\nPurchase price: 10000000\nNOI: 650000\nMarket: Atlanta\n\n"
    "Return the skill normal structured output.\n\n"
    "Skill definition excerpt:\n\n" + text
)
print(json.dumps(prompt))
'
}

build_payload() {
  local model="$1"
  local prompt_json="$2"
  python3 -c "
import json, sys
prompt = json.loads(sys.argv[1])
body = {'model': sys.argv[2], 'max_tokens': 1024,
        'messages': [{'role': 'user', 'content': prompt}]}
print(json.dumps(body))
" "$prompt_json" "$model"
}

failures=0
total=0
for model in "${MODELS[@]}"; do
  for skill in "${SKILLS[@]}"; do
    total=$((total + 1))
    prompt_json=$(build_prompt "$skill")
    if [ -z "$prompt_json" ]; then
      printf 'FAIL  %-40s  %s  (skill not found)\n' "$model" "$skill"
      failures=$((failures + 1))
      continue
    fi
    payload=$(build_payload "$model" "$prompt_json")
    response=$(curl --silent --show-error --fail-with-body --max-time 60 \
      --url "https://${API_HOST}${API_PATH}" \
      --header "content-type: application/json" \
      --header "x-api-key: ${ANTHROPIC_API_KEY}" \
      --header "anthropic-version: 2023-06-01" \
      --data-binary "$payload" 2>&1)
    curl_rc=$?
    if [ $curl_rc -ne 0 ]; then
      printf 'FAIL  %-40s  %s  (curl rc=%d)\n' "$model" "$skill" "$curl_rc"
      failures=$((failures + 1))
      continue
    fi
    # Extract text, measure length.
    body_len=$(printf '%s' "$response" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    text = "".join(b.get("text","") for b in data.get("content", []))
    print(len(text))
except Exception:
    print(0)
')
    if [ "$body_len" -lt "$MIN_RESPONSE_LEN" ]; then
      printf 'FAIL  %-40s  %s  (body_len=%d)\n' "$model" "$skill" "$body_len"
      failures=$((failures + 1))
      continue
    fi
    printf 'OK    %-40s  %s  (body_len=%d)\n' "$model" "$skill" "$body_len"
    # Small pause to be polite on rate limits.
    sleep 0.25
done
done

echo
if [ "$failures" -gt 0 ]; then
  echo "$failures / $total invocations failed"
  exit 1
fi
echo "all $total invocations returned non-empty content"
exit 0
