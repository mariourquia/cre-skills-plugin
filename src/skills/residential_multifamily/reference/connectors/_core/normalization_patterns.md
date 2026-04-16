# Normalization Patterns

Patterns every connector applies when mapping raw fields to canonical types.
These rules are mandatory: a connector whose mapping ignores a pattern that
applies to its data fails the contract test.

Conventions used throughout:

- All examples carry `status: sample` or `status: illustrative`.
- Prose cites no dollar figures or percentage figures. Where numeric behavior
  matters, the examples show the shape of the value, not its magnitude.
- Canonical fields and enums are snake_case ASCII.

Applies to all eight connectors: `pms`, `gl`, `crm`, `ap`, `market_data`,
`construction`, `hr_payroll`, `manual_uploads`.

## Date and datetime

**Policy.** Store timestamps in UTC ISO 8601. Preserve the original offset in
a side field if the source supplied one and the offset is material (e.g.,
lease event timestamps in a market with compliance reporting in local time).
Dates that are date-only stay date-only; do not promote to timestamp at
midnight.

**Canonical grains.**

- `date` - calendar date, no time. Field name ends in `_date`.
- `datetime` - UTC timestamp. Field name ends in `_at`.
- `datetime_with_offset` - datetime plus preserved offset when needed. Two
  fields: `<name>_at` (UTC) and `<name>_at_local_offset` (offset string like
  `+05:30`).

**Worked example.**

Source row (PMS):

```json
{"StartDt": "08/15/2025", "MoveInTs": "2025-08-15 14:30"}
```

Normalized:

```csv
lease_start_date,move_in_at,move_in_at_local_offset
2025-08-15,2025-08-15T18:30:00Z,-04:00
```

Status: `illustrative`.

The source supplied a local time (Eastern Daylight Time, offset `-04:00`).
Normalization converts to UTC and preserves the offset.

Edge cases:

- Ambiguous short dates (`08/15/25` vs `15/08/25`). The mapping rule names the
  source locale explicitly. Ambiguity without locale is a blocker.
- DST transitions. Timestamps on DST-ambiguous instants fall back to the
  vendor's stated convention; absence of a stated convention is a blocker.
- Excel-era serial numbers. Forbidden; the mapping rule converts before
  landing in raw.

## Currency

**Policy.** The operator declares a base currency at subsystem level (default:
`USD` for US operators). Every monetary amount is stored in base currency.
Amounts are stored as decimal strings with explicit precision, not floats.

**Fields.**

- `<name>_base_currency` - amount in the operator's base currency.
- `<name>_base_currency_minor_units` - optional; integer count of minor units
  (cents) for systems that require integer math on money.
- `<name>_source_currency` - optional; the currency as stated by the source.
- `<name>_fx_rate_to_base` - optional; the FX rate applied.
- `<name>_fx_rate_as_of` - optional; the FX rate date.

**FX rate table.** Rates live at
`reference/normalized/fx_rates__<base_currency>.csv` with columns
`from_currency`, `to_base_rate`, `as_of_date`, `source`, `confidence`. The FX
rate used for a transformation is always recorded in
`reference_assumptions_used` on the lineage manifest.

