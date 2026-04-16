# Sage Intacct Onboarding Runbook

Status: wave_4_template
Audience: finance_systems_team, corporate_controller, data_platform_team
Last updated: 2026-04-15

This runbook walks a new residential multifamily deployment through Sage
Intacct adapter onboarding. Every step is gated by a checklist; no step
proceeds until the previous step is signed off. Tolerances reference
`reference/normalized/schemas/reconciliation_tolerance_band.yaml` by name,
never by value.

---

## Step 0. Scope confirmation

**Owner:** corporate_controller + finance_systems_team

Confirm the Intacct modules in scope:

- General Ledger (required)
- Budget Module (required if budget_line is primary from Intacct)
- Forecast Module (required if forecast_line is primary from Intacct)
- Project dimension (required for capex attribution)
- Vendor master (required)
- Dimension master: Entities, Locations, Departments, Classes (required)

Out-of-scope confirmation: AP invoice lifecycle (stays on AppFolio AP
adapter), Order Entry, Inventory, Procurement.

**Exit criterion.** Signed scope document on file; matches the
`manifest.yaml::object_coverage` list.

---

## Step 1. Sandbox provisioning

**Owner:** finance_systems_team

1. Request Intacct sandbox environment from the vendor.
2. Load a representative slice of the operator's chart of accounts, one
   full entity tree, one full dimension set (locations, departments,
   projects, classes), one closed period's journal entries, and one
   published budget version.
3. Confirm the sandbox refresh cadence (daily or on-demand) and the
   extraction latency.
4. Create a non-prod OAuth client credential set in Intacct with read-only
   scopes on all GL objects.

**Exit criterion.** Sandbox passes a smoke test: 7 consecutive days of
pulls land within `expected_latency_minutes` per `source_registry`.

---

## Step 2. Credential model

**Owner:** data_platform_team + corporate_controller

