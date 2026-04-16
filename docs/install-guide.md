# CRE Skills Plugin -- Installation Guide

Version 4.2.0 | Apache 2.0 License

> **Do not use "Add marketplace" in Claude Desktop with this repo URL.** This is not a marketplace plugin. Pasting this URL into Claude Desktop's "Add marketplace" dialog will produce a validation error. Use the installer or CLI method below. See [WHAT-TO-USE-WHEN.md](WHAT-TO-USE-WHEN.md) for the full explanation.

---

## Recommended: Download the Installer

The fastest way to get started on any platform.

### macOS

Download [`cre-skills-v4.2.0.dmg`](https://github.com/mariourquia/cre-skills-plugin/releases/latest), open it, and double-click **CRE Skills Installer**. The installer auto-detects Claude Desktop, Claude Code, or both.

### Windows

Download [`cre-skills-v4.2.0-setup.exe`](https://github.com/mariourquia/cre-skills-plugin/releases/latest) and run the wizard. No admin privileges required. SmartScreen may warn you -- click "More info" > "Run anyway".

After either installer finishes, restart Claude Desktop or start a new Claude Code session.

---

## Alternative: Claude Code CLI

For developers who prefer the command line:

```bash
curl -fsSL https://raw.githubusercontent.com/mariourquia/cre-skills-plugin/main/scripts/install.sh | bash
```

Or add directly:

```bash
claude plugin add github:mariourquia/cre-skills-plugin
```

## Local Development / Testing

```bash
git clone https://github.com/mariourquia/cre-skills-plugin.git
claude plugin add --plugin-dir ./cre-skills-plugin
```

Changes to src/skills/ and src/commands/ take effect immediately without reinstalling.

---

## Prerequisites by Platform

### macOS

| Requirement | Minimum | Check |
|-------------|---------|-------|
| Claude Code CLI | any | `claude --version` |
| git | any | `git --version` |
| Node.js | 18+ | `node --version` |
| Python | 3.10+ | `python3 --version` |

Install Claude Code CLI if not present:

```bash
npm install -g @anthropic-ai/claude-code
```

### Linux (Ubuntu/Debian, Fedora, Arch)

Same requirements as macOS. Node.js 18+ and Python 3.10+ may need manual installation:

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs python3.11

# Fedora
sudo dnf install nodejs python3.11

# Arch
sudo pacman -S nodejs python
```

### Windows (Native)

| Requirement | Minimum | Check |
|-------------|---------|-------|
| Claude Code CLI or Claude Desktop | any | `claude --version` or check Start Menu |
| Node.js | 18+ | `node --version` |
| Python | 3.10+ (optional, for calculators) | `python --version` |

Install Claude Code CLI if not present:

```powershell
npm install -g @anthropic-ai/claude-code
```

Download the `.exe` installer from the [releases page](https://github.com/mariourquia/cre-skills-plugin/releases/latest). No other setup required.

### Windows WSL2 (Alternative)

If you prefer running inside WSL2 instead of native Windows:

1. Install WSL2: `wsl --install` from PowerShell (Admin)
2. Open an Ubuntu terminal
3. Install prerequisites inside WSL:

```bash
# Node.js via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20

# Python
sudo apt-get install -y python3.11 python3.11-venv

# Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

4. Then run the quick install command from inside the WSL terminal.

Note: For most Windows users, the native `.exe` installer is the recommended path. WSL2 is an alternative for users who prefer a Linux environment.

---

## Manual Install (Step by Step)

Use this if the one-command installer fails or you prefer explicit control.

### Step 1: Clone the repository

```bash
git clone https://github.com/mariourquia/cre-skills-plugin.git
```

Clone it wherever you want it to live. A sensible location: `~/.claude/plugins/cre-skills-plugin`.

```bash
mkdir -p ~/.claude/plugins
git clone https://github.com/mariourquia/cre-skills-plugin.git ~/.claude/plugins/cre-skills-plugin
```

### Step 2: Register with Claude Code

```bash
claude plugin add ~/.claude/plugins/cre-skills-plugin
```

Or, if `claude plugin add` is not yet available in your CLI version:

```bash
claude --plugin-dir ~/.claude/plugins/cre-skills-plugin
```

To load the plugin automatically in every session, add the `plugin-dir` to your Claude Code settings file (`~/.claude/settings.json`):

```json
{
  "pluginDirs": ["~/.claude/plugins/cre-skills-plugin"]
}
```

### Step 3: Make calculators executable

```bash
chmod +x ~/.claude/plugins/cre-skills-plugin/src/calculators/*.py
```

### Step 4: Verify

```bash
~/.claude/plugins/cre-skills-plugin/scripts/verify-install.sh
```

---

## Claude Desktop Installation

### macOS DMG Installer

For Claude Desktop users, the DMG is the simplest path.

1. Download `cre-skills-v4.2.0.dmg` from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest).
2. Open the DMG.
3. Double-click "CRE Skills Installer".
4. Follow the Terminal prompts. The installer detects Claude Code and Claude Desktop and configures each automatically.
5. Restart Claude Desktop.

### Windows .exe Installer

For Windows users with Claude Code CLI or Claude Desktop.

1. Download `cre-skills-v4.2.0-setup.exe` from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest).
2. Run the installer. Windows SmartScreen may show a warning -- click "More info" then "Run anyway" (the installer is not yet code-signed).
3. Follow the wizard. Default install location: `%APPDATA%\cre-skills-plugin`.
4. The installer automatically detects Claude Code and Claude Desktop and configures each.
5. Restart Claude Code or Claude Desktop.

