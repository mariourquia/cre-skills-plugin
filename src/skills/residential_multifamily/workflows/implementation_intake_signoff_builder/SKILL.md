---
name: Implementation Intake And Leader Sign-Off Builder
slug: implementation_intake_signoff_builder
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  This workflow stores interview state, evidence references, assumptions, blockers,
  and packet previews in a local session workspace. Those records become stale when
  source systems change, reporting calendars move, owners change, or new artifacts
  arrive. The workflow never treats assumptions as confirmed without explicit evidence.
applies_to:
  segment: [middle_market, affordable, luxury]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [pre_acquisition, development, construction, lease_up, stabilized, renovation, recap_support, disposition]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role:
    - coo_operations_leader
    - cfo_finance_leader
    - director_of_operations
    - regional_manager
    - asset_manager
    - portfolio_manager
    - development_manager
    - construction_manager
    - reporting_finance_ops_lead
    - third_party_manager_oversight_lead
  output_types: [memo, checklist, operating_review, dashboard]
  decision_severity_max: action_requires_approval
references:
  reads:
    - workflows/implementation_intake_signoff_builder/question_bank.yaml
    - workflows/implementation_intake_signoff_builder/evidence_model.yaml
    - workflows/implementation_intake_signoff_builder/interview_modes.md
    - workflows/implementation_intake_signoff_builder/workflows.md
    - workflows/implementation_intake_signoff_builder/schemas/source_inventory_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/source_instance_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/export_field_inventory_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/credentials_model_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/crosswalk_rules_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/source_of_truth_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/reporting_calendar_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/blocker_log_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/assumptions_log_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/decision_log_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/evidence_item_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/signoff_packet_schema.yaml
    - workflows/implementation_intake_signoff_builder/schemas/action_queue_schema.yaml
    - workflows/implementation_intake_signoff_builder/templates/implementation_intake_packet_template.md
    - workflows/implementation_intake_signoff_builder/templates/signoff_packet_template.md
    - workflows/implementation_intake_signoff_builder/templates/action_queue_template.md
    - tailoring/AUDIENCE_MAP.md
    - tailoring/MISSING_DOC_MATRIX.md
    - reference/connectors/source_registry/source_registry.yaml
    - reference/connectors/source_registry/implementation_inventory.md
    - reference/connectors/_core/config_overlay_interaction.md
    - reference/connectors/_core/third_party_manager_oversight.md
    - reference/connectors/master_data/identity_resolution_framework.md
    - reference/connectors/master_data/survivorship_rules.md
    - reference/connectors/adapters/appfolio_pms/manifest.yaml
    - reference/connectors/adapters/sage_intacct_gl/manifest.yaml
    - reference/connectors/adapters/procore_construction/manifest.yaml
    - reference/connectors/adapters/dealpath_deal_pipeline/manifest.yaml
    - reference/connectors/adapters/graysail_placeholder/manifest.yaml
    - reference/connectors/adapters/yardi_multi_role/manifest.yaml
    - reference/connectors/adapters/manual_sources_expanded/manifest.yaml
  writes:
    - workflows/implementation_intake_signoff_builder/sessions/{engagement_id}/{session_id}.yaml
    - workflows/implementation_intake_signoff_builder/sessions/{engagement_id}/{session_id}__preview.md
    - workflows/implementation_intake_signoff_builder/sessions/{engagement_id}/{session_id}__leader_signoff.md
    - workflows/implementation_intake_signoff_builder/sessions/{engagement_id}/{session_id}__action_queue.md
metrics_used: []
escalation_paths:
  - kind: missing_load_bearing_evidence
    to: implementation_pm -> executive_sponsor
  - kind: conflicting_source_of_truth
    to: data_lead -> business_owner -> executive_sponsor
  - kind: blocked_access_or_approval
    to: system_owner -> implementation_sponsor
  - kind: secret_storage_attempt
    to: refuse and require metadata-only capture
approvals_required:
  - implementation_scope_signoff
  - access_provisioning_signoff
  - crosswalk_approval
  - source_of_truth_approval
  - leader_signoff_packet_approval
description: |
  Evidence-driven implementation intake workflow for residential multifamily and
  related CRE operating environments. Guides sponsors, implementation leads, data
  teams, operations leaders, and reporting owners through source inventory, access
  readiness, export evidence, field-level semantics, crosswalk ownership, reporting
  calendar, approvals, blockers, assumptions, and final leader sign-off. Produces
  implementation packets that are usable by both executives and build teams, while
  refusing silent assumption upgrades and refusing secret storage.
---

# Implementation Intake And Leader Sign-Off Builder

## Workflow purpose

Capture the real implementation facts required to move from architecture and planning into build execution. The workflow is evidence-led, progressive, resumable, and explicit about what is confirmed, what is only assumed, what is missing, what is blocked, who owns each unresolved item, and what leadership is being asked to approve.

