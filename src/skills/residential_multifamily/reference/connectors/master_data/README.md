# Master Data Crosswalk Framework

The master data layer answers a single question: given a business record (a property, a unit, a lease, a vendor, a capex project, an employee), what identifier does each connected source system use for that record, and which source wins when they disagree?

This is distinct from the source registry. `../source_registry/` is the inventory of *systems*. `master_data/` is the inventory of *records* and the rules that keep records consistent across those systems.

Every concrete normalized record carries a `source_id` (matching an entry in `../source_registry/source_registry.yaml`) and a source-local primary key. The master data layer introduces the `canonical_id`: the stable, subsystem-owned identifier that every source record for the same underlying business record maps to.

## What this layer is responsible for

- **Canonical ID assignment.** For every business record the subsystem cares about, there is exactly one canonical ID. Canonical IDs are snake_case, opaque, stable across environments, and never reused. Examples: `prop_cta_001`, `unit_cta_001_0304`, `lease_cta_lx_9913`, `vendor_v_00217`.
- **Source-to-canonical mapping.** Each crosswalk file lists rows of the form `{canonical_id, source_system, source_id, match_confidence, match_method, effective_start, effective_end, survivorship_rule, manual_override, reviewer, last_validated_at, notes}`. Schema is `crosswalk.schema.yaml`.
- **Match confidence classification.** Every row carries a confidence value of `high`, `medium`, `low`, or `unresolved`. Only `high` and `medium` rows are eligible for automated downstream use; `low` rows require human sign-off and `unresolved` rows go to the exceptions queue.
- **Survivorship rules.** When two or more sources carry the same canonical record and disagree on a field, the survivorship rule (see `survivorship_rules.md`) names which source wins on which field.
- **Effective dating.** Crosswalk rows carry `effective_start` and optional `effective_end`. This handles changes such as a property code that moves from one PMS to another, a unit that is renumbered, or a vendor rename.
- **Manual override path.** `manual_overrides.yaml` carries structured human decisions that override the default survivorship or match outcome. Every override names an approver, a reason, and an expiration.
- **Unresolved exceptions queue.** When an automated match falls below confidence thresholds or the data cannot be resolved without human review, the row is parked in `unresolved_exceptions_queue.md` with its full context, routed to a named owner.

## Canonical ID versus source ID

- `source_id` in the source registry = the system instance (for example, `east_region_pms`).
- `source_primary_key` inside a source = the identifier that system uses for a specific record (for example, a PMS property code such as `P1038`).
- `canonical_id` in the master data layer = the identifier this subsystem uses for the underlying business record (for example, `prop_cta_001`).

Every crosswalk row pins one `source_id` value and one `source_primary_key` value to exactly one `canonical_id`.

## Match logic

Match logic is rule-based, not probabilistic:

1. **Exact match.** Preferred when both sources emit a shared stable identifier (rare across vendors; common when operators configure a single shared code).
2. **Fuzzy match.** Used when identifiers differ but a combination of attributes (name, address, unit count, year built, legal entity id) reaches a configured similarity threshold. Only produces `medium` confidence at best.
3. **Composite match.** Used when a combination of exact attributes reaches identity (for example, `phone + email + name_last_normalized` for a resident account).
4. **Manual match.** An operator writes the row by hand when no automated rule applies. Always requires a reviewer signature.

Match method is recorded on every row. When a row moves from one method to another (for example, a previously `manual` match is promoted to `composite` because new data arrived), `change_log.md` records the transition.

## Survivorship rules

Survivorship rules are maintained in `survivorship_rules.md`. Rules are field-level, not record-level. For example, on a property record, `property_name` may survive from the PMS while `legal_entity_id` survives from the GL. Survivorship is declarative and deterministic: the same inputs always produce the same output.

## Confidence scoring

| Confidence | Meaning | Downstream use |
|---|---|---|
| `high` | Exact match or composite match on stable attributes, validated within the last reconciliation window. | Automated use permitted everywhere. |
| `medium` | Fuzzy match above threshold, composite match on mutable attributes, or manual match from a prior reviewer. | Automated use permitted for reporting; gated for approvals and external communications. |
| `low` | Fuzzy match below the high threshold but above the reject threshold, or manual match with unresolved ambiguity. | No automated use. Surfaces as a warning in any workflow that consumes the record. |
| `unresolved` | No match could be made; identity cannot be assigned. | Record held in `unresolved_exceptions_queue.md` until human resolution. |

## Effective dating and change management

- `effective_start` is required on every row.
- `effective_end` is optional; null means the row is current.
- When a canonical record undergoes a structural change (unit split, property code migration, vendor rename), the prior row is closed with an `effective_end` and a new row is added with the new `effective_start`.
- `change_log.md` carries the audit trail.

## Common hard cases (covered by specific crosswalks)

1. Same property named differently across PMS and GL. → `property_master_crosswalk.yaml`.
2. Legal entity spans multiple operating properties. → `property_master_crosswalk.yaml` plus the GL connector.
3. Unit renumbering after renovation; split or merge. → `unit_crosswalk.yaml`.
4. Vendor duplicates across AP and construction tools; vendor renames. → `vendor_master_crosswalk.yaml`.
5. Same capex project in GL (posting) and construction tracker (execution). → `capex_project_crosswalk.yaml`, plus `change_order_crosswalk.yaml` and `draw_request_crosswalk.yaml` for linked records.
6. Portfolio property code changes over time. → `property_master_crosswalk.yaml` with effective dating.
7. Resident duplicates across PMS and CRM when the resident submitted two applications, moved between units, or has multiple contact channels. → `resident_account_crosswalk.yaml`.
8. Renewal chain: the current lease links to its prior lease. → `lease_crosswalk.yaml`.
9. Employees shared across properties and contractors embedded in payroll exports. → `employee_crosswalk.yaml`.
10. GL accounts that map to the canonical account taxonomy. → `account_crosswalk.yaml`.

## Protected-class dedup guardrail

Resident-account dedup must never use protected-class attributes (race, color, religion, national origin, sex, familial status, disability, or any state / local protected class) as a match key, a tiebreaker, or a survivorship rule. This is a fair-housing constraint. See `resident_account_crosswalk.yaml` and the `Lead` guardrail in `_core/ontology.md`.

## How this layer is consumed

Skills and workflows do not read source-system primary keys. They read canonical IDs. The master-data layer is the join boundary between the connector layer (source-oriented) and the metric, workflow, and template layers (canonical-oriented). A downstream skill that receives a `property_id` already sees the canonical ID; the crosswalk resolution happened upstream during normalization.
