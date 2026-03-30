#!/usr/bin/env node

/**
 * Engine module tests -- Zero-dependency test suite for orchestrator engine modules.
 *
 * Tests: navigatePath, compareValues, evaluateVerdict, mergeThresholds,
 *        validateDataContract, loadProfile.
 *
 * Run: node tests/test-engine.mjs
 */

import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve plugin root relative to this file
const __dirname = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ROOT = resolve(__dirname, '..');

// Import modules under test
const verdictMod = await import(join(PLUGIN_ROOT, 'orchestrators', 'engine', 'verdict-evaluator.mjs'));
const thresholdMod = await import(join(PLUGIN_ROOT, 'orchestrators', 'engine', 'threshold-merger.mjs'));
const contractMod = await import(join(PLUGIN_ROOT, 'orchestrators', 'engine', 'data-contract-validator.mjs'));
const profileMod = await import(join(PLUGIN_ROOT, 'orchestrators', 'engine', 'profile-loader.mjs'));

const { navigatePath, compareValues, evaluateVerdict } = verdictMod;
const { mergeThresholds } = thresholdMod;
const { validateDataContract } = contractMod;
const { loadProfile } = profileMod;

// ---------------------------------------------------------------------------
// Test harness
// ---------------------------------------------------------------------------

let totalPass = 0;
let totalFail = 0;
const failedTests = [];

function assert(suite, label, condition) {
  const tag = `[${suite}] ${label}`;
  if (condition) {
    totalPass++;
    console.log(`  PASS: ${tag}`);
  } else {
    totalFail++;
    failedTests.push(tag);
    console.log(`  FAIL: ${tag}`);
  }
}

// ---------------------------------------------------------------------------
// 1. navigatePath tests
// ---------------------------------------------------------------------------

function testNavigatePath() {
  console.log('\n--- navigatePath ---');

  // Simple property
  assert('navigatePath', 'simple property', navigatePath({ a: 1 }, 'a') === 1);

  // Nested property
  assert('navigatePath', 'nested property', navigatePath({ a: { b: { c: 42 } } }, 'a.b.c') === 42);

  // Missing key returns undefined
  assert('navigatePath', 'missing key', navigatePath({ a: 1 }, 'b') === undefined);

  // Missing nested key returns undefined
  assert('navigatePath', 'missing nested key', navigatePath({ a: { b: 1 } }, 'a.c.d') === undefined);

  // Null object returns undefined
  assert('navigatePath', 'null object', navigatePath(null, 'a') === undefined);

  // Empty path returns undefined
  assert('navigatePath', 'empty path', navigatePath({ a: 1 }, '') === undefined);

  // Value is zero (falsy but valid)
  assert('navigatePath', 'zero value', navigatePath({ a: 0 }, 'a') === 0);

  // Value is false (falsy but valid)
  assert('navigatePath', 'false value', navigatePath({ a: false }, 'a') === false);

  // Prototype property not accessible
  assert('navigatePath', 'prototype not accessible', navigatePath({}, 'constructor') === undefined);
  assert('navigatePath', 'toString not accessible', navigatePath({}, 'toString') === undefined);
}

// ---------------------------------------------------------------------------
// 2. compareValues tests
// ---------------------------------------------------------------------------

