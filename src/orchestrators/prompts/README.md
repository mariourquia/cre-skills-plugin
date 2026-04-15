# Orchestrator Prompts

Every markdown file in this directory must have a matching `<name>.json` config
under `../configs/`. This 1:1 invariant is enforced by
`tests/test_orchestrator_integrity.py::TestPromptConfigConsistency::test_no_orphan_prompt_files`.

Design references that have no config yet live in
`docs/orchestrator-references/` so the canonical surface here stays
clean.

## Wired prompts (8)

| Prompt file | Config file |
|---|---|
| `capital-stack-orchestrator.md` | `capital-stack.json` |
| `development-orchestrator.md` | `development.json` |
| `disposition-orchestrator.md` | `disposition.json` |
| `fund-management-orchestrator.md` | `fund-management.json` |
| `investment-strategy-orchestrator.md` | `investment-strategy.json` |
| `lp-intelligence-orchestrator.md` | `lp-intelligence.json` |
| `portfolio-management-orchestrator.md` | `portfolio-management.json` |
| `research-intelligence-orchestrator.md` | `research-intelligence.json` |

The remaining 2 of the 10 canonical orchestrators (`acquisition.json`,
`hold-period.json`) are engine-driven via config alone and intentionally have
no prompt artifact. The plugin claims **10 orchestrator pipelines** -- that
count refers only to the configs in `../configs/`.
