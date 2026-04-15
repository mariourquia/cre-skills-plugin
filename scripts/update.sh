#!/usr/bin/env bash
# update.sh -- Update the CRE Skills Plugin to the latest version
#
# Usage:
#   ./scripts/update.sh                   # from inside the plugin repo
#   bash /path/to/cre-skills-plugin/scripts/update.sh

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
SRC_DIR="$REPO_ROOT/src"

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
# Read current version from plugin.json
# ---------------------------------------------------------------------------
get_local_version() {
  python3 -c "
import json
with open('$REPO_ROOT/.claude-plugin/plugin.json') as f:
    d = json.load(f)
print(d.get('version', 'unknown'))
" 2>/dev/null || echo "unknown"
}

# ---------------------------------------------------------------------------
# Preserve user data
# ---------------------------------------------------------------------------
preserve_user_data() {
  if [ ! -d "$DATA_DIR" ]; then
    return 0
  fi

  info "Preserving user data in $DATA_DIR ..."

  local backup_dir="$DATA_DIR/backup-$(date +%Y%m%d-%H%M%S)"
  local backed_up=0

  for f in config.json brand-guidelines.json telemetry.jsonl feedback.jsonl; do
    if [ -f "$DATA_DIR/$f" ]; then
      mkdir -p "$backup_dir"
      cp "$DATA_DIR/$f" "$backup_dir/$f"
      backed_up=$((backed_up + 1))
    fi
  done

  if [ "$backed_up" -gt 0 ]; then
    success "User data backed up to $backup_dir"
  else
    info "No user data to preserve"
  fi
}

# ---------------------------------------------------------------------------
# Check for breaking changes (major version bump)
# ---------------------------------------------------------------------------
check_breaking_changes() {
  local current_version="$1"
  local remote_version="$2"

  local current_major remote_major
  current_major="$(printf '%s' "$current_version" | cut -d. -f1)"
  remote_major="$(printf '%s' "$remote_version" | cut -d. -f1)"

  if [ "${remote_major:-0}" -gt "${current_major:-0}" ]; then
    echo ""
    printf "${YELLOW}  Major version bump detected: v%s -> v%s${RESET}\n" "$current_version" "$remote_version"
    printf "${YELLOW}  This is a breaking change release. Review CHANGELOG.md for details.${RESET}\n"
    echo ""
    printf "  Breaking changes in v%s:\n" "$remote_major"

    # Print CHANGELOG section for the new major version if available
    if [ -f "$REPO_ROOT/CHANGELOG.md" ]; then
      # Extract the first entry from CHANGELOG (most recent)
      python3 -c "
import re
with open('$REPO_ROOT/CHANGELOG.md') as f:
    content = f.read()
# Find first ## [version] block
blocks = re.split(r'^## \[', content, flags=re.MULTILINE)
if len(blocks) > 1:
    first = blocks[1]
    lines = first.split('\n')
    print('  Version: ' + lines[0].split(']')[0])
    for line in lines[1:15]:
        if line.strip():
            print('  ' + line)
" 2>/dev/null || true
    fi
    echo ""

    # Prompt for confirmation on major version upgrades
    if [ -t 0 ]; then
      printf "${BOLD}  Proceed with major version update? [y/N] ${RESET}"
      read -r confirm
      if [[ ! "${confirm:-n}" =~ ^[Yy]$ ]]; then
        info "Update cancelled."
        exit 0
      fi
    fi
  fi
}

