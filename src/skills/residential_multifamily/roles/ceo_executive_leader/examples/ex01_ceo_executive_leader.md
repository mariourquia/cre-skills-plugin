# Example — Monthly Exec Decision Memo (abridged)

**Prompt:** "Draft this month's exec decision memo. Pull COO and CFO monthly memos and the portfolio monthly review."

**Inputs:** COO monthly decision memo; CFO monthly decision memo; portfolio_manager monthly portfolio review; escalation queue.

**Output shape:** see `templates/monthly_exec_decision_memo.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- role: ceo_executive_leader
- output_type: memo + scorecard
- decision_severity: informational + action_requires_approval (where CEO acts within authority)

## Expected packs loaded

- `roles/ceo_executive_leader/`
- `workflows/monthly_exec_meeting/`

## Expected references

- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/same_store_set.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/derived/role_kpi_targets.csv`
- `reference/derived/portfolio_concentration_targets.csv`

## Gates potentially triggered

- Any mandate-touching action routes board / IC per row 17.
- Any fund-document amendment routes row 19 via legal + board + IC.
- Any material public / regulatory event routes row 3 / row 17 via legal + board.

## Confidence banner pattern

```
Inputs: COO monthly decision memo, CFO monthly decision memo, portfolio_manager monthly
portfolio review — all as of the month-ending date. References: same_store_set@{as_of_date},
watchlist_scoring@{as_of_date}, portfolio_concentration_targets@{as_of_date},
approval_threshold_defaults@{as_of_date} (statuses per record). Figures reconcile to the
source monthly memos; discrepancies follow up.
```
