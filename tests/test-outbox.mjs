#!/usr/bin/env node

/**
 * Outbox module tests -- Zero-dependency test suite for feedback-outbox.mjs.
 *
 * Tests: enqueue, pending, drain (success, failure, eviction, empty, timeout).
 * Uses a temp directory to avoid touching real ~/.cre-skills/.
 *
 * Run: node tests/test-outbox.mjs
 */

import { mkdirSync, readFileSync, writeFileSync, rmSync, existsSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { randomUUID } from 'crypto';

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
// Temp directory setup -- override CONFIG_DIR before importing the module
// ---------------------------------------------------------------------------

const TEMP_DIR = join(tmpdir(), `cre-outbox-test-${randomUUID().slice(0, 8)}`);
mkdirSync(TEMP_DIR, { recursive: true });
const OUTBOX_PATH = join(TEMP_DIR, 'outbox.jsonl');

// Read the module source and create a patched version in temp
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ROOT = resolve(__dirname, '..');
const originalSource = readFileSync(join(PLUGIN_ROOT, 'hooks', 'feedback-outbox.mjs'), 'utf8');

// Replace the CONFIG_DIR and OUTBOX_PATH with our temp paths
const patchedSource = originalSource
  .replace(
    "const CONFIG_DIR = join(homedir(), '.cre-skills');",
    `const CONFIG_DIR = ${JSON.stringify(TEMP_DIR)};`
  )
  .replace(
    "const OUTBOX_PATH = join(CONFIG_DIR, 'outbox.jsonl');",
    `const OUTBOX_PATH = ${JSON.stringify(OUTBOX_PATH)};`
  );

const patchedPath = join(TEMP_DIR, 'feedback-outbox-test.mjs');
writeFileSync(patchedPath, patchedSource, 'utf8');

const { enqueue, drain, pending } = await import(patchedPath);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function resetOutbox() {
  if (existsSync(OUTBOX_PATH)) {
    writeFileSync(OUTBOX_PATH, '', 'utf8');
  }
}

function readOutboxEntries() {
  try {
    return readFileSync(OUTBOX_PATH, 'utf8')
      .split('\n')
      .filter(l => l.trim())
      .map(l => JSON.parse(l));
  } catch {
    return [];
  }
}

function makeFeedback(id) {
  return {
    submission_id: `fb_test${id}`,
    submission_type: 'general',
    timestamp: new Date().toISOString(),
    plugin_version: '4.0.0',
    message: `Test feedback ${id}`,
  };
}

// ---------------------------------------------------------------------------
// 1. enqueue tests
// ---------------------------------------------------------------------------

function testEnqueue() {
  console.log('\n--- enqueue ---');
  resetOutbox();

  enqueue(makeFeedback('001'));
  const entries = readOutboxEntries();

  assert('enqueue', 'creates one entry', entries.length === 1);
  assert('enqueue', 'preserves submission_id', entries[0].submission_id === 'fb_test001');
  assert('enqueue', 'adds _outbox metadata', entries[0]._outbox != null);
  assert('enqueue', 'attempts starts at 0', entries[0]._outbox.attempts === 0);
  assert('enqueue', 'queued_at is set', typeof entries[0]._outbox.queued_at === 'string');
  assert('enqueue', 'last_attempt_at is null', entries[0]._outbox.last_attempt_at === null);

  // Enqueue a second entry
  enqueue(makeFeedback('002'));
  const entries2 = readOutboxEntries();
  assert('enqueue', 'appends (now 2 entries)', entries2.length === 2);
  assert('enqueue', 'second entry preserved', entries2[1].submission_id === 'fb_test002');
}

// ---------------------------------------------------------------------------
// 2. pending tests
// ---------------------------------------------------------------------------

function testPending() {
  console.log('\n--- pending ---');
  resetOutbox();

  assert('pending', 'empty outbox returns 0', pending() === 0);

  enqueue(makeFeedback('p1'));
  assert('pending', 'one entry returns 1', pending() === 1);

  enqueue(makeFeedback('p2'));
  enqueue(makeFeedback('p3'));
  assert('pending', 'three entries returns 3', pending() === 3);
}

// ---------------------------------------------------------------------------
// 3. drain tests -- mock fetch via globalThis
// ---------------------------------------------------------------------------

async function testDrainSuccess() {
  console.log('\n--- drain (all succeed) ---');
  resetOutbox();

  enqueue(makeFeedback('d1'));
  enqueue(makeFeedback('d2'));

  const origFetch = globalThis.fetch;
  globalThis.fetch = async () => ({ ok: true, status: 200 });

  const result = await drain('https://example.com/api/feedback');

  globalThis.fetch = origFetch;

  assert('drain-success', 'sent count is 2', result.sent === 2);
  assert('drain-success', 'failed count is 0', result.failed === 0);
  assert('drain-success', 'evicted count is 0', result.evicted === 0);
  assert('drain-success', 'outbox is empty after', pending() === 0);
}

async function testDrainFailure() {
  console.log('\n--- drain (all fail) ---');
  resetOutbox();

  enqueue(makeFeedback('f1'));

  const origFetch = globalThis.fetch;
  globalThis.fetch = async () => ({ ok: false, status: 500 });

  const result = await drain('https://example.com/api/feedback');

  globalThis.fetch = origFetch;

  assert('drain-failure', 'sent count is 0', result.sent === 0);
  assert('drain-failure', 'failed count is 1', result.failed === 1);
  assert('drain-failure', 'outbox still has 1 entry', pending() === 1);

  const entries = readOutboxEntries();
  assert('drain-failure', 'attempts bumped to 1', entries[0]._outbox.attempts === 1);
  assert('drain-failure', 'last_attempt_at is set', entries[0]._outbox.last_attempt_at != null);
}

async function testDrainEviction() {
  console.log('\n--- drain (eviction after max attempts) ---');
  resetOutbox();

  const entry = {
    ...makeFeedback('e1'),
    _outbox: { queued_at: new Date().toISOString(), attempts: 5, last_attempt_at: null },
  };
  writeFileSync(OUTBOX_PATH, JSON.stringify(entry) + '\n', 'utf8');

  const origFetch = globalThis.fetch;
  globalThis.fetch = async () => ({ ok: false, status: 500 });

  const result = await drain('https://example.com/api/feedback');

  globalThis.fetch = origFetch;

  assert('drain-eviction', 'evicted count is 1', result.evicted === 1);
  assert('drain-eviction', 'sent count is 0', result.sent === 0);
  assert('drain-eviction', 'failed count is 0', result.failed === 0);
  assert('drain-eviction', 'outbox is empty after eviction', pending() === 0);
}

async function testDrainEmpty() {
  console.log('\n--- drain (empty outbox) ---');
  resetOutbox();

  const result = await drain('https://example.com/api/feedback');

  assert('drain-empty', 'sent is 0', result.sent === 0);
  assert('drain-empty', 'failed is 0', result.failed === 0);
  assert('drain-empty', 'evicted is 0', result.evicted === 0);
}

async function testDrainNetworkError() {
  console.log('\n--- drain (network error / throw) ---');
  resetOutbox();

  enqueue(makeFeedback('n1'));

  const origFetch = globalThis.fetch;
  globalThis.fetch = async () => { throw new Error('ECONNREFUSED'); };

  const result = await drain('https://example.com/api/feedback');

  globalThis.fetch = origFetch;

  assert('drain-network', 'sent is 0', result.sent === 0);
  assert('drain-network', 'failed is 1', result.failed === 1);

  const entries = readOutboxEntries();
  assert('drain-network', 'attempts bumped to 1', entries[0]._outbox.attempts === 1);
}

async function testDrainMixed() {
  console.log('\n--- drain (mixed: 1 success, 1 fail, 1 evict) ---');
  resetOutbox();

  enqueue(makeFeedback('m1'));
  enqueue(makeFeedback('m2'));

  const evictEntry = {
    ...makeFeedback('m3'),
    _outbox: { queued_at: new Date().toISOString(), attempts: 5, last_attempt_at: null },
  };
  const existing = readFileSync(OUTBOX_PATH, 'utf8');
  writeFileSync(OUTBOX_PATH, existing + JSON.stringify(evictEntry) + '\n', 'utf8');

  let callCount = 0;
  const origFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    callCount++;
    if (callCount === 1) return { ok: true, status: 200 };
    return { ok: false, status: 503 };
  };

  const result = await drain('https://example.com/api/feedback');

  globalThis.fetch = origFetch;

  assert('drain-mixed', 'sent is 1', result.sent === 1);
  assert('drain-mixed', 'failed is 1', result.failed === 1);
  assert('drain-mixed', 'evicted is 1', result.evicted === 1);
  assert('drain-mixed', 'outbox has 1 remaining', pending() === 1);
}

// ---------------------------------------------------------------------------
// Run all tests
// ---------------------------------------------------------------------------

testEnqueue();
testPending();
await testDrainSuccess();
await testDrainFailure();
await testDrainEviction();
await testDrainEmpty();
await testDrainNetworkError();
await testDrainMixed();

// Cleanup
rmSync(TEMP_DIR, { recursive: true, force: true });

// Summary
console.log(`\n${'='.repeat(50)}`);
console.log(`TOTAL: ${totalPass} passed, ${totalFail} failed`);
if (failedTests.length > 0) {
  console.log('\nFailed tests:');
  for (const t of failedTests) console.log(`  - ${t}`);
  process.exit(1);
}
