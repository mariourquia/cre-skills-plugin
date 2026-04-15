# Orchestrator Design References

These markdown files describe orchestrators that exist as design intent but are
**not** wired into the pipeline engine. They live outside `src/orchestrators/prompts/`
on purpose so the catalog and tests can enforce a 1:1 prompt-to-config invariant
inside the plugin.

If a design reference here matures into a real pipeline:
1. Build the matching `<name>.json` config under `src/orchestrators/configs/`
2. Move the markdown file back to `src/orchestrators/prompts/`
3. Rebuild the catalog (`python scripts/catalog-build.py`)

Files in this directory:

| File | Status |
|---|---|
| `asset-management-orchestrator.md` | Pending config; asset-type deep-dive work |
| `challenge-layer-orchestrator.md` | Belongs to the challenge-layer subsystem (`src/orchestrators/challenge-layer/`), not the pipeline engine |
| `legal-orchestrator.md` | Design reference for future legal-workstream pipeline |
| `master-orchestrator.md` | Documentary meta-coordinator; not a pipeline |

Files previously here that were superseded (now in git history only):

- `closing-orchestrator.md` -- agents invoked inline from `acquisition.json`
- `due-diligence-orchestrator.md` -- DD work lives inside `acquisition.json`
- `financing-orchestrator.md` -- superseded by `capital-stack.json`
- `underwriting-orchestrator.md` -- underwriting lives in `acquisition.json`
