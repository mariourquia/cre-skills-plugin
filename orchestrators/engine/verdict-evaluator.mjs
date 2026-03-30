#!/usr/bin/env node

/**
 * Verdict Evaluator -- Evaluates phase verdict logic against agent outputs and thresholds.
 *
 * Export: evaluateVerdict(verdictLogic, agentOutputs, thresholds)
 * Returns: { verdict, passedConditions, failedConditions, unresolvedConditions, dealbreakersTriggered }
 *
 * Run with --test to execute self-tests.
 */

// ---------------------------------------------------------------------------
// Path navigation: "a.b.c" -> obj.a.b.c
// ---------------------------------------------------------------------------

export function navigatePath(obj, path) {
  if (!obj || !path) return undefined;
  const parts = path.split('.');
  let current = obj;
  for (const part of parts) {
    if (current === null || current === undefined) return undefined;
    if (typeof current !== 'object') return undefined;
    const descriptor = Object.getOwnPropertyDescriptor(current, part);
    if (descriptor === undefined) return undefined;
    current = descriptor.value;
  }
  return current;
}

// ---------------------------------------------------------------------------
// Value comparison with operator
// ---------------------------------------------------------------------------

export function compareValues(actual, operator, expected) {
  if (operator === 'exists') return actual !== undefined && actual !== null;
  if (operator === 'not_exists') return actual === undefined || actual === null;

  if (actual === undefined || actual === null) return false;

  switch (operator) {
    case 'eq':
      return actual === expected;
    case 'neq':
      return actual !== expected;
    case 'gt':
      return Number(actual) > Number(expected);
    case 'gte':
      return Number(actual) >= Number(expected);
    case 'lt':
      return Number(actual) < Number(expected);
    case 'lte':
      return Number(actual) <= Number(expected);
    case 'contains':
      if (Array.isArray(actual)) return actual.includes(expected);
      if (typeof actual === 'string') return actual.includes(String(expected));
      return false;
    case 'in':
      if (Array.isArray(expected)) return expected.includes(actual);
      return false;
    default:
      return false;
  }
}

// ---------------------------------------------------------------------------
// Resolve a threshold reference like "underwriting.minIRR" from thresholds object
// ---------------------------------------------------------------------------

function resolveThresholdRef(thresholds, ref) {
  if (ref === undefined || ref === null) return undefined;
  return navigatePath(thresholds, ref);
}

// ---------------------------------------------------------------------------
// Check dealbreakers in agent outputs
// ---------------------------------------------------------------------------

function checkDealbreakers(dealbreakers, agentOutputs) {
  const triggered = [];
  if (!dealbreakers || dealbreakers.length === 0) return triggered;

  // Flatten all agent outputs into a searchable set of flags
  const allFlags = new Set();
  for (const [agentId, output] of Object.entries(agentOutputs)) {
    // Check redFlags array
    if (Array.isArray(output.redFlags)) {
      for (const flag of output.redFlags) allFlags.add(flag);
    }
    // Check output object for dealbreaker keys
    if (output.output && typeof output.output === 'object') {
      for (const key of Object.keys(output.output)) allFlags.add(key);
    }
    // Check status
    if (output.status === 'FAILED') allFlags.add(`${agentId}_FAILED`);
    // Check findings for dealbreaker strings
    if (Array.isArray(output.findings)) {
      for (const f of output.findings) {
        if (typeof f === 'string') allFlags.add(f);
      }
    }
  }

  for (const db of dealbreakers) {
    if (allFlags.has(db)) {
      triggered.push(db);
    }
  }

  return triggered;
}

// ---------------------------------------------------------------------------
// Evaluate pass conditions
// ---------------------------------------------------------------------------

function evaluatePassConditions(conditions, agentOutputs, thresholds) {
  const passed = [];
  const failed = [];
  const unresolved = [];

  if (!conditions) return { passed, failed, unresolved };

  for (const cond of conditions) {
    const condId = cond.conditionId;

    // Special condition: all critical agents complete
    if (condId === 'all-critical-agents-complete') {
      const allDone = Object.values(agentOutputs).every(
        o => o.status === 'COMPLETED' || o.status === undefined
      );
      const anyFailed = Object.values(agentOutputs).some(o => o.status === 'FAILED');
      if (allDone && !anyFailed) {
        passed.push({ conditionId: condId, description: cond.description });
      } else {
        failed.push({ conditionId: condId, description: cond.description, propagate: cond.propagateIfFailed });
      }
      continue;
    }

    // Metric-based condition
    if (cond.metricPath) {
      // Search all agent outputs for the metric
      let actualValue = undefined;
      for (const output of Object.values(agentOutputs)) {
        const val = navigatePath(output.output, cond.metricPath) ??
                    navigatePath(output.metrics, cond.metricPath) ??
                    navigatePath(output, cond.metricPath);
        if (val !== undefined) { actualValue = val; break; }
      }

      if (actualValue === undefined) {
        unresolved.push({ conditionId: condId, description: cond.description, reason: 'metric not found' });
        continue;
      }

      let expectedValue = cond.value;
      if (cond.thresholdRef) {
        expectedValue = resolveThresholdRef(thresholds, cond.thresholdRef);
      }
      if (expectedValue === undefined) expectedValue = cond.value;

      const op = cond.operator || 'eq';
      const result = compareValues(actualValue, op, expectedValue);

      if (result) {
        passed.push({ conditionId: condId, actual: actualValue, expected: expectedValue, operator: op });
      } else {
        failed.push({ conditionId: condId, actual: actualValue, expected: expectedValue, operator: op, propagate: cond.propagateIfFailed });
      }
    } else {
      // Non-metric condition: treated as unresolved (needs external evaluation)
      unresolved.push({ conditionId: condId, description: cond.description, reason: 'no metric path' });
    }
  }

  return { passed, failed, unresolved };
}

