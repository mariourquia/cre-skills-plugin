# Source-of-Truth Matrix — Wave 4 Stack

Status: wave_4_authoritative
Audience: data_platform_team, asset_mgmt, finance_reporting, regional_ops

## Philosophy

Canonical objects in `_core/ontology.md` are source-neutral. This matrix declares
**which system populates each canonical object first-pass**, which one
**survives a conflict**, and **what triggers a blocking exception**.

Sources in scope:

- `appfolio` — AppFolio PMS (PMS domain)
- `intacct` — Sage Intacct (GL domain)
- `procore` — Procore (construction domain)
- `dealpath` — Dealpath (deal_pipeline domain)
- `excel` — Excel market surveys + analyst benchmark packs (market_data + manual_uploads)
- `graysail` — Pending classification; treat as `unresolved` until `runbooks/graysail_classification_path.md` is closed
- `manual` — Operator-maintained spreadsheets, emailed files, shared-drive submissions

## Resolution rules (cross-cutting)

| Rule | Behavior |
|---|---|
| `posting_period_close_wins` | After Intacct close period, Intacct is canonical for any actuals dispute. AppFolio cash receipt is reconciled but does not overwrite. |
| `event_time_priority` | When two sources disagree on event ordering, the source carrying the system-of-record claim for that object wins; the other becomes audit. |
| `effective_dating_required` | All crosswalks carry `effective_start`. Survivorship rule named per row. |
| `disagreement_threshold_band` | Disagreements within band defined in `reference/normalized/schemas/reconciliation_tolerance_band.yaml` reduce confidence to `medium`; outside band blocks affected workflow. |
| `late_arriving_data_supersedes` | Late arrival from primary supersedes earlier secondary load; secondary is preserved as audit row. |
| `pending_classification_blocks` | Where GraySail is named primary, workflow runs in `partial_mode_behavior` until classification closed. |

## Matrix

