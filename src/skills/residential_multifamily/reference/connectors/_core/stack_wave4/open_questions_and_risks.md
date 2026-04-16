# Wave 4 Open Questions and Risks

Status: wave_4_authoritative
Audience: residential_multifamily_subsystem maintainers, asset_mgmt, finance_reporting

These questions surfaced during wave-4 implementation and are NOT closed.
Each item should be resolved before promoting any sub-wave from `stub` to
`active`. Do not silently resolve by code change; route through the canonical
change process where it touches `_core/`.

## Canonical extensions required

### 1. `commitment` canonical object

- **Need**: Procore primary entity is the commitment (purchase_order or subcontract). Currently no canonical `commitment` in `_core/ontology.md`.
- **Options**: (a) Add canonical `commitment` object; (b) Treat commitments as `vendor_contract` extension; (c) Defer to projection layer.
- **Recommended**: (a). Define in ontology with grain of (project_id, vendor_id, commitment_id), required fields total_amount, status, and link to capex_project.
- **Owner**: ontology maintainer + construction_lead
- **Blocking**: sub-wave 4B until resolved

### 2. `asset_crosswalk.yaml`

- **Need**: Dealpath is primary source for canonical `asset` but no `asset_crosswalk.yaml` exists in `master_data/`.
- **Recommended**: Create `master_data/asset_crosswalk.yaml` with full crosswalk schema. Survivorship rule `dealpath_primary_for_asset_pre_close`.
- **Owner**: data_platform_team
- **Blocking**: sub-wave 4A go-live

### 3. `market_crosswalk.yaml` and `submarket_crosswalk.yaml`

- **Need**: Excel market surveys use broker-naming for markets/submarkets; AppFolio uses internal naming. No crosswalk exists.
- **Recommended**: Create both. Effective-dating respected. Survivorship rule `excel_authoritative_for_external_naming` and `appfolio_authoritative_for_internal_naming`.
- **Owner**: data_platform_team + asset_mgmt
- **Blocking**: `recon_market_tag_consistency` cannot run until exists

### 4. New source domain `deal_pipeline`

- **Status**: Added in wave 4 as a new connector domain. Source registry schema already accepts it (enum extended).
- **Open**: workflow_activation_map.yaml does not yet declare workflows scoped to `deal_pipeline`. Proposed workflows below.
- **Owner**: ontology maintainer + asset_mgmt
- **Blocking**: full sub-wave 4A executive summary scope

### 5. Proposed new workflows

These workflows need canonical addition to `workflows/`:

- `pipeline_review`
- `pre_close_deal_tracking`
- `development_pipeline_tracking`
- `acquisition_handoff`
- `executive_pipeline_summary`
- `investment_committee_prep`
- `post_ic_property_setup`
- `lease_up_first_period`
- `delivery_handoff`

Each requires a workflow pack with required_domains, required_normalized_objects,
blocking_issues, partial_mode_behavior, human_approvals_required.

- **Owner**: workflow maintainer
- **Blocking**: each workflow blocks the corresponding handoff outputs

## Source-specific risks

### 6. GraySail classification unresolved

- **Status**: Built as `placeholder_pending_clarification`. Workflows that reference GraySail must run with degraded confidence or block.
- **Required follow-up**: complete `graysail_placeholder/classification_worksheet.md` with operator input.
- **Owner**: asset_mgmt + data_platform_team
- **Blocking**: sub-wave 4C

### 7. Procore commitment-to-invoice reconciliation

- **Risk**: Procore commitments may not always have a 1:1 invoice link in Intacct AP.
- **Mitigation**: `recon_pc_costs_vs_intacct_capex` operates at project-total level until commitment-level reconciliation matures.
- **Owner**: construction_lead + finance_reporting

### 8. AppFolio turn inference

- **Risk**: AppFolio has no native TurnProject object; turns inferred from event sequences. Ambiguous cases (extended vacancy without make-ready, unit transfers) may produce false positives or false negatives.
- **Mitigation**: turn inference rules documented in `appfolio_pms.edge_cases.md`; manual review queue for ambiguous cases.
- **Owner**: regional_ops

### 9. Excel benchmark luxury contamination

- **Risk**: Excel rent comp files may include luxury comps in middle_market sheets.
- **Mitigation**: `recon_excel_luxury_contamination` weekly check; `dq_rule_excel_segment_match` flags at intake.
- **Owner**: asset_mgmt analyst team

### 10. Intacct multi-dimension property tagging

- **Risk**: One canonical property may roll up under (entity, location, project) dim combinations differently across periods.
- **Mitigation**: `account_crosswalk.yaml` carries effective_start; `recon_intacct_property_dim_consistency` weekly check.
- **Owner**: finance_systems_team

## Process risks

### 11. Wave-4 test coverage gap

- **Risk**: Several agents hit context/rate limits before producing tests. Adapter-local `tests/test_adapter.py` may be missing for some adapters.
- **Mitigation**: skill-level `tests/test_stack_wave4_adapter_presence.py` enforces every wave-4 adapter has minimum file set + tests/ directory.
- **Owner**: data_platform_team

### 12. Adapter sample data completeness

- **Risk**: Several adapters have only partial sample_raw/ coverage (missing entities); sample_normalized/ may not exist for some.
- **Mitigation**: enumerate gaps during the next wave-4 completeness pass and assign per adapter.
- **Owner**: data_platform_team

### 13. Source registry merge risk

- **Risk**: Each adapter wrote a `source_registry_entry.yaml` fragment; merge into master `source_registry.yaml` is operator-managed.
- **Mitigation**: integration agent runs `tests/test_source_registry.py` after merge; conflicts caught.
- **Owner**: data_platform_team

### 14. CHANGELOG drift

- **Risk**: Wave 4 adds many files; CHANGELOG may not capture every addition.
- **Mitigation**: next session updates CHANGELOG with full wave-4 inventory.
- **Owner**: maintainer

## Migration notes

- Existing wave-0 to wave-3 stub adapters remain in place; wave-4 vendor adapters are NEW directories, no replacement.
- The new `deal_pipeline` connector domain is additive; existing 8 domains unchanged.
- Source registry adds `deal_pipeline` enum value; this is a backwards-compatible schema extension.

## Blocked items summary

| Item | Blocker for | Severity |
|---|---|---|
| `commitment` ontology object | sub-wave 4B | high |
| `asset_crosswalk.yaml` | sub-wave 4A go-live | high |
| `market_crosswalk.yaml` / `submarket_crosswalk.yaml` | excel-related recons | medium |
| Proposed workflows in `workflows/` | each handoff output | medium |
| GraySail classification | sub-wave 4C | medium |
| Adapter test coverage gaps | wave-4 CI gate | medium |
| Sample data completeness | adapter conformance tests | low |

## Deferred decisions

- Whether `commitment` lives at canonical `_core/ontology.md` or extends `vendor_contract` — pending construction_lead review.
- Whether `pipeline_review` is one workflow or split by acquisition vs development — pending asset_mgmt review.
- Whether GraySail integrates as a separate domain or extends `deal_pipeline` — depends on classification outcome.
- Whether wave-4 reconciliation tolerances (`reference/normalized/schemas/reconciliation_tolerance_band.yaml`) are operator-tunable per org overlay or canonical-only.
