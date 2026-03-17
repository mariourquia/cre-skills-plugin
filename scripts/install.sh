#!/usr/bin/env bash
# install.sh -- Single-command installer for the CRE Skills Plugin
#
# Usage (remote):
#   curl -fsSL https://raw.githubusercontent.com/mariourquia/cre-skills-plugin/main/scripts/install.sh | bash
#
# Usage (local, after cloning):
#   git clone https://github.com/mariourquia/cre-skills-plugin.git
#   cd cre-skills-plugin
#   ./scripts/install.sh

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
# Banner
# ---------------------------------------------------------------------------
print_banner() {
  printf "${CYAN}"
  cat << 'BANNER'

   _____ _____  _____   ____  _  ___ _ _
  / ____|  __ \|  ___| / ___|| |/ (_) | |___
 | |    | |__) | |__   \___ \| ' /| | | / __|
 | |    |  _  /|  __|   ___) | . \| | | \__ \
 | |____|_| \_\|_|____ |____/|_|\_\_|_|_|___/
  \_____|      |______|
   Plugin v1.0.0 -- 80 skills, 40 agents, 6 workflows

BANNER
  printf "${RESET}"
}

# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------
detect_platform() {
  local os
  os="$(uname -s)"
  case "$os" in
    Darwin) PLATFORM="macos" ;;
    Linux)  PLATFORM="linux" ;;
    *)      fail "Unsupported platform: $os. This installer supports macOS and Linux." ;;
  esac
  info "Detected platform: $PLATFORM ($(uname -m))"
}

# ---------------------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------------------
check_git() {
  if ! command -v git &>/dev/null; then
    fail "git is not installed. Install git first: https://git-scm.com/downloads"
  fi
  success "git found: $(git --version)"
}

check_claude() {
  if ! command -v claude &>/dev/null; then
    fail "Claude Code CLI is not installed.

  Install it first:
    npm install -g @anthropic-ai/claude-code

  Then re-run this installer."
  fi
  success "Claude Code CLI found: $(claude --version 2>/dev/null || echo 'installed')"
}

# ---------------------------------------------------------------------------
# Locate or clone the repo
# ---------------------------------------------------------------------------
REPO_URL="https://github.com/mariourquia/cre-skills-plugin.git"
INSTALL_DIR=""

locate_repo() {
  # If we are already inside the repo (local install), use that.
  if [ -f ".claude-plugin/plugin.json" ]; then
    INSTALL_DIR="$(pwd)"
    info "Running from inside the repo: $INSTALL_DIR"
    return
  fi

  # Check one level up (in case cwd is scripts/)
  if [ -f "../.claude-plugin/plugin.json" ]; then
    INSTALL_DIR="$(cd .. && pwd)"
    info "Running from scripts/ directory. Repo root: $INSTALL_DIR"
    return
  fi

  # Not inside the repo -- clone it
  local default_dir="$HOME/.claude/plugins/cre-skills-plugin"
  info "Cloning repo to $default_dir ..."

  if [ -d "$default_dir" ]; then
    warn "Directory already exists: $default_dir"
    info "Pulling latest changes..."
    git -C "$default_dir" pull --ff-only || warn "Pull failed. Using existing copy."
  else
    mkdir -p "$(dirname "$default_dir")"
    git clone "$REPO_URL" "$default_dir"
  fi

  INSTALL_DIR="$default_dir"
  success "Repo ready at $INSTALL_DIR"
}

# ---------------------------------------------------------------------------
# Validate plugin structure
# ---------------------------------------------------------------------------
validate_plugin() {
  local errors=0

  [ -f "$INSTALL_DIR/.claude-plugin/plugin.json" ] || { warn "Missing .claude-plugin/plugin.json"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/skills" ]                      || { warn "Missing skills/ directory"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/agents" ]                      || { warn "Missing agents/ directory"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/routing" ]                     || { warn "Missing routing/ directory"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/commands" ]                    || { warn "Missing commands/ directory"; errors=$((errors + 1)); }
  [ -f "$INSTALL_DIR/hooks/hooks.json" ]            || { warn "Missing hooks/hooks.json"; errors=$((errors + 1)); }

  if [ "$errors" -gt 0 ]; then
    fail "Plugin structure validation failed ($errors errors). The repo may be incomplete."
  fi

  local skill_count
  skill_count="$(find "$INSTALL_DIR/skills" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"
  local agent_count
  agent_count="$(find "$INSTALL_DIR/agents" -maxdepth 1 -name '*.md' ! -name '_*' | wc -l | tr -d ' ')"

  success "Plugin structure valid: $skill_count skills, $agent_count agents"
}

