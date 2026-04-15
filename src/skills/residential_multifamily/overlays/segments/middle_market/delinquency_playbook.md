# Middle-Market Delinquency Playbook

Stage-by-stage delinquency handling for middle-market properties. The posture is:
resident-respectful, policy-driven, tightly documented, and never improvisational.
Every step has an owner, an expected action, and a gate for the next escalation.

The playbook ties to `_core/approval_matrix.md` rows 1 (legal notice) and 2
(eviction). The system drafts and routes; humans approve gated actions.

## Stage 1: day 1 through day 5 after due date

Owner: property manager and assistant property manager.

Actions:

- Automated plain-language reminder via the resident's preferred channel, tuned to
  the tone profile in `resident_comm_tone.md`. No legal language at this stage.
- Ledger validation: verify charges, credits, and any concession accruals before any
  additional outreach.
- Resident outreach (phone or in-person preferred where appropriate) after the
  reminder has gone unacknowledged within the documented window.
- Payment arrangement is not offered unprompted at this stage; it is available if
  the resident asks and qualifies under the documented payment-plan policy.

Escalation gate: if the balance is still open at the stage boundary, advance to
stage 2.

## Stage 2: day 6 through day 15 after due date

Owner: property manager; regional manager is copied on escalations.

Actions:

- Direct call from the PM. The call is documented in the resident ledger.
- Documented payment-plan option, sized per the policy in the reference layer. The
  system never creates a non-standard payment plan; any deviation routes to approval
  under `_core/approval_matrix.md#row_13`.
- Approval package assembled for a pay-or-quit notice if stage 3 is likely. The
  package includes the ledger, prior communications, any payment-plan status, and
  the jurisdictional notice form, which is human-validated and not drafted
  autonomously.

Escalation gate: if the balance remains unresolved and no active payment plan is in
force at the stage boundary, advance to stage 3.

## Stage 3: day 16 and beyond

Owner: property manager, regional manager, legal counsel.

Actions:

- Pay-or-quit notice served only after approval. The approval request cites
  `_core/approval_matrix.md#row_1_legal_notice` and references the jurisdiction's
  notice requirements. Jurisdiction review is a separate human step.
- If the notice period expires without cure, an eviction review opens. Eviction
  filings are gated under `_core/approval_matrix.md#row_2_eviction`, require
  counsel sign-off, and are never autonomous.
- Parallel outreach continues per tone and guardrails; the resident may cure at any
  time through stage 3.

## Reporting emphasis

Delinquency rolling rates, collections rate, and bad-debt rate are the primary
surfaces (see `reporting_emphasis.md`). A property outside the middle-market
delinquency band triggers a case-by-case review and, if sustained, a watchlist
entry.
