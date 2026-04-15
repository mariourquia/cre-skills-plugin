# Change Log Conventions

Every change to a canonical concept, reference value, threshold, routing rule, or overlay is recorded with a `change_log_entry` conforming to `schemas/change_log_entry.yaml`. This is both an audit trail and a data structure the system itself reads (the tailoring skill uses recent entries to summarize drift).

## Locations

- Subsystem-level: `src/skills/residential_multifamily/_core/CHANGELOG.md` — canonical core changes only (ontology, metrics, schemas, routing core, alias registry).
- Pack-level: `<pack_root>/change_log.md` — pack-scoped changes (prose edits, template additions, new overlays added to the pack).
- Reference-level: `reference/archives/<category>/CHANGELOG.md` — one per category. New reference records append here as they pass through review.
- Machine-readable: `reference/archives/change_log.jsonl` — append-only log of every `change_log_entry`.

## Change types

| Type | Meaning |
|---|---|
| `add` | New record, metric, or overlay. `old_value` is null. |
| `update` | Value of an existing record changed. Both `old_value` and `new_value` populated. |
| `supersede` | Full record replaced. `target_ref` points to the new record; `prior_reference_id` in the record itself points to the old. |
| `deprecate` | Record marked inactive. `new_value` is null. |
| `correct` | Record fixed due to data error. Accompanied by a note explaining the error. |
| `rollback` | Reverses a prior change. References the prior change_log_entry via `rollback_of_change_log_id`. |

## Authorship

- `proposed_by` is required. Value is either a human ID (from the org overlay) or an agent ID (e.g., `rent_comp_ingest_agent`).
- `approved_by` is required once status transitions to `approved`. Empty while status is `proposed`.

## Confidence

- `low` — single anecdotal data point, short window, or unverified source.
- `medium` — multi-source, recent, reasonable sample.
- `high` — triangulated sources, recent, representative sample.
- `verified` — cross-checked against authoritative record (e.g., confirmed bid, signed PMA, awarded contract).

## Reason field

Every entry has a `reason_for_change`. Free text, one or two sentences, explaining *why*. "Updating to latest" is insufficient; prefer "CoStar Q1 2026 Charlotte submarket report shows asking rents up ~2.4% QoQ for B-class garden product".

## Affected skills / overlays

Optional but strongly encouraged. A changed reference may affect many packs; listing them makes downstream review easier and is machine-computable from the `reference_manifest.yaml` files.

## Example entry

```yaml
change_log_id: chg_2026_04_15_0001
change_type: add
target_kind: reference_record
target_ref: reference/normalized/market_rents__charlotte_mf.csv#row_a1b2c3
old_value: null
new_value:
  market: Charlotte
  submarket: South End
  segment: middle_market
  property_form: garden
  unit_type_label: B1
  value: 1785
  unit: dollars_per_unit_per_month
  as_of_date: 2026-03-31
source_name: "CoStar 2026-Q1 Charlotte submarket report"
source_type: costar
source_date: 2026-04-05
as_of_date: 2026-03-31
proposed_by: agent:rent_comp_ingest_agent
approved_by: human:mu_owner
proposed_at: 2026-04-05T14:00:00Z
approved_at: 2026-04-05T15:30:00Z
confidence: high
reason_for_change: |
  Quarterly refresh. CoStar submarket asking rent for B-class garden B1 type in South End
  Charlotte. Prior reference was T4 months stale.
affected_skills:
  - roles/property_manager
  - roles/asset_manager
  - workflows/renewal_retention
  - workflows/market_rent_refresh
affected_overlays:
  - segments/middle_market
```

## Deprecation

A record is deprecated when:

- It is superseded by a new record covering the same scope.
- Its source is retracted.
- It is proven incorrect.

Deprecation sets `status: deprecated` on the record and produces a `change_log_entry` with `change_type: deprecate`. Deprecated records are not deleted; they remain in `reference/archives/` for audit.

## Rollback

A rollback restores a prior value and references the entry it reverses:

```yaml
change_log_id: chg_2026_04_16_0001
change_type: rollback
target_kind: reference_record
target_ref: reference/normalized/market_rents__charlotte_mf.csv#row_a1b2c3
old_value: {<post-change value>}
new_value: {<pre-change value>}
rollback_of_change_log_id: chg_2026_04_15_0001
reason_for_change: |
  CoStar correction issued 2026-04-16; original report had an overlapping-property error.
```

## Test enforcement

`tests/residential_multifamily/test_change_log.py` enforces:

- No reference record exists without a corresponding `add` entry.
- Every `status: approved` record has an `approved_by` set and an entry with `approved_at`.
- No silent `update` without both `old_value` and `new_value`.
- Every `supersede` has a `prior_reference_id` chain that resolves.
- `rollback` entries reference a real prior entry.
- Numeric references scanned for implausible jumps (> some threshold) log a warning; review required to approve.
