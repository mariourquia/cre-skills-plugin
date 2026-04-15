# Identity Resolution Framework

This document defines the end-to-end logic for turning source-system records into canonical records. It is the governance framework for every crosswalk file in this directory.

## 1. Separation of canonical id and source id

Two identifier layers coexist throughout the subsystem:

| Layer | Example | Owned by | Stable across |
|---|---|---|---|
| `source_primary_key` | `P1038`, `L000883123`, `V000217` | The source system | The source system only |
| `canonical_id` | `prop_cta_001`, `lease_cta_lx_9913`, `vendor_v_00217` | This subsystem | The life of the business record |

Source primary keys are never exposed to downstream skills. Every downstream artifact reads canonical IDs. The crosswalk layer is the single join boundary between the two.

Canonical IDs are snake_case, opaque, and never reused. Once assigned, a canonical ID is not deleted; when a record is retired, the crosswalk row is closed with an `effective_end` and a status annotation. If the same underlying business record is later recognized, the original canonical ID is reopened with a new `effective_start`.

## 2. Match key strategies

All crosswalk rows declare a `match_method` from the following enum:

### exact

Both sources emit a stable identifier that matches deterministically. Typical cases:

- Operators configured a shared property code across systems.
- A construction tracker and the GL both carry the owner-assigned project code.
- A vendor has a shared tax identifier that both AP and construction carry.

Exact matches yield `high` confidence.

### fuzzy

Identifiers differ. A similarity score over a configured set of attributes determines the match. Attribute sets are object-specific and documented in each crosswalk file:

- `property`: name similarity + address similarity + unit count + year built.
- `vendor`: name similarity + tax id last four + address similarity + services overlap.
- `resident_account`: composite (see below); fuzzy on name_last_normalized only used as a tiebreaker.

Fuzzy matches yield `medium` confidence at best. A fuzzy match below the reject threshold is not recorded; the row goes to the unresolved queue.

### composite

A tuple of exact-match attributes forms the identity. Typical cases:

- `resident_account`: `phone_normalized + email_normalized + lease_id` (never using protected-class attributes).
- `unit`: `property_canonical_id + unit_label_normalized + bedroom_count`.
- `capex_project`: `property_canonical_id + project_name_normalized + target_completion_year`.

Composite matches yield `high` confidence if every attribute is stable; `medium` if any attribute is mutable (for example, unit labels change after renumber).

### manual

A reviewer writes the row by hand. Always requires a named reviewer, a reason, and an entry in `change_log.md`. Confidence is at most `medium` unless supported by a corroborating automated match recorded in the same row.

## 3. Survivorship rules

Survivorship rules are field-level. They are declared in `survivorship_rules.md`. A survivorship rule is a deterministic ordering of sources for each field on each object. The same inputs always produce the same output. If a field is missing from the ranked sources, the next source in the ranking provides it; if no source provides it, the field is null and downstream skills must handle null per the ontology's null-handling rule.

Example (property.property_name):
1. primary source: `pms` (operational name is closest to ground truth)
2. secondary source: `gl` (used when the pms lacks the property)
3. tertiary source: `manual_fallback` (registry of names for third-party managed)

Example (property.legal_entity_id):
1. primary source: `gl` (legal entity is an accounting artifact)
2. secondary source: manual override

Survivorship rules never produce a field value by combining values from multiple sources. The winning source provides the field in full; losing sources are recorded for lineage only.

## 4. Confidence scoring

Confidence is computed once per crosswalk row and recorded in the row itself. It is not recomputed at read time. The scoring function:

| Match method | Best-case confidence | Degrades to medium when | Degrades to low when |
|---|---|---|---|
| exact | high | the shared identifier is operator-configured rather than vendor-native | the shared identifier has been reassigned or duplicated |
| composite | high (stable attrs), medium (mutable attrs) | any attribute in the tuple is mutable | any attribute in the tuple is missing or ambiguous |
| fuzzy | medium | similarity score below the high threshold | similarity score below the medium threshold |
| manual | medium | reviewer lacks corroborating evidence | reviewer flags the match as provisional |

Rows with confidence `unresolved` are not persisted in the crosswalk files. They are parked in `unresolved_exceptions_queue.md` with full context.

## 5. Effective dating

Every crosswalk row carries `effective_start` (required) and `effective_end` (optional, null = current). The framework uses effective dating to handle:

- A property code migrated from one PMS to another. The prior row is closed with `effective_end = migration_date`, a new row is added with `effective_start = migration_date` pointing at the new `source_id` and `source_primary_key`.
- A unit renumbered after renovation. The prior unit row is closed; a new row is added pointing at the same `canonical_id` but the new `source_primary_key`.
- A vendor rename. The prior row is closed; the new row carries the new name and references the prior canonical id (the canonical id does not change).
- A canonical record being retired. The prior row's `effective_end` is set and the `notes` field records the reason. A new row for the same canonical id can be reopened later.

Downstream workflows querying "current" crosswalk rows select rows where `effective_end is null or effective_end > as_of_date`.

## 6. Change management

