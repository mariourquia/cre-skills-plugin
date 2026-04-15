# AppFolio Common Issues Runbook

Status: stub
Wave: 4
Audience: data_platform_team, regional_ops_director, maintenance_supervisor,
ap_manager, corporate_controller, collections_analyst
Scope: the well-known recurring issues with the AppFolio feed and how
to recognize, triage, and remediate each. Every section anchors to the
DQ rule id or reconciliation check that detects the issue, the
synthetic fixture that illustrates it, and the downstream workflow
that is affected. Bands cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

---

## Stale feed

**Anchor.** `af_freshness_property`, `af_freshness_unit`,
`af_freshness_lease`, `af_freshness_charge`, `af_freshness_payment`.

**Signature.** DQ dashboard shows a feed missing its landing window.
Typical root causes: API key rotation failure, AppFolio upstream
outage, extractor worker crash.

**Remediation.**

1. Check credential status (see `appfolio_onboarding.md` section 1).
2. Check AppFolio status page.
3. Restart extractor worker; re-run landing for the missed window.
4. If rotation failure, rotate and re-run. Flag the rotation window
   in the secrets log.

---

## Concession-vs-charge encoding ambiguity

**Anchor.** `af_recon_concession_accrual`,
`af_recon_concession_benchmark_drift`, edge case #4.

**Signature.** Two properties in the same portfolio encode
concessions differently: one posts an explicit
`ChargeType = Concession`, the other zeroes out the first month.
Concession rollups disagree with GL-posted concession expense.

**Remediation.**

1. Do not overwrite posted data. The adapter normalizes both
   conventions to `concessions_total_cents`.
2. Ask ops to standardize on the explicit-charge pattern per
   `runbooks/appfolio_onboarding.md` pilot notes.
3. If the band is exceeded, degrade confidence on the affected
   property-period cell; log to `master_data/unresolved_exceptions_queue.md`.

---

## Lease renewal as new lease vs same lease

**Anchor.** `af_completeness_lease_required`,
`af_referential_charge_lease_present`, crosswalk section on renewals.

**Signature.** AppFolio creates a new `LeaseId` for every renewal
rather than extending the existing lease. Charges may continue under
the prior `LeaseId` for a few days during the transition.

**Remediation.**

1. Adapter emits both leases with `prior_lease_id` link on the renewal.
2. Ledger balance follows `resident_account_id`, not `lease_id`.
3. If charges appear against the closed lease after the renewal
   start_date, investigate for posting drift; runbook step
   `ledger_tie_out`.

---

## Work order priority drift

**Anchor.** `af_conformance_work_order_priority_enum`,
`af_consistency_p1_safety_assignment_sla`.

**Signature.** AppFolio `Priority` value cannot be mapped to the
canonical enum (p1_safety, p2_habitability, p3_standard, p4_cosmetic)
via `map_appfolio_priority`. Common when a property uses a
custom priority label.

**Remediation.**

1. Extend `map_appfolio_priority` to cover the custom label, if
   semantically appropriate.
2. If the custom label has no clear canonical mapping, escalate to
   `maintenance_supervisor` to normalize in AppFolio.
3. Blocker severity: do not auto-assign the ticket until the enum is
   resolved.

---

## Vendor insurance expiry false positives

**Anchor.** `af_consistency_vendor_insurance_not_stale`.

**Signature.** Vendor flagged as stale-insurance but current COI on
file in the AP insurance intake system. Root cause: AppFolio vendor
directory is not the authoritative COI store; Intacct / AP is.

**Remediation.**

1. Confirm via the AP side (insurance_coi_intake) that a current COI
   exists.
2. Update the AppFolio vendor directory to reflect the current expiry.
3. Do not override the warning without confirmation; treat this as a
   data-sync issue between AppFolio and AP.
4. Safety-critical work remains blocked per the ontology guardrail
   until the dispatch-side record is current.

---

## Unit status transitions silently mid-month

**Anchor.** `af_completeness_unit_required`, edge case #11.

**Signature.** Unit transitions from `Occupied` to `Notice` to `Vacant`
mid-month with no explicit `LeaseEvent` record in AppFolio. The event
stream must be reconstructed from the status sequence.

**Remediation.**

1. Adapter derives the implicit events (notice_to_vacate, move_out,
   available_for_lease) from the status transition series.
2. Log derived events with `EventPayload.derived = true`.
3. Do not block the property on missing explicit events; warn and
   reconcile during the next close cycle.

---

## Payment posted to wrong charge

**Anchor.** `af_consistency_ledger_sum_matches_balance`,
`af_recon_payment_deposit`.

**Signature.** A payment lands with `AppliedToChargeIds` referencing
a charge that does not exist, or with `AppliedToChargeIds` empty
despite a non-zero amount.

**Remediation.**

1. Do not auto-rebalance. Flag the resident for collections review.
2. Route to `collections_analyst` for manual rebind.
3. `af_consistency_ledger_sum_matches_balance` blocks the property
   from close until corrected.

---

## NSF reversal handling

**Anchor.** `af_recon_nsf_reversal`.

**Signature.** `TenantPayment.PaymentStatus = NSF` appears but no
matching reversal entry is visible in Intacct yet. The GL reversal
posts at close, not immediately.

**Remediation.**

1. During the interim, adapter treats the payment as reversed on the
   resident ledger but unposted on the GL side.
2. `af_recon_nsf_reversal` warns until close; becomes blocker if the
   reversal persists past close.
3. Collections workflow applies the NSF fee per lease terms.

---

