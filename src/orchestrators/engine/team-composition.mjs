#!/usr/bin/env node

/**
 * Team Composition -- Customizes the challenge-layer agent roster based on investor profiles.
 *
 * Export: customizeTeam(challengeConfig, investorProfile)
 * Returns: modified challengeConfig with agent roster overrides applied
 *
 * Run with --test to execute self-tests.
 */

import { fileURLToPath } from 'node:url';

// ---------------------------------------------------------------------------
// Main: customizeTeam
// ---------------------------------------------------------------------------

/**
 * Apply investor profile team composition overrides to a challenge config.
 *
 * @param {object} challengeConfig - Parsed challenge-layer/config.json
 * @param {object} investorProfile - Parsed investor profile with teamComposition
 * @returns {object} Modified challengeConfig (deep clone -- original is not mutated)
 */
export function customizeTeam(challengeConfig, investorProfile) {
  if (!challengeConfig || !investorProfile) {
    throw new Error('Both challengeConfig and investorProfile are required');
  }

  // Deep clone to avoid mutating the original
  const config = JSON.parse(JSON.stringify(challengeConfig));
  const teamComp = investorProfile.teamComposition;

  if (!teamComp) return config;

  // --- Tier 1 overrides ---
  if (teamComp.tier1Override) {
    const override = teamComp.tier1Override;

    // Replace buyer-dynamic with the profile-specified buyer agent
    if (override.buyerAgent) {
      const agents = config.tiers.tier1.agents;
      for (let i = 0; i < agents.length; i++) {
        if (agents[i].agent === 'buyer-dynamic') {
          agents[i].agent = override.buyerAgent;
          agents[i].file = `${override.buyerAgent}.md`;
          agents[i].outputKey = 'buyer_challenge';
          // Remove runtimeSelection since it is now resolved
          delete agents[i].runtimeSelection;
          break;
        }
      }
    }

    // Add additional agents to tier-1
    if (Array.isArray(override.additionalAgents)) {
      const existingIds = new Set(config.tiers.tier1.agents.map(a => a.agent));
      for (const agentId of override.additionalAgents) {
        if (existingIds.has(agentId)) continue;
        config.tiers.tier1.agents.push({
          agent: agentId,
          file: `${agentId}.md`,
          model: 'claude-sonnet-4-6[1m]',
          inputSet: 'standard',
          maxOutputTokens: 1200,
          estimatedMinutes: 2,
          purpose: `Added by investor profile override: ${investorProfile.investorType}`,
          outputKey: `${agentId.replace(/-/g, '_')}_challenge`,
        });
      }
    }

    // Remove agents from tier-1
    if (Array.isArray(override.removeAgents)) {
      const removeSet = new Set(override.removeAgents);
      config.tiers.tier1.agents = config.tiers.tier1.agents.filter(
        a => !removeSet.has(a.agent)
      );
    }
  }

  // --- Tier 2 bias ---
  if (teamComp.tier2Bias) {
    const bias = teamComp.tier2Bias;
    const triggers = config.tiers.tier2.triggers;

    // Mark triggers that should always fire
    if (Array.isArray(bias.alwaysTrigger)) {
      const alwaysSet = new Set(bias.alwaysTrigger);
      for (const trigger of triggers) {
        if (alwaysSet.has(trigger.triggerId)) {
          trigger.alwaysFire = true;
        }
      }
    }

    // Mark triggers that should never fire
    if (Array.isArray(bias.neverTrigger)) {
      const neverSet = new Set(bias.neverTrigger);
      for (const trigger of triggers) {
        if (neverSet.has(trigger.triggerId)) {
          trigger.neverFire = true;
        }
      }
    }
  }

  return config;
}

// ---------------------------------------------------------------------------
// CLI self-test
// ---------------------------------------------------------------------------

function selfTest() {
  console.log('--- team-composition self-test ---\n');

  const mockConfig = {
    tiers: {
      tier1: {
        agents: [
          { agent: 'cre-veteran', file: 'cre-veteran.md', outputKey: 'veteran_challenge' },
          { agent: 'buyer-dynamic', file: null, outputKey: 'buyer_challenge', runtimeSelection: {} },
          { agent: 'lens-risk-manager', file: 'lens-risk-manager.md', outputKey: 'risk_challenge' },
        ],
      },
      tier2: {
        triggers: [
          { triggerId: 'environmental-rec', condition: 'test', agents: [] },
          { triggerId: 'aggressive-gp', condition: 'test', agents: [] },
          { triggerId: 'high-ltv', condition: 'test', agents: [] },
        ],
      },
    },
  };

  const mockProfile = {
    investorType: 'institutional',
    teamComposition: {
      tier1Override: {
        buyerAgent: 'buyer-pension-fund',
        additionalAgents: ['lens-esg-impact'],
        removeAgents: [],
      },
      tier2Bias: {
        alwaysTrigger: ['environmental-rec'],
        neverTrigger: ['aggressive-gp'],
      },
    },
  };

  let passed = 0;
  let failed = 0;

  function check(name, actual, expected) {
    const ok = actual === expected;
    console.log(`  ${ok ? 'PASS' : 'FAIL'}: ${name} => ${actual} (expected ${expected})`);
    if (ok) passed++;
    else failed++;
  }

  const result = customizeTeam(mockConfig, mockProfile);

  // buyer-dynamic replaced
  const buyerAgent = result.tiers.tier1.agents.find(a => a.agent === 'buyer-pension-fund');
  check('buyer-dynamic replaced with buyer-pension-fund', buyerAgent !== undefined, true);

  // runtimeSelection removed
  check('runtimeSelection removed', buyerAgent ? buyerAgent.runtimeSelection : 'missing', undefined);

  // lens-esg-impact added
  const esgAgent = result.tiers.tier1.agents.find(a => a.agent === 'lens-esg-impact');
  check('lens-esg-impact added to tier1', esgAgent !== undefined, true);

  // Original tier1 count was 3, now should be 4 (replaced 1, added 1, removed 0)
  check('tier1 agent count', result.tiers.tier1.agents.length, 4);

  // alwaysTrigger flag set
  const envTrigger = result.tiers.tier2.triggers.find(t => t.triggerId === 'environmental-rec');
  check('environmental-rec alwaysFire', envTrigger ? envTrigger.alwaysFire : false, true);

  // neverTrigger flag set
  const gpTrigger = result.tiers.tier2.triggers.find(t => t.triggerId === 'aggressive-gp');
  check('aggressive-gp neverFire', gpTrigger ? gpTrigger.neverFire : false, true);

  // high-ltv not flagged
  const ltvTrigger = result.tiers.tier2.triggers.find(t => t.triggerId === 'high-ltv');
  check('high-ltv no bias flags', ltvTrigger ? (ltvTrigger.alwaysFire || ltvTrigger.neverFire || false) : false, false);

  // Original not mutated
  check('original config not mutated', mockConfig.tiers.tier1.agents[1].agent, 'buyer-dynamic');

  console.log(`\nResults: ${passed} passed, ${failed} failed out of ${passed + failed}`);
  console.log(`\nSelf-test: ${failed === 0 ? 'PASS' : 'FAIL'}`);
  process.exit(failed === 0 ? 0 : 1);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1] && process.argv.includes('--test')) {
  selfTest();
}