# ---------------------------------------------------------------------------
# Pull latest from remote
# ---------------------------------------------------------------------------
pull_updates() {
  local local_ver
  local_ver="$(get_local_version)"

  info "Current version: $local_ver"
  info "Pulling latest from remote..."

  # Fetch without merging first so we can inspect
  if ! git fetch origin --quiet 2>/dev/null; then
    fail "Could not reach remote. Check your internet connection."
  fi

  # Get remote version (from fetched plugin.json)
  local remote_ver
  remote_ver="$(git show origin/main:.claude-plugin/plugin.json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('version', 'unknown'))
" 2>/dev/null || echo "unknown")"

  info "Remote version: $remote_ver"

  if [ "$local_ver" = "$remote_ver" ]; then
    success "Already up to date (v$local_ver)"
    return 0
  fi

  check_breaking_changes "$local_ver" "$remote_ver"

  # Stash any local changes so the pull succeeds
  local stashed=false
  if ! git diff --quiet 2>/dev/null; then
    warn "Local changes detected. Stashing before update..."
    git stash push -m "pre-update-stash-$(date +%Y%m%d)" --quiet
    stashed=true
  fi

  # Pull the update
  if git pull --ff-only origin main 2>/dev/null; then
    success "Updated from v$local_ver to v$remote_ver"
  else
    if [ "$stashed" = true ]; then
      git stash pop --quiet 2>/dev/null || true
    fi
    fail "Pull failed. The update may need manual intervention (non-fast-forward)."
  fi

  if [ "$stashed" = true ]; then
    git stash pop --quiet 2>/dev/null || warn "Could not restore stash. Run 'git stash pop' manually."
  fi

  echo "$remote_ver"
}

# ---------------------------------------------------------------------------
# Re-register hooks if hooks.json changed
# ---------------------------------------------------------------------------
check_hooks_registration() {
  # If hooks.json was modified in the last pull, the plugin may need re-adding
  local hooks_changed
  hooks_changed="$(git diff HEAD~1 HEAD --name-only 2>/dev/null | grep -c 'hooks/hooks.json' || echo '0')"

  if [ "$hooks_changed" -gt 0 ]; then
    info "hooks.json changed. Re-registering plugin with Claude Code..."
    if command -v claude &>/dev/null; then
      if claude plugin add "$REPO_ROOT" 2>/dev/null; then
        success "Plugin re-registered with updated hooks"
      else
        warn "Could not re-register plugin automatically."
        warn "Run: claude plugin add $REPO_ROOT"
      fi
    else
      warn "Claude CLI not found. Run: claude plugin add $REPO_ROOT after installing CLI."
    fi
  fi
}

# ---------------------------------------------------------------------------
# Make calculators executable
# ---------------------------------------------------------------------------
make_calculators_executable() {
  local calc_dir="$SRC_DIR/calculators"
  if [ -d "$calc_dir" ]; then
    chmod +x "$calc_dir"/*.py 2>/dev/null || true
  fi
}

# ---------------------------------------------------------------------------
# Print changelog summary
# ---------------------------------------------------------------------------
print_changelog_summary() {
  echo ""
  printf "${BOLD}  Changelog (latest release):${RESET}\n"
  echo ""
  if [ -f "$REPO_ROOT/CHANGELOG.md" ]; then
    python3 -c "
import re
with open('$REPO_ROOT/CHANGELOG.md') as f:
    content = f.read()
blocks = re.split(r'^## \[', content, flags=re.MULTILINE)
if len(blocks) > 1:
    first = '## [' + blocks[1]
    lines = first.split('\n')
    # Print first 20 non-empty lines
    count = 0
    for line in lines:
        if count >= 20:
            break
        if line.strip():
            print('  ' + line)
            count += 1
" 2>/dev/null || warn "Could not read CHANGELOG.md"
  fi
  echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  printf "${CYAN}${BOLD}"
  printf "  CRE Skills Plugin -- Update\n"
  printf "${RESET}"
  echo ""

  info "Plugin root: $REPO_ROOT"

  preserve_user_data

  local new_version
  new_version="$(pull_updates)"

  check_hooks_registration
  make_calculators_executable
  print_changelog_summary

  local final_ver
  final_ver="$(get_local_version)"

  echo ""
  success "Plugin is at v$final_ver"
  echo ""
  printf "  Start a new Claude Code session to activate the updated plugin.\n"
  echo ""
}

main "$@"
