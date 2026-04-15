#!/usr/bin/env bash
# verify-install.sh -- Health check for the CRE Skills Plugin installation
#
# Checks:
#   1. Plugin is registered with Claude Code
#   2. All SKILL.md files exist (one per skill directory)
#   3. All reference files exist (non-zero byte)
#   4. Python calculators are syntactically valid
#   5. hooks.json is valid JSON
#   6. Node.js hook scripts parse correctly
#   7. ~/.cre-skills/ directory is writable
#
# Usage:
#   ./scripts/verify-install.sh
#   ./scripts/verify-install.sh --json     # machine-readable output

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors and formatting
# ---------------------------------------------------------------------------
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

pass()  { printf "  ${GREEN}PASS${RESET}  %s\n" "$1"; }
fail_check()  { printf "  ${RED}FAIL${RESET}  %s\n" "$1"; FAILURES=$((FAILURES + 1)); }
warn_check()  { printf "  ${YELLOW}WARN${RESET}  %s\n" "$1"; WARNINGS=$((WARNINGS + 1)); }
section() { echo ""; printf "${CYAN}${BOLD}  %s${RESET}\n" "$1"; echo "  $(printf '%0.s-' {1..50})"; }

FAILURES=0
WARNINGS=0
JSON_MODE=false

# Check for --json flag
for arg in "$@"; do
  [ "$arg" = "--json" ] && JSON_MODE=true
done

# ---------------------------------------------------------------------------
# Locate repo root
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$REPO_ROOT/src"

if [ ! -f "$REPO_ROOT/.claude-plugin/plugin.json" ]; then
  printf "${RED}ERROR: Cannot locate plugin root at %s${RESET}\n" "$REPO_ROOT"
  exit 1
fi

# ---------------------------------------------------------------------------
# Home directory -- portable
# ---------------------------------------------------------------------------
if [ -z "${HOME:-}" ]; then
  HOME="$(cd ~ && pwd)"
  export HOME
fi

DATA_DIR="$HOME/.cre-skills"

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------
if [ "$JSON_MODE" = false ]; then
  echo ""
  printf "${BOLD}  CRE Skills Plugin -- Install Verification${RESET}\n"
  printf "  Plugin root: ${DIM}%s${RESET}\n" "$REPO_ROOT"
fi

# ---------------------------------------------------------------------------
# Check 1: Plugin registration
# ---------------------------------------------------------------------------
section "1. Claude Code plugin registration"

if ! command -v claude &>/dev/null; then
  warn_check "Claude CLI not found. Cannot verify plugin registration."
else
  if claude plugin list 2>/dev/null | grep -q "cre-skills"; then
    pass "Plugin 'cre-skills' appears in 'claude plugin list'"
  else
    warn_check "'cre-skills' not found in 'claude plugin list'. Plugin may need re-adding."
    warn_check "Run: claude plugin add $REPO_ROOT"
  fi
fi

# ---------------------------------------------------------------------------
# Check 2: SKILL.md files
# ---------------------------------------------------------------------------
section "2. Skill SKILL.md files"

SKILL_DIRS=()
while IFS= read -r -d '' d; do
  SKILL_DIRS+=("$d")
done < <(find "$SRC_DIR/skills" -maxdepth 1 -mindepth 1 -type d -print0 | sort -z)

