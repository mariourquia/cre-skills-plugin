# SLO Definitions, Integration Layer

status_tag: reference

Service-level objectives for the integration layer. All SLOs are declared in qualitative bands. Exact numerics live in `overlays/org/<org_id>/slo_thresholds.yaml` (operator-specific; not in this directory). Operators may tighten bands but may not loosen them below the canonical floors below.

## Guiding principles

1. SLOs describe steady-state operational expectations. They do not bind incident-response timing.
2. Every SLO is observable via events declared in `observability_events.yaml`.
3. Breach of an SLO opens an exception of category `dq_warning` or `dq_blocker` (severity per category) and routes through `exception_routing.yaml`.
4. SLO reviews occur at the cadence in `../rollout/post_launch_monitoring_cadence.md`.
5. Operators override thresholds via the overlay system, not by editing this file.

## SLO categories

### Freshness SLO per domain

For each domain, the fraction of scheduled landings that arrive within cadence plus tolerance, classified into bands:

| Domain | Expected cadence band | Floor (overlay may tighten) |
|---|---|---|
| pms | near-real-time to daily | steady freshness within cadence for the overwhelming majority of landings |
| gl | daily to monthly | steady freshness within cadence for the overwhelming majority of landings |
| crm | near-real-time to daily | steady freshness within cadence for the overwhelming majority of landings |
| ap | daily to monthly | steady freshness within cadence for most landings |
| market_data | weekly to monthly | steady freshness within cadence for most landings |
| construction | daily to monthly | steady freshness within cadence for most landings |
| hr_payroll | weekly to monthly | steady freshness within cadence for most landings |
| manual_uploads | varies per source (typically monthly or quarterly) | best effort, chronic shortfall triggers `cutover_manual_to_system.md` candidacy |

Bands: "overwhelming majority" means the floor for high-frequency critical feeds. "Most" means the floor for less frequent feeds where a single miss has lower operational impact. Exact percentages are operator-set.

### DQ blocker resolution time SLO

Every `dq_blocker` exception carries a dwell-time floor from `exception_routing.yaml`. The SLO is the fraction of blockers resolved within the dwell floor across a rolling window. Bands:

- **On target**: the overwhelming majority of blockers resolve within dwell.
- **At risk**: a sustained share miss dwell for more than one review cycle.
- **Breached**: multiple consecutive review cycles miss the floor.

At-risk triggers a root-cause review at the next weekly readout. Breach escalates to `executive` at the next monthly review.

### Reconciliation completion SLO

The fraction of scheduled reconciliation runs that complete (pass or fail, but not stall) within the cadence window. Bands:

- **On target**: the overwhelming majority of runs complete.
- **At risk**: a sustained share stall or time out.
- **Breached**: recurring stalls that block downstream workflow activation.

### Workflow activation success rate SLO

The fraction of attempted workflow activations that succeed (produce a valid, non-degraded output) within their expected window, across the 27 canonical workflows. Bands:

- **On target**: most activations succeed non-degraded.
- **At risk**: a sustained degraded-mode share across multiple workflows.
- **Breached**: degraded-mode is the norm rather than the exception for one or more audiences' workflows.

### Exception queue health SLO

Composite of queue volume, dwell-time, and closeout rate:

- **On target**: queue volume stable, no items aged beyond SLA, closeouts match arrivals.
- **At risk**: volume rising, dwell expanding, or aging items growing.
- **Breached**: queue is a backlog rather than a working surface.

### Approval gate integrity SLO

The fraction of gated actions that carry a matching approved `ApprovalRequest` at execution time. Floor is absolute: every executed gated action must carry an approval. Any miss is a `policy_violation` incident, not a rate-band observation.

## How operators override

Operators tighten bands in `overlays/org/<org_id>/slo_thresholds.yaml` with:

- exact percent thresholds per band,
- rolling window definitions (for example, trailing week, trailing month, trailing quarter),
- review-cadence alignment (weekly, monthly, quarterly).

Operators may not loosen bands below the qualitative floors listed above. Any attempt to do so fails review and is flagged as an overlay policy violation.

## Relationship to workflows

SLOs feed several canonical workflows:

- `monthly_property_operating_review` and `monthly_asset_management_review` include an integration-layer health section that cites SLO status bands.
- `executive_operating_summary_generation` surfaces composite SLO health to the executive audience.
- `quarterly_portfolio_review` summarizes SLO trends over the quarter.
- `third_party_manager_scorecard_review` reflects the manager's contribution to freshness and reconciliation SLO health for the properties they run.

## Relationship to runbooks

Runbook execution may reduce an SLO in the short term; that is expected during remediation. SLO reviews look at the smoothed rolling window, not the transient.

## No numbers in prose

This file does not state percent targets. Operators carry the actual thresholds in their overlays; the subsystem merely requires that each operator declares one.
