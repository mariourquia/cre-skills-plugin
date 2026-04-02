#!/usr/bin/env node

/**
 * Threshold Merger -- Implements the 6-step thresholdSelectionProtocol from thresholds.json.
 *
 * Export: mergeThresholds(baseThresholds, investorType, investmentStrategy)
 * Returns: { merged, sources, excluded, warnings }
 *
 * Run with --test to execute self-tests.
 */

// ---------------------------------------------------------------------------
// Safe property access (prototype-pollution-safe)
// ---------------------------------------------------------------------------

function safeGet(obj, key) {
  if (obj === null || obj === undefined || typeof obj !== 'object') return undefined;
  const desc = Object.getOwnPropertyDescriptor(obj, key);
  return desc === undefined ? undefined : desc.value;
}

function safeGetPath(obj, path) {
  if (!obj || !path) return undefined;
  const parts = path.split('.');
  let current = obj;
  for (const part of parts) {
    if (current === null || current === undefined) return undefined;
    if (typeof current !== 'object') return undefined;
    const desc = Object.getOwnPropertyDescriptor(current, part);
    if (desc === undefined) return undefined;
    current = desc.value;
  }
  return current;
}

// ---------------------------------------------------------------------------
// Deep merge with source tracking
// ---------------------------------------------------------------------------

function deepMerge(target, source, sourceLabel, sources) {
  if (!source || typeof source !== 'object') return target;

  const result = Object.assign(Object.create(null), target);
  const keys = Object.getOwnPropertyNames(source);

  for (const key of keys) {
    const srcVal = safeGet(source, key);
    const tgtVal = safeGet(result, key);

    if (srcVal !== null && typeof srcVal === 'object' && !Array.isArray(srcVal) &&
        tgtVal !== null && typeof tgtVal === 'object' && !Array.isArray(tgtVal)) {
      result[key] = deepMerge(tgtVal, srcVal, sourceLabel, sources);
    } else {
      result[key] = srcVal;
      if (sources) sources[key] = sourceLabel;
    }
  }

  return result;
}

// ---------------------------------------------------------------------------
// Merge thresholds per protocol
// ---------------------------------------------------------------------------

export function mergeThresholds(baseThresholds, investorType, investmentStrategy) {
  const warnings = [];
  const sources = Object.create(null);

  // Step 1: Validate investorType
  const validTypes = ['institutional', 'pe', 'reit', 'familyOffice', 'syndicator'];
  if (!investorType || !validTypes.includes(investorType)) {
    warnings.push(`Unrecognized investorType "${investorType}"; falling back to base thresholds`);
    return {
      merged: Object.assign(Object.create(null), safeGet(baseThresholds, 'primaryCriteria') || {}),
      sources,
      excluded: null,
      warnings,
    };
  }

  // Step 2: Read investmentStrategy (may be null)
  if (investmentStrategy) {
    const validStrategies = ['core', 'core-plus', 'value-add', 'opportunistic'];
    if (!validStrategies.includes(investmentStrategy)) {
      warnings.push(`Unrecognized investmentStrategy "${investmentStrategy}"; ignoring strategy overlay`);
      investmentStrategy = null;
    }
  }

  // Base layer: primaryCriteria
  const basePrimary = safeGet(baseThresholds, 'primaryCriteria') || {};
  let merged = deepMerge(Object.create(null), basePrimary, 'base', sources);

  // Step 5a: Overlay investor-type primary criteria
  const investorOverrides = safeGetPath(baseThresholds, `primaryCriteriaByInvestorType.${investorType}`);
  if (investorOverrides) {
    merged = deepMerge(merged, investorOverrides, `investorType:${investorType}`, sources);
  } else {
    warnings.push(`No primaryCriteriaByInvestorType entry for "${investorType}"`);
  }

  // Step 3 & 4: Strategy thresholds
  if (investmentStrategy) {
    const strategyByType = safeGetPath(baseThresholds, `strategyThresholdsByInvestorType.${investorType}`);

    if (strategyByType) {
      // Step 4: Check allowedStrategies
      const allowed = safeGet(strategyByType, 'allowedStrategies');
      if (Array.isArray(allowed) && !allowed.includes(investmentStrategy)) {
        return {
          merged: null,
          sources,
          excluded: {
            investorType,
            investmentStrategy,
            allowedStrategies: allowed,
            reason: `Strategy "${investmentStrategy}" is not allowed for investor type "${investorType}"`,
          },
          warnings,
        };
      }

      // Step 5b: Overlay strategy-specific thresholds
      const strategyOverrides = safeGet(strategyByType, investmentStrategy);
      if (strategyOverrides) {
        merged = deepMerge(merged, strategyOverrides, `strategy:${investorType}/${investmentStrategy}`, sources);
      }
    } else {
      warnings.push(`No strategyThresholdsByInvestorType entry for "${investorType}"`);
    }
  }

  // Also merge secondary criteria if available
  const baseSecondary = safeGet(baseThresholds, 'secondaryCriteria') || {};
  let mergedSecondary = deepMerge(Object.create(null), baseSecondary, 'base:secondary', sources);

  const investorSecondary = safeGetPath(baseThresholds, `secondaryCriteriaByInvestorType.${investorType}`);
  if (investorSecondary) {
    mergedSecondary = deepMerge(mergedSecondary, investorSecondary, `investorType:${investorType}:secondary`, sources);
  }

  // Merge dealbreakers: base + investor-specific (append, not replace)
  const baseDealbreakers = safeGet(baseThresholds, 'dealbreakers') || [];
  const investorDealbreakers = safeGetPath(baseThresholds, `dealbreakersByInvestorType.${investorType}`) || [];
  const allDealbreakers = [...new Set([...baseDealbreakers, ...investorDealbreakers])];

  // Compose full merged object
  const fullMerged = Object.create(null);
  fullMerged.primaryCriteria = merged;
  fullMerged.secondaryCriteria = mergedSecondary;
  fullMerged.dealbreakers = allDealbreakers;

  // Copy phase-specific thresholds through
  for (const key of ['dueDiligence', 'underwriting', 'financing', 'legal', 'closing', 'riskScore', 'strategyThresholds']) {
    const val = safeGet(baseThresholds, key);
    if (val !== undefined) fullMerged[key] = val;
  }

  return { merged: fullMerged, sources, excluded: null, warnings };
}

