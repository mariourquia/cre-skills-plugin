# Procore Onboarding Runbook

Audience: data_platform_team, construction_lead, development_lead, finance_systems_team
Status: wave_5

Sequential playbook for bringing a new Procore company or project into the
residential_multifamily integration layer. Mirrors the pattern established
by `dealpath_onboarding.md` and `appfolio_onboarding.md`.

## Preconditions

- Dealpath deal has reached `ic_approved` (for development projects) or a
  capex project intake form has been ingested (for renovation / component
  replacement).
- `dev_project_crosswalk` or `capex_project_crosswalk` has a row staged
  with the canonical id and the Dealpath or intake source_id.
- Intacct has (or will have) a dim_project value reserved for the project
  budget; see `sage_intacct_common_issues.md::dim_project_setup` (proposed).
- Operator has confirmed which downstream PMS (AppFolio or Yardi) will
  own the property at delivery.

## Step 1 — API / OAuth setup

1. Register the integration application in the Procore Developer Portal
   under the owner organization.
2. Record the `client_id` and `client_secret` in the operator's secret
   store; never commit to the repo.
3. Request the following OAuth scopes:
   - Company-level: `read_only` on projects, companies, directory.
   - Project-level: `read_only` on budget, commitments, change_orders,
     payment_applications, schedule, punch_list.
4. Configure a service-account user at the company level with the above
   project-level roles enabled across all projects in scope.
5. Verify the company id and service-account user id. Record both in the
   `source_registry_entry.yaml` notes for audit.

## Step 2 — Project creation handoff from Dealpath

For each IC-approved development deal or capex project intake:

1. Pull `asset_id`, `legal_entity_id`, `project_name`, `target_budget`,
   `target_schedule`, `funding_source` from the Dealpath deal record via
   `dealpath_prod` adapter.
2. Create a Procore project using the standardized template (copy from
   existing operator template projects):
   - Project name format: `<market_abbr>_<asset_slug>_<project_type>`
   - Project type: set per Dealpath deal_type mapping
     (`new_construction`, `major_renovation`, etc.).
   - Stage: `Pre-Construction`.
   - Company (owner company): set from Dealpath `legal_entity_id`
     resolved via entity_crosswalk.
3. Import the cost code library (see Step 3).
4. Configure the project directory with the development PM, GC PM, and
   owner rep users.
5. Seed the `dev_project_crosswalk` row with
   `source_system = procore_prod` and the new Procore `project_id`.
6. Verify the `capex_project_crosswalk` row exists with both Procore
   and Intacct source systems before any commitment is signed.

## Step 3 — Cost-code library import

1. Use the organization-wide standard CSI cost code library defined at
   `reference/normalized/schemas/capex_line_item.yaml` (CSI divisions 01
   through 48).
2. Import as a Procore project cost code set; verify each division has
   at least one section imported.
3. Verify that `account_crosswalk.yaml` resolves every cost code to an
   Intacct GL account; open a master_data unresolved_exceptions_queue
   ticket for unmapped codes.
4. Flag non-CSI cost codes for `pc_conformance_csi_division` review;
   resolve or annotate before first commitment signs.

## Step 4 — Vendor master sync model

1. Before first commitment signs, sync the vendor directory:
   - Pull AP vendor master from Intacct (`sage_intacct_prod` adapter).
   - Pull PMS vendor master from AppFolio or Yardi (whichever operates
     post-delivery on this asset).
   - Match existing Procore directory entries by
     `tax_id_last_four + trade + legal_name`; resolve via
     `vendor_master_crosswalk` composite match.
2. For any Procore directory vendor without an AP match, create the AP
   record in Intacct first, then create the crosswalk row. Do not sign a
   commitment to a vendor without a canonical AP record.
3. Confirm vendor `insurance_expiry` is current per
   `pc_consistency_vendor_insurance_active`; expired vendors block
   commitment signatures.

## Step 5 — Draw schedule alignment with Intacct posting calendar

1. Confirm the Intacct posting calendar close dates with the corporate
   controller.
2. Configure Procore pay-app billing windows so that pay-app approval
   lands at least `draw_posting_lag_band` days before the Intacct close;
   see `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
3. Establish a monthly sync point between the GC's project accountant
   and the operator's AP team for draw posting reconciliation per
   `pc_recon_draw_approved_vs_cash_funded`.
4. Seed the `draw_request_crosswalk` with the first period's Procore
   pay-app id and reserve the Intacct journal id pattern
   (e.g., `GL-DRAW-<asset_slug>-###`).

## Step 6 — Schedule baseline capture

1. Enable Procore's schedule baseline feature at project setup; without
   this feature, `pc_consistency_schedule_baseline_preserved` cannot run.
2. Import the baseline schedule from the GC (MS Project or P6) or build
   natively in Procore Gantt.
3. Capture the first baseline revision with `baseline_revision_id =
   baseline_v1` before construction start; record the operator name and
   date on the revision.
4. Any subsequent re-baselining must advance the `baseline_revision_id`
   and carry an operator note explaining the trigger (schedule recovery,
   major CO, owner directive).

## Step 7 — First data pull and validation

1. Schedule the first adapter pull within 24 hours of project creation.
2. Verify sample_raw files land with expected entity types (projects,
   commitments initially empty, vendors, cost_codes).
3. Run `tests/test_procore_adapter.py` to confirm manifest and required-
   file conformance.
4. Verify `pc_freshness_projects` passes; schedule the recurring pull
   cadence (default daily; operator may increase during intake).
5. Confirm `capex_project_crosswalk` resolution and `dev_project_crosswalk`
   resolution for every project in scope.

## Step 8 — Declare onboarding complete

The project is considered onboarded when all of the following pass:

- `pc_freshness_projects`, `pc_freshness_commitments`, `pc_freshness_draws`
  all pass on the daily pull.
- `pc_referential_commitment_project_fk` and
  `pc_referential_vendor_master_fk` pass for every record in the first
  pull.
- `pc_consistency_schedule_baseline_preserved` passes; baseline_v1 is
  captured.
- The workflow `construction_meeting_prep_and_action_tracking` runs a
  full cycle without blocking issues.
- `source_registry_entry.yaml::status` updates from `stubbed` to `active`.

Log the transition in `_core/change_log.md` and update the project's
`source_registry_entry.yaml::last_validated_at` to the onboarding date.

## Rollback

If the onboarding fails validation:

1. Mark the project Procore status as `Pre-Construction` hold.
2. Do not sign any commitments until the failing check passes.
3. Route to `master_data/unresolved_exceptions_queue.md` and open a
   runbook task for the specific failing check.
4. If the project cannot onboard, revert the `dev_project_crosswalk`
   row and mark the Dealpath deal handoff as rejected via
   `recon_dp_dev_to_pc`.
