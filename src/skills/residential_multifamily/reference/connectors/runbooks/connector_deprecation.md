# Runbook: Connector Deprecation

status_tag: reference

Sunset a source connector. A replacement path exists and will absorb the connector's `object_coverage`.

## 1. Trigger

- Deprecation is scheduled based on vendor end-of-life, consolidation, cutover completion, or portfolio-composition change.
- Announced by the `data_owner` or `business_owner` with consumer-audience sign-off.
- Replaced by another source whose connector contract covers the same canonical objects.

## 2. Symptoms

- The deprecating source still produces data on cadence but no longer has an operational justification.
- Users have been asked to stop configuring new loads against the source.
- A deprecation banner appears on the source's registry entry.

## 3. Likely causes (ranked)

1. Vendor retired the product.
2. Consolidation, two sources merged into one.
3. Portfolio disposition removed the properties that needed the source.
4. Cutover completed; the manual-to-system cutover runbook already moved the traffic.
5. Cost, risk, or compliance decision to stop using the source.

## 4. Immediate actions (minute-by-minute, numbered)

1. Publish a deprecation announcement. Audiences: `data_owner`, `business_owner`, `technical_owner`, all consumer audiences whose workflows read from the source, and `executive` if the source feeds executive reporting.
2. Document the replacement path for every canonical object in `object_coverage`. Each object must have either a replacement source or an explicit "no longer needed" rationale.
3. Set a deprecation timeline. Typical phases: announcement, dual-run (new source primary, deprecating source shadow), cutoff date, retention-only period (raw archive retained, no new landings), retirement.
4. Dual-run: both sources land. The new source is primary; the deprecating source is shadow. Compare per-object reconciliation across both; flag divergences.
5. Repoint `master_data/` crosswalks to the replacement source's `source_id` ahead of the cutoff date.
6. Update every skill pack's `reference_manifest.yaml` that declared reads on the source. The replacement entity contracts must satisfy the declared reads; otherwise the packs need updates.
7. On cutoff date, stop accepting new landings from the deprecating source. Set `status: deprecated` in the registry with a `notes` entry naming the replacement and the cutoff date.
8. Retain the raw archive immutably per `layer_design.md` (planned in connectors/_core). Raw files never become writable; only the ingestion path turns off.
9. After the retention-only period, retire credentials and infrastructure for the deprecated source; confirm with `technical_owner` that no live connections remain.

## 5. Escalation path

- `data_owner` and `business_owner` own the deprecation.
- `technical_owner` owns adapter retirement.
- Primary consumer audience signs off on replacement readiness.
- `finance_reporting` signs off on finance-adjacent deprecations.
- `compliance_risk` signs off on regulatory-program deprecations.
- `executive` signs off if the source feeds board, lender, investor, or regulator reports.
- `legal_counsel` signs off if the source is subject to a contractual retention obligation.

## 6. Affected workflows

Depends on the source. Every workflow reading the `object_coverage` must be re-tested against the replacement. Common cases:

- gl connector deprecation: `monthly_property_operating_review`, `monthly_asset_management_review`, `executive_operating_summary_generation`, `quarterly_portfolio_review`, `budget_build`, `reforecast`.
- pms connector deprecation: all property-scoped operational workflows.
- ap connector deprecation: `bid_leveling_procurement_review`, `vendor_dispatch_sla_review`.
- market_data connector deprecation: `market_rent_refresh`, `rent_comp_intake`.
- construction connector deprecation: `draw_package_review`, `cost_to_complete_review`, `change_order_review`, `construction_meeting_prep_and_action_tracking`, `schedule_risk_review`, `capital_project_intake_and_prioritization`, `bid_leveling_procurement_review`, `capex_estimate_generation`.

## 7. Recovery steps

- If the replacement source fails during dual-run, delay the cutoff. Keep both sources active and reopen the dual-run window.
- If a replacement gap is discovered after cutoff, roll back the deprecation per `reference_rollback.md` protocols: restore the deprecating source to `active` and repoint crosswalks. This is disruptive and requires executive sign-off.
- Raw files from the deprecated source remain queryable for audit; they are never deleted during the retention period.

## 8. Verification steps

- Registry entry is `status: deprecated` with a complete replacement note.
- No live landings from the source after the cutoff date.
- Every crosswalk reference repointed.
- Every skill pack `reference_manifest.yaml` updated.
- Downstream workflows pass reconciliation with the replacement source alone.
- Raw archive intact.

## 9. Post-incident review hooks

- Deprecation event logged to the subsystem change log per `_core/change_log_conventions.md`.
- `executive` monthly operations review notes the deprecation.
- Any post-deprecation incident tied to data-gap surfaced via the exception queue feeds a root-cause review.
- At the end of the retention-only period, `data_owner` confirms retention obligations are met; if yes, the source is fully retired in the registry; if no, retention continues.
