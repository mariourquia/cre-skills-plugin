# Market Data Provider Stub

Adapter id: `market_data_provider_stub`
Vendor family: `generic_market_data_stub`
Connector domain: `market_data`
Status: `stub`

## Scope

Stub overlay on the canonical `market_data` connector at
`../../market_data/`. Documents the rent-comp formats, concession-encoding
conventions, submarket-tagging habits, and effective-date handling most
commonly seen across subscription market-data providers and manual
survey sheets. Canonical `market_data` schema remains the contract.

Orientation examples (not endorsements, not in file paths): providers
commonly encountered include CoStar, Axiometrics (RealPage), Yardi
Matrix, Apartments.com (CoStar), and HelloData.ai families, plus manual
leasing-team survey spreadsheets. Operators fork this stub to an
internal codename.

## Assumed source objects

- `market_comp` (per-observation rent-comp record)

## Raw payload naming

- `rent_comps_<submarket>_<yyyymmdd>.csv`
- `manual_survey_<submarket>_<yyyymm>.xlsx`
- `comp_export_<provider>_<yyyymmdd>.csv`

Synthetic example at `example_raw_payload.jsonl`, `status: sample`.

## Mapping template usage

Apply `mapping_template.yaml` over the canonical market_data mapping at
`../../market_data/mapping.yaml`. Canonical mapping wins on conflict.

## Known limitations

- Stubs carry synthetic data only.
- Concession encoding is highly provider-specific; the hints here cover
  common shapes but not every variation.
- Submarket taxonomies never align out of the box; expect to maintain
  an internal crosswalk.

## Common gotchas

- Conflicting sources for the same comp. Rank by `observation_method`
  and `effective_date` freshness; a lease-audited observation outranks
  a survey estimate.
- Stale comps. A comp is only as current as its underlying lease;
  always carry `effective_date` and filter on freshness.
- Outlier rents from broker puffery. Apply outlier flags before the
  comp enters a benchmarking roll-up.
- Missing submarket tags. Route through `map_submarket` against the
  internal submarket taxonomy.
- Manual survey sheets vary widely in layout. Expect template drift;
  this typically lives on the manual-upload adapter, not this one.
- Concession encoding: weeks-free, months-free, percent-off, one-time
  credit. Normalize into `concession_periods` plus `concession_type`.
- Unit-type labels rarely align across providers. Maintain a
  unit-type crosswalk if consuming multiple feeds.
- Providers may redact building-level identity. Preserve any
  anonymization flags through normalization.
