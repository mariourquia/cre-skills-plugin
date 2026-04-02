#!/usr/bin/env node

/**
 * Handoff Router -- Routes data between orchestrator pipelines using the handoff registry.
 *
 * Export: evaluateHandoffs(fromOrchestrator, pipelineVerdict, pipelineOutput, options)
 * Returns: { handoffs: [{ toOrchestrator, triggerCondition, matched, dataExtracted, dataValid }] }
 *
 * CLI: node handoff-router.mjs --from acquisition --verdict PROCEED [--no-handoff] [--dry-run] [--test]
 *
 * Run with --test to execute self-tests.
 */

import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

// ---------------------------------------------------------------------------
// Resolve plugin root from this file's location or from options
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function resolvePluginRoot(options) {
  return options?.pluginRoot || join(__dirname, '..', '..');
}

// ---------------------------------------------------------------------------
// Load handoff registry
// ---------------------------------------------------------------------------

async function loadRegistry(pluginRoot) {
  const filePath = join(pluginRoot, 'orchestrators', 'engine', 'handoff-registry.json');
  if (!existsSync(filePath)) {
    throw new Error(`Handoff registry not found: ${filePath}`);
  }
  const raw = await readFile(filePath, 'utf-8');
  return JSON.parse(raw);
}

// ---------------------------------------------------------------------------
// Trigger condition evaluator
// ---------------------------------------------------------------------------

function evaluateTriggerCondition(trigger, fromOrchestrator, pipelineVerdict) {
  // Normalize the trigger string for matching.
  // Trigger examples from the registry:
  //   "acquisition.verdict == 'GO' AND closing.status == 'COMPLETED'"
  //   "hold-period.verdict == 'EXIT'"
  //   "underwriting.status == 'COMPLETED' AND underwriting.verdict != 'FAIL'"
  //   "fund.phase.deployment.dealSelected == true"
  //   "research.verdict == 'INVEST'"
  //
  // We match on two signals: the fromOrchestrator name appearing in the trigger,
  // and the pipelineVerdict appearing as a quoted value or boolean.

  const triggerLower = trigger.toLowerCase();
  const verdictLower = pipelineVerdict.toLowerCase();

  // Check if the trigger references our orchestrator (by ID fragment)
  const fromLower = fromOrchestrator.toLowerCase();
  const orchestratorMatch = triggerLower.includes(fromLower);

  // Check if the verdict appears in the trigger as a value
  // Look for patterns like == 'PROCEED', == 'GO', == 'EXIT', == true
  const verdictMatch = triggerLower.includes(`'${verdictLower}'`)
    || triggerLower.includes(`"${verdictLower}"`)
    || triggerLower.includes(`== ${verdictLower}`);

  // Also match common verdict aliases
  const aliasMap = {
    proceed: ['go', 'completed', 'proceed'],
    go: ['proceed', 'go', 'completed'],
    completed: ['proceed', 'go', 'completed'],
    kill: ['fail', 'kill', 'reject'],
    fail: ['kill', 'fail', 'reject'],
    exit: ['exit', 'sell'],
    sell: ['exit', 'sell'],
    invest: ['invest', 'deploy'],
    deploy: ['deploy', 'invest'],
  };

  const aliases = aliasMap[verdictLower] || [verdictLower];
  const aliasMatch = aliases.some(alias =>
    triggerLower.includes(`'${alias}'`) || triggerLower.includes(`"${alias}"`)
  );

  return orchestratorMatch && (verdictMatch || aliasMatch);
}

// ---------------------------------------------------------------------------
// Data extraction and validation against dataContract
// ---------------------------------------------------------------------------

function extractAndValidate(dataContract, pipelineOutput) {
  const extracted = {};
  const missing = [];
  const present = [];

  if (!dataContract) {
    return { extracted, missing, present, valid: true };
  }

  // Check required fields
  if (dataContract.required) {
    for (const [fieldName, spec] of Object.entries(dataContract.required)) {
      const value = navigatePath(pipelineOutput, spec.sourcePath || fieldName);
      if (value !== undefined && value !== null) {
        extracted[fieldName] = value;
        present.push(fieldName);
      } else {
        missing.push(fieldName);
      }
    }
  }

  // Check optional fields (extract if present, do not flag if missing)
  if (dataContract.optional) {
    for (const [fieldName, spec] of Object.entries(dataContract.optional)) {
      const value = navigatePath(pipelineOutput, spec.sourcePath || fieldName);
      if (value !== undefined && value !== null) {
        extracted[fieldName] = value;
        present.push(fieldName);
      }
    }
  }

  const valid = missing.length === 0;
  return { extracted, missing, present, valid };
}

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
// Core: evaluateHandoffs
// ---------------------------------------------------------------------------

