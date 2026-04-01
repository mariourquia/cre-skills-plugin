#!/usr/bin/env node
/**
 * CRE Skills Plugin -- Feedback Redaction Utility
 *
 * Sanitizes free-text fields in feedback submissions before storage.
 * Standalone module: importable by other scripts or callable via CLI.
 *
 * CLI usage:
 *   echo '{"message":"bug at /Users/me/proj"}' | node scripts/redact-feedback.mjs
 *   Outputs redacted JSON to stdout.
 *
 * Programmatic usage:
 *   import { redactText, redactSubmission } from './redact-feedback.mjs';
 *
 * No external dependencies. Node stdlib only.
 */

import { readFileSync } from 'fs';

// --- Patterns ---

// Absolute file paths: /Users/..., /home/..., /var/..., C:\..., ~/...
const FILE_PATH_RE = /(?:~\/|\/(?:Users|home|var|tmp|opt|etc|mnt|Volumes|private)\/)\S+/g;
const WIN_PATH_RE = /[A-Z]:\\[\w\\. -]+/g;

// Email addresses in free text (user@domain.tld)
const EMAIL_RE = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;

// Sequences of 5+ digits (SSNs, account numbers, phone-like strings)
const DIGIT_SEQ_RE = /\b\d{5,}\b/g;

// Environment variable assignments: KEY=value or KEY="value"
const ENV_VAR_RE = /\b[A-Z_]{2,}=\S+/g;

// --- Core redaction ---

/**
 * Redact sensitive patterns from a single string.
 * @param {string} text - Raw input text.
 * @returns {string} Redacted text.
 */
export function redactText(text) {
  if (typeof text !== 'string') return text;

  return text
    .replace(FILE_PATH_RE, '[PATH_REDACTED]')
    .replace(WIN_PATH_RE, '[PATH_REDACTED]')
    .replace(EMAIL_RE, '[EMAIL_REDACTED]')
    .replace(DIGIT_SEQ_RE, '[NUM_REDACTED]')
    .replace(ENV_VAR_RE, '[ENV_REDACTED]');
}

/**
 * Redact sensitive content from a feedback submission object.
 * Applies redaction to free-text fields only. Preserves structured fields
 * (submission_id, type, rating, skill_slug, etc.) untouched.
 *
 * The contact_email field is NOT redacted -- the user explicitly provided it.
 *
 * @param {object} submission - Raw feedback submission.
 * @returns {object} Redacted copy (original is not mutated).
 */
export function redactSubmission(submission) {
  if (!submission || typeof submission !== 'object') return submission;

  const redacted = { ...submission };

  // Free-text fields to redact
  if (typeof redacted.message === 'string') {
    redacted.message = redactText(redacted.message);
  }

  if (typeof redacted.category === 'string') {
    redacted.category = redactText(redacted.category);
  }

  if (typeof redacted.organization === 'string') {
    redacted.organization = redactText(redacted.organization);
  }

  // Context sub-object
  if (redacted.context && typeof redacted.context === 'object') {
    redacted.context = { ...redacted.context };

    if (typeof redacted.context.error_category === 'string') {
      redacted.context.error_category = redactText(redacted.context.error_category);
    }
    if (typeof redacted.context.what_user_tried === 'string') {
      redacted.context.what_user_tried = redactText(redacted.context.what_user_tried);
    }
    if (typeof redacted.context.what_happened === 'string') {
      redacted.context.what_happened = redactText(redacted.context.what_happened);
    }
  }

  return redacted;
}

// --- CLI mode ---

function main() {
  let input;
  try {
    input = readFileSync(0, 'utf8');
  } catch {
    process.stderr.write('Usage: echo \'{"message":"..."}\' | node scripts/redact-feedback.mjs\n');
    process.exit(1);
  }

  if (!input.trim()) {
    process.stderr.write('No input on stdin.\n');
    process.exit(1);
  }

  let submission;
  try {
    submission = JSON.parse(input);
  } catch {
    process.stderr.write('Invalid JSON on stdin.\n');
    process.exit(1);
  }

  const redacted = redactSubmission(submission);
  process.stdout.write(JSON.stringify(redacted, null, 2) + '\n');
}

// Only run CLI when invoked directly (not imported)
const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'));
if (isMain) {
  main();
}
