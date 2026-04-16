# Success Metrics

status_tag: reference

Qualitative rollout success metrics. Thresholds live in `overlays/org/<org_id>/`; this document names the categories and the qualitative bands.

## Principle

Rollout success is measured by whether the integration layer does its job quietly. A successful rollout is one where data lands on time, reconciles cleanly, workflows activate for the right audiences, approval gates hold, and the operator's decision-making is better informed than before. Noise, exceptions, overrides, and rework are all signals of incomplete success.

## Categories

### Data freshness within cadence

For every source and every domain, the share of scheduled landings arriving within cadence plus tolerance. Bands:

- **On target**: landings arrive within cadence almost always.
- **At risk**: landings slip regularly; the slips are bounded but rising.
- **Breached**: landings slip frequently, or multiple domains are slipping at once.

Reference: `../monitoring/slo_definitions.md` freshness SLO.

### Exception queue boundedness

Is the exception queue a working surface or a backlog? Bands:

- **On target**: volume stable, dwell-time under SLA, closeouts match arrivals.
- **At risk**: volume rising, dwell expanding, or aging items accumulating.
- **Breached**: the queue is a backlog; consumer audiences lose visibility.

Reference: `../runbooks/exception_queue_review.md`.

### Workflow activation rate

The share of attempted workflow activations that succeed with non-degraded confidence across in-scope workflows. Bands:

- **On target**: activations succeed non-degraded almost always.
- **At risk**: degraded activations rising.
- **Breached**: degraded-mode is the norm for one or more audiences' workflows.

Reference: `../monitoring/slo_definitions.md`.

### User trust signals via tailoring feedback loop

Tailoring sessions collect feedback on the subsystem's outputs. Signals pulled from those sessions:

- **On target**: audiences express trust in outputs, use the subsystem as the primary source for its scope, and surface refinement ideas (rather than correction requests).
- **At risk**: audiences pair subsystem outputs with manual cross-checks as a rule; trust is partial.
- **Breached**: audiences bypass subsystem outputs and rely on alternative sources; trust has not been established.

Reference: `tailoring/SKILL.md` and the organization's feedback cadence.

### Approval-gate integrity

The share of gated actions executed with a matching approved `ApprovalRequest`. Bands:

- **On target**: every gated action has a matching approval; log tail consistent.
- **At risk**: unusual patterns in the log (late approvals, auto-approvals within tolerance but frequent).
- **Breached**: even a single executed action without a matching approval. Binary floor; no band gradation.

Reference: `_core/approval_matrix.md` and `../runbooks/financial_control_gate_breach.md`.

### Fair-housing and legal-sensitive posture

The operator's containment and handling of fair-housing-sensitive and legal-sensitive events. Bands:

- **On target**: no incidents, or incidents contained cleanly with legal sign-off, no broad-channel leakage.
- **At risk**: a near-miss required containment and revealed a gap in routing.
- **Breached**: any incident with broad-channel leakage, any delay in containment, or any action taken without `legal_counsel` sign-off.

Reference: `../runbooks/fair_housing_sensitive_flag.md`.

### Rollback frequency

The number of rollbacks initiated during the rollout. Bands:

- **On target**: no rollbacks after the first wave.
- **At risk**: one rollback per wave, contained.
- **Breached**: repeated rollbacks, or a single Wave-4 rollback.

### Cross-wave regression

Whether activation of a later wave caused regression in an earlier wave's scope. Bands:

- **On target**: no regressions.
- **At risk**: minor regressions resolved within a cadence cycle.
- **Breached**: persistent regression in an earlier wave's scope that the later wave introduced.

### Reference rollback frequency

The number of benchmark rollbacks per refresh cycle. Bands:

- **On target**: rollbacks occur only on genuine source-quality issues, not on methodology mistakes.
- **At risk**: rollback per quarter or more; review the refresh process.
- **Breached**: rollbacks on consecutive cycles; the refresh process itself needs restructuring.

Reference: `../runbooks/reference_rollback.md`, `../runbooks/benchmark_refresh.md`.

### Regulatory-program posture

For operators with regulatory-program exposure:

- **On target**: every filing deadline met, every regulatory exception contained cleanly, `compliance_risk` sign-off current.
- **At risk**: a filing was delayed but not missed; a regulatory exception was close to SLO breach.
- **Breached**: a filing was missed or a regulatory exception reached public or regulator surfaces.

## How operators use this document

1. Operators pick the band thresholds that map to their overlay. Numerics live in `overlays/org/<org_id>/rollout_success_thresholds.yaml` (operator-specific; not in this repo).
2. Every monthly review references these categories.
3. The quarterly review aggregates the bands into a composite readout for `executive` and `finance_reporting`.
4. Band transitions are logged per `_core/change_log_conventions.md`.

## What this document deliberately omits

- Percent targets, count targets, dollar targets, all in overlays.
- Ranking of sources by importance, that belongs in `source_registry.yaml` notes and overlay configuration.
- Vendor-specific success criteria, the subsystem is vendor-neutral.

## Non-metric signals

Not all success is numeric. Qualitative signals worth tracking:

- Site teams report that data is consistently correct when they open it.
- `finance_reporting` reduces time spent on manual reconciliation between systems.
- `asset_mgmt` starts conversations with data rather than about data.
- `executive` monthly reviews reference subsystem outputs directly rather than summaries prepared separately.
- `compliance_risk` reports fewer ad-hoc data pulls for fair-housing monitoring.

These signals are surfaced during the tailoring feedback loop and fed into the success-metrics review.