This workflow is designed for mixed operating environments: direct-system access, file-only third-party manager submissions, legacy-system coexistence, construction and development stacks, benchmark workbooks, shared-drive reports, and emailed operating packs. It does not accept vague statements like "we use AppFolio" as implementation-ready.

## Trigger conditions

- **Explicit:** "implementation intake", "implementation discovery", "sign-off memo", "sign-off packet", "systems and environments covered", "capture source inventory", "gather evidence for build readiness", "prepare leadership sign-off".
- **Implicit:** connector onboarding cannot proceed because source scope, environments, field layouts, approvals, or owners are still unclear.
- **Recurring:** resume sessions, missing-doc chase, and leadership-review refresh before a build phase or milestone gate.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Sponsor objective and implementation scope | narrative | required | plain-language objective, scope, and success definition |
| Source inventory | register | required | systems, modules, environments, owners, status |
| Evidence set | register | required | artifacts, screenshots, exports, report packs, mappings |
| Export and field inventory | register | required | actual files, tabs, columns, sample values, quirks |
| Access model | register | required | access path, provisioning flow, approvals, restrictions |
| Crosswalk and source-of-truth rules | register | required | entity keys, precedence, overrides, approval owner |
| Reporting calendar and SLA map | register | required | close, reviews, owner reporting, approvals |
| Missing-doc and blocker log | register | required | unresolved artifacts, blocked approvals, follow-up dates |
| Assumptions and confidence log | register | required | every unresolved assumption, evidence gap, and impact |
| Decision log | register | required | confirmed implementation decisions and downstream effect |
| Leader review context | narrative | required | requested decisions, approvals, owners, dates, recommendation |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Implementation intake packet | `operating_review` | concise readiness summary for build teams and sponsors |
| Source inventory register | `checklist` | one record per system, owner, environment, confidence, blocker |
| Source instance register | `checklist` | one record per environment or instance |
| Export and field inventory | `checklist` | one record per export family or key field set |
| Credentials and access model packet | `memo` | metadata only, no secrets |
| Crosswalk and source-of-truth register | `checklist` | entity mapping rules, precedence, owners, approvals |
| Reporting calendar and SLA register | `checklist` | cadence, owner, dependency, escalation |
| Missing docs and blockers log | `checklist` | explicit outstanding items with severity and due dates |
| Assumptions and confidence log | `checklist` | every assumption and why it still exists |
| Decision log | `checklist` | every implementation decision and follow-up |
| Leader sign-off pack | `memo` | concise executive-ready sign-off memo |
| Action queue | `checklist` | prioritized next actions by business, technical, data, reporting, controls, and dependencies |

## Required context

`asset_class`, `management_mode`, sponsor role, implementation sponsor or owner, systems in scope, source environments in scope, and the intended implementation phase. `segment`, `form_factor`, `lifecycle_stage`, `market`, `org_id`, and `workflow` sharpen routing but are not the only signals.

## Process

1. **Anchor the implementation objective.** Record the business outcome, in-scope systems, in-scope environments, required sign-off audience, and build phase this packet is intended to authorize.
2. **Stage the interview path.** Resolve the correct mode: executive overview, source-by-source discovery, field inventory, crosswalk mapping, reporting calendar, approvals and controls, missing-doc chase, sign-off packaging, or exception resolution.
3. **Build the source inventory.** For every source, capture the actual business role, active or legacy status, module scope, environment scope, owner, admin contact, and source-of-truth candidacy.
4. **Capture actual access and export facts.** Record access method, sandbox and production availability, export owner, credentials owner, provisioning flow, refresh cadence, restrictions, and evidence received. Metadata only. No secrets.
5. **Capture actual files and fields.** Record actual export names, tabs, columns, sample values, null behavior, quirks, and transformation needs. Require screenshots, exports, report packs, dictionaries, or other artifacts when available.
6. **Capture crosswalk and source-of-truth rules.** Document identity resolution keys, fallback keys, manual override path, effective-date rules, precedence logic, disagreement rules, and approval owner for each important entity family.
7. **Capture cadence and controls.** Record reporting calendar, close cadence, review meetings, owner reporting deadlines, approval SLAs, and escalation path for blocked approvals or late inputs.
8. **Surface missing evidence early.** Every unanswered or unsupported load-bearing answer is marked `missing`, `blocked`, or `conflicting`. The workflow opens a missing-doc or blocker item immediately rather than at the end.
9. **Score confidence without upgrading assumptions.** Confirmed evidence raises confidence. Verbal answers, inferred answers, third-party-manager-submitted files, and unresolved conflicts keep confidence lower.
10. **Assemble execution-ready artifacts.** Produce the intake packet, registers, blocker log, assumptions log, decision log, and action queue before leadership review begins.
11. **Assemble the leader sign-off pack.** Produce a concise memo covering objective, systems and environments, confirmed facts, assumptions, blockers, top risks, decisions requested, approvals requested, owners and dates, recommendation, and approval section.
12. **Pause and resume safely.** Persist session state after every answer and preview render. Resume from the saved queue, not from memory.
13. **Refuse unsafe behavior.** Never store actual passwords, API keys, tokens, or bearer strings. Never mark an assumption as confirmed without explicit evidence. Never mutate canonical definitions or connector contracts from this workflow.