function testCompareValues() {
  console.log('\n--- compareValues ---');

  assert('compareValues', 'eq: 5 == 5', compareValues(5, 'eq', 5) === true);
  assert('compareValues', 'eq: 5 != 6', compareValues(5, 'eq', 6) === false);
  assert('compareValues', 'neq: 5 != 6', compareValues(5, 'neq', 6) === true);
  assert('compareValues', 'neq: 5 == 5', compareValues(5, 'neq', 5) === false);
  assert('compareValues', 'gt: 6 > 5', compareValues(6, 'gt', 5) === true);
  assert('compareValues', 'gt: 5 > 5', compareValues(5, 'gt', 5) === false);
  assert('compareValues', 'gte: 5 >= 5', compareValues(5, 'gte', 5) === true);
  assert('compareValues', 'gte: 4 >= 5', compareValues(4, 'gte', 5) === false);
  assert('compareValues', 'lt: 4 < 5', compareValues(4, 'lt', 5) === true);
  assert('compareValues', 'lt: 5 < 5', compareValues(5, 'lt', 5) === false);
  assert('compareValues', 'lte: 5 <= 5', compareValues(5, 'lte', 5) === true);
  assert('compareValues', 'lte: 6 <= 5', compareValues(6, 'lte', 5) === false);
  assert('compareValues', 'contains: array includes', compareValues([1, 2, 3], 'contains', 2) === true);
  assert('compareValues', 'contains: array missing', compareValues([1, 2, 3], 'contains', 4) === false);
  assert('compareValues', 'contains: string includes', compareValues('hello world', 'contains', 'world') === true);
  assert('compareValues', 'in: value in array', compareValues('a', 'in', ['a', 'b', 'c']) === true);
  assert('compareValues', 'in: value not in array', compareValues('d', 'in', ['a', 'b', 'c']) === false);
  assert('compareValues', 'exists: value present', compareValues(42, 'exists', null) === true);
  assert('compareValues', 'exists: null', compareValues(null, 'exists', null) === false);
  assert('compareValues', 'not_exists: undefined', compareValues(undefined, 'not_exists', null) === true);
  assert('compareValues', 'not_exists: present', compareValues(42, 'not_exists', null) === false);
  assert('compareValues', 'null actual with eq', compareValues(null, 'eq', 5) === false);
}

// ---------------------------------------------------------------------------
// 3. evaluateVerdict tests
// ---------------------------------------------------------------------------

function testEvaluateVerdict() {
  console.log('\n--- evaluateVerdict ---');

  // PROCEED: all agents complete, no issues
  {
    const logic = {
      passConditions: [{ conditionId: 'all-critical-agents-complete', description: 'All agents done', propagateIfFailed: true }],
      failConditions: [],
      conditionalConditions: [],
      dealbreakers: ['envLien'],
    };
    const outputs = {
      agent1: { status: 'COMPLETED', redFlags: [], findings: [], output: {}, metrics: {} },
      agent2: { status: 'COMPLETED', redFlags: [], findings: [], output: {}, metrics: {} },
    };
    const result = evaluateVerdict(logic, outputs, {});
    assert('evaluateVerdict', 'PROCEED: clean outputs', result.verdict === 'PROCEED');
    assert('evaluateVerdict', 'PROCEED: no dealbreakers', result.dealbreakersTriggered.length === 0);
  }

  // KILL: dealbreaker triggered
  {
    const logic = {
      passConditions: [],
      failConditions: [],
      conditionalConditions: [],
      dealbreakers: ['envLien', 'titleCloud'],
    };
    const outputs = {
      agent1: { status: 'COMPLETED', redFlags: ['envLien'], findings: [], output: {}, metrics: {} },
    };
    const result = evaluateVerdict(logic, outputs, {});
    assert('evaluateVerdict', 'KILL: dealbreaker', result.verdict === 'KILL');
    assert('evaluateVerdict', 'KILL: identifies envLien', result.dealbreakersTriggered.includes('envLien'));
    assert('evaluateVerdict', 'KILL: only envLien', result.dealbreakersTriggered.length === 1);
  }

  // CONDITIONAL: agent failure
  {
    const logic = {
      passConditions: [{ conditionId: 'all-critical-agents-complete', description: 'test', propagateIfFailed: true }],
      failConditions: [],
      conditionalConditions: [],
      dealbreakers: [],
    };
    const outputs = {
      agent1: { status: 'COMPLETED', redFlags: [], findings: [], output: {}, metrics: {} },
      agent2: { status: 'FAILED', redFlags: [], findings: [], output: {}, metrics: {} },
    };
    const result = evaluateVerdict(logic, outputs, {});
    assert('evaluateVerdict', 'CONDITIONAL: agent failure', result.verdict === 'CONDITIONAL');
  }

  // KILL: fail condition met
  {
    const logic = {
      passConditions: [],
      failConditions: [{ conditionId: 'irr-below-floor', metricPath: 'irr', operator: 'lt', value: 0.10, propagateIfFailed: true }],
      conditionalConditions: [],
      dealbreakers: [],
    };
    const outputs = {
      model: { status: 'COMPLETED', redFlags: [], findings: [], output: { irr: 0.05 }, metrics: {} },
    };
    const result = evaluateVerdict(logic, outputs, {});
    assert('evaluateVerdict', 'KILL: fail condition', result.verdict === 'KILL');
  }

  // No verdictLogic => PROCEED
  {
    const result = evaluateVerdict(null, {}, {});
    assert('evaluateVerdict', 'null logic => PROCEED', result.verdict === 'PROCEED');
  }
}

