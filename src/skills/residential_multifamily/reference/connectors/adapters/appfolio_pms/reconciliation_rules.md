# AppFolio Reconciliation Rules

Status: stub
Wave: 4
Scope: cross-system reconciliation patterns where AppFolio is one of the
paired sources. Concrete checks with ids and tolerance references are in
`reconciliation_checks.yaml`. All tolerance bands cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`; this
file carries no hardcoded numeric thresholds.

## 1. AppFolio vs Intacct (PMS vs GL)

AppFolio is the resident-facing ledger. Intacct is the posted GL.
Disagreements follow `posting_period_close_wins` from
`_core/stack_wave4/source_of_truth_matrix.md`: pre-close, AppFolio is
provisional; at period close, Intacct becomes canonical for any actuals
dispute.

| Reconciliation | AppFolio role | Intacct role | Cadence | Tolerance ref |
|---|---|---|---|---|
| Rent collection vs GL revenue | cash receipts + tenant charge stream | posted revenue by account & property dim | monthly (close) | `revenue_basis_band` |
| Concession accrual vs concession GL | ChargeType in {Credit, Concession} sum | concession expense account posting | monthly | `revenue_basis_band` |
| Payment dep vs bank deposit | TenantPayment postings | bank account GL line | daily (close cycle) | `cash_tie_band` (presence) |
| Property list vs GL entity dim | Property feed | Intacct entity dimension | weekly | presence check (no band) |
| Vendor master (dispatch vs tax) | AppFolio vendor directory | Intacct vendor record (tax id, W-9) | weekly | `identity_match_band` |
| NSF reversal vs GL reversal | TenantPayment.PaymentStatus = NSF | GL reversing entry | monthly | `cash_tie_band` |

**Pattern.** AppFolio posts the resident-side record first (receipt, charge, concession). Intacct posts the GL side at close. Disagreements within `revenue_basis_band` reduce confidence to `medium` on affected property-period cells. Disagreements outside the band block
`monthly_property_operating_review` and `monthly_asset_management_review`
per `workflow_activation_additions.yaml::blocking_issues`.

**Key gotcha.** An AppFolio charge flagged `AdjustmentSource =
ManualAdjustment` that does not appear in Intacct is the single most
common source of false-positive tie-out failures. `edge_cases.md`
covers the recognition pattern.

## 2. AppFolio vs Excel (operator benchmarks)

AppFolio is the operator's own rent and concession state. Excel market
surveys and concession benchmark packs are the external reference.
Disagreement here is not a ledger error; it is market-drift signal
that a workflow must surface.

| Reconciliation | AppFolio role | Excel role | Cadence | Tolerance ref |
|---|---|---|---|---|
| Rent comp drift | unit-level MarketRent + executed lease rent | external rent comp pack (per submarket, bedroom count, class) | weekly | `comp_outlier_band` |
| Concession benchmark drift | ConcessionsTotal per lease ÷ base_rent | external concession benchmark (months-off per submarket) | weekly | `segment_match_band` (for mix) |
| Submarket tag consistency | AppFolio SubmarketLabel | Excel rent comp submarket field | weekly | `submarket_tag_band` |
| Market rent vs advertised | AppFolio MarketRent | Excel asking rent per submarket | weekly | `comp_outlier_band` |

**Pattern.** Drift signals refresh `market_rent_refresh` and
`renewal_retention` workflows. Blockers on Excel side are staleness,
not disagreement; AppFolio side rarely blocks from this reconciliation.

**Key gotcha.** AppFolio operator-populated `MarketLabel` and
`SubmarketLabel` drift from the market taxonomy in
`master_data/market_crosswalk.yaml` and `master_data/submarket_crosswalk.yaml`.
Resolve the labels before running comp joins, not after.

## 3. AppFolio vs Procore (vendor overlap, construction-delivered units)

Vendor overlap is the primary reconciliation surface with Procore. The
same vendor may appear in AppFolio (dispatched for work orders) and in
Procore (awarded subcontractor commitments). Three-way match includes
Intacct; see `recon_vendor_three_way` in
`_core/stack_wave4/stack_reconciliation_matrix.md`.

| Reconciliation | AppFolio role | Procore role | Cadence | Tolerance ref |
|---|---|---|---|---|
| Vendor identity | AppFolio vendor directory | Procore subcontractor directory | weekly | `identity_match_band` |
| Handoff at delivery (lease-up) | Unit roster go-live per property | Procore project at `final_completion` | event-driven | `delivery_handoff_band` |
| Capital project vs resident-facing fee | n/a | Procore capex commitments | monthly | n/a (presence) |

**Pattern.** At delivery, Procore hands off the unit roster to AppFolio;
until AppFolio has the units, lease-up cannot begin. `recon_pc_to_af_at_delivery` is the blocker-severity check for this boundary.

## 4. AppFolio vs Dealpath (post-IC property setup landing)

AppFolio is the landing point for a post-IC property setup. Dealpath is
the seed. Until the AppFolio PropertyId exists and resolves via
`property_master_crosswalk`, the Dealpath deal is not consumable by any
downstream operating workflow.

| Reconciliation | AppFolio role | Dealpath role | Cadence | Tolerance ref |
|---|---|---|---|---|
| Deal close to property setup landing | PropertyId assignment + GL Partner link | closed deal record + approval_request | weekly, warn → blocker after lag | `handoff_lag_band` |
| Asset / property identity | AppFolio PropertyId | Dealpath asset_id | event-driven on close | via `asset_crosswalk` + `property_master_crosswalk` |

**Pattern.** Dealpath rows marked `closed` without a downstream AppFolio
PropertyId + Intacct entity dim within `handoff_lag_band` block the
`acquisition_handoff` workflow. AppFolio side surfaces only when the
property appears without a corresponding deal.

## Confidence model

Each reconciliation outcome contributes to the workflow's `effective_confidence`
exactly as defined in `_core/stack_wave4/stack_reconciliation_matrix.md`:

- `pass` (within `silent_audit` band) → no impact
- `pass_with_drift` (within `confidence_reduced` band) → degrade to `medium`
- `fail` (outside `blocker` band) → block the downstream workflow
  per `workflow_activation_additions.yaml::blocking_issues`

Operators cannot suppress these outcomes. Manual release goes through
`runbooks/manual_override_approval.md` per connectors `_core/`.

## Cross-reference

| Topic | See |
|---|---|
| Cross-system matrix | `_core/stack_wave4/stack_reconciliation_matrix.md` |
| Source-of-truth | `_core/stack_wave4/source_of_truth_matrix.md` |
| Concrete checks | `reconciliation_checks.yaml` |
| Edge patterns | `edge_cases.md` |
| Runbooks | `runbooks/appfolio_onboarding.md`, `runbooks/appfolio_common_issues.md` |
