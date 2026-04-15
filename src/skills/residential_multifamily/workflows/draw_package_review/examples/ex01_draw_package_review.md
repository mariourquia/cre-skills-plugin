# Example — Draw Package Review (abridged)

**Prompt:** "Review the April draw for the Willow Creek construction project. It's due to the lender on the 25th."

**Inputs:** full draw package + contract register + cost-to-date + COs + lien waivers + insurance certs + compliance attestations + schedule + lender overlay.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- market: Charlotte
- project_id: willow_creek_construction
- loan_id: loan_willow_creek
- role: construction_manager / asset_manager
- output_type: memo
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/draw_package_review/`
- `workflows/cost_to_complete_review/` (triggered if variance)
- `workflows/schedule_risk_review/` (triggered if variance)
- `workflows/change_order_review/` (COs included in the draw)
- `overlays/segments/middle_market/`
- `overlays/lifecycle/construction/`
- `overlays/management_mode/owner_oversight/`

## Expected references

- `reference/normalized/capex_line_items__scope.csv`
- `reference/normalized/labor_rates__charlotte.csv`
- `reference/normalized/material_costs__southeast_residential.csv`
- `reference/normalized/lender_draw_requirements__loan_willow_creek.yaml`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Row 12: internal draw submission readiness.
- Row 14: lender final submission.
- Rows 10 / 11: any COs embedded in the draw.
- Row 4: any safety-critical scope change inside a CO.

## Expected output shape

- Five-stage validation summary.
- CM review checklist per attachment.
- AM review memo with cost-to-complete, contingency, CO%, schedule variance, cycle time.
- Attachment gap list (if any).
- Approval request bundle (row 12 + row 14).

## Confidence banner pattern

```
References: lender_draw_requirements__loan_willow_creek@2026-01-15 (sample, loan-doc overlay pending),
capex_line_items@2026-03-31 (starter), labor_rates__charlotte@2026-03-31 (sample),
contingency_assumptions@2026-03-31 (starter).
Insurance certificate expirations and lien waiver period coverage surfaced per vendor.
```