// ---------------------------------------------------------------------------
// 4. mergeThresholds tests
// ---------------------------------------------------------------------------

function testMergeThresholds() {
  console.log('\n--- mergeThresholds ---');

  const sampleThresholds = {
    primaryCriteria: {
      dscr: { pass: 1.25, conditional: 1.0, fail: 1.0 },
      ltv: { maxPass: 0.75, maxConditional: 0.80, fail: 0.80 },
    },
    primaryCriteriaByInvestorType: {
      institutional: {
        dscr: { pass: 1.35, conditional: 1.25, fail: 1.15 },
        ltv: { maxPass: 0.40, maxConditional: 0.50, fail: 0.60 },
      },
    },
    strategyThresholdsByInvestorType: {
      institutional: {
        allowedStrategies: ['core', 'core-plus'],
        core: { minDSCR: 1.40, maxLTV: 0.45 },
        'core-plus': { minDSCR: 1.30, maxLTV: 0.55 },
      },
    },
    dealbreakers: ['Active title dispute'],
    dealbreakersByInvestorType: {
      institutional: ['LTV exceeding 0.60'],
    },
    secondaryCriteria: { occupancy: { strong: 0.95 } },
    secondaryCriteriaByInvestorType: {},
  };

  // Base only (unknown type)
  {
    const result = mergeThresholds(sampleThresholds, 'unknown-type', null);
    assert('mergeThresholds', 'unknown type: has warnings', result.warnings.length > 0);
    assert('mergeThresholds', 'unknown type: merged not null', result.merged !== null);
  }

  // Investor override
  {
    const result = mergeThresholds(sampleThresholds, 'institutional', null);
    assert('mergeThresholds', 'investor override: not excluded', result.excluded === null);
    const primary = result.merged.primaryCriteria;
    assert('mergeThresholds', 'investor override: dscr.pass=1.35', primary.dscr && primary.dscr.pass === 1.35);
    assert('mergeThresholds', 'investor override: ltv.maxPass=0.40', primary.ltv && primary.ltv.maxPass === 0.40);
  }

  // Excluded strategy
  {
    const result = mergeThresholds(sampleThresholds, 'institutional', 'value-add');
    assert('mergeThresholds', 'excluded strategy: excluded set', result.excluded !== null);
    assert('mergeThresholds', 'excluded strategy: allowed has core', result.excluded.allowedStrategies.includes('core'));
  }

  // Strategy overlay
  {
    const result = mergeThresholds(sampleThresholds, 'institutional', 'core');
    assert('mergeThresholds', 'strategy overlay: not excluded', result.excluded === null);
    const primary = result.merged.primaryCriteria;
    assert('mergeThresholds', 'strategy overlay: minDSCR=1.40', primary.minDSCR === 1.40);
    assert('mergeThresholds', 'strategy overlay: maxLTV=0.45', primary.maxLTV === 0.45);
  }

  // Dealbreaker merging
  {
    const result = mergeThresholds(sampleThresholds, 'institutional', null);
    const dbs = result.merged.dealbreakers;
    assert('mergeThresholds', 'dealbreakers: includes base', dbs.includes('Active title dispute'));
    assert('mergeThresholds', 'dealbreakers: includes investor', dbs.includes('LTV exceeding 0.60'));
  }
}

// ---------------------------------------------------------------------------
// 5. validateDataContract tests
// ---------------------------------------------------------------------------

