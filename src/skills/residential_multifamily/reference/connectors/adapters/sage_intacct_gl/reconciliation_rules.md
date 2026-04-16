# Sage Intacct Reconciliation Rules

Status: wave_4_authoritative
Audience: data_platform_team, corporate_controller, finance_systems_team, asset_mgmt_director

This document is the narrative companion to `reconciliation_checks.yaml`.
Per-adapter checks use the `ic_recon_` prefix. All tolerance thresholds are
cited by name from `reference/normalized/schemas/reconciliation_tolerance_band.yaml`;
no numeric values are hardcoded here. When a reconciliation is named in the
wave-4 `stack_reconciliation_matrix.md`, that cross-stack check_id is quoted
verbatim to preserve traceability.

---

## Pair 1. Intacct <-> AppFolio (PMS)

AppFolio is primary for resident-side receivables and cash receipts. Intacct
is primary for posted GL actuals. Reconciliation sits at the cash-to-accrual
seam and the vendor-master tri-reconciliation.

### 1A. Cash receipts

| Surface | Source of truth |
|---|---|
| Resident charge ledger | AppFolio (primary) |
| Resident payment receipt | AppFolio (primary) |
| GL posted revenue (accrual) | Intacct (primary) |
| GL posted deposit (cash) | Intacct (primary after close) |

Cash posted in Intacct for a given property and period must reconcile to the
AppFolio payment receipt export for the same period within
`revenue_basis_band`. After period close, Intacct wins; AppFolio receipts
become audit rows. Drift beyond the band and not explained by a documented
timing gap is a `warning` that degrades workflow confidence to `medium`.

Cross-reference: `stack_reconciliation_matrix.md::recon_af_collections_vs_intacct_revenue`.

### 1B. Vendor master (Intacct <-> AppFolio)

| Field | Intacct survives | AppFolio survives |
|---|---|---|
| Tax id | X | |
| Legal name | X | |
| Payment terms label | X | |
| AP invoice lifecycle status | | X |
| Vendor preferred flag (operations) | | X |
| Service dispatch history | | X |

Three-way match (adds Procore under Pair 3) runs weekly. Identity match uses
`identity_match_band`. Mismatch degrades to `warning`; unresolved after
`vendor_three_way_resolution_band` escalates to `blocker`.

Cross-reference: `stack_reconciliation_matrix.md::recon_vendor_three_way`.

### 1C. Property dimension consistency

Every property present in AppFolio must map to an Intacct `LOCATIONID` or
`ENTITYID` via `property_master_crosswalk`. A property active in AppFolio
without an Intacct dimension mapping is a `blocker` because actual_lines
posted in Intacct would strand with missing property_id.

Cross-reference: `stack_reconciliation_matrix.md::recon_af_property_list_vs_intacct_dim`.

---

## Pair 2. Intacct <-> Procore (Construction)

Procore owns commitment, change order, and draw request lifecycle. Intacct
owns posted capex. Reconciliation guards the commitment-to-posted spend
handshake.

### 2A. Commitment vs posted spend

For every active capex_project_id, weekly reconciliation compares:

- Procore commitment amount (sum of approved commitments plus approved change
  orders)
- Intacct posted spend (sum of actual_line.amount_cents where PROJECTID
  resolves to the same capex_project_id and canonical_account_slug is in
  capex family)

Drift beyond `capex_posting_band` is a `warning` that escalates to `blocker`
after `co_posting_lag_band` for change orders and `draw_posting_lag_band` for
draws.

Cross-references:
- `stack_reconciliation_matrix.md::recon_pc_costs_vs_intacct_capex`
- `stack_reconciliation_matrix.md::recon_pc_co_pending_vs_posted`
- `stack_reconciliation_matrix.md::recon_pc_draw_vs_posted`

### 2B. Project dimension handshake

Every active Procore capex project must have a corresponding Intacct
`PROJECTID` row with `project_dim_lock_status` in {open, locked}. A Procore
project without an Intacct Project dimension is a `blocker` on
`cost_to_complete_review`.

### 2C. Vendor crosswalk (contractors)

Procore carries contractor insurance expiry and trade classification;
Intacct carries tax id and payment terms. The three-way match from Pair 1B
extends to contractors.

---

## Pair 3. Intacct <-> HR/Payroll

HR/Payroll produces payroll_line detail at the employee grain. Intacct posts
the payroll journal at the GL grain. Reconciliation guards that payroll hits
the right property dimension and the right account (payroll vs contract
labor).

### 3A. Payroll line entity attribution

For every pay period:

- Sum of payroll_line.amount_cents by canonical property_id (from HR/Payroll
  feed via `employee_crosswalk` and `staffing_plan`) must equal Sum of
  actual_line.amount_cents for Intacct account in payroll family (5010,
  5020) by resolved property_id, within `staffing_drift_band`.

Drift is a `warning` on the `monthly_property_operating_review` workflow and
feeds into `budget_build` staffing assumption refresh.

Cross-reference: `stack_reconciliation_matrix.md::recon_staffing_benchmark_vs_actual`.

### 3B. Contractor vs employee classification

