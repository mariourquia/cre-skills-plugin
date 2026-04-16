# Pilot Property Guidance

status_tag: reference

How to pick a pilot property or pilot portfolio for the integration layer. Applies to any operator onboarding; does not describe a specific operator's choice.

## Why pilot before broad rollout

A pilot validates the connector contracts, the crosswalks, the reconciliation checks, the runbooks, and the workflow activation map against real operational conditions. Systemic problems surface at a pilot with bounded blast radius. Broad rollout is riskier because crosswalk gaps multiply across properties and a single mapping error can propagate.

## Two viable pilot shapes

### Single-property pilot

Pick one property, ideally representative of the majority of the operator's portfolio. The subsystem is validated end-to-end against that one property.

Advantages:

- Fast iteration.
- Tight feedback loop between on-site operations and integration-layer changes.
- Crosswalks limited to one property; fewer variables.

Disadvantages:

- Does not validate portfolio-level aggregation or cross-property roll-up.
- Does not exercise workflow variants across multiple form factors, segments, lifecycles, or regulatory programs.
- Operator may draw false confidence from success at a non-representative asset.

When to prefer: the operator has a highly homogeneous portfolio (same segment, same form factor, same lifecycle, same management mode).

### Portfolio-of-three pilot

Pick three properties whose attributes span the relevant axes (see diversity section below).

Advantages:

- Validates cross-property aggregation.
- Surfaces overlay composition issues (segment, regulatory, form factor, lifecycle, management mode) in combination.
- Stress-tests crosswalks with meaningful variation.
- Reveals whether reconciliation checks are tuned too tight or too loose when real variance is present.

Disadvantages:

- Slower.
- Requires site-level cooperation at three locations simultaneously.
- More complex coordination across audiences.

When to prefer: the operator has a mixed portfolio by segment, lifecycle, regulatory program, or management mode. Portfolio-of-three is the default recommendation.

## Diversity across axes

When selecting pilot properties, cover as many of the following axes as practical:

### form_factor

- `garden`, `walk_up`, `wrap`, `suburban_mid_rise`, `urban_mid_rise`, `high_rise`.
- A pilot covering at least two form factors stress-tests amenity-density and building-system modeling.

### lifecycle_stage

- `development`, `construction`, `lease_up`, `stabilized`, `renovation`, `recap_support`.
- Pilots for Wave 1 should emphasize `stabilized` and `lease_up`. Pilots for Wave 3 add `construction` and `renovation`.

### management_mode

- `self_managed`, `third_party_managed`, `owner_oversight`.
- If the operator uses a third-party manager, include one TPM-managed property in the pilot to exercise the TPM data path.

### segment

- `middle_market`, `luxury`.
- Segment overlays behave differently; at least one property per segment in use.

### regulatory_program

- `none`, `lihtc`, `hud_section_8`, `hud_202_811`, `usda_rd`, `state_program`, `mixed_income`.
- A regulatory-program property in the pilot activates the regulatory overlay stack and exercises `compliance_risk` controls.
- If the operator has no regulated properties, the pilot skips this axis and `compliance_risk` still validates the fair-housing path.

### property_age_band

- Newer (post-2010), mid-age (post-1990), older.
- Older properties often have data-quality issues with historical rent roll and deferred maintenance; worth exercising.

### market_diversity

- At least two markets if the operator has multi-market exposure. Markets affect rent comps, concessions, and payroll bands; single-market pilots miss this.

## Selection heuristic

Rank candidate pilot properties by:

1. Operational stability. Pick properties whose operations are steady, not in the middle of a major turnover, lease-up push, or construction event, unless that is the specific pilot condition being tested.
2. Site-team readiness. Pick properties where the site team has bandwidth and willingness to validate outputs. Pilots with unwilling site teams produce false negatives.
3. Data availability. Pick properties whose source systems already emit the required entities. A property where pms or gl is historically noisy is a weaker pilot choice, unless data-cleanup is explicitly part of the pilot scope.
4. Audience coverage. Pick properties whose operations exercise all 8 canonical audiences within the pilot window; avoid properties that do not exercise `construction`, `compliance_risk`, or `site_ops` if those audiences are in scope for the operator.

## Anti-patterns

- **Newest asset**: tempting because data is cleanest; misleading because historical data-quality issues are absent.
- **Most troubled asset**: tempting because it has the most operational pain; the pilot becomes a rescue mission rather than a validation.
- **Hand-picked by one audience only**: skews the pilot toward one audience's success criteria and misses others.
- **Property outside the operator's scope**: a pilot using a property the operator is about to dispose of produces results that never feed a production workflow.

## Acceptance signals

A pilot has succeeded when:

- Every in-scope connector has landed and reconciled for the pilot properties across at least one full cadence window per domain.
- Every in-scope canonical workflow has activated with non-degraded confidence for the pilot properties.
- Every in-scope audience has consumed at least one workflow output and reviewed it.
- The exception queue is bounded; aging items are closed within SLA.
- `../rollout/pilot_to_production_gate.md` criteria are met or have a defined remediation plan.

## Acceptance signals that do not count

- "The system ran without crashing for a week." Not sufficient, uptime is necessary but not sufficient.
- "Senior leadership is happy." Not sufficient, a pilot needs validation by the audiences that will use the system, not just its sponsor.
- "The numbers look reasonable." Not sufficient, compare to an independent reference (prior-period report, operator-prepared analysis) before accepting.

## Rollback from pilot

If the pilot fails, do not broaden scope. Instead:

- Identify root cause via the appropriate runbook (typically `failed_normalization_triage.md`, `property_crosswalk_issue.md`, or `schema_drift_escalation.md`).
- Fix at the contract or crosswalk layer.
- Re-pilot with the same set of properties before expanding.

If the pilot partially succeeds, expand only to adjacent properties that share the successful attributes; do not expand to properties on an untested axis until that axis has its own pilot validation.
