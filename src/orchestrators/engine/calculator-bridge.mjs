/**
 * calculator-bridge.mjs
 *
 * Thin bridge that lets orchestrator phases invoke calculators via
 * `scripts/calculator-invoker.py` without the operator shelling out.
 * See docs/orchestrator-v0-design.md section 3.
 *
 * Design constraints:
 *  - Zero runtime dependencies in Node. Calls Python via child_process.
 *  - Python3 must be discoverable as `python3` on PATH (consistent with
 *    the rest of the plugin's scripts/*.py tooling).
 *  - Bridge does NOT validate calculator-specific inputs — the
 *    invoker is the schema source of truth. Bridge surfaces whatever
 *    the invoker returns (including validation_errors).
 */

import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SLUG_RE = /^[a-z][a-z0-9_]{0,64}$/;

export class CalculatorBridgeError extends Error {
  constructor(message, context = {}) {
    super(message);
    this.name = 'CalculatorBridgeError';
    this.context = context;
  }
}

function locateInvoker(pluginRoot) {
  // pluginRoot resolved by executor.resolvePluginRoot points at the
  // directory containing `orchestrators/`. scripts/ is its sibling, so
  // we walk up one.
  const candidates = [
    join(pluginRoot, '..', 'scripts', 'calculator-invoker.py'),
    join(pluginRoot, 'scripts', 'calculator-invoker.py'),
  ];
  for (const c of candidates) {
    if (existsSync(c)) return c;
  }
  throw new CalculatorBridgeError(
    'calculator-invoker.py not found relative to plugin root',
    { pluginRoot, candidates },
  );
}

function locateRegistry(pluginRoot) {
  const candidates = [
    join(pluginRoot, '..', 'scripts', 'calculator-registry.json'),
    join(pluginRoot, 'scripts', 'calculator-registry.json'),
  ];
  for (const c of candidates) {
    if (existsSync(c)) return c;
  }
  throw new CalculatorBridgeError(
    'calculator-registry.json not found relative to plugin root',
    { pluginRoot, candidates },
  );
}

/**
 * Invoke a single calculator. Returns the parsed JSON output on
 * success. Throws CalculatorBridgeError with structured `context` on
 * failure (invoker crash, non-zero exit, unparseable stdout,
 * validation errors surfaced by the invoker itself).
 */
export function invokeCalculator(slug, inputs, options = {}) {
  if (!SLUG_RE.test(slug)) {
    throw new CalculatorBridgeError(
      `calculator slug "${slug}" does not match ${SLUG_RE}`,
    );
  }
  const pluginRoot = options.pluginRoot;
  if (!pluginRoot) {
    throw new CalculatorBridgeError('invokeCalculator requires options.pluginRoot');
  }
  const invoker = locateInvoker(pluginRoot);
  const python = process.env.CRE_SKILLS_PYTHON || 'python3';

  const spawnResult = spawnSync(
    python,
    [invoker, slug, '--json', JSON.stringify(inputs || {})],
    { encoding: 'utf-8' },
  );
  if (spawnResult.error) {
    throw new CalculatorBridgeError(
      `failed to spawn python for calculator "${slug}": ${spawnResult.error.message}`,
      { slug, spawnError: String(spawnResult.error) },
    );
  }
  const stdout = spawnResult.stdout || '';
  const stderr = spawnResult.stderr || '';
  let parsed = null;
  try {
    parsed = stdout.trim() ? JSON.parse(stdout) : null;
  } catch (err) {
    throw new CalculatorBridgeError(
      `calculator "${slug}" returned unparseable stdout`,
      { slug, stdout, stderr, exitCode: spawnResult.status },
    );
  }
  // Check calculator-invoker's structured failure envelopes BEFORE
  // the generic non-zero-exit path. The invoker exits 1 on validation
  // errors and on unknown calculators, but carries a richer payload
  // on stdout that callers should see.
  if (parsed && typeof parsed === 'object' && Array.isArray(parsed.validation_errors)) {
    throw new CalculatorBridgeError(
      `calculator "${slug}" validation errors: ${parsed.validation_errors.join('; ')}`,
      { slug, validation_errors: parsed.validation_errors },
    );
  }
  if (parsed && typeof parsed === 'object' && parsed.error) {
    throw new CalculatorBridgeError(
      `calculator "${slug}" reported error: ${parsed.error}`,
      { slug, error: parsed.error, available: parsed.available },
    );
  }
  if (spawnResult.status !== 0) {
    throw new CalculatorBridgeError(
      `calculator "${slug}" exited ${spawnResult.status}`,
      { slug, stdout: parsed, stderr, exitCode: spawnResult.status },
    );
  }
  return parsed;
}

/**
 * Execute every `tool_calls` entry declared on a phase config. Shape:
 *   phase.tool_calls = [{ tool: "quick_screen", inputs: {...}, as?: "screen" }, ...]
 *
 * Returns { results, errors } where `results` is keyed by the `as`
 * alias (falling back to `tool`) and `errors` is a (possibly empty)
 * array of per-call CalculatorBridgeError objects.
 */
export function invokeToolCalls(phase, options = {}) {
  const calls = phase.tool_calls || [];
  const results = {};
  const errors = [];
  for (const call of calls) {
    const alias = call.as || call.tool;
    try {
      results[alias] = invokeCalculator(call.tool, call.inputs || {}, options);
    } catch (err) {
      errors.push({ alias, call, error: err });
    }
  }
  return { results, errors };
}

/**
 * Return the set of known calculator slugs (for dry-run + diagnostics).
 */
export function listKnownCalculators(pluginRoot) {
  const reg = JSON.parse(readFileSync(locateRegistry(pluginRoot), 'utf-8'));
  return Object.keys(reg.calculators || {}).sort();
}