SKILL_TOTAL=${#SKILL_DIRS[@]}
SKILL_MISSING=0

for d in "${SKILL_DIRS[@]}"; do
  slug="$(basename "$d")"
  if [ ! -f "$d/SKILL.md" ]; then
    fail_check "Missing SKILL.md: skills/$slug/"
    SKILL_MISSING=$((SKILL_MISSING + 1))
  fi
done

if [ "$SKILL_MISSING" -eq 0 ]; then
  pass "$SKILL_TOTAL skill directories all have SKILL.md"
else
  fail_check "$SKILL_MISSING of $SKILL_TOTAL skill directories are missing SKILL.md"
fi

# ---------------------------------------------------------------------------
# Check 3: Reference files (non-empty)
# ---------------------------------------------------------------------------
section "3. Reference files"

REF_TOTAL=0
REF_EMPTY=0

while IFS= read -r -d '' f; do
  REF_TOTAL=$((REF_TOTAL + 1))
  if [ ! -s "$f" ]; then
    fail_check "Empty reference file: ${f#"$REPO_ROOT/"}"
    REF_EMPTY=$((REF_EMPTY + 1))
  fi
done < <(find "$SRC_DIR/skills" -path "*/references/*" -type f -print0)

if [ "$REF_EMPTY" -eq 0 ]; then
  pass "$REF_TOTAL reference files all non-empty"
else
  fail_check "$REF_EMPTY of $REF_TOTAL reference files are empty"
fi

# ---------------------------------------------------------------------------
# Check 4: Python calculator syntax
# ---------------------------------------------------------------------------
section "4. Python calculators"

CALC_DIR="$SRC_DIR/calculators"
CALC_TOTAL=0
CALC_ERRORS=0

if [ ! -d "$CALC_DIR" ]; then
  warn_check "Calculator directory not found: src/calculators/"
elif ! command -v python3 &>/dev/null; then
  warn_check "python3 not found. Cannot verify calculator syntax."
else
  while IFS= read -r -d '' f; do
    CALC_TOTAL=$((CALC_TOTAL + 1))
    fname="$(basename "$f")"
    err="$(python3 -c "
import ast, sys
with open(sys.argv[1]) as fh:
    src = fh.read()
try:
    ast.parse(src)
    print('ok')
except SyntaxError as e:
    print(f'error: {e}')
" "$f" 2>&1)"
    if [ "$err" = "ok" ]; then
      : # silent on pass
    else
      fail_check "Syntax error in $fname: $err"
      CALC_ERRORS=$((CALC_ERRORS + 1))
    fi
  done < <(find "$CALC_DIR" -name '*.py' -print0)

  if [ "$CALC_ERRORS" -eq 0 ] && [ "$CALC_TOTAL" -gt 0 ]; then
    pass "$CALC_TOTAL Python calculators are syntactically valid"
  elif [ "$CALC_TOTAL" -eq 0 ]; then
    warn_check "No Python calculator files found in src/calculators/"
  fi

  # Check executability
  NOT_EXEC=0
  while IFS= read -r -d '' f; do
    if [ ! -x "$f" ]; then
      NOT_EXEC=$((NOT_EXEC + 1))
    fi
  done < <(find "$CALC_DIR" -name '*.py' -print0)
  if [ "$NOT_EXEC" -gt 0 ]; then
    warn_check "$NOT_EXEC calculators are not executable. Run: chmod +x src/calculators/*.py"
  fi
fi

# ---------------------------------------------------------------------------
# Check 5: hooks.json validity
# ---------------------------------------------------------------------------
section "5. hooks.json"

HOOKS_FILE="$SRC_DIR/hooks/hooks.json"

if [ ! -f "$HOOKS_FILE" ]; then
  fail_check "hooks/hooks.json not found"
else
  if python3 -c "import json; json.load(open('$HOOKS_FILE'))" 2>/dev/null; then
    pass "hooks/hooks.json is valid JSON"
  else
    fail_check "hooks/hooks.json is not valid JSON"
  fi
fi

# ---------------------------------------------------------------------------
# Check 6: Node.js hook scripts
# ---------------------------------------------------------------------------
section "6. Node.js hook scripts"

HOOKS_DIR="$SRC_DIR/hooks"
HOOK_ERRORS=0

if ! command -v node &>/dev/null; then
  warn_check "node not found. Cannot verify hook script syntax."
else
  for script in telemetry-init.mjs telemetry-capture.mjs session-summary.mjs; do
    f="$HOOKS_DIR/$script"
    if [ ! -f "$f" ]; then
      fail_check "Missing hook script: hooks/$script"
      HOOK_ERRORS=$((HOOK_ERRORS + 1))
      continue
    fi

    # Use --check flag equivalent: parse via node --input-type=module with syntax check
    if node --check "$f" 2>/dev/null; then
      : # silent pass
    else
      fail_check "Syntax error in hooks/$script"
      HOOK_ERRORS=$((HOOK_ERRORS + 1))
    fi
  done

  if [ "$HOOK_ERRORS" -eq 0 ]; then
    pass "All 3 Node.js hook scripts parse correctly"
  fi

  # Check Node.js version
  node_ver="$(node --version 2>/dev/null | tr -d 'v')"
  node_major="$(printf '%s' "$node_ver" | cut -d. -f1)"
  if [ "${node_major:-0}" -lt 18 ]; then
    warn_check "Node.js v$node_ver detected. Hooks require v18+. Upgrade: https://nodejs.org/"
  fi
fi

# ---------------------------------------------------------------------------
# Check 7: ~/.cre-skills/ writability
# ---------------------------------------------------------------------------
section "7. User data directory"

if [ -d "$DATA_DIR" ]; then
  if [ -w "$DATA_DIR" ]; then
    pass "$DATA_DIR exists and is writable"
  else
    fail_check "$DATA_DIR exists but is not writable. Run: chmod u+w $DATA_DIR"
  fi
else
  # Try to create it
  if mkdir -p "$DATA_DIR" 2>/dev/null; then
    if [ -w "$DATA_DIR" ]; then
      pass "$DATA_DIR created and is writable"
    else
      fail_check "$DATA_DIR created but is not writable"
    fi
  else
    fail_check "Cannot create $DATA_DIR. Check permissions on $HOME"
  fi
fi

# Check config.json if it exists
if [ -f "$DATA_DIR/config.json" ]; then
  if python3 -c "import json; json.load(open('$DATA_DIR/config.json'))" 2>/dev/null; then
    pass "$DATA_DIR/config.json is valid JSON"
  else
    fail_check "$DATA_DIR/config.json is malformed. Delete it to reset on next session start."
  fi
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
printf "${BOLD}  Summary${RESET}\n"
echo "  $(printf '%0.s-' {1..50})"
echo ""

if [ "$FAILURES" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
  printf "  ${GREEN}${BOLD}All checks passed.${RESET} Plugin is healthy.\n"
elif [ "$FAILURES" -eq 0 ]; then
  printf "  ${YELLOW}${BOLD}%d warning(s), 0 failures.${RESET} Plugin should work but review warnings.\n" "$WARNINGS"
else
  printf "  ${RED}${BOLD}%d failure(s), %d warning(s).${RESET} Fix failures before using the plugin.\n" "$FAILURES" "$WARNINGS"
fi

echo ""
printf "  Skills:     ${BOLD}%d${RESET} directories checked\n" "$SKILL_TOTAL"
printf "  References: ${BOLD}%d${RESET} files checked\n" "$REF_TOTAL"
printf "  Calculators:${BOLD}%d${RESET} scripts checked\n" "${CALC_TOTAL:-0}"
echo ""

# ---------------------------------------------------------------------------
# JSON output mode
# ---------------------------------------------------------------------------
if [ "$JSON_MODE" = true ]; then
  python3 -c "
import json
print(json.dumps({
    'version': open('$REPO_ROOT/.claude-plugin/plugin.json').read(),
    'failures': $FAILURES,
    'warnings': $WARNINGS,
    'skill_dirs': $SKILL_TOTAL,
    'ref_files': $REF_TOTAL,
    'calculators': ${CALC_TOTAL:-0},
    'healthy': $( [ $FAILURES -eq 0 ] && echo 'true' || echo 'false'),
}, indent=2))
" 2>/dev/null
fi

# Exit non-zero if there are failures
[ "$FAILURES" -eq 0 ] || exit 1
