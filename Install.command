#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# CRE Skills Plugin installer (double-click from Finder or run in DMG)
#
# For non-technical users: the .app bundle calls this automatically.
# For developers: just run this file directly.
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

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

# ── Navigate to repo root ────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Verify we're in the right place
if [ ! -d "skills" ] || [ ! -d "agents" ]; then
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

            ┌──┐                        ┌─────┐   ┌──┐
            │  │  ┌──┐    ┌───┐  ┌──┐   │     │   │  │     ┌─┐
       ┌──┐ │  │  │  │ ┌┐ │   │  │  │┌──┤     │┌──┤  │  ┌┐ │ │  ┌──┐
       │  │ │  │┌─┤  │ ││ │   │┌─┤  ││  │     ││  │  │┌─┤│ │ │┌─┤  │
    ┌──┤  │ │  ││ │  ├─┤│ │   ││ │  ││  │     ││  │  ││ ││ │ ││ │  │
  ──┤  │  ├─┤  ││ │  │ ││ │   ││ │  ││  │     ││  │  ││ ││ │ ││ │  ├──
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

HEADER
printf "${RESET}"

printf "${BLUE}  Plugin Installer v1.0.0${RESET}\n"
printf "${DIM}  80 skills | 40 agents | 6 workflow chains${RESET}\n"
echo ""

# ── Step 1: Check prerequisites ──────────────────────────────────────

bold "  Checking prerequisites..."
echo ""

HAS_CLAUDE_CODE=false
HAS_CLAUDE_DESKTOP=false

# Check for Claude Code CLI
if command -v claude &>/dev/null; then
    HAS_CLAUDE_CODE=true
    green "  Claude Code CLI found: $(claude --version 2>/dev/null || echo 'installed')"
else
    yellow "  Claude Code CLI not found (optional)"
fi

# Check for Claude Desktop
CLAUDE_DESKTOP_APP="/Applications/Claude.app"
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
if [ -d "$CLAUDE_DESKTOP_APP" ] || [ -d "$CLAUDE_CONFIG_DIR" ]; then
    HAS_CLAUDE_DESKTOP=true
    green "  Claude Desktop found"
else
    yellow "  Claude Desktop not found (optional)"
fi

# At least one must exist
if [ "$HAS_CLAUDE_CODE" = false ] && [ "$HAS_CLAUDE_DESKTOP" = false ]; then
    echo ""
    red "  Neither Claude Code nor Claude Desktop was found."
    echo ""
    echo "  Install one of these first:"
    printf "    ${CYAN}Claude Code:${RESET}    npm install -g @anthropic-ai/claude-code\n"
    printf "    ${CYAN}Claude Desktop:${RESET} https://claude.ai/download\n"
    echo ""
    press_to_exit 1
fi

echo ""

# ── Step 2: Install the plugin ────────────────────────────────────────

INSTALL_DIR="$SCRIPT_DIR"
bold "  Installing CRE Skills Plugin..."
printf "  ${DIM}Location: %s${RESET}\n" "$INSTALL_DIR"
echo ""

INSTALLED_SOMEWHERE=false

# Install to Claude Code if available
if [ "$HAS_CLAUDE_CODE" = true ]; then
    printf "  ${BLUE}Installing to Claude Code...${RESET}\n"
    if claude plugin add "$INSTALL_DIR" 2>/dev/null; then
        green "  Claude Code plugin registered"
        INSTALLED_SOMEWHERE=true
    else
        yellow "  Claude Code 'plugin add' not available in this version."
        printf "  ${DIM}Use: claude --plugin-dir %s${RESET}\n" "$INSTALL_DIR"
        INSTALLED_SOMEWHERE=true
    fi
    echo ""
fi

# Install to Claude Desktop if available
if [ "$HAS_CLAUDE_DESKTOP" = true ]; then
    printf "  ${BLUE}Configuring Claude Desktop...${RESET}\n"

    CLAUDE_SKILLS_DIR="$HOME/Library/Application Support/Claude/skills/cre-skills-plugin"

    mkdir -p "$CLAUDE_SKILLS_DIR"
    rsync -rlpt --delete \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='.DS_Store' \
        --exclude='node_modules' \
        --exclude='dist' \
        "$INSTALL_DIR/" "$CLAUDE_SKILLS_DIR/" 2>/dev/null && {
        green "  Skills copied to Claude Desktop"
        INSTALLED_SOMEWHERE=true
    } || {
        yellow "  Could not copy skills to Claude Desktop directory."
        dim "  You can manually copy the plugin folder to Claude Desktop's skills location."
    }
    echo ""
fi

if [ "$INSTALLED_SOMEWHERE" = false ]; then
    yellow "  Automatic registration did not succeed."
    printf "  ${DIM}Manual: claude --plugin-dir %s${RESET}\n" "$INSTALL_DIR"
fi

# ── Step 3: Success ───────────────────────────────────────────────────

echo ""
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
green "  CRE Skills Plugin installed successfully!"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

printf "  ${BOLD}Quick Start${RESET}\n"
echo ""
printf "  ${CYAN}/cre-skills:cre-route${RESET}        Route any CRE task to the right skill\n"
printf "  ${CYAN}/cre-skills:deal-quick-screen${RESET} Screen a deal in seconds\n"
printf "  ${CYAN}/cre-skills:cre-workflows${RESET}    Browse 6 end-to-end workflow chains\n"
printf "  ${CYAN}/cre-skills:cre-agents${RESET}       List 40 expert agents\n"
echo ""

printf "  ${BOLD}Example${RESET}\n"
echo ""
printf "  ${DIM}> /cre-skills:deal-quick-screen${RESET}\n"
printf "  ${DIM}  240-unit garden-style multifamily in Raleigh, NC.${RESET}\n"
printf "  ${DIM}  Asking \$42M. 2018 vintage. Occupancy 93%%.${RESET}\n"
printf "  ${DIM}  In-place NOI \$2.6M. Rents 12%% below market.${RESET}\n"
echo ""

printf "  ${BOLD}What's Included${RESET}\n"
echo ""
printf "  ${GREEN}80${RESET} skills across 16 categories\n"
printf "  ${GREEN}40${RESET} expert agents (Pension Fund, PE, REIT, Risk Mgr, ...)\n"
printf "  ${GREEN} 6${RESET} workflow chains (Acquisition, Capital Stack, Hold, ...)\n"
echo ""
printf "  Plugin location: ${DIM}%s${RESET}\n" "$INSTALL_DIR"
echo ""

press_to_exit 0
