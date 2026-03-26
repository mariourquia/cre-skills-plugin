#!/usr/bin/env node
/**
 * CRE Skills Plugin -- PostToolUse hook
 * Appends a skill_invoked JSONL record to ~/.cre-skills/telemetry.jsonl
 * when a CRE SKILL.md is read and telemetry is enabled.
 * Reads hook input from stdin (Claude Code passes PostToolUse data as JSON on stdin).
 * No external dependencies. Node stdlib only.
 */

import { readFileSync, appendFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const CONFIG_DIR = join(homedir(), '.cre-skills');
const CONFIG_PATH = join(CONFIG_DIR, 'config.json');
const TELEMETRY_PATH = join(CONFIG_DIR, 'telemetry.jsonl');

// Matches skills/<slug>/SKILL.md pattern in any string field
const SKILL_PATH_RE = /skills\/([^/]+)\/SKILL\.md/;

function readConfig() {
  try {
    const raw = readFileSync(CONFIG_PATH, 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function isoDate() {
  return new Date().toISOString().slice(0, 10);
}

function appendRecord(record) {
  try {
    mkdirSync(CONFIG_DIR, { recursive: true });
    appendFileSync(TELEMETRY_PATH, JSON.stringify(record) + '\n', 'utf8');
  } catch {
    // Never crash the session over a write failure.
  }
}

function readStdinSync() {
  try {
    return readFileSync('/dev/stdin', 'utf8');
  } catch {
    return '';
  }
}

function extractSlugFromInput(hookData) {
  if (!hookData || typeof hookData !== 'object') return null;

  const input = hookData.tool_input || hookData.input || {};
  const result = hookData.tool_result || hookData.result || {};

  // Collect all string values to scan for the skill path pattern
  const candidates = [];

  for (const key of ['file_path', 'path', 'filename', 'command', 'content']) {
    if (typeof input[key] === 'string') {
      candidates.push(input[key]);
    }
  }

  if (typeof result === 'string') candidates.push(result);
  if (result && typeof result.content === 'string') candidates.push(result.content);

  for (const candidate of candidates) {
    const match = SKILL_PATH_RE.exec(candidate);
    if (match) return match[1];
  }

  return null;
}

function main() {
  const config = readConfig();

  // If config is missing or telemetry is disabled, exit silently.
  if (!config || !config.telemetry) {
    process.exit(0);
  }

  const stdinData = readStdinSync();
  if (!stdinData.trim()) {
    process.exit(0);
  }

  let hookData;
  try {
    hookData = JSON.parse(stdinData);
  } catch {
    // Unparseable input -- exit silently.
    process.exit(0);
  }

  const slug = extractSlugFromInput(hookData);
  if (!slug) {
    process.exit(0);
  }

  const record = {
    event: 'skill_invoked',
    skill: slug,
    date: isoDate(),
    anonymous_id: config.anonymousId || 'unknown',
  };

  appendRecord(record);
}

main();
