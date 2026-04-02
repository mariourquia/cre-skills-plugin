#!/usr/bin/env node
/**
 * CRE Skills Plugin -- SessionStart hook
 * Initializes ~/.cre-skills/config.json on first run.
 * Shows a one-time privacy notice when firstRunComplete is false.
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
    telemetry: true,
    survey: false,
    feedback: {
      mode: 'ask_each_time',
      include_context: true,
      backend_url: 'https://cre-skills-feedback-api.vercel.app/api/feedback',
    },
    anonymousId: randomUUID(),
    firstRunComplete: false,
    version: '4.0.0',
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

  // Backfill: enable telemetry for existing installs upgrading to v4
  if (config.version && config.version < '4.0.0' && config.telemetry === false) {
    config.telemetry = true;
    config.version = '4.0.0';
    writeConfig(config);
  }

  // Backfill feedback config for existing installs
  if (!config.feedback || !config.feedback.backend_url) {
    config.feedback = {
      mode: 'ask_each_time',
      include_context: true,
      backend_url: 'https://cre-skills-feedback-api.vercel.app/api/feedback',
    };
    writeConfig(config);
  }

  // Backfill firstRunAt for installs that predate this field
  if (config.firstRunComplete && !config.firstRunAt) {
    config.firstRunAt = new Date().toISOString().slice(0, 10);
    writeConfig(config);
  }

  if (!config.firstRunComplete) {
    process.stdout.write(
      '[CRE Skills] Welcome! Anonymous usage telemetry is enabled by default.\n' +
      '\n' +
      'What is tracked (anonymous, local-only):\n' +
      '  - Which skill was used (slug only, e.g. "deal-quick-screen")\n' +
      '  - Date of use (no time, no timezone)\n' +
      '  - A random anonymous ID (no name, email, or identity)\n' +
      '\n' +
      'What is NEVER tracked:\n' +
      '  - Deal data, financial figures, rent rolls, property details\n' +
      '  - File paths, prompts, AI responses, or any text you type\n' +
      '  - Your name, email, IP address, or organization\n' +
      '\n' +
      'All data stays on your machine at ~/.cre-skills/telemetry.jsonl\n' +
      'To opt out: set "telemetry": false in ~/.cre-skills/config.json\n' +
      'Full details: PRIVACY.md\n'
    );
    config.firstRunComplete = true;
    config.firstRunAt = new Date().toISOString().slice(0, 10);
    writeConfig(config);
  }
}

main();
