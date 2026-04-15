# Example — Weekly Regional Scorecard (abridged)

**Prompt:** "Build this week's regional scorecard for the 8 Southeast properties. Flag bottom quartile on delinquency and make-ready."

**Inputs:** 8 site scorecards; regional rollover schedule; regional vendor log; regional marketing feed.

**Output shape:** see `templates/weekly_regional_scorecard.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- management_mode: third_party_managed + self_managed (mixed regional portfolio)
- role: regional_manager
- output_type: scorecard
- decision_severity: recommendation

## Expected packs loaded

- `roles/regional_manager/`
- `workflows/regional_operating_review/`
- `workflows/corrective_action_plan/` (triggered if underperformers)
- `overlays/segments/middle_market/`
- Per-site form_factor and lifecycle overlays

## Expected references

- `reference/normalized/collections_benchmarks__southeast_mf.csv`
- `reference/normalized/staffing_ratios__middle_market.csv`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/role_kpi_targets.csv`
- `reference/derived/same_store_set.csv`

## Gates potentially triggered

- Any CAP with above-policy concessions proposed routes to approval_request row 13.
- Any legal-notice-ready delinquency cases route via PM to approval_request row 1.
- Any site-level disbursement above regional threshold routes to asset_manager (rows 6, 7).

## Confidence banner pattern

```
References: collections_benchmarks@{as_of_date} (status: starter, overlay pending);
role_kpi_targets@{as_of_date}; same_store_set@{as_of_date}. Site data: rent rolls at run-time
snapshots; funnel and WO data live.
```
