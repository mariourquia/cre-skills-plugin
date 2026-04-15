# budget_file template

status: template

## Purpose

Annual operating budget per property per GL account code. Landed as CSV. This markdown is the operator-facing companion to `budget_file_template.csv`: explains each column, acceptable values, and how the CSV maps to the canonical schema.

## Expected CSV header

```
property_id,account_code,budget_year,budget_version,annual_amount_usd,period_split,notes
```

## Column reference

| Column | Type | Required | Description |
|---|---|---|---|
| `property_id` | string | yes | Property code, matches property master. |
| `account_code` | string | yes | GL account code, matches chart of accounts. |
| `budget_year` | integer | yes | Budget year in YYYY form. |
| `budget_version` | enum | yes | One of: draft, approved, reforecast_q1, reforecast_q2, reforecast_q3, final. |
| `annual_amount_usd` | currency | yes | Annual budget amount in dollars. The connector stores in cents. |
| `period_split` | string | no | Method for splitting annual amount into periods: even, seasonal, custom. |
| `notes` | string | no | Narrative notes for this budget line. |

## Cadence

Annual at launch, mid-year reforecast uploads as needed. Multiple `budget_version` values for the same (property_id, account_code, budget_year) tuple are permitted and disambiguate each other.

## Crosswalk requirements

- `property_id` must exist in property master at landing.
- `account_code` must exist in `gl.chart_of_accounts` (or in the manual_uploads-bootstrapped COA fallback).

## Schema pointer

See `src/skills/residential_multifamily/reference/connectors/manual_uploads/schema.yaml` under `entities.budget_file` for the full entity contract.
