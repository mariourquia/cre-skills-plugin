#!/usr/bin/env node

/**
 * Trigger Evaluator -- Parses and evaluates trigger condition strings against a context object.
 *
 * Export: evaluateTrigger(condition, context)
 * Returns: boolean
 *
 * Run with --test to execute self-tests.
 */

import { fileURLToPath } from 'node:url';

// ---------------------------------------------------------------------------
// Dot-path navigation (mirrors verdict-evaluator pattern)
// ---------------------------------------------------------------------------

function navigatePath(obj, path) {
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
// Single comparison evaluation
// ---------------------------------------------------------------------------

function evaluateSingle(left, operator, right, context) {
  const actualValue = navigatePath(context, left);

  switch (operator) {
    case 'includes':
    case 'contains': {
      if (Array.isArray(actualValue)) {
        return actualValue.indexOf(right) !== -1;
      }
      if (typeof actualValue === 'string') {
        return actualValue.indexOf(right) !== -1;
      }
      return false;
    }
    case '==': {
      if (actualValue === undefined || actualValue === null) return false;
      // eslint-disable-next-line eqeqeq
      return String(actualValue) == String(right);
    }
    case '!=': {
      if (actualValue === undefined || actualValue === null) return true;
      // eslint-disable-next-line eqeqeq
      return String(actualValue) != String(right);
    }
    case '>': {
      const numRight = resolveNumericRight(right, context);
      return Number(actualValue) > numRight;
    }
    case '>=': {
      const numRight = resolveNumericRight(right, context);
      return Number(actualValue) >= numRight;
    }
    case '<': {
      const numRight = resolveNumericRight(right, context);
      return Number(actualValue) < numRight;
    }
    case '<=': {
      const numRight = resolveNumericRight(right, context);
      return Number(actualValue) <= numRight;
    }
    default:
      return false;
  }
}

/**
 * Resolve the right-hand side of a comparison. If it looks like a dot-path
 * that resolves to a number (e.g., "thresholds.primaryCriteria.ltv.maxConditional"),
 * navigate the context. If it contains arithmetic (e.g., "deal.purchasePrice * 0.10"),
 * attempt a simple multiply/divide. Otherwise parse as a number or return the string.
 */
function resolveNumericRight(right, context) {
  if (right === undefined || right === null) return NaN;
  const trimmed = String(right).trim();

  // Check for simple arithmetic: path * number or path / number
  const arithMatch = trimmed.match(/^(.+?)\s*([*/])\s*(.+)$/);
  if (arithMatch) {
    const leftVal = resolveNumericRight(arithMatch[1].trim(), context);
    const rightVal = parseFloat(arithMatch[3].trim());
    if (!isNaN(leftVal) && !isNaN(rightVal)) {
      return arithMatch[2] === '*' ? leftVal * rightVal : leftVal / rightVal;
    }
  }

  // Try as a context path
  if (trimmed.indexOf('.') !== -1 && !/^\d/.test(trimmed)) {
    const resolved = navigatePath(context, trimmed);
    if (resolved !== undefined && resolved !== null) return Number(resolved);
  }

  // Plain number
  return parseFloat(trimmed);
}

// ---------------------------------------------------------------------------
// Parse a single clause: "left operator right"
// ---------------------------------------------------------------------------

const OPERATORS = ['includes', 'contains', '!=', '==', '>=', '<=', '>', '<'];

function parseClause(clause) {
  const trimmed = clause.trim();
  for (const op of OPERATORS) {
    const idx = trimmed.indexOf(` ${op} `);
    if (idx !== -1) {
      const left = trimmed.substring(0, idx).trim();
      const right = trimmed.substring(idx + op.length + 2).trim().replace(/^'|'$/g, '');
      return { left, operator: op, right };
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// Main: evaluateTrigger
// ---------------------------------------------------------------------------

/**
 * Evaluate a trigger condition string against a context object.
 *
 * Supports: includes, contains, ==, !=, >, >=, <, <=
 * Supports: AND, OR combinators (left-to-right, no precedence)
 * Supports: dot-path navigation for nested properties
 *
 * @param {string} condition - Trigger condition string
 * @param {object} context - Context object with nested properties
 * @returns {boolean} Whether the trigger fires
 */
export function evaluateTrigger(condition, context) {
  if (!condition || typeof condition !== 'string') return false;
  if (!context || typeof context !== 'object') return false;

  try {
    // Split on AND/OR preserving the combinator
    const parts = [];
    const combinators = [];
    // Split by ' AND ' and ' OR '
    const tokens = condition.split(/\s+(AND|OR)\s+/);

    for (let i = 0; i < tokens.length; i++) {
      if (tokens[i] === 'AND' || tokens[i] === 'OR') {
        combinators.push(tokens[i]);
      } else {
        parts.push(tokens[i]);
      }
    }

    if (parts.length === 0) return false;

    // Evaluate first clause
    const firstParsed = parseClause(parts[0]);
    if (!firstParsed) return false;
    let result = evaluateSingle(firstParsed.left, firstParsed.operator, firstParsed.right, context);

    // Apply combinators left-to-right
    for (let i = 0; i < combinators.length; i++) {
      const clauseParsed = parseClause(parts[i + 1]);
      if (!clauseParsed) return false;
      const clauseResult = evaluateSingle(clauseParsed.left, clauseParsed.operator, clauseParsed.right, context);

      if (combinators[i] === 'AND') {
        result = result && clauseResult;
      } else {
        result = result || clauseResult;
      }
    }

    return result;
  } catch {
    // Fail-safe: don't trigger on unparseable conditions
    return false;
  }
}

// ---------------------------------------------------------------------------
// CLI self-test
// ---------------------------------------------------------------------------

function selfTest() {
  console.log('--- trigger-evaluator self-test ---\n');

  const ctx = {
    deal: {
      strategy: 'value-add',
      entitlementRisk: true,
      financing: { ltv: 0.75 },
      dueDiligence: { redFlags: ['environmental-contamination', 'title-issue'] },
      capex: { immediate: 600000, fiveYear: 800000 },
      purchasePrice: 5000000,
      rentRoll: { rollover12Month: 0.30, anchorTenantExpiry: false },
      legal: { insuranceFlags: [], floodZone: 'X', windstormExclusion: false },
    },
    pipeline: { verdict: 'CONDITIONAL' },
    thresholds: { primaryCriteria: { ltv: { maxConditional: 0.50 } } },
  };

  const tests = [
    {
      name: 'Simple equality',
      condition: "deal.strategy == 'value-add'",
      expected: true,
    },
    {
      name: 'Inequality',
      condition: "deal.strategy != 'core'",
      expected: true,
    },
    {
      name: 'Includes (array)',
      condition: "deal.dueDiligence.redFlags includes 'environmental-contamination'",
      expected: true,
    },
    {
      name: 'Includes (array, not present)',
      condition: "deal.dueDiligence.redFlags includes 'flood-risk'",
      expected: false,
    },
    {
      name: 'Numeric greater-than',
      condition: 'deal.financing.ltv > 0.70',
      expected: true,
    },
    {
      name: 'Numeric less-than',
      condition: 'deal.financing.ltv < 0.50',
      expected: false,
    },
    {
      name: 'Numeric with context path RHS',
      condition: 'deal.financing.ltv > thresholds.primaryCriteria.ltv.maxConditional',
      expected: true,
    },
    {
      name: 'AND combinator (both true)',
      condition: "deal.strategy == 'value-add' AND deal.entitlementRisk == true",
      expected: true,
    },
    {
      name: 'AND combinator (one false)',
      condition: "deal.strategy == 'core' AND deal.entitlementRisk == true",
      expected: false,
    },
    {
      name: 'OR combinator (one true)',
      condition: "deal.strategy == 'core' OR deal.entitlementRisk == true",
      expected: true,
    },
    {
      name: 'Nested path navigation',
      condition: 'deal.rentRoll.rollover12Month > 0.25',
      expected: true,
    },
    {
      name: 'Unparseable condition',
      condition: 'this is not a valid condition string',
      expected: false,
    },
    {
      name: 'Arithmetic in RHS',
      condition: 'deal.capex.fiveYear > deal.purchasePrice * 0.10',
      expected: true,
    },
    {
      name: 'Pipeline verdict check',
      condition: "pipeline.verdict == 'CONDITIONAL'",
      expected: true,
    },
  ];

  let passed = 0;
  let failed = 0;

  for (const t of tests) {
    const result = evaluateTrigger(t.condition, ctx);
    const ok = result === t.expected;
    console.log(`  ${ok ? 'PASS' : 'FAIL'}: ${t.name} => ${result} (expected ${t.expected})`);
    if (ok) passed++;
    else failed++;
  }

  console.log(`\nResults: ${passed} passed, ${failed} failed out of ${tests.length}`);
  console.log(`\nSelf-test: ${failed === 0 ? 'PASS' : 'FAIL'}`);
  process.exit(failed === 0 ? 0 : 1);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1] && process.argv.includes('--test')) {
  selfTest();
}
