#!/usr/bin/env node
/**
 * CRE Skills Plugin -- Feedback Retry Outbox
 *
 * Queues failed remote feedback submissions for retry on next session start.
 * Storage: ~/.cre-skills/outbox.jsonl
 *
 * Exports:
 *   enqueue(entry)           -- append a failed submission for later retry
 *   drain(backendUrl)        -- retry pending entries (async, with per-request timeout)
 *   pending()                -- return count of queued items
 *
 * No external dependencies. Node stdlib + global fetch only.
 */

import { readFileSync, writeFileSync, appendFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const CONFIG_DIR = join(homedir(), '.cre-skills');
const OUTBOX_PATH = join(CONFIG_DIR, 'outbox.jsonl');
const MAX_ATTEMPTS = 5;
const REQUEST_TIMEOUT_MS = 4000;

// ---------------------------------------------------------------------------
// Read / write helpers
// ---------------------------------------------------------------------------

function readOutbox() {
  try {
    const raw = readFileSync(OUTBOX_PATH, 'utf8');
    return raw
      .split('\n')
      .filter(line => line.trim())
      .map(line => {
        try {
          return JSON.parse(line);
        } catch {
          return null;
        }
      })
      .filter(Boolean);
  } catch {
    return [];
  }
}

function writeOutbox(entries) {
  mkdirSync(CONFIG_DIR, { recursive: true });
  const data = entries.length
    ? entries.map(e => JSON.stringify(e)).join('\n') + '\n'
    : '';
  writeFileSync(OUTBOX_PATH, data, 'utf8');
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Append a failed feedback submission to the outbox for later retry.
 * @param {object} entry - The feedback record that failed to send remotely.
 */
export function enqueue(entry) {
  mkdirSync(CONFIG_DIR, { recursive: true });
  const record = {
    ...entry,
    _outbox: {
      queued_at: new Date().toISOString(),
      attempts: 0,
      last_attempt_at: null,
    },
  };
  appendFileSync(OUTBOX_PATH, JSON.stringify(record) + '\n', 'utf8');
}

/**
 * Retry all pending outbox entries against the backend.
 * - Successful sends (2xx) are removed.
 * - Failed sends get their attempt count bumped.
 * - Entries exceeding MAX_ATTEMPTS are evicted (dropped permanently).
 * - Each request has a 4-second timeout to avoid blocking session start.
 *
 * @param {string} backendUrl - The feedback API endpoint.
 * @returns {Promise<{sent: number, failed: number, evicted: number}>}
 */
export async function drain(backendUrl) {
  // Validate that the backend URL uses HTTPS to prevent data exfiltration
  try {
    const u = new URL(backendUrl);
    if (u.protocol !== 'https:') {
      return { sent: 0, failed: 0, evicted: 0 };
    }
  } catch {
    return { sent: 0, failed: 0, evicted: 0 };
  }

  const entries = readOutbox();
  if (entries.length === 0) {
    return { sent: 0, failed: 0, evicted: 0 };
  }

  const remaining = [];
  let sent = 0;
  let evicted = 0;

  for (const entry of entries) {
    const meta = entry._outbox || { attempts: 0, queued_at: null, last_attempt_at: null };

    if (meta.attempts >= MAX_ATTEMPTS) {
      evicted++;
      continue;
    }

    try {
      const { _outbox, ...payload } = entry;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

      const res = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Plugin-Version': payload.plugin_version || 'unknown',
          'X-Outbox-Retry': String(meta.attempts + 1),
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      clearTimeout(timer);

      if (res.ok) {
        sent++;
      } else {
        meta.attempts++;
        meta.last_attempt_at = new Date().toISOString();
        remaining.push({ ...entry, _outbox: meta });
      }
    } catch {
      meta.attempts++;
      meta.last_attempt_at = new Date().toISOString();
      remaining.push({ ...entry, _outbox: meta });
    }
  }

  writeOutbox(remaining);
  return { sent, failed: remaining.length, evicted };
}

/**
 * Return the number of entries waiting in the outbox.
 * @returns {number}
 */
export function pending() {
  return readOutbox().length;
}