function testValidateDataContract() {
  console.log('\n--- validateDataContract ---');

  // Pass: all required keys present with correct types
  {
    const output = { rentRoll: { units: 100 }, envStatus: 'CLEAN', cost: 5000000 };
    const contract = {
      rentRoll: { type: 'object', required: true },
      envStatus: { type: 'string', required: true },
      cost: { type: 'number', required: true },
    };
    const result = validateDataContract(output, contract);
    assert('dataContract', 'pass: valid output', result.valid === true);
    assert('dataContract', 'pass: no missing keys', result.missingKeys.length === 0);
    assert('dataContract', 'pass: no type errors', result.typeErrors.length === 0);
  }

  // Missing required key
  {
    const output = { envStatus: 'CLEAN' };
    const contract = {
      rentRoll: { type: 'object', required: true },
      envStatus: { type: 'string', required: true },
    };
    const result = validateDataContract(output, contract);
    assert('dataContract', 'missing required: invalid', result.valid === false);
    assert('dataContract', 'missing required: identifies rentRoll', result.missingKeys.includes('rentRoll'));
  }

  // Wrong type
  {
    const output = { rentRoll: 'not an object', envStatus: 'CLEAN' };
    const contract = {
      rentRoll: { type: 'object', required: true },
      envStatus: { type: 'string', required: true },
    };
    const result = validateDataContract(output, contract);
    assert('dataContract', 'wrong type: invalid', result.valid === false);
    assert('dataContract', 'wrong type: type error on rentRoll', result.typeErrors.some(e => e.key === 'rentRoll'));
  }

  // Optional key missing is fine
  {
    const output = { required1: 'yes' };
    const contract = {
      required1: { type: 'string', required: true },
      optional1: { type: 'number', required: false },
    };
    const result = validateDataContract(output, contract);
    assert('dataContract', 'optional missing: still valid', result.valid === true);
  }

  // Null output with required keys
  {
    const contract = { data: { type: 'object', required: true } };
    const result = validateDataContract(null, contract);
    assert('dataContract', 'null output: invalid', result.valid === false);
  }

  // No contract spec
  {
    const result = validateDataContract({ a: 1 }, null);
    assert('dataContract', 'no contract: valid with warning', result.valid === true && result.warnings.length > 0);
  }
}

// ---------------------------------------------------------------------------
// 6. loadProfile tests
// ---------------------------------------------------------------------------

function testLoadProfile() {
  console.log('\n--- loadProfile ---');

  // Valid type: institutional
  {
    try {
      const profile = loadProfile('institutional', PLUGIN_ROOT);
      assert('loadProfile', 'institutional: loads', profile !== null);
      assert('loadProfile', 'institutional: has investorType', profile.investorType === 'institutional');
    } catch (err) {
      assert('loadProfile', `institutional: loads (error: ${err.message})`, false);
    }
  }

  // Alias resolution: pe -> private-equity
  {
    try {
      const profile = loadProfile('pe', PLUGIN_ROOT);
      assert('loadProfile', 'alias pe: loads private-equity', profile !== null);
    } catch (err) {
      assert('loadProfile', `alias pe: loads (error: ${err.message})`, false);
    }
  }

  // Alias resolution: pension-fund -> institutional
  {
    try {
      const profile = loadProfile('pension-fund', PLUGIN_ROOT);
      assert('loadProfile', 'alias pension-fund: loads institutional', profile.investorType === 'institutional');
    } catch (err) {
      assert('loadProfile', `alias pension-fund: loads (error: ${err.message})`, false);
    }
  }

  // Invalid type throws
  {
    try {
      loadProfile('nonexistent-type-xyz', PLUGIN_ROOT);
      assert('loadProfile', 'invalid type: throws', false);
    } catch (err) {
      assert('loadProfile', 'invalid type: throws', err.message.includes('not found'));
    }
  }

  // Null type throws
  {
    try {
      loadProfile(null, PLUGIN_ROOT);
      assert('loadProfile', 'null type: throws', false);
    } catch (err) {
      assert('loadProfile', 'null type: throws', err.message.includes('required'));
    }
  }
}

// ---------------------------------------------------------------------------
// Run all tests
// ---------------------------------------------------------------------------

console.log('========================================');
console.log('  CRE Pipeline Engine -- Test Suite');
console.log('========================================');

testNavigatePath();
testCompareValues();
testEvaluateVerdict();
testMergeThresholds();
testValidateDataContract();
testLoadProfile();

console.log('\n========================================');
console.log(`  TOTAL: ${totalPass} passed, ${totalFail} failed`);
if (failedTests.length > 0) {
  console.log('\n  Failed tests:');
  for (const t of failedTests) console.log(`    - ${t}`);
}
console.log('========================================\n');

process.exit(totalFail > 0 ? 1 : 0);
