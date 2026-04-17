# Tests

Structural and functional integrity tests for the CRE Skills Plugin. Most tests validate plugin layout, catalog parity, hook/script syntax, reference data integrity, and release hygiene. A smaller set exercises individual calculators and orchestrator state machines.

## Requirements

- Python 3.10+
- Node.js 18+ (for hook script syntax checks and calculator-bridge smoke tests)
- `pytest` (`pip install pytest`)

No other runtime dependencies. The Python suite uses only the standard library plus `pytest`; the Node test harnesses used by a few orchestrator tests live under `tests/harness_*.mjs` and require no npm install.

## Running the test suite

From the repo root:

```bash
python -m pytest tests/ -v
```

Run a single test module:

```bash
python -m pytest tests/test_plugin_integrity.py -v
```

Run the residential_multifamily subsystem suite:

```bash
python -m pytest src/skills/residential_multifamily/tests/ -v
```

## What is tested

The suite covers (non-exhaustive; regenerate this list with `ls tests/test_*.py`):

| Area | Representative tests |
|------|----------------------|
| Plugin manifest and structure | `test_plugin_integrity.py`, `test_required_files_exist` |
| Catalog / filesystem parity | `test_canonical_consistency.py`, `test_catalog_claim_integrity.py` |
| Release hygiene | `test_release_hygiene.py`, `test_release_version_parity.py` |
| Hook script syntax | `test_plugin_integrity.py::TestHookScripts` |
| Python calculators (syntax + behavior) | `test_plugin_integrity.py::TestCalculators`, `test_e2e_skill_calculator.py` |
| MCP server | `test_plugin_integrity.py::TestMcpServer` |
| Orchestrator engine | `test_orchestrator_integrity.py`, `test_orchestrator_deal_state.py`, `test_orchestrator_gates_variants.py`, `test_orchestrator_calculator_bridge.py` |
| Installer hardening (Windows BOM, argv, hook scope) | `test_installer_hardening.py` |
| residential_multifamily subsystem | `src/skills/residential_multifamily/tests/` |
| Sealed-close gating (v4.2.0 Obj 5) | `test_period_seal_gating.py` |
| Finance placeholder scanner (v4.2.0 Obj 6) | `test_finance_placeholder_scanner.py` |
| Executive output contract (v4.2.0 Obj 8) | `test_executive_output_contract.py` |

## CI

The same suite runs on every push and pull request to `main` via `.github/workflows/ci.yml`, across Python 3.10/3.11/3.12 and Node 18/20/22.