export function evaluateHandoffs(fromOrchestrator, pipelineVerdict, pipelineOutput, options = {}) {
  const registry = options._registry; // Injected for testing; otherwise loaded in CLI path
  const noHandoff = options.noHandoff || false;
  const dryRun = options.dryRun || false;

  if (!registry || !registry.handoffs) {
    throw new Error('Handoff registry not loaded. Pass options._registry or use the CLI.');
  }

  const results = [];

  // Filter handoffs where fromOrchestrator matches
  for (const handoff of registry.handoffs) {
    const fromId = handoff.from?.orchestratorId || '';
    const fromMatch = fromId.toLowerCase().includes(fromOrchestrator.toLowerCase());
    if (!fromMatch) continue;

    // Evaluate trigger condition
    const triggered = evaluateTriggerCondition(
      handoff.trigger,
      fromOrchestrator,
      pipelineVerdict
    );

    const toOrchestrator = handoff.to?.orchestratorId || 'unknown';
    const toPhase = handoff.to?.phase || '';

    if (triggered) {
      // Extract and validate data
      const { extracted, missing, present, valid } = extractAndValidate(
        handoff.dataContract,
        pipelineOutput || {}
      );

      const dataFieldCount = Object.keys(extracted).length;

      console.log(`[HANDOFF] ${fromId} -> ${toOrchestrator}: triggered (verdict=${pipelineVerdict})`);

      if (dryRun) {
        console.log(`  [DRY-RUN] Would hand off to ${toOrchestrator} (phase: ${toPhase}) with ${dataFieldCount} data fields`);
        if (missing.length > 0) {
          console.log(`  [DRY-RUN] Missing required fields: ${missing.join(', ')}`);
        }
      } else if (noHandoff) {
        console.log(`  [SKIP] --no-handoff flag set. Dispatch suppressed.`);
      } else {
        console.log(`  [HANDOFF] Would invoke: ${toOrchestrator} (phase: ${toPhase}) with ${dataFieldCount} data fields (dispatch is future work)`);
      }

      results.push({
        id: handoff.id,
        toOrchestrator,
        toPhase,
        triggerCondition: handoff.trigger,
        matched: true,
        dataExtracted: present,
        dataMissing: missing,
        dataValid: valid,
        dataFieldCount,
      });
    } else {
      results.push({
        id: handoff.id,
        toOrchestrator,
        toPhase,
        triggerCondition: handoff.trigger,
        matched: false,
        dataExtracted: [],
        dataMissing: [],
        dataValid: false,
        dataFieldCount: 0,
      });
    }
  }

  return { handoffs: results };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

async function main() {
  const args = process.argv.slice(2);

  const getArg = (flag) => {
    const idx = args.indexOf(flag);
    return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : null;
  };
  const hasFlag = (flag) => args.includes(flag);

  const from = getArg('--from');
  const verdict = getArg('--verdict');
  const noHandoff = hasFlag('--no-handoff');
  const dryRun = hasFlag('--dry-run');
  const testMode = hasFlag('--test');

  if (testMode) {
    await runTests();
    return;
  }

  if (!from || !verdict) {
    console.error('Usage: node handoff-router.mjs --from <orchestrator> --verdict <PROCEED|CONDITIONAL|KILL> [--no-handoff] [--dry-run]');
    console.error('       node handoff-router.mjs --test');
    console.error('');
    console.error('Examples:');
    console.error('  node handoff-router.mjs --from acquisition --verdict PROCEED --dry-run');
    console.error('  node handoff-router.mjs --from hold-period --verdict EXIT');
    console.error('  node handoff-router.mjs --from disposition --verdict SELL --no-handoff');
    process.exit(1);
  }

  const pluginRoot = resolvePluginRoot({});

  try {
    const registry = await loadRegistry(pluginRoot);
    const result = evaluateHandoffs(from, verdict, {}, {
      _registry: registry,
      noHandoff,
      dryRun,
    });

    const triggered = result.handoffs.filter(h => h.matched);
    const skipped = result.handoffs.filter(h => !h.matched);

    console.log(`\n--- Handoff Evaluation ---`);
    console.log(`From:      ${from}`);
    console.log(`Verdict:   ${verdict}`);
    console.log(`Matched:   ${triggered.length}`);
    console.log(`Skipped:   ${skipped.length}`);

    if (triggered.length > 0) {
      console.log('\nTriggered handoffs:');
      for (const h of triggered) {
        console.log(`  ${h.id}: -> ${h.toOrchestrator} (phase: ${h.toPhase}), data valid: ${h.dataValid}, fields: ${h.dataFieldCount}`);
      }
    }
  } catch (err) {
    console.error(`[ERROR] ${err.message}`);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Self-tests (--test flag)
// ---------------------------------------------------------------------------

async function runTests() {
  let passed = 0;
  let failed = 0;

  function assert(condition, label) {
    if (condition) {
      console.log(`  PASS: ${label}`);
      passed++;
    } else {
      console.error(`  FAIL: ${label}`);
      failed++;
    }
  }

  console.log('\n--- handoff-router.mjs self-tests ---\n');

  // Load the real registry
  const pluginRoot = resolvePluginRoot({});
  const registry = await loadRegistry(pluginRoot);

  // Test 1: acquisition -> hold-period handoff with PROCEED/GO verdict
  console.log('Test 1: acquisition-orchestrator with GO verdict');
  {
    const result = evaluateHandoffs('acquisition', 'GO', {}, { _registry: registry, dryRun: true });
    const triggered = result.handoffs.filter(h => h.matched);
    assert(triggered.length >= 1, `At least 1 handoff triggered (got ${triggered.length})`);
    const toHoldPeriod = triggered.find(h => h.toOrchestrator.includes('hold-period'));
    assert(toHoldPeriod !== undefined, 'Handoff to hold-period-orchestrator found');
  }

  // Test 2: hold-period -> disposition handoff with EXIT verdict
  console.log('\nTest 2: hold-period-orchestrator with EXIT verdict');
  {
    const result = evaluateHandoffs('hold-period', 'EXIT', {}, { _registry: registry, dryRun: true });
    const triggered = result.handoffs.filter(h => h.matched);
    assert(triggered.length >= 1, `At least 1 handoff triggered (got ${triggered.length})`);
    const toDispo = triggered.find(h => h.toOrchestrator.includes('disposition'));
    assert(toDispo !== undefined, 'Handoff to disposition-orchestrator found');
  }

  // Test 3: Data extraction from pipeline output
  console.log('\nTest 3: Data extraction and validation');
  {
    const mockOutput = {
      financials: {
        stabilizedNOI: 1200000,
        purchasePrice: 15000000,
      },
      closingDate: '2026-03-15',
    };
    const result = evaluateHandoffs('acquisition', 'GO', mockOutput, { _registry: registry, dryRun: true });
    const toHold = result.handoffs.find(h => h.matched && h.toOrchestrator.includes('hold-period'));
    if (toHold) {
      assert(toHold.dataExtracted.includes('stabilized_noi'), 'stabilized_noi extracted');
      assert(toHold.dataExtracted.includes('purchase_price'), 'purchase_price extracted');
      assert(toHold.dataExtracted.includes('closing_date'), 'closing_date extracted');
      assert(toHold.dataMissing.length > 0, 'Some required fields still missing (incomplete mock)');
    } else {
      console.error('  SKIP: hold-period handoff not triggered');
      failed++;
    }
  }

  // Test 4: No handoffs for unmatched orchestrator
  console.log('\nTest 4: No handoffs for unknown orchestrator');
  {
    const result = evaluateHandoffs('nonexistent-orchestrator', 'PROCEED', {}, { _registry: registry });
    assert(result.handoffs.length === 0, 'No handoffs matched');
  }

  // Test 5: Trigger condition evaluator
  console.log('\nTest 5: Trigger condition evaluation');
  {
    assert(
      evaluateTriggerCondition("acquisition.verdict == 'GO'", 'acquisition', 'GO'),
      "Matches acquisition/GO"
    );
    assert(
      evaluateTriggerCondition("hold-period.verdict == 'EXIT'", 'hold-period', 'EXIT'),
      "Matches hold-period/EXIT"
    );
    assert(
      !evaluateTriggerCondition("acquisition.verdict == 'GO'", 'acquisition', 'KILL'),
      "Does not match acquisition/KILL against GO trigger"
    );
    assert(
      !evaluateTriggerCondition("disposition.verdict == 'SELL'", 'acquisition', 'SELL'),
      "Does not match wrong orchestrator"
    );
  }

  // Summary
  console.log(`\n--- Results: ${passed} passed, ${failed} failed ---`);
  if (failed > 0) process.exit(1);
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

const isMain = process.argv[1] && (
  process.argv[1].endsWith('handoff-router.mjs') ||
  process.argv[1] === fileURLToPath(import.meta.url)
);

if (isMain) {
  main().catch(err => {
    console.error(`[FATAL] ${err.message}`);
    process.exit(1);
  });
}
