# Example — Quarterly Reforecast (abridged)

**Prompt:** "Reforecast Ashford Park through year-end using March actuals."

**Inputs:** actuals through March + budget + prior forecast + rent roll snapshot + assumption references.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: asset_manager
- market: Charlotte
- output_type: operating_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/reforecast/`
- `workflows/market_rent_refresh/` (invoked if market reference stale)
- `overlays/segments/middle_market/`

## Expected references

Same as `workflows/budget_build/`.

## Gates potentially triggered

- Final submission: row 14 (lender), 15 / 16 (LP / board).

## Expected output shape

- Actuals variance vs. budget (MTD, YTD).
- Forward revenue and expense builds.
- Year-end landing comparison (budget vs. prior forecast vs. new forecast).
- Forecast-accuracy calibration view.
- Sensitivity appendix.
- Owner submission draft if applicable.

## Confidence banner pattern

```
All assumption references surfaced with as_of_date and status.
Change basis memo attached for any revision above overlay materiality.
```
