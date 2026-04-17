# Changelog

## [Unreleased]

### Added (v4.4, orchestrator engine — PR A of 3)
- **Persistent deal-scoped state (design doc section 1).** New
  `src/orchestrators/engine/deal-state.mjs` loads, writes (atomic via
  `.tmp`+rename), and mutates `<home>/.claude/cre-skills/deals/<deal_id>/state.json`
  against the schema shipped in the v4.4 scaffold. Executor gains
  `--deal-id <id>`: first run initializes state, subsequent runs
  resume from `verdicts_by_phase` and skip already-resolved phases.
  Mismatched `--pipeline` + existing deal refuses (exit 3).
- **Human-in-the-loop audit log (design doc section 5).** New
  `src/orchestrators/engine/audit-log.mjs` appends newline-delimited
  JSON events to `<dealDir>/audit_log.jsonl`. Append-only invariant:
  never reads-and-rewrites. Every orchestrator event (pipeline_started,
  phase_started/completed, pipeline_halted/completed, resume_started)
  carries `timestamp`, `event`, `actor`, `deal_id`, `run_id`.
- `tests/test_orchestrator_deal_state.py` (5 tests) covers roundtrip,
  resume, pipeline-mismatch refusal, audit append-only (SHA-256 prefix
  check), and back-compat (omitting `--deal-id` creates no deal dir).
- Omitting `--deal-id` keeps the pre-v4.4 ephemeral session flow
  unchanged — no existing behavior regresses.

## [4.2.0] - 2026-04-16

### Added (plugin v4.2.0 — hardening pass 2 close)
- **Sealed-close gating (Obj 5).** New `_core/schemas/period_seal.yaml` canonicalizes close_status ordering (`draft < soft_close < hard_close < locked`) and the `as_of` / `close_lock_timestamp` / `budget_version` / `reforecast_version` fields. `_core/final_marked_workflows.yaml` gains a `period_grade_workflows` registry enumerating six slugs with their minimum close-status floor. Six workflow `reference_manifest.yaml` files (`executive_operating_summary_generation`, `quarterly_portfolio_review`, `monthly_property_operating_review`, `monthly_asset_management_review`, `reforecast`, `budget_build`) declare `required_period_seal`. `tests/test_period_seal_gating.py` (5 tests) enforces the contract.
- **Finance placeholder scanner (Obj 6).** New `_core/reference_data_integrity.md` documents the rule: placeholder tokens (`TBD`, `TODO`, `FIXME`, `XXX`, `PLACEHOLDER`, `TKTK`) in any reference CSV read by a final-marked workflow require an explicit placeholder label. `tests/test_finance_placeholder_scanner.py` (4 tests) runs on every CSV read by the final-marked manifests.
- **Executive output contract (Obj 8).** New `_core/executive_output_contract.md` defines verdict-first structure, source-class labels (`[operator]` / `[derived]` / `[benchmark]` / `[overlay]` / `[placeholder]`), and refusal-artifact shape for final-marked output. Four final-marked SKILL.md files (executive operating summary, IC prep, quarterly portfolio review, executive pipeline summary) reference the contract; the canonical example (`executive_operating_summary_generation/examples/ex01_*.md`) demonstrates the full pattern. `tests/test_executive_output_contract.py` (4 tests) enforces the references and the canonical example shape.
- `_core/schemas/reference_manifest.yaml` extended to admit `required_period_seal` as a typed top-level field.

### Changed (plugin v4.2.0)
- `residential_multifamily` subsystem: `status: draft` → `status: beta_rc`, version `0.5.0` → `0.6.0`.
- `.claude-plugin/plugin.json` version `4.1.2` → `4.2.0`.
- `.claude-plugin/marketplace.json` plugin version `4.1.2` → `4.2.0`.
- `src/catalog/catalog.yaml` plugin_version `4.1.2` → `4.2.0`.
- README "Release Maturity" row for residential_multifamily downgraded `Experimental` → `Beta RC`; Known Limitations refreshed to reflect period-seal and executive-output-contract coverage.
- Implementation hardening Obj 5 / 6 / 8 flipped from `deferred pass 2` to `done (pass 2)`; test totals ratcheted up.
- Installer scripts (`scripts/Install.ps1`, `scripts/install.sh`, `Install.command`) fallback version strings bumped to 4.2.0.
- Docs (`docs/INSTALL.md`, `docs/install-guide.md`, `docs/install-desktop.md`, `CONTRIBUTING.md`, `PRIVACY.md`) version banners and examples bumped to v4.2.0.
- `src/hooks/telemetry-init.mjs` default-config version and upgrade-backfill threshold bumped to 4.2.0.

### Fixed (plugin v4.2.0)
- `tests/test_catalog_claim_integrity.py::test_build_artifact_hook_prompts_match_catalog` now passes vacuously when the `builds/` directory is absent (fresh clones and CI). Previously asserted presence unconditionally, failing the test outside developer environments.
- `.gitleaks.toml` allowlists `src/skills/*/workflows/*/tools/test_*.py` so deliberate fake-secret fixtures in TUI scrubbing tests do not register as real secrets.

### Removed (plugin v4.2.0)
- Stale `docs/plans/build-system-refactor.md` and `docs/plans/residential-multifamily-refinement-2026-04-15.md` (completed-plan docs per release-hygiene validator).

### Security notes (plugin v4.2.0)
- All 4 hardening-pass-2 commits + 2 release-hygiene fixup commits signed via 1Password SSH (ED25519).
- Gitleaks, semgrep-cloud-platform/scan, secrets-scan all green on PR #31 (24/24 CI checks).
- No new dependencies added in this release.


