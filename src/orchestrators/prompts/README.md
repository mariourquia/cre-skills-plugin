# Orchestrator Prompts — Wiring Status

This directory contains prompt files used by the orchestrator engine and by documentary references. **Not every prompt here is wired into the pipeline engine.**

## Canonical 10 (wired — have matching config in `../configs/` and appear in catalog)

These 8 prompt files are production orchestrators with both a prompt and a config:

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

The remaining 2 canonical orchestrators (`acquisition.json`, `hold-period.json`) are engine-driven via config alone and do not yet have a prompt artifact in this directory.

## Documentary / experimental prompts (not wired)

These prompts describe desired pipeline behavior but do **not** have matching configs in `../configs/` and are **not** loaded by the pipeline engine. They are preserved for product design reference and experimental development:

- `asset-management-orchestrator.md` — referenced by asset-type deep-dive work; pending config
- `challenge-layer-orchestrator.md` — belongs to the challenge-layer subsystem (see `../challenge-layer/`), not the pipeline engine
- `closing-orchestrator.md` — design reference for the closing phase; agents currently invoked inline from `acquisition.json`
- `due-diligence-orchestrator.md` — design reference; DD work is currently inside `acquisition.json`
- `financing-orchestrator.md` — design reference; superseded by `capital-stack.json`
- `legal-orchestrator.md` — design reference
- `master-orchestrator.md` — documentary meta-coordinator; not a pipeline
- `underwriting-orchestrator.md` — design reference; underwriting lives in `acquisition.json`

**Do not add these to the catalog or claim them in public-facing counts.** The plugin claims 10 orchestrator pipelines — that count refers only to the 10 configs in `../configs/`.
