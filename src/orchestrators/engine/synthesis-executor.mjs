#!/usr/bin/env node

/**
 * Synthesis Executor -- Aggregates tier outputs and produces a challenge layer synthesis.
 *
 * Export: executeSynthesis(tierOutputs, pipelineResult, challengeConfig)
 * Returns: { challengeSummary, verdictConfirmation, unresolvedDisagreements, conditionsPrecedent, icRecommendation }
 *
 * Run with --test to execute self-tests.
 */

import { fileURLToPath } from 'node:url';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function countPerspectives(tierOutputs) {
  let count = 0;
  if (tierOutputs.tier1) count += Object.keys(tierOutputs.tier1).length;
  if (tierOutputs.tier2) count += Object.keys(tierOutputs.tier2).length;
  if (tierOutputs.tier3) count += Object.keys(tierOutputs.tier3).length;
  return count;
}

function truncateOutputs(tierOutputs, maxTokens) {
  // Rough truncation: stringify and limit by character count (approx 4 chars per token)
  const charLimit = maxTokens * 4;
  const serialized = JSON.stringify(tierOutputs);
  if (serialized.length <= charLimit) return tierOutputs;

  // Truncate by removing tier3 first, then tier2 detail
  const truncated = {
    tier1: tierOutputs.tier1,
    tier2: tierOutputs.tier2,
    tier3: Object.create(null),
  };

  const reSerialized = JSON.stringify(truncated);
  if (reSerialized.length <= charLimit) return truncated;

  // Further truncation: summarize tier2 keys only
  const tier2Summary = Object.create(null);
  if (tierOutputs.tier2) {
    for (const key of Object.keys(tierOutputs.tier2)) {
      tier2Summary[key] = { status: tierOutputs.tier2[key].status || 'truncated' };
    }
  }

  return {
    tier1: tierOutputs.tier1,
    tier2: tier2Summary,
    tier3: Object.create(null),
  };
}

function detectCriticalDisagreements(tierOutputs, pipelineVerdict) {
  // Stub detection: scan tier outputs for any stub that might indicate
  // disagreement. In production, actual agent outputs would carry structured
  // verdict recommendations that can be compared.
  //
  // For now, return an empty array. When real agents run, this function
  // should compare each agent's recommended verdict against the pipeline
  // verdict and flag any that disagree.
  return [];
}

// ---------------------------------------------------------------------------
// Main: executeSynthesis
// ---------------------------------------------------------------------------

/**
 * Aggregate tier outputs and produce a synthesis result for IC presentation.
 *
 * @param {object} tierOutputs - { tier1: { [outputKey]: output }, tier2: {...}, tier3: {...} }
 * @param {object} pipelineResult - { verdict, phases }
 * @param {object} challengeConfig - Parsed config for token budgets and synthesis agent config
 * @returns {object} Synthesis result
 */
export function executeSynthesis(tierOutputs, pipelineResult, challengeConfig) {
  const totalPerspectives = countPerspectives(tierOutputs);

  // Determine token budget for synthesis context
  const synthesisConfig = challengeConfig.synthesis || {};
  const maxOutputTokens = synthesisConfig.maxOutputTokens || 3000;
  const totalBudgetMax = challengeConfig.executionConfig
    ? challengeConfig.executionConfig.totalBudgetTokensMax || 90000
    : 90000;

  // Truncate tier outputs to fit within the synthesis token budget
  const truncatedOutputs = truncateOutputs(tierOutputs, totalBudgetMax);

  console.log(`[SYNTHESIS] Aggregating ${totalPerspectives} perspectives for deal-team-lead`);

  // Stub: deal-team-lead dispatch (actual agent call is future work)
  // In production, this would send truncatedOutputs to the deal-team-lead agent
  // and receive a structured synthesis response.

  const originalVerdict = pipelineResult.verdict;
  const criticalDisagreements = detectCriticalDisagreements(tierOutputs, originalVerdict);
  const hasVerdictChange = criticalDisagreements.length > 0;

  const challengeSummary = `Challenge layer reviewed by ${totalPerspectives} perspective${totalPerspectives !== 1 ? 's' : ''}`;

  const verdictConfirmation = hasVerdictChange ? 'REVISED' : originalVerdict;

  const result = {
    challengeSummary,
    verdictConfirmation,
    unresolvedDisagreements: criticalDisagreements,
    conditionsPrecedent: [],
    icRecommendation: verdictConfirmation,
    perspectiveCount: totalPerspectives,
    synthesisAgent: synthesisConfig.agent || 'deal-team-lead',
    synthesisModel: synthesisConfig.model || 'claude-opus-4-6[1m]',
    maxOutputTokens,
  };

  // Flag if verdict changed from pipeline
  if (verdictConfirmation !== originalVerdict) {
    result.requiresHumanConfirmation = true;
    result.originalPipelineVerdict = originalVerdict;
  }

  return result;
}

