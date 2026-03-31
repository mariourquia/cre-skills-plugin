#!/usr/bin/env bash
# install.sh -- Single-command installer for the CRE Skills Plugin v2.5.0
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
   Plugin v2.5.0 -- 105 skills, 55 agents, 6 workflows

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
    Darwin)     PLATFORM="macos" ;;
    Linux)      PLATFORM="linux" ;;
    CYGWIN*|MINGW*|MSYS*)
      PLATFORM="windows-wsl"
      warn "Windows/WSL detected. Some features require WSL2 with Node.js installed natively."
      ;;
    *)          fail "Unsupported platform: $os. This installer supports macOS, Linux, and Windows WSL." ;;
  esac
  info "Detected platform: $PLATFORM ($(uname -m))"
}

# ---------------------------------------------------------------------------
# Home directory -- portable across macOS/Linux/WSL
# ---------------------------------------------------------------------------
resolve_home() {
  # $HOME is set by every POSIX shell; $USERPROFILE is Windows-only.
  # In WSL, $HOME is the Linux home, which is correct.
  if [ -z "${HOME:-}" ]; then
    HOME="$(cd ~ && pwd)"
  fi
  export HOME
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

check_node() {
  if command -v node &>/dev/null; then
    local node_ver
    node_ver="$(node --version 2>/dev/null | tr -d 'v')"
    local node_major
    node_major="$(printf '%s' "$node_ver" | cut -d. -f1)"
    if [ "${node_major:-0}" -ge 18 ]; then
      success "Node.js found: v$node_ver"
    else
      warn "Node.js v$node_ver found but v18+ is required for hooks. The plugin will work but hook scripts may fail."
    fi
  else
    warn "Node.js not found. Hooks (telemetry, session summary) require Node.js 18+."
    warn "Install from https://nodejs.org/"
  fi
}

check_python() {
  local found=""
  for candidate in python3.14 python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" &>/dev/null; then
      local ver
      ver=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
      local major minor
      major="$(printf '%s' "$ver" | cut -d. -f1)"
      minor="$(printf '%s' "$ver" | cut -d. -f2)"
      if [ "${major:-0}" -ge 3 ] && [ "${minor:-0}" -ge 10 ]; then
        found="$candidate"
        break
      fi
    fi
  done
  if [ -n "$found" ]; then
    success "Python found: $("$found" --version)"
  else
    warn "Python 3.10+ not found. Calculator scripts will not be executable."
    warn "Install from https://www.python.org/downloads/"
  fi
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
# v1 -> v2 migration
# ---------------------------------------------------------------------------
DATA_DIR="$HOME/.cre-skills"

handle_v1_migration() {
  # Check for any existing data that needs preserving
  if [ ! -d "$DATA_DIR" ]; then
    return 0
  fi

  info "Existing ~/.cre-skills/ directory found. Checking for v1 data..."

  # Check plugin.json version to detect v1 install
  local installed_version=""
  if [ -f "$DATA_DIR/config.json" ]; then
    installed_version="$(python3 -c "import json; d=json.load(open('$DATA_DIR/config.json')); print(d.get('version','unknown'))" 2>/dev/null || echo "unknown")"
  fi

  if [ "$installed_version" = "unknown" ] || [[ "$installed_version" == 1.* ]]; then
    echo ""
    printf "${YELLOW}  v1 -> v2 migration detected.${RESET}\n"
    printf "${YELLOW}  v2.0.0 changes:${RESET}\n"
    printf "    - License changed from MIT to Apache 2.0\n"
    printf "    - 11 new skills added (total: 91)\n"
    printf "    - New telemetry hooks (PostToolUse, Stop)\n"
    printf "    - Python calculator scripts\n"
    echo ""
    printf "${BOLD}  License change notice:${RESET}\n"
    printf "  This plugin is now licensed under the Apache License 2.0.\n"
    printf "  See LICENSE and NOTICE files in the plugin directory for details.\n"
    echo ""
  fi

  # Backup user-customized files before any overwrite
  backup_user_data
}

backup_user_data() {
  local backup_dir="$DATA_DIR/backup-$(date +%Y%m%d-%H%M%S)"
  local backed_up=0

  # Files that contain user customization
  for f in config.json brand-guidelines.json; do
    if [ -f "$DATA_DIR/$f" ]; then
      mkdir -p "$backup_dir"
      cp "$DATA_DIR/$f" "$backup_dir/$f"
      backed_up=$((backed_up + 1))
    fi
  done

  if [ "$backed_up" -gt 0 ]; then
    success "User config backed up to $backup_dir"
  fi
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

  # Not inside the repo -- clone or update it
  local default_dir="$HOME/.claude/plugins/cre-skills-plugin"
  info "Cloning repo to $default_dir ..."

  if [ -d "$default_dir" ]; then
    warn "Directory already exists: $default_dir"
    info "Pulling latest changes..."
    if git -C "$default_dir" pull --ff-only 2>/dev/null; then
      success "Updated to latest"
    else
      warn "Pull failed (local changes?). Using existing copy."
    fi
  else
    mkdir -p "$(dirname "$default_dir")"
    git clone "$REPO_URL" "$default_dir"
  fi

  INSTALL_DIR="$default_dir"
  success "Repo ready at $INSTALL_DIR"
}

# ---------------------------------------------------------------------------
# Make calculators executable
# ---------------------------------------------------------------------------
make_calculators_executable() {
  local calc_dir="$INSTALL_DIR/scripts/calculators"
  if [ -d "$calc_dir" ]; then
    chmod +x "$calc_dir"/*.py 2>/dev/null || true
    local count
    count="$(ls "$calc_dir"/*.py 2>/dev/null | wc -l | tr -d ' ')"
    success "Made $count Python calculators executable"
  fi
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

  if claude plugin add "$INSTALL_DIR" 2>/dev/null; then
    success "Plugin installed successfully"
  else
    # Fall back to manual instructions if plugin subcommand not available
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
       CRE Skills Plugin v2.5.0 -- Installed
  ============================================
SUCCESS
  printf "${RESET}"
  echo ""
  printf "  ${BOLD}Quick Start${RESET}\n"
  echo ""
  printf "  ${CYAN}/cre-skills:cre-route${RESET}       Find the right skill for any CRE task\n"
  printf "  ${CYAN}/cre-skills:cre-workflows${RESET}   Browse 6 end-to-end workflow chains\n"
  printf "  ${CYAN}/cre-skills:cre-agents${RESET}      List 55 expert subagents\n"
  echo ""
  printf "  ${BOLD}Example Commands${RESET}\n"
  echo ""
  printf "  ${DIM}/cre-skills:cre-route quick screen this deal${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route size a loan for a \$15M multifamily${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route generate an IC memo${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route normalize this T-12${RESET}\n"
  echo ""
  printf "  ${BOLD}Skill Categories (105 skills)${RESET}\n"
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
  printf "  Run ${CYAN}scripts/verify-install.sh${RESET} to confirm everything is healthy.\n"
  echo ""
  printf "  Plugin location: ${DIM}%s${RESET}\n" "$INSTALL_DIR"
  echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  print_banner
  resolve_home
  detect_platform
  check_git
  check_node
  check_python
  check_claude
  handle_v1_migration
  locate_repo
  validate_plugin
  make_calculators_executable

  if install_plugin; then
    verify_installation
  fi

  print_success
}

main "$@"
