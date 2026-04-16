# AppFolio Edge Cases

Status: stub
Wave: 4
Scope: operational edge cases that AppFolio emits which require special
handling in the adapter, crosswalks, or downstream workflow. Every case
cites the DQ rule, reconciliation check, or crosswalk row that owns the
detection. No numeric thresholds hardcoded; bands cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

Every edge case uses synthetic property names drawn from the fixture
set (Ashford Park, Willow Creek, Maple Vista, Cedar Grove) and carries
a recognition signature plus a remediation pointer.

---

## 1. Unit renumbering after renovation

**Signature.** Historical lease and work order rows reference a unit
label that no longer appears in the current unit feed. Example:
`Ashford Park` unit `301` became `3A` after a full-floor renovation in
2024.

**Detection.** `unit_crosswalk` rows already encode this: the prior row
is closed with `effective_end`; the new row shares the same
`canonical_id`. Tests in `af_referential_lease_unit_present` depend on
the crosswalk; if the crosswalk row is missing, lease resolution fails.

**Remediation.** Add the renumber to `unit_crosswalk.yaml` with a new
`source_id` pointing to the new label. `manual_override = true` because
AppFolio does not emit a renumber mapping row natively.

Related: `unit_crosswalk.yaml` section 7.3.

---

## 2. Lease assigned to wrong unit

**Signature.** Lease record in AppFolio carries `UnitId` that contradicts
the `CurrentLeaseId` on the unit feed. Example: lease `L500042` claims
unit `103` at Ashford Park, but unit `103` shows a different
`CurrentLeaseId`.

**Detection.** `af_referential_lease_unit_present` at blocker severity.
Usually occurs when a leasing agent applied a lease to the wrong unit
and the correction has not been posted.

**Remediation.** Block the affected property from
`monthly_property_operating_review` until corrected in AppFolio.
Never overwrite silently. Log to
`master_data/unresolved_exceptions_queue.md`.

---

## 3. Mid-month rent increase on renewal

**Signature.** Renewal lease `LeaseRenewalStatus = OfferAccepted`
starts mid-month (e.g., Willow Creek lease `L500065` starts 2026-04-15)
with a new `MonthlyRent` higher than the prior lease.

**Detection.** Not a data quality failure; requires correct proration.
The adapter preserves the new `MonthlyRent` value. The downstream
revenue rollup must apply the per-day split from start_date.

**Remediation.** `af_consistency_lease_term_months` allows this because
`term_months` is recorded as 12 and the partial-month proration is
handled by the revenue calculation, not by the lease term check.
Document in the month's variance narrative if the proration drives a
line-level variance.

---

## 4. Concession encoded as charge offset vs separate field

**Signature.** Two AppFolio properties in the same portfolio encode
concessions differently: one uses `ChargeType = Concession` as a
negative charge; the other zeroes out base rent in the first month
instead of posting an explicit concession charge. Example: `Ashford
Park` vs `Willow Creek`.

**Detection.** `af_recon_concession_accrual` and
`af_recon_concession_benchmark_drift` both surface this. `sample_raw`
leases illustrate both patterns (`L500002` carries
`ConcessionsTotal = 1820`, concession posted as charge; `L500005`
carries `ConcessionsTotal = 847.50`, partial month proration).

**Remediation.** The canonical normalization always emits
`concessions_total_cents` as a positive number of cents with the sign
convention documented in `normalized_contract.yaml`. The adapter sums
`ChargeType in {Credit, Concession}` regardless of the encoding
pattern. Ops teams are asked to standardize on the explicit-charge
pattern during onboarding per
`runbooks/appfolio_onboarding.md::concession_convention`.

---

## 5. Partial-month proration

**Signature.** Lease starts or ends mid-month; charges for the first or
last month are pro-rated by AppFolio using the 30-day convention while
operator math uses the actual-days convention (or vice versa).

**Detection.** `af_consistency_ledger_sum_matches_balance` may fire
when the operator's internal ledger pack uses a different proration
rule from AppFolio's own posting.

**Remediation.** Document the proration convention per property in
`runbooks/appfolio_common_issues.md::proration_disagreement`. The
canonical side records the charge exactly as posted; variance is
surfaced in `monthly_property_operating_review` and not blocked.

---

## 6. Transferred resident with prior balance

**Signature.** Resident `R000412` at Ashford Park transferred from
unit `101` to unit `201`. AppFolio generates a new `LeaseId` (`L500020`)
but preserves `TenantId` (`T800001`). The prior lease carries a
non-zero balance that must follow the resident to the new lease.

**Detection.** `af_referential_charge_lease_present` allows historical
charges to warn, not block. `resident_account_crosswalk` preserves one
canonical `resident_account_id` across both leases. The prior lease
event sequence must close with `TransferOut`; the new lease must open
with `TransferIn`.

