# Pilot-to-Production Gate

status_tag: reference

Criteria for moving any domain from pilot to production. Applied per source, per domain, per wave. A domain can be in pilot for one source and in production for another; the gate is evaluated per source.

## The five gate criteria

All five must be satisfied before a source transitions from pilot (`status: stubbed` with limited consumer workflows activated) to production (`status: active` with full consumer workflow activation).

### Criterion 1, Sign-off

Sign-offs from:

- `data_owner`, confirms the source's data quality is production-acceptable.
- `business_owner`, confirms the use case is production-justified.
- `technical_owner`, confirms the adapter is production-ready.
- Primary consumer audience, confirms they are prepared to rely on the source.
- `finance_reporting`, always, for any source feeding finance-adjacent outputs.
- `compliance_risk`, for any source with `pii_classification: high` or higher, or `legal_sensitivity: high` or higher, or any regulatory-program exposure.
- `legal_counsel`, for any source with legal-document content or contract-binding implications.
- `executive`, for any source feeding executive, lender, investor, or board-facing reports.

Each sign-off is recorded in the source's `source_registry.yaml` notes and in the subsystem change log per `_core/change_log_conventions.md`.

### Criterion 2, DQ stability period

A sustained period during which reconciliation checks are green across a minimum number of landings. Operator sets the exact window in their overlay; floors:

- High-frequency sources (near-real-time to daily): at least one full cadence cycle plus a stability buffer with zero blocker failures.
- Weekly sources: at least two full cycles with zero blocker failures.
- Monthly sources: at least two full cycles with zero blocker failures.
- Quarterly sources: at least one full cycle with zero blocker failures, supported by a shorter proxy evaluation.

Warnings are permitted during the stability period if they are triaged and documented. A persistent warning without resolution is a de facto blocker and fails the gate.

### Criterion 3, Reconciliation stability

Reconciliation behavior must be stable, not just green:

- Record counts, identity resolution, date coverage, lease-status, unit-count, and budget-actual checks all remain within their declared tolerances across the stability period.
- No check has flipped between pass and fail within the period.
- Crosswalks referenced by the source are not pending-change at the moment of transition.
- Source-vs-source reconciliation (where two sources carry overlapping objects) is aligned.

### Criterion 4, Exception dwell time

Exception-queue behavior for the source is production-bounded:

- No open aging item for this source exceeds its dwell-time SLA per `../monitoring/exception_routing.yaml`.
- Average dwell time for `dq_warning` and lower-severity items is within the overlay's declared band.
- Volume per cadence cycle is within the overlay's steady-state band.

### Criterion 5, Workflow activation readiness

Every canonical workflow that will depend on the source once in production can activate with non-degraded confidence for in-scope properties:

- The workflow activation map (`../_core/workflow_activation_map.yaml`, planned) returns "ready" for those workflows.
- At least one pilot property has completed each dependent workflow and produced an output that was reviewed by the consumer audience.
- Minimum viable data requirements (`minimum_viable_data.md`) are met without needing manual-only fallbacks.

## Gate evaluation process

1. Pilot lead compiles the criteria-evidence packet.
2. The packet is reviewed at the weekly operations review (`post_launch_monitoring_cadence.md`).
3. If the packet is complete and all criteria are satisfied, the gate is scheduled for approval.
4. Approvers listed in Criterion 1 sign off in the subsystem's approval workflow.
5. On full sign-off, the source transitions from `status: stubbed` to `status: active`. Observability emits `registry_status_transition`.
6. The transition is announced to affected audiences through `../monitoring/alert_channel_design.md`.
7. The subsystem change log records the transition per `_core/change_log_conventions.md`.

## Failing the gate

A gate failure is not a stigma; it is information. Common failure modes and responses:

- **Sign-off missing**: schedule the missing audience for review; do not rush the sign-off.
- **DQ stability period incomplete**: extend the pilot until the period is satisfied.
- **Persistent warning**: resolve the warning or reclassify it as a production-acceptable residual; persistent warnings do not age into acceptance silently.
- **Aging exception**: resolve the exception before transition.
- **Workflow activation in degraded mode**: verify the degradation is not a function of the pilot source itself; if it is, the gate fails.

## Re-running the gate

A pilot that fails the gate can be re-run once the underlying issue is fixed. The gate is not a one-shot; it is a repeatable evaluation.

A source that has been in production and degrades to `status: degraded` can be re-evaluated for a gate once stabilized. The gate criteria apply the same way.

## What the gate does not do

- The gate does not cap the number of pilots. Multiple sources can be in pilot simultaneously.
- The gate does not substitute for wave entry or exit criteria in `rollout_waves.md`. Both apply.
- The gate does not govern manual overrides or approval overrides; those follow their own runbooks.
- The gate does not govern benchmark refreshes; those follow `benchmark_refresh.md`.

## Special cases

### Regulatory-program sources

For sources whose `object_coverage` supports a regulatory program, Criterion 1 elevates:

- `compliance_risk` sign-off is always required.
- `legal_counsel` sign-off is required if the source's data could be cited in a regulator filing.
- An overlay-specific review is required; the regulatory overlay owner attends.

### Fair-housing-adjacent sources

For sources whose `object_coverage` includes fields that could feed fair-housing-sensitive decisions (screening, demographic indicators, protected-class proxies), the gate adds:

- A boundary review: confirm the connector's `schema.yaml` and `mapping.yaml` exclude sensitive fields where they should be excluded.
- A leakage test: a synthetic record with a sensitive field verifies the boundary holds.
- `compliance_risk` and `legal_counsel` sign-off.

### Third-party-manager-driven sources

For sources landing through `operator_owner_portal_sftp` or similar TPM paths, the gate adds:

- A TPM-relationship sign-off confirming the manager accepts the data-sharing arrangement.
- A `third_party_manager_scorecard_review` baseline run against the pilot data.

## Post-gate

Once a source is `status: active`, it is subject to steady-state SLOs and monitoring. A production source that degrades in behavior may be returned to `degraded` status without re-passing the pilot-to-production gate (the gate is forward-only). Re-entry to `active` from `degraded` requires the gate again.
