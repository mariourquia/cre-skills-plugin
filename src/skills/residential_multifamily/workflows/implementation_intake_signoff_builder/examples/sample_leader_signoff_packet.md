# Leader Sign-Off Pack

## Document Purpose

Authorize or reject the move from planning into build execution for the Sunrise owner-oversight implementation.

## Implementation Objective

Stand up an evidence-backed implementation package for AppFolio operations, Sage Intacct finance, Procore construction, Dealpath pipeline, GraySail benchmark updates, Yardi legacy reporting, and third-party-manager submissions.

## Systems And Environments Covered

- AppFolio east-region production
- Sage Intacct production
- Procore production
- Dealpath production
- GraySail workbook delivery path
- Yardi legacy export path
- Third-party-manager monthly owner packs delivered through shared drive and email

## What Has Been Confirmed

- AppFolio operating scope, property coverage, and core export path are documented.
- Monthly close and owner reporting cadence are documented.
- Access provisioning ownership is named for owner-managed systems.
- The initial property and reporting-entity crosswalk direction is defined.

## What Is Still Assumed

- GraySail appears to be the benchmark owner, but the workbook and owner confirmation are still pending.
- Yardi legacy scope appears limited to a short list of properties, but the signed sunset list is still pending.
- Third-party-manager file submissions are assumed to remain the interim source for one region until direct access is approved.

## What Is Blocked

- Intacct field dictionary and dimension semantics are still missing.
- One Yardi legacy mapping conflicts with the owner reporting hierarchy.
- The third-party manager has not yet delivered delinquency backup and attestation for the file-only properties.

## Top Three Risks

- Mapping and report design can stall if Intacct field semantics are not delivered on time.
- Portfolio rollups can misstate property or reporting-entity results if the Yardi conflict remains open.
- Confidence will remain reduced for file-only properties if the third-party-manager backup continues to arrive late.

## Decisions Requested

- Confirm the final source-of-truth owner for development and capex reporting across Procore, Dealpath, and Intacct.
- Confirm whether Yardi legacy reporting remains in scope after the next close cycle.
- Confirm whether conditional build start is acceptable while third-party-manager backup remains file-only.

## Approvals Requested

- Approve the access provisioning path for Intacct exports.
- Approve the initial property and reporting-entity crosswalk rule.
- Approve conditional build readiness once the named blockers are closed or formally waived.

## Owners And Dates

- Controller: provide Intacct field dictionary by April 18, 2026.
- Data lead: resolve Yardi legacy conflict by April 16, 2026.
- TPM oversight lead: obtain missing backup and attestation by April 17, 2026.

## Recommendation

Approve with conditions. The packet is strong enough to guide build planning, but not strong enough for unrestricted execution until the blocked items above are closed or leadership accepts the named residual risk explicitly.

## Approval Section

- Reviewer name:
- Reviewer role:
- Review date:
- Approval status: pending leadership review
- Approval notes:
- Conditions if any:
