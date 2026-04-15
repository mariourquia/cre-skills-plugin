# Example — Bid Leveling and Procurement Review (abridged)

**Prompt:** "Level the three bids received for the Ashford Park roof replacement and recommend award."

**Inputs:** scope statement + three bid submissions + estimator baseline + approved vendor list + cert status + contingency overlay.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- market: Charlotte
- role: construction_manager
- output_type: memo
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/bid_leveling_procurement_review/`
- `workflows/capex_estimate_generation/` (baseline)
- `workflows/vendor_dispatch_sla_review/` (scorecard context)
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/capex_line_items__roofing.csv`
- `reference/normalized/labor_rates__charlotte.csv`
- `reference/normalized/material_costs__southeast_residential.csv`
- `reference/normalized/approved_vendor_list__charlotte.csv`
- `reference/normalized/vendor_rate_cards__charlotte.csv`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Bid award: row 9.
- Contract signature: row 19.

## Expected output shape

- Level sheet (line items x bidders).
- Scope clarification list.
- Qualifications summary.
- Vendor verification status.
- Recommended award memo.
- Approval request bundle.

## Confidence banner pattern

```
References: capex_line_items__roofing@2026-03-31 (starter),
labor_rates__charlotte@2026-03-31 (sample),
approved_vendor_list__charlotte@2026-04-01 (starter).
Per-bidder cert freshness explicit in verification table.
```
