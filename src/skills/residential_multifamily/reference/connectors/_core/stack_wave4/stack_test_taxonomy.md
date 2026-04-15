# Stack Test Taxonomy — Wave 4

Status: wave_4_authoritative
Audience: data_platform_team, qa

Wave 4 adds stack-specific tests on top of the existing 192-test baseline.
Tests live in two places:
- Skill-level: `tests/test_*.py` (rolls up across all adapters)
- Adapter-local: `reference/connectors/adapters/<vendor>/tests/test_adapter.py`

| Test Class | Location | Asserts |
|---|---|---|
| Adapter contract tests | `adapters/<vendor>/tests/test_adapter.py` | manifest.yaml conforms to adapter_manifest.schema.yaml; required files present (README, source_contract, normalized_contract, samples, dq_rules); connector_domain valid; vendor_family declared |
| Field-mapping tests | `adapters/<vendor>/tests/test_adapter.py` | field_mapping.yaml covers every entity in sample_raw; every canonical field declared has a transform_hint; no unmapped raw fields without explicit `omit:` reason |
| Raw-to-normalized tests | `adapters/<vendor>/tests/test_adapter.py` | every sample_raw record has a corresponding sample_normalized record with same logical key; provenance envelope preserved end-to-end |
| Normalized-to-derived tests | `tests/test_stack_normalized_to_derived.py` (new) | for at least 2 derived metrics per workflow, normalized inputs produce expected derived shape (compute test against canonical metric formula in `_core/metrics.md`) |
| Identity resolution tests | `tests/test_master_data_crosswalks.py` (extend) | every crosswalk_additions.yaml fragment merges cleanly; canonical_id collisions detected; effective_dating monotonic |
| Crosswalk effective-date tests | `tests/test_master_data_crosswalks.py` (extend) | for any source_id with two rows, effective_start dates do not overlap unless one row carries effective_end before the second's effective_start |
| Source disagreement tests | `tests/test_stack_source_disagreement.py` (new) | for every object in source_of_truth_matrix.md, simulated disagreement triggers correct resolution rule (primary wins, secondary becomes audit) |
| DQ hard-fail and soft-fail tests | `adapters/<vendor>/tests/test_adapter.py` | every dq_rule with severity=blocker, a sample_invalid record triggers it; every severity=warning record degrades confidence not blocks |
| Reconciliation tests | `tests/test_stack_reconciliation.py` (new) | every check_id in stack_reconciliation_matrix.md exists in some adapter's reconciliation_checks.yaml; tolerance refs resolve to a reconciliation_tolerance_band.yaml entry |
| Workflow activation tests | `tests/test_workflow_activation_map.py` (extend) | every wave-4 adapter's workflow_activation_additions.yaml references workflows that exist in `workflows/` OR are tagged `proposed_new` with a follow-up note |
| Fallback-mode tests | `tests/test_stack_fallback_modes.py` (new) | for each workflow with `partial_mode_behavior`, missing-input scenario produces the documented partial output, never silent failure |
| Excel template validation tests | `adapters/excel_market_surveys/tests/test_adapter.py` | each template_schema parses; sample_valid passes schema; sample_invalid triggers documented error |
| GraySail classification-path tests | `adapters/graysail_placeholder/tests/test_adapter.py` | placeholder manifest declares `placeholder_pending_clarification`; classification_worksheet present; bounded_assumptions has confidence + remediation; no canonical workflow has GraySail as `primary` source while status is placeholder |
| Schema drift tests | `tests/test_stack_schema_drift.py` (new) | for each adapter, raw payload schema version captured; drift detection scaffold present; alerts wired to `schema_drift_escalation.md` |
| Regression tests | `tests/test_canonical_regression.py` (new) | canonical metric definitions in `_core/metrics.md` unchanged; canonical ontology unchanged; routing axes unchanged; if any of these change, test fails with explicit instruction to update via canonical-change process |
| Security/config tests | `tests/test_integration_security.py` (extend) | no secrets in any wave-4 adapter file (grep credential patterns); pii_classification declared on every source_registry entry; sample data carries `status: sample` tag; no real names/addresses |

## Pytest collection

All tests collected by repo-level `conftest.py`. Adapter-local tests use the
`_test_helpers.py` module already present in `reference/connectors/adapters/`.

## CI gates

- Wave-4 tests must be added to the existing CI workflow (no new CI file)
- Test failure on any wave-4 test blocks merge
- Test execution time target: <60 seconds for wave-4 additions

## Coverage targets (informational)

| Adapter | Tests in wave 4 | Cumulative tests after wave 4 |
|---|---|---|
| appfolio_pms | ~20 | ~20 |
| sage_intacct_gl | ~20 | ~20 |
| procore_construction | ~20 | ~20 |
| dealpath_deal_pipeline | ~15 | ~15 |
| excel_market_surveys | ~25 | ~25 |
| manual_sources_expanded | ~10 | ~10 |
| graysail_placeholder | ~8 | ~8 |
| Skill-level wave-4 (5 new test files) | ~30 | (added to 192 baseline) |
| Total wave-4 net adds | ~148 | ~340 |