**Minor units.** For integer math on money, use `*_minor_units` with a
precision of two decimal places (or the currency's standard). Conversion
between major and minor units never loses precision; all conversion is
integer-safe.

**Worked example.**

Source row (GL, base currency `USD`):

```json
{"AcctName": "Repairs", "Amount": "1,234.56"}
```

Normalized:

```csv
account_name,amount_base_currency,amount_base_currency_minor_units
repairs,1234.56,123456
```

Status: `illustrative`.

The amount is a decimal string (not a float), with minor units preserved as
integer. No figure appears in prose.

## Unit - square footage and time

**Square-foot variants.**

- `nrsf` - net rentable square feet.
- `rsf` - rentable square feet (may equal `nrsf` in multifamily; differs in
  commercial).
- `usable_sf` - usable area for the resident.
- `gross_sf` - gross building square feet.

Normalize source headers explicitly. Ambiguous `SqFt` headers are mapped to a
named variant or rejected.

**Time units.**

- `days` - integer count of days.
- `months` - integer count of months; used for lease term.
- `years` - integer count of years.

Mixed-grain conversions use the operator-declared convention in
`overlays/org/<org_id>/unit_conventions.yaml`, defaulting to calendar months
(28–31 days per month) for leasing and 30-day months for rent-per-day
calculations unless stated otherwise.

**Worked example.**

Source row (PMS):

```json
{"UnitSqFt": "875", "LeaseTermMos": "12"}
```

Normalized:

```csv
unit_nrsf,lease_term_months
875,12
```

Status: `illustrative`.

## Status standardization

**Policy.** Every object has a canonical enum. Source-side statuses map
through `mapping.yaml` into the canonical enum. Unmapped source values are
rejected (no silent bucketing). The mapping rule for an enum field always
names every known source value.

**Canonical enums (selected examples).**

- `Lease.status`: `pending`, `occupied`, `notice`, `terminated`,
  `holdover`, `evicted`.
- `WorkOrder.status`: `open`, `assigned`, `in_progress`, `on_hold`,
  `completed`, `cancelled`.
- `DelinquencyCase.status`: `open`, `notice_served`, `payment_plan`,
  `in_legal`, `closed_paid`, `closed_writeoff`.
- `CapexProject.status`: `proposed`, `approved`, `bidding`, `contracted`,
  `in_progress`, `substantial_complete`, `closed_out`.

**Worked example.**

Source values from vendor A: `OCC`, `NTV`, `TERM`, `HOLD`, `EVT`.

Mapping fragment:

```yaml
- source_field: Status
  canonical_field: lease.status
  transform_rule: enum_map
  mapping:
    OCC: occupied
    NTV: notice
    TERM: terminated
    HOLD: holdover
    EVT: evicted
  null_handling_rule: reject
  validation_rule: must_be_in_canonical_enum
```

Status: `illustrative`.

## Boolean normalization

**Policy.** Canonical booleans are `true` and `false`. Source-side booleans
arrive as `Y`/`N`, `1`/`0`, `yes`/`no`, `true`/`false`, or text flags.

**Transform rule.** `boolean_map` with explicit mapping.

**Null handling.** Null values remain null unless the field is required. A
required null is a blocker.

**Worked example.**

Mapping fragment:

```yaml
- source_field: PetAllowed
  canonical_field: lease.pets_allowed
  transform_rule: boolean_map
  mapping:
    Y: true
    N: false
    YES: true
    NO: false
    "1": true
    "0": false
  null_handling_rule: pass_through
  validation_rule: must_be_boolean_or_null
```

Status: `illustrative`.

## Text trimming and canonicalization

**Policy.**

- Strip leading and trailing whitespace.
- Collapse internal whitespace runs to a single space.
- Preserve original case in display fields; canonicalize to lowercase in
  identifier fields.
- Canonical identifiers remove diacritics (e.g., `José` → `jose`) via NFKD
  normalization + ASCII fold.
- Punctuation in identifiers is replaced with underscores or removed per the
  field's canonical rule; display fields retain punctuation.

**Display vs identifier distinction.** A field named `property_name` is a
display field and preserves case, punctuation, and diacritics. A field named
`property_slug` is an identifier and is canonicalized.

**Worked example.**

Source row:

```json
{"PropertyName": "  Highland  Gardens  "}
```

Normalized:

```csv
property_name,property_slug
Highland Gardens,highland_gardens
```

Status: `illustrative`.

## Enum mapping with unknown-value handling

**Policy.** Enum mappings are explicit. Unknown source values never map to a
default. Unknown values are quarantined with reason
`enum_value_unmapped:<source_value>`. The connector's change log captures the
unknown value and opens a task to update the mapping.

**Worked example.**

A vendor begins emitting a new lease status `CONV` not in the mapping. A row
with `Status=CONV` lands in quarantine. The connector's change log shows:

```yaml
- change_id: sc_2026_04_15_pms_00012
  change_type: enum_added
  detected_at: 2026-04-15T04:15:22Z
  detected_by: schema_drift_check
  prior_definition:
    enum_values: [OCC, NTV, TERM, HOLD, EVT]
  new_definition:
    enum_values: [OCC, NTV, TERM, HOLD, EVT, CONV]
  mapping_action_required: true
  remediation_plan_ref: reference/connectors/pms/change_log.md#2026-04-15-enum-conv
  status: open
```

Status: `illustrative`.

## Numeric precision

**Policy.**

- **Counts.** Integer. No decimals. `units_total`, `days_vacant`,
  `headcount_approved`.
- **Rates and ratios.** Decimal with explicit precision. Occupancy is stored
  as a decimal in the range zero to one. Percentage display happens at render
  time.
- **Money.** Decimal string with currency-specific precision. See Currency.
- **Square footage.** Integer unless the source is a decimal (e.g., BOMA
  measurements).

**Display vs storage.** Storage holds the canonical decimal (`0.945`). Render
converts to percent (`94.5%`). Prose never writes the figure.

**Worked example.**

Source row:

```json
{"OccPct": "94.5%"}
```

Normalized:

```csv
physical_occupancy
0.945
```

Status: `illustrative`.

## Null, NaN, unknown, and not-applicable

**Policy.** Four distinct states exist and are not conflated.

- `null` - the source did not supply a value.
- `unknown` - the source explicitly reported that a value exists but is not
  known.
- `not_applicable` - the field does not apply to this row by business rule.
- `NaN` - forbidden in storage; treat as blocker at landing.

**Representation.**

- `null` - empty cell in CSV; `null` in JSON.
- `unknown` - explicit string `"unknown"` in a secondary `*_state` column,
  paired with `null` in the value column. Example: `lease_end_date=null`,
  `lease_end_date_state="unknown"`.
- `not_applicable` - explicit string `"not_applicable"` in the paired state
  column.

**Field behavior.** The schema declares which states are valid per field.
Required fields cannot be null. Optional fields may be null. State-carrying
fields use the paired-column pattern.

**Worked example.**

A month-to-month lease has no defined end date. Rather than backfilling with
a placeholder:

```csv
lease_id,lease_end_date,lease_end_date_state
l_0009881,,not_applicable
```

Status: `illustrative`.

A lease where the end date exists in the source system but was redacted
before export:

```csv
lease_id,lease_end_date,lease_end_date_state
l_0009882,,unknown
```

Status: `illustrative`.

A lease with a normal end date:

```csv
lease_id,lease_end_date,lease_end_date_state
l_0009883,2026-08-14,known
```

Status: `illustrative`.

## Cross-pattern worked example - a CRM lead row

Source row from a CRM vendor:

```json
{
  "LeadID": "L-38291",
  "Name": "  María  Núñez ",
  "Email": "maria@example.test",
  "PropCode": "HG1",
  "SourceChannel": "PaidSocial_Insta",
  "IsHotLead": "Y",
  "InquiryTs": "04/15/2026 09:12 ET",
  "Qualified": "unknown",
  "AnnualIncome": "72,500.00 USD",
  "source_name": "crm_primary",
  "source_type": "crm",
  "source_date": "2026-04-15",
  "extracted_at": "2026-04-15T13:20:05Z",
  "extractor_version": "crm-adapter-0.2.4",
  "source_row_id": "crm_primary::lead::L-38291"
}
```

Normalization applies:

- Text trimming and identifier canonicalization to produce `lead.full_name`
  (display preserved) and `lead.full_name_slug` (canonical).
- Date and datetime: `InquiryTs` to UTC with offset preserved.
- Enum map: `SourceChannel` to canonical `paid_social_instagram`.
- Boolean map: `IsHotLead=Y` to `lead.is_hot_lead=true`.
- Unknown state: `Qualified=unknown` produces `lead.qualified=null` and
  `lead.qualified_state=unknown`.
- Currency: `AnnualIncome` parses the currency tag `USD` to
  `income_annual_source_currency=USD` and computes
  `income_annual_base_currency` (base=USD here so the FX rate is 1.0 and the
  value matches).
- Identity resolution: `PropCode=HG1` maps to `property_id=hg1_columbus_oh`.

Normalized row:

```csv
lead_id,property_id,full_name,full_name_slug,email,source_channel,is_hot_lead,inquiry_at,inquiry_at_local_offset,qualified,qualified_state,income_annual_base_currency,as_of_date,normalized_version,lineage_manifest_id,identity_resolution_status,row_status
l_crm_primary_38291,hg1_columbus_oh,María Núñez,maria_nunez,maria@example.test,paid_social_instagram,true,2026-04-15T13:12:00Z,-04:00,,unknown,72500.00,2026-04-15,crm-lead-0.2.0,lm_2026_04_15_crm_primary_00003,resolved,valid
```

Status: `illustrative`.

No dollar figure or percent figure appears in this document's prose. Numeric
behavior lives in the examples, tagged `illustrative`.