// ---------------------------------------------------------------------------
// Evaluate fail conditions
// ---------------------------------------------------------------------------

function evaluateFailConditions(conditions, agentOutputs, thresholds) {
  const triggered = [];
  if (!conditions) return triggered;

  for (const cond of conditions) {
    if (!cond.metricPath) continue;

    let actualValue = undefined;
    for (const output of Object.values(agentOutputs)) {
      const val = navigatePath(output.output, cond.metricPath) ??
                  navigatePath(output.metrics, cond.metricPath) ??
                  navigatePath(output, cond.metricPath);
      if (val !== undefined) { actualValue = val; break; }
    }

    if (actualValue === undefined) continue;

    let expectedValue = cond.value;
    if (cond.thresholdRef) {
      expectedValue = resolveThresholdRef(thresholds, cond.thresholdRef);
    }

    const op = cond.operator || 'eq';
    if (compareValues(actualValue, op, expectedValue)) {
      triggered.push({
        conditionId: cond.conditionId,
        description: cond.description,
        actual: actualValue,
        expected: expectedValue,
        propagate: cond.propagateIfFailed,
      });
    }
  }

  return triggered;
}

// ---------------------------------------------------------------------------
// Evaluate conditional conditions
// ---------------------------------------------------------------------------

function evaluateConditionalConditions(conditions, agentOutputs, thresholds) {
  const active = [];
  if (!conditions) return active;

  for (const cond of conditions) {
    // Conditional conditions are noted if present; they don't fail the phase
    // but shift verdict from PROCEED to CONDITIONAL
    if (cond.metricPath) {
      let actualValue = undefined;
      for (const output of Object.values(agentOutputs)) {
        const val = navigatePath(output.output, cond.metricPath) ??
                    navigatePath(output.metrics, cond.metricPath) ??
                    navigatePath(output, cond.metricPath);
        if (val !== undefined) { actualValue = val; break; }
      }

      if (actualValue !== undefined && cond.operator) {
        let expectedValue = cond.value;
        if (cond.thresholdRef) {
          expectedValue = resolveThresholdRef(thresholds, cond.thresholdRef);
        }
        if (compareValues(actualValue, cond.operator, expectedValue)) {
          active.push({ conditionId: cond.conditionId, description: cond.description, propagate: cond.propagateIfFailed });
        }
      }
    } else {
      // Non-metric conditionals: check if any agent flagged the condition
      const flagged = Object.values(agentOutputs).some(o => {
        if (Array.isArray(o.findings)) return o.findings.includes(cond.conditionId);
        if (Array.isArray(o.redFlags)) return o.redFlags.includes(cond.conditionId);
        return false;
      });
      if (flagged) {
        active.push({ conditionId: cond.conditionId, description: cond.description, propagate: cond.propagateIfFailed });
      }
    }
  }

  return active;
}

// ---------------------------------------------------------------------------
// Main verdict evaluator
// ---------------------------------------------------------------------------