// ---------------------------------------------------------------------------
// CLI self-test
// ---------------------------------------------------------------------------

function selfTest() {
  console.log('--- synthesis-executor self-test ---\n');

  const mockTierOutputs = {
    tier1: {
      veteran_challenge: { agentId: 'cre-veteran', status: 'stub', output: 'placeholder' },
      ic_challenge: { agentId: 'ic-challenger', status: 'stub', output: 'placeholder' },
      risk_challenge: { agentId: 'lens-risk-manager', status: 'stub', output: 'placeholder' },
    },
    tier2: {
      'environmental-rec_lens-esg-impact': { agentId: 'lens-esg-impact', status: 'stub', output: 'placeholder' },
    },
    tier3: {},
  };

  const mockPipeline = {
    verdict: 'GO',
    phases: [{ phase: 1, score: 85 }],
  };

  const mockConfig = {
    synthesis: {
      agent: 'deal-team-lead',
      model: 'claude-opus-4-6[1m]',
      maxOutputTokens: 3000,
    },
    executionConfig: {
      totalBudgetTokensMax: 90000,
    },
  };

  let passed = 0;
  let failed = 0;

  function check(name, actual, expected) {
    const ok = actual === expected;
    console.log(`  ${ok ? 'PASS' : 'FAIL'}: ${name} => ${JSON.stringify(actual)} (expected ${JSON.stringify(expected)})`);
    if (ok) passed++;
    else failed++;
  }

  const result = executeSynthesis(mockTierOutputs, mockPipeline, mockConfig);

  check('perspectiveCount', result.perspectiveCount, 4);
  check('challengeSummary includes count', result.challengeSummary.includes('4'), true);
  check('verdictConfirmation matches original (no disagreements)', result.verdictConfirmation, 'GO');
  check('icRecommendation matches verdict', result.icRecommendation, 'GO');
  check('unresolvedDisagreements is empty array', Array.isArray(result.unresolvedDisagreements), true);
  check('unresolvedDisagreements length', result.unresolvedDisagreements.length, 0);
  check('conditionsPrecedent is empty array', Array.isArray(result.conditionsPrecedent), true);
  check('synthesisAgent', result.synthesisAgent, 'deal-team-lead');
  check('synthesisModel', result.synthesisModel, 'claude-opus-4-6[1m]');
  check('no requiresHumanConfirmation when verdict unchanged', result.requiresHumanConfirmation, undefined);

  // Test with empty tier outputs
  const emptyResult = executeSynthesis({ tier1: {}, tier2: {}, tier3: {} }, mockPipeline, mockConfig);
  check('zero perspectives', emptyResult.perspectiveCount, 0);
  check('zero perspectives summary', emptyResult.challengeSummary.includes('0'), true);

  console.log(`\nResults: ${passed} passed, ${failed} failed out of ${passed + failed}`);
  console.log(`\nSelf-test: ${failed === 0 ? 'PASS' : 'FAIL'}`);
  process.exit(failed === 0 ? 0 : 1);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1] && process.argv.includes('--test')) {
  selfTest();
}
