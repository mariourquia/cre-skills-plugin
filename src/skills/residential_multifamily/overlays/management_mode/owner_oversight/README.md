# Owner-Oversight Mode Overlay

Loads alongside `third_party_managed` when the asker is owner-side. The overlay
specifies the owner's oversight surfaces over the TPM, anchored to the TPM
Oversight metric family in `_core/metrics.md`.

## What this overlay shifts

- Reporting emphasis: TPM scorecard surfaces (report timeliness, KPI completeness,
  variance-narrative quality, budget adherence, staffing vacancy, collections
  performance, turn performance, service-level adherence, approval response time,
  audit issues).
- Approval posture: owner AM, portfolio manager, or COO are the signatories on
  owner-side approval lanes. The TPM cannot self-approve into owner-side lanes.
- Escalation: owner-oversight surfaces route severities beyond TPM authority to
  the owner's internal chain.

<a id="scorecard_cadence"></a>

## TPM scorecard cadence

- Monthly: review the scorecard inputs delivered by the TPM. Flag any metric
  outside the target band. Attach variance-narrative quality score.
- Quarterly: deep-dive review covering scorecard trend, corrective-action status,
  staffing, and any audit-issue movement.
- Annual: scorecard roll-up for contract-renewal discussion and fee benchmarking
  (fee benchmarking is an asset-management workstream, not a skill surface here).

<a id="audit_tracking"></a>

## Audit-issue tracking

- Owner-initiated audits and TPM-internal audits both feed the same audit-issue
  log.
- Each issue carries a severity, remediation owner, due date, and status.
- Open issues past due are a scorecard penalty; severity-weighted breaches escalate
  to executive review.

## When this overlay is loaded

- Owner-side user asks for an operating review, scorecard, approval decision, or
  variance explanation in a TPM-managed property.
- Portfolio-level reporting that rolls up TPM-managed assets.
- Any owner-side final submission (lender or LP) where the TPM is an input
  source; the owner-oversight overlay asserts data-integrity posture before the
  final submission gate.

## Interaction with self_managed

This overlay does not load in self-managed properties; the self-managed overlay
already implies owner oversight because the owner is the operator.