## Partial-month proration disagreements

**Anchor.** `af_consistency_ledger_sum_matches_balance`, edge case #5.

**Signature.** Operator's internal ledger pack uses 30-day proration;
AppFolio uses actual-days (or vice versa). Resident ledger balance
disagrees within a few dollars per mid-month move-in.

**Remediation.**

1. Document the operator's proration convention per property (not
   portfolio-wide; properties may diverge).
2. If the band is exceeded beyond `ledger_tie_band`, escalate to
   `regional_ops_director` to reconcile.
3. Do not adjust the canonical record; surface the gap in the
   monthly variance narrative.

---

## Ledger reconciliation lag

**Anchor.** `af_recon_collections_vs_gl_revenue`,
`af_recon_payment_deposit`.

**Signature.** AppFolio-side cash receipts lead the Intacct-side GL
posting by several days. Pre-close, this is expected. Post-close, the
lag should be zero.

**Remediation.**

1. Pre-close: ignore; this is the designed behavior per
   `posting_period_close_wins`.
2. At close: if the lag persists, investigate unmapped accounts or
   unposted manual journals in Intacct. Route to
   `corporate_controller`.
3. After close period lock, Intacct becomes canonical; do not
   backfill AppFolio postings.

---

## Property unmapped in GL

**Anchor.** `af_recon_property_list_vs_gl_entity_dim`.

**Signature.** AppFolio property exists but no Intacct entity dim
resolves the `GLPartnerCode`. Typically happens at post-IC setup
before the Intacct side lands.

**Remediation.**

1. Confirm with `corporate_controller` that the entity dim is being
   provisioned.
2. If within `handoff_lag_band`, warn only.
3. If beyond the band, block `monthly_property_operating_review` for
   that property and escalate.
4. See `appfolio_onboarding.md` section 5 for the full post-IC
   procedure.

---

## Fair-housing guardrail hit

**Anchor.** `af_guardrail_lead_notes_no_protected_class`,
`af_guardrail_application_decided_requires_policy_ref`.

**Signature.** Free-text note on a lead or application contains a
protected-class flag (race, color, religion, national origin, sex,
familial status, disability, state / local class). Or: an application
transitioned to a decided status without a resolved policy_ref.

**Remediation.**

1. Immediate: block the entire `lead_to_lease_funnel_review` workflow
   for the affected property.
2. Route to `compliance_analyst` + `legal_counsel`.
3. Do not redact silently. The raw record is preserved for audit; the
   flag triggers remediation via the operator's fair-housing
   protocol.
4. Release the block only after documented remediation.

---

## Rent comp drift

**Anchor.** `af_recon_rent_comp_drift`,
`af_recon_concession_benchmark_drift`.

**Signature.** AppFolio executed rents diverge from the external
Excel rent comp pack beyond `comp_outlier_band`. Usually driven by
concession mix rather than base rent drift.

**Remediation.**

1. Check concession encoding first (ambiguity above).
2. If concession-adjusted rent still drifts, refresh the rent comp
   pack (Excel side) or trigger a pricing review via
   `renewal_retention` workflow.
3. Warn only; do not block.

---

## Submarket tag drift

**Anchor.** `af_recon_submarket_tag_consistency`.

**Signature.** AppFolio `SubmarketLabel` does not resolve to any
canonical submarket via `submarket_crosswalk.yaml`.

**Remediation.**

1. Update `submarket_crosswalk.yaml` to cover the label, if it names a
   legitimate submarket.
2. If the label is stale or operator-internal, normalize in AppFolio
   to the canonical submarket name.

---

## Orphan charge

**Anchor.** `af_referential_charge_lease_present`.

**Signature.** Charge lands with a `LeaseId` that does not resolve
via `lease_crosswalk`.

**Remediation.**

1. Most common cause: charge posted shortly before the lease record
   lands (write-order gap). Defer one extract window and re-check.
2. If persistent, investigate for a lease_crosswalk gap or a
   deleted-lease race. Route to
   `master_data/unresolved_exceptions_queue.md`.

---

## Vendor directory dedup

**Anchor.** `af_recon_vendor_master_three_way`,
`af_recon_vendor_overlap_with_procore`.

**Signature.** Same vendor appears under multiple `VendorId` in
AppFolio across GL Partners. Typical with portfolio-wide dispatch.

**Remediation.**

1. Dedupe via `vendor_master_crosswalk.yaml` with
   `match_method = fuzzy` or `manual`, `manual_override = true`.
2. Confirm tax_id continuity via Intacct.
3. Run three-way match weekly; do not block dispatch while dedup is
   in flight.

---

## Long offline unit

**Anchor.** Derived check in asset-management workflow; edge case #11.

**Signature.** Unit has been `Offline` or `Down` for more than 90
days with no `ExpectedReturnDate` update.

**Remediation.**

1. Tag the unit for depreciation review in
   `monthly_asset_management_review`.
2. Require a recovery plan or write-off decision from
   `regional_ops_director`.
3. Do not auto-restore the unit to rentable status.

---

## Vendor market mismatch

**Anchor.** `af_recon_vendor_overlap_with_procore`, edge case #8.

**Signature.** Work order dispatched to a vendor whose
`markets_served` does not include the property's market. Root cause:
portfolio-wide dispatch rule ignores geographic fit.

**Remediation.**

1. Warn the maintenance supervisor; do not reroute automatically.
2. Track SLA breaches tied to geographic mismatch for the next
   vendor dispatch review.
3. Update the vendor's `markets_served` in AppFolio if the list is
   stale.
