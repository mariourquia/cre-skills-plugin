# Sample Implementation Intake Packet

## Implementation Objective

Prepare the Sunrise owner-oversight portfolio for build execution across AppFolio, Sage Intacct, Procore, Dealpath, GraySail benchmark workbooks, Yardi legacy reporting, and third-party-manager file submissions.

## Systems In Scope

- AppFolio operations
- Sage Intacct finance
- Procore construction and capex
- Dealpath pipeline and approvals
- GraySail benchmark workbook flow
- Yardi legacy exports
- Third-party-manager owner packs

## Environments In Scope

- AppFolio east-region production
- Intacct production
- Procore production
- Dealpath production
- GraySail workbook drop
- Yardi legacy export path

## Current Confidence

Medium overall. AppFolio scope, reporting calendar, and access routing are confirmed. Intacct field semantics, one legacy Yardi mapping, and third-party-manager backup still reduce readiness.

## Key Blockers

- Intacct field dictionary is still missing.
- Yardi legacy reporting-entity mapping conflicts with the owner reporting hierarchy.
- Third-party-manager delinquency backup is not yet attached.

## Main Dependencies

- Finance must provide the Intacct field semantics needed for mapping and reporting design.
- Data lead must clear the Yardi conflict before crosswalk logic is locked.
- TPM oversight lead must obtain the missing backup and attestation for file-only reporting.

## Readiness Summary

The implementation can move from architecture into conditional build preparation, but not into unrestricted execution. Source inventory, access routing, and calendar expectations are now explicit. Remaining risk is concentrated in field semantics, legacy identity mapping, and third-party-manager evidence quality.

## Immediate Next Actions

- Close the Intacct field dictionary gap.
- Resolve the Yardi reporting-entity conflict.
- Obtain the missing TPM delinquency backup.
- Return the packet for final sponsor review once those items are either closed or explicitly waived.
