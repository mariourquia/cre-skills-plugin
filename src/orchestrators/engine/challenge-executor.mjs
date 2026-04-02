#!/usr/bin/env node

/**
 * Challenge Executor -- Orchestrates the 3-tier challenge layer after a pipeline verdict.
 *
 * Export: executeChallenge(pipelineResult, dealContext, options)
 * Returns: { originalVerdict, challengeVerdict, changed, tiers, synthesis, disagreements }
 *
 * Run with --test to execute self-tests.
 */

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { evaluateTrigger } from './trigger-evaluator.mjs';
import { executeSynthesis } from './synthesis-executor.mjs';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function resolvePluginRoot(providedRoot) {
  if (providedRoot) return providedRoot;
  const thisFile = fileURLToPath(import.meta.url);
  // engine/ -> orchestrators/ -> plugin root
  return dirname(dirname(dirname(thisFile)));
}

function loadChallengeConfig(pluginRoot) {
  const configPath = join(pluginRoot, 'orchestrators', 'challenge-layer', 'config.json');
  const raw = readFileSync(configPath, 'utf-8');
  return JSON.parse(raw);
}

function buildAgentInput(inputSet, pipelineResult, dealContext, contextScoping) {
  const setConfig = contextScoping.inputSets[inputSet] || contextScoping.inputSets.standard;
  const tokenBudget = setConfig.tokens;
  const includes = setConfig.includes || [];

  return {
    inputSet,
    tokenBudget,
    includes,
    pipelineVerdict: pipelineResult.verdict,
    dealSummary: {
      investorType: dealContext.investorType || null,
      strategy: dealContext.strategy || null,
      propertyType: dealContext.propertyType || null,
    },
    phases: pipelineResult.phases || [],
    agentOutputs: pipelineResult.agentOutputs || {},
  };
}

function resolveBuyerDynamicAgent(agentConfig, dealContext) {
  if (!agentConfig.runtimeSelection) return agentConfig.file;

  const fieldPath = agentConfig.runtimeSelection.field || '';
  const mapping = agentConfig.runtimeSelection.mapping || {};
  const parts = fieldPath.split('.');
  let value = dealContext;
  for (const part of parts) {
    if (value === null || value === undefined || typeof value !== 'object') {
      value = undefined;
      break;
    }
    const desc = Object.getOwnPropertyDescriptor(value, part);
    value = desc !== undefined ? desc.value : undefined;
  }

  if (value && typeof value === 'string') {
    const mapped = Object.getOwnPropertyDescriptor(mapping, value);
    if (mapped !== undefined) return mapped.value;
  }

  const defaultDesc = Object.getOwnPropertyDescriptor(mapping, 'default');
  return defaultDesc !== undefined ? defaultDesc.value : null;
}

// ---------------------------------------------------------------------------
// Stub dispatch -- placeholder until real agent calls are wired
// ---------------------------------------------------------------------------

function stubDispatch(agentId, agentFile, agentInput) {
  return {
    agentId,
    agentFile,
    status: 'stub',
    output: `[Stub] ${agentId} analysis placeholder. Actual agent dispatch is future work.`,
    timestamp: new Date().toISOString(),
  };
}

// ---------------------------------------------------------------------------
// Tier 1: Always-run, sequential
// ---------------------------------------------------------------------------

async function executeTier1(config, pipelineResult, dealContext) {
  const tier1 = config.tiers.tier1;
  const results = Object.create(null);
  const agentsMeta = [];

  for (const agent of tier1.agents) {
    const agentId = agent.agent;
    let agentFile = agent.file;

    // Handle buyer-dynamic runtime selection
    if (agentId === 'buyer-dynamic') {
      agentFile = resolveBuyerDynamicAgent(agent, dealContext);
    }

    const inputSet = agent.inputSet || 'standard';
    const agentInput = buildAgentInput(inputSet, pipelineResult, dealContext, config.contextScoping);
    const estimatedMinutes = agent.estimatedMinutes || 2;

    console.log(`[CHALLENGE T1] Dispatching: ${agentId} (${estimatedMinutes}min)`);

    const output = stubDispatch(agentId, agentFile, agentInput);
    const outputKey = agent.outputKey || agentId;
    results[outputKey] = output;

    agentsMeta.push({
      agentId,
      agentFile,
      outputKey,
      inputSet,
      estimatedMinutes,
      status: output.status,
    });
  }

  return { results, agentsMeta, agentCount: tier1.agents.length };
}

// ---------------------------------------------------------------------------
// Tier 2: Conditional, parallel groups
// ---------------------------------------------------------------------------

async function executeTier2(config, pipelineResult, dealContext, options) {
  if (options.skipTier2) {
    console.log('[CHALLENGE T2] Skipped by options');
    return { results: Object.create(null), triggered: [], agentCount: 0 };
  }

  const tier2 = config.tiers.tier2;
  const results = Object.create(null);
  const triggered = [];
  let agentCount = 0;

  // Build a combined context for trigger evaluation
  const triggerContext = Object.assign(Object.create(null), dealContext);
  triggerContext.pipeline = { verdict: pipelineResult.verdict };

  for (const trigger of tier2.triggers) {
    const condition = trigger.condition || '';
    const isTriggered = evaluateTrigger(condition, triggerContext);

    if (!isTriggered) continue;

    console.log(`[CHALLENGE T2] Trigger fired: ${trigger.triggerId}`);
    triggered.push(trigger.triggerId);

    // Dispatch all agents in this trigger group (conceptually parallel)
    for (const agent of trigger.agents) {
      const agentId = agent.agent;
      const agentFile = agent.file;
      const inputSet = agent.inputSet || 'standard';
      const agentInput = buildAgentInput(inputSet, pipelineResult, dealContext, config.contextScoping);

      console.log(`[CHALLENGE T2] Dispatching: ${agentId} (trigger: ${trigger.triggerId})`);

      const output = stubDispatch(agentId, agentFile, agentInput);
      const outputKey = `${trigger.triggerId}_${agentId}`;
      results[outputKey] = output;
      agentCount++;
    }
  }

  return { results, triggered, agentCount };
}

