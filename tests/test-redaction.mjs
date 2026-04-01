#!/usr/bin/env node

/**
 * Redaction utility tests -- Zero-dependency test suite for scripts/redact-feedback.mjs.
 *
 * Run: node tests/test-redaction.mjs
 */

import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ROOT = resolve(__dirname, '..');

const { redactText, redactSubmission } = await import(
  join(PLUGIN_ROOT, 'scripts', 'redact-feedback.mjs')
);

// ---------------------------------------------------------------------------
// Test harness (same pattern as test-engine.mjs)
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
// 1. redactText -- file paths
// ---------------------------------------------------------------------------

function testRedactPaths() {
  console.log('\n--- redactText: file paths ---');

  assert('paths', 'unix home path',
    redactText('Error at /Users/mario/project/src/app.ts') ===
    'Error at [PATH_REDACTED]');

  assert('paths', 'linux home path',
    redactText('File /home/ubuntu/.config/settings.json missing') ===
    'File [PATH_REDACTED] missing');

  assert('paths', 'tilde path',
    redactText('Config at ~/.cre-skills/config.json') ===
    'Config at [PATH_REDACTED]');

  assert('paths', 'windows path',
    redactText('Found at C:\\Users\\mario\\Documents\\deal.xlsx') ===
    'Found at [PATH_REDACTED]');

  assert('paths', 'var path',
    redactText('Log at /var/log/syslog') ===
    'Log at [PATH_REDACTED]');

  assert('paths', 'preserves non-path slashes',
    redactText('ratio is 10/15') === 'ratio is 10/15');
}

// ---------------------------------------------------------------------------
// 2. redactText -- email addresses
// ---------------------------------------------------------------------------

function testRedactEmails() {
  console.log('\n--- redactText: email addresses ---');

  assert('emails', 'standard email',
    redactText('Contact alice@example.com for details') ===
    'Contact [EMAIL_REDACTED] for details');

  assert('emails', 'email with dots and plus',
    redactText('Sent to user.name+tag@domain.co.uk') ===
    'Sent to [EMAIL_REDACTED]');

  assert('emails', 'no false positive on @ in code',
    redactText('use @property decorator').includes('@property'));
}

// ---------------------------------------------------------------------------
// 3. redactText -- digit sequences
// ---------------------------------------------------------------------------

function testRedactDigits() {
  console.log('\n--- redactText: digit sequences ---');

  assert('digits', '5+ digit sequence',
    redactText('Account 123456789 was affected') ===
    'Account [NUM_REDACTED] was affected');

  assert('digits', 'SSN-like',
    redactText('SSN 987654321 found in output') ===
    'SSN [NUM_REDACTED] found in output');

  assert('digits', 'preserves 4-digit numbers',
    redactText('Port 8080 is in use') === 'Port 8080 is in use');

  assert('digits', 'preserves year numbers',
    redactText('Built in 2026') === 'Built in 2026');
}

// ---------------------------------------------------------------------------
// 4. redactText -- env vars
// ---------------------------------------------------------------------------

function testRedactEnvVars() {
  console.log('\n--- redactText: env vars ---');

  assert('env', 'API key pattern',
    redactText('Set API_KEY=sk-abc123xyz to authenticate') ===
    'Set [ENV_REDACTED] to authenticate');

  assert('env', 'database URL',
    redactText('DATABASE_URL=postgres://user:pass@host/db') ===
    '[ENV_REDACTED]');

  assert('env', 'preserves normal uppercase words',
    redactText('The DSCR was 1.25') === 'The DSCR was 1.25');
}

// ---------------------------------------------------------------------------
// 5. redactText -- edge cases
// ---------------------------------------------------------------------------

function testRedactEdgeCases() {
  console.log('\n--- redactText: edge cases ---');

  assert('edge', 'null input returns null',
    redactText(null) === null);

  assert('edge', 'undefined input returns undefined',
    redactText(undefined) === undefined);

  assert('edge', 'number input returns number',
    redactText(42) === 42);

  assert('edge', 'empty string',
    redactText('') === '');

  assert('edge', 'no sensitive content unchanged',
    redactText('The cap rate was 5.5% on this deal') ===
    'The cap rate was 5.5% on this deal');
}

