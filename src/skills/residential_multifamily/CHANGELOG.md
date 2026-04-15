# Residential Multifamily Subsystem — Changelog

## 0.5.0 — 2026-04-15 — Wave-5 stack completion + Yardi multi-role adapter

### Added

- **Yardi multi-role adapter** at `reference/connectors/adapters/yardi_multi_role/` (43 files): manifest + classification_worksheet + bounded_assumptions + provisional_source_contract + source_contract + normalized_contract + field_mapping + dq_rules (29 `yd_` rules) + reconciliation_rules + reconciliation_checks (13 `yd_recon_`) + edge_cases + crosswalk_additions (10 crosswalks) + workflow_activation_additions + 11 sample_raw + 11 sample_normalized JSONL + 4 runbooks + tests + README. Multi-role posture: PMS / GL / CRM / reporting / legacy historical, all gated behind `runbooks/yardi_classification_path.md`.
- **Canonical `Commitment / PurchaseCommitment` object** in `_core/ontology.md` (Procore primary entity). 33 canonical objects total (was 32). Includes status enum, retainage / commitment-balance fields, vendor-insurance guardrail.
- **9 new workflow packs** under `workflows/`: pipeline_review, pre_close_deal_tracking, investment_committee_prep, acquisition_handoff, post_ic_property_setup, delivery_handoff, development_pipeline_tracking, lease_up_first_period, executive_pipeline_summary. Each ships SKILL.md + reference_manifest + routing + change_log + examples/. Total workflow packs: 35 (was 26).
- **Wave-5 fill of 7 wave-4 adapters** (each reaches the 17-deliverable bar): appfolio_pms, sage_intacct_gl, procore_construction, dealpath_deal_pipeline, excel_market_surveys, manual_sources_expanded, graysail_placeholder. Adds dq_rules.yaml, reconciliation_rules.md, reconciliation_checks.yaml, edge_cases.md, crosswalk_additions.yaml, workflow_activation_additions.yaml, runbooks, sample data, and per-adapter test suite. Per-adapter rule_id prefixes: `af_`, `ic_`, `pc_`, `dp_`, `ex_`, `ms_`, `gs_`.
- **`reference/normalized/schemas/reconciliation_tolerance_band.yaml`** — canonical tolerance-band registry (37 bands) referenced by every adapter dq_rules and reconciliation_checks. Closes a wave-3 reference gap.
- **`pyproject.toml`** at repo root configures `pythonpath` so skill-local tests collect cleanly when pytest is invoked from project root. Closes the wave-3 conftest collection regression.
- **Yardi registry wiring**: vendor_family_registry adds yardi_multi_role + 7 wave-4 adapter records; source_registry adds 5 Yardi source records; master_data crosswalks gain Yardi rows across property_master, unit, lease, vendor_master, account, capex_project, dev_project, asset, market, submarket, resident_account.
- **Wave-5 metric additions**: `_core/metrics.md` adds 68 proposed metrics across pipeline / pre-close / IC / handoff / development extension / lease-up extension / portfolio summary families. Each marked status: proposed for promotion in next operationalization cycle.
- **9 new workflow_activation_map.yaml entries** + companion section in workflow_activation_map.md.
- **`tests/test_stack_wave5.py`** — 72 wave-5 conformance tests covering Yardi adapter, commitment object, 9 workflow packs, tolerance band schema, conftest fix.

### Changed

- `_core/schemas/skill_manifest.yaml` enums extended (additive only): `applies_to.lifecycle` adds `pre_acquisition` and `disposition`; `applies_to.output_types` adds `handoff_checklist`, `ic_packet`, `pipeline_summary`.
- `_core/schemas/reference_manifest.yaml` enums extended (additive only): `reads.fallback_behavior` adds `proceed_with_default`; `writes.write_mode` adds `propose_then_approve` (handoff workflows propose crosswalk row writes pending approval).
- `_core/stack_wave4/source_of_truth_matrix.md` — `commitment` row is no longer a placeholder (canonical object now exists); Yardi precedence is operator-classified per 5 role profiles.
- `tests/test_source_registry.py` ALLOWED_DOMAINS adds `deal_pipeline`; `tests/test_workflow_activation_map.py` ALLOWED_DOMAINS adds `deal_pipeline`; `tests/test_adapter_conformance.py` splits EXPECTED_ADAPTER_DIRS into LEGACY + STACK lists with layout-aware file checks.
- `reference/connectors/adapters/_test_helpers.py` `run_adapter_manifest_checks()` is now layout-aware: legacy stubs validate against full schema + single-file payload pattern; stack-specific adapters spot-check required-id fields + multi-file sample directories.

### Migration notes

- Wave 5 is purely additive. Wave-4 adapters that referenced `commitment` as a placeholder canonical now resolve against the new ontology object; no rename required.
- Operators running pytest from project root no longer need to `cd` into the skill tests dir.
- Yardi adapter ships at `status: stub` and is gated behind `yardi_multi_role/runbooks/yardi_classification_path.md`. No workflow trusts Yardi data until that classification closes for the operator's environment.
- All 244 skill-level tests pass; 231 connector-level tests pass; 475 total.

### Known follow-ups (deferred to wave 6)

- Promote wave-5 proposed metrics from `proposed` to `canonical` status as operationalization run completes.
- `commitment_crosswalk.yaml` has not yet been carved out as a dedicated file in `master_data/`; commitment crosswalk rows currently live inline on adapter `crosswalk_additions.yaml` files.
- Directory rename `residential_multifamily` -> `residential-multifamily` remains deferred; wave-5 did not address.
- GraySail adapter remains classification-pending; operator must complete `yardi_multi_role/runbooks/graysail_classification_path.md`.

## 0.1.0 — 2026-04-15 — Phase 1 foundation

Initial subsystem scaffold.

### Added

- Canonical `_core/` layer: taxonomy, ontology, metric contracts, routing framework, approval matrix, guardrails, naming conventions, change-log conventions, alias registry, schemas.
- Role packs under `roles/` (16 roles covering site through executive).
- Workflow packs under `workflows/` (24 workflows across operations, finance, development, construction, TPM oversight, executive).
- Overlays: middle-market segment (full depth), affordable + luxury stubs, form factor overlays, lifecycle overlays, management mode overlays.
- Reference schemas + starter CSVs across 16 reference categories; all starter data tagged `status: sample | starter | illustrative | placeholder`.
- Templates covering operating, reporting, construction, TPM oversight, resident communications.
- Tailoring skill with interactive terminal UI pattern, question bank, org overlay builder, missing-docs queue.
- Test suite validating reference manifests, metric completeness, no-hardcoded-figures, routing, naming, rendering.

### Not yet included

- Live market data.
- Deep affordable / LIHTC / HUD compliance logic (stubbed only).
- Deep luxury / high-rise logic (stubbed only).
- Student, senior, BTR, mixed-use residential overlays.
- International markets.
