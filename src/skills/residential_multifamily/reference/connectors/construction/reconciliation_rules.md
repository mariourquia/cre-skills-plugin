# Construction Reconciliation Rules

Narrative describing how reconciliation in the construction domain works.

## Reconciliation scope

The construction connector lands development budgets, estimates, bid packages, commitments, change orders, draw requests, schedule milestones, and punch items. It reconciles with:

- The general ledger (for capex postings versus draws).
- The accounts-payable system (for commitment and vendor alignment).
- The PMS turn records (for unit-level rehab when turn costs feed capex projects).

## Totals that must agree

### Commitment ceiling versus draws plus change orders

For each commitment_id, `sum(draws where approval_status IN (approved, funded)) <= contract_total_cents + sum(co.cost_delta_cents where status = approved)`. Tolerance is zero. Enforced by `construction_commitment_change_order_draw`.

### Capex spend versus draws

For each project_id, `sum(gl.capex_actual.amount_cents)` reconciles with `sum(construction.draw_request.amount_requested_cents where approval_status IN (approved, funded))` at project completion. Intra-period tolerance depends on retention and lien-waiver timing declared in `construction/manifest.yaml`.

### Budget versus commitment coverage

For each project, `sum(dev_budget.amount_cents where scenario = current_of_record)` is greater than or equal to `sum(commitment.contract_total_cents)` plus `sum(change_order.cost_delta_cents where status = approved)`. Breach indicates overcommitment; holds landing.

### AP commitment versus construction commitment

For each vendor-project commitment pair, the AP-side and construction-side totals reconcile via the commitment_bridge. Tolerance is zero.

## Tolerances

| Reconciliation | Absolute tolerance | Relative tolerance |
|---|---|---|
| Commitment ceiling vs draws + COs | 0 | 0 |
| Capex spend vs draws | 0 at project close | retention & lien-waiver dependent intra-period |
| Budget vs commitment coverage | 0 | 0 |
| AP vs construction commitment | 0 | 0 |

All non-zero tolerance values live in the connector manifest.

## Escalation triggers

- Overdraw on a commitment escalates to the construction-project-command-center and to the approval matrix in `_core/approval_matrix.md`.
- Contingency burning ahead of percent-complete escalates to the asset_mgmt and executive audiences (schedule_risk_review workflow triggers).
- Missing lien waiver on a draw escalates to the compliance_risk audience.
- Rehab/capex miscoding escalates to the asset_mgmt audience because it distorts both NOI and renovation-yield.

## Cross-domain reconciliation dependencies

Construction reconciliation is a precondition for:

- Draw package review (workflow).
- Cost-to-complete review (workflow).
- Capex prioritizer skill.
- Dev proforma engine (for projects under construction).

Blockers hold these workflows and skills for the affected project.