// ---------------------------------------------------------------------------
// 6. redactSubmission -- full object
// ---------------------------------------------------------------------------

function testRedactSubmission() {
  console.log('\n--- redactSubmission: full object ---');

  const raw = {
    submission_id: 'fb_abc123def456',
    submission_type: 'bug',
    timestamp: '2026-04-01T12:00:00Z',
    plugin_version: '2.5.0',
    install_id_hash: 'sha256_deadbeef',
    message: 'Crashed when reading /Users/mario/deals/rent-roll.xlsx with account 123456789',
    rating: 4,
    severity: 'high',
    skill_slug: 'rent-roll-analyzer',
    contact_email: 'mario@example.com',
    context: {
      skills_used_this_session: ['rent-roll-analyzer', 'acquisition-underwriting-engine'],
      error_category: 'FileReadError at /Users/mario/deals/data.csv',
      what_user_tried: 'Analyzed rent roll from ~/Downloads/rr.xlsx',
      what_happened: 'Script failed with DATABASE_URL=postgres://localhost/cre error',
    },
  };

  const redacted = redactSubmission(raw);

  // Structured fields preserved
  assert('submission', 'preserves submission_id',
    redacted.submission_id === 'fb_abc123def456');
  assert('submission', 'preserves submission_type',
    redacted.submission_type === 'bug');
  assert('submission', 'preserves rating',
    redacted.rating === 4);
  assert('submission', 'preserves skill_slug',
    redacted.skill_slug === 'rent-roll-analyzer');

  // Contact email preserved (user explicitly provided it)
  assert('submission', 'preserves contact_email',
    redacted.contact_email === 'mario@example.com');

  // Free-text fields redacted
  assert('submission', 'message: path redacted',
    !redacted.message.includes('/Users/mario'));
  assert('submission', 'message: digits redacted',
    !redacted.message.includes('123456789'));

  // Context fields redacted
  assert('submission', 'context.error_category: path redacted',
    !redacted.context.error_category.includes('/Users/mario'));
  assert('submission', 'context.what_user_tried: tilde path redacted',
    !redacted.context.what_user_tried.includes('~/Downloads'));
  assert('submission', 'context.what_happened: env var redacted',
    !redacted.context.what_happened.includes('DATABASE_URL='));

  // Context array preserved (skill slugs are not free text)
  assert('submission', 'context.skills_used_this_session preserved',
    Array.isArray(redacted.context.skills_used_this_session) &&
    redacted.context.skills_used_this_session.length === 2);

  // Original not mutated
  assert('submission', 'original not mutated',
    raw.message.includes('/Users/mario'));
}

// ---------------------------------------------------------------------------
// 7. redactSubmission -- edge cases
// ---------------------------------------------------------------------------

function testRedactSubmissionEdge() {
  console.log('\n--- redactSubmission: edge cases ---');

  assert('sub-edge', 'null returns null',
    redactSubmission(null) === null);

  assert('sub-edge', 'string returns string',
    redactSubmission('hello') === 'hello');

  assert('sub-edge', 'empty object returns empty object',
    JSON.stringify(redactSubmission({})) === '{}');

  assert('sub-edge', 'missing context is fine',
    redactSubmission({ message: 'test' }).message === 'test');

  assert('sub-edge', 'null context preserved',
    redactSubmission({ message: 'test', context: null }).context === null);
}

// ---------------------------------------------------------------------------
// Run all tests
// ---------------------------------------------------------------------------

console.log('========================================');
console.log('  CRE Feedback Redaction -- Test Suite');
console.log('========================================');

testRedactPaths();
testRedactEmails();
testRedactDigits();
testRedactEnvVars();
testRedactEdgeCases();
testRedactSubmission();
testRedactSubmissionEdge();

console.log('\n========================================');
console.log(`  TOTAL: ${totalPass} passed, ${totalFail} failed`);
if (failedTests.length > 0) {
  console.log('\n  Failed tests:');
  for (const t of failedTests) console.log(`    - ${t}`);
}
console.log('========================================\n');

process.exit(totalFail > 0 ? 1 : 0);