### Added (residential_multifamily v0.5.0 - wave-5 stack completion + Yardi 2026-04-15)
- `reference/connectors/adapters/yardi_multi_role/` - Yardi adapter (multi-role posture). 43 files including `manifest.yaml` (multi-role mapping_hints across PMS/GL/CRM/reporting feeds, 17 known_gotchas), `classification_worksheet.md` (4-dimension operator decision: role / access path / operating pattern / data sensitivity), `bounded_assumptions.yaml` (14 assumptions with lifts_when), `provisional_source_contract.yaml` (21 entity families, all `requires_classification: true`), `source_contract.yaml` (organized by 7 Yardi sub-systems), `normalized_contract.yaml` with per-role precedence, `field_mapping.yaml`, `dq_rules.yaml` (29 rules `yd_` prefix), `reconciliation_rules.md` + `reconciliation_checks.yaml` (13 checks `yd_recon_` prefix; AppFolio cutover, Intacct parallel, Procore handoff, Dealpath post-IC, Excel, GraySail deferred), `edge_cases.md` (20 cases including legacy/parallel/historical), `crosswalk_additions.yaml` (10 crosswalks with effective_start + survivorship_rule + per-attribute source_of_record), `workflow_activation_additions.yaml` (role_by_classification for 6 existing + 10 proposed workflows), 11 `sample_raw/*.jsonl` + 11 `sample_normalized/*.jsonl`, 4 runbooks (classification_path, onboarding, common_issues, migration_to_appfolio), `tests/test_yardi_adapter.py` (15 tests), `README.md`.
- `_core/ontology.md` adds canonical `Commitment / PurchaseCommitment` object — buy-side contractual obligation with original_amount, approved_change_orders_amount, revised_amount, paid_to_date, retainage_held, balance_to_complete, status (draft|out_for_signature|executed|in_progress|complete|terminated|cancelled), funding_source, bonded, lien_waiver_required. Procore primary; Intacct posted-spend reconciliation; Yardi historical fallback. Guardrail: no `executed` transition without non-expired vendor insurance + bond where required.
- 9 new workflow packs under `workflows/`: `pipeline_review` (weekly Dealpath pipeline by stage), `pre_close_deal_tracking` (closing-checklist + key-date countdown), `investment_committee_prep` (pre-IC packet assembly with sensitivity tests), `acquisition_handoff` (deal-close → operating asset coordination across AppFolio + Intacct + vendor master), `post_ic_property_setup` (placeholder property/entity creation pre-close), `delivery_handoff` (Procore TCO → AppFolio operating activation + dev_project_crosswalk closure), `development_pipeline_tracking` (weekly Procore project rollup vs baseline), `lease_up_first_period` (monthly ramp tracking 6-18 months post-delivery), `executive_pipeline_summary` (monthly board-ready rollup of pipeline + capex commitment exposure). Each pack ships SKILL.md (frontmatter + body), reference_manifest.yaml, routing.yaml, change_log.md, examples/.
- Wave-5 fill of 7 wave-4 adapters (all reaching the 17-deliverable bar):
  - `appfolio_pms/`: 5 sample_raw + 5 sample_normalized JSONL files (work_orders, leads, applications, vendors, turns); `dq_rules.yaml` (26 rules `af_` prefix); `reconciliation_rules.md`; `reconciliation_checks.yaml` (13 checks `af_recon_`); `edge_cases.md` (12 cases); `crosswalk_additions.yaml`; `workflow_activation_additions.yaml`; `runbooks/appfolio_onboarding.md` + `appfolio_common_issues.md`; `tests/test_appfolio_adapter.py` (26 tests).
  - `sage_intacct_gl/`: 5 sample_raw + 5 sample_normalized JSONL files (actual_lines, budget_lines, forecast_lines, vendors, projects); `dq_rules.yaml` (23 rules `ic_` prefix); `reconciliation_rules.md`; `reconciliation_checks.yaml` (16 checks `ic_recon_`); `edge_cases.md` (15 cases); `crosswalk_additions.yaml`; `workflow_activation_additions.yaml`; `runbooks/sage_intacct_onboarding.md` + `sage_intacct_common_issues.md`; `tests/test_sage_intacct_adapter.py` (26 tests).
  - `procore_construction/`: 7 sample_raw + 7 sample_normalized JSONL files (projects, commitments, change_orders, draw_requests, schedule_milestones, vendors, cost_codes); `dq_rules.yaml` (21 rules `pc_` prefix); `reconciliation_rules.md` (5 cross-system sections including Procore↔Yardi delivery handoff); `reconciliation_checks.yaml` (13 checks `pc_recon_`); `edge_cases.md` (13 cases); `crosswalk_additions.yaml`; `workflow_activation_additions.yaml`; `runbooks/procore_onboarding.md` + `procore_common_issues.md`; `tests/test_procore_adapter.py` (17 tests).
  - `dealpath_deal_pipeline/`: full `source_contract.yaml`, `normalized_contract.yaml`, `field_mapping.yaml`; 6 sample_raw + 6 sample_normalized JSONL (deals, assets, deal_milestones, deal_key_dates, ic_decisions, deal_team); `reconciliation_rules.md`; `reconciliation_checks.yaml` (13 checks `dp_recon_`); `edge_cases.md` (15 cases); `crosswalk_additions.yaml` (asset, property_master, dev_project, market crosswalks); `runbooks/dealpath_onboarding.md` + `dealpath_common_issues.md`; `tests/test_dealpath_adapter.py` (11 tests).
  - `excel_market_surveys/`: 5 new template_schemas (vendor_rate_card, turn_cost_library, capex_cost_library, schedule_assumption, market_commentary); `normalized_contract.yaml` (11 canonical objects with `as_of_required: true`); `field_mapping.yaml`; 5 sample_valid CSVs + 3 sample_invalid CSVs; `dq_rules.yaml` (21 rules `ex_` prefix); `reconciliation_rules.md`; `reconciliation_checks.yaml` (12 checks `ex_recon_`); `edge_cases.md` (16 cases); `crosswalk_additions.yaml`; `workflow_activation_additions.yaml`; `runbooks/excel_onboarding.md` + `excel_common_issues.md`; `tests/test_excel_adapter.py` (13 tests).
  - `manual_sources_expanded/`: `file_family_registry.yaml` (12 file families); `normalized_contract.yaml`; 7 sample_files CSVs (TPM monthly, variance narrative, bid tab, approval matrix threshold, escalation log, payroll summary, manual property correction); `reconciliation_rules.md`; `reconciliation_checks.yaml` (15 checks `ms_recon_`); `edge_cases.md` (16 cases); `crosswalk_additions.yaml`; `runbooks/manual_sources_onboarding.md` + `manual_common_issues.md`; `tests/test_manual_sources_adapter.py` (8 tests).
  - `graysail_placeholder/`: `runbooks/graysail_classification_path.md` (operator decision tree with 8 checkpoints); `dq_rules.yaml` (10 deferred-mode rules `gs_` prefix, all severity warning until classification closes); `edge_cases.md` (10 cases); `workflow_activation_additions.yaml` (every workflow in `partial_mode_behavior: blocked_pending_classification`); `tests/test_graysail_adapter.py` (7 tests).
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml` - canonical tolerance-band registry referenced by every adapter `dq_rules.yaml` and `reconciliation_checks.yaml`. ~37 named bands (close_feed_lag, capex_posting, dev_handoff_lag, ledger_drift, occupancy_drift, etc.) with default_value, severity_below_band / severity_above_band, overridable_by overlay scopes. Closes a wave-3 reference gap surfaced by wave-4 adapters.
- `pyproject.toml` at repo root configures `pythonpath` so skill-local tests collect cleanly when pytest is invoked from project root. Closes the wave-3 conftest collection regression that forced developers to `cd src/skills/residential_multifamily/tests/` before running pytest.
- Wave-5 Yardi integration into registries: `vendor_family_registry.yaml` adds `yardi_multi_role` + `yardi_voyager_classified_template`; `source_registry/source_registry.yaml` adds 5 Yardi source records (`yardi_voyager_pms_stub`, `yardi_voyager_gl_stub`, `yardi_rentcafe_stub`, `yardi_data_connect_stub`, `yardi_legacy_export_stub`); `master_data/` crosswalks (property_master, unit, lease, vendor_master, account, capex_project, dev_project, asset, market, submarket, resident_account) gain Yardi rows with `effective_start: 2026-04-15` and `provenance: wave_5_yardi_adapter`.
- `_core/stack_wave4/source_of_truth_matrix.md` updated: `commitment` row no longer placeholder (canonical object now exists in ontology); Yardi precedence is operator-classified, with five role profiles (yardi_primary_operating, yardi_primary_accounting, yardi_primary_leasing_only, yardi_legacy_historical, yardi_parallel_partial) defining how Yardi displaces or co-exists with AppFolio / Intacct / Dealpath / Procore.

### Changed (residential_multifamily v0.5.0)
- `_core/ontology.md` - canonical objects: 32 → 33 (commitment added). Wave-5 is otherwise additive; no canonical metric, routing axis, or workflow-pack contract was modified.
- `tests/test_source_registry.py` ALLOWED_DOMAINS extended to include `deal_pipeline` (the wave-4 source domain that was added to the schema but not to the test guardrail).
- Adapter inventory: 15 → 16 (yardi_multi_role added). Workflow pack count: 26 → 35 (9 wave-5 packs added). Canonical objects: 32 → 33.

### Migration notes (residential_multifamily v0.5.0)
- Wave 5 is purely additive. Wave-4 adapters that referenced `commitment` as a placeholder canonical now resolve against the new ontology object; no rename required.
- Operators running pytest from project root no longer need to `cd` into `src/skills/residential_multifamily/tests/`. Existing skill-local test invocations continue to work.
- The new Yardi adapter ships at `status: stub` and is gated behind `yardi_multi_role/runbooks/yardi_classification_path.md`. No workflow trusts Yardi data until that classification closes for the operator's environment.
- Several tolerances cited by wave-4 adapter rules now resolve against `reference/normalized/schemas/reconciliation_tolerance_band.yaml`. Overlays may override per band via the `overridable_by` mechanism.

### Added (residential_multifamily v0.4.0 - stack-specific operationalization 2026-04-15)
- `reference/connectors/adapters/appfolio_pms/` - AppFolio PMS adapter. Manifest, source_contract, normalized_contract, field_mapping, mapping_template, sample_raw/ (properties, units, leases, lease_events, tenants, charges, payments), source_registry_entry, tests. Primary source for unit roster, lease, charge, payment, work order, vendor directory, leasing funnel; secondary for property and vendor master.
- `reference/connectors/adapters/sage_intacct_gl/` - Sage Intacct GL adapter. Manifest, source_contract, normalized_contract, field_mapping, sample_raw/ (chart_of_accounts, dimensions, journal_entries), source_registry_entry, tests. Primary for budget/forecast/actuals/variance; survives AppFolio for posted actuals after close.
- `reference/connectors/adapters/procore_construction/` - Procore construction adapter. Manifest, source_contract, normalized_contract, field_mapping, mapping_template, source_registry_entry, tests. Primary for construction project, commitments (placeholder), change orders, draws, schedule milestones; reconciles to Intacct on capex postings.
- `reference/connectors/adapters/dealpath_deal_pipeline/` - Dealpath deal-pipeline adapter. Manifest, README, dq_rules, workflow_activation_additions, source_registry_entry, tests. Primary source for pre-close deal state, IC milestones, deal team assignments, deal key dates. Seeds downstream AppFolio/Procore/Intacct setup.
- `reference/connectors/adapters/excel_market_surveys/` - Excel market-survey intake framework. Manifest, README, intake_manifest, 7 template_schemas (rent_comp, concession_tracker, market_survey_workbook, analyst_benchmark_pack, staffing_benchmark, labor_rate_sheet, material_price_sheet), source_registry_entry (5 file families), tests. Treats Excel as first-class production input with provenance, staleness, reviewer attestation.
- `reference/connectors/adapters/manual_sources_expanded/` - Expanded manual-source coverage for emailed files, shared-drive submissions, operator workbooks, approval matrices, TPM submissions, bid tabs. Manifest, README, dq_rules, workflow_activation_additions, source_registry_entry (4 file families), tests.
- `reference/connectors/adapters/graysail_placeholder/` - GraySail non-destructive integration stub pending classification. Manifest, README, classification_worksheet, bounded_assumptions, provisional_source_contract, workflow_relevance_map, source_registry_entry (status: planned), tests. Workflows blocked from treating GraySail as primary while placeholder.
- `reference/connectors/deal_pipeline/` - new vendor-neutral connector domain for deal pipeline data. Manifest, schema, mapping, sample_input, README. Backward-compatible enum extension to `source_registry.schema.yaml::source_domain`.
- `reference/connectors/_core/stack_wave4/` - cross-cutting wave-4 design docs: source_of_truth_matrix.md (48 canonical objects with primary/secondary/fallback + disagreement resolution), lifecycle_handoffs.md (8 explicit cross-system handoffs with payloads), stack_reconciliation_matrix.md (21 stack-level reconciliations), stack_rollout_wave4.md (4 sub-waves: 4A/4B/4C/4D), third_party_manager_oversight.md (3 TPM data scenarios + confidence flags), stack_test_taxonomy.md (16 test classes), open_questions_and_risks.md (14 items including ontology extensions).
- `reference/connectors/master_data/asset_crosswalk.yaml` - new crosswalk for canonical `asset` (Dealpath primary).
- `reference/connectors/master_data/market_crosswalk.yaml` - new crosswalk reconciling Excel broker naming with AppFolio internal slugs.
- `reference/connectors/master_data/submarket_crosswalk.yaml` - new crosswalk for submarket name reconciliation.
- `reference/connectors/source_registry/source_registry.yaml` - 14 wave-4 source entries merged from per-adapter fragments. Total registered sources: 13 -> 27.
- `tests/test_stack_wave4.py` - 69 wave-4 conformance tests (adapter directory presence, manifests carry wave_4 tag, source_registry merge integrity, GraySail status remains planned, PII classifications valid, no credential strings, deal_pipeline domain exists, cross-cutting docs present, new crosswalks present). All passing.

### Changed (residential_multifamily v0.4.0)
- `reference/connectors/source_registry/source_registry.schema.yaml` - `source_domain` enum extended to include `deal_pipeline`. Backward compatible.
- Adapter inventory grew from 8 vendor-neutral stubs to 8 stubs + 7 stack-specific adapters (appfolio_pms, sage_intacct_gl, procore_construction, dealpath_deal_pipeline, excel_market_surveys, manual_sources_expanded, graysail_placeholder). Total adapter directories: 8 -> 15.
- Wave-4 net test additions: 69 stack-specific + ~8 per adapter local tests added so far (additional adapter-local tests scheduled per `_core/stack_wave4/stack_test_taxonomy.md`).

### Migration notes (residential_multifamily v0.4.0)
- Wave 4 is purely additive. No canonical `_core/` object, metric, workflow, or routing axis was modified. Adding the `deal_pipeline` source domain extends the integration layer enum; not a canonical-base change.
- Several adapters carry incomplete content from this pass (sample data partial, some runbooks pending, reconciliation_rules.md / edge_cases.md / crosswalk_additions.yaml fragments not yet authored for every adapter). Tracked in `_core/stack_wave4/open_questions_and_risks.md`.
- Surfaces canonical extensions required for full sub-wave 4B operations: (1) `commitment` ontology object (Procore primary entity), (2) proposed new workflows (`pipeline_review`, `pre_close_deal_tracking`, `development_pipeline_tracking`, `acquisition_handoff`, `executive_pipeline_summary`, `investment_committee_prep`, `post_ic_property_setup`, `lease_up_first_period`, `delivery_handoff`).
- GraySail integration deferred behind `runbooks/graysail_classification_path.md` workflow; sub-wave 4C blocked until completion.

### Added (residential_multifamily v0.3.0 - operationalization pass 2026-04-15)
- `reference/connectors/source_registry/` - source inventory and system coverage matrix. 13 starter records spanning all 8 source domains plus planned entries. Includes schema, vendor family hints, implementation inventory.
- `reference/connectors/master_data/` - entity crosswalk framework covering property, unit, lease, resident, vendor, account, capex project, change order, draw request, employee, dev project. Identity resolution framework with canonical/source ID separation, confidence scoring, survivorship rules, effective dating. Manual overrides and unresolved exceptions queue.
- `reference/connectors/hr_payroll/` - HR/payroll/staffing connector stub with 8 entities (employee, staffing_position, role_assignment, property_assignment, vacancy_status, payroll_line, overtime_line, employee_vs_contractor_flag), PII-minimized sample payloads, reconciliation and DQ rules.
- `reference/connectors/manual_uploads/` - first-class manual/document/file-drop connector with 15 entity templates (budget, forecast, owner report, bid tab, rent survey, comp sheet, approval matrix, property list, staffing model, capex request, draw package, monthly review pack, delinquency report, work order backlog, pm scorecard) plus 16 file templates under `file_templates/`.
- `reference/connectors/_core/` - shared integration-layer docs: layer_design (raw/normalized/derived), lineage, normalization_patterns, field_mapping_template, raw_to_normalized_design, derived_dependencies, workflow_activation_map (YAML + MD), third_party_manager_oversight, exception_taxonomy, config_overlay_interaction, plus schemas for lineage_manifest, mapping_override_log, benchmark_update_log.
- `reference/connectors/_core/security/` - 15 security and privacy artifacts: security_model, pii_classification, secrets_handling, masking_and_redaction, config_templates, pii_sample_policy, fair_housing_controls, legal_hold_and_retention, audit_trail, unsafe_defaults_registry, approval_gates_for_integration_actions, least_privilege_guidance, config_overlay_interaction, security_testing_guidance.
- `reference/connectors/runbooks/` - 16 operational runbooks covering new source onboarding, schema change, missing file, stale feed, property crosswalk issue, unmapped account, benchmark refresh, failed normalization triage, exception queue review, manual override approval, cutover manual-to-system, connector deprecation, fair housing sensitive flag, financial control gate breach, schema drift escalation, reference rollback.
- `reference/connectors/monitoring/` - alert_policies (25), exception_routing (12 categories), observability_events (22), slo_definitions, alert_channel_design, escalation_matrix.
- `reference/connectors/rollout/` - 5-wave rollout plan, minimum viable data per workflow, pilot property guidance, go-live checklist, rollback plan, success metrics, post-launch monitoring cadence, cutover procedures, pilot-to-production gate.
- `reference/connectors/adapters/` - 8 vendor-family adapter stubs (pms, gl, crm, ap, market_data, construction, hr_payroll, manual_excel) with adapter_manifest schema, lifecycle doc, authoring guide, gotchas, vendor_family_registry.
- Shared QA library extended under `reference/connectors/qa/`: freshness_sla, referential_integrity, enum_conformance, temporal_monotonic, provenance_required, cross_source_reconciliation, reasonableness_band.
- Per-domain depth added to existing 6 connectors (pms, gl, crm, ap, market_data, construction): identity_resolution.md, dq_rules.yaml, reconciliation_rules.md, derived_dependencies.md, field_mapping.yaml. Reconciliation checks expanded from 27 total to 96 total.
- 7 new pytest modules: `test_source_registry.py`, `test_master_data_crosswalks.py`, `test_workflow_activation_map.py`, `test_runbook_structure.py`, `test_adapter_conformance.py`, `test_integration_security.py`, `test_integration_layer_presence.py`. Skill-local test count: 69 -> 103. Connector-local test count: 22 -> 89. Total: 91 -> 192.

### Changed (residential_multifamily v0.3.0)
- `reference/connectors/_schema/connector_manifest.schema.yaml` - `connector_kind` enum extended from 6 to 8 kinds (adds `hr_payroll`, `manual_uploads`). Backward compatible.
- `reference/connectors/_schema/reconciliation_check.schema.yaml` - optional template fields added (`parameters`, `severity_default`, `remediation_pattern`, `affected_workflows`) so shared qa templates validate cleanly.
- `tests/test_connector_contracts.py` - `REQUIRED_DOMAINS` extended to 8 (adds `hr_payroll`, `manual_uploads`).
- `hr_payroll/manifest.yaml` and `manual_uploads/manifest.yaml` - updated to declare their true `connector_kind` now that the canonical enum supports them.

### Migration notes (residential_multifamily v0.3.0)
- Integration-layer work extends `reference/connectors/` rather than creating a parallel `integrations/` tree. This preserves the existing BOUNDARIES.md layer contract. No canonical `_core/` object, metric, workflow, or routing axis was redefined.
- Directory rename `residential_multifamily` -> `residential-multifamily` is still deferred to a dedicated pass.

### Added (residential_multifamily v0.2.0 - refinement pass 2026-04-15)
- `overlays/regulatory/` overlay family — regulated affordable housing split into its own family, separate from conventional market-positioning segments. Starter stubs for 6 programs (lihtc, hud_section_8, hud_202_811, usda_rd, state_program, mixed_income) plus 9 shared compliance surfaces (eligibility, income limits, rent limits, UA, recertification, compliance calendar, agency reporting, file audit, escalation sensitivity). No program-specific schedules populated; architecture only.
- `reference/connectors/` vendor-neutral ingestion layer with stubs for 6 source domains (pms, gl, crm, ap, market_data, construction). Each connector: manifest, schema (47 entities across all 6), mapping template, sample input / normalized, reconciliation checks, tests. Reference-layer QA checks under `qa/` for record_count, duplicate_id, null_critical_field, date_coverage, unit_count_reconciliation, lease_status_reconciliation, budget_actual_alignment, commitment_change_order_draw.
- `_core/BOUNDARIES.md` — canonical boundary document: what lives in core, segment, regulatory, market, org layers. Enforced by `tests/test_boundary_rules.py`.
- `_core/routing/axes.yaml` — new `regulatory_program` axis with values `[none, lihtc, hud_section_8, hud_202_811, usda_rd, state_program, mixed_income]`. Default `none`. Additive; existing packs require no change.
- `_core/routing/rules.yaml` — two new rules: r011 (explicit regulatory workflow invocation) and r012 (defensive guard: never auto-load regulatory overlays for conventional segment routes).
- `tailoring/AUDIENCE_MAP.md`, `tailoring/DIFF_APPROVAL_PREVIEW.md`, `tailoring/MISSING_DOC_MATRIX.md` — canonical tailoring specs.
- `tailoring/question_banks/executive.yaml`, `finance_reporting.yaml`, `compliance_risk.yaml`, `site_ops.yaml` — 8-audience split.
- 4 new pytest modules: `test_regulatory_isolation.py`, `test_connector_contracts.py`, `test_tailoring_canonical_immutability.py`, `test_boundary_rules.py`.

### Changed (residential_multifamily v0.2.0)
- `overlays/segments/` now holds conventional market-positioning only (`middle_market` + `luxury`). `overlays/segments/affordable/` retained with a deprecation banner and migration pointer to `overlays/regulatory/affordable/`.
- `_core/routing/axes.yaml` — `segment` values narrowed from `[middle_market, affordable, luxury]` to `[middle_market, luxury]`; legacy `affordable` value accepted for one cycle as a migration alias that prompts the user for `regulatory_program` and retries routing.
- `_core/schemas/overlay_manifest.yaml` — additively extended to support `overlay_kind: regulatory` and `regulatory.program`; adds optional `parent_overlay`, `scope.regulatory_program`, `scope.jurisdiction`, and top-level `status` enum. Pre-existing overlays validate without modification.
- `_core/DESIGN_RULES.md` — Rule 6 hierarchy updated to surface `regulatory_program` as a distinct axis from `segment`.
- `_core/naming_conventions.md` — adds "Directory-slug exception for subsystem roots" (documents the snake_case subsystem-root exception to the repo's kebab-case skill convention) and "Segment vs regulatory program" section.
- `tailoring/SKILL.md` — `references.reads` extended; "Templates used" section updated to enumerate the 8-bank layout.
- `tailoring/question_banks/coo.yaml`, `cfo.yaml`, `reporting.yaml` — retained with top-of-file deprecation banners pointing at `executive.yaml` / `finance_reporting.yaml`.

### Deprecated (residential_multifamily)
- `overlays/segments/affordable/` — use `overlays/regulatory/affordable/`. Old path retained with `DEPRECATED.md` stub for one refinement cycle to catch late-migrating callers.
- `tailoring/question_banks/coo.yaml`, `cfo.yaml`, `reporting.yaml` — use `executive.yaml` and `finance_reporting.yaml`. Retained for resume of in-flight sessions.

### Migration notes (residential_multifamily)
- Any `reference_manifest.yaml` reading `overlays/segments/affordable/` should update the path to `overlays/regulatory/affordable/`. Old path continues to resolve for one cycle.
- Any callsite using axis value `segment: affordable` should set `segment` to `middle_market` or `luxury` (conventional positioning) and set `regulatory_program` to the relevant program (or `none`). The router detects the legacy value and prompts.
- The residential multifamily subsystem directory is NOT renamed to `residential-multifamily` in this pass. Tracked for a dedicated ticket.
- Skill status remains `draft`; no top-level plugin version bump. The `residential_multifamily` catalog entry is re-synchronized to `status: draft` (was `stable` — mismatch with SKILL.md fixed).

### Added
- `residential_multifamily` skill — institutional-grade operating system for U.S. residential multifamily property management (534 files, 35,920 lines). Covers the full operating stack:
  - `_core/`: ontology (30+ objects), 72 metric contracts, routing framework with 3 worked examples, 20-action approval matrix, fair-housing + safety guardrails, alias registry
  - `roles/`: 15 role packs (property manager flagship; asset manager, TPM-oversight-lead, reporting/finance-ops at same depth; COO/CFO/CEO as rollup consumers)
  - `workflows/`: 26 workflows with 6 flagships (delinquency_collections, monthly_asset_management_review, bid_leveling_procurement_review, draw_package_review, TPM_scorecard_review, executive_operating_summary_generation)
  - `overlays/`: segment (middle_market deep + affordable/luxury/high_rise stubs), form_factor x6, lifecycle x6, management_mode x3
  - `reference/`: 16 category schemas, ~250 starter CSV rows (all tagged sample/starter/placeholder), 16 update-flow walk-throughs
  - `templates/`: 40 templates with legal-review banners on statutory-notice templates
  - `tailoring/`: interactive TUI (stdlib + PyYAML, ANSI, session persistence, resume), 7 audience question banks with 124 questions, 23 unit tests
  - `tests/`: 12 pytest modules, 40/40 pass — enforces no-hardcoded-figures, metric-contract uniqueness, approval gating, fair-housing banners, naming collisions
- Skill ships with `status: draft` and self-declared stale-data notice — all reference files are tagged `sample | starter | illustrative | placeholder`, update before operational use

### Changed
- Skills count: 112 -> 113 (propagated via `scripts/catalog-build.py` and `scripts/catalog-generate.py` to README stats table, plugin.json description, registry.yaml, hooks SessionStart prompt, routing table)
- Prose counts in README, docs/INSTALL.md, docs/install-cowork.md, docs/install-desktop.md, docs/WHAT-TO-USE-WHEN.md, docs/install-guide.md updated to 113 (historical release notes under docs/releases/ left unchanged)

### Added (CI)
- `scripts/prose-drift-check.py` — grep-based CI guard that flags hardcoded skill/agent/calculator/reference-file counts in prose outside the `CATALOG:STATS` markers. Wired into `.github/workflows/ci.yml` so future skill additions fail CI until every current-state doc is updated or explicitly wrapped in `<!-- PROSE-DRIFT:IGNORE-START -->` / `<!-- PROSE-DRIFT:IGNORE-END -->` markers. Closes the gap the generator never covered (14 stale "112" references in prose surfaced during this merge).

### Notes
- No version bump in this entry — the skill status is `draft`, version should bump when the subsystem moves to `deployed`

## [4.1.2] - 2026-04-13

### Added
- Install docs for Codex, Gemini, Grok, Manus targets
- Cosign verification steps per target
- Non-technical quickstart section in `docs/INSTALL.md`

### Changed
- Collapsed checksum/signing details into developer-only details blocks

### Notes
- Doc-only release; no plugin behavior changes

## [4.1.1] - 2026-04-02

### Added
- Desktop and portable zip build targets in `release.yml`
- Source archives attached to each release
- Cosign signing for all release artifacts
- Consolidated `SHA256SUMS` across targets

### Changed
- Release workflow produces 4 platform targets per tag (macOS DMG, Windows EXE, desktop zip, portable zip)

## [4.1.0] - 2026-04-02

### Added
- Same-repo marketplace install path
- Cowork install guidance (Desktop zip upload flow)
- Structured installer telemetry (install start, success, failure, edge cases)

### Fixed
- `/doctor` now recognizes the plugin (`plugin.json` moved to repo root)
- Windows installer verification and plugin cache layout
- PS1 installer: step-by-step progress and structured error reporting

## [4.0.0] - 2026-04-02

### Added
- MCP server (src/mcp-server.mjs): zero-dependency stdio JSON-RPC server with 8 tools
  (cre_route, cre_list_skills, cre_skill_detail, cre_workspace_create/get/list/update,
  cre_send_feedback) for Claude Desktop visibility
- Feedback retry outbox (src/hooks/feedback-outbox.mjs): failed remote submissions are
  queued in ~/.cre-skills/outbox.jsonl and retried on next session start (4s timeout
  per request, max 5 attempts before eviction)
- Canonical catalog system: src/catalog/catalog.yaml as single source of truth for all
  plugin metadata (196 items: 105 skills, 54 agents, 9 commands, 12 calculators,
  10 orchestrators, 6 workflows)
- Catalog schema: src/catalog/catalog.schema.json
- Build script: scripts/catalog-build.py (scan repo -> catalog.yaml + dist/catalog.json)
- Generator script: scripts/catalog-generate.py (catalog -> README, hooks, plugin.json,
  routing, registry)
- Catalog-driven router: src/routing/skill-dispatcher.mjs now reads dist/catalog.json with
  artifact-aware matching, confidence scoring, downstream recommendations, and markdown fallback
- Output styles: src/templates/output-styles/ with 5 format templates (exec-brief, ic-memo,
  pm-action-list, lender-brief, lp-update)
- userConfig in plugin.json: primary_asset_types, preferred_markets, default_output_style,
  feedback_mode, brand_name
- ADR: docs/adr/0001-catalog-source-of-truth.md
- Migration guide: docs/MIGRATION.md
- Release checklist: docs/release-checklist.md
- Workspace entrypoints: 7 top-level skills (deal-intake, lease-strategy-papering,
  asset-ops-cockpit, capital-projects-development, fund-lp-reporting, navigator, plugin-admin)
- Persistent workspace state: local JSON storage for session continuity
- Next-best-action footer: mandatory structured output for workspace skills

### Changed
- Build system refactor: all source content (skills, agents, commands, hooks, routing,
  orchestrators, calculators, lib, catalog, MCP server, templates) moved from repo root
  into `src/`. Symlinks removed. `scripts/`, `docs/`, `tests/`, `dist/`, `registry.yaml`,
  and `README.md` remain at repo root. Build output goes to `builds/`.
- Feedback default mode: ask_each_time -> local_only (privacy-first)
- Feedback backend_url default: pre-configured -> empty (opt-in remote submission)
- registry.yaml: manually maintained -> generated from catalog
- Router: markdown-table parsing -> catalog-driven with fallback
- README Key Stats: hardcoded -> generated from catalog (18 categories)
- Plugin version: 3.0.0 -> 4.0.0
- Telemetry now enabled by default (opt-out model). Records only skill slug +
  date + anonymous UUID. No deal data, financials, prompts, or identity.
  All data stays local at ~/.cre-skills/telemetry.jsonl
- First-run notice clearly explains what is and is not tracked, and how to opt out
- Windows installer registers in ~/.claude/ plugin system instead of
  %APPDATA%\Claude\skills\
- Stale doc references: added notices to USER-GUIDE.md for unimplemented CLI scripts

### Fixed
- PRIVACY.md: claimed remote submission was "Future -- Not Available Yet" when code
  had it active by default. Now accurately describes it as available but opt-in.
- docs/feedback-system.md: contradicted itself on default feedback mode
- feedback-summary command: now reads both feedback.jsonl and feedback-log.jsonl
- Hooks.json SessionStart prompt: counts now generated from catalog
- Windows Desktop not seeing installed plugin (wrong install directory)

## [3.0.0] - 2026-04-01

### Added
- Feedback system: /cre-skills:send-feedback and /cre-skills:report-problem commands for
  structured feedback intake without leaving the session
- Remote feedback submission via Vercel Function + Supabase backend at
  cre-skills-feedback-api.vercel.app (default mode: ask_each_time, user confirms each send)
- Automatic redaction of file paths, emails, digit sequences, and env vars from feedback
  text before storage (scripts/redact-feedback.mjs, 38 behavioral tests)
- Weekly feedback prompt: non-intrusive reminder at session end after 7+ days of use,
  shown once per 7 days, only when CRE skills were used in the session
- Feedback schemas: feedback-submission.schema.json, feedback-config.schema.json
- Architecture documentation: docs/feedback-system.md
- 38 redaction tests (tests/test-redaction.mjs) + 4 new structural integrity tests
- firstRunAt timestamp tracking for install age calculation

### Changed
- Total commands: 7 -> 9 (added send-feedback, report-problem)
- Config model: added feedback block (mode, include_context, backend_url, last_prompt_shown_at)
- hooks/hooks.json: SessionStart prompt updated with new commands
- hooks/telemetry-init.mjs: feedback config initialization + backfill for existing installs
- hooks/session-summary.mjs: weekly feedback prompt logic
- PRIVACY.md: documented structured feedback data flow, redaction rules, remote submission
- README.md: feedback section, updated stats (9 commands), project structure

## [2.5.0] - 2026-03-28

### Added
- construction-cost-estimator: full CSI MasterFormat cost estimation with 11 workflows including
  visual input (floor plans/drawings), generative output (ASCII mockups), and co-creation design
  loops. Includes construction_estimator.py calculator (zero dependencies), 925-line CSI cost
  database, 60+ city regional cost factors, and soft cost benchmarks reference.
- property-management-orchestrator: deep PM command center with 10 workflows across all asset
  types. Routes to downstream skills (building-systems, work-order-triage, PM operations, etc.).
  Includes 8 asset-type module stubs (multifamily through hospitality) for v3.0 deep-dive,
  IREM/BOMA KPI benchmarks, monthly report template, and vendor management framework.
- space-planning-redesign-orchestrator: multi-agent orchestrator for space redesign ideation
  with 5 specialist subagents (space programmer, design visualizer, cost estimator, market
  validator, ROI analyst). Includes amenity cost benchmarks, tenant survey templates,
  competitive audit framework, and ROI model template. Status: stub (full orchestration in v3.0).
- Windows .exe installer via Inno Setup (no admin privileges, auto-detects Claude Code + Desktop)
- GitHub Actions workflow for building Windows installer on windows-latest runner
- 12th Python calculator: construction_estimator.py

### Changed
- Total skills: 99 -> 105 (6 new)
- Total reference files: 225 -> 247 (22 new)
- routing/CRE-ROUTING.md updated with 3 new skill routing triggers
- hooks/hooks.json SessionStart prompt updated to 102 skills, 55 agents
- Install.ps1 added for Windows post-install configuration

## [2.0.0] - 2026-03-25

### Added
- 19 new skills (total: 99 skills): title-commitment-reviewer, tenant-credit-analyzer,
  term-sheet-builder, loan-document-reviewer, transfer-document-preparer, funds-flow-calculator,
  lease-option-structurer, lease-trade-out-analyzer, gp-performance-evaluator, fund-terms-comparator,
  lp-data-request-generator, sec-reg-d-compliance, monte-carlo-return-simulator,
  property-management-operations, distribution-notice-generator, 1031-pipeline-manager,
  deal-attribution-tracker, emerging-manager-evaluator, fund-raise-negotiation-engine
- 11 Python calculator scripts (zero dependencies): debt_sizing, covenant_tester, npv_trade_out,
  option_valuation, proration_calculator, quick_screen, tenant_credit_scorer, transfer_tax,
  waterfall_calculator, monte_carlo_simulator, fund_fee_modeler
- Orchestration engine: 10 multi-agent pipelines (acquisition, capital-stack, hold-period,
  disposition, development, fund-management, research, strategy, portfolio, lp-intelligence)
  with 10 JSON configs, 16 prompt files, 8 investor profiles, strategy matrix, challenge layer,
  disagreement/reversal schemas, and cross-chain handoff registry
- 14 lifecycle agents across research, strategy, asset-management, portfolio, fund, disposition,
  and LP intelligence categories (total: 54 agents)
- 225 reference files (up from 171 in v1.0.0)
- Brand guidelines system: auto-loads from ~/.cre-skills/brand-guidelines.json for 8 deliverable skills
- PostToolUse hook (telemetry-capture.mjs) -- tracks skill invocations when telemetry is opt-in
- Stop hook (session-summary.mjs) -- writes session_end record and optional feedback prompt
- telemetry-init.mjs SessionStart hook -- initializes ~/.cre-skills/config.json on first run
- 4 new commands: brand-config, orchestrate, usage-stats, feedback-summary (total: 7 commands)
- scripts/update.sh -- pulls latest, handles major version migration, preserves user data
- scripts/uninstall.sh -- clean removal with user data preservation prompt
- scripts/verify-install.sh -- full health check (skills, refs, calculators, hooks, data dir)
- docs/install-guide.md -- comprehensive installation guide for all platforms
- PRIVACY.md, SECURITY.md

### Changed
- License changed from MIT to Apache 2.0 (adds explicit patent grant)
- NOTICE file added for Apache 2.0 compliance with Avi Hacker attribution
- scripts/install.sh updated for v2: Node.js/Python checks, v1->v2 migration, backup, calculators
- Install.command version string updated to v2.0.0
- README.md rewritten for v2.0.0 with full skill catalog, workflow chains, calculators, brand guidelines
- hooks/telemetry-capture.mjs: replaced /dev/stdin with fd 0 for Windows WSL compatibility
- verify-install.sh: counts all reference files (*.md + *.yaml), not just *.md


### Breaking Changes
- License: MIT -> Apache 2.0. Existing installations continue to function; license governs
  redistribution and use going forward.

---

## [1.0.0] - 2026-03-17

### Added
- 80 CRE skill packs across 16 subcategories
- 171 reference files (formulas, templates, frameworks, worked examples)
- 40 expert subagent definitions across 8 categories
- 6 workflow chain documents
- 3 plugin commands (cre-route, cre-workflows, cre-agents)
- SessionStart hook for context-efficient routing
- Machine-readable skill registry (registry.yaml)
- CRE routing index for skill discovery
- MIT license
