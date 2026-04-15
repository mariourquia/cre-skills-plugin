# Runbook: Property Crosswalk Issue

status_tag: reference

A property identifier from an inbound feed cannot be resolved against the master-data crosswalk, a duplicate is suspected, or a rename event has occurred.

## 1. Trigger

- Monitoring alert `unresolved_property_id` fires during normalization.
- `identity_unresolved` exception appears in the queue for a pms, gl, crm, ap, construction, or manual_uploads source.
- A tailoring session adds a property that is not yet in `master_data/property_master_crosswalk.yaml`.
- `unit_count_reconciliation` check fails because two crosswalk entries collapse to the same canonical property.

## 2. Symptoms

- Normalized output for the property is empty or partial.
- `orphan_property_id` counters climb in the reconciliation report.
- Two different `property_id` values point to the same canonical property (duplicate).
- A property code changed upstream (for example, PMS renumbering after a renovation) and downstream workflows still reference the old code.
- Vendor invoices in ap reference a property not currently in the owned portfolio, possible legitimate new acquisition or possible data contamination.

## 3. Likely causes (ranked)

1. Legitimate new property that has not been added to the crosswalk yet.
2. Property code renamed or renumbered upstream without a paired crosswalk update.
3. Two source systems issued different `property_id` values for the same canonical property and the crosswalk is missing the mapping.
4. Property was sold or transferred but records continue to arrive from the prior system.
5. Data contamination, records for a property the operator does not own, pointing at a misconfigured feed.

## 4. Immediate actions (minute-by-minute, numbered)

1. Capture the orphan records. Move them to `reference/raw/<domain>/_quarantine/<YYYY>/<MM>/` tagged with `reason: unresolved_property_id`.
2. Pull the candidate property details from the source file: address, unit count, legal entity, and any internal owner-entity identifier.
3. Inspect `master_data/property_master_crosswalk.yaml` for a potential match. Search by address, legal entity, and prior identifier history.
4. Apply the survivorship rule described in `master_data/`: when two sources disagree, the source with the highest source-of-truth rank for the field wins, and the crosswalk records the other system's code as a secondary identifier. The survivorship rule is data-level; it does not alter operator policy.
5. If a match is found, draft a crosswalk update proposing the new identifier as either a primary or secondary alias. The proposal is never auto-applied; it requires approval per `_core/approval_matrix.md` row 20 (changes to ontology, canonical data, alias registry).
6. If no match is found, confirm whether the property is in scope (pull the portfolio roster from `overlays/org/<org_id>/`). If out of scope, classify as data contamination and escalate to `technical_owner` and `business_owner` for the source to investigate feed misconfiguration.
7. If the source is a manual_uploads feed where the property names routinely vary, the fix is not a crosswalk entry per incident; it is a cutover to a stabilized identifier, consider `cutover_manual_to_system.md`.
8. Open an approval request for the proposed crosswalk change. Once approved, update the crosswalk, release the quarantined records, and rerun normalization.

## 5. Escalation path

- First responder: `on_call_ops`.
- `data_owner` for the affected source.
- `asset_mgmt` audience for portfolio composition questions (is this property in scope).
- `regional_ops` for site-level confirmation.
- `compliance_risk` if the affected property is in a regulatory program, an unmapped property can mean missing compliance.
- Any crosswalk change routes through the approval gate in `_core/approval_matrix.md` row 20 (system maintainer plus designated reviewer).

## 6. Affected workflows

Every property-scoped workflow. Examples:

- `monthly_property_operating_review`, cannot run for the property until resolved.
- `monthly_asset_management_review`, the portfolio roll-up has a gap.
- `executive_operating_summary_generation`, `quarterly_portfolio_review`, aggregates are short by one property or double-counted.
- `delinquency_collections`, `renewal_retention`, `lead_to_lease_funnel_review`, operationally blind at the affected property.
- `draw_package_review`, `cost_to_complete_review`, construction spend misattributed.
- `third_party_manager_scorecard_review`, manager scorecard incomplete.

## 7. Recovery steps

- Apply the approved crosswalk change.
- Release the quarantined records and re-run normalization.
- Backfill derived benchmarks that depend on the property.
- For rename cases, ensure the prior identifier is retained as a historical alias, not deleted, so older records remain resolvable.
- For data-contamination cases, instruct the source system owner to correct the upstream configuration; hold future records out of production until confirmed.

## 8. Verification steps

- `unit_count_reconciliation` passes for the property.
- `orphan_property_id` counter returns to zero for the affected source.
- Normalized records for the property appear in the expected entities.
- Workflows scoped to the property run cleanly on the next activation.
- `master_data/property_master_crosswalk.yaml` reflects the approved change with an effective-date timestamp.

## 9. Post-incident review hooks

- Log the crosswalk change to the subsystem change log per `_core/change_log_conventions.md`.
- Retain the approval-request artifact for audit.
- If crosswalk issues cluster in one source, escalate to a `cutover_manual_to_system.md` review.
- `asset_mgmt` attends the next monthly review and confirms the portfolio roster matches the crosswalk.
- Any property in a regulatory program is also reviewed by `compliance_risk` to confirm the program-specific reporting paths absorb the change.
