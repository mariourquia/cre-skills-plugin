# Missing Document Matrix — Tailoring

The canonical specification for missing-document detection, tracking, and lifecycle across the 8-audience tailoring interview. A missing document is any policy, template, playbook, contract, or reference artifact that the tailoring skill determines is needed to ground one or more overlay keys. The skill never fabricates the content of a missing document; it records the gap, tracks the fulfillment, and blocks the dependent overlay keys from the session diff until the document is mapped.

This document works in tandem with `tailoring/missing_docs_queue.yaml` (the runtime queue) and `tailoring/doc_catalog.yaml` (the catalog of known document slugs).

## Status enum

Every entry in `missing_docs_queue.yaml` carries one of the following statuses:

| Status | Description |
|---|---|
| `requested` | The tailoring skill asked for the document during an interview. Waiting on the operator to provide it. Dependent overlay keys are marked `pending_doc` in the session state. |
| `received` | The document arrived in `tailoring/inbound/{org_id}/` (or an operator-designated inbound path). Not yet parsed; overlay keys remain `pending_doc`. |
| `mapped` | The document has been parsed (manually or by an ingest handler) and the overlay keys it fills have values. The queue entry is closed and the `pending_doc` flag is cleared on the dependent keys. |
| `missing` | The document was requested, has not been received, and the interim `substitute_behavior` is active. Dependent overlay keys remain `pending_doc`; the session can still produce a preview, but the preview marks those keys as incomplete. |
| `blocked` | A `priority: p1` document is `missing` with no valid `substitute_behavior`, and the dependent overlay keys are load-bearing for a requested output. The dependent keys are excluded from the preview diff entirely. The operator must either produce the document or explicitly accept a named fallback before the overlay can be applied. |

Status transitions: `requested → received → mapped` (happy path). `requested → missing` after the substitute_behavior grace window elapses. `missing → blocked` when a p1 document remains `missing` past the block threshold. `received → mapped` requires an ingest handler or manual mapping entry in the session.

## Audience → expected documents → overlay keys

Each audience has an expected document list. The tailoring skill triggers a `missing_docs_queue` entry whenever an interview answer would be grounded by one of these documents and the operator cannot produce it in-session.

### executive

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `org_chart` | Executive / operating org chart | `overlay.yaml#org_chart_ref`, `overlay.yaml#staffing_ratios.*` |
| `approval_matrix_policy` | Operator's written approval matrix policy | `overlay.yaml#approval_matrix.*` thresholds and approver lists |
| `portfolio_segmentation_policy` | How the operator segments its portfolio (segment, program, region) | `overlay.yaml#portfolio_segmentation.*` |
| `risk_tolerance_policy` | Written risk tolerance posture | `overlay.yaml#risk_tolerance.*`, `overlay.yaml#capital_allocation.*` |

### regional_ops

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `regional_operating_cadence` | RM / DOO operating cadence document | `overlay.yaml#regional_ops.cadence.*` |
| `portfolio_map` | Portfolio map (properties → regions → RMs) | `overlay.yaml#regional_ops.region_assignments` |
| `regional_staffing_model` | Regional staffing model (span of control, regional roles) | `overlay.yaml#staffing_ratios.regional_*` |

### asset_mgmt

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `business_plan_template` | Operator's standard business plan template for a property | `overlay.yaml#asset_mgmt.business_plan_schema` |
| `variance_threshold_policy` | Asset-level variance thresholds for alert / escalation | `overlay.yaml#asset_mgmt.variance_thresholds.*` |
| `hold_period_policy` | Target hold period / disposition posture | `overlay.yaml#asset_mgmt.hold_period_*` |

### finance_reporting

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `chart_of_accounts` | Current chart of accounts plus NOI-category mapping | `overlay.yaml#finance.coa_ref` |
| `budget_template` | Standard budget template | `overlay.yaml#finance.budget_template_ref` |
| `variance_policy` | CFO-level variance policy (thresholds, escalation) | `overlay.yaml#finance.variance_policy.*` |
| `investor_reporting_cadence` | Investor / LP reporting cadence and format | `overlay.yaml#reporting.investor_cadence` |
| `lender_reporting_cadence` | Lender reporting cadence and covenant package | `overlay.yaml#reporting.lender_cadence`, `overlay.yaml#reporting.covenant_package_ref` |

### development

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `development_underwriting_assumptions` | Standard dev underwriting assumption set | `overlay.yaml#development.underwriting_assumption_ref` |
| `developer_fee_structure` | Developer fee structure (tiers, earn schedule) | `overlay.yaml#development.developer_fee_structure` |
| `preconstruction_sign_off_policy` | Preconstruction sign-off gate definition | `overlay.yaml#development.preconstruction_sign_off_policy` |

