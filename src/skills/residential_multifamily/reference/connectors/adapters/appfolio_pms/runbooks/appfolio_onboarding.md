# AppFolio Onboarding Runbook

Status: stub
Wave: 4
Audience: data_platform_team, regional_ops_director, corporate_controller
Scope: the procedure for standing up the `appfolio_prod` source and
moving it from `stubbed` to `active` per
`source_registry_entry.yaml`.

This runbook covers credentials, sandbox setup, dual-run validation,
and cut-over. It does not replace the AppFolio vendor-provided
onboarding guide; it is the operator-side companion for the residential
multifamily subsystem.

---

## 1. Credential model

**Who provides credentials.** AppFolio Property Manager issues API
keys via the AppFolio admin console. The credential owner is
`data_platform_team`; the business owner is `regional_portfolio_lead`.

**Secret storage.** Credentials live in the operator's secrets manager
(Azure Key Vault or equivalent). The source_registry declares
`credential_method: api_key_placeholder` until sandbox is wired; flip
to `api_key_live` only after the dual-run window completes.

**Rotation.** Rotate at least every 90 days. Rotation failure must
surface through `af_freshness_*` DQ rules (the adapter cannot read
the feed with a stale key). Document the rotation window in
`security/pii_classification.md`.

**Scope.** Request read-only scope covering properties, units, leases,
tenants, charges, payments, work orders, vendors, and leads. Do not
request write scope for the initial rollout; write scope is reserved
for a later wave.

---

## 2. Sandbox setup

**Environment.** AppFolio issues a sandbox tenant per operator. The
source_registry should carry both `appfolio_sandbox` and
`appfolio_prod` entries during the dual-run window; `appfolio_prod`
stays in `status: stubbed` until cut-over.

**Pilot properties.** Select one property per GL Partner, one
stabilized and one lease-up. The synthetic fixture set uses Ashford
Park (stabilized, GLP_SAMPLE_ALPHA) and Maple Vista (lease-up,
GLP_SAMPLE_GAMMA) for this pattern.

**Data seed.** Extract a full historical window (24 months of
charges, payments, work orders) into the sandbox for reconciliation
dry-run. Do not extract production PII into the sandbox; use redacted
fixtures per `security/pii_classification.md`.

---

## 3. Dual-run protocol

Run AppFolio through the adapter alongside the incumbent process
(spreadsheet-based operating reports, legacy PMS if present) for a
minimum of two close cycles. The dual-run window exists to surface:

- field-mapping gaps (caught by DQ rules `af_completeness_*`)
- enum drift (caught by `af_conformance_*`)
- crosswalk resolution failures (caught by
  `af_referential_*` + master_data unresolved_exceptions queue)
- reconciliation drift vs Intacct (caught by
  `af_recon_collections_vs_gl_revenue`)
- fair-housing guardrail hits (caught by `af_guardrail_*`)

Cut-over requires all blocker-severity rules to be green for the
pilot property set for two consecutive close cycles. Warning-severity
findings are allowed during dual run; they must be triaged before
cut-over.

**Exit criteria.** Document pass / fail for each pilot property.
`regional_ops_director` signs off with `corporate_controller`
concurrence.

---

## 4. Validation checklist

Before flipping `appfolio_prod.status` from `stubbed` to `active`,
verify:

- [ ] All entities in `source_registry_entry.yaml::object_coverage`
      land per `expected_latency_minutes`.
- [ ] `property_master_crosswalk.yaml` has rows for every pilot
      property with `confidence >= medium`.
- [ ] `unit_crosswalk.yaml` has rows for every unit in the pilot
      property set.
- [ ] `lease_crosswalk.yaml` has rows for every active lease in the
      pilot property set.
- [ ] `resident_account_crosswalk.yaml` has rows for every active
      resident; no protected-class attributes in match keys.
- [ ] `vendor_master_crosswalk.yaml` resolves every dispatched vendor
      in the pilot work_order sample.
- [ ] `af_consistency_ledger_sum_matches_balance` passes for every
      resident in the pilot window.
- [ ] `af_recon_collections_vs_gl_revenue` passes within
      `revenue_basis_band` for every pilot property-period (see
      `reference/normalized/schemas/reconciliation_tolerance_band.yaml`).
- [ ] `af_guardrail_lead_notes_no_protected_class` passes for the
      full lead sample.
- [ ] `af_guardrail_application_decided_requires_policy_ref` passes
      for every decided application.
- [ ] Sandbox and production give identical normalized output on the
      redacted fixture set.

---

## 5. Post-IC property setup landing

When a Dealpath deal closes, AppFolio is the landing point for the
property setup. The handoff is covered by
`af_recon_post_ic_property_setup_landing`.

**Procedure:**

1. `dealpath_prod` deal transitions to `closed`.
2. `data_platform_team` creates the AppFolio property record
   (PropertyId assigned by AppFolio, GL Partner code assigned per
   operator convention).
3. `corporate_controller` populates the Intacct entity dim and
   refreshes `property_master_crosswalk.yaml`.
4. `regional_ops_director` signs off after the first full reconciliation
   window (`af_recon_property_list_vs_gl_entity_dim` passes).

If the handoff exceeds `handoff_lag_band` per
`reconciliation_tolerance_band.yaml`, the reconciliation check blocks
`acquisition_handoff` until resolved.

---

## 6. Asset identity resolution (anchor: recon check)

`af_recon_asset_identity` ties `appfolio.PropertyId` to
`dealpath.asset_id` via `asset_crosswalk.yaml`. On first landing, the
crosswalk row must be manually created with
`match_method = manual` and `confidence = high` per
`master_data/identity_resolution_framework.md`.

---

## 7. Escalation path

| Condition | Route to |
|---|---|
| Stale feed beyond expected latency | data_platform_team |
| PII exposure risk | security_review queue |
| Fair-housing guardrail hit | compliance_analyst + legal_counsel |
| Ledger tie-out outside blocker band | corporate_controller |
| Property unmapped in GL | corporate_controller + regional_ops_director |
| Delivery handoff miss at lease-up | development_lead + regional_ops_director |

Escalation details per category live in
`runbooks/appfolio_common_issues.md`.

---

## 8. Cut-over to `active` status

1. Confirm validation checklist complete.
2. Update `source_registry_entry.yaml::status` from `stubbed` to
   `active`.
3. Update `manifest.yaml::status` from `stub` to `active`.
4. Announce cut-over in the operations change log.
5. Monitor blocker-severity rules daily for two weeks before reducing
   review cadence.

Rollback to `stubbed` is permitted if blocker-severity rules fire
persistently in production; see
`runbooks/appfolio_common_issues.md` for per-class playbooks.