HR/Payroll flags each record as W-2 or 1099. The `employee_crosswalk`
carries the employment_type note. Contract labor must post to
`expense_contract_labor` (GL account 6050); employee payroll must post to
`expense_payroll` (GL accounts 5010, 5020). Misclassification is a
`warning`; drift beyond `labor_rate_drift_band` becomes a `blocker`.

### 3C. Labor rate drift

Cross-reference: `stack_reconciliation_matrix.md::recon_labor_rate_vs_payroll`.
Quarterly cadence. Excel labor rate reference vs HR/Payroll vs Intacct
posted. Drift beyond `labor_rate_drift_band` triggers `benchmark_refresh.md`
workflow.

---

## Pair 4. Intacct <-> Manual (variance narratives and spreadsheet fallback)

Manual uploads fill the variance_explanation surface and the budget fallback
for properties not yet on the Intacct Budget Module.

### 4A. Variance narrative coverage

For any `(property_id, canonical_account_slug, period)` where
`abs(variance_cents) > variance_narrative_required_band`, a manager
narrative must be present. Absent narrative is a `warning` that escalates to
`blocker` after `variance_narrative_deadline_band` past period close.

Guardrail: the narrative may originate in Intacct's Budget Module note field
(the adapter joins that field onto the variance_explanation record) OR in a
manual spreadsheet submission. Either satisfies the rule.

### 4B. Manual budget fallback

For properties whose budget_line is sourced from manual spreadsheet uploads
rather than the Intacct Budget Module, the manual file's attestation must
arrive per `tpm_submission_band` before the variance calculation can run.
Drift converts the variance row to `low_confidence`.

Cross-reference: `stack_reconciliation_matrix.md::recon_tpm_file_submission_lag`.

---

## Pair 5. Intacct <-> Dealpath (post-close entity setup)

Dealpath is primary for pre-close deal pipeline. Intacct picks up post-close
when the property entity and chart-of-accounts are provisioned.

### 5A. Post-close entity setup handshake

For every deal with `stage = closed` in Dealpath:

- Dealpath must have `asset.id` set.
- Intacct must provision `ENTITYID` (or `LOCATIONID`, per deployment
  pattern) within `handoff_lag_band`.
- `property_master_crosswalk` must carry a row linking the Intacct dim to
  the canonical `property_id` and the Dealpath `asset.id`.

Missing or delayed entity setup is a `warning` that escalates to `blocker`
after `handoff_lag_band` past closed date.

Cross-reference: `stack_reconciliation_matrix.md::recon_dp_approved_vs_setup`.

### 5B. Post-close dimension reuse

Placeholder Intacct Project rows (e.g., `PRJ_PLACEHOLDER_*`) created during
deal diligence must be resolved to concrete capex_project_ids post-close.
Unresolved placeholders after `handoff_lag_band` block
`capital_project_intake_and_prioritization`.

---

## Cross-pair summary

| Pair | Primary workflows impacted | Cadence | Primary runbook |
|---|---|---|---|
| Intacct <-> AppFolio (cash) | monthly_property_operating_review, monthly_asset_management_review | monthly | sage_intacct_common_issues.md::cash_accrual_drift |
| Intacct <-> AppFolio (vendor) | vendor_dispatch_sla_review, owner_approval_routing | weekly | sage_intacct_common_issues.md::vendor_crosswalk_mismatch |
| Intacct <-> AppFolio (property dim) | monthly_property_operating_review | weekly | sage_intacct_common_issues.md::property_dim_missing |
| Intacct <-> Procore (commitments) | cost_to_complete_review, draw_package_review, capex_spend_vs_plan | weekly | sage_intacct_common_issues.md::capex_posting_drift |
| Intacct <-> Procore (project dim) | capital_project_intake_and_prioritization | weekly | sage_intacct_common_issues.md::capex_project_unmapped |
| Intacct <-> HR/Payroll (entity) | monthly_property_operating_review, budget_build | monthly | sage_intacct_common_issues.md::payroll_entity_drift |
| Intacct <-> HR/Payroll (class) | budget_build | quarterly | sage_intacct_common_issues.md::labor_classification_drift |
| Intacct <-> Manual (narrative) | monthly_property_operating_review, executive_operating_summary_generation | monthly | sage_intacct_common_issues.md::variance_narrative_missing |
| Intacct <-> Manual (budget fallback) | budget_build, reforecast | quarterly | sage_intacct_common_issues.md::manual_budget_fallback |
| Intacct <-> Dealpath (handoff) | acquisition_handoff, post_ic_property_setup | event-driven | sage_intacct_common_issues.md::post_close_entity_setup |

---

## Confidence model

Every reconciliation outcome contributes to the workflow's
`effective_confidence`:

- `pass` (within `silent_audit` band) --> no impact
- `pass_with_drift` (within `confidence_reduced` band) --> degrade `high` to `medium`
- `fail` (outside `blocker` band) --> block per `workflow_activation_map.yaml::blocking_issues`

Operators cannot suppress `effective_confidence`. Releases require
`manual_override_approval.md` with `audit_trail.md` logging.
