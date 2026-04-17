#!/usr/bin/env node

/**
 * CRE Pipeline Executor -- Zero-dependency state machine for multi-phase orchestration.
 *
 * Usage:
 *   node executor.mjs --pipeline acquisition [--investor-type institutional] \
 *     [--strategy core-plus] [--dry-run] [--resume <id>] [--skip-challenge] [--no-handoff]
 *
 * Reads pipeline config, builds a topologically sorted phase plan, dispatches agents
 * per phase (stub), evaluates phase verdicts, writes checkpoints, and aggregates a
 * final pipeline verdict.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { homedir } from 'node:os';
import { randomUUID } from 'node:crypto';

import {
  initState,
  readState,
  writeState,
  recordPhaseStart,
  recordPhaseVerdict,
  isPhaseAlreadyResolved,
} from './deal-state.mjs';
import { appendEvent as appendAuditEvent } from './audit-log.mjs';
import {
  loadVariantOverlay,
  applyVariantOverlay,
  variantExists,
} from './variant-loader.mjs';
import { evaluatePhaseGates } from './approval-gate.mjs';

// ---------------------------------------------------------------------------
// CLI arg parsing
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = {
    pipeline: null,
    investorType: null,
    strategy: null,
    dryRun: false,
    resume: null,
    dealId: null,
    skipChallenge: false,
    noHandoff: false,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--pipeline' && argv[i + 1]) { args.pipeline = argv[++i]; continue; }
    if (a === '--investor-type' && argv[i + 1]) { args.investorType = argv[++i]; continue; }
    if (a === '--strategy' && argv[i + 1]) { args.strategy = argv[++i]; continue; }
    if (a === '--dry-run') { args.dryRun = true; continue; }
    if (a === '--resume' && argv[i + 1]) { args.resume = argv[++i]; continue; }
    if (a === '--deal-id' && argv[i + 1]) { args.dealId = argv[++i]; continue; }
    if (a === '--skip-challenge') { args.skipChallenge = true; continue; }
    if (a === '--no-handoff') { args.noHandoff = true; continue; }
  }

  return args;
}

// ---------------------------------------------------------------------------
// File loading helpers
// ---------------------------------------------------------------------------

function loadJSON(filePath) {
  const raw = readFileSync(filePath, 'utf-8');
  return JSON.parse(raw);
}

function resolvePluginRoot() {
  // Walk up from this file until we find a directory containing orchestrators/
  let dir = dirname(resolve(import.meta.url.replace('file://', '')));
  for (let i = 0; i < 10; i++) {
    if (existsSync(join(dir, 'orchestrators'))) return dir;
    dir = dirname(dir);
  }
  // Fallback: two levels up from engine/
  return resolve(dirname(resolve(import.meta.url.replace('file://', ''))), '..', '..');
}

// ---------------------------------------------------------------------------
// Topological sort of phases by upstreamDependencies
// ---------------------------------------------------------------------------

function topologicalSort(phases) {
  const phaseMap = new Map();
  for (const p of phases) phaseMap.set(p.phaseId, p);

  const visited = new Set();
  const order = [];
  const visiting = new Set();

  function visit(id) {
    if (visited.has(id)) return;
    if (visiting.has(id)) throw new Error(`Circular dependency detected at phase: ${id}`);
    visiting.add(id);

    const phase = phaseMap.get(id);
    if (!phase) throw new Error(`Unknown phaseId referenced in dependencies: ${id}`);

    const deps = (phase.upstreamDependencies || []).map(d => d.phaseId);
    for (const dep of deps) visit(dep);

    visiting.delete(id);
    visited.add(id);
    order.push(phase);
  }

  for (const p of phases) visit(p.phaseId);
  return order;
}

// ---------------------------------------------------------------------------
// Checkpoint I/O
// ---------------------------------------------------------------------------

function checkpointDir(sessionId) {
  return join(homedir(), '.cre-skills', 'checkpoints', sessionId);
}

function writeCheckpoint(sessionId, phaseId, data) {
  const dir = checkpointDir(sessionId);
  mkdirSync(dir, { recursive: true });
  const filePath = join(dir, `${phaseId}.json`);
  writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
  return filePath;
}

function readCheckpoint(sessionId, phaseId) {
  const filePath = join(checkpointDir(sessionId), `${phaseId}.json`);
  if (!existsSync(filePath)) return null;
  return loadJSON(filePath);
}

// ---------------------------------------------------------------------------
// Agent loader stub
// ---------------------------------------------------------------------------

function loadAgentStub(agentConfig, pluginRoot) {
  const agentId = agentConfig.agentId;
  const filePath = join(pluginRoot, agentConfig.file);
  const fileExists = existsSync(filePath);
  return { agentId, filePath, fileExists, skillRefs: agentConfig.skillRefs || [] };
}

// ---------------------------------------------------------------------------
// Agent dispatch stub
// ---------------------------------------------------------------------------

function dispatchAgent(agent, phaseId, sessionId) {
  console.log(`  DISPATCH: ${agent.agentId} (phase: ${phaseId}, session: ${sessionId})`);
  // Stub output simulating an agent that completed successfully
  return {
    agentId: agent.agentId,
    status: 'COMPLETED',
    findings: [],
    redFlags: [],
    dataGaps: [],
    metrics: {},
    output: {},
  };
}

// ---------------------------------------------------------------------------
// Verdict evaluator (delegate to module)
// ---------------------------------------------------------------------------

async function loadVerdictEvaluator(pluginRoot) {
  const modPath = join(pluginRoot, 'orchestrators', 'engine', 'verdict-evaluator.mjs');
  if (!existsSync(modPath)) {
    console.warn('[WARN] verdict-evaluator.mjs not found; using built-in stub');
    return null;
  }
  const mod = await import(modPath);
  return mod.evaluateVerdict;
}

// ---------------------------------------------------------------------------
// Threshold merger (delegate to module)
// ---------------------------------------------------------------------------

async function loadThresholdMerger(pluginRoot) {
  const modPath = join(pluginRoot, 'orchestrators', 'engine', 'threshold-merger.mjs');
  if (!existsSync(modPath)) {
    console.warn('[WARN] threshold-merger.mjs not found; using built-in stub');
    return null;
  }
  const mod = await import(modPath);
  return mod.mergeThresholds;
}

// ---------------------------------------------------------------------------
// Profile loader (delegate to module)
// ---------------------------------------------------------------------------

async function loadProfileLoader(pluginRoot) {
  const modPath = join(pluginRoot, 'orchestrators', 'engine', 'profile-loader.mjs');
  if (!existsSync(modPath)) return null;
  const mod = await import(modPath);
  return mod.loadProfile;
}

// ---------------------------------------------------------------------------
// Stub: challenge layer
// ---------------------------------------------------------------------------

function runChallengeLayer(pipelineOutputs, config) {
  console.log('\n--- Challenge Layer (stub) ---');
  console.log('  Would dispatch Tier 1 perspective agents against pipeline outputs.');
  console.log('  Would evaluate Tier 2 conditional triggers.');
  console.log('  Challenge layer skipped (stub mode).');
  return { challenged: false, verdictRevised: false };
}

// ---------------------------------------------------------------------------
// Stub: handoff router
// ---------------------------------------------------------------------------

function runHandoffRouter(pipelineVerdict, crossChainHandoffs) {
  console.log('\n--- Cross-Chain Handoff Router (stub) ---');
  if (!crossChainHandoffs || crossChainHandoffs.length === 0) {
    console.log('  No handoffs configured.');
    return;
  }
  for (const h of crossChainHandoffs) {
    console.log(`  HANDOFF: ${h.direction} -> ${h.counterpartOrchestrator}`);
    console.log(`    Trigger: ${h.triggerCondition}`);
    console.log(`    Data keys: ${Object.keys(h.dataContract || {}).join(', ')}`);
  }
}

// ---------------------------------------------------------------------------
// Phase execution
// ---------------------------------------------------------------------------

function executePhase(phase, sessionId, pluginRoot, evaluateVerdictFn, thresholds, phaseResults) {
  const phaseId = phase.phaseId;
  console.log(`\n====== Phase: ${phase.name} (${phaseId}) [weight: ${phase.weight}] ======`);

  // Check upstream dependencies
  const deps = phase.upstreamDependencies || [];
  for (const dep of deps) {
    const upstream = phaseResults.get(dep.phaseId);
    if (!upstream) {
      console.log(`  [BLOCK] Upstream phase "${dep.phaseId}" has no result. Halting.`);
      return { phaseId, verdict: 'BLOCKED', reason: `Missing upstream: ${dep.phaseId}` };
    }
    const validStatuses = dep.requiredStatus || ['COMPLETED', 'CONDITIONAL'];
    if (!validStatuses.includes(upstream.verdict) && upstream.verdict !== 'PROCEED') {
      console.log(`  [BLOCK] Upstream "${dep.phaseId}" verdict=${upstream.verdict}, need one of: ${validStatuses.join(', ')}`);
      return { phaseId, verdict: 'BLOCKED', reason: `Upstream ${dep.phaseId} verdict: ${upstream.verdict}` };
    }
    // Check required data keys
    for (const rdk of (dep.requiredDataKeys || [])) {
      if (rdk.critical && (!upstream.outputs || upstream.outputs[rdk.key] === undefined)) {
        console.log(`  [WARN] Missing critical data key "${rdk.key}" from upstream "${dep.phaseId}"`);
      }
    }
  }

  // Dispatch agents
  const agents = phase.agents || [];
  const agentOutputs = {};

  // Sort agents within phase: those with no deps first
  const noDeps = agents.filter(a => !a.dependencies || a.dependencies.length === 0);
  const withDeps = agents.filter(a => a.dependencies && a.dependencies.length > 0);

  console.log(`  Agents (no deps, parallelizable): ${noDeps.map(a => a.agentId).join(', ') || 'none'}`);
  console.log(`  Agents (with deps, sequential):   ${withDeps.map(a => a.agentId).join(', ') || 'none'}`);

  for (const agent of noDeps) {
    const loaded = loadAgentStub(agent, pluginRoot);
    const result = dispatchAgent(agent, phaseId, sessionId);
    agentOutputs[agent.agentId] = result;
  }

  for (const agent of withDeps) {
    // Verify intra-phase deps completed
    const missingDeps = (agent.dependencies || []).filter(d => !agentOutputs[d] || agentOutputs[d].status !== 'COMPLETED');
    if (missingDeps.length > 0) {
      console.log(`  [WARN] Agent ${agent.agentId} has unmet deps: ${missingDeps.join(', ')}`);
    }
    const result = dispatchAgent(agent, phaseId, sessionId);
    agentOutputs[agent.agentId] = result;
  }

  // Evaluate phase verdict
  let verdict = 'PROCEED';
  let verdictDetail = {};
  const verdictLogic = phase.verdictLogic;

  if (verdictLogic && evaluateVerdictFn) {
    try {
      verdictDetail = evaluateVerdictFn(verdictLogic, agentOutputs, thresholds);
      verdict = verdictDetail.verdict || 'PROCEED';
    } catch (err) {
      console.log(`  [ERROR] Verdict evaluation failed: ${err.message}`);
      verdict = 'ERROR';
    }
  } else {
    // Fallback: all agents completed => PROCEED
    const allCompleted = Object.values(agentOutputs).every(o => o.status === 'COMPLETED');
    verdict = allCompleted ? 'COMPLETED' : 'CONDITIONAL';
    verdictDetail = { verdict, fallback: true };
  }

  console.log(`  Phase verdict: ${verdict}`);

  const result = {
    phaseId,
    phaseName: phase.name,
    verdict,
    verdictDetail,
    agentCount: agents.length,
    completedAgents: Object.values(agentOutputs).filter(o => o.status === 'COMPLETED').length,
    outputs: agentOutputs,
    timestamp: new Date().toISOString(),
  };

  return result;
}

// ---------------------------------------------------------------------------
// Verdict normalization for persistent state
// ---------------------------------------------------------------------------

function normalizeVerdictForState(verdict) {
  // deal_state.schema.json accepts: PROCEED, CONDITIONAL, KILL,
  // AWAITING_APPROVAL, REFUSED. The executor uses a slightly wider
  // vocabulary (COMPLETED, BLOCKED, FAILED) for phase-local purposes.
  switch (verdict) {
    case 'PROCEED':
    case 'COMPLETED':
      return 'PROCEED';
    case 'CONDITIONAL':
      return 'CONDITIONAL';
    case 'KILL':
    case 'BLOCKED':
    case 'FAILED':
      return 'KILL';
    case 'AWAITING_APPROVAL':
      return 'AWAITING_APPROVAL';
    case 'REFUSED':
      return 'REFUSED';
    default:
      return 'CONDITIONAL';
  }
}

// ---------------------------------------------------------------------------
// Pipeline verdict aggregation
// ---------------------------------------------------------------------------

function aggregatePipelineVerdict(phaseResults, config) {
  const verdictValues = config.checkpointConfig?.verdictValues || {};
  const results = Array.from(phaseResults.values());

  // Any AWAITING_APPROVAL -> AWAITING_APPROVAL (pipeline paused, not killed)
  if (results.some(r => r.verdict === 'AWAITING_APPROVAL')) {
    const paused = results.filter(r => r.verdict === 'AWAITING_APPROVAL').map(r => r.phaseId);
    return {
      verdict: 'AWAITING_APPROVAL',
      reason: `Awaiting human approval on: ${paused.join(', ')}`,
      verdictValues,
    };
  }

  // Any KILL / FAILED phase -> KILL
  if (results.some(r => r.verdict === 'KILL' || r.verdict === 'FAILED')) {
    return { verdict: 'KILL', reason: 'One or more phases returned KILL or FAILED', verdictValues };
  }

  // Any BLOCKED -> KILL
  if (results.some(r => r.verdict === 'BLOCKED')) {
    return { verdict: 'KILL', reason: 'One or more phases blocked by upstream failure', verdictValues };
  }

  // Any CONDITIONAL -> CONDITIONAL
  if (results.some(r => r.verdict === 'CONDITIONAL')) {
    const condPhases = results.filter(r => r.verdict === 'CONDITIONAL').map(r => r.phaseId);
    return { verdict: 'CONDITIONAL', reason: `Conditional phases: ${condPhases.join(', ')}`, verdictValues };
  }

  return { verdict: 'PROCEED', reason: 'All phases cleared', verdictValues };
}

// ---------------------------------------------------------------------------
// Dry-run plan printer
// ---------------------------------------------------------------------------

function printDryRunPlan(config, sortedPhases, mergedThresholds, args) {
  console.log('\n=== DRY RUN: Pipeline Execution Plan ===\n');
  console.log(`Pipeline:       ${config.orchestratorId}`);
  console.log(`Version:        ${config.version}`);
  console.log(`Entity type:    ${config.entityType}`);
  console.log(`Investor type:  ${args.investorType || 'base'}`);
  console.log(`Strategy:       ${args.strategy || 'default'}`);
  console.log(`Description:    ${config.description}\n`);

  console.log('Phase execution order:');
  for (let i = 0; i < sortedPhases.length; i++) {
    const p = sortedPhases[i];
    const deps = (p.upstreamDependencies || []).map(d => d.phaseId);
    const agents = (p.agents || []).map(a => `${a.agentId}${a.critical ? '*' : ''}`);
    console.log(`  ${i + 1}. ${p.name} (${p.phaseId}) [weight=${p.weight}]`);
    console.log(`     Upstream deps: ${deps.length > 0 ? deps.join(', ') : 'none'}`);
    console.log(`     Agents (${agents.length}): ${agents.join(', ')}`);
    if (p.verdictLogic) {
      const db = (p.verdictLogic.dealbreakers || []);
      console.log(`     Dealbreakers: ${db.length > 0 ? db.join(', ') : 'none'}`);
    }
  }

  if (mergedThresholds && mergedThresholds.merged) {
    console.log('\nMerged thresholds source map:');
    for (const [key, src] of Object.entries(mergedThresholds.sources || {})) {
      console.log(`  ${key}: ${src}`);
    }
  }

  if (config.crossChainHandoffs && config.crossChainHandoffs.length > 0) {
    console.log('\nCross-chain handoffs:');
    for (const h of config.crossChainHandoffs) {
      console.log(`  ${h.direction} -> ${h.counterpartOrchestrator} (trigger: ${h.triggerCondition})`);
    }
  }

  const totalAgents = sortedPhases.reduce((sum, p) => sum + (p.agents || []).length, 0);
  const criticalAgents = sortedPhases.reduce((sum, p) => sum + (p.agents || []).filter(a => a.critical).length, 0);
  console.log(`\nTotal agents: ${totalAgents} (${criticalAgents} critical)`);
  console.log('Verdict vocabulary:', Object.keys(config.checkpointConfig?.verdictValues || {}).join(', '));
}

// ---------------------------------------------------------------------------
// Summary printer
// ---------------------------------------------------------------------------

function printSummary(pipelineVerdict, phaseResults, sessionId, config) {
  console.log('\n====================================================');
  console.log('  PIPELINE EXECUTION SUMMARY');
  console.log('====================================================');
  console.log(`Pipeline:   ${config.orchestratorId}`);
  console.log(`Session:    ${sessionId}`);
  console.log(`Verdict:    ${pipelineVerdict.verdict}`);
  console.log(`Reason:     ${pipelineVerdict.reason}`);
  console.log('');
  console.log('Phase results:');
  for (const [phaseId, result] of phaseResults) {
    const icon = result.verdict === 'PROCEED' || result.verdict === 'COMPLETED' ? '[OK]'
      : result.verdict === 'CONDITIONAL' ? '[??]'
      : '[!!]';
    console.log(`  ${icon} ${result.phaseName || phaseId}: ${result.verdict} (${result.completedAgents}/${result.agentCount} agents)`);
  }
  console.log('');
  if (pipelineVerdict.verdict === 'PROCEED') {
    console.log('Pipeline cleared. Ready for downstream handoff.');
  } else if (pipelineVerdict.verdict === 'CONDITIONAL') {
    console.log('Pipeline conditionally cleared. Review conditions before proceeding.');
  } else {
    console.log('Pipeline terminated. Deal is not viable at current terms.');
  }
  console.log(`\nCheckpoints written to: ${checkpointDir(sessionId)}`);
  console.log('====================================================\n');
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const args = parseArgs(process.argv);

  if (!args.pipeline) {
    console.error('Usage: node executor.mjs --pipeline <name> [options]');
    console.error('Options:');
    console.error('  --pipeline <name>          Pipeline config name (required)');
    console.error('  --investor-type <type>     Investor type override');
    console.error('  --strategy <strategy>      Investment strategy override');
    console.error('  --dry-run                  Print execution plan and exit');
    console.error('  --deal-id <id>             Persist deal-scoped state and audit log (v4.4)');
    console.error('  --resume <sessionId>       Legacy checkpoint-only resume');
    console.error('  --skip-challenge           Skip the challenge layer');
    console.error('  --no-handoff               Skip cross-chain handoffs');
    process.exit(1);
  }

  const pluginRoot = resolvePluginRoot();
  console.log(`Plugin root: ${pluginRoot}`);

  // Load pipeline config
  const configPath = join(pluginRoot, 'orchestrators', 'configs', `${args.pipeline}.json`);
  if (!existsSync(configPath)) {
    console.error(`Pipeline config not found: ${configPath}`);
    process.exit(1);
  }
  let config = loadJSON(configPath);
  console.log(`Loaded pipeline: ${config.orchestratorId} v${config.version}`);

  // Variant overlay (v4.4, design doc section 4). When --strategy
  // matches a variant dir under configs/<pipeline>/variants/, apply
  // its weight overrides and added approval gates.
  if (args.strategy && variantExists(pluginRoot, args.pipeline, args.strategy)) {
    const overlay = loadVariantOverlay(pluginRoot, args.pipeline, args.strategy);
    config = applyVariantOverlay(config, overlay);
    console.log(`Applied variant overlay: ${args.strategy}`);
  } else if (args.strategy) {
    console.log(
      `No variant directory at configs/${args.pipeline}/variants/${args.strategy} — ` +
      `--strategy treated as a threshold-merge hint only.`,
    );
  }

  // Load thresholds
  const thresholdsPath = join(pluginRoot, 'orchestrators', 'thresholds.json');
  let thresholds = {};
  if (existsSync(thresholdsPath)) {
    thresholds = loadJSON(thresholdsPath);
    console.log('Loaded thresholds.json');
  } else {
    console.warn('[WARN] thresholds.json not found; using empty thresholds');
  }

  // Load investor profile and merge thresholds
  let mergedThresholds = null;
  const mergeThresholds = await loadThresholdMerger(pluginRoot);
  const loadProfileFn = await loadProfileLoader(pluginRoot);

  if (args.investorType) {
    if (loadProfileFn) {
      try {
        const profile = loadProfileFn(args.investorType, pluginRoot);
        console.log(`Loaded investor profile: ${profile.investorType}`);
      } catch (err) {
        console.warn(`[WARN] Could not load investor profile: ${err.message}`);
      }
    }

    if (mergeThresholds) {
      mergedThresholds = mergeThresholds(thresholds, args.investorType, args.strategy || null);
      if (mergedThresholds.excluded) {
        console.error(`Strategy "${args.strategy}" is not allowed for investor type "${args.investorType}".`);
        console.error(`Allowed strategies: ${mergedThresholds.excluded.allowedStrategies?.join(', ')}`);
        process.exit(1);
      }
      console.log(`Merged thresholds for ${args.investorType}/${args.strategy || 'default'}`);
    }
  }

  const effectiveThresholds = mergedThresholds?.merged || thresholds;

  // Build phase order
  const sortedPhases = topologicalSort(config.phases || []);
  console.log(`Phase order: ${sortedPhases.map(p => p.phaseId).join(' -> ')}`);

  // Dry run: print plan and exit
  if (args.dryRun) {
    printDryRunPlan(config, sortedPhases, mergedThresholds, args);
    process.exit(0);
  }

  // Session setup
  const sessionId = args.resume || randomUUID();
  const persistentMode = Boolean(args.dealId);
  console.log(
    `\nSession: ${sessionId}${args.resume ? ' (resumed)' : ''}` +
    (persistentMode ? ` | deal_id: ${args.dealId}` : ''),
  );

  // Persistent deal state (only when --deal-id is provided)
  let dealState = null;
  if (persistentMode) {
    const firstPhaseId = sortedPhases[0]?.phaseId || '';
    const existing = readState(args.dealId);
    if (existing) {
      if (existing.pipeline !== args.pipeline) {
        console.error(
          `[ERROR] Deal "${args.dealId}" was initialized with pipeline "${existing.pipeline}" ` +
          `but --pipeline ${args.pipeline} was passed. Refusing to mix pipelines for one deal.`,
        );
        process.exit(3);
      }
      dealState = existing;
      console.log(`[RESUME] Loaded existing deal state (run_id=${dealState.run_id}).`);
      appendAuditEvent({
        event: 'resume_started',
        actor: 'executor',
        deal_id: args.dealId,
        run_id: dealState.run_id,
      });
    } else {
      dealState = initState({
        dealId: args.dealId,
        pipeline: args.pipeline,
        variant: args.strategy || undefined,
        currentPhase: firstPhaseId,
        runId: sessionId,
      });
      writeState(dealState);
      appendAuditEvent({
        event: 'pipeline_started',
        actor: 'executor',
        deal_id: args.dealId,
        run_id: dealState.run_id,
        pipeline: args.pipeline,
        variant: args.strategy || null,
      });
    }
  }

  // Load verdict evaluator
  const evaluateVerdictFn = await loadVerdictEvaluator(pluginRoot);

  // Execute phases
  const phaseResults = new Map();

  for (const phase of sortedPhases) {
    // Persistent-mode resume: skip phases already resolved.
    if (persistentMode && isPhaseAlreadyResolved(dealState, phase.phaseId)) {
      const prior = dealState.verdicts_by_phase[phase.phaseId];
      console.log(
        `\n[RESUME] Skipping already-resolved phase: ${phase.phaseId} ` +
        `(verdict: ${prior.verdict})`,
      );
      phaseResults.set(phase.phaseId, {
        phaseId: phase.phaseId,
        phaseName: phase.name,
        verdict: prior.verdict,
        verdictDetail: { verdict: prior.verdict, resumed: true },
        agentCount: (phase.agents || []).length,
        completedAgents: (phase.agents || []).length,
        outputs: {},
        timestamp: prior.timestamp,
      });
      continue;
    }

    // Legacy checkpoint-only resume.
    if (args.resume && !persistentMode) {
      const existing = readCheckpoint(sessionId, phase.phaseId);
      if (existing && (existing.verdict === 'PROCEED' || existing.verdict === 'COMPLETED')) {
        console.log(`\n[RESUME] Skipping completed phase: ${phase.phaseId} (verdict: ${existing.verdict})`);
        phaseResults.set(phase.phaseId, existing);
        continue;
      }
    }

    if (persistentMode) {
      recordPhaseStart(dealState, phase.phaseId);
      writeState(dealState);
      appendAuditEvent({
        event: 'phase_started',
        actor: 'executor',
        deal_id: args.dealId,
        run_id: dealState.run_id,
        phase_id: phase.phaseId,
      });
    }

    // Approval gates: if this phase declares any, evaluate against
    // deal state BEFORE agent dispatch. Blocks the pipeline with
    // AWAITING_APPROVAL until an operator runs approve-gate.mjs.
    if (persistentMode && (phase.approval_gates || []).length > 0) {
      const gateEval = evaluatePhaseGates(phase, dealState);
      for (const gate of gateEval.newlyOpened) {
        appendAuditEvent({
          event: 'gate_opened',
          actor: 'executor',
          deal_id: args.dealId,
          run_id: dealState.run_id,
          phase_id: phase.phaseId,
          gate_id: gate.gate_id,
          approval_matrix_row: gate.approval_matrix_row,
        });
      }
      if (gateEval.blocked) {
        const blockedGateIds = gateEval.blockingGates.map((g) => g.gate_id).join(', ');
        console.log(
          `\n[HALT] Phase "${phase.phaseId}" awaits approval on gate(s): ${blockedGateIds}`,
        );
        const haltResult = {
          phaseId: phase.phaseId,
          phaseName: phase.name,
          verdict: 'AWAITING_APPROVAL',
          verdictDetail: {
            verdict: 'AWAITING_APPROVAL',
            blocking_gates: blockedGateIds,
          },
          agentCount: (phase.agents || []).length,
          completedAgents: 0,
          outputs: {},
          timestamp: new Date().toISOString(),
        };
        phaseResults.set(phase.phaseId, haltResult);
        writeCheckpoint(sessionId, phase.phaseId, haltResult);
        recordPhaseVerdict(
          dealState,
          phase.phaseId,
          'AWAITING_APPROVAL',
          `blocking_gates: ${blockedGateIds}`,
        );
        writeState(dealState);
        appendAuditEvent({
          event: 'phase_blocked',
          actor: 'executor',
          deal_id: args.dealId,
          run_id: dealState.run_id,
          phase_id: phase.phaseId,
          verdict: 'AWAITING_APPROVAL',
          blocking_gates: blockedGateIds,
        });
        break;
      }
      // State was mutated by evaluatePhaseGates.openGateIfAbsent; persist.
      writeState(dealState);
    }

    const result = executePhase(phase, sessionId, pluginRoot, evaluateVerdictFn, effectiveThresholds, phaseResults);
    phaseResults.set(phase.phaseId, result);

    // Write checkpoint (legacy side-car, preserved for back-compat).
    const cpPath = writeCheckpoint(sessionId, phase.phaseId, result);
    console.log(`  Checkpoint: ${cpPath}`);

    // Persist deal state + audit event.
    if (persistentMode) {
      const normalizedVerdict = normalizeVerdictForState(result.verdict);
      recordPhaseVerdict(
        dealState,
        phase.phaseId,
        normalizedVerdict,
        result.verdictDetail?.reason || '',
      );
      writeState(dealState);
      appendAuditEvent({
        event: 'phase_completed',
        actor: 'executor',
        deal_id: args.dealId,
        run_id: dealState.run_id,
        phase_id: phase.phaseId,
        verdict: normalizedVerdict,
      });
    }

    // If phase verdict is KILL or FAILED, halt pipeline
    if (result.verdict === 'KILL' || result.verdict === 'FAILED') {
      console.log(`\n[HALT] Phase "${phase.phaseId}" returned ${result.verdict}. Pipeline terminated.`);
      if (persistentMode) {
        appendAuditEvent({
          event: 'pipeline_halted',
          actor: 'executor',
          deal_id: args.dealId,
          run_id: dealState.run_id,
          phase_id: phase.phaseId,
          verdict: result.verdict,
        });
      }
      break;
    }
  }

  // Aggregate pipeline verdict
  const pipelineVerdict = aggregatePipelineVerdict(phaseResults, config);

  // Challenge layer
  if (!args.skipChallenge && config.challengeLayer) {
    runChallengeLayer(phaseResults, config.challengeLayer);
  }

  // Handoff router
  if (!args.noHandoff && config.crossChainHandoffs) {
    runHandoffRouter(pipelineVerdict, config.crossChainHandoffs);
  }

  // Write pipeline-level checkpoint
  const pipelineSummary = {
    orchestratorId: config.orchestratorId,
    sessionId,
    verdict: pipelineVerdict,
    phases: Object.fromEntries(
      Array.from(phaseResults.entries()).map(([k, v]) => [k, { verdict: v.verdict, agents: v.agentCount }])
    ),
    timestamp: new Date().toISOString(),
  };
  writeCheckpoint(sessionId, '_pipeline', pipelineSummary);

  // Print summary
  printSummary(pipelineVerdict, phaseResults, sessionId, config);

  if (persistentMode && dealState) {
    appendAuditEvent({
      event: 'pipeline_completed',
      actor: 'executor',
      deal_id: args.dealId,
      run_id: dealState.run_id,
      verdict: pipelineVerdict.verdict,
    });
  }

  // Exit 0 on PROCEED / CONDITIONAL / AWAITING_APPROVAL, 1 on KILL.
  // AWAITING_APPROVAL is a pause, not a failure.
  process.exit(pipelineVerdict.verdict === 'KILL' ? 1 : 0);
}

main().catch(err => {
  console.error(`[FATAL] ${err.message}`);
  console.error(err.stack);
  process.exit(2);
});
