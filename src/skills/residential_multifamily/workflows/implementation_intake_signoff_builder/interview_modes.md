# Interview Modes

## Executive Overview

- **Mode id:** `executive_overview`
- **Use when:** scope, sponsor, business objective, systems covered, or sign-off audience are still unclear.
- **Primary audience:** COO, CFO, implementation sponsor, portfolio leadership.
- **Outputs emphasized:** implementation objective, systems and environments covered, confirmed facts, unresolved assumptions, blockers, top risks, decisions requested, approvals requested, recommendation.

## Source-By-Source Implementation Discovery

- **Mode id:** `source_by_source_implementation_discovery`
- **Use when:** actual systems, owners, modules, environments, access paths, and deployment caveats must be documented system by system.
- **Primary audience:** systems admin, implementation PM, finance systems owner, operations systems owner.
- **Outputs emphasized:** source inventory register, source instance register, access model packet.

## Field-Level Export And File Inventory

- **Mode id:** `field_level_export_and_file_inventory`
- **Use when:** sample exports, workbooks, PDFs, tabs, columns, dictionaries, or actual field names are needed for connector or mapping work.
- **Primary audience:** data lead, analyst, implementation engineer, reporting owner.
- **Outputs emphasized:** export and field inventory, evidence set, missing-doc log.

## Crosswalk And Identity Mapping

- **Mode id:** `crosswalk_and_identity_mapping`
- **Use when:** property, unit, vendor, project, account, market, reporting-entity, or other identity rules must be confirmed.
- **Primary audience:** data lead, implementation architect, reporting finance lead.
- **Outputs emphasized:** crosswalk register, source-of-truth register, exception log.

## Reporting Calendar And SLA

- **Mode id:** `reporting_calendar_and_sla`
- **Use when:** close timing, weekly reviews, monthly owner reporting, investor deadlines, benchmark refresh cadence, or approval SLAs are still fuzzy.
- **Primary audience:** controller, reporting lead, operations lead, asset manager.
- **Outputs emphasized:** reporting calendar and SLA register, blocker log, action queue.

## Approval And Controls

- **Mode id:** `approval_and_controls`
- **Use when:** access requests, mapping approvals, benchmark approvals, financially material approvals, legal-sensitive output approvals, or escalation paths need to be explicit.
- **Primary audience:** sponsor, controller, operations lead, technology owner.
- **Outputs emphasized:** approval matrix summary, controls summary, decisions requested, approvals requested.

## Missing-Doc Chase

- **Mode id:** `missing_doc_chase`
- **Use when:** the workflow is blocked by missing sample exports, field dictionaries, calendars, approval matrices, property lists, project lists, or other key artifacts.
- **Primary audience:** whoever owns the missing artifact.
- **Outputs emphasized:** missing docs and blockers log, owner follow-up dates, action queue.

## Sign-Off Packaging

- **Mode id:** `signoff_packaging`
- **Use when:** leadership needs a concise review packet that clearly states what is confirmed, assumed, blocked, risky, and requested.
- **Primary audience:** COO, CFO, implementation sponsor, executive reviewer.
- **Outputs emphasized:** implementation intake packet, leader sign-off pack, action queue.

## Exception Resolution

- **Mode id:** `exception_resolution`
- **Use when:** evidence conflicts, crosswalk ownership is ambiguous, source-of-truth rules disagree, or approvals are blocked without an agreed escalation path.
- **Primary audience:** decision owner, data lead, implementation sponsor.
- **Outputs emphasized:** exception summary, decision log, updated blockers, revised action queue.

## Progressive Disclosure Rules

- Start with the shallowest mode that can answer the next real question.
- Move to deeper modes only when the current evidence shows a real implementation gap.
- Keep questions hidden when systems, roles, or management modes make them irrelevant.
- Show blockers as soon as they appear, not only at final packaging time.
