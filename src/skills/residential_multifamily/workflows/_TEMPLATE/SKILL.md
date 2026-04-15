---
name: <Human-readable workflow name>
slug: <workflow_slug>
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  <What might drift.>
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized]
  management_mode: [self_managed, third_party_managed]
  role: []                # list roles that typically invoke this workflow
  output_types: [<pick from taxonomy Axis 9>]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/...
  writes: []
metrics_used:
  - <canonical_slugs>
escalation_paths: []
approvals_required: []
description: |
  One paragraph: what the workflow does and when it triggers.
---

# <Workflow Name>

## Workflow purpose

One paragraph.

## Trigger conditions

- Explicit phrases.
- Implicit signals.
- Recurring contexts.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|

## Outputs

| Output | Type | Shape |
|---|---|---|

## Required context

What axes / references the router must supply before the workflow can run.

## Process

1. Step one.
2. Step two.

Include decision points and branches.

## Metrics used

Cite by slug.

## Reference files used

Paths.

## Escalation points

Where the workflow hands off mid-process.

## Required approvals

Threshold-triggered and policy-triggered.

## Failure modes

Known ways the workflow gets wrong.

## Edge cases

Unusual inputs and how the workflow handles them.

## Example invocations

## Example outputs