### construction

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `gc_selection_criteria` | GC selection / shortlist criteria | `overlay.yaml#construction.gc_selection_criteria` |
| `contract_structure_policy` | Preferred contract structure (GMP, lump sum, cost-plus) | `overlay.yaml#construction.contract_structure_policy` |
| `change_order_policy` | Change-order approval policy | `overlay.yaml#construction.change_order_policy` |
| `draw_approval_policy` | Draw-request approval policy and sequencing | `overlay.yaml#construction.draw_approval_policy` |

### compliance_risk

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `fair_housing_training_policy` | Fair housing training cadence and content | `overlay.yaml#compliance_fair_housing.*` |
| `screening_policy_document` | Resident screening policy (criteria, adverse-action process) | `overlay.yaml#compliance_screening.*` |
| `vawa_policy` | VAWA compliance policy | `overlay.yaml#compliance_vawa.*` |
| `emergency_response_playbook` | Emergency response and life-safety playbook | `overlay.yaml#compliance_emergency_response.*` |
| `regulatory_program_participation_list` | List of properties and the regulatory programs they participate in | `overlay.yaml#compliance_regulatory_programs.*` |

### site_ops

| doc_slug | doc_title | Fills overlay keys (examples) |
|---|---|---|
| `site_operating_manual` | Site operating manual (PM norms, coverage, escalation) | `overlay.yaml#site_ops.manual_ref` |
| `staffing_schedule_template` | Default staffing schedule by form factor | `overlay.yaml#site_ops.staffing_schedule_ref` |
| `unit_turn_sop` | Unit turn scope and SOP | `overlay.yaml#site_ops.unit_turn_sop_ref` |
| `work_order_sop` | Work order intake, triage, SLA SOP | `overlay.yaml#site_ops.work_order_sop_ref` |

## Protocol

### How a missing-doc entry is created

1. An interview answer references a policy, template, or reference artifact the skill does not currently have (for example, the operator says "our approval thresholds are in our approval matrix policy — I can send it later").
2. The skill looks up the `doc_slug` in `tailoring/doc_catalog.yaml` to confirm the slug exists and to read its `overlay_keys_filled` list.
3. The skill writes a new entry in `tailoring/missing_docs_queue.yaml` with: `doc_slug`, `doc_title`, `requested_from_role`, `requested_at`, `priority` (p1 / p2 / p3 per the trigger), `used_by_overlay_keys` (copied from the catalog), `substitute_behavior` (copied from the catalog), `status: requested`, `notes` (the interview context).
4. The skill marks the dependent `used_by_overlay_keys` as `pending_doc` in the current session state.
5. The skill tells the operator: the doc name, why it is needed, which overlay keys depend on it, and the interim behavior.

### How substitute_behavior works while the doc is missing

Every entry in `doc_catalog.yaml` carries a `substitute_behavior` field that describes what the skill does while the document is `missing`. Three canonical behaviors:

- `use_canonical_default` — use the value from `overlays/org/_defaults/` for the dependent keys; mark them `pending_doc` but still include them in the preview as provisional.
- `refuse_to_render` — do not include the dependent keys in the preview at all; any downstream pack asking for them gets a `pending_doc` refusal.
- `prompt_in_session` — walk the operator through a structured set of questions that stand in for the document; the answers are recorded with a `provenance: interview_substitute` flag so they can be replaced when the document arrives.

The substitute_behavior is advisory to the tailoring skill; the behavior chosen for any given doc is set in `doc_catalog.yaml` and should not be overridden per session.

### Blocker criteria

An entry reaches `blocked` status (dependent overlay keys excluded from preview) when all three are true:

1. Priority is `p1`.
2. Status has been `missing` past the block threshold (default 14 days from `requested_at`; override per doc via `block_threshold_days` in the catalog).
3. `substitute_behavior` is `refuse_to_render` (i.e., there is no usable interim posture).

When a session preview would otherwise include a blocked key, the preview refuses that key's inclusion, surfaces the queue entry number, and asks the operator to produce the document or accept an explicit named fallback (which is recorded in the session with a `fallback_accepted_by` and `fallback_reason`).

## Cross-references

- `tailoring/missing_docs_queue.yaml` — the runtime queue. Schema-validated against this matrix.
- `tailoring/doc_catalog.yaml` — the catalog of known document slugs; every `missing_doc_triggers` entry in a question bank must reference a slug in this catalog.
- `tailoring/DIFF_APPROVAL_PREVIEW.md` section 7 refusal condition #5 and #6 enforce catalog and `pending_doc` integrity at preview time.
- `tailoring/AUDIENCE_MAP.md` for the audience-to-bank mapping used by the expected-document tables above.

## Versioning

`missing_doc_matrix_version: "0.1.0"` — bump on addition of new expected documents or status transitions. The runtime queue validator pins to a compatible major version.
