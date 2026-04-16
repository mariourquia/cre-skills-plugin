# Next Session Handoff

## 2026-04-15 residential_multifamily wave-5 stack completion + Yardi (v0.5.0)

Wave 5 closes the wave-4 content gaps, introduces the Yardi multi-role adapter, adds the canonical `commitment` object, ships 9 deal-pipeline / handoff / lease-up / executive workflow packs, and creates the `reconciliation_tolerance_band.yaml` schema. All 475 tests pass (244 skill + 231 connector).

### What landed (v0.5.0)

**Yardi multi-role adapter** at `reference/connectors/adapters/yardi_multi_role/` (43 files). Multi-role posture (PMS / GL / CRM / reporting / legacy historical), gated behind `runbooks/yardi_classification_path.md`. 29 dq rules with `yd_` prefix, 13 reconciliation checks `yd_recon_`, 10 crosswalk additions, 11 sample_raw + 11 sample_normalized JSONL files, 4 runbooks. Status: stub until operator classification closes.

**Canonical `Commitment / PurchaseCommitment`** added to `_core/ontology.md`. 33 canonical objects total (was 32). Procore primary, Intacct posted-spend reconciliation, Yardi historical fallback. Source-of-truth matrix updated to remove placeholder marking.

**9 new workflow packs** under `workflows/`: `pipeline_review`, `pre_close_deal_tracking`, `investment_committee_prep`, `acquisition_handoff`, `post_ic_property_setup`, `delivery_handoff`, `development_pipeline_tracking`, `lease_up_first_period`, `executive_pipeline_summary`. Total workflow packs: 35 (was 26).

**Wave-5 fill of 7 wave-4 adapters** to the 17-deliverable bar: appfolio_pms (af_), sage_intacct_gl (ic_), procore_construction (pc_), dealpath_deal_pipeline (dp_), excel_market_surveys (ex_), manual_sources_expanded (ms_), graysail_placeholder (gs_). Each gains dq_rules + reconciliation_rules + reconciliation_checks + edge_cases + crosswalk_additions + workflow_activation_additions + per-adapter test suite.