## Metrics used

This workflow uses section progress, evidence coverage, blocker count, and confidence scoring inside its session engine, but it does not yet declare canonical subsystem metrics in `_core/metrics.md`. Until those contracts are promoted to canonical status, they remain local workflow controls rather than routed metrics.

## Reference files used

- `workflows/implementation_intake_signoff_builder/question_bank.yaml`
- `workflows/implementation_intake_signoff_builder/evidence_model.yaml`
- `workflows/implementation_intake_signoff_builder/interview_modes.md`
- `workflows/implementation_intake_signoff_builder/schemas/*.yaml`
- `workflows/implementation_intake_signoff_builder/templates/*.md`
- `tailoring/AUDIENCE_MAP.md`
- `tailoring/MISSING_DOC_MATRIX.md`
- `reference/connectors/source_registry/source_registry.yaml`
- `reference/connectors/source_registry/implementation_inventory.md`
- `reference/connectors/_core/config_overlay_interaction.md`
- `reference/connectors/_core/third_party_manager_oversight.md`
- adapter manifests for AppFolio, Sage Intacct, Procore, Dealpath, GraySail, Yardi, and manual-source expansion

## Escalation points

- **Missing load-bearing evidence.** The packet may continue in draft, but leadership review is blocked until the missing artifact owner is named and due date set.
- **Conflicting source-of-truth or crosswalk logic.** The workflow moves to exception resolution and names the owner required to decide.
- **Blocked access or approvals.** The workflow escalates to the system owner and implementation sponsor.
- **Third-party-manager file-only reporting.** The workflow continues, but confidence is reduced and the sign-off pack names the dependency explicitly.
- **Secret-storage attempt.** The workflow refuses the value and asks for metadata only.

## Required approvals

- Implementation scope sign-off.
- Access provisioning sign-off.
- Crosswalk approval.
- Source-of-truth approval.
- Leader sign-off packet approval.

## Failure modes

1. Treating a system name as implementation readiness. Fix: require environment, module, access path, and evidence.
2. Treating verbal confirmation as confirmed fact. Fix: keep it `confirmed_verbal` until evidence arrives.
3. Forgetting legacy or partial sources. Fix: source inventory includes active, partial, planned, legacy, and historical statuses.
4. Capturing credentials in plain text. Fix: reject secret-like values and capture owner, method, and approval path only.
5. Hiding blockers until the end. Fix: blockers open as soon as missing evidence or approval dependencies are known.
6. Producing an executive memo that is too vague for implementation. Fix: every memo section links back to structured registers and logs.
7. Producing an engineer packet that is unreadable for leadership. Fix: keep the sign-off memo concise and plain-language while preserving explicit facts, assumptions, owners, and approvals.

## Edge cases

- **Third-party manager file-only environment:** direct system access is absent, monthly packs arrive late, and calendars differ. The workflow supports it, but confidence remains lower until owner-side evidence improves.
- **Legacy Yardi plus AppFolio coexistence:** the workflow records both systems, marks the legacy source explicitly, and requires a clear source-of-truth rule for overlapping objects.
- **GraySail or workbook-driven benchmarks:** the workflow captures workbook ownership, refresh cadence, attestation path, and evidence source rather than assuming the benchmark is governed.
- **Development and construction mixed with stabilized operations:** Procore and Dealpath can be in scope alongside AppFolio and Intacct. The workflow keeps build-phase and operating-phase evidence separate, then reconciles them in the sign-off packet.
- **Multiple stakeholders over time:** session persistence is first-class, so a controller, operations lead, and sponsor can enrich the same packet across several reviews.

## Example invocations

1. "Run implementation intake for the Sunrise owner-oversight portfolio and prepare a sponsor sign-off memo."
2. "We need the real source inventory, export evidence, and crosswalk ownership before build starts."
3. "Package the implementation assumptions, blockers, decisions requested, and approvals requested for the COO and CFO."

## Example outputs

### Output — Leader sign-off pack (abridged)

**Implementation objective.** Build-ready onboarding package for AppFolio operations, Sage Intacct finance, Procore construction, Dealpath pipeline, GraySail benchmark workbooks, and Yardi legacy exports.

**Systems and environments covered.** Production and sandbox environments are named explicitly. Legacy Yardi remains in scope for a defined subset of properties.

**Confirmed facts.** AppFolio operations exports, monthly close calendar, source inventory ownership, and current approval routing are evidence-backed.

**Assumptions and blockers.** Intacct field dictionary, one Yardi export sample, and the benchmark refresh owner remain unresolved.

**Recommendation.** Approve build-readiness with conditions only after the named blockers clear and the requested decisions are assigned.
