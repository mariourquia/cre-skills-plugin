#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# CRE Skills Plugin installer (double-click from Finder or run in DMG)
#
# 1. Copies plugin to ~/.claude/plugins/cache/local/cre-skills-plugin/
# 2. Registers in installed_plugins.json + settings.json
# 3. Registers MCP server in Claude Desktop config
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Error trap: generate diagnostic report on failure ────────────────
cleanup_on_error() {
    local exit_code=$?
    if [ "$exit_code" -ne 0 ]; then
        echo ""
        printf '\033[1;31m  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n'
        printf '\033[1;31m  INSTALLATION ERROR (exit code %s)\033[0m\n' "$exit_code"
        printf '\033[1;31m  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n'
        echo ""
        send_telemetry "unhandled_exit" "Install.command exited with code $exit_code"
        dim "  An anonymous error report was sent to help improve the installer."
        echo ""
        echo "  Submit a bug report:"
        echo "  https://github.com/mariourquia/cre-skills-plugin/issues/new?labels=bug,installer"
        echo ""
        printf '\033[1mPress Enter to close this window.\033[0m\n'
        read -r
    fi
}
trap cleanup_on_error EXIT

clear

# ── Colors ────────────────────────────────────────────────────────────

GREEN='\033[1;32m'
BLUE='\033[1;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

bold()   { printf "${BOLD}%s${RESET}\n" "$*"; }
green()  { printf "${GREEN}%s${RESET}\n" "$*"; }
blue()   { printf "${BLUE}%s${RESET}\n" "$*"; }
yellow() { printf "${YELLOW}%s${RESET}\n" "$*"; }
red()    { printf "${RED}%s${RESET}\n" "$*"; }
dim()    { printf "${DIM}%s${RESET}\n" "$*"; }

press_to_exit() {
    echo ""
    bold "Press Enter to close this window."
    read -r
    exit "${1:-0}"
}

# ── Telemetry (curl-based, no Python/Node dependency) ──────────────

TELEMETRY_URL="https://cre-skills-feedback-api.vercel.app/api/installer-telemetry"
PLUGIN_NAME_CONST="cre-skills-plugin"
INSTALLER_VERSION_CONST="4.2.0"

