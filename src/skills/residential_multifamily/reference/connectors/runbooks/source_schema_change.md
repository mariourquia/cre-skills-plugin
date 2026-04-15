# Runbook: Source Schema Change

status_tag: reference

Vendor or upstream source adds, renames, or removes a field. The subsystem must decide: tolerate, remap, or escalate.

## 1. Trigger

- Schema-drift test in the affected connector's `tests/test_sample_normalizes.py` or `tests/test_manifest.py` fails on a new production landing.
- `_schema/entity_contract.schema.yaml` validation rejects incoming records because a required field is missing or a type mismatch appears.
- `technical_owner` or upstream vendor announces a schema change via a release note.

## 2. Symptoms

- Normalized row count drops sharply for an affected entity.
- Reconciliation check `null_critical_field` flips from pass to fail.
- Reconciliation check `record_count` fails because records are rejected at landing.
- Downstream workflows report "data unavailable" where they previously ran green.
- An exception of category `schema_drift` appears in the exception queue.

## 3. Likely causes (ranked)

1. Vendor version upgrade added or renamed a field.
2. Vendor removed a deprecated field on schedule (check vendor release notes).
3. Vendor extension or custom plugin enabled that introduced a new field set.
4. Adapter-side bug that changed field emission; confirm by diffing the `extractor_version`.
5. Operator-side configuration change (vendor admin renamed a custom field).

## 4. Immediate actions (minute-by-minute, numbered)

1. Capture the failing raw file. Copy to `reference/raw/<domain>/_quarantine/<YYYY>/<MM>/` with a reason note.
2. Diff the incoming schema against the connector's `schema.yaml`. Enumerate added, renamed, removed, and type-changed fields.
3. Classify each delta:
   - **Added optional field**: tolerate. Update `schema.yaml` to declare the new optional field; update `mapping.yaml` with `optional_source: true` unless the field is useful downstream.
   - **Added required-looking field**: tolerate as optional until a downstream consumer is identified. Do not promote to required without metric-contract review.
   - **Renamed field**: remap. Update `mapping.yaml` source column for the affected normalized target.
   - **Removed field, not required downstream**: tolerate. Remove from `schema.yaml` and `mapping.yaml`.
   - **Removed field, required by one or more metrics**: escalate. This breaks downstream workflows.
   - **Type change**: remap with an explicit transform rule; validate with a fresh sample before unquarantining production.
4. For any escalation-class delta, open a `change_log_entry` per `_core/change_log_conventions.md` and route to `data_owner`, `business_owner`, `technical_owner`, and the relevant audience (`finance_reporting` for gl, `asset_mgmt` or `regional_ops` for pms, `compliance_risk` for regulatory sources).
5. Apply the mapping change in a feature branch. Run connector tests. Land a new sanitized sample under `reference/raw/<domain>/_samples/`.
6. If the delta is tolerate-class, promote the mapping change, re-run reconciliation, and release the quarantined raw file for normal processing.
7. If the delta is remap-class with metric impact, coordinate with affected skill packs via their `reference_manifest.yaml`, add a deprecation banner if a metric numerator shifts.
8. If the delta is escalate-class, place the affected workflows into degraded mode per `schema_drift_escalation.md` until the metric owner signs off on a resolution plan.

## 5. Escalation path

- `technical_owner` owns adapter changes.
- `data_owner` owns reconciliation recovery.
- `business_owner` signs off on metric-impacting remaps.
- For regulatory sources, `compliance_risk` must confirm the remap does not break a compliance obligation.
- For sources feeding `executive`-facing reporting, `finance_reporting` must confirm variance narratives still resolve.

## 6. Affected workflows

All workflows that read the affected entity. For example:

- pms `lease` schema change: `delinquency_collections`, `renewal_retention`, `move_in_administration`, `move_out_administration`, `monthly_property_operating_review`, `lead_to_lease_funnel_review`.
- gl `account` schema change: every GL-dependent workflow (`budget_build`, `reforecast`, `monthly_property_operating_review`, `monthly_asset_management_review`, `executive_operating_summary_generation`, `quarterly_portfolio_review`).
- construction `change_order` schema change: `change_order_review`, `draw_package_review`, `cost_to_complete_review`, `construction_meeting_prep_and_action_tracking`.

## 7. Recovery steps

- Unquarantine raw files once the new mapping lands and reconciliation is green.
- Backfill normalized records that were rejected during the incident window.
- If the remap altered historical meaning (e.g., a field was silently renamed upstream a week before detection), flag the affected records with a `mapping_override_log` entry naming the window and the reason.
- Notify skill-pack owners whose `reference_manifest.yaml` declares reads from the affected entity.

## 8. Verification steps

- `tests/test_sample_normalizes.py` passes with the new sample.
- Reconciliation checks green for two consecutive scheduled landings.
- No orphan records in the normalized layer.
- Workflow activation map recomputes correctly; `workflow_activation_map.yaml` shows no regression.
- If a metric contract was impacted, its unit tests pass.

## 9. Post-incident review hooks

- Log the schema-change event to the subsystem change log per `_core/change_log_conventions.md`.
- Cross-reference the mapping-override log entry.
- The `data_owner` attends the next `monthly_asset_management_review` and reports the incident.
- Recurring schema changes from the same vendor family flow into a quarterly vendor-health review attended by `executive`, `finance_reporting`, and `compliance_risk`.
- Any fair-housing-sensitive field (screening, demographic) that changed schema routes to `fair_housing_sensitive_flag.md` regardless of apparent impact.
