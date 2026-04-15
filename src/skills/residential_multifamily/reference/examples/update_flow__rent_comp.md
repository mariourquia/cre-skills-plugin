# Update Flow Walk-Through — `rent_comp` (CoStar Quarterly Refresh)

Scenario: CoStar publishes its 2026-Q1 Charlotte submarket report on 2026-04-05. The `rent_comp_ingest_agent` picks up the new file and drives a quarterly refresh of `market_rent_benchmark` rows for Charlotte and the underlying `rent_comp` observations that feed them.

## 1. Inbound

The CoStar CSV lands at:

```
reference/raw/rent_comp/2026/03/costar__2026-03-31.csv
```

Row shape (one property-level comp per row):

| source_row_id | property_name | submarket | unit_type_label | asking_rent | effective_rent | occupancy_pct |
|---------------|---------------|-----------|-----------------|-------------|----------------|---------------|
| CS-2026Q1-000412 | Ashford Park | South End | A1 | 1635 | 1595 | 94.5 |
| CS-2026Q1-000413 | Ashford Park | South End | B1 | 1945 | 1895 | 94.5 |

Status at ingest: `proposed`, confidence `medium` (single vendor).

## 2. Validation

Validate each row against `_core/schemas/reference_record.yaml` + `reference/normalized/schemas/rent_comp.yaml`:

- required fields populated (`market`, `submarket`, `segment`, `property_form`, `unit_type_label`, `unit_beds`, `source_date`, `as_of_date`)
- `value` (asking_rent) numeric and within plausible band (flag outside 0.5x-2.0x of prior peer median)
- `unit` set to `dollars_per_unit_per_month`
- `scenario` = `actual`

Rows failing validation are written to `reference/raw/rent_comp/2026/03/_rejected__2026-03-31.csv` with reason.

## 3. Normalization

For each valid row, build a normalized row targeting:

```
reference/normalized/rent_comps__charlotte_mf.csv
```

With `reference_id = rc-<market>-<property_slug>-<unit_type_slug>-<as_of_date_slug>`.

Simultaneously, aggregate property-level comps into submarket/unit-type benchmark rows, writing to:

```
reference/normalized/market_rents__charlotte_mf.csv
```

Each benchmark row carries `sample_size_properties`, `trailing_3mo_change_pct`, `rent_per_sf`.

If a benchmark row supersedes an existing one, set `prior_reference_id` on the new row.

## 4. Approval

Compute the delta between new `value` and prior approved value per (submarket, unit_type_label). If delta magnitude exceeds the configured rent_comp delta threshold (default 8% QoQ), open an `approval_request` and park the row in `status: proposed`. If delta is within band, auto-approve (`status: approved`).

## 5. Change Log Entry

Append a `change_log_entry` for every approved row:

```yaml
change_log_id: chg_2026_04_05_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/market_rents__charlotte_mf.csv#mrb-charlotte-southend-mm-garden-a1-20260331
old_value:
  value: 1595
  as_of_date: 2025-12-31
new_value:
  value: 1625
  as_of_date: 2026-03-31
source_name: "CoStar 2026-Q1 Charlotte submarket report (illustrative)"
source_type: costar
source_date: 2026-04-05
as_of_date: 2026-03-31
proposed_by: agent:rent_comp_ingest_agent
approved_by: human:mu_owner
proposed_at: 2026-04-05T14:00:00Z
approved_at: 2026-04-05T15:30:00Z
confidence: medium
reason_for_change: |
  Quarterly refresh. CoStar submarket asking rent for B-class garden A1 in South End
  Charlotte shifted +1.9% QoQ; within auto-approve band.
affected_skills:
  - roles/property_manager
  - roles/asset_manager
  - workflows/renewal_retention
  - workflows/market_rent_refresh
  - workflows/lead_to_lease_funnel_review
affected_overlays:
  - segments/middle_market
```

Also append to `reference/archives/change_log.jsonl` and to `reference/archives/rent_comp/CHANGELOG.md`.

## 6. Derived Recomputation

`reference/derived/role_kpi_targets.csv` consumes `market_rents__*` indirectly through the `peer_median` and benchmark bands it inherits from `collections_benchmarks__*` and trade-out targets. No recomputation is required for this refresh.

However, if the overlay `overlays/segments/middle_market/service_standards.md` references the Charlotte median for a "market_rent_per_sf" column, the overlay's `reference_manifest.yaml` is checked for recompute triggers. If flagged, the overlay's derived view is regenerated.

## 7. Skill Notification

Every pack whose `reference_manifest.yaml` lists either path is logged as affected:

- `roles/property_manager` (reads `market_rents__{market}_mf.csv`)
- `roles/asset_manager`
- `workflows/market_rent_refresh`
- `workflows/renewal_retention`

The tailoring skill's missing-docs queue is **not** touched; this was a scheduled refresh, not a gap.

## 8. Archival

Prior approved rows are copied to:

```
reference/archives/market_rent_benchmark/2025/12/market_rents__charlotte_mf__2025-12-31.csv
```

and their `status` flipped to `deprecated` in the archive copy. The archive write is idempotent.

## Confidence banner the skill surfaces

```
References: market_rents__charlotte_mf.csv@2026-03-31 (medium confidence, CoStar Q1 2026 refresh, auto-approved within 8% QoQ band).
```