**Reference / schema additions:**
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml` — 37+ named tolerance bands cited across all dq_rules and reconciliation_checks (closes wave-3 reference gap).
- `_core/metrics.md` adds 68 wave-5 proposed metrics across pipeline / pre-close / IC / handoff / development extension / lease-up extension / portfolio summary families.
- `_core/schemas/skill_manifest.yaml` enums extended (additive): `applies_to.lifecycle` += `pre_acquisition`, `disposition`; `applies_to.output_types` += `handoff_checklist`, `ic_packet`, `pipeline_summary`.
- `_core/schemas/reference_manifest.yaml` enums extended (additive): `reads.fallback_behavior` += `proceed_with_default`; `writes.write_mode` += `propose_then_approve`.

**Yardi registry wiring:**
- `vendor_family_registry.yaml` adds yardi_multi_role + 7 wave-4 adapters.
- `source_registry.yaml` adds 5 Yardi source records (yardi_voyager_pms_stub, yardi_voyager_gl_stub, yardi_rentcafe_stub, yardi_data_connect_stub, yardi_legacy_export_stub).
- `master_data/` crosswalks gain Yardi rows (property_master, unit, lease, vendor_master, account, capex_project, dev_project, asset, market, submarket, resident_account).

**Test infrastructure:**
- `pyproject.toml` at repo root configures `pythonpath` (closes wave-3 conftest collection regression).
- `tests/test_stack_wave5.py` — 72 wave-5 conformance tests.
- `_test_helpers.py::run_adapter_manifest_checks` is now layout-aware (legacy single-file pattern vs wave-4/5 multi-file directory pattern).
- `test_adapter_conformance.py` splits EXPECTED_ADAPTER_DIRS into LEGACY_ADAPTER_DIRS + STACK_ADAPTER_DIRS with layout-aware file checks.

### Pending wave-5 work (next-session priorities — wave 6)

1. **Promote 68 proposed metrics from `proposed` to canonical status.** Each wave-5 metric in `_core/metrics.md` ships at `status: proposed`. Operationalization run should validate band semantics, source feed reconciliation, and target band per overlay before promotion. `alias_registry.yaml` updates required when promoted.

2. **Carve out `commitment_crosswalk.yaml` in `master_data/`.** Wave-5 commitment crosswalk rows currently live inline on adapter `crosswalk_additions.yaml` files (procore, intacct, yardi). Promote to a dedicated crosswalk file when first non-procore commitment source goes live.

3. **Directory rename `residential_multifamily` -> `residential-multifamily`.** Long-standing deferred item. Touches conftest.py SUBSYS assertion, pyproject.toml pythonpath, src/catalog/catalog.yaml id + source_path, registry.yaml, every reference_manifest.yaml that path-references the subsystem. Keep as standalone PR: high-churn, pure rename, zero behavioral change. Update memory notes after.

4. **Yardi classification operationalization.** `yardi_multi_role/runbooks/yardi_classification_path.md` is the operator decision tree. Until an operator closes classification for their environment, no workflow trusts Yardi as primary. Once closed, fork yardi_multi_role into role-specific adapter (e.g. yardi_primary_pms, yardi_legacy_historical) and advance status to starter.

5. **GraySail classification operationalization.** Same pattern as Yardi but blocked at an earlier stage. Operator must complete `yardi_multi_role/runbooks/graysail_classification_path.md` (file present, operator input pending). Workflows referencing GraySail run in `partial_mode_behavior: blocked_pending_classification` until then.

6. **Workflow activation map maintenance.** When new workflows arrive, update both `_core/workflow_activation_map.yaml` (machine-readable) and `_core/workflow_activation_map.md` (companion). Wave-5 added 9; wave-6 should follow same pattern.

### Earlier deferred items (still applicable)

The v0.4.0 / v0.3.0 deferred-items list below remains relevant; wave-5 closed the 4 highest-priority adapter content gaps but did not address LIHTC/HUD schedules, luxury segment depth, tailoring TUI 8-audience wiring, compliance workflows, jurisdiction overlays, approval-matrix threshold validation, fair-housing linter, or canonical-metric promotion of `insurance_expiry_exposure`.

---

## 2026-04-15 residential_multifamily wave-4 stack-specific operationalization (v0.4.0)

Wave 4 wired AppFolio, Sage Intacct, Procore, Dealpath, Excel market surveys,
GraySail (placeholder), and expanded manual sources into the canonical
residential_multifamily skill. The vendor-neutral wave-3 framework is
respected — no canonical metric, ontology object, or routing axis was
modified. A new `deal_pipeline` source domain was added (additive enum
extension only).

### What landed (v0.4.0)

**7 new stack-specific adapters** under `src/skills/residential_multifamily/reference/connectors/adapters/`:

| Adapter | Domain | Status | Coverage |
|---|---|---|---|
| `appfolio_pms` | pms | stubbed | property, unit, lease, charge, payment, work_order, vendor, leasing funnel |
| `sage_intacct_gl` | gl | stubbed | budget, forecast, actuals, variance, capex, vendor, dimensions |
| `procore_construction` | construction | stubbed | project, commitment (placeholder), CO, draw, schedule, vendor |
| `dealpath_deal_pipeline` | deal_pipeline (new) | stubbed | deal, asset, IC milestones, deal team, key dates |
| `excel_market_surveys` | market_data | active | rent comps, concessions, capex cost library, staffing, labor (5 file families) |
| `manual_sources_expanded` | manual_uploads | active | TPM submissions, operator monthly reports, bid tabs, approval matrix (4 file families) |
| `graysail_placeholder` | other | planned | non-destructive stub pending classification |

**Cross-cutting wave-4 docs** under `reference/connectors/_core/stack_wave4/`:

- `source_of_truth_matrix.md` (48 canonical objects mapped)
- `lifecycle_handoffs.md` (8 explicit handoffs with synthetic payloads)
- `stack_reconciliation_matrix.md` (21 stack-level reconciliations)
- `stack_rollout_wave4.md` (4 sub-waves: 4A/4B/4C/4D)
- `third_party_manager_oversight.md` (TPM scenarios + confidence flags)
- `stack_test_taxonomy.md` (16 test classes)
- `open_questions_and_risks.md` (14 items)

**New crosswalks** under `reference/connectors/master_data/`:

- `asset_crosswalk.yaml` (Dealpath primary)
- `market_crosswalk.yaml` (Excel↔AppFolio reconciliation)
- `submarket_crosswalk.yaml`

**Source registry**: 14 wave-4 entries merged. Total: 13 → 27 source records.

**Tests**: `tests/test_stack_wave4.py` adds 69 wave-4 conformance tests. All passing
(`cd src/skills/residential_multifamily/tests && python3 -m pytest test_stack_wave4.py`).
Pre-existing wave-3 import path issue (top-level pytest collection fails for skill-level
tests that import `from conftest import SUBSYS`) is unchanged — unrelated to wave-4.

### Pending wave-4 work (next session priorities)

The wave-4 implementation pass was time-constrained. Several adapters carry partial content. Highest-value gaps to close:

1. **Adapter sample data completeness** — 5 of 7 adapters are missing full `sample_raw/` and `sample_normalized/` coverage. Intended target per adapter:
   - `appfolio_pms`: add `work_orders.jsonl`, `leads.jsonl`, `applications.jsonl`, `vendors.jsonl`, `turns.jsonl` to sample_raw + complete sample_normalized
   - `sage_intacct_gl`: add `actual_lines.jsonl`, `budget_lines.jsonl`, `forecast_lines.jsonl`, `vendors.jsonl`, `projects.jsonl` to sample_raw + complete sample_normalized
   - `procore_construction`: write entire sample_raw + sample_normalized (currently empty)
   - `dealpath_deal_pipeline`: write all source_contract.yaml, normalized_contract.yaml, field_mapping.yaml, sample_raw + sample_normalized (currently has only manifest, README, dq_rules, source_registry_entry, workflow_activation_additions, tests)
   - `excel_market_surveys`: add 5 more template_schemas (vendor_rate_card, turn_cost_library, capex_cost_library, schedule_assumption, market_commentary), normalized_contract, field_mapping, sample_valid/, sample_invalid/, dq_rules, reconciliation_rules
   - `manual_sources_expanded`: add file_family_registry.yaml, normalized_contract, sample_files/, reconciliation_rules

2. **Per-adapter `dq_rules.yaml`, `reconciliation_rules.md`, `reconciliation_checks.yaml`, `edge_cases.md`** — only `dealpath_deal_pipeline` and `manual_sources_expanded` have dq_rules.yaml. Add to AppFolio, Intacct, Procore, Excel.

3. **Per-adapter `crosswalk_additions.yaml`** — fragments for adding rows to existing crosswalks (property_master, unit, lease, vendor_master, account, capex_project, etc.) + new asset/market/submarket crosswalks. Currently absent for all 7 adapters.

4. **Per-adapter `runbooks/{vendor}_onboarding.md` + `runbooks/{vendor}_common_issues.md`** — directory exists for some, content pending for all.

5. **`workflow_activation_additions.yaml`** — present for `dealpath_deal_pipeline` and `manual_sources_expanded`. Add for AppFolio, Intacct, Procore, Excel, GraySail.

6. **Canonical extensions surfaced by wave 4** (require canonical-change process):
   - **`commitment` ontology object** — Procore primary entity; currently no canonical home. Either add `commitment` to `_core/ontology.md` or extend `vendor_contract`.
   - **Proposed new workflows** — the 9 workflows referenced by wave-4 handoffs (`pipeline_review`, `pre_close_deal_tracking`, `development_pipeline_tracking`, `acquisition_handoff`, `executive_pipeline_summary`, `investment_committee_prep`, `post_ic_property_setup`, `lease_up_first_period`, `delivery_handoff`) need pack creation under `workflows/`.
   - **GraySail classification** — complete `runbooks/graysail_classification_path.md` (file pending) and `adapters/graysail_placeholder/classification_worksheet.md` (file present, awaiting operator input).

7. **Wave-3 test infrastructure regression** — 19 skill-level tests fail collection from project root because pytest finds `reference/connectors/adapters/conftest.py` instead of `tests/conftest.py`. Tests pass when run from `src/skills/residential_multifamily/tests/` directly. Pre-existing, unrelated to wave-4, but worth fixing.

### Suggested prompt for next session

```
Continue wave-4 stack-specific operationalization for residential_multifamily.
Read session_state/NEXT_SESSION_PROMPT.md for the gap inventory. Priority:

