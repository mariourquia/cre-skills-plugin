# Tests

Structural integrity tests for the CRE Skills Plugin. These validate plugin layout, file presence, and syntax -- not behavioral correctness (skills are markdown-based, not executable code).

## Requirements

- Python 3.10+
- Node.js 18+ (for hook script syntax checks)
- `pytest` (`pip install pytest`)

No other dependencies required. The test suite uses only the Python standard library plus `pytest`.

## Running Tests

From the repo root:

```bash
python -m pytest tests/ -v
```

To run a single test class:

```bash
python -m pytest tests/test_plugin_integrity.py::TestPluginStructure -v
```

## What Is Tested

| Test | Description |
|------|-------------|
| `test_plugin_json_valid` | `plugin.json` parses as valid JSON, version is 4.0.0, license is Apache-2.0 |
| `test_all_skills_have_skillmd` | Every directory under `src/skills/` contains a `SKILL.md` |
| `test_hooks_json_valid` | `src/hooks/hooks.json` parses as valid JSON and has a `hooks` key |
| `test_hook_scripts_syntax` | All `.mjs` files in `src/hooks/` pass `node --check` |
| `test_python_calculators_syntax` | All `.py` files in `src/calculators/` are syntactically valid Python |
| `test_required_files_exist` | Root-level required files are present (LICENSE, NOTICE, README.md, etc.) |
| `test_agents_index_exists` | `src/agents/_index.md` exists |
| `test_routing_index_exists` | `src/routing/CRE-ROUTING.md` exists |
| `test_skill_count_matches_plugin_json` | At least 88 `SKILL.md` files exist across skill directories |

## CI

These same tests run automatically on every push and pull request to `main` via `.github/workflows/ci.yml`, across Python 3.10/3.11/3.12 and Node 18/20/22.
