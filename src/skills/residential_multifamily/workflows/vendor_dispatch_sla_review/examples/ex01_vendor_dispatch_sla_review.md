# Example — Vendor Dispatch and SLA Review (abridged)

**Prompt:** "Run the weekly SLA review for Ashford Park."

**Inputs:** WorkOrder log T90 + `reference/normalized/approved_vendor_list__charlotte.csv` + rate cards + `reference/normalized/vendor_sla_policy__{org}.yaml`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: maintenance_supervisor
- market: Charlotte
- output_type: scorecard
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/vendor_dispatch_sla_review/`
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/approved_vendor_list__charlotte.csv`
- `reference/normalized/vendor_rate_cards__charlotte.csv`
- `reference/normalized/vendor_sla_policy__{org}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Vendor contract signature: row 19.
- Preferred-list change requiring asset_manager approval per overlay.

## Expected output shape

- Per-vendor scorecard rows (SLA, repeat, cost discipline, cert freshness).
- Underperformer list with proposed action.
- Cert-refresh request checklist.
- Rotation proposal memo for quarterly consolidation.

## Confidence banner pattern

```
References: approved_vendor_list__charlotte@2026-04-01 (starter),
vendor_rate_cards__charlotte@2026-04-01 (sample),
vendor_sla_policy@2026-03-31 (starter).
Per-vendor cert freshness surfaced in scorecard rows.
```