- Any change to a crosswalk row is logged in `change_log.md` with `{canonical_id, source_id, source_primary_key, change_type, reviewer, reviewed_at, prior_value_summary, new_value_summary, reason}`.
- Rows cannot be deleted. Corrections are done by closing the incorrect row and opening a corrected row. The change log records both events.
- Manual overrides live in `manual_overrides.yaml` and carry an approver, a reason, and an expiration. When an override expires, the default survivorship applies unless the override is renewed.
- Rows with confidence `low` are reviewed at least once per rollout wave. `last_validated_at` records the review date; a row whose `last_validated_at` is older than the configured staleness window is escalated.

## 7. Common hard cases

The framework is designed around the following recurring problems. Every one is covered by at least one specific crosswalk file and an entry in `survivorship_rules.md`.

### 7.1 Same property, different names

PMS carries `Ashford Park`; GL carries `Ashford Park Holdings LLC - Ops Account`. The names are different but refer to the same operating asset. Resolution: `property_master_crosswalk.yaml` with a manual entry (or fuzzy match on address). Canonical id points both rows to a single property.

### 7.2 Legal entity spans multiple operating properties

A single LLC owns three properties in the same submarket and is represented as one row in the GL. Each property has its own PMS record. Resolution: each property gets its own `canonical_id`; each `property_master_crosswalk.yaml` row for the GL side carries the legal entity id plus a `notes` field recording the multi-property relationship. The GL connector's schema carries the legal entity at the property level, not the legal-entity level; downstream finance workflows read the legal entity from the property record.

### 7.3 Unit renumbering after renovation

A property undergoes a full-floor renovation. Units previously numbered 301-320 are renumbered 3A-3T. PMS emits new unit ids. Resolution: `unit_crosswalk.yaml` closes the prior rows with `effective_end = renovation_complete_date` and opens new rows with `effective_start = renovation_complete_date`, same `canonical_id` in each case. Historical reports that query units as of a date before the renovation see the old labels; current reports see the new labels.

### 7.4 Unit split or merge

Two units combined into one, or one unit split into two. Canonical ids for the source units are retired on the split / merge date. New canonical ids are opened. The crosswalk notes field records the split or merge event. Historical lease and payment data remain tied to the retired canonical ids; no attempt is made to retroactively reassign history.

### 7.5 Vendor duplicates across AP and construction

Construction tracker emits vendor `V00217` (trade subcontractor). AP emits vendor `AP-CONC-3221` (same subcontractor, different tax year legal name). Resolution: `vendor_master_crosswalk.yaml` assigns one canonical vendor id with two rows, one per source. `survivorship_rules.md` names the AP record as survivor for legal name and tax id, and the construction tracker as survivor for trade classification.

### 7.6 Same capex project in GL and construction

Construction tracker emits `P-REN-001` (renovation project at Charlotte property). GL emits `21-4501-CTA` (capex account suffix + property code). Resolution: `capex_project_crosswalk.yaml` assigns one canonical project id; both rows link. `change_order_crosswalk.yaml` and `draw_request_crosswalk.yaml` resolve linked records.

### 7.7 Portfolio property code changes over time

A property is sold from one owner legal entity to another; the PMS retains the operating record but the GL posts under a new legal entity id. Resolution: the canonical property id persists; `property_master_crosswalk.yaml` closes the prior GL row and opens a new GL row at the transfer date. `survivorship_rules.md` names the GL as the survivor source for legal entity id; the transfer is reflected immediately.

### 7.8 Resident account dedup across PMS and CRM

Prospect submitted two applications. One led to a lease; the other did not. Resolution: `resident_account_crosswalk.yaml` uses composite match on `phone_normalized + email_normalized + name_last_normalized`. The lead record from CRM and the resident account record from PMS converge on a single canonical resident id when the composite is stable. Protected-class attributes are never used as match keys. Never dedup on race, color, religion, national origin, sex, familial status, disability, or any state / local protected class.

### 7.9 Renewal chain across sources

A lease renews; the PMS emits a new lease id. `lease_crosswalk.yaml` carries `prior_lease_canonical_id` and `next_lease_canonical_id` pointers so the renewal chain is navigable without tying the canonical ids to source-specific ids.

### 7.10 Employee shared across properties; contractor flagged

Maintenance lead covers three properties on a rotation. Payroll export carries one employee record with no property field. Resolution: `employee_crosswalk.yaml` carries a list of `{canonical_property_id, fte_share, role_on_property}` for each canonical employee id. Contractors are flagged with `employment_type = contractor` and handled distinctly in downstream payroll rollups.

### 7.11 Regulatory program identity

Under the regulatory overlay, a property, unit, and resident may appear in a compliance reporting source with its own identifier space. Rows for these sources are siloed inside the regulatory overlay and are not available to core skills unless the overlay is active.

## 8. Operational contract

- The master data layer depends on the source registry. A crosswalk row whose `source_system` is not a registered `source_id` is rejected at load.
- The master data layer is consumed by normalization, not bypassed. A normalized record never carries a `source_primary_key` without a corresponding `canonical_id`; if the crosswalk cannot resolve the identity, the record is held at the raw layer and routed to the unresolved queue.
- The master data layer is versioned. Every change flows through `change_log.md`.
