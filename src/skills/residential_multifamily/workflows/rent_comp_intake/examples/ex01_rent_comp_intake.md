# Example — Rent Comp Intake (abridged)

**Prompt:** "Log the shopped comps from the Charlotte South End tour."

**Inputs:** raw comp records + overlay normalization rules + current market rent benchmark.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- market: Charlotte, submarket: South End
- role: property_manager
- output_type: checklist
- decision_severity: recommendation

## Expected packs loaded

- `workflows/rent_comp_intake/`
- `overlays/segments/middle_market/`

## Expected references

- `reference/raw/rent_comp/`
- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/comp_normalization_rules__middle_market.yaml`

## Gates potentially triggered

- Magnitude delta above overlay threshold -> reference update approval.

## Expected output shape

- Validated raw records written to `reference/raw/rent_comp/<yyyy>/<mm>/`.
- Normalized upserts to `market_rents__charlotte_mf.csv`.
- Change-log entries appended.
- Approval request for any comp whose delta exceeds threshold.

## Confidence banner pattern

```
References: comp_normalization_rules__middle_market@2026-03-31 (starter).
Raw source types surfaced per record.
```
