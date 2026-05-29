# Warehouse Schema & Naming Conventions

This reference defines the target datasets the pipeline assembles, the canonical
provenance columns every row carries, the warehouse table-naming convention, and
the canonical `source_ref` join-key form. It is documentation that GUIDES Claude;
none of these tables are created or queried by a live engine. Treat every schema
here as a contract a human or downstream pipeline will implement.

## The canonical provenance columns (every row, every dataset)

These eight columns are appended to every assembled row regardless of dataset.
Their names and meanings are fixed and must survive every downstream handoff.

| Column | Meaning | Allowed values / form |
|---|---|---|
| `source_doc` | Originating document id | e.g. `T12-001`, `OM-001`, `RR-001`, `LSE-003` |
| `locator` | Exact in-document span the extractor cited (copied verbatim) | `OM-001#p14`, `T12-001!Summary!B6`, `RR-001!Detail!E2:E219` |
| `source_ref` | **Canonical join key** back to the data room | `data-room/<doc>#<anchor>` (see below) |
| `extracted_by` | Upstream skill that produced the row | `document-to-data-room-extractor` \| `lease-abstract-extractor` \| `rent-roll-analyzer` \| `t12-normalizer` |
| `classification` | What kind of value this is | `source-fact` \| `calculated` \| `modeled-assumption` \| `requires-review` |
| `confidence` | Trust in the value | `high` \| `medium` \| `low` |
| `review_status` | Human/validation review state | `accepted` \| `needs-review` \| `flagged` |
| `extracted_at` | When the upstream extraction was produced (ISO 8601) | e.g. `2026-05-20T14:02:00Z` |

### Canonical `source_ref` form

`source_ref` is the single column the entire downstream chain joins on. Normalize
the extractor's `locator` into:

```
data-room/<doc>#<anchor>
```

- `<doc>` is the document id (`source_doc`).
- `<anchor>` is the in-document address: a page (`p14`), a sheet+cell (`Summary!B6`),
  or a sheet+range (`Detail!E2:E219`).

Examples:

| Upstream locator | Canonical `source_ref` |
|---|---|
| `OM-001#p14` | `data-room/OM-001#p14` |
| `T12-001!Summary!B6` | `data-room/T12-001#Summary!B6` |
| `RR-001!Detail!E2:E219` | `data-room/RR-001#Detail!E2:E219` |
| `LSE-003#p2 "base rent $32 PSF"` | `data-room/LSE-003#p2` |

A `source_ref` that does not resolve to this shape fails the
`source_ref_resolves` validation rule and the row cannot be deck-ready. The anchor
must be non-empty: `data-room/OM-001#` (no anchor) is invalid.

## Classification semantics

| Classification | Definition | Deck behavior |
|---|---|---|
| `source-fact` | Read directly from a document by an extractor | Deck-ready if gate passes |
| `calculated` | Deterministically derived from source facts (column sum, ratio of two source facts) | Deck-ready if gate passes; show the derivation if asked |
| `modeled-assumption` | Introduced by a model or analyst; not present in any document (e.g. an assumed exit cap, a market growth rate) | May pass the gate but MUST remain labeled "modeled"; never relabel as a fact |
| `requires-review` | The classification itself is uncertain | Treated as a soft failure -> `needs-review`; not deck-ready under `committed` |

Assembly never upgrades a classification. A missing classification maps to
`requires-review`, never to `source-fact`.

## Target datasets and grains

The pipeline assembles incoming extractor rows into these datasets. `grain` is the
row-level meaning — what one row represents. The "fed by" column names the upstream
extractor(s) whose rows land here.

| Dataset key | Grain (one row = ...) | Fed by |
|---|---|---|
| `property_master` | one attribute of the asset (year built, units/SF, submarket) | document-to-data-room-extractor (OM/ALTA) |
| `revenue_lineitems` | one revenue line item per period | t12-normalizer, document-to-data-room-extractor |
| `expense_lineitems` | one expense line item per period | t12-normalizer, document-to-data-room-extractor |
| `rent_roll_aggregate` | one rent-roll aggregate metric as-of a date | rent-roll-analyzer, document-to-data-room-extractor |
| `lease_economics` | one lease's redacted economic structure | lease-abstract-extractor, document-to-data-room-extractor |
| `debt_terms` | one quoted/structured debt term | document-to-data-room-extractor (agency quote) |
| `physical_condition` | one PCA finding (immediate repair, reserve, useful life) | document-to-data-room-extractor (PCA) |
| `title_findings` | one ALTA/title finding (easement, encroachment, flood zone) | document-to-data-room-extractor (ALTA) |

### Per-dataset business columns (in addition to the 8 provenance columns)

```yaml
property_master:
  grain: one attribute of the asset
  columns: [attribute, value, unit]            # e.g. year_built, units, submarket

revenue_lineitems:
  grain: one revenue line item per period
  columns: [line_item, amount, period]         # amount USD; period e.g. "2025 TTM"

expense_lineitems:
  grain: one expense line item per period
  columns: [line_item, amount, period]

rent_roll_aggregate:
  grain: one aggregate metric as-of a date
  columns: [metric, value, unit, as_of]        # e.g. physical_occupancy %, in_place_gpr USD

lease_economics:
  grain: one lease (tenant redacted to a code)
  columns: [tenant_code, suite_sf, commencement, expiration, base_rent_psf, escalation, recovery_structure, renewal_options]

debt_terms:
  grain: one quoted/structured debt term
  columns: [lender, program, term_name, term_value, unit]   # e.g. max_ltv 0.75, min_dscr 1.25x

physical_condition:
  grain: one PCA finding
  columns: [finding_type, system, amount, unit, useful_life_years]

title_findings:
  grain: one ALTA/title finding
  columns: [finding_type, detail, flag]
```

## Warehouse table naming convention

Default convention: `cre_<dataset>_<grain>`.

- All lowercase, `snake_case`.
- **Asset-type-agnostic.** Never bake `multifamily`, `office`, `retail`, or
  `industrial` into a table name; asset type is a column, not a table. (The
  registry validator bans hardcoded asset-type strings elsewhere; keep table
  names neutral for the same reason.)
- Stable across deals, so the warehouse accumulates comparable rows over time.
- The `<grain>` suffix disambiguates grain when a dataset could be summarized at
  more than one level.

| Dataset key | Table name |
|---|---|
| `property_master` | `cre_property_master_attribute` |
| `revenue_lineitems` | `cre_revenue_lineitems_period` |
| `expense_lineitems` | `cre_expense_lineitems_period` |
| `rent_roll_aggregate` | `cre_rent_roll_aggregate_asof` |
| `lease_economics` | `cre_lease_economics_lease` |
| `debt_terms` | `cre_debt_terms_term` |
| `physical_condition` | `cre_physical_condition_finding` |
| `title_findings` | `cre_title_findings_finding` |

Override the convention only to match an existing enterprise warehouse standard,
and state the override explicitly in the output so the exhibit-mapper and deck
composer know the table names they will bind to.

## Self-describing output requirement

Because there is no live catalog behind these tables, the assembled output must
restate each active schema (columns + grain + table name) inline. A downstream
reader — human or `warehouse-to-exhibit-mapper` — should be able to understand the
dataset from the output alone, without consulting this file.