**Remediation.** Adapter emits `event_type = transfer_out` and
`transfer_in` derived from `TransferFromLeaseId`. Ledger balance
follows the `resident_account_id`, not the `lease_id`.

---

## 7. Vendor with expired insurance dispatched to non-safety work

**Signature.** Vendor `V00554` (sample_hvac_appliance_co) has
`InsuranceExpiryDate = 2026-02-28`. A work order was dispatched on
2026-04-05 for a non-p1_safety appliance replacement at Willow Creek.

**Detection.** `af_consistency_vendor_insurance_not_stale` fires at
warning severity. The canonical ontology (`_core/ontology.md`) blocks
dispatch for `p1_safety` specifically when
`insurance_expiry_date < today`; non-safety work receives a warning.

**Remediation.** Emit the work order, flag the vendor for a COI
refresh via `runbooks/appfolio_common_issues.md::vendor_insurance_stale`,
and escalate to `ap_manager` if the expiry is outside
`vendor_insurance_freshness_band` per
`reconciliation_tolerance_band.yaml`.

---

## 8. Work order routed to vendor in different market

**Signature.** Work order `WO700003` at Willow Creek (Atlanta market)
was auto-routed to a vendor whose `markets_served` list is
`[sample_market_alpha]` (Charlotte). AppFolio dispatches by portfolio
assignment, not by geographic proximity.

**Detection.** Not a hard DQ failure; surfaces as a `warning` outcome
in `vendor_dispatch_sla_review` where the geographic mismatch may
explain delayed response times. The canonical `vendor.markets_served`
field records the vendor's declared markets; the workflow compares
against the work order's property market.

**Remediation.** Manual intervention via
`runbooks/appfolio_common_issues.md::vendor_market_mismatch`.
Retain the work order as-posted; do not silently reroute.

---

## 9. AppFolio property setup before legal entity id is assigned in Intacct

**Signature.** A closed Dealpath deal lands a property record in
AppFolio with a `GLPartnerCode` placeholder (e.g., `GLP_SAMPLE_GAMMA_TBD`)
before the Intacct legal entity is fully set up. Example: Maple Vista
lease-up arrived in the feed before Intacct's
`legal_entity_id` dim was populated.

**Detection.** `af_recon_property_list_vs_gl_entity_dim` and
`af_recon_post_ic_property_setup_landing` both fire; the handoff lag
grows past `handoff_lag_band` and blocks
`monthly_property_operating_review` for that property.

**Remediation.** `runbooks/appfolio_onboarding.md::post_ic_property_setup`
defines the runbook. Do not create an ad-hoc legal entity; wait for
the Intacct setup to land and update `property_master_crosswalk` with
the resolved `legal_entity_id`.

---

## 10. Blank email / phone in lead

**Signature.** Guest card `GC600003` at Willow Creek carries no email
and no phone. This is valid; walk-in leads often lack contact fields.

**Detection.** Not a DQ failure per design. `af_completeness_lease_required`
only enforces lease-required fields; `Lead.contact_email` and
`Lead.contact_phone` are optional in `_core/ontology.md`.

**Remediation.** Adapter emits the lead with nulls intact. Never
default to a synthetic email or phone. The canonical
`lead.pipeline_stage` still progresses normally; follow-up is handled
in person or by visit log.

---

## 11. Unit out-of-service for more than 90 days

**Signature.** Unit `U20016` at Ashford Park has been `Offline` since
2025-01-15 with `OfflineReason = water_damage_restoration` and
`ExpectedReturnDate = 2026-06-01`. That is beyond 90 days offline.

**Detection.** A derived check (not in the base DQ rule set, owned by
the downstream property review workflow) flags the unit for
depreciation review. The canonical `unit.status` is `down`; occupancy
rollups exclude it per `_core/ontology.md`.

**Remediation.** Flag to `monthly_asset_management_review` as a
depreciation candidate. Document recovery plan in
`runbooks/appfolio_common_issues.md::long_offline_unit` with a target
return or write-off decision.

---

## 12. Bulk renewal pack staged but not posted

**Signature.** Leasing director created 25 renewal offers in AppFolio
in batch. All carry `LeaseRenewalStatus = OfferExtended` but
`ExecutedDate` is null; operators have not yet chased signatures.

**Detection.** Not a DQ failure. The canonical lease.status stays
`in_effect` until AppFolio transitions to the new lease record. The
`renewal_retention` workflow tracks the aging of offers via a derived
metric.

**Remediation.** Surface the count and aging in `renewal_retention`
output; do not overwrite or re-offer. Batch conversion happens in
AppFolio's own UI, not via the adapter.
