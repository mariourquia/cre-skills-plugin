# Field Mapping Template

Every connector's `mapping.yaml` (or per-entity mapping file) follows this
template. The template is the contract. A connector that omits a required
column fails the contract test.

Applies to all eight connectors: `pms`, `gl`, `crm`, `ap`, `market_data`,
`construction`, `hr_payroll`, `manual_uploads`.

## Required columns

Every entry in a `mapping.yaml` has these eleven fields.

| # | Field | Purpose |
|---|---|---|
| 1 | `source_field` | The source-side column name as it appears in the raw artifact. |
| 2 | `source_description` | One-line description of what the source emits in this field. |
| 3 | `canonical_field` | The dotted canonical path: `<object>.<field>` (e.g., `lease.start_date`). |
| 4 | `transform_rule` | The normalization rule applied. One of the defined rule slugs. |
| 5 | `type_cast_rule` | The type the canonical field expects. |
| 6 | `null_handling_rule` | How to handle null source values. |
| 7 | `default_rule` | What default, if any, to apply when the source is null and a default is permitted. |
| 8 | `validation_rule` | Invariant the normalized value must satisfy. |
| 9 | `required_for_load` | Boolean. `true` means the row cannot normalize without this field. |
| 10 | `required_for_kpi` | Boolean. `true` means the field feeds a KPI; missing values emit a DQ warning on the relevant metric scope. |
| 11 | `provenance_note` | Free-text note about source idiosyncrasy, vendor-specific behavior, known issues. |

## Allowed rule slugs

These slugs are the only `transform_rule` values a connector may use. New
slugs require an addition to this template.

- `pass_through` - copy source value unchanged after type coercion.
- `trim` - strip leading/trailing whitespace. Combines with other rules.
- `canonicalize_text_identifier` - NFKD + ASCII fold + lowercase + collapse
  whitespace to single underscore.
- `canonicalize_text_display` - strip leading/trailing whitespace only.
- `date_parse` - parse source date format to canonical ISO date. Requires a
  `source_format` sub-rule.
- `datetime_parse_to_utc` - parse source datetime to UTC, preserving original
  offset if present. Requires a `source_format` and `source_tz` or
  `offset_column` sub-rule.
- `currency_parse_to_base` - parse source currency to base currency using the
  FX rate table. Produces paired `<name>_base_currency`,
  `<name>_source_currency`, `<name>_fx_rate_to_base`.
- `enum_map` - explicit mapping from source enum values to canonical enum
  values. Unmapped source values are rejected.
- `boolean_map` - explicit mapping from source boolean expressions to true or
  false.
- `numeric_coerce` - coerce to numeric with explicit precision and rounding
  rule. Requires a `precision` sub-rule.
- `integer_coerce` - coerce to integer with explicit rounding rule.
- `split_paired_state_column` - produce `<name>` and `<name>_state` for
  fields that carry null / unknown / not_applicable semantics.
- `identity_resolve_reference` - look up a canonical identifier in the master
  data layer. Requires a `resolver` sub-rule naming the target object and the
  source keys.
- `derive_from_expression` - compute the canonical value from a deterministic
  expression over other source fields. Requires a named `expression` sub-rule.
- `reject` - never used as a `transform_rule`; use `reject` in
  `null_handling_rule` or `validation_rule` when a condition should block the
  row.

## Allowed `null_handling_rule` values

- `pass_through` - null source yields null canonical (field is optional).
- `reject` - null source causes the row to quarantine.
- `default` - null source yields the `default_rule` value; not legal without
  a non-null `default_rule`.
- `paired_state` - null source sets the paired `<name>_state` column to
  `unknown` or `not_applicable` per the field's rule.

## Allowed `validation_rule` patterns

- `must_be_non_null`
- `must_be_positive`
- `must_be_non_negative`
- `must_be_in_canonical_enum`
- `must_be_date`
- `must_be_datetime_utc`
- `must_be_iso_date_range`
- `must_match_pattern:<regex>`
- `must_be_in_set:[a,b,c]`
- `must_match_master_data:<object>`
- `must_be_boolean_or_null`
- `custom:<slug>` - named invariant defined in the connector's
  `reconciliation_checks.yaml`.

## Example entries

### Example 1 - simple date field

```yaml
- source_field: StartDt
  source_description: Source PMS lease start date in 8-digit YYYYMMDD form.
  canonical_field: lease.start_date
  transform_rule: date_parse
  type_cast_rule: date
  null_handling_rule: reject
  default_rule: null
  validation_rule: must_be_date
  required_for_load: true
  required_for_kpi: true
  provenance_note: vendor A emits as YYYYMMDD; vendor B as MM/DD/YYYY; mapping is vendor-forked downstream.
```

Status: `illustrative`.

### Example 2 - money with currency parse