**Note**: The installer does not require administrator privileges.

The plugin directory for Claude Desktop on Windows is:

```
%APPDATA%\cre-skills-plugin\
```

### Manual Claude Desktop Configuration

If you have already cloned the repo via the CLI method:

1. Open Claude Desktop.
2. Go to **Settings** > **Plugins**.
3. Click **Add Plugin** (or **Load from Disk**).
4. Select the cloned `cre-skills-plugin` directory.
5. Confirm `cre-skills` appears as Active in the plugin list.
6. Start a new conversation to activate the SessionStart hook.

The plugin directory for Claude Desktop on macOS is:

```
~/Library/Application Support/Claude/skills/cre-skills-plugin/
```

You can also copy the plugin there directly and it will be picked up on next launch.

---

## Claude.ai Web Installation

This plugin is not available in the Claude Desktop or Claude.ai marketplace. There is no `marketplace.json` in this repo and pasting the repo URL into "Add marketplace" will fail.

The plugin is available via Claude Code CLI (plugin install) and Claude Desktop (DMG/EXE installer only). See [WHAT-TO-USE-WHEN.md](WHAT-TO-USE-WHEN.md) for which method to use.

---

## VS Code / JetBrains

The plugin is a Claude Code plugin, not a VS Code or JetBrains extension. It works when you run Claude Code within VS Code's integrated terminal:

```bash
# From VS Code terminal
claude --plugin-dir /path/to/cre-skills-plugin
```

There is no separate VS Code extension or JetBrains plugin.

---

## Updating from v1 to v2

### What Changed

| Area | v1.0.0 | v2.0.0 | v3.0.0 | v4.0.0 |
|------|--------|--------|--------|--------|
| Skills | 80 | 99 | 105 | 112 |
| License | MIT | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| Hooks | SessionStart | SessionStart + PostToolUse + Stop | Same | Same |
| Calculators | 0 | 11 | 11 | 12 |
| Commands | 3 | 7 | 9 | 11 |
| Source layout | flat (root) | flat (root) | flat (root) | `src/` directory |

### License Change Notice

v2.0.0 changes the license from MIT to Apache 2.0. The Apache 2.0 license includes an explicit patent grant. For most users this makes no practical difference. Review the `LICENSE` and `NOTICE` files for details.

### Automatic Migration

Run the v2 installer. It detects v1 data and:

1. Backs up `~/.cre-skills/config.json` and `brand-guidelines.json` before any overwrite.
2. Displays the license change notice.
3. Updates the plugin to v2.