Intacct Web Services requires three credentials: sender_id (Anthropic-
provisioned application identity), company_id (operator's Intacct tenant),
and user credential (service account with restricted scopes). The adapter
uses `credential_method: oauth_placeholder` in the source registry.

Operator must create:

- A dedicated service user (do not reuse a named person's account).
- A restricted-access role assigned only to the service user: read on
  Accounts, Dimensions, GL Entry, GL Batch, Budget Detail, Forecast
  Detail, Vendor, Project. No write or admin permissions.
- A rotation schedule per `security/pii_classification.md`. Tax id is the
  most sensitive field carried; treat the credential as a restricted
  secret.

**Exit criterion.** Credential stored per `security/secrets_rotation.md`;
rotated at least every 90 days.

---

## Step 3. Deployment pattern selection

**Owner:** corporate_controller

Two patterns are supported; selection depends on the operator's legal
structure:

1. **Entity-per-property (SPE pattern).** Each property has its own legal
   entity; `ENTITYID` alone resolves to `property_id`. Common with funds
   where each SPV holds one asset.
2. **Roll-up-entity pattern.** Multiple properties share one legal entity;
   `LOCATIONID` disambiguates. Common with operator-owned regional
   portfolios.

Operator declares the pattern in `property_master_crosswalk` notes. Mixed
patterns (different properties use different patterns) are supported but
require explicit per-row notes.

**Exit criterion.** Pattern is declared on every property row in
`property_master_crosswalk`.

---

## Step 4. Chart-of-accounts mapping pre-flight

**Owner:** corporate_controller

1. Export the operator's full chart of accounts from Intacct.
2. For every active `GLACCOUNTNO`, assign a canonical slug via the
   `account_crosswalk`. Start from `crosswalk_additions.yaml::account_crosswalk_additions`
   and extend for each account not already mapped.
3. Every capex account must be flagged with `CAPITALIZATION_FLAG = true`
   so `ic_consistency_capex_opex_misclass` can run.
4. Reclassification (operator renames or re-codes accounts) is captured
   with `effective_start`/`effective_end` on the crosswalk rows.

**Exit criterion.** Zero unmapped active `GLACCOUNTNO` values when
`ic_conformance_account_in_coa` runs against the sandbox data.

---

## Step 5. Dimension mapping pre-flight

**Owner:** finance_systems_team + regional_ops_director

1. Export all dimension records (Entities, Locations, Departments,
   Projects, Classes).
2. For each active `LOCATIONID` or `ENTITYID` corresponding to a
   residential property, create a `property_master_crosswalk` row with the
   canonical `property_id`.
3. For each active `PROJECTID` representing a capex project, create a
   `capex_project_crosswalk` row linking to the canonical `capex_project_id`
   and to the Procore project id (if present).
4. Class dimension is optional — map if the operator uses Class for fund or
   reporting segment slicing.
5. Department dimension is typically not used for property attribution —
   do not map to `property_id`.

**Exit criterion.** Zero unresolved `LOCATIONID`/`ENTITYID` when
`ic_conformance_property_dim_in_crosswalk` runs against the sandbox data.

---

## Step 6. Budget-version naming convention

**Owner:** corporate_controller

Budget version labels drift in operator shops (common patterns:
`initial_2026`, `fy26_v1`, `2026 Approved`, `Board Approved 2026`). Enforce
a single pattern for the adapter:

- `<scenario>_<fiscal_year>[_<revision>]`, all snake_case.
- `scenario` is one of: `approved`, `midyear_draft`, `midyear_approved`,
  `yearend_estimate`, `stress_downside`, `stress_upside`.
- `fiscal_year` is the operator's FY label (`fy26`, `fy27`).
- `revision` is optional; use `v1`, `v2` etc.

Example: `approved_fy26_v1`, `midyear_draft_fy26_v2`.

`map_intacct_budget_version` resolves each label; unmapped labels land as
`unresolved_budget_version_<BUDGETID>` and degrade confidence to medium.

**Exit criterion.** All current `BUDGETNAME` values resolve via
`map_intacct_budget_version`.

---

## Step 7. Dual-run during cutover

**Owner:** data_platform_team + corporate_controller

For the first full close cycle (one month minimum), run the Intacct
adapter in parallel with the operator's incumbent reporting process.

- Intacct actual_line sums per `(property_id, canonical_account_slug,
  period)` are compared to the incumbent report.
- Drift within `account_class_band` is silent_audit.
- Drift beyond band is surfaced to `corporate_controller` for
  reconciliation before publication.
- Variance narrative validation: every narrative authored in the incumbent
  flow must appear under the corresponding `variance_explanation` in the
  normalized feed.

**Exit criterion.** Zero unexplained drift beyond `account_class_band` in
one full close cycle.

---

## Step 8. Period-close handshake

**Owner:** corporate_controller

Intacct's period-close workflow emits a `period_close_timestamp` the
adapter must consume:

1. Once the close completes in Intacct, the adapter blocks any new
   postings into the closed period unless a formal reopen event is logged.
2. The adapter's daily extraction loop consumes the close event and
   signals downstream workflows (`monthly_property_operating_review`,
   `reforecast`) that the closed period's numbers are authoritative.
3. Any reopen event carries `reopened_by_user_id` and `reopen_reason`
   fields in the normalized journal feed.

**Exit criterion.** Close handshake tested against the sandbox with both a
clean close and a simulated reopen.

---

## Step 9. Reconciliation runner activation

**Owner:** data_platform_team

Activate each reconciliation in `reconciliation_checks.yaml`:

- Daily: `ic_recon_unmapped_account`, `ic_freshness_actual_lines_daily`.
- Weekly: `ic_recon_property_dim_present`, `ic_recon_capex_project_dim_handshake`,
  `ic_recon_manual_journal_attribution`, `ic_recon_period_reopen_drift`,
  `ic_recon_vendor_three_way`, `ic_recon_capex_commitment_vs_posted`,
  `ic_recon_co_pending_vs_posted`, `ic_recon_draw_vs_posted`.
- Monthly: `ic_recon_cash_to_accrual_revenue`, `ic_recon_capex_opex_misclass`,
  `ic_recon_variance_narrative_coverage`, `ic_recon_payroll_entity_attribution`.
- Quarterly: `ic_recon_labor_classification`, `ic_recon_manual_budget_fallback_attestation`.
- Event-driven: `ic_recon_post_close_entity_setup`.

**Exit criterion.** Every reconciliation runs cleanly in the sandbox for
one full close cycle before prod activation.

---

## Step 10. Production cutover

**Owner:** corporate_controller + cfo + data_platform_team

1. Disable the incumbent reporting flow.
2. Switch the Intacct adapter to prod environment and credentials.
3. Run a mirrored extraction for 7 calendar days and compare against the
   last parallel-run outputs.
4. Sign off on cutover in the operator runbook log.
5. Announce cutover to downstream workflow consumers (asset_mgmt,
   executive, IC).

**Exit criterion.** Prod feed delivers within `expected_latency_minutes`
for 30 consecutive days with no blocker-severity reconciliation failures.
