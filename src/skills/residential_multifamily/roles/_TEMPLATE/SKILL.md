---
name: <Human-readable role name>
slug: <role_slug>
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: role
targets:
  - claude_code
stale_data: |
  <What might drift. E.g., benchmark ranges, staffing ratios, policy references.>
applies_to:
  segment: [middle_market]              # default; add affordable/luxury when overlays diverge
  form_factor: []                       # empty = all supported
  lifecycle: [stabilized]               # default; packs that apply across stages list all
  management_mode: [self_managed, third_party_managed]
  role: [<role_slug>]
  output_types: [memo, kpi_review, checklist, email_draft, operating_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/...
  writes: []
metrics_used:
  - <canonical_metric_slugs_from__core_metrics>
escalation_paths:
  - kind: <kind>
    to: <next-role or approval_request>
approvals_required:
  - <action_name>
description: |
  One paragraph: what the role does and when it triggers.
---

# <Role Name>

## Role mission

One paragraph.

## Core responsibilities

### Daily
- ...
### Weekly
- ...
### Monthly
- ...
### Quarterly
- ...

## Primary KPIs

Cite by canonical slug. Target bands pulled from `reference/derived/role_kpi_targets.csv`.

| Metric | Default target band | Source |
|---|---|---|
| `physical_occupancy` | (overlay-provided) | `reference/derived/role_kpi_targets.csv` |

## Decision rights

Explicit list of what the role decides autonomously, what routes up, what requires approval.

## Inputs consumed

Document types, systems, references.

## Outputs produced

Templates, memos, reviews, emails.

## Cross-functional handoffs

Who the role hands off to, in what artifacts.

## Escalation paths

For each escalation kind (legal, safety, fair_housing, financial_threshold, policy_exception), the next step.

## Approval thresholds

Point to `_core/approval_matrix.md` and the org overlay.

## Typical failure modes

5–10 common ways this role gets wrong.

## Skill dependencies

Workflow packs this role invokes.

## Templates used

Paths.

## Reference files used

Paths.

## Example invocations

Three short prompts that should trigger this pack.

## Example outputs

One or two worked examples (input → output).