export function evaluateVerdict(verdictLogic, agentOutputs, thresholds) {
  if (!verdictLogic) {
    return { verdict: 'PROCEED', passedConditions: [], failedConditions: [], unresolvedConditions: [], dealbreakersTriggered: [] };
  }

  // 1. Check dealbreakers (highest priority)
  const dealbreakersTriggered = checkDealbreakers(verdictLogic.dealbreakers || [], agentOutputs);

  if (dealbreakersTriggered.length > 0) {
    return {
      verdict: 'KILL',
      passedConditions: [],
      failedConditions: [],
      unresolvedConditions: [],
      dealbreakersTriggered,
      reason: `Dealbreakers triggered: ${dealbreakersTriggered.join(', ')}`,
    };
  }

  // 2. Evaluate fail conditions
  const failTriggered = evaluateFailConditions(verdictLogic.failConditions, agentOutputs, thresholds);

  if (failTriggered.length > 0) {
    return {
      verdict: 'KILL',
      passedConditions: [],
      failedConditions: failTriggered,
      unresolvedConditions: [],
      dealbreakersTriggered: [],
      reason: `Fail conditions triggered: ${failTriggered.map(f => f.conditionId).join(', ')}`,
    };
  }

  // 3. Evaluate pass conditions
  const { passed, failed, unresolved } = evaluatePassConditions(verdictLogic.passConditions, agentOutputs, thresholds);

  // 4. Evaluate conditional conditions
  const conditionalActive = evaluateConditionalConditions(verdictLogic.conditionalConditions, agentOutputs, thresholds);

  // 5. Determine verdict: KILL > CONDITIONAL > PROCEED
  let verdict;

  // If any pass condition with propagateIfFailed failed, this is significant
  const propagatingFailures = failed.filter(f => f.propagate);

  if (propagatingFailures.length > 0) {
    // Propagating pass-condition failures are serious but not necessarily KILL
    // unless combined with other signals
    verdict = 'CONDITIONAL';
  } else if (conditionalActive.length > 0) {
    verdict = 'CONDITIONAL';
  } else if (failed.length > 0) {
    // Non-propagating failures still push to CONDITIONAL
    verdict = 'CONDITIONAL';
  } else {
    verdict = 'PROCEED';
  }

  return {
    verdict,
    passedConditions: passed,
    failedConditions: failed,
    unresolvedConditions: unresolved,
    dealbreakersTriggered: [],
    conditionalConditions: conditionalActive,
  };
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

  console.log('\n--- verdict-evaluator self-tests ---\n');

  // Test 1: PROCEED when all agents complete, no dealbreakers
  {
    const logic = {
      passConditions: [{ conditionId: 'all-critical-agents-complete', description: 'test', propagateIfFailed: true }],
      failConditions: [],
      conditionalConditions: [],
      dealbreakers: ['envLien'],
    };
    const outputs = { agent1: { status: 'COMPLETED', redFlags: [], findings: [], output: {}, metrics: {} } };
    const result = evaluateVerdict(logic, outputs, {});
    assert('PROCEED: all agents complete, no dealbreakers', result.verdict === 'PROCEED');
  }

  // Test 2: KILL on dealbreaker
  {
    const logic = {
      passConditions: [],
      failConditions: [],
      conditionalConditions: [],
      dealbreakers: ['envLien'],
    };
    const outputs = { agent1: { status: 'COMPLETED', redFlags: ['envLien'], findings: [], output: {}, metrics: {} } };
    const result = evaluateVerdict(logic, outputs, {});
    assert('KILL: dealbreaker triggered', result.verdict === 'KILL');
    assert('KILL: dealbreaker identified', result.dealbreakersTriggered.includes('envLien'));
  }

  // Test 3: CONDITIONAL when agent fails
  {
    const logic = {
      passConditions: [{ conditionId: 'all-critical-agents-complete', description: 'test', propagateIfFailed: true }],
      failConditions: [],
      conditionalConditions: [],
      dealbreakers: [],
    };
    const outputs = { agent1: { status: 'FAILED', redFlags: [], findings: [], output: {}, metrics: {} } };
    const result = evaluateVerdict(logic, outputs, {});
    assert('CONDITIONAL: agent failure', result.verdict === 'CONDITIONAL');
  }

  // Test 4: KILL on fail condition
  {
    const logic = {
      passConditions: [],
      failConditions: [{ conditionId: 'dscr-too-low', metricPath: 'dscr', operator: 'lt', value: 1.0, propagateIfFailed: true }],
      conditionalConditions: [],
      dealbreakers: [],
    };
    const outputs = { agent1: { status: 'COMPLETED', redFlags: [], findings: [], output: { dscr: 0.8 }, metrics: {} } };
    const result = evaluateVerdict(logic, outputs, {});
    assert('KILL: fail condition triggered', result.verdict === 'KILL');
  }

  // Test 5: CONDITIONAL from conditional condition
  {
    const logic = {
      passConditions: [{ conditionId: 'all-critical-agents-complete', description: 'test', propagateIfFailed: false }],
      failConditions: [],
      conditionalConditions: [{ conditionId: 'minor-issue', description: 'minor', propagateIfFailed: false }],
      dealbreakers: [],
    };
    const outputs = {
      agent1: { status: 'COMPLETED', redFlags: [], findings: ['minor-issue'], output: {}, metrics: {} },
    };
    const result = evaluateVerdict(logic, outputs, {});
    assert('CONDITIONAL: conditional condition active', result.verdict === 'CONDITIONAL');
  }

  console.log(`\nResults: ${pass} passed, ${fail} failed\n`);
  process.exit(fail > 0 ? 1 : 0);
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

if (process.argv[1] && (process.argv[1].endsWith('verdict-evaluator.mjs') || process.argv[1].endsWith('verdict-evaluator'))) {
  if (process.argv.includes('--test')) {
    runTests();
  }
}
