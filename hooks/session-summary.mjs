#!/usr/bin/env node
/**
 * CRE Skills Plugin -- Stop hook
 * Writes a session_end JSONL record to ~/.cre-skills/telemetry.jsonl
 * and optionally outputs a feedback prompt if survey is enabled.
 * No external dependencies. Node stdlib only.
 */

import { readFileSync, appendFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const CONFIG_DIR = join(homedir(), '.cre-skills');
const CONFIG_PATH = join(CONFIG_DIR, 'config.json');
const TELEMETRY_PATH = join(CONFIG_DIR, 'telemetry.jsonl');

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

/**
 * Read today's skill_invoked records from telemetry.jsonl that match
 * the current anonymous_id. Returns a de-duplicated array of skill slugs.
 */
function getTodaysSkills(anonymousId) {
  const today = isoDate();
  const skills = new Set();

  try {
    const raw = readFileSync(TELEMETRY_PATH, 'utf8');
    for (const line of raw.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      try {
        const record = JSON.parse(trimmed);
        if (
          record.event === 'skill_invoked' &&
          record.date === today &&
          record.anonymous_id === anonymousId &&
          typeof record.skill === 'string'
        ) {
          skills.add(record.skill);
        }
      } catch {
        // Skip malformed lines
      }
    }
  } catch {
    // File may not exist yet -- that is fine.
  }

  return Array.from(skills);
}

function appendRecord(record) {
  try {
    mkdirSync(CONFIG_DIR, { recursive: true });
    appendFileSync(TELEMETRY_PATH, JSON.stringify(record) + '\n', 'utf8');
  } catch {
    // Never crash the session over a write failure.
  }
}

function main() {
  const config = readConfig();
  if (!config) {
    process.exit(0);
  }

  const anonymousId = config.anonymousId || 'unknown';

  if (config.telemetry) {
    const skillsUsed = getTodaysSkills(anonymousId);

    // Only write a session_end record if at least one skill was used.
    if (skillsUsed.length > 0) {
      const record = {
        event: 'session_end',
        skills_used: skillsUsed,
        date: isoDate(),
        anonymous_id: anonymousId,
      };
      appendRecord(record);
    }
  }

  if (config.survey) {
    const skillsUsed = config.telemetry
      ? getTodaysSkills(anonymousId)
      : getTodaysSkills(anonymousId);

    // Only show the survey prompt if CRE skills were used this session.
    if (skillsUsed.length > 0) {
      process.stdout.write(
        '[CRE Skills] How useful was this session? (1-5, Enter to skip): \n' +
        'To submit feedback, run /cre-skills:feedback-summary or edit ~/.cre-skills/feedback.jsonl directly.\n'
      );
    }
  }
}

main();
