# Example — Weekly Funnel Review (abridged)

**Prompt:** "Run this week's funnel review for Ashford Park. Flag anything off band."

**Inputs:** CRM lead + tour + application snapshot; rent roll availability; renewal pipeline; marketing channel feed.

**Output shape:** see `templates/weekly_funnel_review__middle_market.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: leasing_manager
- market: (asker-provided)
- output_type: kpi_review
- decision_severity: recommendation

## Expected packs loaded

- `roles/leasing_manager/`
- `workflows/lead_to_lease_funnel_review/`
- `workflows/pricing_concession_proposal/`
- `workflows/renewal_retention/`
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`

## Expected references

- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/normalized/marketing_channel_mix__middle_market.csv`
- `reference/derived/role_kpi_targets.csv`

## Gates potentially triggered

- Any proposed concession outside policy routes to property_manager (approval matrix row 13).
- Any pricing exception routes to property_manager.
- Any screening exception routes through assistant_property_manager -> property_manager.

## Confidence banner pattern

```
References: market_rents@{as_of_date}, concessions@{as_of_date}, marketing_mix@{as_of_date}
(statuses per record). Funnel data live CRM. Rent roll snapshot at run time.
```
