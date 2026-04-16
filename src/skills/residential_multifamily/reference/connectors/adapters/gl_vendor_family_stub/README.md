# GL Vendor Family Stub

Adapter id: `gl_vendor_family_stub`
Vendor family: `generic_erp_stub`
Connector domain: `gl`
Status: `stub`

## Scope

Stub overlay on the canonical `gl` connector at `../../gl/`. Documents
the account-coding conventions, journal-description habits, and posting-
date taxonomies most commonly seen in mid-market ERP and GL exports.
Canonical `gl` schema remains the contract.

Orientation examples (not endorsements, not in file paths): ERP families
typically encountered include platforms in the Sage Intacct, NetSuite,
Microsoft Dynamics, Yardi Voyager, MRI, Workday Financials, and SAP
ByDesign ecosystems. Operators fork this stub to an internal codename
before populating real payloads.

## Assumed source objects

- `budget_line` (annual and monthly planned amounts per account)
- `forecast_line` (rolling reforecasts by period)
- `variance_explanation` (manager commentary on budget vs actual)
- `capex_project` (project master with budget and committed)
- `change_order` (scope or budget deltas on a capex project)
- `draw_request` (construction draws with retention)

## Raw payload naming

Typical export filenames follow patterns such as:

- `trial_balance_<yyyymm>.csv`
- `gl_journal_detail_<yyyymm>.csv`
- `budget_<fiscal_year>.xlsx`
- `reforecast_<fiscal_year>_v<version>.xlsx`

The synthetic example lives at `example_raw_payload.jsonl` with
`status: sample`.

## Mapping template usage

Apply `mapping_template.yaml` on top of the canonical GL mapping at
`../../gl/mapping.yaml`. Canonical mapping wins on conflict. For account
coding, map through `map_account_slug`; the crosswalk resolves segmented
accounts to canonical slugs.

## Known limitations

- Stubs carry synthetic data only.
- Account taxonomies vary. Mapping hints cover common shapes (5-digit,
  7-digit, segmented) but real accounts require the crosswalk.
- Budget versions and scenario tags are often embedded in worksheet
  names rather than columns; manual-upload adapter covers that path.

## Common gotchas

- Multi-entity consolidation rolls inflate totals. Always filter or
  dedup by reporting-entity column.
- Account-rename history is typically undocumented inside the ERP.
  Maintain history in the `account_crosswalk`.
- Late accruals post to the wrong `operating_month`. Reconcile
  `posting_date` vs `operating_month` as a blocking check in variance
  analysis.
- Capex-opex coding drift is common. Use the `capex_project`
  crosswalk to reclassify.
- Reversing entries show up twice; handle the sign flip explicitly.
