# Installation Guide

No coding experience required. Choose the method that matches your setup.

## Quickest Install (non-technical users)

**macOS:** Download the `.dmg` file from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest), open it, and double-click the installer. That's it.

**Windows:** Download the `.exe` file from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest) and run the wizard. If Windows SmartScreen warns you, click "More info" then "Run anyway."

After installing, open Claude Desktop or Claude Code and type:

```
/cre-skills:deal-quick-screen
```

Then paste your deal details. The 112 CRE skills are ready to use.

> **Important:** On Windows, update Claude Code to the latest version first.
> Open PowerShell and run: `npm i -g @anthropic-ai/claude-code@latest`

> **Do not use "Add marketplace" in Claude Desktop with this repo URL.** This is not a marketplace plugin. Use the installer or CLI method below instead. See [WHAT-TO-USE-WHEN.md](WHAT-TO-USE-WHEN.md) for details.

---

## All Install Methods

### Claude Code

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

1. Download [`cre-skills-v4.1.2.dmg`](https://github.com/mariourquia/cre-skills-plugin/releases/latest) from the latest release.
2. Open the DMG in Finder.
3. Double-click **CRE Skills Installer**.
4. A Terminal window opens -- follow the prompts (no commands to type).
5. Restart Claude Desktop.

### Windows -- EXE Installer

1. Download [`cre-skills-v4.1.2-setup.exe`](https://github.com/mariourquia/cre-skills-plugin/releases/latest) from the latest release.
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

## Codex CLI (OpenAI)

```bash
# Download portable.zip from the latest release
unzip cre-skills-portable.zip -d /tmp/cre-skills

# Project-level (recommended)
cp -r /tmp/cre-skills/skills/ .agents/skills/

# User-level (all projects)
cp -r /tmp/cre-skills/skills/ ~/.codex/skills/
```

Skills are detected automatically. Run `/skills` to verify.

---

## Gemini CLI (Google)

```bash
# Download portable.zip from the latest release
unzip cre-skills-portable.zip -d /tmp/cre-skills

# Workspace-level (recommended)
cp -r /tmp/cre-skills/skills/ .gemini/skills/

# User-level (all projects)
cp -r /tmp/cre-skills/skills/ ~/.gemini/skills/
```

Or install via `gemini skills install` if available.

---

## Grok CLI (xAI)

```bash
# Download portable.zip from the latest release
unzip cre-skills-portable.zip -d /tmp/cre-skills

# Project-level
cp -r /tmp/cre-skills/skills/ .agents/skills/

# User-level
cp -r /tmp/cre-skills/skills/ ~/.agents/skills/
```

Run `/skills` in the TUI to verify.

---

## Manus

```bash
# Download portable.zip from the latest release
unzip cre-skills-portable.zip -d /tmp/cre-skills

# Copy to Manus skills directory
cp -r /tmp/cre-skills/skills/* /home/ubuntu/skills/
```

Skills are auto-detected. Type `/SKILL_NAME` to invoke.

---

## Any Other Agent

The `cre-skills-portable.zip` contains universal `SKILL.md` files that work with any AI agent supporting the Agent Skills standard. Extract and copy the `skills/` directory to wherever your agent reads skill definitions.

---

## Building From Source

If you need to build target-specific artifacts yourself:

```bash
# Install build tools
cd tools && npm install && cd ..

# Build all 4 targets
npx --prefix tools tsx tools/build.ts --target all

# Validate
npx --prefix tools tsx tools/validate.ts --target all

# Package
npx --prefix tools tsx tools/package/package-claude-code.ts
npx --prefix tools tsx tools/package/package-cowork.ts
npx --prefix tools tsx tools/package/package-desktop.ts
npx --prefix tools tsx tools/package/package-portable.ts
```

Artifacts appear in `dist/` with SHA-256 checksums.

---

<details>
<summary>Verify downloads (developers)</summary>

All release assets include SHA-256 checksums (`.sha256` file) and [Sigstore cosign](https://www.sigstore.dev/) signatures (`.sig` + `.cert` files) for supply-chain verification. Most users do not need these.

```bash
cosign verify-blob --certificate cre-skills-*.cert \
  --signature cre-skills-*.sig \
  --certificate-identity-regexp "github.com/mariourquia" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  cre-skills-*.zip
```
</details>

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
