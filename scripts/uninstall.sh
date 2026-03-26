#!/usr/bin/env bash
# uninstall.sh -- Remove the CRE Skills Plugin
#
# Usage:
#   ./scripts/uninstall.sh

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors and formatting
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

info()    { printf "${CYAN}[INFO]${RESET}  %s\n" "$1"; }
success() { printf "${GREEN}[OK]${RESET}    %s\n" "$1"; }
warn()    { printf "${YELLOW}[WARN]${RESET}  %s\n" "$1"; }
fail()    { printf "${RED}[FAIL]${RESET}  %s\n" "$1"; exit 1; }

# ---------------------------------------------------------------------------
# Locate repo root
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ ! -f "$REPO_ROOT/.claude-plugin/plugin.json" ]; then
  fail "Cannot locate plugin root. Run this script from inside the cre-skills-plugin directory."
fi

cd "$REPO_ROOT"

# ---------------------------------------------------------------------------
# Home directory -- portable
# ---------------------------------------------------------------------------
if [ -z "${HOME:-}" ]; then
  HOME="$(cd ~ && pwd)"
  export HOME
fi

DATA_DIR="$HOME/.cre-skills"

# ---------------------------------------------------------------------------
# Confirm uninstall
# ---------------------------------------------------------------------------
confirm_uninstall() {
  echo ""
  printf "${YELLOW}${BOLD}  This will remove the CRE Skills Plugin from Claude Code.${RESET}\n"
  echo ""

  if [ -t 0 ]; then
    printf "${BOLD}  Proceed with uninstall? [y/N] ${RESET}"
    read -r confirm
    if [[ ! "${confirm:-n}" =~ ^[Yy]$ ]]; then
      info "Uninstall cancelled."
      exit 0
    fi
  fi
}

# ---------------------------------------------------------------------------
# Remove plugin from Claude Code
# ---------------------------------------------------------------------------
remove_plugin() {
  info "Removing plugin from Claude Code..."

  if ! command -v claude &>/dev/null; then
    warn "Claude CLI not found. Skipping 'claude plugin remove'."
    warn "If you registered the plugin manually, remove it from your Claude Code settings."
    return 0
  fi

  if claude plugin remove cre-skills 2>/dev/null; then
    success "Plugin removed from Claude Code"
  else
    warn "'claude plugin remove cre-skills' did not succeed."
    warn "The plugin may already be unregistered, or the CLI version does not support this command."
    warn "If it still appears in Claude Code, remove it via Settings > Plugins."
  fi
}

# ---------------------------------------------------------------------------
# Ask about user data
# ---------------------------------------------------------------------------
handle_user_data() {
  if [ ! -d "$DATA_DIR" ]; then
    info "No user data directory found ($DATA_DIR)"
    return 0
  fi

  echo ""
  printf "  ${BOLD}User data found at:${RESET} $DATA_DIR\n"
  echo ""

  # List what's there
  local has_telemetry=false has_feedback=false has_config=false has_brand=false
  [ -f "$DATA_DIR/telemetry.jsonl" ]       && has_telemetry=true
  [ -f "$DATA_DIR/feedback.jsonl" ]        && has_feedback=true
  [ -f "$DATA_DIR/config.json" ]           && has_config=true
  [ -f "$DATA_DIR/brand-guidelines.json" ] && has_brand=true

  printf "  Contents:\n"
  "$has_config"    && printf "    - config.json (opt-in preferences)\n"       || true
  "$has_brand"     && printf "    - brand-guidelines.json (your brand config)\n" || true
  "$has_telemetry" && printf "    - telemetry.jsonl (anonymous usage records)\n" || true
  "$has_feedback"  && printf "    - feedback.jsonl (session feedback)\n"        || true
  echo ""

  if [ -t 0 ]; then
    printf "${BOLD}  Keep ~/.cre-skills/ data? [Y/n] ${RESET}"
    read -r keep
    if [[ "${keep:-y}" =~ ^[Yy]$ ]] || [ -z "${keep:-}" ]; then
      success "User data preserved at $DATA_DIR"
      return 0
    fi
  else
    # Non-interactive: preserve data by default
    success "User data preserved at $DATA_DIR (non-interactive mode)"
    return 0
  fi

  # User chose to delete
  warn "Removing $DATA_DIR ..."
  rm -rf "$DATA_DIR"
  success "User data removed"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  printf "${CYAN}${BOLD}"
  printf "  CRE Skills Plugin -- Uninstall\n"
  printf "${RESET}"
  echo ""

  info "Plugin root: $REPO_ROOT"

  confirm_uninstall
  remove_plugin
  handle_user_data

  echo ""
  printf "${GREEN}${BOLD}  CRE Skills Plugin uninstalled.${RESET}\n"
  echo ""
  printf "  The plugin files remain at: ${DIM}%s${RESET}\n" "$REPO_ROOT"
  printf "  To fully remove: ${DIM}rm -rf %s${RESET}\n" "$REPO_ROOT"
  echo ""
}

main "$@"
