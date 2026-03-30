#!/usr/bin/env node

/**
 * Workflow Executor -- Executes multi-step workflow chains defined in routing/workflows/*.md files.
 *
 * Export: executeWorkflow(workflowName, options)
 * Returns: { workflowId, steps, currentStep, verdict, completed }
 *
 * CLI: node workflow-executor.mjs --workflow deal-pipeline-acquisition [--resume <id>] [--dry-run] [--step <N>] [--test]
 *
 * Run with --test to parse one workflow file, print parsed steps, and verify structure.
 */

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomBytes } from 'node:crypto';

// ---------------------------------------------------------------------------
// Resolve plugin root from this file's location or from options
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function resolvePluginRoot(options) {
  return options?.pluginRoot || join(__dirname, '..', '..');
}

function resolveStateDir() {
  const home = process.env.HOME || process.env.USERPROFILE || '/tmp';
  return join(home, '.cre-skills', 'workflows');
}

function generateWorkflowId() {
  return randomBytes(8).toString('hex');
}

// ---------------------------------------------------------------------------
// Markdown table parser -- extracts step rows from workflow .md files
// ---------------------------------------------------------------------------

function parseMarkdownTable(lines) {
  // Find the header row containing "Step" and "Skill"
  let headerIdx = -1;
  for (let i = 0; i < lines.length; i++) {
    const lower = lines[i].toLowerCase();
    if (lower.includes('|') && lower.includes('step') && lower.includes('skill')) {
      headerIdx = i;
      break;
    }
  }
  if (headerIdx === -1) return [];

  // Parse header columns
  const headerCells = splitTableRow(lines[headerIdx]);
  const colMap = {};
  for (let c = 0; c < headerCells.length; c++) {
    const cell = headerCells[c].toLowerCase().trim();
    if (cell.includes('step')) colMap.step = c;
    else if (cell.includes('skill') && !cell.includes('daily') && !cell.includes('ops')) colMap.skill = c;
    else if (cell.includes('input')) colMap.inputs = c;
    else if (cell.includes('output')) colMap.outputs = c;
    else if (cell.includes('decision') || cell.includes('gate')) colMap.decisionGate = c;
    else if (cell.includes('daily') || cell.includes('ops')) colMap.dailyOps = c;
  }

  // Skip separator row (---|----|---)
  let dataStart = headerIdx + 1;
  if (dataStart < lines.length && /^\s*\|[\s\-:|]+\|\s*$/.test(lines[dataStart])) {
    dataStart++;
  }

  // Parse data rows
  const steps = [];
  for (let i = dataStart; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line.startsWith('|')) break;
    // Skip label-only rows like "| **FINANCING TRACK** |"
    const cells = splitTableRow(line);
    const stepCell = (cells[colMap.step] || '').trim();
    const skillCell = (cells[colMap.skill] || '').trim();
    if (!skillCell || skillCell.startsWith('**')) continue;

    const stepNumber = normalizeStepNumber(stepCell);
    if (stepNumber === null) continue;

    steps.push({
      stepNumber,
      stepRaw: stepCell,
      skillSlug: skillCell,
      inputs: (cells[colMap.inputs] || '').trim(),
      outputs: (cells[colMap.outputs] || '').trim(),
      decisionGate: (cells[colMap.decisionGate] || '').trim(),
      dailyOps: (cells[colMap.dailyOps] || '').trim(),
      parallelWith: null,
    });
  }

  // Detect parallel steps (e.g., 4a/4b, 2a/2b/2c, 12a/12b/12c, 13a/13b)
  detectParallelSteps(steps);

  return steps;
}

function splitTableRow(line) {
  // Split "|col1|col2|col3|" into ["col1", "col2", "col3"]
  const trimmed = line.trim();
  const inner = trimmed.startsWith('|') ? trimmed.slice(1) : trimmed;
  const withoutTrailing = inner.endsWith('|') ? inner.slice(0, -1) : inner;
  return withoutTrailing.split('|').map(s => s.trim());
}

function normalizeStepNumber(raw) {
  if (!raw) return null;
  const cleaned = raw.replace(/\*\*/g, '').trim();
  // Match patterns: "1", "4a", "12b", "13a"
  const match = cleaned.match(/^(\d+)([a-z]?)$/);
  if (!match) return null;
  return cleaned;
}

