# Yardi Migration to AppFolio Runbook

Cutover protocol when Yardi is being replaced by AppFolio. Covers
historical preservation, dual-run window, and freezing books in Yardi.

This runbook applies when
`classification_worksheet.md::Dimension_3::operating_pattern` is
`yardi_cutover_in_progress` or `yardi_cutover_completed_archival`.

---

## Phases

```
Phase 0  Planning
Phase 1  Pre-cutover preparation
Phase 2  Dual-run window
Phase 3  Cutover per property
Phase 4  Post-cutover archival
```

---

## Phase 0: Planning

### Deliverables

- Migration plan document (operator owned)
- Per-property `cutover_effective_date` schedule
- AppFolio property setup sequence (follows Dealpath-to-AppFolio
  handoff pattern)
- Data mapping plan:
  - `property_master_crosswalk` pre-populated with AppFolio + Yardi
    property ids
  - `unit_crosswalk` pre-populated
  - `lease_crosswalk` pre-populated for active + notice + future
    leases
  - `resident_account_crosswalk` pre-populated
  - `vendor_master_crosswalk` pre-populated
  - `charge_code_crosswalk_by_property` populated for every
    (propid, chargecode) in both systems
  - `account_crosswalk` populated for GL
- Rollback plan (operator owned)

### Sign-offs

- regional_ops_director
- finance_reporting
- data_platform_team
- compliance_risk

---

## Phase 1: Pre-cutover preparation

### Per property

1. Create AppFolio property record.
2. Import unit roster from Yardi into AppFolio.
3. Import active / notice / future leases.
4. Import resident accounts with open balances.
5. Reconcile imported data against Yardi source:
   - unit count match
   - open balance match
   - active lease count match

### Systemic

1. Enable `yardi_voyager_stub` and `appfolio_prod` extracts in
   parallel.
2. Verify `property_master_crosswalk` resolves both systems for each
   property.
3. Activate reconciliation check `yd_recon_yardi_vs_appfolio_overlap`.
4. Declare `dual_run_window_start`.

---

## Phase 2: Dual-run window

### Duration

Typically 30-90 days per property, bounded by
`cutover_overlap_band` from
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

### Daily protocol

1. Pull extracts from both systems.
2. Run `yd_recon_yardi_vs_appfolio_overlap` at property-period grain.
3. Within band: silent_audit.
4. Within band but flagged drift: warning; downstream workflows
   annotate output with `dual_run_active = true` and degrade
   confidence to `medium`.
5. Outside band: blocker. Escalate to regional_ops_director before
   allowing downstream workflows to consume either source.

### Workflow posture during dual-run

- `migration_validation` workflow runs daily (see
  `workflow_activation_additions.yaml`).
- `monthly_property_operating_review` runs against AppFolio primary
  (if AppFolio is the go-forward system) with Yardi overlap flagged.
- `executive_reporting` shows both sources with reconciliation status
  banner.

### PII handling

Resident data appears in both systems simultaneously. Apply the
strictest PII posture declared in
`classification_worksheet.md::Dimension_4`.

---

## Phase 3: Cutover per property

### Trigger

1. Dual-run period for the property has satisfied
   `cutover_overlap_band` for N consecutive days (N declared in
   migration plan).
2. Final tie-out signed by finance_reporting.

### Steps

1. Set `cutover_effective_date` for the property.
2. Update `property_master_crosswalk` row:
   - `effective_end: cutover_effective_date` on Yardi-source row
   - `effective_start: cutover_effective_date` on AppFolio-source row
   - `survivorship_rule: cutover_completed_archival; appfolio_primary_post_cutover; yardi_historical_only`
3. Freeze writes in Yardi:
   - Disable automated charge generation for the property
   - Disable automated payment posting for the property
   - Operator-side sign-off protocol for any manual back-office
     correction post-cutover (requires data_platform_team approval)
4. Activate `yd_consistency_historical_only_mode` for the property.
5. Re-route all operating workflows to AppFolio as primary.

### Freezing books in Yardi

The finance team typically runs a final Yardi close for the property
through the cutover month:

1. Post all accrued charges for the cutover month in Yardi.
2. Run Yardi month-close for the property.
3. Export final trial balance for audit.
4. Import opening balance into AppFolio as of
   `cutover_effective_date + 1`.
5. Reconcile opening balance in AppFolio matches final trial balance
   in Yardi.

---

## Phase 4: Post-cutover archival

### Active archival period (first 12-24 months)

1. Retain full Yardi read access for historical comparatives.
2. Run monthly verification that archive read-paths still work:
   ```
   pull one property, one lease, one charge stream from Yardi
   -> confirm extract succeeds
   -> confirm field_mapping.yaml decodes cleanly
   ```
3. Any new chargecode, account_code, or operator config change that
   breaks decode triggers a maintenance ticket.

### Long-term archival (24+ months)

1. Reduce extract frequency to quarterly.
2. Retain historical crosswalk rows with `effective_end` set.
3. If operator sunsets Yardi tenant, export raw data to cold storage
   before tenant decommission.

### Comparative reporting

Historical comparatives (3-5 year trend reports) pull from Yardi for
periods ≤ `cutover_effective_date - 1 day` and AppFolio thereafter.
The split is enforced at the workflow layer; no adapter-level work
required once crosswalks carry effective dates.

---

## Rollback protocol

If cutover fails and operator needs to roll back to Yardi:

1. Reverse Phase 3 steps: unfreeze Yardi writes; freeze AppFolio.
2. Revert `property_master_crosswalk` effective-dating.
3. Deactivate `yd_consistency_historical_only_mode`.
4. Escalate to regional_ops_director and finance_reporting.
5. Document rollback in
   `../../_core/stack_wave4/open_questions_and_risks.md`.

---

## Common cutover issues

- **Open balance mismatch on import**: usually timing — Yardi charge
  posted after export cutoff. Reconcile and re-import.
- **Lease end-date mismatch**: lease renewal posted in one system
  before the other. Manual lease sync; document the source that
  resolved first.
- **Vendor directory divergence**: reconcile via
  `vendor_master_crosswalk` before cutover.
- **Chargecode decode gap**: every Yardi chargecode must map to an
  AppFolio ChargeType before cutover; otherwise post-cutover revenue
  attribution breaks.
- **GL actuals drift**: run `yd_recon_yardi_vs_intacct_gl_parallel`
  through the cutover month.
- **Orphan work_order**: Yardi work_order not yet closed when
  cutover executes — import into AppFolio as open work_order with
  source reference.

---

## Post-cutover verification checklist

- [ ] Every property has `cutover_effective_date` set
- [ ] Every property_master_crosswalk row has effective-dating
- [ ] `yd_consistency_historical_only_mode` active
- [ ] No Yardi writes after cutover date (confirmed via daily
      monitoring for 30 days)
- [ ] AppFolio workflows running as primary for every property
- [ ] Historical read-paths verified
- [ ] Sign-offs from regional_ops_director, finance_reporting,
      compliance_risk
