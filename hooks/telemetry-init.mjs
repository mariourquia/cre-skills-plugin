#!/usr/bin/env node
/**
 * CRE Skills Plugin -- SessionStart hook
 * Initializes ~/.cre-skills/config.json on first run.
 * Shows a one-time consent notice when firstRunComplete is false.
 * No external dependencies. Node stdlib only.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';
import { randomUUID } from 'crypto';
import { homedir } from 'os';

const CONFIG_DIR = join(homedir(), '.cre-skills');
const CONFIG_PATH = join(CONFIG_DIR, 'config.json');

function defaultConfig() {
  return {
    telemetry: false,
    survey: false,
    feedback: {
      mode: 'local_only',
      include_context: true,
      backend_url: '',
    },
    anonymousId: randomUUID(),
    firstRunComplete: false,
    version: '3.0.0',
  };
}

function readConfig() {
  try {
    const raw = readFileSync(CONFIG_PATH, 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function writeConfig(config) {
  try {
    mkdirSync(CONFIG_DIR, { recursive: true });
    writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + '\n', 'utf8');
  } catch {
    // Never crash the session over a config write failure.
  }
}

function main() {
  let config = readConfig();

  if (!config) {
    config = defaultConfig();
    writeConfig(config);
  }

  // Backfill feedback config for existing installs (added in v3.0.0)
  if (!config.feedback) {
    config.feedback = { mode: 'local_only', include_context: true, backend_url: '' };
    writeConfig(config);
  }

  // Backfill firstRunAt for installs that predate this field
  if (config.firstRunComplete && !config.firstRunAt) {
    config.firstRunAt = new Date().toISOString().slice(0, 10);
    writeConfig(config);
  }

  if (!config.firstRunComplete) {
    process.stdout.write(
      '[CRE Skills] First run detected. Telemetry and feedback are disabled by default.\n' +
      'To enable anonymous usage tracking: set "telemetry": true in ~/.cre-skills/config.json\n' +
      'To enable post-session feedback prompts: set "survey": true in ~/.cre-skills/config.json\n' +
      'To share feedback anytime: /cre-skills:send-feedback or /cre-skills:report-problem\n' +
      'See PRIVACY.md for what is and isn\'t collected.\n'
    );
    config.firstRunComplete = true;
    config.firstRunAt = new Date().toISOString().slice(0, 10);
    writeConfig(config);
  }
}

main();
