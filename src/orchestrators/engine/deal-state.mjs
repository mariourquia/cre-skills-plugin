/**
 * deal-state.mjs
 *
 * Persistent deal-scoped orchestrator state. See
 * docs/orchestrator-v0-design.md section 1 and
 * src/orchestrators/schemas/deal_state.schema.json.
 *
 * State lives at `<homeBase>/.claude/cre-skills/deals/<deal_id>/state.json`.
 * `homeBase` defaults to `os.homedir()` but honors the `CRE_SKILLS_HOME`
 * env var so integration tests can point the runtime at a tmp dir without
 * monkey-patching the home directory.
 *
 * This module is pure in the sense that every side-effecting function
 * takes a `baseDir` argument (directly or via env), so it can be tested
 * without touching the operator's real home directory.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, renameSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { randomUUID } from 'node:crypto';

// ---------------------------------------------------------------------------
// Constants pulled from the schema. Kept in sync by
// tests/test_orchestrator_deal_state.py (deal_state.schema.json is the
// source of truth; these arrays mirror it for fast-path validation).
// ---------------------------------------------------------------------------

const SUPPORTED_PIPELINES = [
  'acquisition',
  'capital-stack',
  'development',
  'disposition',
  'fund-management',
  'hold-period',
  'investment-strategy',
  'lp-intelligence',
  'portfolio-management',
  'research-intelligence',
];

const VERDICT_VOCAB = [
  'PROCEED',
  'CONDITIONAL',
  'KILL',
  'AWAITING_APPROVAL',
  'REFUSED',
];

const RESUMABLE_VERDICTS = new Set(['PROCEED', 'CONDITIONAL']);

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

export function resolveBaseDir() {
  // Tests set CRE_SKILLS_HOME to a tmp dir; production uses the user's home.
  const override = process.env.CRE_SKILLS_HOME;
  return override && override.length > 0 ? override : homedir();
}

export function dealDir(dealId, baseDir) {
  const base = baseDir || resolveBaseDir();
  return join(base, '.claude', 'cre-skills', 'deals', dealId);
}

export function stateFilePath(dealId, baseDir) {
  return join(dealDir(dealId, baseDir), 'state.json');
}

// ---------------------------------------------------------------------------
// Shape validation (structural; the JSON Schema file is the contract of record)
// ---------------------------------------------------------------------------

export function assertValidState(state) {
  if (!state || typeof state !== 'object') {
    throw new Error('deal state must be an object');
  }
  const required = [
    'deal_id',
    'pipeline',
    'phase_history',
    'current_phase',
    'verdicts_by_phase',
    'approval_gate_log',
    'created_at',
    'updated_at',
    'run_id',
  ];
  for (const k of required) {
    if (!(k in state)) {
      throw new Error(`deal state missing required key: ${k}`);
    }
  }
  if (!/^[A-Za-z0-9_.-]{1,128}$/.test(state.deal_id)) {
    throw new Error(`deal state deal_id does not match pattern: ${state.deal_id}`);
  }
  if (!SUPPORTED_PIPELINES.includes(state.pipeline)) {
    throw new Error(`deal state pipeline not in supported set: ${state.pipeline}`);
  }
  if (!Array.isArray(state.phase_history)) {
    throw new Error('deal state phase_history must be an array');
  }
  if (!Array.isArray(state.approval_gate_log)) {
    throw new Error('deal state approval_gate_log must be an array');
  }
  if (typeof state.verdicts_by_phase !== 'object' || Array.isArray(state.verdicts_by_phase)) {
    throw new Error('deal state verdicts_by_phase must be an object');
  }
}

// ---------------------------------------------------------------------------
// Init / read / write
// ---------------------------------------------------------------------------

export function initState({ dealId, pipeline, variant, currentPhase, runId }) {
  if (!dealId) throw new Error('initState: dealId is required');
  if (!pipeline) throw new Error('initState: pipeline is required');
  if (!SUPPORTED_PIPELINES.includes(pipeline)) {
    throw new Error(`initState: unsupported pipeline "${pipeline}"`);
  }
  const now = new Date().toISOString();
  const state = {
    deal_id: dealId,
    pipeline,
    phase_history: [],
    current_phase: currentPhase || '',
    verdicts_by_phase: {},
    approval_gate_log: [],
    created_at: now,
    updated_at: now,
    run_id: runId || randomUUID(),
  };
  if (variant) state.variant = variant;
  assertValidState(state);
  return state;
}

export function readState(dealId, baseDir) {
  const path = stateFilePath(dealId, baseDir);
  if (!existsSync(path)) return null;
  const raw = readFileSync(path, 'utf-8');
  const state = JSON.parse(raw);
  assertValidState(state);
  return state;
}

export function writeState(state, baseDir) {
  assertValidState(state);
  state.updated_at = new Date().toISOString();
  const dir = dealDir(state.deal_id, baseDir);
  mkdirSync(dir, { recursive: true });
  const target = stateFilePath(state.deal_id, baseDir);
  const tmp = `${target}.tmp`;
  writeFileSync(tmp, JSON.stringify(state, null, 2), 'utf-8');
  renameSync(tmp, target);
  return target;
}

// ---------------------------------------------------------------------------
// Mutators (pure-ish: mutate and return the same object for chaining clarity)
// ---------------------------------------------------------------------------

export function recordPhaseStart(state, phaseId) {
  if (!VERDICT_VOCAB) {
    // unreachable; referenced so linters keep the import
  }
  state.current_phase = phaseId;
  if (!state.phase_history.some((p) => p.phase_id === phaseId && !p.completed_at)) {
    state.phase_history.push({
      phase_id: phaseId,
      started_at: new Date().toISOString(),
      completed_at: null,
      verdict: null,
    });
  }
  return state;
}

export function recordPhaseVerdict(state, phaseId, verdict, rationale) {
  if (!VERDICT_VOCAB.includes(verdict)) {
    throw new Error(`recordPhaseVerdict: verdict "${verdict}" not in ${VERDICT_VOCAB.join(', ')}`);
  }
  const now = new Date().toISOString();
  state.verdicts_by_phase[phaseId] = { verdict, timestamp: now, rationale: rationale || '' };

  // Close open history entry for this phase, if any.
  const open = state.phase_history.find(
    (p) => p.phase_id === phaseId && !p.completed_at,
  );
  if (open) {
    open.completed_at = now;
    open.verdict = verdict;
    if (rationale) open.rationale = rationale;
  } else {
    state.phase_history.push({
      phase_id: phaseId,
      started_at: now,
      completed_at: now,
      verdict,
      ...(rationale ? { rationale } : {}),
    });
  }
  return state;
}

export function appendGateEvent(state, gateEvent) {
  if (!gateEvent || !gateEvent.gate_id) {
    throw new Error('appendGateEvent: gate event must include gate_id');
  }
  state.approval_gate_log.push(gateEvent);
  return state;
}

// ---------------------------------------------------------------------------
// Resume helpers
// ---------------------------------------------------------------------------

export function isPhaseAlreadyResolved(state, phaseId) {
  const entry = state.verdicts_by_phase[phaseId];
  if (!entry) return false;
  return RESUMABLE_VERDICTS.has(entry.verdict);
}

export const _internal = {
  SUPPORTED_PIPELINES,
  VERDICT_VOCAB,
  RESUMABLE_VERDICTS,
};