| Canonical Object | Primary | Secondary | Fallback | Disagreement Resolution | Timestamp Rule | Effective Dating | Block Threshold |
|---|---|---|---|---|---|---|---|
| deal | dealpath | manual | manual | dealpath wins until close, then dealpath retains pre-close audit | deal_stage_changed_at | from `effective_start` on `dev_project_crosswalk` row | closed deal lacking downstream property/project for >5 business days |
| asset | dealpath | manual | manual | dealpath wins until close; post-close, AppFolio + Intacct co-define operating asset | asset_created_at | per asset_crosswalk row | duplicate asset name in same market |
| development_project | dealpath | procore | manual | dealpath seeds; procore canonical once project executes | project_kickoff | per dev_project_crosswalk | dealpath-approved deal lacking procore project >10 business days |
| construction_project | procore | dealpath | intacct | procore primary; intacct reconciles cost; dealpath for governance milestones | project_phase_changed_at | per dev_project_crosswalk | procore project lacking intacct project dimension |
| capex_project | procore | intacct | manual | procore for scope/commitments; intacct for posted spend | project_created_at | per capex_project_crosswalk | capex project active in procore but unmapped in intacct |
| property | appfolio | intacct | dealpath | appfolio for operating identity; intacct for legal_entity_id | property_setup_at | per property_master_crosswalk | property in appfolio with no intacct entity dim mapping |
| building | appfolio | manual | manual | appfolio sole | n/a | per property_master_crosswalk parent | n/a |
| unit | appfolio | manual | manual | appfolio sole | unit_status_changed_at | per unit_crosswalk | unit count mismatch with rent roll |
| unit_type / floor_plan | appfolio | manual | manual | appfolio sole | n/a | n/a | unit references missing unit_type |
| resident_account | appfolio | manual | n/a | appfolio sole | account_opened_at | per resident_account_crosswalk | unresolved tenant identity carrying balance |
| lease | appfolio | manual | n/a | appfolio sole | lease_signed_at | per lease_crosswalk | lease in appfolio without unit |
| lease_event | appfolio | manual | n/a | appfolio sole | event_date | n/a | lease event sequence inconsistent with status |
| lead | appfolio | manual | n/a | appfolio sole; CRM domain may layer secondary | inquiry_date | n/a | n/a |
| showing / tour | appfolio | manual | n/a | appfolio sole | scheduled_date | n/a | n/a |
| application | appfolio | manual | n/a | appfolio sole | applied_date | n/a | n/a |
| approval_outcome | appfolio | manual | n/a | appfolio sole; policy_ref required | decided_date | n/a | denial without policy_ref |
| charge | appfolio | intacct | n/a | appfolio for resident-side ledger; intacct for posting | charge_date | n/a | charge without lease ref |
| payment | appfolio | intacct | n/a | appfolio for cash receipt; intacct after close | payment_date | n/a | payment with no charge applied |
| delinquency_case | appfolio | manual | n/a | appfolio sole | stage_entered_date | n/a | legal_flag without approval_request |
| work_order | appfolio | manual | n/a | appfolio sole | reported_date | n/a | p1_safety with no assignment in 4h |
| turn_project | appfolio | manual | n/a | appfolio sole; turn inferred from event sequence | move_out_date | n/a | turn lacking move_out_date |
| vendor | appfolio | intacct | procore | three-way reconciliation; intacct survives for tax id, appfolio for service dispatch, procore for construction commitments | vendor_added_at | per vendor_master_crosswalk | duplicate vendor across two systems unresolved |
| invoice | intacct | procore | ap (manual) | intacct primary; procore commitment-side reconciles | invoice_date | n/a | unposted invoice >30 days |
| commitment | procore | intacct | manual | procore primary for scope + executed state; intacct primary for posted spend; manual for non-procore legacy commitments | commitment_executed_date (state); commitment_created_at (audit) | per commitment_crosswalk row when introduced | commitment overdrawn vs revised_amount; status=executed without insurance/bond per Vendor guardrail |
| commitment (yardi-historical) | yardi | manual | n/a | yardi sole for legacy/historical commitments not present in procore; do not overwrite procore primary | commitment_executed_date | per commitment_crosswalk row when introduced | yardi-only commitment referenced by active project lacking procore mapping |
| budget_line | intacct | manual | excel | intacct sole; excel benchmarks inform build only | as_of_date | budget version | budget version unmapped |
| forecast_line | intacct | manual | excel | intacct sole | as_of_date | forecast version | forecast inconsistent with prior actuals trend |
| actual_line | intacct | appfolio | n/a | intacct sole post-close | posting_date | n/a | unmapped account or unmapped property dim |
| variance_explanation | manual | intacct | n/a | manual narrative on intacct numbers | as_of_date | n/a | variance > policy band without narrative |
| staffing_position | manual | excel | hr_payroll | manual operator plan; excel benchmark calibrates; hr_payroll validates | as_of_date | n/a | actual headcount > plan without note |
| payroll_line | intacct | hr_payroll | manual | intacct sole post-close | pay_period_end | n/a | unmapped employee dim |
| rent_comp | excel | manual | dealpath | excel sole | as_of_date | per file_family staleness window | as_of_date older than staleness_threshold_days |
| market_rent_benchmark | excel | manual | n/a | excel sole | as_of_date | per file family | n/a |
| concession_benchmark | excel | manual | appfolio | excel primary; appfolio drift detection | as_of_date | per file family | n/a |
| occupancy_benchmark | excel | manual | n/a | excel sole | as_of_date | n/a | n/a |
| labor_rate_reference | excel | manual | hr_payroll | excel + hr_payroll periodic calibration | as_of_date | n/a | drift > tolerance vs payroll |
| material_cost_reference | excel | manual | procore | excel + procore commitments calibration | as_of_date | n/a | n/a |
| turn_cost_reference | excel | appfolio | manual | excel + appfolio actuals calibration | as_of_date | n/a | n/a |
| estimate_line_item | procore | excel | manual | procore primary; excel for assumption sourcing | n/a | n/a | line item missing source_basis |
| bid_package | procore | manual | n/a | procore sole | n/a | n/a | award without bid leveling |
| change_order | procore | intacct | manual | procore primary; intacct reconciles posted | co_status_changed_at | n/a | approved CO not posted in intacct >10 days |
| draw_request | procore | intacct | manual | procore primary; intacct reconciles posted | draw_submitted_at | n/a | draw approved no posting >5 days |
| schedule_milestone | procore | manual | n/a | procore sole; baseline preserved | milestone_baseline_date | n/a | milestone slip > policy band |
| approval_request | manual | dealpath | manual | manual or dealpath depending on subject | created_at | n/a | gated action executed without approval |
| escalation_event | manual | n/a | n/a | manual sole | created_at | n/a | n/a |
| source_record_audit | system | n/a | n/a | system writes | landed_at | n/a | n/a |
| market_commentary | excel | manual | n/a | excel + manual | as_of_date | n/a | n/a |
| vendor_rate | excel | manual | ap | excel sole; ap calibrates | as_of_date | n/a | drift > tolerance vs ap |