(1) Complete the adapter content gaps for AppFolio, Intacct, Procore, Dealpath,
    Excel, manual_sources, GraySail per the pending-work list (sample data,
    dq_rules, reconciliation_rules, edge_cases, crosswalk_additions, runbooks).
    Each adapter should reach the 17-deliverable bar from the wave-4 spec.

(2) Add the canonical 'commitment' object to _core/ontology.md (Procore primary
    entity) and update the source_of_truth_matrix.md row.

(3) Create the 9 proposed workflows under workflows/ (pipeline_review,
    pre_close_deal_tracking, etc.) — each as a workflow pack with required_domains,
    required_normalized_objects, blocking_issues, partial_mode_behavior,
    human_approvals_required.

(4) Fix the wave-3 conftest collection issue so 'pytest' from project root finds
    src/skills/residential_multifamily/tests/conftest.py before
    reference/connectors/adapters/conftest.py.

Maintain canonical immutability. Wave-4 work is additive only.
Spawn parallel agents per adapter; merge fragments at end as in v0.4.0.
```

### Earlier deferred items (still applicable)

The v0.3.0 deferred-items list below remains relevant; wave-4 did not address them.

---

## 2026-04-15 residential_multifamily operationalization pass (v0.3.0) - deferred items

Remaining gaps after the v0.3.0 operationalization pass. The integration layer is now fully scaffolded (source registry, master-data crosswalks, 8 connector stubs, runbooks, monitoring, rollout, adapters, security). Pick any subset; none block rollout wave 0 or wave 1.

### Wave 4 priorities (highest value)

1. **Directory rename `residential_multifamily` -> `residential-multifamily`.** Long-standing deferred item. Touches `src/skills/residential_multifamily/tests/conftest.py` (L23-26 assertion), `src/catalog/catalog.yaml` (id + source_path), `registry.yaml`, `CHANGELOG.md`, `docs/plans/`, `scripts/catalog-build.py`, `scripts/catalog-generate.py`, and every `reference_manifest.yaml` that path-references the subsystem. Keep as a standalone PR: high-churn, pure rename, zero behavioral change. Update memory note `cre_skills_residential_multifamily_conventions.md` afterward.

2. **Deep LIHTC / HUD schedule population.** `overlays/regulatory/affordable/programs/{lihtc,hud_section_8,hud_202_811,usda_rd,state_program,mixed_income}/` carry architectural stubs only. Populate rent-limit schedules, income-limit schedules, UA tables, recertification calendars under `reference/normalized/{rent_limits,income_limits,ua_schedules}__{program}_{market}.csv`. Companion: populate agency-reporting templates. Every schedule must carry provenance + as_of + approval metadata per `reference/connectors/_core/benchmark_update_log.schema.yaml`.

3. **Live PMS / GL adapters.** The vendor-family adapter stubs exist under `reference/connectors/adapters/` (pms_vendor_family_stub, gl_vendor_family_stub, etc.) and are status=stub. Fork into named vendor adapters (Yardi, RealPage, Entrata, MRI, AppFolio for PMS; Sage Intacct, MRI, NetSuite, Yardi GL for GL). Each fork populates example_raw_payload.jsonl with real sanitized payload, refines mapping_template.yaml against real column headers, validates via tests, advances status to starter or production per `adapters/adapter_lifecycle.md`. Register in vendor_family_registry.yaml + source_registry.yaml.

4. **Luxury segment depth.** Still a stub; populate brand-standard posture, concierge service packs, amenity programming reference, luxury screening posture, luxury renewal strategy. Compose with middle_market baseline; diverge only where the positioning demands.

5. **Tailoring TUI 8-audience wiring.** `tailoring/tools/tailoring_tui.py` still reads the 7 legacy question banks. Extend to read the 8-audience map from `AUDIENCE_MAP.md` and use the new `executive.yaml` / `finance_reporting.yaml` / `compliance_risk.yaml` / `site_ops.yaml` banks. Preserve session-resume compatibility with existing `sessions/` files. Wire DIFF_APPROVAL_PREVIEW.md flow (preview bundle -> sign_off_queue -> commit).

### Wave 4 secondary

6. **Implement compliance workflows.** Rule `r011` in `_core/routing/rules.yaml` references `workflows/{compliance_calendar_review, income_certification_cycle, rent_limit_test, agency_reporting_prep, file_audit_prep, recertification_batch}` - none exist yet. Each is a multi-step workflow pack.

7. **Jurisdiction overlays.** `overlays/regulatory/jurisdictions/` is a template; populate state / local HFA overrides as operator scenarios arise.

8. **Approval-matrix threshold validation.** When the tailoring interview collects numeric thresholds, validate `tier1 < tier2 < tier3` and reject loose or out-of-order sets. Current scope is a preview only.

9. **Fair-housing linter.** Scan draft delinquency / screening / resident communication templates for common FH red-flag patterns (rigid credit-score cutoffs, source-of-income discrimination). Current `test_fair_housing_banner.py` checks the banner exists but not the content. See `_core/security/fair_housing_controls.md` for the forbidden-practice taxonomy.

10. **Promote proposed canonical metrics.** Integration layer flagged candidates for `_core/metrics.md` elevation:
    - `insurance_expiry_exposure` (referenced by AP + PMS reconciliation checks but no canonical metric quantifies portfolio-wide COI expiry risk).
