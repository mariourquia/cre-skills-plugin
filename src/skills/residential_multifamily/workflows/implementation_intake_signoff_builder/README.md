# Implementation Intake And Leader Sign-Off Builder

## Assumptions And Repo Fit Notes

- This package extends the existing `residential_multifamily` subsystem as a workflow pack, not as a standalone subsystem.
- The design intentionally follows the `tailoring/` pattern for progressive disclosure, session persistence, missing-doc tracking, preview, and sign-off gating.
- The workflow writes only to its own session workspace under `workflows/implementation_intake_signoff_builder/sessions/`. It does not mutate `_core/`, `overlays/`, `reference/`, or connector contracts.
- Actual secrets are out of scope. The workflow captures credential ownership, approval path, and provisioning method only.
- The empty scaffold at `workflows/implementation_intake_signoff_builder/` existed before this implementation. No overlapping edits were present in this worktree when this package was built.

## Final Proposed File Tree

```text
workflows/implementation_intake_signoff_builder/
  README.md
  SKILL.md
  routing.yaml
  reference_manifest.yaml
  workflows.md
  interview_modes.md
  question_bank.yaml
  evidence_model.yaml
  schemas/
    action_queue_schema.yaml
    assumptions_log_schema.yaml
    blocker_log_schema.yaml
    credentials_model_schema.yaml
    crosswalk_rules_schema.yaml
    decision_log_schema.yaml
    evidence_item_schema.yaml
    export_field_inventory_schema.yaml
    reporting_calendar_schema.yaml
    session_state_schema.yaml
    signoff_packet_schema.yaml
    source_instance_schema.yaml
    source_inventory_schema.yaml
    source_of_truth_schema.yaml
  templates/
    action_queue_template.md
    implementation_intake_packet_template.md
    signoff_packet_template.md
  examples/
    ex01_owner_oversight_multisystem/
      INPUT.md
      ROUTING.md
      OUTPUT.md
    sample_action_queue.md
    sample_assumptions_log.yaml
    sample_blocker_log.yaml
    sample_decision_log.yaml
    sample_evidence_set.yaml
    sample_implementation_intake_packet.md
    sample_leader_signoff_packet.md
    sample_session_state.yaml
  sessions/
    .gitignore
    README.md
  tests/
    README.md
  tools/
    implementation_intake_tui.py
```

## Skill Purpose And User Flows

The workflow moves a multifamily implementation from vague planning into execution-ready intake. It captures the real source inventory, evidence-backed export facts, field names, access model, crosswalk logic, reporting cadence, approvals, blockers, assumptions, decisions, and sponsor sign-off needed for downstream build work.

Primary user flows:

- Executive sponsor starts with a short scope and sign-off brief, then delegates detailed evidence capture.
- Implementation lead runs source-by-source discovery and records what is confirmed, assumed, blocked, or conflicting.
- Data and systems leads capture export layouts, crosswalk ownership, source-of-truth rules, and access constraints.
- Reporting and operations leads document close calendars, review cadences, owner reporting packs, and approval SLAs.
- Leadership reviews a concise sign-off packet before the build phase begins.

## Interview Modes And Routing Logic

See [interview_modes.md](./interview_modes.md). The workflow supports nine guided modes:

- `executive_overview`
- `source_by_source_implementation_discovery`
- `field_level_export_and_file_inventory`
- `crosswalk_and_identity_mapping`
- `reporting_calendar_and_sla`
- `approval_and_controls`
- `missing_doc_chase`
- `signoff_packaging`
- `exception_resolution`

Routing logic is progressive:

- Start with `executive_overview` when scope, sponsor, and implementation objective are not yet explicit.
- Drop into source-specific, field-specific, crosswalk, reporting, or controls modes only when the preceding evidence suggests that deeper detail is required.
- Surface `missing_doc_chase` as soon as a required artifact is absent.
- Use `signoff_packaging` only after confirmed facts, assumptions, blockers, and decisions are explicit.
- Use `exception_resolution` when evidence conflicts or ownership is unclear.

## Question Bank Design

See [question_bank.yaml](./question_bank.yaml). Each question carries:

- `question_id`
- `category`
- `audience`
- `trigger_condition`
- `prerequisite_questions`
- `question_text`
- `why_this_matters`
- `expected_answer_type`
- `evidence_requested`
- `severity_if_unanswered`
- `confidence_effect`
- `related_objects`
- `related_outputs`
- `skip_logic`
- `follow_up_logic`

