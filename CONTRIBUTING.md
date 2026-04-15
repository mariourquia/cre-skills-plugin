# Contributing to CRE Skills Plugin

Thank you for your interest in contributing. This plugin provides institutional-grade CRE skills for Claude Code, covering deal pipeline, capital markets, asset management, leasing, development, disposition, and operations.

Contributions fall into four categories: new skills, new agents, improvements to existing content, and infrastructure changes.

---

## Table of Contents

- [Adding a New Skill](#adding-a-new-skill)
- [Adding a New Agent](#adding-a-new-agent)
- [Skill Quality Requirements](#skill-quality-requirements)
- [Agent Quality Requirements](#agent-quality-requirements)
- [Improving Existing Content](#improving-existing-content)
- [Infrastructure Changes](#infrastructure-changes)
- [PR Process](#pr-process)
- [Code of Conduct](#code-of-conduct)

---

## Adding a New Skill

Skills live in `src/skills/<slug>/` where `<slug>` is a lowercase-hyphenated name describing the skill's function.

### Directory Structure

```
src/skills/<slug>/
  SKILL.md                    # Skill definition (required)
  references/                 # Supporting reference files (required, at least 1)
    <reference-file>.md       # Markdown reference
    <reference-file>.yaml     # Structured data reference
```

### SKILL.md Format

Every SKILL.md must include these sections, in this order:

```markdown
---
name: <slug>
slug: <slug>
version: 0.1.0
status: deployed
category: reit-cre
description: "One-paragraph description of what the skill does, when it triggers, and what it produces."
targets:
  - claude_code
---

# Skill Display Name

One-paragraph persona and behavioral description. Establishes the expert role Claude adopts when this skill activates.

## When to Activate

- Bullet list of trigger conditions (user actions, phrases, contexts)
- Include negative triggers (when NOT to activate, and which skill to use instead)

## Input Schema

Table of fields the user provides. Each field has:
| Field | Required | Default if Missing |

Include fallback logic: "If fewer than N required fields are present, ask clarifying questions."

## Process

### Step 1: [Name]
Detailed instructions for the first step.

### Step 2: [Name]
...continue for all steps.

## Output Format

Exact structure of what the skill produces. Use code blocks for templates.

## Red Flags

Bullet list of warning signs the skill should surface. These are domain-specific risks that require human judgment.

## Chain Notes

Which skill(s) come before and after this one in a workflow:
- **Upstream**: [skill-slug] -- when the user has already done X
- **Downstream**: [skill-slug] -- suggest this as the next step
```

### Reference Files

Every skill must include at least one reference file in its `references/` directory. Reference files provide the domain knowledge the skill depends on:

- **Methodology files** (`.md`): Explain formulas, frameworks, industry standards, or analytical approaches.
- **Data files** (`.yaml`): Structured lookup tables, benchmarks, checklists, templates, or worked examples.

Name reference files descriptively: `loan-sizing-formulas.md`, `replacement-cost-benchmarks.yaml`, `worked-screening-example.yaml`.

---

## Adding a New Agent

Agents live in `src/agents/<name>.md` where `<name>` is a lowercase-hyphenated role identifier.

### Agent File Format

```markdown
---
description: "One-paragraph summary of who this agent is, their experience level, analytical lens, and when to deploy them."
---

# Agent Display Name

Detailed persona description. Establishes background, experience, and default stance.

## How You Think

The agent's mental model, biases, and analytical approach.

## What You Prioritize

Numbered list of what this agent focuses on, in order of importance.

## Your Analytical Framework

What the agent produces when deployed. Specific deliverables.

## What You Challenge

Assumptions and patterns this agent pushes back on.

## Your Key Questions

Numbered list of questions this agent always asks.

## Output Style

How the agent formats responses: tone, structure, level of detail.
```

### Agent Categories

Place new agents into the appropriate category. If adding a new category, update `src/agents/_index.md` to include it.

| Category | Purpose | Examples |
|---|---|---|
| Investment Function | Role-based professionals | acquisitions-analyst, asset-manager |
| Adversarial / Challenge | Devil's advocate stress-testers | conservative-lender, ic-challenger |
| Titan Thinking-Style | Channel CRE legend frameworks | titan-zell, titan-linneman |
| Stakeholder Perspective | External viewpoints deals must satisfy | perspective-tenant, perspective-lender |
| Institutional Buyer | How different buyers evaluate assets | buyer-pension-fund, buyer-private-equity |
| Analytical Lens | Different analytical frames | lens-quantitative, lens-contrarian |
| Composite / Orchestration | General-purpose or multi-agent orchestrators | cre-veteran, deal-team-lead |

---

## Skill Quality Requirements

A skill is ready for merge when it meets all of the following:

- [ ] **SKILL.md exists** with all required sections (frontmatter, persona, trigger conditions, input schema, process steps, output format, red flags, chain notes)
- [ ] **At least 1 reference file** in `references/` with substantive domain content
- [ ] **Trigger conditions are specific** -- not vague catch-alls. Include negative triggers.
- [ ] **Input schema has defaults** for every optional field, with conservative assumptions stated
- [ ] **Process steps are actionable** -- Claude can follow them without ambiguity
- [ ] **Output format uses a template** -- not just "produce a report"
- [ ] **Red flags are domain-specific** -- not generic risk warnings
- [ ] **Chain notes point to real skills** that exist in the plugin (or are being added in the same PR)
- [ ] **No hallucinated data** -- reference files use real industry benchmarks or clearly label examples as illustrative
- [ ] **Slug matches directory name** -- `src/skills/foo-bar/SKILL.md` has `slug: foo-bar` in frontmatter

---

## Agent Quality Requirements

An agent is ready for merge when it meets all of the following:

- [ ] **Clear perspective** -- the agent has a distinct point of view, not a generic "expert"
- [ ] **Analytical framework** -- specific deliverables the agent produces, not vague descriptions
- [ ] **Key questions** -- at least 5 questions the agent always asks
- [ ] **Output format** -- defined tone, structure, and detail level
- [ ] **Challenge patterns** -- assumptions the agent pushes back on
- [ ] **Category fit** -- placed in the correct agent category
- [ ] **Listed in `src/agents/_index.md`** -- the agent roster index includes the new agent
- [ ] **Description frontmatter** -- the `description` field in YAML frontmatter is a complete one-paragraph summary

---

## Improving Existing Content

Improvements to existing skills and agents are welcome. Common improvements:

- Adding reference files to skills that have only one
- Improving process steps with more specific instructions
- Adding worked examples (`.yaml` files with realistic numbers)
- Expanding red flag lists based on real-world experience
- Fixing chain notes to point to the correct upstream/downstream skills
- Adding negative trigger conditions to reduce misrouting

When improving, preserve the existing structure. Do not reorganize sections or rename files without discussion in an issue first.

---

## Infrastructure Changes

Changes to these files require extra review:

- `.claude-plugin/plugin.json` -- plugin manifest, the **single source of truth** for version, description, and bundled config paths. Claude Code reads this for `/doctor` and plugin detection. The CI version check (`scripts/version_check.py`) validates that installer fallback values match this file.
- `src/hooks/hooks.json` -- session start behavior
- `src/routing/CRE-ROUTING.md` -- routing index (must stay in sync with skills)
- `registry.yaml` -- machine-readable skill index (must stay in sync with skills)
- `src/commands/*.md` -- slash commands

If you add a new skill, you must also:
1. Add it to `src/routing/CRE-ROUTING.md` with appropriate trigger patterns
2. Add it to `registry.yaml` with correct metadata

---

## Distribution

Release artifacts are published to GitHub Releases when a version tag is pushed.

### Artifacts

- **Source archives** (`.tar.gz`, `.zip`): Auto-generated by GitHub when a release is created from a tag.
- **macOS DMG** (`cre-skills-v<version>.dmg`): Built locally via the `scripts/create-dmg.sh` script. The DMG contains a self-extracting installer that detects Claude Code and/or Claude Desktop and configures both.

### Release Process

1. Tag the release: `git tag v4.1.2 && git push origin v4.1.2`
2. Build the DMG: `./scripts/create-dmg.sh`
3. Create a GitHub release from the tag and attach the DMG as a release asset alongside the auto-generated source archives.

### Code Signing

No Apple code signing is required for distribution. The DMG installer is a shell script packaged inside a disk image. Users who want to sign the DMG with their own Developer ID can do so using `codesign` before distributing within their organization.

---

## PR Process

1. **Fork the repo** and create a branch: `feature/<skill-slug>` or `feature/agent-<name>`
2. **Add your files** following the structures above
3. **Self-review** against the quality checklists
4. **Open a PR** with:
   - Title: `Add skill: <name>` or `Add agent: <name>` or `Improve: <description>`
   - Body: What the skill/agent does, why it is needed, and which workflow chain it fits into
5. **Respond to review feedback** -- maintainers may request changes to trigger conditions, process steps, or reference content
6. **Squash and merge** once approved

### PR Checklist

```markdown
- [ ] SKILL.md has all required sections
- [ ] At least 1 reference file included
- [ ] Added to src/routing/CRE-ROUTING.md
- [ ] Added to registry.yaml
- [ ] Slug matches directory name
- [ ] No hallucinated benchmarks or data
- [ ] Chain notes point to existing skills
```

---

## Code of Conduct

This project follows standard open-source conduct expectations:

- Be respectful and constructive in discussions and reviews.
- Focus feedback on the content, not the contributor.
- CRE is a domain with strong opinions. Back claims with data, industry standards, or cited sources.
- No proprietary or confidential deal data in reference files. Use realistic but fictional examples.
- No copyrighted content from third-party publications. Describe methodologies in your own words.

---

## Questions

Open an issue on the GitHub repo for:
- Proposals for new skills or agents
- Questions about the plugin structure
- Bug reports (misrouting, incorrect reference data, broken chain notes)
- Feature requests (new workflow chains, new agent categories)
