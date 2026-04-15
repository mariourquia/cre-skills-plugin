#!/usr/bin/env bash
# Validate marketplace and plugin manifest structure for cre-skills-plugin
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

check() {
    if [ "$1" = "0" ]; then
        printf '  \033[32mPASS\033[0m %s\n' "$2"
    else
        printf '  \033[31mFAIL\033[0m %s\n' "$2"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "Validating marketplace structure..."
echo ""

# 1. .claude-plugin/marketplace.json exists
test -f "$REPO_ROOT/.claude-plugin/marketplace.json"
check $? ".claude-plugin/marketplace.json exists"

# 2. .claude-plugin/plugin.json exists
test -f "$REPO_ROOT/.claude-plugin/plugin.json"
check $? ".claude-plugin/plugin.json exists"

# 3. marketplace.json is valid JSON
python3 -c "import json; json.load(open('$REPO_ROOT/.claude-plugin/marketplace.json'))" 2>/dev/null
check $? "marketplace.json is valid JSON"

# 4. plugin.json is valid JSON
python3 -c "import json; json.load(open('$REPO_ROOT/.claude-plugin/plugin.json'))" 2>/dev/null
check $? "plugin.json is valid JSON"

# 5. marketplace.json has required fields
python3 -c "
import json, sys
m = json.load(open('$REPO_ROOT/.claude-plugin/marketplace.json'))
assert 'name' in m, 'missing name'
assert 'owner' in m, 'missing owner'
assert 'plugins' in m, 'missing plugins'
assert len(m['plugins']) > 0, 'no plugins'
assert 'name' in m['plugins'][0], 'plugin missing name'
assert 'source' in m['plugins'][0], 'plugin missing source'
" 2>/dev/null
check $? "marketplace.json has required fields"

# 6. Plugin source path resolves
SOURCE=$(python3 -c "import json; print(json.load(open('$REPO_ROOT/.claude-plugin/marketplace.json'))['plugins'][0]['source'])")
if [ "$SOURCE" = "." ]; then
    test -f "$REPO_ROOT/.claude-plugin/plugin.json"
    check $? "Plugin source '.' resolves (plugin.json at root)"
else
    test -d "$REPO_ROOT/$SOURCE"
    check $? "Plugin source '$SOURCE' resolves"
fi

# 7. Component paths resolve
python3 -c "
import json, os, sys
p = json.load(open('$REPO_ROOT/.claude-plugin/plugin.json'))
root = '$REPO_ROOT'
errors = []
for key in ['skills', 'agents', 'commands']:
    path = p.get(key, key + '/')
    full = os.path.join(root, path.lstrip('./'))
    if not os.path.exists(full):
        errors.append(f'{key}: {full} not found')
if errors:
    print('; '.join(errors), file=sys.stderr)
    sys.exit(1)
" 2>/dev/null
check $? "Component paths (skills, agents, commands) resolve"

# 8. Hooks file exists
python3 -c "
import json, os
p = json.load(open('$REPO_ROOT/.claude-plugin/plugin.json'))
hooks_path = p.get('hooks', 'hooks/hooks.json')
full = os.path.join('$REPO_ROOT', hooks_path.lstrip('./'))
assert os.path.exists(full), f'hooks not found at {full}'
" 2>/dev/null
check $? "Hooks configuration resolves"

# 9. MCP server config exists
python3 -c "
import json, os
p = json.load(open('$REPO_ROOT/.claude-plugin/plugin.json'))
mcp_path = p.get('mcpServers', '.mcp.json')
if isinstance(mcp_path, str):
    rel = mcp_path[2:] if mcp_path.startswith('./') else mcp_path
    full = os.path.join('$REPO_ROOT', rel)
    assert os.path.exists(full), f'MCP config not found at {full}'
" 2>/dev/null
check $? "MCP server config resolves"

# 10. mcp-server.mjs exists
test -f "$REPO_ROOT/src/mcp-server.mjs"
check $? "mcp-server.mjs exists"

# 11. plugin.json is single-sourced (no stray src/plugin/ duplicate)
test ! -f "$REPO_ROOT/src/plugin/plugin.json"
check $? "no duplicate plugin.json under src/plugin/ (.claude-plugin/ is canonical)"

# 12. Version consistency
MKT_VER=$(python3 -c "import json; print(json.load(open('$REPO_ROOT/.claude-plugin/marketplace.json'))['plugins'][0].get('version',''))" 2>/dev/null)
PLG_VER=$(python3 -c "import json; print(json.load(open('$REPO_ROOT/.claude-plugin/plugin.json')).get('version',''))" 2>/dev/null)
if [ -n "$MKT_VER" ] && [ -n "$PLG_VER" ] && [ "$MKT_VER" != "$PLG_VER" ]; then
    check 1 "Version match (marketplace=$MKT_VER vs plugin=$PLG_VER)"
else
    check 0 "Version consistency (marketplace=$MKT_VER, plugin=$PLG_VER)"
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "  $ERRORS check(s) FAILED"
    exit 1
else
    echo "  All checks passed"
fi
