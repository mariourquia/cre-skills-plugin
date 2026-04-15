# Example — Weekly Delinquency Review (abridged)

**Prompt:** "Run this week's delinquency review for Ashford Park. Include fair-housing scan and list every case that should open an approval."

**Inputs:** resident ledger (current + T12) + DelinquencyCase records + rent roll snapshot + `reference/normalized/jurisdiction_legal_notice_rules__charlotte.yaml` + `reference/normalized/delinquency_playbook_middle_market.csv` + `reference/normalized/payment_plan_policy__{org}.yaml`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: property_manager
- market: Charlotte, submarket: South End
- jurisdiction: Charlotte (Mecklenburg County)
- output_type: kpi_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/delinquency_collections/`
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/collections_benchmarks__southeast_mf.csv`
- `reference/normalized/delinquency_playbook_middle_market.csv`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/jurisdiction_legal_notice_rules__charlotte.yaml`
- `reference/normalized/payment_plan_policy__{org}.yaml`
- `reference/derived/role_kpi_targets.csv`

## Gates potentially triggered

- Row 1 for each legal-notice draft (stages `31_60` pre-legal, `61_90` legal notice).
- Row 2 for any eviction-filing draft (stage `91_plus`).
- Row 3 for any fair-housing flag or accommodation-related exposure.
- Row 13 for any non-standard payment plan.
- Rows 6 or 7 for write-offs at or above thresholds.

## Expected output shape

- Aging distribution (stage counts + dollars).
- Week-over-week stage transitions.
- Per-case action list with gate row and due date.
- Draft resident communication set with `legal_review_required` where applicable.
- Approval request bundle pre-filled per case.
- Fair-housing scan result.
- Confidence banner with overlay freshness.

## Confidence banner pattern

```
References: delinquency_playbook_middle_market@2026-03-31 (starter),
jurisdiction_legal_notice_rules__charlotte@2026-02-15 (sample, operator overlay override pending),
payment_plan_policy@2026-03-31 (starter),
role_kpi_targets@2026-03-31 (starter).
Data freshness: ledger snapshot 2026-04-12 08:00 local; rent roll snapshot 2026-04-12 08:00 local.
Fair-housing baseline: trailing 90 days, last refreshed 2026-04-01.
```