The question bank is intentionally evidence-aware, role-aware, and system-aware. AppFolio, Sage Intacct, Procore, Dealpath, GraySail, Yardi, manual spreadsheets, emailed report packs, and third-party manager submissions are all first-class question paths.

## Evidence Model Design

See [evidence_model.yaml](./evidence_model.yaml). The workflow separates:

- answer status: `confirmed_by_artifact`, `confirmed_by_screenshot`, `confirmed_by_export`, `confirmed_by_document`, `confirmed_verbal`, `inferred`, `assumed`, `missing`, `blocked`, `conflicting`
- evidence lifecycle: `received_not_reviewed`, `reviewed_incomplete`, `reviewed_sufficient`, `conflicting_with_prior`
- coverage level: `single_property`, `multi_property_partial`, `portfolio_full`, `system_partial`, `system_full`

Confidence is derived from both answer status and evidence quality. Third-party-manager-submitted evidence is allowed, but it lowers confidence unless matched to source-native artifacts.

## Schemas And Templates

Schemas live under [schemas](./schemas/) and cover the required registers and logs:

- source inventory
- source instance
- export and field inventory
- credentials and access model
- crosswalk rules
- source-of-truth rules
- reporting calendar
- blocker log
- assumptions log
- decision log
- sign-off packet
- action queue
- evidence item
- session state

Templates live under [templates](./templates/):

- [implementation_intake_packet_template.md](./templates/implementation_intake_packet_template.md)
- [signoff_packet_template.md](./templates/signoff_packet_template.md)
- [action_queue_template.md](./templates/action_queue_template.md)

## Output Artifact Definitions

The workflow produces the following artifacts:

- Implementation Intake Packet
- Source Inventory Register
- Source Instance Register
- Export And Field Inventory
- Credentials And Access Model Packet
- Crosswalk And Source-Of-Truth Register
- Reporting Calendar And SLA Register
- Missing Docs And Blockers Log
- Assumptions And Confidence Log
- Decision Log
- Leader Sign-Off Pack
- Action Queue

Each output is designed for both implementation execution and leadership review. The sign-off pack is intentionally plain-language and brief, while still naming assumptions, blockers, owners, approvals, and decisions.

## Sample Sign-Off Packet

See [sample_leader_signoff_packet.md](./examples/sample_leader_signoff_packet.md). It includes:

- implementation objective
- systems and environments covered
- confirmed facts
- unresolved assumptions
- blocked items
- top three risks
- decisions requested
- approvals requested
- owners and dates
- recommendation
- approval section

## Examples

The example set includes:

- a routed workflow example: [ex01_owner_oversight_multisystem](./examples/ex01_owner_oversight_multisystem)
- a sample evidence set: [sample_evidence_set.yaml](./examples/sample_evidence_set.yaml)
- a sample intake packet: [sample_implementation_intake_packet.md](./examples/sample_implementation_intake_packet.md)
- a sample leader sign-off packet: [sample_leader_signoff_packet.md](./examples/sample_leader_signoff_packet.md)
- a sample blocker log: [sample_blocker_log.yaml](./examples/sample_blocker_log.yaml)
- a sample assumptions log: [sample_assumptions_log.yaml](./examples/sample_assumptions_log.yaml)
- a sample decision log: [sample_decision_log.yaml](./examples/sample_decision_log.yaml)
- a sample session state: [sample_session_state.yaml](./examples/sample_session_state.yaml)
- a sample action queue: [sample_action_queue.md](./examples/sample_action_queue.md)

## Tests And Validation Checks

Validation is split between the workflow tool and subsystem pytest coverage:

- question metadata completeness
- mode coverage and category coverage
- trigger and skip behavior
- blocker and missing-doc detection
- evidence tagging and conflict detection
- confidence scoring
- no-secret-storage guardrails
- sign-off packet generation
- action queue generation
- resume behavior
- canonical-base protection
- third-party manager mode behavior

See [tests/README.md](./tests/README.md) and the subsystem pytest file under `src/skills/residential_multifamily/tests/`.

## Open Risks, Limitations, And Next Enhancements

- The terminal helper is intentionally lightweight. It is suitable for guided intake and preview, but not yet a full multi-user case-management console.
- The workflow captures crosswalk logic and source-of-truth rules, but it does not apply connector or master-data changes automatically.
- Sample artifacts are implementation-grade examples, not live production records.
- Future enhancement areas: richer attachment ingestion, deeper schema validation against real uploaded files, automatic packet assembly from live evidence folders, and connector-specific intake accelerators by vendor family.
