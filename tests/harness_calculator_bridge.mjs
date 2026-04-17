#!/usr/bin/env node

/**
 * Test harness for the calculator bridge. Not used in production.
 *
 * Reads --slug and --inputs (JSON) from argv, invokes the bridge,
 * and prints either the bridge-returned JSON (success) or a
 * structured error envelope (failure). The pytest tests shell out
 * to this harness so the bridge's Node code path is exercised for
 * real instead of reimplemented in Python.
 */

import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  invokeCalculator,
  CalculatorBridgeError,
} from '../src/orchestrators/engine/calculator-bridge.mjs';

function parseArgs(argv) {
  const out = { slug: null, inputsJson: '{}' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--slug' && argv[i + 1]) { out.slug = argv[++i]; continue; }
    if (a === '--inputs' && argv[i + 1]) { out.inputsJson = argv[++i]; continue; }
  }
  return out;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.slug) {
    console.error('Usage: harness_calculator_bridge.mjs --slug <slug> --inputs <json>');
    process.exit(2);
  }
  let inputs;
  try {
    inputs = JSON.parse(args.inputsJson);
  } catch (err) {
    console.error(`bad --inputs JSON: ${err.message}`);
    process.exit(2);
  }

  const here = dirname(fileURLToPath(import.meta.url));
  const pluginRoot = resolve(here, '..', 'src');

  try {
    const out = invokeCalculator(args.slug, inputs, { pluginRoot });
    console.log(JSON.stringify({ ok: true, result: out }));
  } catch (err) {
    if (err instanceof CalculatorBridgeError) {
      console.log(JSON.stringify({
        ok: false,
        error_name: err.name,
        message: err.message,
        context: err.context,
      }));
      process.exit(1);
    }
    console.log(JSON.stringify({
      ok: false,
      error_name: err.name || 'Error',
      message: err.message,
    }));
    process.exit(3);
  }
}

main();
