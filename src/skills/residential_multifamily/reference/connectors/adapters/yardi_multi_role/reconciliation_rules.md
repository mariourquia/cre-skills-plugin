# Yardi Reconciliation Rules

How Yardi reconciles against every other system in the stack. Yardi is
the most flexible source family, so every cross-system reconciliation
depends on the operator's classification outcome. All tolerance bands
cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`;
no numeric thresholds are hardcoded.

## Effective-dating semantics

- Every cross-system crosswalk row carries `effective_start` and
  `survivorship_rule`. Historical leases and retired unit structures are
  joined via `effective_end_date` — current-period workflows only read
  rows where `effective_end_date IS NULL OR effective_end_date >
  as_of_date`.
- Cutover windows carry `cutover_effective_date` per property. Post-
  cutover writes from Yardi are blocked; historical reads are retained.
- Accrual month is canonical for period attribution in GL reconciliation.
  Post_date is audit-only unless the operator declares post_date-primary
  convention in Dimension 2b of `classification_worksheet.md`.

## System-by-system reconciliation

| Counterpart | Domain | Yardi role | Reconciliation pattern | Tolerance | Severity |
|---|---|---|---|---|---|
| AppFolio | PMS | overlap during cutover | property-period grain tie-out on rent roll + ledger; post-cutover Yardi writes blocked | `cutover_overlap_band` | warning in window, blocker after |
| Intacct | GL | parallel during yardi_plus_intacct | account-period grain tie-out, accrual book canonical | `gl_parallel_band` | warning within band, blocker outside |
| Procore | construction | Yardi job_cost secondary, Procore primary | propid-job-period tie-out; Procore commitments canonical; Yardi job_cost reconciles posted | `procore_yardi_jobcost_band` | warning |
| Dealpath | deal_pipeline | post-IC acquisition landing into Yardi | deal_id-to-propid handoff with max handoff_lag_days | `handoff_lag_band` | warning within band, blocker outside |
| Excel | market_data | rent-comp benchmarks against Yardi market_rent | submarket-grain rent drift | `comp_drift_band` | warning |
| GraySail | pending classification | deferred | deferred_until_graysail_classification_closes | n/a | n/a |

## AppFolio overlap (PMS cutover)

When both Yardi and AppFolio are live for the same property during a
cutover window:

1. Declare `cutover_effective_date` per property in
   `runbooks/yardi_migration_to_appfolio.md`.
2. Dual-run window has a tolerance band `cutover_overlap_band` during
   which both systems may carry the same property-period.
3. Rent roll tie-out runs at property-period grain:
   - unit count (active rentable)
   - gross potential rent
   - occupied unit count
   - leased unit count (occupied + future)
4. Ledger tie-out runs at property-period-charge_type grain:
   - billed rent
   - collected rent
   - concessions applied
   - delinquency aging buckets
5. Post-cutover, Yardi writes are blocked by rule
   `yd_consistency_historical_only_mode`. AppFolio becomes sole source.
   Yardi retains read-only for historical comparatives.

## Intacct parallel (GL)

When operator runs `yardi_plus_intacct` (Yardi PMS, Intacct GL):

1. Yardi charges/payments reconcile to Intacct posted entries at
   property-account-period grain.
2. Accrual book is canonical. Yardi post_date vs Intacct posting_date
   drift flagged by `yd_consistency_post_vs_accrual`.
3. Intacct wins on any accrual-book actuals dispute post-close (per
   `source_of_truth_matrix.md::posting_period_close_wins`).
4. Cash book reconciliation runs separately; cash vs accrual drift is
   expected and NOT reconciled against accrual totals.
5. Recovery-fee handling: residential portfolios block on non-null
   recovery_code in Yardi; commercial/mixed portfolios reconcile via
   `recovery_fee_band`.

## Intacct parallel (Yardi primary GL)

When operator runs `primary_gl` in Yardi and Intacct is the reporting
layer (rare; reversed posture):

1. Yardi wins post-close; Intacct reconciles trial balance.
2. Reversed recon direction: Yardi sends actuals forward; Intacct
   validates. Mismatches flagged against `gl_parallel_band`.
3. Journal ref drift: Yardi journal_ref and Intacct journal_ref need
   not match but the posting totals per period-account must.

## Procore handoff (construction)

When operator runs Procore + Yardi (Yardi carries some job_cost):

1. Procore primary for scope, commitments, change orders, draws.
2. Yardi secondary for posted job-cost entries (when operator runs
   Procore-free on a subset of capex projects).
3. Reconciliation at propid-job-period grain against Procore posted
   commitments. Drift beyond `procore_yardi_jobcost_band` flagged.
4. Procore project -> Yardi job mapping via `capex_project_crosswalk`.

## Dealpath post-IC landing

When Dealpath-approved deal closes and the property lands in Yardi
(instead of AppFolio):

1. Dealpath deal_id -> Yardi propid handoff recorded via
   `asset_crosswalk`.
2. Handoff-lag tolerance `handoff_lag_band` — beyond band, blocker per
   rule `yd_recon_dealpath_to_yardi_handoff`.
3. Operating data starts flowing in Yardi post-setup; Dealpath retains
   pre-close audit trail.

## Excel market benchmarks

1. Excel rent-comp benchmarks at submarket grain.
2. Yardi market_rent drift against Excel benchmarks flagged via
   `comp_drift_band`.
3. Drift in band: reduce confidence on rent-optimization workflows.
   Drift outside band: block per
   `workflow_activation_map.yaml::blocking_issues`.

## GraySail (pending classification)

Reconciliation deferred until
`../../_core/stack_wave4/runbooks/graysail_classification_path.md` closes.
No Yardi-GraySail reconciliation today. If GraySail later classifies as
an SOP/approval-policy store, Yardi approval_outcome records may
reconcile against GraySail approval_matrix rows.

## Reconciliation-dependent confidence

Every reconciliation outcome contributes to the workflow's
`effective_confidence`:

- `pass` (within `silent_audit` band): no impact
- `pass_with_drift` (within `confidence_reduced` band): degrade workflow
  confidence to `medium`
- `fail` (outside `blocker` band): block workflow per
  `workflow_activation_map.yaml::blocking_issues`

The thresholds themselves live in
`reference/normalized/schemas/reconciliation_tolerance_band.yaml` (cited,
not hardcoded here).

## Cross-system anti-patterns guarded against

- Both Yardi and AppFolio writing to the same property-period simultaneously
  post-cutover (`yd_consistency_overlap_with_appfolio`).
- Yardi charge code decoded globally instead of property-scoped
  (`yd_conformance_chargecode_property_scoped`).
- GL actuals pulled from Yardi on post_date when accrual-month is
  canonical (`yd_consistency_post_vs_accrual`).
- RentCafe lead stage ahead of Voyager applicant record beyond
  `rentcafe_to_voyager_latency_band`
  (`yd_consistency_rentcafe_leadstate_vs_voyager`).
- Historical lease joined to current unit when unit retired post-renovation
  (effective-dating protocol in `dc_dim_unit_effective`).
