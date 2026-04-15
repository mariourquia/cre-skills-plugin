# Example — Unit Turn and Make-Ready (abridged)

**Prompt:** "Start the classic turn on unit 101 at Ashford Park, vacate 2026-04-30."

**Inputs:** turn handoff record + `reference/normalized/unit_turn_cost_library__charlotte.csv` + approved vendor list + rate cards + benchmarks.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: maintenance_supervisor
- market: Charlotte
- output_type: estimate
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/unit_turn_make_ready/`
- `workflows/work_order_triage/` (vendor-verification reuse)
- `workflows/move_in_administration/` (downstream handoff)
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/unit_turn_cost_library__charlotte.csv`
- `reference/normalized/approved_vendor_list__charlotte.csv`
- `reference/normalized/vendor_rate_cards__charlotte.csv`
- `reference/normalized/turn_benchmarks__charlotte.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Disbursement above threshold: row 6 or 7.
- Safety-critical scope change: row 4.

## Expected output shape

- Turn plan checklist with trades, order, durations.
- Line-item estimate against library.
- Dispatch log.
- Weekly pipeline snapshot with stages and aging.
- Reconciliation memo comparing actual vs. estimate vs. library.

## Confidence banner pattern

```
References: unit_turn_cost_library__charlotte@2026-03-31 (sample),
turn_benchmarks__charlotte@2026-03-31 (starter),
approved_vendor_list__charlotte@2026-04-01 (starter).
Vendor license/insurance freshness surfaced at dispatch.
```
