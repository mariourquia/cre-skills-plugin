# Example — Cross-Regional Scorecard (abridged)

**Prompt:** "Build the cross-regional scorecard for this week, all regions."

**Inputs:** weekly regional scorecards (from all regional_managers); enterprise vendor program state; HRIS.

**Output shape:** see `templates/weekly_cross_regional_scorecard.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- role: director_of_operations
- output_type: scorecard
- decision_severity: informational

## Expected packs loaded

- `roles/director_of_operations/`
- `workflows/regional_operating_review/` (consumes)
- `overlays/segments/middle_market/`
- Region-level overlays per the regional_manager packs feeding up

## Expected references

- `reference/normalized/staffing_ratios__middle_market.csv`
- `reference/derived/role_kpi_targets.csv`
- `reference/derived/same_store_set.csv`
- `reference/normalized/ops_sop_library__middle_market.csv`

## Gates potentially triggered

- Any policy clarification rising to substantive change opens approval_request row 17.
- Senior staffing changes route row 18 with HR.
- Cross-regional vendor contract bindings route row 19.

## Confidence banner pattern

```
References: staffing_ratios@{as_of_date}, role_kpi_targets@{as_of_date}, same_store_set@{as_of_date}
(statuses per record). Regional inputs per each regional_manager weekly pack.
```
