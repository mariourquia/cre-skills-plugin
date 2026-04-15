# Affordable Regulatory Overlay: Divergence from Conventional Segments

> Moved from `overlays/segments/affordable/` to
> `overlays/regulatory/affordable/` in refinement pass 2026-04-15. The
> affordable regime is a compliance axis, not a market-positioning segment;
> the old path continues to hold a deprecated stub and a `DEPRECATED.md`
> notice for one refinement cycle. New callers should target this path.

Status: stub. Phase 1 ships architecture and starter concept stubs. This
file enumerates how the affordable regulatory overlay is expected to differ
from a conventional (middle_market or luxury) segment so future depth can be
built without rework.

The affordable regulatory overlay covers LIHTC, HUD-subsidized
(Section 8 HAP, project-based vouchers, tenant-based vouchers), USDA Rural
Development, state and local affordable programs, HUD 202 / 811, and mixed-
income properties operating under a regulatory agreement.

## Compliance surfaces that do not exist in conventional segments

- Rent-limit testing against program-specific maximum rents. Programs include
  LIHTC (AMI-banded set-asides, average-income test sets, state-specific
  schedules), HUD (contract rents, utility allowance splits), USDA RD, and
  state / local programs with their own schedules.
- Income certification at move-in and on recertification cadence.
  Documentation requirements differ by program.
- Utility allowance schedule tracking and reconciliation.
- Student status rules (LIHTC).
- Household composition rules (HUD).
- Subsidy payment reconciliation (HAP contracts, voucher portability, TRACS /
  iMAX submissions).
- Agency inspection readiness (REAC / NSPIRE, UPCS, program-specific).
- Extended use covenants and qualified contract timelines (LIHTC).

## Screening divergence

- Eligibility screening includes program-specific criteria that do not apply
  in conventional segments (AMI qualification, student status, household
  composition, subsidy documentation).
- Source-of-income screening is typically prohibited and is doubly so where a
  jurisdiction makes source-of-income a protected class.
- Individualized assessment for criminal history follows HUD guidance; agency
  programs may layer additional requirements.
- Background-check vendors and document-verification vendors may differ from
  conventional vendor preferences.

## Reporting divergence

Reporting adds:

- Rent-limit compliance rate and waterfall against program maxima.
- Certification timeliness and backlog.
- Subsidy reconciliation status.
- Agency-inspection readiness.
- Exit-testing risk (LIHTC noncompliance, VAWA, fair-housing complaints).

Segment emphases (collections, controllable opex, trade-out) still apply but
are framed within affordability constraints: concessions are restricted or
prohibited by program rules; rent growth is capped by program limits, not by
market.

## Delinquency posture divergence

- Affordability constraints reshape the delinquency playbook. Many residents
  pay a tenant portion plus a subsidy portion; the system separates the two
  in ledger views.
- Payment plans and waivers interact with program rules; ad-hoc deals are
  prohibited.
- Eviction pathways may carry additional program-specific prerequisites and
  may require agency notice or coordination.

## Communication divergence

- Residents in affordable programs receive program-specific notices (annual
  recertification notice, income-verification requests, rent-increase
  notices per program cadence). These carry `legal_review_required` banners
  and are reviewed by humans.
- Tone remains plain-language and respectful (same as segment).
- Language access may require multi-language communication per property
  demographics and program requirements.

## Staffing divergence

- A designated compliance lead or outsourced compliance service is required.
- Training emphasis shifts toward program rules (LIHTC, HUD, state).
- Agency relationships add a coordination surface not present in
  conventional segments.

## Amenity and service divergence

- Service standards remain; amenity investment levels may differ based on
  underwriting and program constraints.
- Resident services programming (financial literacy, after-school, workforce
  resources) may be required under certain programs.

## What Phase 1 does not build

- Populated program-specific rent-limit, income-limit, and utility-allowance
  reference schedules.
- Compliance workflow packs.
- Program-specific approval matrix overrides with numeric thresholds.
- Form templates and agency-submission integrations.

These land in Phase 2 alongside the reference layer.
