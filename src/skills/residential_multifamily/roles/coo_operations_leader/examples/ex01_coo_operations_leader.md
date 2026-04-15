# Example — Weekly Exec Ops Brief (abridged)

**Prompt:** "Build this week's exec ops brief. Pull watchlist and TPM remedy items; flag anything life-safety / fair-housing / legal."

**Inputs:** weekly cross-regional scorecard; weekly portfolio scorecard; weekly TPM scorecard snapshot; exception feed across ops / asset / TPM / legal.

**Output shape:** see `templates/weekly_exec_brief_ops.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- role: coo_operations_leader
- output_type: scorecard + memo
- decision_severity: informational + action_requires_approval (on approvals COO is acting on)

## Expected packs loaded

- `roles/coo_operations_leader/`
- `workflows/weekly_exec_brief_ops/`

## Expected references

- `reference/derived/same_store_set.csv`
- `reference/derived/watchlist_scoring.yaml`
- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- COO acts on approvals within authority; above authority items are routed.
- Any fair-housing enterprise issue routes legal + CEO (row 3).
- Any senior staffing action routes HR + CEO (row 18).
- Any SOP substantive change routes row 17.

## Confidence banner pattern

```
Inputs: weekly cross-regional scorecard, portfolio watchlist, TPM snapshot, legal update
— all as of the week-ending date. References: same_store_set@{as_of_date},
watchlist_scoring@{as_of_date}, role_kpi_targets@{as_of_date} (statuses per record).
```
