# AGENTS.md — cre-skills-plugin

Public open-core CRE skills plugin (Apache-2.0). The paid governance layer lives
in the private sibling repo `cre-skills-pro`; net-new premium work lands there,
while this repo carries the free knowledge layer (skills, agents, calculators,
catalog, MCP server, installers).

## Tests (two suites — run both before any release)

```bash
python3 -m pytest            # scoped suite (pyproject testpaths: residential_multifamily)
python3 -m pytest tests/     # top-level integration suite (catalog, manifests, installers)
```

- `tests/conftest.py` rebuilds `dist/catalog.json` (via `catalog-build.py --json`)
  once per session, so a single run from a fresh checkout is deterministic and
  always tests current sources. Do not remove that fixture: most of `tests/`
  consumes `dist/catalog.json`, which is gitignored.
- `src/skills/residential_multifamily/workflows/implementation_intake_signoff_builder`
  is excluded from the scoped run (see pyproject comment) — known Wave-5 gap.
- GitHub Actions billing is OFF for this account. These local suites are the
  only gate; never claim CI will catch anything.

## Generated artifacts (never hand-edit)

- `src/catalog/catalog.yaml` + `dist/catalog.json` — `python3 scripts/catalog-build.py`
  (`--json` writes only the dist file; rebuilds are idempotent: a content-identical
  rebuild preserves the existing `generated_at` stamp).
- `docs/integrations/amos-skill-manifest.sample.json` —
  `python3 scripts/amos-manifest-build.py --emit-sample`.

## Releases

1. `python3 scripts/release-bump.py --version X.Y.Z` — bumps `.claude-plugin/plugin.json`
   and every mechanical pin (install.sh, install docs, README header) and regenerates
   the artifacts above. `tests/test_version_pins.py` is the tripwire if a pin drifts.
2. Follow the printed manual checklist (CHANGELOG section, README tagline,
   binaries, ROADMAP for minor/major).
3. Tag `vX.Y.Z` only after BOTH pytest suites are green.

## Conventions

- Never commit to `main`; branch → PR → merge (confirm with Mario before PR/merge/push).
- Commits are agent-signed (repo-local `agent_signing` key); no `Co-Authored-By`
  or other attribution trailers.
- Python: snake_case, type hints on new/modified functions.
