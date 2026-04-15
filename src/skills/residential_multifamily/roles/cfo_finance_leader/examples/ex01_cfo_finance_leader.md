# Example — Weekly Exec Finance Brief (abridged)

**Prompt:** "Build this week's exec finance brief. Pull covenant cushion posture and any treasury exceptions."

**Inputs:** weekly covenant cushion snapshot (reporting_finance_ops_lead); treasury feed; exception feed (audit, insurance, tax).

**Output shape:** see `templates/weekly_exec_brief_finance.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- role: cfo_finance_leader
- output_type: scorecard + memo
- decision_severity: informational + action_requires_approval (where CFO is acting)

## Expected packs loaded

- `roles/cfo_finance_leader/`
- `workflows/weekly_exec_brief_finance/`

## Expected references

- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/covenant_calculation_library.csv`
- `reference/derived/watchlist_scoring.yaml`
- `reference/derived/budget_attainment_history.csv`
- `reference/derived/forecast_accuracy_history.csv`

## Gates potentially triggered

- Any covenant cushion breach risk routes row 14.
- Any refi / recap / workout routes rows 15, 16 via CEO.
- Any audit finding of material severity routes row 17 via CEO / board.
- Any investor / lender final routes rows 14, 15, 16.

## Confidence banner pattern

```
References: covenant_calculation_library@{as_of_date, per loan},
variance_materiality_policy@{as_of_date}, budget_attainment_history@{as_of_date},
forecast_accuracy_history@{as_of_date} (statuses per record).
```
