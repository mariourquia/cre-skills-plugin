# Example — Executive Operating Summary (abridged, board packet)

**Prompt:** "Build the Q1 2026 board packet for the residential portfolio."

**Inputs:** AM reviews (3 months per asset) + quarterly portfolio review + same-store set + watchlist scoring + fund debt schedule + capex program summary + board packet template.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- audience: board
- org_id: {org}
- period: Q1 2026
- role: ceo_executive_leader / cfo_finance_leader
- output_type: operating_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/executive_operating_summary_generation/`
- `workflows/quarterly_portfolio_review/` (feeder)
- `workflows/monthly_asset_management_review/` (feeder)
- `overlays/segments/middle_market/`
- `overlays/management_mode/owner_oversight/`

## Expected references

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/derived/same_store_set__{org}.yaml`
- `reference/normalized/board_packet_template__{org}.md`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Board submission: row 16.
- Investor submission (if dual-audience): row 15.
- Lender submission (parallel workflow): row 14.
- Fair-housing / compliance disclosure: counsel-led; row 3 if public-facing.

## Expected output shape

- 1-3 page narrative summary with cited metrics.
- 1-page KPI dashboard.
- Covenant posture view.
- Watchlist distribution + top movers with drivers.
- Capex program summary.
- Lease-up status view (if applicable).
- Forecast discipline summary.
- Forward view.
- Approval request bundle.

## Confidence banner pattern

```
References: watchlist_scoring@2026-03-31 (starter), same_store_set@2026-03-31 (starter),
board_packet_template@2026-03-31 (starter), role_kpi_targets@2026-03-31 (starter).
External-use notation on any sample-tagged reference.
```
