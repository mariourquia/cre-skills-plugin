# Stack Rollout — Wave 4

Status: wave_4_authoritative
Audience: cffo, asset_mgmt, finance_reporting, regional_ops, data_platform_team, compliance_risk

This wave operationalizes the AppFolio + Sage Intacct + Procore + Dealpath +
Excel + GraySail + manual stack against the canonical residential_multifamily
skill. Wave 4 splits into four sub-waves to manage operational risk.

## Sub-wave 4A — Pipeline + Operations + Finance + Benchmarks

**Scope**: Dealpath, AppFolio, Sage Intacct, Excel market surveys.

**Prerequisites**:
- Wave 0–3 complete (canonical base, vendor-neutral framework, 192 tests passing)
- `_core/stack_wave4/source_of_truth_matrix.md` reviewed by asset_mgmt + finance_reporting
- Crosswalks present: property_master_crosswalk, account_crosswalk, vendor_master_crosswalk, lease_crosswalk, asset_crosswalk (new), market_crosswalk (new), submarket_crosswalk (new)
- Source registry entries for: appfolio_prod, sage_intacct_prod, dealpath_prod, excel_market_surveys (per file family)

**Minimum viable outputs**:
- Monthly property operating review for 1 pilot property (full canonical inputs from AppFolio + Intacct, market context from Excel)
- Pre-close deal pipeline review (Dealpath sole source)
- Acquisition handoff (Dealpath → AppFolio + Intacct setup) for 1 pilot deal
- Market rent refresh + rent comp intake at file-family cadence

**Confidence expectations**:
- Property scorecard: medium
- Pipeline review: high (Dealpath sole source)
- Market rent refresh: medium (drift detection still calibrating)

**Go-live checks**:
- Each adapter `manifest.yaml` valid, status set to `stub` or `active` per real readiness
- Each adapter has `source_registry_entry.yaml` registered in master `source_registry.yaml`
- Crosswalks resolve for all pilot property identifiers
- Reconciliation `recon_af_property_list_vs_intacct_dim` green for pilot
- Reconciliation `recon_excel_freshness_vs_use` green
- Three runbooks rehearsed: `appfolio_common_issues.md`, `sage_intacct_common_issues.md`, `excel_market_survey_common_issues.md`

**Rollback criteria**:
- Reconciliation blocker fails persist >5 business days
- Workflow output rejected by asset_mgmt for two consecutive months
- PII or financial sensitivity violation detected by `test_integration_security.py`

**Success measures**:
- Property scorecard delivered within 5 business days of close
- Pipeline review accepted by IC
- 0 unauthorized PII exposure in samples

## Sub-wave 4B — Construction + Project Controls

**Scope**: Procore, plus reconciliations Procore↔Intacct and Procore↔Dealpath.

**Prerequisites**:
- Sub-wave 4A live for 60+ days
- `dev_project_crosswalk` and `capex_project_crosswalk` populated for all active projects
- Procore project naming convention finalized (matches property naming for delivery handoff)
- Cost code → Intacct account crosswalk locked
- Vendor master deduped via `recon_vendor_three_way`

**Minimum viable outputs**:
- Cost-to-complete review weekly for 1 active construction project
- Change order review event-driven
- Draw package summary for monthly draw cycle
- Schedule risk review with baseline preserved

**Confidence expectations**:
- Cost-to-complete: medium (calibration ongoing)
- Schedule risk: high (Procore primary)
- Draw package: medium (timing reconciliation with Intacct)

**Go-live checks**:
- Procore `source_registry_entry.yaml` registered
- `recon_pc_costs_vs_intacct_capex` green at project-total level
- `recon_pc_co_pending_vs_posted` lag below tolerance
- `recon_dp_dev_to_pc` lag below tolerance for active projects

**Rollback criteria**:
- Schedule baseline drift not preserved (loss of audit trail)
- Vendor duplicates >1 per active project
- Project cost reconciliation blocker fails persist >2 weeks

**Success measures**:
- Construction project review accepted by construction_lead
- Procore-Intacct cost reconciliation within tolerance for all active projects
- Project-to-property delivery handoff completed for at least one project

## Sub-wave 4C — GraySail + Third-Party Manager + Executive Rollup

**Scope**: GraySail (post-classification), TPM file submission pathways, executive rollup hardening.

**Prerequisites**:
- Sub-wave 4A and 4B live and stable
- GraySail classification closed via `runbooks/graysail_classification_path.md`
- `manual_sources_expanded` adapter file family registry approved
- Third-party manager file submission SLA defined
- Executive summary template approved by cffo

**Minimum viable outputs**:
- TPM scorecard for all third-party-managed properties
- Quarterly portfolio review with confidence-annotated metrics
- Executive operating summary with all wave-4 sources contributing

**Confidence expectations**:
- TPM scorecard: medium (file submission lag a known degradation)
- Quarterly portfolio: high (after 4A and 4B mature)
- Executive summary: high

**Go-live checks**:
- GraySail status moved from `placeholder_pending_clarification` to `stub` or `active`
- `recon_tpm_file_submission_lag` measured for all TPM properties
- Executive summary template review across cffo, asset_mgmt, executive

**Rollback criteria**:
- GraySail integration breaks an existing reconciliation
- TPM scorecard error rate >5%
- Executive summary requires manual rebuild more than once per quarter

**Success measures**:
- TPM scorecards consistently delivered on cadence
- Quarterly portfolio review accepted by IC
- Executive summary requires no manual data assembly

## Sub-wave 4D — Automation + Confidence + Portfolio Analytics

**Scope**: Tighter workflow gating, automated confidence scoring across stack, expanded portfolio analytics.

**Prerequisites**:
- All of 4A–4C stable for 90+ days
- `recon_*` checks running automatically with operator-friendly exception queue
- Override audit trail validated in `audit_trail.md` for at least 10 overrides

**Minimum viable outputs**:
- Workflow blocker enforcement (no override without `manual_override_approval.md` runbook)
- Cross-source confidence score on every workflow output
- Portfolio-level analytics with same-store cohort, market aggregates, watchlist scoring

**Confidence expectations**:
- High across all canonical workflows
- Confidence floor enforced

**Go-live checks**:
- All `monitoring/alert_policies.yaml` policies tuned (no false-positive flooding)
- All `runbooks/*.md` rehearsed within last 90 days
- Wave 4 regression test suite in CI

**Rollback criteria**:
- Confidence scoring causes false blockers
- Workflow gating blocks routine operations >5% of cycles

**Success measures**:
- Operator override rate <2% per quarter
- Workflow output confidence consistently `high`
- Asset management cycle time reduction quantifiable

## Cross-cutting wave-4 dependencies

- `BOUNDARIES.md` and `DESIGN_RULES.md` unchanged
- `_core/ontology.md` extended only via approved canonical change (commitment object pending)
- `master_data/asset_crosswalk.yaml`, `market_crosswalk.yaml`, `submarket_crosswalk.yaml` created in 4A
- `workflows/` may add: `pipeline_review`, `pre_close_deal_tracking`, `development_pipeline_tracking`, `acquisition_handoff`, `executive_pipeline_summary`, `investment_committee_prep`, `post_ic_property_setup`, `lease_up_first_period`, `delivery_handoff` (each requires canonical workflow review)