// ---------------------------------------------------------------------------
// Self-tests (run with --test)
// ---------------------------------------------------------------------------

function runTests() {
  let pass = 0;
  let fail = 0;

  function assert(label, condition) {
    if (condition) { pass++; console.log(`  PASS: ${label}`); }
    else { fail++; console.log(`  FAIL: ${label}`); }
  }

  console.log('\n--- threshold-merger self-tests ---\n');

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
    secondaryCriteriaByInvestorType: {
      institutional: { occupancy: { strong: 0.97 } },
    },
  };

  // Test 1: Base only (unknown investor type)
  {
    const result = mergeThresholds(sampleThresholds, 'unknown', null);
    assert('Base only: returns merged with warning', result.merged !== null && result.warnings.length > 0);
  }

  // Test 2: Investor override applied
  {
    const result = mergeThresholds(sampleThresholds, 'institutional', null);
    assert('Investor override: excluded is null', result.excluded === null);
    const dscr = safeGetPath(result.merged, 'primaryCriteria.dscr');
    assert('Investor override: dscr.pass = 1.35', dscr && dscr.pass === 1.35);
  }

  // Test 3: Excluded strategy
  {
    const result = mergeThresholds(sampleThresholds, 'institutional', 'value-add');
    assert('Excluded strategy: excluded is set', result.excluded !== null);
    assert('Excluded strategy: reason mentions value-add', result.excluded.reason.includes('value-add'));
  }

  // Test 4: Strategy overlay
  {
    const result = mergeThresholds(sampleThresholds, 'institutional', 'core');
    assert('Strategy overlay: excluded is null', result.excluded === null);
    const primary = safeGet(result.merged, 'primaryCriteria');
    const minDSCR = safeGet(primary, 'minDSCR');
    assert('Strategy overlay: minDSCR = 1.40', minDSCR === 1.40);
  }

  console.log(`\nResults: ${pass} passed, ${fail} failed\n`);
  process.exit(fail > 0 ? 1 : 0);
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

const scriptName = process.argv[1] || '';
if (scriptName.endsWith('threshold-merger.mjs') || scriptName.endsWith('threshold-merger')) {
  if (process.argv.includes('--test')) {
    runTests();
  }
}