// ---------------------------------------------------------------------------
// Tier 3: On-request
// ---------------------------------------------------------------------------

async function executeTier3(config, options) {
  if (options.skipTier3) {
    console.log('[CHALLENGE T3] Skipped by options');
    return { results: Object.create(null), available: [], selected: [], agentCount: 0 };
  }

  const tier3 = config.tiers.tier3;
  const available = tier3.agents.map(a => ({
    agentId: a.agent,
    purpose: a.purpose,
  }));

  const agentIds = available.map(a => a.agentId);
  console.log(`[CHALLENGE T3] Available: [${agentIds.join(', ')}] -- user selection would happen here`);

  // Stub: no agents selected (user interaction is future work)
  return { results: Object.create(null), available, selected: [], agentCount: 0 };
}

// ---------------------------------------------------------------------------
// Main: executeChallenge
// ---------------------------------------------------------------------------

/**
 * Orchestrate the 3-tier challenge layer against a pipeline verdict.
 *
 * @param {object} pipelineResult - { verdict, phases, agentOutputs }
 * @param {object} dealContext - { investorType, strategy, propertyType, ... }
 * @param {object} [options] - { skipTier2, skipTier3, tierTimeout, pluginRoot }
 * @returns {Promise<object>} Challenge result
 */
export async function executeChallenge(pipelineResult, dealContext, options = {}) {
  const pluginRoot = resolvePluginRoot(options.pluginRoot);
  const config = loadChallengeConfig(pluginRoot);

  const originalVerdict = pipelineResult.verdict;
  const tierTimeout = options.tierTimeout || config.executionConfig.tier1TimeoutMinutes * 60000;

  // --- Tier 1 ---
  const tier1Result = await executeTier1(config, pipelineResult, dealContext);

  // --- Tier 2 ---
  const tier2Result = await executeTier2(config, pipelineResult, dealContext, {
    skipTier2: options.skipTier2 || false,
  });

  // --- Tier 3 ---
  const tier3Result = await executeTier3(config, {
    skipTier3: options.skipTier3 !== false ? true : false,
  });

  // --- Synthesis ---
  const tierOutputs = {
    tier1: tier1Result.results,
    tier2: tier2Result.results,
    tier3: tier3Result.results,
  };

  const totalPerspectives = tier1Result.agentCount + tier2Result.agentCount + tier3Result.agentCount;
  console.log(`[CHALLENGE SYNTHESIS] Dispatching deal-team-lead with ${totalPerspectives} agent perspectives`);

  const synthesis = executeSynthesis(tierOutputs, pipelineResult, config);

  const challengeVerdict = synthesis.verdictConfirmation;
  const changed = challengeVerdict !== originalVerdict;

  if (changed) {
    console.log(`[VERDICT CHANGE] Original: ${originalVerdict}, Challenge recommends: ${challengeVerdict} -- requires human confirmation`);
  }

  return {
    originalVerdict,
    challengeVerdict,
    changed,
    tiers: {
      tier1: {
        agentCount: tier1Result.agentCount,
        agents: tier1Result.agentsMeta,
      },
      tier2: {
        agentCount: tier2Result.agentCount,
        triggered: tier2Result.triggered,
      },
      tier3: {
        agentCount: tier3Result.agentCount,
        available: tier3Result.available,
        selected: tier3Result.selected,
      },
    },
    synthesis,
    disagreements: synthesis.unresolvedDisagreements || [],
  };
}

// ---------------------------------------------------------------------------
// CLI self-test
// ---------------------------------------------------------------------------

async function selfTest() {
  console.log('--- challenge-executor self-test ---\n');

  const mockPipeline = {
    verdict: 'CONDITIONAL',
    phases: [{ phase: 1, score: 72 }],
    agentOutputs: {},
  };

  const mockDeal = {
    investorType: 'pension-fund',
    strategy: 'core',
    propertyType: 'multifamily',
    deal: {
      investorType: 'pension-fund',
      dueDiligence: { redFlags: [] },
      financing: { ltv: 0.45 },
      capex: { immediate: 100000, fiveYear: 300000 },
      strategy: 'core',
    },
    pipeline: { verdict: 'CONDITIONAL' },
  };

  try {
    const result = await executeChallenge(mockPipeline, mockDeal, {
      skipTier3: true,
    });

    console.log('\nResult summary:');
    console.log(`  originalVerdict: ${result.originalVerdict}`);
    console.log(`  challengeVerdict: ${result.challengeVerdict}`);
    console.log(`  changed: ${result.changed}`);
    console.log(`  tier1 agents: ${result.tiers.tier1.agentCount}`);
    console.log(`  tier2 triggered: [${result.tiers.tier2.triggered.join(', ')}]`);
    console.log(`  tier3 selected: ${result.tiers.tier3.selected.length}`);
    console.log(`  disagreements: ${result.disagreements.length}`);

    const pass = result.originalVerdict === 'CONDITIONAL'
      && result.tiers.tier1.agentCount === 8
      && Array.isArray(result.disagreements);

    console.log(`\nSelf-test: ${pass ? 'PASS' : 'FAIL'}`);
    process.exit(pass ? 0 : 1);
  } catch (err) {
    console.error('Self-test FAILED with error:', err.message);
    process.exit(1);
  }
}

if (process.argv.includes('--test')) {
  selfTest();
}
