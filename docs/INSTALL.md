# Installation Guide

> **Do not use "Add marketplace" in Claude Desktop with this repo URL.** This is not a marketplace plugin. Pasting `https://github.com/mariourquia/cre-skills-plugin` into Claude Desktop's "Add marketplace" dialog will fail with a validation error. Use the installer or CLI method below instead. See [WHAT-TO-USE-WHEN.md](WHAT-TO-USE-WHEN.md) for the full explanation of which install method to use.

---

## Claude Code

### One-liner (recommended)

```bash
claude plugin install --repo mariourquia/cre-skills-plugin
```

### From Release Artifact

1. Download `cre-skills-claude-code.zip` from the latest [GitHub Release](https://github.com/mariourquia/cre-skills-plugin/releases)
2. Unzip and install:
   ```bash
   unzip cre-skills-claude-code.zip -d cre-skills-plugin
   claude plugin install --dir cre-skills-plugin
   ```
3. Verify:
   ```bash
   claude --plugin-dir cre-skills-plugin -p "list available CRE skills"
   ```

### From Source (development)

```bash
git clone https://github.com/mariourquia/cre-skills-plugin.git
cd cre-skills-plugin
claude --plugin-dir .
```

Symlinks in the repo root point to `src/`, so the plugin loads correctly from the repo root.

### Verification (Claude Code)

1. Start a new conversation (SessionStart hook fires on conversation start).
2. Run: `claude plugin list` and confirm `cre-skills` appears.
3. Try: `/cre-skills:cre-route screen this deal`
4. Run the structural health check:
   ```bash
   ./scripts/verify-install.sh
   ```

---

## Claude Desktop

### macOS -- DMG Installer

1. Download [`cre-skills-v4.0.0.dmg`](https://github.com/mariourquia/cre-skills-plugin/releases/latest) from the latest release.
2. Open the DMG in Finder.
3. Double-click **CRE Skills Installer**.
4. A Terminal window opens -- follow the prompts (no commands to type).
5. Restart Claude Desktop.

### Windows -- EXE Installer

1. Download [`cre-skills-v4.0.0-setup.exe`](https://github.com/mariourquia/cre-skills-plugin/releases/latest) from the latest release.
2. Run the installer. Windows SmartScreen may warn you -- click **More info**, then **Run anyway** (the installer is not code-signed yet).
3. Follow the wizard. Default location: `%APPDATA%\cre-skills-plugin`.
4. Restart Claude Desktop.

No admin privileges required.

### Verification (Claude Desktop)

1. Open Claude Desktop.
2. Go to **Settings > Developer > MCP Servers**.
3. Confirm `cre-skills` appears in the server list.
4. Start a new conversation and ask: "What CRE skills do you have?"
5. Try a concrete prompt: "Screen this deal -- 240-unit multifamily, Raleigh, $42M"

If `cre-skills` does not appear in the MCP server list, see Troubleshooting below.

---

## Cowork

### From Release Artifact

1. Download `cre-skills-cowork.zip` from the latest [GitHub Release](https://github.com/mariourquia/cre-skills-plugin/releases)
2. Import via Cowork's plugin interface

### What's Different in Cowork

- Skill frontmatter contains only `name` and `description`
- Agents include `model` and `color` fields (required by Cowork)
- Commands have no `name` field in frontmatter
- Hooks are prompt-only (no telemetry scripts)
- Orchestrators, MCP server, and Python calculators are not included
- Manifest has no `userConfig` block

See [COMPATIBILITY.md](COMPATIBILITY.md) for the full matrix.

---

## Building From Source

If you need to build target-specific artifacts yourself:

```bash
# Install build tools
cd tools && npm install && cd ..

# Build both targets
npx --prefix tools tsx tools/build.ts --target all

# Validate
npx --prefix tools tsx tools/validate.ts --target all

# Package
npx --prefix tools tsx tools/package/package-cowork.ts
npx --prefix tools tsx tools/package/package-claude-code.ts
```

Artifacts appear in `dist/` with SHA-256 checksums.

---

## Verification

After installing, verify the checksum:

```bash
shasum -a 256 -c cre-skills-cowork.zip.sha256
shasum -a 256 -c cre-skills-claude-code.zip.sha256
```

---

## Troubleshooting

### Skills not appearing in Claude Desktop

1. Restart Claude Desktop after installation.
2. Check **Settings > Developer > MCP Servers** for a `cre-skills` entry.
3. Verify Node.js 18+ is installed: open Terminal and run `node --version`.
4. Check that the config file contains the MCP entry:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
5. If `cre-skills` is missing from the config, re-run the installer.

### Skills not activating in Claude Code

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

### Windows SmartScreen blocks the installer

The `.exe` installer is not code-signed. Windows SmartScreen will warn "Windows protected your PC." Click "More info" then "Run anyway." You can verify the SHA256 checksum from the release page.

### Validation error when pasting repo URL into "Add marketplace"

This is expected. This repo is not a marketplace plugin. Use the DMG/EXE installer for Claude Desktop or `claude plugin install` for Claude Code. See [WHAT-TO-USE-WHEN.md](WHAT-TO-USE-WHEN.md).