```bash
# From inside the existing plugin directory
./scripts/install.sh

# Or re-run the one-liner
curl -fsSL https://raw.githubusercontent.com/mariourquia/cre-skills-plugin/main/scripts/install.sh | bash
```

### Manual Migration

```bash
cd /path/to/cre-skills-plugin
git pull --ff-only origin main
claude plugin add .
```

Your `~/.cre-skills/` data (config, brand guidelines, telemetry, feedback) is never touched by `git pull`. It is safe.

---

## Updating to Latest

```bash
cd /path/to/cre-skills-plugin
./scripts/update.sh
```

The update script:
- Pulls the latest from `origin/main`.
- Checks for major version bumps and prompts for confirmation.
- Backs up your user data before pulling.
- Re-registers the plugin if `hooks.json` changed.
- Prints a changelog summary.

---

## Verifying the Installation

Run the health check:

```bash
./scripts/verify-install.sh
```

Expected output (healthy):

```
  PASS  113 skill directories all have SKILL.md
  PASS  247 reference files all non-empty
  PASS  12 Python calculators are syntactically valid
  PASS  src/hooks/hooks.json is valid JSON
  PASS  All 3 Node.js hook scripts parse correctly
  PASS  ~/.cre-skills exists and is writable
```

Machine-readable output for CI:

```bash
./scripts/verify-install.sh --json
```

---

## Troubleshooting

### Skills not activating

- Start a **new** conversation. The SessionStart hook only fires at conversation start.
- Confirm the plugin appears as Active: `claude plugin list`
- If not listed: `claude plugin add /path/to/cre-skills-plugin`

### "claude plugin add" not found

Your CLI version may predate the `plugin` subcommand. Use:

```bash
claude --plugin-dir /path/to/cre-skills-plugin
```

Or update Claude Code:

```bash
npm update -g @anthropic-ai/claude-code
```

### Node.js hook errors

Hooks require Node.js 18+. Check:

```bash
node --version
```

If below 18, upgrade from [nodejs.org](https://nodejs.org/) or via nvm:

```bash
nvm install 20 && nvm use 20
```

### Python calculators fail to run

```bash
# Check Python version
python3 --version  # needs 3.10+

# Make executable
chmod +x /path/to/cre-skills-plugin/src/calculators/*.py

# Test a calculator directly
python3 /path/to/cre-skills-plugin/src/calculators/debt_sizing.py
```

### Wrong skill activates

Use the router to find the exact skill:

```
/cre-skills:cre-route <describe your task>
```

The router matches against 91+ trigger patterns. If the match is ambiguous it presents 2-3 options.

### ~/.cre-skills/config.json errors

Delete the file to reset it. It will be recreated with defaults on next session start:

```bash
rm ~/.cre-skills/config.json
```

### Windows SmartScreen warning

The `.exe` installer is not code-signed. Windows SmartScreen will warn "Windows protected your PC." Click "More info" then "Run anyway." This is safe -- the installer is built reproducibly from source via GitHub Actions. You can verify the SHA256 checksum from the release page. Code signing will be added in a future release.

### Hooks not firing on Windows WSL

Confirm you are running Claude Code inside the WSL terminal (not native Windows). The hook scripts use Node.js `os.homedir()` which resolves to the Linux home directory in WSL.

---

## Uninstalling

```bash
./scripts/uninstall.sh
```

The script removes the plugin from Claude Code and asks whether to keep `~/.cre-skills/` user data (config, brand guidelines, telemetry, feedback). Plugin files themselves are not deleted -- remove the directory manually if desired.

---

## Post-Install Quick Start

Once installed, start a new conversation:

```
/cre-skills:cre-route quick screen this deal

240-unit garden-style multifamily in Raleigh, NC. Asking $42M. 2018 vintage.
Current occupancy 93%. In-place NOI $2.6M. Broker says rents are 12% below market.
```

Browse workflows:

```
/cre-skills:cre-workflows
```

List agents:

```
/cre-skills:cre-agents
```

Set up brand guidelines for investor deliverables:

```
/cre-skills:brand-config
```
