# PMS Identity Resolution

How property, unit, lease, and resident identities in the PMS connector crosswalk to canonical identifiers used by the residential multifamily subsystem.

## Crosswalk pointers

- `reference/connectors/master_data/property_crosswalk.yaml`: property identity across systems.
- `reference/connectors/master_data/unit_crosswalk.yaml`: unit identity and renumbering history.
- `reference/connectors/master_data/resident_crosswalk.yaml`: resident identity across leases and households.
- `reference/connectors/master_data/household_registry.yaml`: household-to-resident roll-up.
- `reference/connectors/master_data/employee_unit_registry.yaml`: employee-unit and model-unit exclusions.

All crosswalks declare survivor ids, merge history, and effective windows. A row in any PMS entity that references a non-survivor id without a merged_into pointer is rejected at landing.

## Match methods

| Method | Use | Confidence |
|---|---|---|
| `exact` | PMS-native primary keys (property_id, unit_id, lease_id, resident_account_id) where the PMS is authoritative. | Highest. Used as the default when PMS is the canonical source. |
| `composite` | (property_id, unit_label) where unit_id has changed across renumbering, or (property_id, normalized_contact_hash, move_in_date) where resident_account_id is missing. | High. Used when a migration or rename has invalidated the native id. |
| `fuzzy` | Normalized-name and date-of-birth hash for resident identity across legacy systems; normalized property-name match for property identity across acquisitions. | Medium. Always queued to operator review before the crosswalk is updated. |
| `manual` | Operator-adjudicated merge recorded in the crosswalk with reviewer and timestamp. | Authoritative once recorded. Supersedes exact and composite on conflict. |

## Confidence scoring

Every candidate crosswalk row carries a `confidence_tier` in (`system_of_record`, `high`, `medium`, `low`). Downstream metrics consume only `system_of_record` and `high` by default; `medium` and `low` rows are queued for operator adjudication before promotion to normalized.

## Hard cases

### Same property named differently across systems

A property may appear as `The Reserve at Crest` in the PMS, `Reserve Crest` in the AP system, and `RESERVE CREST MF` in the GL. The property_crosswalk declares a canonical property_id with aliases; each connector maps its native name to the canonical id before landing. Failure mode: a new alias not yet registered lands records against a new phantom property_id, splitting occupancy and NOI. Mitigation: `pms_missing_property_mapping` blocks promotion until the alias is added.

### Unit renumbering after renovation

Renovations that combine studios into one-bedrooms or split two-bedrooms into two studios invalidate the native unit_id. The unit_crosswalk preserves the unit lineage: a successor unit_id points to one or more predecessor unit_ids with a `lineage_reason` (combine, split, renumber). Failure mode: occupancy and rent-per-sf time series break at renovation. Mitigation: the crosswalk's lineage lets downstream metrics stitch pre- and post-renovation observations.

### Resident identity across multiple leases

A resident who signs a new lease in the same building (transfer) or a different property in the portfolio may be issued a new resident_account_id. The resident_crosswalk carries a `canonical_resident_id` that groups account_ids for the same person. Failure mode: transfer retention rates under-count if each account_id is treated independently. Mitigation: `pms_transferred_unit_consistency` requires transfer_from_lease_id on the new lease and a `lease_terminated` event with `reason = transfer` on the prior lease.

### Household versus individual resident

A household may carry multiple adult residents on one lease. Household identity is tracked via `household_id` in the resident_crosswalk; a lease always maps to exactly one household. Failure mode: duplicate application records across household members inflate lead volume. Mitigation: `pms_multiple_applicants_one_household` requires applications within one (property_id, household_id, lease_cycle) to resolve to one lease_id.

### Corporate lease residents

A corporate entity (relocation service, insurer, or master-lease tenant) may be the lease signatory while the occupant is a natural person. The resident_crosswalk carries a `corporate_lease_flag` and a separate `occupant_resident_id` when known. Failure mode: delinquency and collections metrics treat corporate counterparties as if they were individual residents. Mitigation: downstream workflows branch on `corporate_lease_flag`.

### Employee-unit exclusions

Units flagged `employee` or `model` in pms.unit are excluded from unit_count_rentable and from occupancy denominators. The employee_unit_registry records which units are employee units and which employee is assigned. Failure mode: employee units counted as occupied inflate portfolio occupancy without revenue. Mitigation: `pms_employee_unit_flag_excluded_from_occupancy` and `pms_model_unit_flag_excluded_from_occupancy`.

## Failure modes summary

| Failure | Symptom | Check |
|---|---|---|
| Unregistered property alias | New phantom property_id with split occupancy | `pms_missing_property_mapping` (via gl and ap), property_crosswalk missing alias |
| Unit lineage missing across renovation | Rent-per-sf time series breaks | Unit crosswalk lineage_reason missing |
| Transferred resident treated as new | Understated transfer retention | `pms_transferred_unit_consistency` |
| Two active leases for one household | Duplicate application dedup failure | `pms_multiple_applicants_one_household` |
| Corporate lease handled as individual | Delinquency workflow misroutes | corporate_lease_flag unset |
| Employee unit counted as rentable | Inflated occupancy | `pms_employee_unit_flag_excluded_from_occupancy` |
| Model unit counted as rentable | Inflated occupancy | `pms_model_unit_flag_excluded_from_occupancy` |
