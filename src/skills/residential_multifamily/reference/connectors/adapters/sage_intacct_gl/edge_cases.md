# Sage Intacct Edge Cases

Status: wave_4_authoritative
Audience: corporate_controller, finance_systems_team, data_platform_team

Every enumerated edge case below is observed in residential multifamily
Intacct deployments. Each case declares:

- **Trigger** — the pattern that raises the edge case.
- **Detection** — which DQ rule or reconciliation check fires (with
  `ic_` or `ic_recon_` prefix).
- **Handling** — the canonical resolution path.
- **Ownership** — the role that owns closure.

Tolerance bands, when referenced, are cited by name from
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`; never
numeric.

---

## 1. Late-arriving accrual posted after period close

**Trigger.** Utility or vendor invoice arrives after period close but
operator accrues into the just-closed period (reopen + post) rather than
taking it to the current period.

**Detection.** `ic_consistency_posting_period_close_lock` +
`ic_recon_period_reopen_drift`. The posting carries `BATCH_DATE >
period_close_timestamp` with a `period_reopen_event` present.

**Handling.** The normalized row carries `late_post_flag = true`. Downstream
variance_explanation must re-compute for the reopened period. The
`monthly_property_operating_review` for the prior period re-runs with the
late-post rows included and a revision note. `period_reopen_lag_band`
governs how long the rerun window stays open.

**Ownership.** `corporate_controller` approves reopen; `finance_systems_team`
reruns the monthly report.

---

## 2. Period reopen after close without formal reopen event

**Trigger.** Operator posts into a closed period using back-dated
`BATCH_DATE` but without the Intacct period reopen workflow being run. The
period lock should have blocked the post; a misconfigured ledger or a
manual workaround let it through.

**Detection.** `ic_consistency_posting_period_close_lock` fires as blocker
(no matching reopen event).

**Handling.** The posting is tagged but held in a quarantine layer; no
downstream actual_line aggregation consumes the row until the reopen is
formally processed or the post is reversed into the current period. Block
propagates to `monthly_property_operating_review`.

**Ownership.** `corporate_controller` reconciles.

---

## 3. Budget version unmapped

**Trigger.** New `BUDGETID` is published by operator with a non-conforming
`BUDGETNAME` label (e.g., "initial_2026" instead of `approved_2026_v1`).
`map_intacct_budget_version` has no entry for the new id.

**Detection.** `ic_conformance_posting_state_enum` fires for the state;
downstream aggregation cannot resolve the scenario slug.

**Handling.** Operator applies budget-version naming convention per
`sage_intacct_onboarding.md::budget_version_naming`. Until relabeled, the
budget rows are normalized with `scenario = unresolved_budget_version_<BUDGETID>`
and downstream variance calculation treats them as `low_confidence`.

**Ownership.** `corporate_controller` enforces naming; `finance_systems_team`
extends the map.

---

## 4. Multi-entity allocation with no property dim

**Trigger.** Corporate-level allocation journal posts at `ENTITYID=ENT_CORP`
with no `LOCATIONID`. Costs are economically borne by several operating
properties but the posting does not split them.

**Detection.** `ic_consistency_posted_without_approver` (if above band) and
`ic_recon_manual_journal_attribution`.

**Handling.** Two paths:
1. **Split at source.** Operator repost the allocation with per-property
   `LOCATIONID` splits; original posting is reversed.
2. **Allocate downstream.** A named allocation basis in
   `property_master_crosswalk` (e.g., `by_unit_count`, `by_revenue`) drives
   a derived allocation layer. The allocated rows are tagged
   `derived_allocation = true`.

`sage_intacct_common_issues.md::manual_journal_attrib` documents which
path applies.

**Ownership.** `corporate_controller` chooses the path.

---

## 5. Dimension on placeholder property awaiting setup

**Trigger.** During pre-close diligence, operator creates a placeholder
Intacct `PROJECTID` (e.g., `PRJ_PLACEHOLDER_NEW_ACQ`) and pre-loads
estimates against it. After close, the placeholder must be resolved to a
concrete capex_project_id tied to the newly-provisioned property.

**Detection.** `ic_guardrail_placeholder_project_must_resolve` +
`ic_recon_post_close_entity_setup`.

**Handling.** Placeholder row carries `placeholder_flag = true` in the
normalized projects feed. Resolution is event-driven at deal close: a new
concrete `PROJECTID` is provisioned, the placeholder is retired, and the
capex_project_crosswalk row is created linking old and new via
`prior_canonical_id`.

**Ownership.** `finance_systems_team` provisions; `asset_mgmt_director`
validates.

---

## 6. Vendor created in AppFolio before Intacct sync

**Trigger.** Property staff add a vendor to AppFolio for dispatch; the
vendor has no Intacct record until AP sync runs. A work order is issued
and completed before Intacct carries the vendor.

**Detection.** `ic_referential_vendor_in_master` +
`ic_recon_vendor_three_way` (AppFolio has row; Intacct does not).

**Handling.** The actual_line posting from AP hits Intacct with a new
`VENDORID` mid-period; `vendor_master_crosswalk` gets a new row matching
the AppFolio source. Three-way match re-runs the following week. In the
interim, the row carries `vendor_sync_pending_flag = true`.

**Ownership.** `ap_manager` drives AP onboarding; `finance_systems_team`
ensures the crosswalk row is created.

---

## 7. Payroll line missing dim_property

**Trigger.** HR/Payroll export carries a role assignment (regional
maintenance lead) that covers three properties, no single `property_id` is
attributed. Intacct posts payroll at the corporate entity level or to a
rotation property.

**Detection.** `ic_recon_payroll_entity_attribution` (HR/Payroll sum by
property_id disagrees with Intacct sum by property_id outside
`staffing_drift_band`).

**Handling.** `staffing_plan` in `employee_crosswalk` carries `fte_share`
per property. A derived allocation layer redistributes the unattributed
payroll by `fte_share`. The original posting is preserved for audit; the
allocated rows are tagged `derived_allocation = true`.

**Ownership.** `hr_director` maintains the `fte_share` values;
`regional_ops_director` validates.

---

## 8. Capex commitment in Procore not yet projected in Intacct dim

**Trigger.** Procore carries an approved commitment against a new capex
project. The Intacct `PROJECTID` for the same project has not yet been
created.

**Detection.** `ic_recon_capex_project_dim_handshake` fires as blocker.

**Handling.** `capital_project_intake_and_prioritization` is blocked until
the Intacct `PROJECTID` is provisioned and the `capex_project_crosswalk`
row is created. Procore continues to carry the commitment; no Intacct
posting is accepted for the project until the dim exists.

**Ownership.** `finance_systems_team` provisions the dim on controller
approval.

---

## 9. Intercompany elimination entries

**Trigger.** Entity A pays a shared service bill on behalf of Entity B.
Intacct generates an intercompany receivable on A and intercompany payable
on B. At consolidation, the intercompany balances eliminate.

**Detection.** `ic_referential_vendor_in_master` on the intercompany
vendor slug; `ic_consistency_debit_credit_balanced` at the consolidation
layer.

**Handling.** Intercompany postings carry a `SOURCE_MODULE = "Intercompany"`
tag in the normalized feed. Consolidation layer subtracts both sides at
the reporting class boundary (fund, portfolio). Intercompany elimination
detail is preserved as audit rows; not surfaced to property-level
`monthly_property_operating_review`.

**Ownership.** `corporate_controller` runs the intercompany elimination;
consolidation layer logic lives in `_core/` (referenced here, not
reimplemented).

---

## 10. Mid-period reorg of dim hierarchy

**Trigger.** Operator reorganizes the entity or location hierarchy mid-year
(e.g., splits a roll-up entity into two SPEs, or moves a property from one
fund class to another). Mid-period postings may carry old dim; later
postings carry new dim.

**Detection.** `ic_conformance_property_dim_in_crosswalk` +
`ic_recon_property_dim_present` (some rows resolve under the old dim,
others under the new).

**Handling.** `property_master_crosswalk` accepts `effective_start` and
`effective_end` on the affected rows. During the transition window, the
adapter resolves `property_id` using the posting's `BATCH_DATE` against
the `effective_start` of the crosswalk row. Historical actuals under the
old dim remain stable; new actuals under the new dim flow through.

**Ownership.** `corporate_controller` approves the reorg;
`finance_systems_team` updates the crosswalk; `asset_mgmt_director`
validates downstream reports.

---

## 11. Accrual reversal misalignment

**Trigger.** Accrual posted in month A with `REVERSAL` flag set to
reverse in month B; the reversal posts but the original accrual is not
matched (the `REVERSAL_OF` pointer is wrong or missing), creating a
double-count.

**Detection.** `ic_consistency_accrual_reverses_next_period` +
`ic_uniqueness_transaction_id`.

**Handling.** Adapter flags the row with `reversal_misalignment_flag = true`.
Variance calculation for affected `(property_id, account_id, period)` runs
in two modes — with reversal, without reversal — and surfaces the
discrepancy. `monthly_property_operating_review` degrades to
`low_confidence` for the affected lines.

**Ownership.** `corporate_controller` reconciles; reversing journals are
corrected at source.

---

## 12. Variance narrative absent for material line

**Trigger.** Actual vs budget variance for a property/account/period
exceeds `variance_narrative_required_band` but no narrative is present in
Intacct Budget Module or manual upload.

**Detection.** `ic_consistency_budget_vs_reforecast_variance` +
`ic_recon_variance_narrative_coverage`.

**Handling.** `variance_explanation` record is created with
`narrative = null` and `narrative_missing_flag = true`. Monthly report is
produced with `effective_confidence = medium`. After
`variance_narrative_deadline_band` past close, the row becomes blocker and
halts `executive_operating_summary_generation`.

**Ownership.** `regional_ops_director` authors narrative;
`asset_mgmt_director` reviews.

---

## 13. Consolidation entries without supporting detail

**Trigger.** Corporate-level consolidation journal posts a top-line
adjustment (e.g., a fund-level fair-value mark) with no per-property
detail. The amount materially affects the fund's reported NOI.

**Detection.** `ic_completeness_required_dims_actual` at the fund class
level; `ic_consistency_posted_without_approver` if above approval band.

**Handling.** Consolidation entries carry `consolidation_only_flag = true`
in the normalized feed. They are excluded from
`monthly_property_operating_review` (which is property-grain) and surface
only in `quarterly_portfolio_review` and
`executive_operating_summary_generation` at the fund grain. Supporting
memo must be attached to the journal in Intacct; missing memo blocks
`executive_operating_summary_generation`.

**Ownership.** `cfo` approves consolidation entries; `corporate_controller`
ensures memo is attached.

---

## 14. Chart-of-account rename

**Trigger.** Operator renames an account (`5100 Repairs and Maintenance`
becomes `5100 R&M - Operating`) or moves an account to a new code
(`5100` becomes `5105`). Historical postings carry the old code; new
postings carry the new.

**Detection.** `ic_conformance_account_in_coa` on historical postings if
the old code is retired from the chart.

**Handling.** `account_crosswalk` keeps historical rows with
`effective_end` set to the rename date, and a new row is opened for the
new code with `effective_start` on the rename date. Same
`canonical_account_slug` survives across the rename so variance history
is continuous. The adapter resolves `canonical_account_slug` using the
posting's `BATCH_DATE` against the `effective_start` of the crosswalk row.

**Ownership.** `corporate_controller` approves rename;
`finance_systems_team` updates the crosswalk.

---

## 15. Forecast vintage conflict

**Trigger.** Two forecast records post with the same
`(property_id, account_id, period)` but different `AS_OF_DATE` vintages
(e.g., `reforecast_q1` and `reforecast_q2` both cover April FY26). This
is legitimate but downstream aggregation must pick the right vintage.

**Detection.** `ic_uniqueness_forecast_composite_key` (warning, not
blocker).

**Handling.** Both rows are preserved. The `reforecast` workflow selects
the latest `AS_OF_DATE` by default; the `quarterly_portfolio_review`
surfaces both vintages side-by-side with `variance_from_prior` already
computed. Operators can pin a specific vintage via
`manual_overrides.yaml` if needed.

**Ownership.** `finance_systems_team` defines the default selection;
`asset_mgmt_director` authorizes overrides.