```yaml
- source_field: MoRent
  source_description: Monthly contract rent as a currency string with thousands separator.
  canonical_field: lease.monthly_rent_base_currency
  transform_rule: currency_parse_to_base
  type_cast_rule: decimal
  null_handling_rule: reject
  default_rule: null
  validation_rule: must_be_non_negative
  required_for_load: true
  required_for_kpi: true
  provenance_note: FX rate sourced from reference/normalized/fx_rates__usd.csv.
```

Status: `illustrative`.

### Example 3 - enum with explicit mapping

```yaml
- source_field: Status
  source_description: Source PMS lease status short code.
  canonical_field: lease.status
  transform_rule: enum_map
  type_cast_rule: string
  null_handling_rule: reject
  default_rule: null
  validation_rule: must_be_in_canonical_enum
  required_for_load: true
  required_for_kpi: true
  provenance_note: new source value CONV observed 2026-04-15; mapping action open; see change log sc_2026_04_15_pms_00012.
  mapping:
    OCC: occupied
    NTV: notice
    TERM: terminated
    HOLD: holdover
    EVT: evicted
```

Status: `illustrative`.

### Example 4 - boolean with Y/N source

```yaml
- source_field: PetAllowed
  source_description: Flag indicating whether the lease permits pets.
  canonical_field: lease.pets_allowed
  transform_rule: boolean_map
  type_cast_rule: boolean
  null_handling_rule: pass_through
  default_rule: null
  validation_rule: must_be_boolean_or_null
  required_for_load: false
  required_for_kpi: false
  provenance_note: vendor emits Y or N.
  mapping:
    Y: true
    N: false
```

Status: `illustrative`.

### Example 5 - identity resolution

```yaml
- source_field: PropCode
  source_description: Vendor-side short code for property.
  canonical_field: property.property_id
  transform_rule: identity_resolve_reference
  type_cast_rule: string
  null_handling_rule: reject
  default_rule: null
  validation_rule: must_match_master_data:property
  required_for_load: true
  required_for_kpi: true
  provenance_note: resolved via reference/connectors/master_data/property_crosswalk.csv.
  resolver:
    target_object: property
    source_keys: [PropCode]
    target_key: property_id
    on_unresolved: quarantine
```

Status: `illustrative`.

### Example 6 - paired-state column

```yaml
- source_field: LeaseEndDt
  source_description: Source PMS lease end date; absent on month-to-month leases.
  canonical_field: lease.end_date
  transform_rule: split_paired_state_column
  type_cast_rule: date
  null_handling_rule: paired_state
  default_rule: null
  validation_rule: custom:paired_state_valid
  required_for_load: true
  required_for_kpi: true
  provenance_note: null in source = not_applicable on month-to-month; explicit placeholder 1/1/2099 = unknown.
  paired_state_rules:
    null_source: not_applicable
    placeholder_values:
      - value: "1/1/2099"
        state: unknown
```

Status: `illustrative`.

### Example 7 - derived from expression

```yaml
- source_field: null
  source_description: Canonical field computed from multiple source fields; not sourced directly.
  canonical_field: lease.term_months
  transform_rule: derive_from_expression
  type_cast_rule: integer
  null_handling_rule: reject
  default_rule: null
  validation_rule: must_be_positive
  required_for_load: true
  required_for_kpi: true
  provenance_note: computed as months between lease.start_date and lease.end_date rounded down.
  expression:
    name: months_between_start_and_end
    inputs: [lease.start_date, lease.end_date]
    rule: floor_months_between
```

Status: `illustrative`.

## Ordering and organization

Within a connector's `mapping.yaml`, entries are grouped by canonical object
(e.g., all `lease.*` entries together). Within a group, entries are ordered:

1. Primary-key fields first.
2. Required-for-load fields next.
3. Required-for-KPI fields next.
4. Optional fields last.

Inside each tier, alphabetical by `canonical_field`.

## Vendor-specific overrides

A connector that supports more than one vendor forks vendor-specific mappings
under `<connector>/vendors/<vendor>/mapping.yaml`. Overrides apply to
specific `canonical_field` entries and inherit every other field from the
parent mapping. Overrides are logged in `mapping_override_log.yaml` per
`lineage.md`.

## Validation at authoring time

Every `mapping.yaml` is validated by
`tests/test_connector_contracts.py` against:

- Every canonical field resolves to a field defined in `_core/ontology.md` or
  an explicit extension manifest.
- Every enum value listed in `mapping` is present in the canonical enum.
- Every `transform_rule` is one of the defined rule slugs.
- Every `validation_rule` is one of the defined patterns or a named custom
  rule.
- `required_for_load: true` implies `null_handling_rule: reject`.
- `transform_rule: enum_map` implies presence of a `mapping` sub-block.
- `transform_rule: date_parse` implies presence of a `source_format` sub-rule.
- `transform_rule: currency_parse_to_base` implies FX rate table exists.
- `transform_rule: identity_resolve_reference` implies presence of a
  `resolver` sub-rule.
