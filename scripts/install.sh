#!/usr/bin/env bash
# install.sh -- Single-command installer for the CRE Skills Plugin v4.0.0
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
   Plugin v4.0.0 -- 112 skills, 54 agents, 6 workflows

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
  if [ -f "src/plugin/plugin.json" ]; then
    INSTALL_DIR="$(pwd)"
    info "Running from inside the repo: $INSTALL_DIR"
    return
  fi

  # Check one level up (in case cwd is scripts/)
  if [ -f "../src/plugin/plugin.json" ]; then
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

  [ -f "$INSTALL_DIR/src/plugin/plugin.json" ] || { warn "Missing src/plugin/plugin.json"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/src/skills" ]              || { warn "Missing src/skills/ directory"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/src/agents" ]              || { warn "Missing src/agents/ directory"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/src/routing" ]             || { warn "Missing src/routing/ directory"; errors=$((errors + 1)); }
  [ -d "$INSTALL_DIR/src/commands" ]            || { warn "Missing src/commands/ directory"; errors=$((errors + 1)); }
  [ -f "$INSTALL_DIR/src/hooks/hooks.json" ]    || { warn "Missing src/hooks/hooks.json"; errors=$((errors + 1)); }

  if [ "$errors" -gt 0 ]; then
    fail "Plugin structure validation failed ($errors errors). The repo may be incomplete."
  fi

  local skill_count
  skill_count="$(find "$INSTALL_DIR/src/skills" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"
  local agent_count
  agent_count="$(find "$INSTALL_DIR/src/agents" -maxdepth 1 -name '*.md' ! -name '_*' | wc -l | tr -d ' ')"

  success "Plugin structure valid: $skill_count skills, $agent_count agents"
}

# ---------------------------------------------------------------------------
# Install the plugin
# ---------------------------------------------------------------------------
install_plugin() {
  info "Registering plugin..."

  local claude_home="$HOME/.claude"
  local plugin_version
  plugin_version="$(python3 -c "import json; print(json.load(open('$INSTALL_DIR/src/plugin/plugin.json'))['version'])" 2>/dev/null || echo "4.1.2")"
  local plugins_cache="$claude_home/plugins/cache/local/cre-skills-plugin/$plugin_version"
  local installed_file="$claude_home/plugins/installed_plugins.json"
  local settings_file="$claude_home/settings.json"
  local plugin_key="cre-skills@local"
  local now
  now="$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"

  # 1. Copy plugin to the plugins cache (two-step: src/ contents first, then top-level items)
  mkdir -p "$plugins_cache"
  rsync -a --delete \
    --exclude '.git' --exclude '__pycache__' --exclude 'node_modules' \
    "$INSTALL_DIR/src/" "$plugins_cache/"
  rsync -a \
    --exclude '.git' --exclude '__pycache__' --exclude 'node_modules' \
    --exclude 'dist' --exclude '.venv' --exclude '.local' \
    --exclude 'src' --exclude 'builds' --exclude 'tools' \
    --exclude 'config' --exclude 'docs/plans' --exclude 'docs/specs' \
    --exclude 'docs/design' --exclude 'tests/golden' \
    --exclude 'tests/snapshots' --exclude 'tests/fixtures' \
    "$INSTALL_DIR/" "$plugins_cache/"
  # Create .claude-plugin/ layout expected by Claude Code
  mkdir -p "$plugins_cache/.claude-plugin"
  cp "$plugins_cache/plugin/plugin.json" "$plugins_cache/.claude-plugin/plugin.json" 2>/dev/null || true
  success "Plugin files copied to $plugins_cache"

  # 2. Register in installed_plugins.json
  if [ -f "$installed_file" ]; then
    # Add or update the local plugin entry
    python3 -c "
import json, sys
with open('$installed_file') as f:
    data = json.load(f)
data.setdefault('plugins', {})['$plugin_key'] = [{
    'scope': 'user',
    'installPath': '$plugins_cache',
    'version': '$plugin_version',
    'installedAt': '$now',
    'lastUpdated': '$now'
}]
with open('$installed_file', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && success "Registered in installed_plugins.json" || warn "Could not update installed_plugins.json"
  else
    mkdir -p "$(dirname "$installed_file")"
    printf '{"version":2,"plugins":{"%s":[{"scope":"user","installPath":"%s","version":"%s","installedAt":"%s","lastUpdated":"%s"}]}}' \
      "$plugin_key" "$plugins_cache" "$plugin_version" "$now" "$now" > "$installed_file"
    success "Created installed_plugins.json"
  fi

  # 3. Enable in settings.json
  if [ -f "$settings_file" ]; then
    python3 -c "
import json
with open('$settings_file') as f:
    data = json.load(f)
data.setdefault('enabledPlugins', {})['$plugin_key'] = True
with open('$settings_file', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && success "Enabled in settings.json" || warn "Could not update settings.json"
  else
    printf '{"enabledPlugins":{"%s":true}}' "$plugin_key" > "$settings_file"
    success "Created settings.json"
  fi

  # 4. Register MCP server for Claude Desktop
  #    Per Anthropic docs: Claude Desktop reads ONLY from
  #    ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
  local desktop_config="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
  if [ ! -d "$(dirname "$desktop_config")" ]; then
    # Try Linux path
    desktop_config="$HOME/.config/Claude/claude_desktop_config.json"
  fi

  if [ -d "$(dirname "$desktop_config")" ] || [ -f "$desktop_config" ]; then
    python3 -c "
import json, os
config_path = '$desktop_config'
os.makedirs(os.path.dirname(config_path), exist_ok=True)
if os.path.exists(config_path):
    with open(config_path) as f:
        data = json.load(f)
else:
    data = {}
data.setdefault('mcpServers', {})['cre-skills'] = {
    'command': 'node',
    'args': ['$plugins_cache/mcp-server.mjs']
}
with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && success "MCP server registered for Claude Desktop" || warn "Could not register MCP server (non-fatal)"
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
    # Check if registered in settings.json directly
    if [ -f "$HOME/.claude/settings.json" ] && grep -q "cre-skills" "$HOME/.claude/settings.json" 2>/dev/null; then
      success "Plugin registered in settings.json (restart Claude to activate)"
    else
      warn "Could not verify plugin registration."
      info "Try: claude --plugin-dir $INSTALL_DIR"
    fi
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
       CRE Skills Plugin v4.0.0 -- Installed
  ============================================
SUCCESS
  printf "${RESET}"
  echo ""
  printf "  ${BOLD}Quick Start${RESET}\n"
  echo ""
  printf "  ${CYAN}/cre-skills:cre-route${RESET}       Find the right skill for any CRE task\n"
  printf "  ${CYAN}/cre-skills:cre-workflows${RESET}   Browse 6 end-to-end workflow chains\n"
  printf "  ${CYAN}/cre-skills:cre-agents${RESET}      List 54 expert subagents\n"
  echo ""
  printf "  ${BOLD}Example Commands${RESET}\n"
  echo ""
  printf "  ${DIM}/cre-skills:cre-route quick screen this deal${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route size a loan for a \$15M multifamily${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route generate an IC memo${RESET}\n"
  printf "  ${DIM}/cre-skills:cre-route normalize this T-12${RESET}\n"
  echo ""
  printf "  ${BOLD}Skill Categories (112 skills)${RESET}\n"
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
