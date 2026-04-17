/**
 * audit-log.mjs
 *
 * Append-only JSONL audit log for orchestrator events. Lives next to the
 * deal state file at `<dealDir>/audit_log.jsonl`. See
 * docs/orchestrator-v0-design.md section 5.
 *
 * Event shape intentionally mirrors the residential_multifamily
 * `approval_audit_log.jsonl` superset so downstream tooling that reads
 * both logs can use a single parser. Orchestrator-specific events
 * (phase_started, phase_completed) carry the common header plus their
 * own fields.
 *
 * Append-only invariant: this module only ever opens files in append
 * mode. It never reads-and-rewrites. Tests assert the byte prefix is
 * immutable across multiple appends.
 */

import { appendFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { dealDir } from './deal-state.mjs';

const REQUIRED_EVENT_KEYS = ['event', 'actor', 'deal_id'];

const ORCHESTRATOR_EVENT_VOCAB = new Set([
  'pipeline_started',
  'pipeline_completed',
  'pipeline_halted',
  'phase_started',
  'phase_completed',
  'phase_blocked',
  'gate_opened',
  'gate_approved',
  'gate_approved_with_conditions',
  'gate_denied',
  'gate_expired',
  'calculator_invoked',
  'calculator_failed',
  'variant_selected',
  'resume_started',
]);

export function auditLogPath(dealId, baseDir) {
  return join(dealDir(dealId, baseDir), 'audit_log.jsonl');
}

export function appendEvent(event, baseDir) {
  for (const k of REQUIRED_EVENT_KEYS) {
    if (!(k in event)) {
      throw new Error(`appendEvent: event missing required key "${k}"`);
    }
  }
  if (!ORCHESTRATOR_EVENT_VOCAB.has(event.event)) {
    throw new Error(
      `appendEvent: unknown event type "${event.event}". ` +
      `Extend ORCHESTRATOR_EVENT_VOCAB in audit-log.mjs when adding a new event.`,
    );
  }
  const enriched = {
    timestamp: event.timestamp || new Date().toISOString(),
    ...event,
  };
  const dir = dealDir(event.deal_id, baseDir);
  mkdirSync(dir, { recursive: true });
  const path = auditLogPath(event.deal_id, baseDir);
  appendFileSync(path, JSON.stringify(enriched) + '\n', 'utf-8');
  return { path, entry: enriched };
}

export function readEvents(dealId, baseDir) {
  const path = auditLogPath(dealId, baseDir);
  if (!existsSync(path)) return [];
  const raw = readFileSync(path, 'utf-8');
  if (!raw) return [];
  return raw
    .split('\n')
    .filter((line) => line.trim().length > 0)
    .map((line) => JSON.parse(line));
}

export const _internal = {
  REQUIRED_EVENT_KEYS,
  ORCHESTRATOR_EVENT_VOCAB,
};
