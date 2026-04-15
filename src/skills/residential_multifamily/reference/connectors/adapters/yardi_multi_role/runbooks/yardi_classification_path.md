# Yardi Classification Path

Step-by-step operator decision tree for closing
`../classification_worksheet.md`. This runbook is the operational
companion to the worksheet; it tells you WHAT to do after each
worksheet answer, not WHAT to answer.

Until every required dimension closes, the adapter stays at
`status: stub` and workflows must not hard-depend on Yardi as primary
per `../bounded_assumptions.yaml::yardi_role.unknown`.

---

## Step 0: Preconditions

1. Confirm operator has signed a data-use agreement permitting
   extraction from Yardi sub-systems in scope.
2. Confirm `property_master_crosswalk` is seeded for at least one
   property (or schedule seeding as part of Step 3).
3. Identify the operator-side owner for each of: Voyager PMS, Voyager
   GL, RentCafe leasing, Data Connect warehouse, report exports.

---

## Step 1: Close Dimension 1 (Role)

1. Interview operator data_platform_team, finance_reporting, and
   regional_ops_director.
2. For each sub-system in scope, select one role from Dimension 1.
   Multiple roles are common. Record evidence and open questions.
3. If the operator selects `mixed_by_portfolio_segment`, document the
   per-segment split in the worksheet.
4. Decision branch:
   - `legacy_historical_only` OR `dual_run_during_cutover` → skip to
     Step 5 (migration path) before continuing.
   - Any other role → continue to Step 2.

---

## Step 2: Close Dimension 2 (Access Path)

1. For each sub-system implied by the role selection, pick at least
   one access path in Dimension 2.
2. Identify the access path's operator contact for credentials.
3. Do NOT capture credentials in this adapter directory. Credentials
   flow through the subsystem's secrets workflow declared in
   `../../_core/stack_wave4/security/`.
4. If `api_voyager_rest` is selected, confirm OAuth/API-key scope
   permits the declared object_coverage.
5. If `data_connect_warehouse` is selected, verify warehouse refresh
   schedule and record the expected_latency_minutes.
6. If RentCafe access is `no_extraction`, set
   `rentcafe_scope_confirmed = false` globally and note that
   RentCafe-sourced objects remain quarantined per
   `../bounded_assumptions.yaml::rentcafe_lead_data_access`.
7. If report_export_files is selected, register every template_id in
   `master_data/report_export_templates` before running any ingest.

---

## Step 3: Close Dimension 3 (Operating Pattern)

1. Record the operator's day-to-day usage pattern.
2. Cadence: declare for each sub-system. Voyager PMS is typically
   hourly to daily; GL is daily to weekly; Data Connect follows
   warehouse refresh cadence; report_exports are manual on-demand.
3. Document the stack-mix pattern (standalone Yardi vs
   `yardi_plus_intacct` vs `yardi_plus_appfolio_split` vs reporting-
   only).
4. If operator declares `yardi_cutover_in_progress`, jump to Step 5
   before advancing the adapter.

---

## Step 4: Close Dimension 4 (Data Sensitivity and Control)

1. Walk sections 4a, 4b, 4c, 4d, 4e with `compliance_risk` and the
   operator's data-governance owner.
2. Apply the strictest declared posture; loosening is never default.
3. Obtain sign-offs: `data_platform_team`, `finance_reporting`,
   `compliance_risk`, `regional_ops_director`.
4. Record `last_reviewed_at`.
5. Until Section 4 closes, NO live sample data may reach downstream
   consumers. Raw landing is retained with strongest redaction.

---

## Step 5: Migration / cutover decision

If classification outcome is `yardi_cutover_in_progress` or
`yardi_cutover_completed_archival` or `dual_run_during_cutover`:

1. Follow `yardi_migration_to_appfolio.md` for cutover protocol.
2. Record `cutover_effective_date` per property in the migration
   runbook.
3. Adapter writes are bounded per `yd_consistency_historical_only_mode`.

If classification outcome is `yardi_reporting_only`:

1. Only Data Connect and report_export access paths are active.
2. Operating writes from Yardi are blocked.

---

## Step 6: Advance the adapter status

Once Dimensions 1-4 close with sign-offs:

1. Update `../manifest.yaml`:
   - `status: starter` if first-pass with real extracts has validated.
   - `status: production` after dual-run validation passes for 30+
     days AND `review_cadence` triggers.
2. Update `../source_registry_entry` (future file; seeded once
   classification closes) with:
   - `credential_method`
   - `expected_latency_minutes`
   - `object_coverage` (filtered to role-applicable objects)
   - `pii_classification`, `financial_sensitivity`, `legal_sensitivity`
     per Dimension 4
   - `status: active`
3. Lift `../bounded_assumptions.yaml::yardi_role.unknown`.
4. Remove `classification_pending_blocks_primary_claims` gate.
5. Update `../../_core/stack_wave4/source_of_truth_matrix.md` to
   reflect the per-object precedence declared in Dimension 1.

---

## Step 7: Set review cadence

1. Quarterly review of classification posture (role, access path).
2. Monthly review of DQ rule outcomes for the adapter.
3. Annual review of Dimension 4 sensitivity posture with
   `compliance_risk`.

---

## Escalation

Any blocker encountered during this path must be logged in
`../../_core/stack_wave4/open_questions_and_risks.md`. Role escalations:

- Access-path blockers → data_platform_team
- Sensitivity blockers → compliance_risk + executive
- Migration-window blockers → regional_ops_director + finance_reporting
