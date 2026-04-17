#!/usr/bin/env node

/**
 * approve-gate.mjs
 *
 * CLI to clear an approval gate on a persisted deal. Kept separate
 * from executor.mjs so the executor never approves its own gates —
 * approvals always come from a separate, explicit human-driven
 * invocation. See docs/orchestrator-v0-design.md section 2.
 *
 * Usage:
 *   node approve-gate.mjs --deal-id <id> --gate-id <gid> \
 *     --status approved|approved_with_conditions|denied|expired \
 *     --approved-by <name> [--conditions "text"] [--denial-reason "text"]
 */

import { readState, writeState } from './deal-state.mjs';
import { decideGate } from './approval-gate.mjs';
import { appendEvent as appendAuditEvent } from './audit-log.mjs';

function parseArgs(argv) {
  const args = {
    dealId: null,
    gateId: null,
    status: null,
    approvedBy: null,
    conditions: null,
    denialReason: null,
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--deal-id' && argv[i + 1]) { args.dealId = argv[++i]; continue; }
    if (a === '--gate-id' && argv[i + 1]) { args.gateId = argv[++i]; continue; }
    if (a === '--status' && argv[i + 1]) { args.status = argv[++i]; continue; }
    if (a === '--approved-by' && argv[i + 1]) { args.approvedBy = argv[++i]; continue; }
    if (a === '--conditions' && argv[i + 1]) { args.conditions = argv[++i]; continue; }
    if (a === '--denial-reason' && argv[i + 1]) { args.denialReason = argv[++i]; continue; }
  }
  return args;
}

function usage() {
  console.error(
    'Usage: node approve-gate.mjs --deal-id <id> --gate-id <gid> ' +
    '--status <approved|approved_with_conditions|denied|expired> ' +
    '[--approved-by <name>] [--conditions "<text>"] [--denial-reason "<text>"]',
  );
}

function statusToAuditEvent(status) {
  switch (status) {
    case 'approved': return 'gate_approved';
    case 'approved_with_conditions': return 'gate_approved_with_conditions';
    case 'denied': return 'gate_denied';
    case 'expired': return 'gate_expired';
    default: throw new Error(`Unknown status "${status}"`);
  }
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.dealId || !args.gateId || !args.status) {
    usage();
    process.exit(1);
  }

  const state = readState(args.dealId);
  if (!state) {
    console.error(`No deal state for deal_id "${args.dealId}"`);
    process.exit(2);
  }

  let record;
  try {
    record = decideGate(state, args.gateId, {
      status: args.status,
      approved_by: args.approvedBy || undefined,
      conditions_text: args.conditions || undefined,
      denial_reason: args.denialReason || undefined,
    });
  } catch (err) {
    console.error(`[ERROR] ${err.message}`);
    process.exit(3);
  }

  writeState(state);
  appendAuditEvent({
    event: statusToAuditEvent(args.status),
    actor: args.approvedBy || 'unknown',
    deal_id: args.dealId,
    run_id: state.run_id,
    gate_id: args.gateId,
    approval_matrix_row: record.approval_matrix_row,
    status: args.status,
  });

  console.log(
    `Gate "${args.gateId}" on deal "${args.dealId}" is now ${args.status}` +
    (args.approvedBy ? ` (by ${args.approvedBy})` : '') + '.',
  );
}

main().catch((err) => {
  console.error(`[FATAL] ${err.message}`);
  process.exit(4);
});
