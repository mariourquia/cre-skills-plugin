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
INSTALLER_VERSION_CONST="4.1.0"

send_telemetry() {
    local step_failed="$1"
    local error_msg="$2"
    local prereqs_json="${3:-{}}"

    {
        local id_source
        id_source="$(hostname)-$(whoami)"
        local install_hash
        install_hash=$(printf '%s' "$id_source" | shasum -a 256 | cut -d' ' -f1)
        local event_seed
        event_seed="$step_failed-$error_msg-$(date +%s)"
        local event_id
        event_id="it_$(printf '%s' "$event_seed" | shasum -a 256 | cut -d' ' -f1 | head -c 16)"

        # Truncate error message
        if [ ${#error_msg} -gt 2000 ]; then
            error_msg="${error_msg:0:2000}"
        fi

        curl -s -X POST "$TELEMETRY_URL" \
            -H "Content-Type: application/json" \
            -d "$(printf '{"id":"%s","plugin_name":"%s","plugin_version":"%s","installer_type":"command","os":"macos","os_version":"%s","arch":"%s","step_failed":"%s","error_message":"%s","prereqs":%s,"install_id_hash":"%s"}' \
                "$event_id" "$PLUGIN_NAME_CONST" "$INSTALLER_VERSION_CONST" \
                "$(sw_vers -productVersion 2>/dev/null || uname -r)" \
                "$(uname -m)" \
                "$step_failed" \
                "$error_msg" \
                "$prereqs_json" \
                "$install_hash")" \
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

printf "${BLUE}  Plugin Installer v4.0.0${RESET}\n"
printf "${DIM}  112 skills | 54 agents | 8 MCP tools | 6 workflow chains${RESET}\n"
echo ""

# ── Step 1: Check prerequisites ──────────────────────────────────────

bold "  Checking prerequisites..."
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

if ! command -v python3 &>/dev/null; then
    yellow "  python3 not found. Some features may be limited."
    yellow "  Install with: xcode-select --install"
fi

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

echo ""

# ── Step 2: Register plugin ──────────────────────────────────────────

INSTALL_DIR="$SCRIPT_DIR"
PLUGIN_VERSION="$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/src/plugin/plugin.json'))['version'])" 2>/dev/null || echo "4.0.0")"
CLAUDE_HOME="$HOME/.claude"
PLUGINS_CACHE="$CLAUDE_HOME/plugins/cache/local/cre-skills-plugin/$PLUGIN_VERSION"
INSTALLED_PLUGINS="$CLAUDE_HOME/plugins/installed_plugins.json"
SETTINGS_FILE="$CLAUDE_HOME/settings.json"
PLUGIN_KEY="cre-skills@local"
NOW="$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"

bold "  Installing CRE Skills Plugin..."
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
green "  Plugin files copied to cache"

# Build catalog if not present
if [ ! -f "$PLUGINS_CACHE/dist/catalog.json" ] && command -v python3 &>/dev/null; then
    (cd "$PLUGINS_CACHE" && python3 scripts/catalog-build.py 2>/dev/null) && \
        green "  Catalog built" || true
fi

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
" 2>/dev/null && green "  MCP server registered for Claude Desktop" || {
    yellow "  Could not register MCP server (non-fatal)"
    send_telemetry "mcp_config" "Python MCP config write failed"
}
fi

echo ""

# ── Step 3: Success ───────────────────────────────────────────────────

echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
green "  CRE Skills Plugin v4.0.0 installed!"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

printf "  ${BOLD}Quick Start${RESET}\n"
echo ""
printf "  ${CYAN}/cre-skills:cre-route${RESET}         Route any CRE task to the right skill\n"
printf "  ${CYAN}/cre-skills:deal-intake${RESET}       Start a deal workspace\n"
printf "  ${CYAN}/cre-skills:navigator${RESET}         Browse all 112 skills\n"
printf "  ${CYAN}/cre-skills:cre-agents${RESET}        List 54 expert agents\n"
echo ""

printf "  ${BOLD}Where It Works${RESET}\n"
echo ""
printf "  ${GREEN}Claude Code${RESET}     112 skills + 54 agents + hooks\n"
printf "  ${GREEN}Claude Desktop${RESET}  8 MCP tools (route, list, workspace, feedback)\n"
echo ""

printf "  ${BOLD}Restart Claude Desktop${RESET} to see the MCP server.\n"
echo ""
printf "  Plugin location: ${DIM}%s${RESET}\n" "$PLUGINS_CACHE"
echo ""

press_to_exit 0
