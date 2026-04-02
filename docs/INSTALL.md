# Installation Guide

## Claude Code

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

## Verification

After installing, verify the checksum:

```bash
shasum -a 256 -c cre-skills-cowork.zip.sha256
shasum -a 256 -c cre-skills-claude-code.zip.sha256
```
