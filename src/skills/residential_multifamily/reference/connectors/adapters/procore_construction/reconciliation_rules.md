# Procore Reconciliation Rules

Status: wave_5
Audience: data_platform_team, construction_lead, finance_systems_team, development_lead

Narrative specification of how Procore reconciles against adjacent stack
members. Each section names the canonical objects in scope, the dual-source
question the reconciliation answers, and the runbook that resolves a break.
Numeric tolerances always cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml` and are never
hardcoded here.

Every concrete check for these rules lives in `reconciliation_checks.yaml`
with the prefix `pc_recon_`.

## 1. Procore x Intacct — Financial reconciliation

Procore owns the construction-side commitment lifecycle (commitments, COs,
draws). Intacct owns posted GL actuals (capex_actual, draw funding, vendor
payment). Disagreement is usually timing, sometimes structure.

### 1.1 Commitment vs posted spend

- Canonical objects: `commitment` (Procore primary), `actual_line` (Intacct
  primary), `capex_project` (shared anchor via `capex_project_crosswalk`).
- Question: For each commitment, does cumulative Intacct posted spend to
  the commitment's GL account + project dimension track the Procore
  `billed_to_date` / `paid_to_date` within tolerance?
- Band: `capex_posting_band` per `reconciliation_tolerance_band.yaml`.
- Expected lag: Intacct posting follows Procore pay-app approval by the
  AP close cycle; the band accommodates the posting delay.
- Outside-band result: block `cost_to_complete_review` and
  `draw_package_review` until resolution.
- Runbook: `runbooks/procore_common_issues.md::cost_posting_lag`.

### 1.2 Change order vs invoice posting

- Canonical objects: `change_order` (Procore primary), `invoice` (Intacct
  primary).
- Question: Does every approved Procore CO that has triggered billing have
  a matching Intacct invoice line within the posting band, and does every
  pending CO stay excluded from the Intacct budget snapshot?
- Band: `co_posting_lag_band` per `reconciliation_tolerance_band.yaml`.
- Outside-band result: warn until lag threshold, block after.
- Anti-pattern guarded against: approved CO silently missed on Intacct side;
  or pending CO double-counted in Intacct pending-revised-budget snapshot.
- Runbook: `runbooks/procore_common_issues.md::co_posting_lag`.

### 1.3 Draw request vs cash funded

- Canonical objects: `draw_request` (Procore primary — submission and
  approval), `actual_line` (Intacct primary — funding posting).
- Question: Every Procore-approved draw must post as a funded line in Intacct
  within the funding band; unapproved / pending draws must not post.
- Band: `draw_posting_lag_band` per `reconciliation_tolerance_band.yaml`.
- Outside-band result: warn then block `draw_package_review`.
- Runbook: `runbooks/procore_common_issues.md::draw_posting_lag`.

## 2. Procore x Dealpath — Development handoff

- Canonical objects: `deal` (Dealpath primary), `development_project`
  (Dealpath seeds, Procore executes), `capex_project`.
- Question: Every IC-approved development deal in Dealpath has a Procore
  project opened within the handoff window; every Procore development
  project carries a linked Dealpath `asset_id` via `dev_project_crosswalk`.
- Band: `dev_handoff_lag` per `reconciliation_tolerance_band.yaml`.
- Outside-band result: warn until lag, block `capital_project_intake_and_prioritization`
  after.
- Handoff payload: asset_id, legal_entity_id, target_budget, target_schedule,
  project_owner_company, funding_source (from Dealpath) -> seed Procore
  project + capex_project_crosswalk + dev_project_crosswalk row.
- Anti-pattern: Procore project opened without a Dealpath anchor; or Dealpath
  IC-approved deal sitting without a Procore shell beyond the handoff window.
- Runbook: `runbooks/dealpath_common_issues.md::dev_handoff`.

## 3. Procore x Excel — Estimate vs material cost reference calibration

- Canonical objects: `estimate_line_item` (Procore primary),
  `material_cost_reference` (Excel primary), `labor_rate_reference` (Excel
  + hr_payroll).
- Question: Procore estimate line unit costs must fall within the Excel
  material_cost_reference band by cost_code; persistent drift implies the
  reference library is stale or the project estimate carries escalation
  beyond benchmark.
- Band: `material_reference_drift_band` per `reconciliation_tolerance_band.yaml`.
- Outside-band result: warn, surface in `capex_estimate_generation` output.
- Runbook: `runbooks/benchmark_refresh.md`.

## 4. Procore x AppFolio — Vendor master and post-delivery handoff

Post-delivery, AppFolio becomes the primary dispatch system for operational
work. Procore-side vendors that survive into property operations must resolve
to the same canonical `vendor_id`.

### 4.1 Vendor master overlap post-delivery

- Canonical objects: `vendor` (three-way: Intacct AP + Procore + AppFolio).
- Question: For every Procore vendor that carries a post-delivery warranty
  or punchlist callback, does the vendor_master_crosswalk resolve the
  Procore directory id, Intacct AP vendor id, and AppFolio vendor id to the
  same canonical vendor_id?
- Band: `identity_match_band` per `reconciliation_tolerance_band.yaml`.
- Outside-band result: warn; feed into `vendor_dispatch_sla_review`.
- Runbook: `runbooks/vendor_crosswalk_mismatch.md`.

### 4.2 Delivery handoff

- Canonical objects: `construction_project` -> `property` -> `unit`.
- Question: At `project_phase = Post Construction` (canonical `delivered` /
  `lease_up`), does a Property open in AppFolio with the
  `capex_project_crosswalk` / `property_master_crosswalk` row linking back
  to the Procore project?
- Band: `delivery_handoff_band` per `reconciliation_tolerance_band.yaml`.
- Outside-band result: block `lease_up_first_period`.
- Runbook: `runbooks/procore_common_issues.md::delivery_handoff`.

## 5. Procore x Yardi — Where development project lands into operations

Yardi plays an alternate PMS role for some operators. For this adapter, the
rule is symmetric to the Procore x AppFolio case: at delivery the Procore
project rolls over to the canonical `Property` in Yardi (when the operator
uses Yardi rather than AppFolio for post-delivery operations). The
`property_master_crosswalk` carries the Yardi property_id; the
`capex_project_crosswalk` preserves the Procore project_id for warranty
callback traceability.

- Canonical objects: `construction_project` -> `property` (Yardi primary when
  operator uses Yardi for post-delivery operations).
- Question: Same as 4.2 but with Yardi as downstream PMS.
- Band: `delivery_handoff_band`.
- Outside-band result: block `lease_up_first_period`.
- Note: The Yardi adapter at `adapters/yardi_multi_role/` remains a stub;
  this rule is documented for completeness and does not yet have
  corresponding machine checks.

## Cross-cutting reconciliation invariants

1. `posting_period_close_wins`: Once Intacct closes the period, Intacct
   supersedes Procore for any actuals dispute touching that period.
   Procore remains authoritative for future-period commitment and CO state.
2. `late_arriving_supersedes`: Late Procore updates (post-hoc CO
   adjustments, backdated commitments) supersede earlier pulls; prior rows
   preserved as audit rows.
3. `pending_status_does_not_post`: Pending COs must never contribute to
   canonical `revised_contract_total_cents` or to Intacct budget snapshots.
4. `retainage_preserved_through_closeout`: Commitment retainage_balance
   and cumulative pay-app retainage must reconcile at closeout; pre-closeout
   drift is expected but tracked.