function detectParallelSteps(steps) {
  // Group steps by their numeric prefix
  const groups = {};
  for (const step of steps) {
    const match = step.stepNumber.match(/^(\d+)([a-z])$/);
    if (match) {
      const base = match[1];
      if (!groups[base]) groups[base] = [];
      groups[base].push(step);
    }
  }

  // Mark parallel siblings
  for (const [, group] of Object.entries(groups)) {
    if (group.length > 1) {
      const siblings = group.map(s => s.stepNumber);
      for (const step of group) {
        step.parallelWith = siblings.filter(s => s !== step.stepNumber);
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Parse workflow header (name and description)
// ---------------------------------------------------------------------------

function parseWorkflowHeader(lines) {
  let name = '';
  let description = '';
  for (const line of lines) {
    if (line.startsWith('# ') && !name) {
      name = line.replace(/^#+\s*/, '').replace(/^Workflow Chain:\s*/i, '').trim();
    } else if (line.startsWith('## Purpose')) {
      // Next non-empty line is the description
      const idx = lines.indexOf(line);
      for (let j = idx + 1; j < lines.length; j++) {
        if (lines[j].trim()) {
          description = lines[j].trim();
          break;
        }
      }
      break;
    }
  }
  return { name, description };
}

// ---------------------------------------------------------------------------
// Build dependency graph
// ---------------------------------------------------------------------------

function buildDependencyGraph(steps) {
  const deps = {};
  const stepNumbers = steps.map(s => s.stepNumber);

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const current = step.stepNumber;
    deps[current] = [];

    if (i === 0) continue;

    // For parallel steps like 4a, they depend on the previous non-parallel step
    const currentMatch = current.match(/^(\d+)([a-z])$/);
    if (currentMatch) {
      const base = parseInt(currentMatch[1], 10);
      // Depend on the step just before this parallel group
      const prevBase = String(base - 1);
      // Find the highest sub-step of (base-1) or just (base-1) itself
      const candidates = stepNumbers.filter(s => {
        const m = s.match(/^(\d+)([a-z]?)$/);
        return m && parseInt(m[1], 10) === base - 1;
      });
      if (candidates.length > 0) {
        // For parallel steps, depend on all variants of the previous step
        // (or just the single previous step if no variants)
        deps[current] = [...candidates];
      }
    } else {
      // Sequential step: depends on previous step(s)
      const currentNum = parseInt(current, 10);
      const prevNum = currentNum - 1;
      // Find all steps with the previous number (could be parallel: 4a, 4b)
      const candidates = stepNumbers.filter(s => {
        const m = s.match(/^(\d+)([a-z]?)$/);
        return m && parseInt(m[1], 10) === prevNum;
      });
      if (candidates.length > 0) {
        deps[current] = [...candidates];
      }
    }
  }

  return deps;
}

// ---------------------------------------------------------------------------
// Topological sort for execution order
// ---------------------------------------------------------------------------

function topologicalSort(steps, deps) {
  const sorted = [];
  const visited = new Set();
  const visiting = new Set();
  const stepMap = {};
  for (const step of steps) {
    stepMap[step.stepNumber] = step;
  }

  function visit(num) {
    if (visited.has(num)) return;
    if (visiting.has(num)) return; // cycle guard
    visiting.add(num);
    for (const dep of (deps[num] || [])) {
      visit(dep);
    }
    visiting.delete(num);
    visited.add(num);
    if (stepMap[num]) sorted.push(stepMap[num]);
  }

  for (const step of steps) {
    visit(step.stepNumber);
  }

  return sorted;
}

// ---------------------------------------------------------------------------
// Checkpoint I/O
// ---------------------------------------------------------------------------

async function ensureDir(dir) {
  if (!existsSync(dir)) {
    await mkdir(dir, { recursive: true });
  }
}

async function writeCheckpoint(stateDir, workflowId, stepNumber, data) {
  const dir = join(stateDir, workflowId);
  await ensureDir(dir);
  const filePath = join(dir, `step${stepNumber}.json`);
  await writeFile(filePath, JSON.stringify(data, null, 2), 'utf-8');
}

async function writeState(stateDir, workflowId, state) {
  const dir = join(stateDir, workflowId);
  await ensureDir(dir);
  const filePath = join(dir, 'state.json');
  await writeFile(filePath, JSON.stringify(state, null, 2), 'utf-8');
}

async function readState(stateDir, workflowId) {
  const filePath = join(stateDir, workflowId, 'state.json');
  if (!existsSync(filePath)) return null;
  const raw = await readFile(filePath, 'utf-8');
  return JSON.parse(raw);
}

async function readCheckpoint(stateDir, workflowId, stepNumber) {
  const filePath = join(stateDir, workflowId, `step${stepNumber}.json`);
  if (!existsSync(filePath)) return null;
  const raw = await readFile(filePath, 'utf-8');
  return JSON.parse(raw);
}

// ---------------------------------------------------------------------------
// Core: parseWorkflowFile
// ---------------------------------------------------------------------------

async function parseWorkflowFile(workflowName, pluginRoot) {
  const filePath = join(pluginRoot, 'routing', 'workflows', `${workflowName}.md`);
  if (!existsSync(filePath)) {
    throw new Error(`Workflow file not found: ${filePath}`);
  }

  const content = await readFile(filePath, 'utf-8');
  const lines = content.split('\n');
  const header = parseWorkflowHeader(lines);
  const steps = parseMarkdownTable(lines);
  const deps = buildDependencyGraph(steps);
  const sorted = topologicalSort(steps, deps);

  return {
    name: header.name,
    description: header.description,
    steps: sorted,
    dependencies: deps,
    filePath,
  };
}

// ---------------------------------------------------------------------------
// Core: executeWorkflow
// ---------------------------------------------------------------------------

export async function executeWorkflow(workflowName, options = {}) {
  const pluginRoot = resolvePluginRoot(options);
  const stateDir = resolveStateDir();
  const dryRun = options.dryRun || false;
  const startStep = options.startStep || null;

  // Parse the workflow
  const workflow = await parseWorkflowFile(workflowName, pluginRoot);

  if (workflow.steps.length === 0) {
    throw new Error(`No steps found in workflow: ${workflowName}`);
  }

  // Dry run: print and exit
  if (dryRun) {
    return printDryRun(workflow);
  }

  // Resume or start fresh
  let workflowId;
  let existingState = null;
  const completedSteps = new Set();

  if (options.resume) {
    workflowId = options.resume;
    existingState = await readState(stateDir, workflowId);
    if (!existingState) {
      throw new Error(`No state found for workflow ID: ${workflowId}`);
    }
    // Populate completed steps from saved state
    for (const s of existingState.steps) {
      if (s.status === 'completed') {
        completedSteps.add(s.stepNumber);
      }
    }
    console.log(`[RESUME] Resuming workflow ${workflowId} from step ${existingState.currentStep}`);
  } else {
    workflowId = generateWorkflowId();
  }

  // Build state
  const state = existingState || {
    workflowName,
    workflowId,
    startedAt: new Date().toISOString(),
    steps: workflow.steps.map(s => ({
      stepNumber: s.stepNumber,
      skill: s.skillSlug,
      status: 'pending',
      verdict: null,
    })),
    currentStep: workflow.steps[0].stepNumber,
    overallVerdict: null,
  };

  // Execute steps in topological order
  let halted = false;
  let haltVerdict = null;

  for (const step of workflow.steps) {
    // Skip completed steps (resume path)
    if (completedSteps.has(step.stepNumber)) {
      continue;
    }

    // Skip steps before startStep if specified
    if (startStep && !hasReachedStep(step.stepNumber, startStep, workflow.steps)) {
      continue;
    }

    // Update current step
    state.currentStep = step.stepNumber;
    const stepState = state.steps.find(s => s.stepNumber === step.stepNumber);

    // Log step invocation
    console.log(`[STEP ${step.stepNumber}] Invoking: ${step.skillSlug}`);

    // Stub skill dispatch
    const inputSummary = step.inputs ? step.inputs.slice(0, 120) : '(no inputs specified)';
    console.log(`  DISPATCH: /${step.skillSlug} with inputs: ${inputSummary}`);

    // Handle parallel steps (stub: sequential execution, log parallel intent)
    if (step.parallelWith && step.parallelWith.length > 0) {
      console.log(`  PARALLEL: Would execute concurrently with step(s) ${step.parallelWith.join(', ')}`);
    }

    // Generate placeholder output
    const stepOutput = {
      stepNumber: step.stepNumber,
      skill: step.skillSlug,
      dispatchedAt: new Date().toISOString(),
      completedAt: new Date().toISOString(),
      output: `[PLACEHOLDER] Output from ${step.skillSlug}`,
      verdict: null,
    };

    // Evaluate decision gate
    if (step.decisionGate && step.decisionGate !== 'None' && !step.decisionGate.toLowerCase().startsWith('none')) {
      console.log(`  [GATE] ${step.skillSlug} decision gate: ${step.decisionGate}`);

      // Check for KILL/KEEP language
      const gateText = step.decisionGate.toLowerCase();
      const hasKill = gateText.includes('kill');
      const hasKeep = gateText.includes('keep');

      if (hasKill || hasKeep) {
        // Stub: default to KEEP (actual user interaction is future work)
        stepOutput.verdict = 'KEEP';
        console.log(`  [GATE] Stub verdict: KEEP (user interaction is future work)`);
      } else {
        // Soft gate or advisory -- continue
        stepOutput.verdict = 'PROCEED';
        console.log(`  [GATE] Advisory gate noted. Proceeding.`);
      }

      // If verdict were KILL, halt the workflow
      if (stepOutput.verdict === 'KILL') {
        halted = true;
        haltVerdict = 'KILL';
        if (stepState) {
          stepState.status = 'killed';
          stepState.verdict = 'KILL';
        }

        // Write checkpoint
        await writeCheckpoint(stateDir, workflowId, step.stepNumber, stepOutput);
        state.overallVerdict = 'KILL';
        await writeState(stateDir, workflowId, state);

        console.log(`  [HALT] Workflow halted at step ${step.stepNumber}. Verdict: KILL`);
        break;
      }
    }

    // Mark step completed
    if (stepState) {
      stepState.status = 'completed';
      stepState.verdict = stepOutput.verdict || 'COMPLETED';
    }
    completedSteps.add(step.stepNumber);

    // Write checkpoint
    await writeCheckpoint(stateDir, workflowId, step.stepNumber, stepOutput);
    await writeState(stateDir, workflowId, state);
  }

  // Final state
  const allCompleted = state.steps.every(s => s.status === 'completed');
  if (allCompleted && !halted) {
    state.overallVerdict = 'COMPLETED';
  }
  state.completedAt = allCompleted || halted ? new Date().toISOString() : null;
  await writeState(stateDir, workflowId, state);

  return {
    workflowId,
    steps: state.steps,
    currentStep: state.currentStep,
    verdict: state.overallVerdict,
    completed: allCompleted,
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function hasReachedStep(current, target, steps) {
  const currentIdx = steps.findIndex(s => s.stepNumber === current);
  const targetIdx = steps.findIndex(s => s.stepNumber === target);
  return currentIdx >= targetIdx;
}

function printDryRun(workflow) {
  console.log(`\n=== WORKFLOW: ${workflow.name} ===`);
  console.log(`Description: ${workflow.description}`);
  console.log(`Steps: ${workflow.steps.length}`);
  console.log(`Source: ${workflow.filePath}\n`);

  console.log('Step | Skill                              | Gate                    | Parallel | Dependencies');
  console.log('-----|------------------------------------|--------------------------|---------|--------------');

  for (const step of workflow.steps) {
    const gate = step.decisionGate
      ? (step.decisionGate.length > 24 ? step.decisionGate.slice(0, 21) + '...' : step.decisionGate)
      : '--';
    const parallel = step.parallelWith ? step.parallelWith.join(',') : '--';
    const deps = (workflow.dependencies[step.stepNumber] || []).join(',') || '--';
    const skill = step.skillSlug.length > 36
      ? step.skillSlug.slice(0, 33) + '...'
      : step.skillSlug;

    console.log(
      `${step.stepNumber.padEnd(5)}| ${skill.padEnd(37)}| ${gate.padEnd(25)}| ${parallel.padEnd(8)}| ${deps}`
    );
  }

  console.log('');

  return {
    workflowId: null,
    steps: workflow.steps.map(s => ({
      stepNumber: s.stepNumber,
      skill: s.skillSlug,
      status: 'dry-run',
      verdict: null,
    })),
    currentStep: null,
    verdict: null,
    completed: false,
  };
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

  const workflowName = getArg('--workflow');
  const resume = getArg('--resume');
  const dryRun = hasFlag('--dry-run');
  const startStep = getArg('--step');
  const testMode = hasFlag('--test');

  if (testMode) {
    await runTests();
    return;
  }

  if (!workflowName) {
    console.error('Usage: node workflow-executor.mjs --workflow <name> [--resume <id>] [--dry-run] [--step <N>]');
    console.error('       node workflow-executor.mjs --test');
    console.error('');
    console.error('Examples:');
    console.error('  node workflow-executor.mjs --workflow deal-pipeline-acquisition --dry-run');
    console.error('  node workflow-executor.mjs --workflow capital-stack-assembly');
    console.error('  node workflow-executor.mjs --workflow deal-pipeline-acquisition --resume abc123def456');
    process.exit(1);
  }

  try {
    const result = await executeWorkflow(workflowName, {
      dryRun,
      resume,
      startStep,
    });

    if (!dryRun) {
      console.log('\n--- Workflow Result ---');
      console.log(`ID:        ${result.workflowId}`);
      console.log(`Verdict:   ${result.verdict || 'IN_PROGRESS'}`);
      console.log(`Completed: ${result.completed}`);
      console.log(`Steps:     ${result.steps.length}`);
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
  const pluginRoot = resolvePluginRoot({});
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

  console.log('\n--- workflow-executor.mjs self-tests ---\n');

  // Test 1: Parse deal-pipeline-acquisition workflow
  console.log('Test 1: Parse deal-pipeline-acquisition');
  try {
    const workflow = await parseWorkflowFile('deal-pipeline-acquisition', pluginRoot);
    assert(workflow.name.length > 0, 'Workflow name parsed');
    assert(workflow.steps.length > 10, `Found ${workflow.steps.length} steps (expected >10)`);
    assert(workflow.steps[0].skillSlug === 'sourcing-outreach-system', `First skill is sourcing-outreach-system`);
    assert(workflow.steps[1].skillSlug === 'deal-quick-screen', `Second skill is deal-quick-screen`);

    // Check parallel detection (12a/12b/12c are the financing track parallel steps)
    const step12a = workflow.steps.find(s => s.stepNumber === '12a');
    const step12b = workflow.steps.find(s => s.stepNumber === '12b');
    assert(step12a !== undefined, 'Found parallel step 12a');
    assert(step12a && step12a.parallelWith && step12a.parallelWith.includes('12b'), 'Step 12a is parallel with 12b');
    assert(step12b !== undefined, 'Found parallel step 12b');

    // Check dependency graph
    assert(Object.keys(workflow.dependencies).length === workflow.steps.length, 'Dependency graph covers all steps');

    // Check a decision gate
    const screen = workflow.steps.find(s => s.skillSlug === 'deal-quick-screen');
    assert(screen && screen.decisionGate.includes('KILL'), 'deal-quick-screen has KILL gate');
  } catch (err) {
    console.error(`  ERROR: ${err.message}`);
    failed++;
  }

  // Test 2: Parse capital-stack-assembly workflow
  console.log('\nTest 2: Parse capital-stack-assembly');
  try {
    const workflow = await parseWorkflowFile('capital-stack-assembly', pluginRoot);
    assert(workflow.name.length > 0, 'Workflow name parsed');
    assert(workflow.steps.length >= 4, `Found ${workflow.steps.length} steps (expected >=4)`);

    // Check parallel steps 2a/2b/2c
    const step2a = workflow.steps.find(s => s.stepNumber === '2a');
    const step2b = workflow.steps.find(s => s.stepNumber === '2b');
    assert(step2a !== undefined, 'Found parallel step 2a');
    assert(step2b !== undefined, 'Found parallel step 2b');
    assert(
      step2a && step2a.parallelWith && step2a.parallelWith.includes('2b'),
      'Step 2a is parallel with 2b'
    );
  } catch (err) {
    console.error(`  ERROR: ${err.message}`);
    failed++;
  }

  // Test 3: Table parser edge cases
  console.log('\nTest 3: Table parser edge cases');
  const testLines = [
    '| Step | Skill | Inputs | Outputs | Decision Gate |',
    '|------|-------|--------|---------|---------------|',
    '| 1 | skill-a | some inputs | some outputs | None |',
    '| **LABEL** | | | | |',
    '| 2 | skill-b | more inputs | more outputs | KILL if bad |',
  ];
  const parsed = parseMarkdownTable(testLines);
  assert(parsed.length === 2, `Parsed 2 data rows (skipped label row)`);
  assert(parsed[0].skillSlug === 'skill-a', 'First skill parsed');
  assert(parsed[1].decisionGate.includes('KILL'), 'Decision gate parsed');

  // Summary
  console.log(`\n--- Results: ${passed} passed, ${failed} failed ---`);
  if (failed > 0) process.exit(1);
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

const isMain = process.argv[1] && (
  process.argv[1].endsWith('workflow-executor.mjs') ||
  process.argv[1] === fileURLToPath(import.meta.url)
);

if (isMain) {
  main().catch(err => {
    console.error(`[FATAL] ${err.message}`);
    process.exit(1);
  });
}