send_telemetry() {
    local step_failed="$1"
    local error_msg="$2"
    local prereqs_json="${3:-{}}"

    {
        local install_id_file="$HOME/.cre-skills/install-id"
        local install_uuid
        if [ -f "$install_id_file" ]; then
            install_uuid="$(cat "$install_id_file")"
        else
            mkdir -p "$HOME/.cre-skills"
            install_uuid="$(python3 -c 'import uuid; print(uuid.uuid4())' 2>/dev/null || cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "unknown-$(date +%s)")"
            echo "$install_uuid" > "$install_id_file"
        fi
        local install_hash="$install_uuid"
        local event_seed
        event_seed="$step_failed-$error_msg-$(date +%s)"
        local event_id
        event_id="it_$(printf '%s' "$event_seed" | shasum -a 256 | cut -d' ' -f1 | head -c 16)"

        # Truncate error message
        if [ ${#error_msg} -gt 2000 ]; then
            error_msg="${error_msg:0:2000}"
        fi

        # Compute duration since install start (0 if not yet set)
        local duration=0
        if [ -n "${INSTALL_START:-}" ]; then
            duration=$(( $(date +%s) - INSTALL_START ))
        fi

        # Build status field
        local status="failure"
        if [ -z "$step_failed" ] && [ -z "$error_msg" ]; then
            status="success"
        fi

        curl -s -X POST "$TELEMETRY_URL" \
            -H "Content-Type: application/json" \
            -d "$(printf '{"id":"%s","plugin_name":"%s","plugin_version":"%s","installer_type":"command","os":"macos","os_version":"%s","arch":"%s","status":"%s","step_failed":"%s","error_message":"%s","prereqs":%s,"install_id_hash":"%s","python_version":"%s","python_source":"%s","node_version":"%s","node_source":"%s","claude_code_present":%s,"claude_desktop_present":%s,"step_results":{%s},"edge_cases":"%s","remediations":"%s","total_duration_s":%d}' \
                "$event_id" "$PLUGIN_NAME_CONST" "$INSTALLER_VERSION_CONST" \
                "$(sw_vers -productVersion 2>/dev/null || uname -r)" \
                "$(uname -m)" \
                "$status" \
                "$step_failed" \
                "$error_msg" \
                "$prereqs_json" \
                "$install_hash" \
                "${PYTHON_VERSION:-not_found}" \
                "${PYTHON_SOURCE:-not_found}" \
                "${NODE_VERSION:-not_found}" \
                "${NODE_SOURCE:-not_found}" \
                "${HAS_CLAUDE_CODE:-false}" \
                "${HAS_CLAUDE_DESKTOP:-false}" \
                "${STEP_RESULTS:-}" \
                "${EDGE_CASES:-}" \
                "${REMEDIATIONS:-}" \
                "$duration")" \
            --connect-timeout 5 --max-time 10 2>/dev/null
    } &
}

# ── Navigate to repo root ────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "src/skills" ] || [ ! -d "src/agents" ]; then
    red "Could not find the CRE Skills Plugin files."
    echo "Make sure this file is in the cre-skills-plugin folder."
    press_to_exit 1
fi

# ── ASCII art header ──────────────────────────────────────────────────

printf "${CYAN}"
cat << 'HEADER'

 ██████╗██████╗ ███████╗    ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
██║     ██████╔╝█████╗      ███████╗█████╔╝ ██║██║     ██║     ███████╗
██║     ██╔══██╗██╔══╝      ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
╚██████╗██║  ██║███████╗    ███████║██║  ██╗██║███████╗███████╗███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

                                            ╔═╗
                                     ┌─┐    ║ ║  ┌─┐
                              ┌──┐   │ │    ║ ║  │ │
                     ┌───┐    │  │   │ │ ┌┐ ║ ║  │ │ ┌──┐
              ┌──┐   │   │ ┌┐ │  │┌──┤ │ ││ ║ ║  │ │ │  │   ┌─┐
         ┌──┐ │  │   │   │ ││ │  ││  │ │ ││ ║ ║┌─┤ │ │  │┌──┤ │
    ┌─┐  │  │ │  │┌──┤   │ ││ │  ││  │ │ ││ ║ ║│ │ │ │  ││  │ │  ┌─┐
    │ │  │  │ │  ││  │   │ ││ │  ││  │ │ ││ ║ ║│ │ │ │  ││  │ │  │ │
  ──┤ ├──┤  ├─┤  ││  │   ├─┤│ │  ││  │ ├─┤│ ║ ║│ │ ├─┤  ││  │ ├──┤ ├──
  ░░│B├░░│R├░│O├░│O├░│K├░│L├│Y│N│░░░░░░║M║A║N║H║A║T║T║A║N║░░░░░░░░░░░░
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ░░░░░░░░░░░░≈≈≈≈≈≈≈≈≈ EAST  RIVER ≈≈≈≈≈≈≈≈≈░░░░░░░░░░░░░░░░░░░░░░░░░░

HEADER
printf "${RESET}"

printf "${BLUE}  Plugin Installer v4.2.0${RESET}\n"
printf "${DIM}  113 skills | 54 agents | 8 MCP tools | 6 workflow chains${RESET}\n"
echo ""

# ── Timing and structured telemetry tracking ────────────────────────

INSTALL_START=$(date +%s)
STEP_RESULTS=""
EDGE_CASES=""
REMEDIATIONS=""

add_step_result() { STEP_RESULTS="${STEP_RESULTS:+$STEP_RESULTS,}\"$1\":\"$2\""; }
add_edge_case()   { EDGE_CASES="${EDGE_CASES:+$EDGE_CASES,}$1"; }
add_remediation()  { REMEDIATIONS="${REMEDIATIONS:+$REMEDIATIONS,}$1"; }

detect_python_source() {
    local py_path
    py_path="$(command -v python3 2>/dev/null || true)"
    if [ -z "$py_path" ]; then
        echo "not_found"
    elif echo "$py_path" | grep -q "Cellar\|Homebrew"; then
        echo "brew"
    elif echo "$py_path" | grep -q "CommandLineTools\|Xcode"; then
        echo "xcode-clt"
    else
        echo "system"
    fi
}

detect_node_source() {
    local node_path
    node_path="$(command -v node 2>/dev/null || true)"
    if [ -z "$node_path" ]; then
        echo "not_found"
    elif echo "$node_path" | grep -q "Cellar\|Homebrew"; then
        echo "brew"
    elif echo "$node_path" | grep -q ".nvm"; then
        echo "nvm"
    else
        echo "system"
    fi
}

# ── Step counter ─────────────────────────────────────────────────────

STEP=0
TOTAL_STEPS=7
step() {
    STEP=$((STEP + 1))
    bold "  [$STEP/$TOTAL_STEPS] $1"
}

# ── Edge case detection ─────────────────────────────────────────────

if echo "$HOME" | grep -q ' '; then
    add_edge_case "spaces_in_home"
    yellow "  Warning: Home path contains spaces. This may cause issues."
fi
if echo "$HOME" | LC_ALL=C grep -q '[^[:print:]]'; then
    add_edge_case "non_ascii_username"
fi

# ── Step 1: Check prerequisites ──────────────────────────────────────

step "Checking prerequisites..."
echo ""

HAS_CLAUDE_CODE=false
HAS_CLAUDE_DESKTOP=false

if command -v claude &>/dev/null; then
    HAS_CLAUDE_CODE=true
    green "  Claude Code CLI found: $(claude --version 2>/dev/null || echo 'installed')"
else
    yellow "  Claude Code CLI not found (optional)"
fi

CLAUDE_DESKTOP_APP="/Applications/Claude.app"
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
if [ -d "$CLAUDE_DESKTOP_APP" ] || [ -d "$CLAUDE_CONFIG_DIR" ]; then
    HAS_CLAUDE_DESKTOP=true
    green "  Claude Desktop found"
else
    yellow "  Claude Desktop not found (optional)"
fi

# Check Node.js (required for MCP server)
if command -v node &>/dev/null; then
    green "  Node.js found: $(node --version 2>/dev/null)"
else
    yellow "  Node.js not found. Attempting to install..."

    if command -v brew &>/dev/null; then
        dim "  Installing via Homebrew..."
        brew install node 2>&1 | while read -r line; do
            printf "\r\033[2m  %s\033[0m\033[K" "$line"
        done
        printf "\r\033[K"

        if command -v node &>/dev/null; then
            green "  Node.js installed: $(node --version)"
            add_remediation "node_brew_install"
        else
            red "  Node.js installation failed."
            echo "  Install manually: https://nodejs.org/"
            send_telemetry "node_install" "brew install node failed" '{"node":"missing","brew":"failed"}'
            press_to_exit 1
        fi
    else
        red "  Node.js is required but not found."
        echo ""
        echo "  Install one of:"
        dim "    brew install node"
        dim "    https://nodejs.org/en/download"
        echo ""
        send_telemetry "node_install" "Node.js missing, no brew available" '{"node":"missing","brew":"not_installed"}'
        press_to_exit 1
    fi
fi

# Detect python version and source
PYTHON_VERSION="not_found"
PYTHON_SOURCE="not_found"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION="$(python3 --version 2>/dev/null | awk '{print $2}' || echo "unknown")"
    PYTHON_SOURCE="$(detect_python_source)"
else
    yellow "  python3 not found. Some features may be limited."
    yellow "  Install with: xcode-select --install"
fi

# Detect node version and source
NODE_VERSION="$(node --version 2>/dev/null || echo "not_found")"
NODE_SOURCE="$(detect_node_source)"

if [ "$HAS_CLAUDE_CODE" = false ] && [ "$HAS_CLAUDE_DESKTOP" = false ]; then
    echo ""
    red "  Neither Claude Code nor Claude Desktop was found."
    echo ""
    echo "  Install one of these first:"
    printf "    ${CYAN}Claude Code:${RESET}    https://claude.ai/download\n"
    printf "    ${CYAN}Claude Desktop:${RESET} https://claude.ai/download\n"
    echo ""
    send_telemetry "no_claude" "Neither Claude Code nor Claude Desktop found"
    press_to_exit 1
fi

add_step_result "prereqs" "ok"
echo ""

# ── Step 2: Register plugin ──────────────────────────────────────────

INSTALL_DIR="$SCRIPT_DIR"
PLUGIN_VERSION="$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "4.2.0")"
CLAUDE_HOME="$HOME/.claude"
PLUGINS_CACHE="$CLAUDE_HOME/plugins/cache/local/cre-skills-plugin/$PLUGIN_VERSION"
INSTALLED_PLUGINS="$CLAUDE_HOME/plugins/installed_plugins.json"
SETTINGS_FILE="$CLAUDE_HOME/settings.json"
PLUGIN_KEY="cre-skills@local"
NOW="$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"

# Edge case: spaces in install path or read-only filesystem
if echo "$INSTALL_DIR" | grep -q ' '; then
    add_edge_case "spaces_in_path"
    yellow "  Warning: Install path contains spaces. This may cause issues."
fi
if ! touch "$INSTALL_DIR/.write_test" 2>/dev/null; then
    add_edge_case "read_only_filesystem"
    red "  Error: Cannot write to install directory."
    send_telemetry "read_only_fs" "Install directory is read-only"
    press_to_exit 1
else
    rm -f "$INSTALL_DIR/.write_test"
fi

step "Copying plugin files..."
printf "  ${DIM}Source: %s${RESET}\n" "$INSTALL_DIR"
echo ""

# 1. Copy to plugin cache (two-step: src/ contents first, then top-level items)
mkdir -p "$PLUGINS_CACHE"
rsync -a --delete \
    --exclude '.git' --exclude '__pycache__' --exclude 'node_modules' \
    "$INSTALL_DIR/src/" "$PLUGINS_CACHE/"
rsync -a \
    --exclude '.git' --exclude '__pycache__' --exclude 'node_modules' \
    --exclude 'dist' --exclude '.venv' --exclude '.local' \
    --exclude 'src' --exclude 'builds' --exclude 'tools' \
    --exclude 'config' --exclude 'docs/plans' --exclude 'docs/specs' \
    --exclude 'docs/design' --exclude 'tests/golden' \
    --exclude 'tests/snapshots' --exclude 'tests/fixtures' \
    "$INSTALL_DIR/" "$PLUGINS_CACHE/"

# rsync's second pass already copied $INSTALL_DIR/.claude-plugin/plugin.json into
# the cache root. Defensively ensure the dir exists and recover from $INSTALL_DIR
# if a custom rsync filter dropped the dotdir.
mkdir -p "$PLUGINS_CACHE/.claude-plugin"
if [ ! -f "$PLUGINS_CACHE/.claude-plugin/plugin.json" ] && [ -f "$INSTALL_DIR/.claude-plugin/plugin.json" ]; then
    cp "$INSTALL_DIR/.claude-plugin/plugin.json" "$PLUGINS_CACHE/.claude-plugin/plugin.json"
fi
green "  Plugin files copied to cache"
add_step_result "copy_files" "ok"

step "Building catalog..."
if [ ! -f "$PLUGINS_CACHE/dist/catalog.json" ] && command -v python3 &>/dev/null; then
    if (cd "$PLUGINS_CACHE" && python3 scripts/catalog-build.py 2>/dev/null); then
        green "  Catalog built"
        add_step_result "catalog" "ok"
    else
        add_step_result "catalog" "skipped"
    fi
else
    add_step_result "catalog" "skipped"
fi

step "Registering plugin..."

# 2. Register in installed_plugins.json
if [ -f "$INSTALLED_PLUGINS" ]; then
    python3 -c "
import json
with open('$INSTALLED_PLUGINS') as f:
    data = json.load(f)
data.setdefault('plugins', {})['$PLUGIN_KEY'] = [{
    'scope': 'user',
    'installPath': '$PLUGINS_CACHE',
    'version': '$PLUGIN_VERSION',
    'installedAt': '$NOW',
    'lastUpdated': '$NOW'
}]
with open('$INSTALLED_PLUGINS', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && green "  Registered in installed_plugins.json" || yellow "  Could not update installed_plugins.json"
else
    mkdir -p "$(dirname "$INSTALLED_PLUGINS")"
    printf '{"version":2,"plugins":{"%s":[{"scope":"user","installPath":"%s","version":"%s","installedAt":"%s","lastUpdated":"%s"}]}}' \
        "$PLUGIN_KEY" "$PLUGINS_CACHE" "$PLUGIN_VERSION" "$NOW" "$NOW" > "$INSTALLED_PLUGINS"
    green "  Created installed_plugins.json"
fi

# 3. Enable in settings.json
if [ -f "$SETTINGS_FILE" ]; then
    python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
data.setdefault('enabledPlugins', {})['$PLUGIN_KEY'] = True
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && green "  Enabled in settings.json" || yellow "  Could not update settings.json"
else
    printf '{"enabledPlugins":{"%s":true}}' "$PLUGIN_KEY" > "$SETTINGS_FILE"
    green "  Created settings.json"
fi
add_step_result "register" "ok"

step "Configuring MCP server..."

# 4. Register MCP server for Claude Desktop
DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ ! -d "$(dirname "$DESKTOP_CONFIG")" ]; then
    DESKTOP_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
fi

if [ -d "$(dirname "$DESKTOP_CONFIG")" ] || [ "$HAS_CLAUDE_DESKTOP" = true ]; then
    python3 -c "
import json, os
config_path = '''$DESKTOP_CONFIG'''
os.makedirs(os.path.dirname(config_path), exist_ok=True)
if os.path.exists(config_path):
    with open(config_path) as f:
        data = json.load(f)
else:
    data = {}
data.setdefault('mcpServers', {})['cre-skills'] = {
    'command': 'node',
    'args': ['$PLUGINS_CACHE/mcp-server.mjs']
}
with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && { green "  MCP server registered for Claude Desktop"; add_step_result "mcp_config" "ok"; } || {
    yellow "  Could not register MCP server (non-fatal)"
    add_step_result "mcp_config" "fail"
    send_telemetry "mcp_config" "Python MCP config write failed"
}
fi

echo ""

# ── Post-install verification ────────────────────────────────────────

step "Verifying installation..."

SKILL_COUNT="$(find "$PLUGINS_CACHE/skills" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
AGENT_COUNT="$(find "$PLUGINS_CACHE/agents" -maxdepth 1 -name '*.md' ! -name '_*' 2>/dev/null | wc -l | tr -d ' ')"
MCP_OK="false"
[ -f "$PLUGINS_CACHE/mcp-server.mjs" ] && MCP_OK="true"

VERIFY_FAILS=0
green "  Verification:"
echo "    Skills: $SKILL_COUNT (expected 113)"
echo "    Agents: $AGENT_COUNT (expected 54)"
echo "    MCP server: $MCP_OK"

# Verify registration files
if [ -f "$INSTALLED_PLUGINS" ]; then
    if python3 -c "import json; d=json.load(open('$INSTALLED_PLUGINS')); assert 'cre-skills@local' in d.get('plugins',{})" 2>/dev/null; then
        echo "    installed_plugins.json: OK"
    else
        echo "    installed_plugins.json: entry missing"
        VERIFY_FAILS=$((VERIFY_FAILS + 1))
    fi
fi
if [ -f "$SETTINGS_FILE" ]; then
    if python3 -c "import json; d=json.load(open('$SETTINGS_FILE')); assert d.get('enabledPlugins',{}).get('cre-skills@local')" 2>/dev/null; then
        echo "    settings.json: plugin enabled"
    else
        echo "    settings.json: plugin not enabled"
        VERIFY_FAILS=$((VERIFY_FAILS + 1))
    fi
fi

if [ "$VERIFY_FAILS" -gt 0 ]; then
    yellow "  $VERIFY_FAILS verification check(s) failed"
    add_step_result "verify" "fail"
else
    add_step_result "verify" "ok"
fi
echo ""

# ── Done ─────────────────────────────────────────────────────────────

step "Done!"

echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
green "  CRE Skills Plugin v$PLUGIN_VERSION installed!"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

printf "  ${BOLD}Quick Start${RESET}\n"
echo ""
printf "  ${CYAN}/cre-skills:cre-route${RESET}         Route any CRE task to the right skill\n"
printf "  ${CYAN}/cre-skills:deal-intake${RESET}       Start a deal workspace\n"
printf "  ${CYAN}/cre-skills:navigator${RESET}         Browse all 113 skills\n"
printf "  ${CYAN}/cre-skills:cre-agents${RESET}        List 54 expert agents\n"
echo ""

printf "  ${BOLD}Where It Works${RESET}\n"
echo ""
printf "  ${GREEN}Claude Code${RESET}     113 skills + 54 agents + hooks\n"
printf "  ${GREEN}Claude Desktop${RESET}  8 MCP tools (route, list, workspace, feedback)\n"
echo ""

printf "  ${BOLD}Restart Claude Desktop${RESET} to see the MCP server.\n"
echo ""
printf "  Plugin location: ${DIM}%s${RESET}\n" "$PLUGINS_CACHE"
echo ""

# ── Success telemetry ────────────────────────────────────────────────

send_telemetry "" ""

press_to_exit 0
