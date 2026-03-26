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
    anonymousId: randomUUID(),
    firstRunComplete: false,
    version: '2.0.0',
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

  if (!config.firstRunComplete) {
    process.stdout.write(
      '[CRE Skills] First run detected. Telemetry and feedback are disabled by default.\n' +
      'To enable anonymous usage tracking: set "telemetry": true in ~/.cre-skills/config.json\n' +
      'To enable post-session feedback prompts: set "survey": true in ~/.cre-skills/config.json\n' +
      'See PRIVACY.md for what is and isn\'t collected.\n'
    );
    config.firstRunComplete = true;
    writeConfig(config);
  }
}

main();