# ---------------------------------------------------------------------------
# Install the plugin
# ---------------------------------------------------------------------------
install_plugin() {
  info "Installing plugin via Claude Code CLI..."

  # claude plugin add expects a path to the plugin directory
  if claude plugin add "$INSTALL_DIR" 2>/dev/null; then
    success "Plugin installed successfully"
  else
    # If the plugin command is not available or fails, fall back to manual instructions
    warn "Automatic installation via 'claude plugin add' did not succeed."
    warn "This may mean the plugin subcommand is not yet available in your CLI version."
    echo ""
    info "Manual installation: run Claude Code with the plugin directory:"
    echo ""
    printf "  ${BOLD}claude --plugin-dir %s${RESET}\n" "$INSTALL_DIR"
    echo ""
    info "Or add to your Claude Code settings to load it automatically."
    return 1
  fi
}

# ---------------------------------------------------------------------------
# Verify installation
# ---------------------------------------------------------------------------
verify_installation() {
  info "Verifying installation..."

  # Check that the cre-route command is discoverable
  # We test by checking that claude recognizes the plugin namespace
  if claude plugin list 2>/dev/null | grep -q "cre-skills"; then
    success "Plugin 'cre-skills' is registered"
  else
    warn "Could not verify plugin registration via 'claude plugin list'."
    warn "The plugin may still work. Try running: /cre-skills:cre-route"
  fi
}

# ---------------------------------------------------------------------------
# Print success message
# ---------------------------------------------------------------------------
print_success() {
  echo ""
  printf "${GREEN}${BOLD}"
  cat << 'SUCCESS'
  ============================================
       CRE Skills Plugin -- Installed
  ============================================
SUCCESS
  printf "${RESET}"
  echo ""
  printf "  ${BOLD}Quick Start${RESET}\n"
  echo ""
  printf "  ${CYAN}/cre-skills:cre-route${RESET}       Find the right skill for any CRE task\n"
  printf "  ${CYAN}/cre-skills:cre-workflows${RESET}   Browse 6 end-to-end workflow chains\n"
  printf "  ${CYAN}/cre-skills:cre-agents${RESET}      List 40 expert subagents\n"
  echo ""
  printf "  ${BOLD}Example Commands${RESET}\n"
  echo ""
  printf "  ${DIM}/cre-skills:cre-route quick screen this deal${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route size a loan for a $15M multifamily${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route generate an IC memo${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route normalize this T-12${RESET}\n"
  echo ""
  printf "  ${BOLD}Skill Categories${RESET}\n"
  echo ""
  printf "  Deal Pipeline      Screening, underwriting, DD, closing\n"
  printf "  Capital Markets    Loan sizing, cap stack, debt monitoring, refi\n"
  printf "  Asset Management   NOI plans, budgets, capex, variance reports\n"
  printf "  Leasing            Abstracts, comps, negotiation, retention\n"
  printf "  Investor Relations Pitch decks, quarterly updates, fund ops\n"
  printf "  Development        Proformas, entitlements, construction mgmt\n"
  printf "  Disposition        Strategy, prep, PSA review\n"
  printf "  Market Research    Submarket analysis, supply/demand, comps\n"
  printf "  Tax & Compliance   1031, cost seg, opportunity zones, carbon\n"
  printf "  Operations         Work orders, vendors, insurance, property admin\n"
  echo ""
  printf "  Plugin location: ${DIM}%s${RESET}\n" "$INSTALL_DIR"
  echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  print_banner
  detect_platform
  check_git
  check_claude
  locate_repo
  validate_plugin

  if install_plugin; then
    verify_installation
  fi

  print_success
}

main "$@"