## When disagreement becomes a blocker (vs. confidence reduction)

| Severity | Behavior |
|---|---|
| `confidence_reduced` | Workflow runs in `partial_mode_behavior`. Output marks affected metric as `low_confidence`. Discrepancy logged to `monitoring/observability_events.yaml`. |
| `blocker` | Workflow halts. Exception routed via `monitoring/exception_routing.yaml`. Runbook surfaces in operator queue. |
| `silent_audit` | Within tolerance band; no operator surfacing; row preserved for audit. |

The thresholds themselves live in `reference/normalized/schemas/reconciliation_tolerance_band.yaml` (cited, not hardcoded here).

## Open

- `asset_crosswalk.yaml`, `market_crosswalk.yaml`, `submarket_crosswalk.yaml` were created in wave 4 (present in `master_data/`). No longer open.
- `commitment_crosswalk.yaml` not yet created in `master_data/`. Wave 5 introduced the canonical `commitment` object (`_core/ontology.md`); the crosswalk row pattern is defined inline on adapter `crosswalk_additions.yaml` files (procore, intacct, yardi). Promote to a dedicated `commitment_crosswalk.yaml` in master_data when first non-procore commitment source goes live.
- GraySail row deferred until `runbooks/graysail_classification_path.md` operator-completed (file present; classification still pending operator input).
- Yardi row added below as wave-5; primary status depends on per-environment classification per `yardi_multi_role/classification_worksheet.md`.

## Yardi rows (wave 5; classification-pending precedence)

Yardi precedence is **operator-classified**. Until `yardi_multi_role/runbooks/yardi_classification_path.md` closes for the environment, treat every Yardi-touched object as `unresolved` and run dependent workflows in `partial_mode_behavior`. After classification, slot Yardi into the matrix per the role chosen:

| Yardi role (after classification) | Effect on existing rows |
|---|---|
| `yardi_primary_operating` | Yardi displaces AppFolio as primary for property, unit, lease, lease_event, charge, payment, work_order on the in-scope subset of properties; AppFolio becomes secondary on those properties. |
| `yardi_primary_accounting` | Yardi displaces Intacct as primary for actual_line, budget_line, forecast_line, vendor, invoice on the in-scope subset of entities; Intacct becomes secondary. |
| `yardi_primary_leasing_only` | Yardi (RentCafe) displaces AppFolio as primary for lead, tour, application, approval_outcome only; AppFolio remains primary for everything else. |
| `yardi_legacy_historical` | Yardi remains audit-only; AppFolio + Intacct stay primary. Yardi survives only for pre-cutoff queries. |
| `yardi_parallel_partial` | Per-property routing rule: each property carries a `primary_pms_source` attribute on its `property_master_crosswalk` row (`appfolio` or `yardi`); workflows fan out per-property. |

Survivorship rule when Yardi and another source disagree post-classification: per-attribute resolution per `crosswalk_additions.yaml::source_of_record_per_attribute` on the relevant Yardi crosswalk row. Conflict resolution defaults to the system declared `primary_for_attribute`; if none declared, the per-row `survivorship_rule` from the crosswalk file applies; if still ambiguous, the discrepancy is logged via `monitoring/observability_events.yaml` with severity per `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
