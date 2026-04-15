# Affordable Segment: Divergence from Middle-Market

Status: stub. This overlay is not deepened in Phase 1. This file enumerates how the
affordable segment is expected to differ from `middle_market` so future depth can be
built without rework.

The affordable segment includes LIHTC, HUD-subsidized (Section 8 HAP, project-based
vouchers, tenant-based vouchers), USDA Rural Development, state and local affordable
programs, and workforce-restricted properties operating under a regulatory agreement.

## Compliance surfaces that do not exist in middle-market

- Rent limit testing against program-specific maximum rents. Programs include LIHTC
  (various AMI-banded set-asides such as sixty-percent and fifty-percent AMI bands,
  average-income test sets, and state-specific schedules), HUD (contract rents,
  utility allowance splits), and state and local programs with their own schedules.
- Income certification at move-in and on recertification cadence. Documentation
  requirements differ by program (LIHTC annual recertification posture varies by
  property mix, HUD annual plus interim, state programs per regulatory agreement).
- Utility allowance schedule tracking and reconciliation.
- Student status rules (LIHTC).
- Household composition rules (HUD).
- Subsidy payment reconciliation (HAP contracts, voucher portability, TRACS / iMAX
  submissions).
- Agency inspection readiness (REAC / NSPIRE, UPCS, program-specific).
- Extended use covenants and qualified contract timelines (LIHTC).

<a id="screening_divergence"></a>

## Screening divergence

- Eligibility screening includes program-specific criteria that do not apply in
  middle-market (AMI qualification, student status, household composition, subsidy
  documentation).
- Source-of-income screening is typically prohibited and is doubly so where a
  jurisdiction makes source-of-income a protected class.
- Individualized assessment for criminal history follows HUD 2016 guidance; agency
  programs may layer additional requirements.
- Background-check vendors and document-verification vendors may differ from
  middle-market vendor preferences.

<a id="reporting_divergence"></a>

## Reporting divergence

Reporting for affordable adds:

- Rent-limit compliance rate and waterfall against program maxima.
- Certification timeliness and backlog.
- Subsidy reconciliation status.
- Agency-inspection readiness.
- Exit-testing risk (LIHTC noncompliance, VAWA, fair-housing complaints).

Middle-market emphases (collections, controllable opex, trade-out) still apply but
are framed within affordability constraints: concessions are restricted or
prohibited by program rules; rent growth is capped by program limits, not by
market.

## Delinquency posture divergence

- Affordability constraints reshape the delinquency playbook. Many residents pay
  a tenant portion plus a subsidy portion; the system separates the two in ledger
  views.
- Payment plans and waivers interact with program rules; ad-hoc deals are prohibited.
- Eviction pathways may carry additional program-specific prerequisites and may
  require agency notice or coordination.

## Communication divergence

- Residents in affordable programs receive program-specific notices (annual
  recertification notice, income-verification requests, rent-increase notices per
  program cadence). These carry `legal_review_required` banners and are reviewed
  by humans.
- Tone remains plain-language and respectful (same as middle-market).
- Language access may require multi-language communication per property
  demographics and program requirements.

## Staffing divergence

- A designated compliance lead or outsourced compliance service is required.
- Training emphasis shifts toward program rules (LIHTC, HUD, state).
- Agency relationships add a coordination surface not present in middle-market.

## Amenity and service divergence

- Service standards remain; amenity investment levels may differ based on
  underwriting and program constraints.
- Resident services programming (financial literacy, after-school, workforce
  resources) may be required under certain programs.

## What Phase 1 does not build

- Full overlay.yaml depth.
- Compliance workflow packs.
- Program-specific rent-limit and utility-allowance reference schedules.
- Program-specific approval matrix overrides (e.g., REAC/NSPIRE escalation).

These remain on the roadmap and are expected to be built after middle-market depth
is stabilized.
