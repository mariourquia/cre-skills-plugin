/**
 * approval-gate.mjs
 *
 * Human-in-the-loop approval gate evaluator. See
 * docs/orchestrator-v0-design.md section 2 and
 * src/orchestrators/schemas/approval_gate.schema.json.
 *
 * A phase declares zero or more `approval_gates` (injected by the
 * variant loader when the variant adds them). Before the executor
 * dispatches agents for that phase, it calls
 * `evaluatePhaseGates(phase, dealState)` to determine whether any
 * gate is pending/denied/expired. If so, the phase verdict becomes
 * AWAITING_APPROVAL and execution halts until an operator flips
 * the gate via `approve-gate.mjs`.
 *
 * Gates persist in `dealState.approval_gate_log`. The first time the
 * executor encounters a gate, it appends a `status: pending` entry
 * and emits the `gate_opened` audit event. Subsequent encounters
 * find the existing entry and respect its status.
 */

const CLEARED_STATUSES = new Set(['approved', 'approved_with_conditions']);
const BLOCKED_STATUSES = new Set(['pending', 'denied', 'expired']);

function findExistingGate(dealState, gateId) {
  return (dealState.approval_gate_log || []).find(
    (g) => g.gate_id === gateId,
  );
}

/**
 * Open a pending gate in the deal state if it has not been seen yet.
 * Returns the (new or existing) gate record. Does not persist state
 * to disk — caller is responsible for writeState + audit event.
 */
export function openGateIfAbsent(dealState, gateSpec) {
  const existing = findExistingGate(dealState, gateSpec.gate_id);
  if (existing) return { record: existing, created: false };
  const now = new Date().toISOString();
  const record = {
    gate_id: gateSpec.gate_id,
    required_approvers: gateSpec.required_approvers || [],
    approval_matrix_row: gateSpec.approval_matrix_row,
    evidence_required: gateSpec.evidence_required || [],
    status: 'pending',
    created_at: now,
    updated_at: now,
  };
  dealState.approval_gate_log = dealState.approval_gate_log || [];
  dealState.approval_gate_log.push(record);
  return { record, created: true };
}

/**
 * Inspect all gates declared on `phase` against `dealState`.
 *
 * Returns: { blocked: boolean, blockingGates: [...], newlyOpened: [...] }
 *  - blocked: true if any gate has status in BLOCKED_STATUSES
 *  - blockingGates: gate records (with current status) blocking the phase
 *  - newlyOpened: gates that were just appended to the state (caller must persist)
 */
export function evaluatePhaseGates(phase, dealState) {
  const gates = phase.approval_gates || [];
  if (gates.length === 0) {
    return { blocked: false, blockingGates: [], newlyOpened: [] };
  }

  const newlyOpened = [];
  const blockingGates = [];

  for (const spec of gates) {
    const { record, created } = openGateIfAbsent(dealState, spec);
    if (created) newlyOpened.push(record);
    if (BLOCKED_STATUSES.has(record.status)) {
      blockingGates.push(record);
    } else if (!CLEARED_STATUSES.has(record.status)) {
      // Unknown / future status — treat as blocking, loudly.
      blockingGates.push({ ...record, _note: `unknown status "${record.status}"` });
    }
  }

  return {
    blocked: blockingGates.length > 0,
    blockingGates,
    newlyOpened,
  };
}

/**
 * Apply a decision to a gate record in dealState. Caller persists
 * with writeState + audit event.
 *
 * decision.status must be one of: approved, approved_with_conditions,
 * denied, expired.
 */
export function decideGate(dealState, gateId, decision) {
  const record = findExistingGate(dealState, gateId);
  if (!record) {
    throw new Error(`No gate with gate_id "${gateId}" in deal state`);
  }
  const allowed = new Set([
    'approved',
    'approved_with_conditions',
    'denied',
    'expired',
  ]);
  if (!allowed.has(decision.status)) {
    throw new Error(
      `decideGate: status "${decision.status}" not in ${[...allowed].join(', ')}`,
    );
  }
  const now = new Date().toISOString();
  record.status = decision.status;
  record.updated_at = now;
  if (decision.status === 'approved' || decision.status === 'approved_with_conditions') {
    record.approved_at = now;
    record.approved_by = decision.approved_by || 'unknown';
    if (decision.conditions_text) record.conditions_text = decision.conditions_text;
  }
  if (decision.status === 'denied' && decision.denial_reason) {
    record.denial_reason = decision.denial_reason;
  }
  if (decision.evidence_hashes) record.evidence_hashes = decision.evidence_hashes;
  return record;
}

export const _internal = { CLEARED_STATUSES, BLOCKED_STATUSES };
