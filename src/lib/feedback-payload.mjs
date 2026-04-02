/**
 * CRE Skills Plugin -- Customization Feedback Payload Builder
 *
 * Constructs structured feedback payloads for skill customizations,
 * applies privacy filters based on user configuration, and manages
 * consent state.
 *
 * Privacy modes (from least to most data):
 *   off                  -- no feedback payload created
 *   metadata_only        -- skill slug, categories, rationale, hashes
 *   metadata_and_summary -- + diff summary (line counts, sections changed)
 *   metadata_and_diff    -- + full unified diff text
 *   metadata_and_content -- + full modified SKILL.md content (requires consent)
 *
 * Default: metadata_only with require_consent: true
 *
 * Zero external dependencies.
 */

import { readFileSync, writeFileSync, appendFileSync, mkdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir, platform } from "node:os";
import { randomUUID } from "node:crypto";

const CRE_DIR = join(homedir(), ".cre-skills");
const CONFIG_PATH = join(CRE_DIR, "config.json");
const FEEDBACK_LOG = join(CRE_DIR, "feedback-log.jsonl");
const OUTBOX_PATH = join(CRE_DIR, "outbox.jsonl");

/**
 * Valid feedback modes, ordered by data exposure.
 */
export const FEEDBACK_MODES = [
  "off",
  "metadata_only",
  "metadata_and_summary",
  "metadata_and_diff",
  "metadata_and_content",
];

/**
 * Read the customization config block from ~/.cre-skills/config.json.
 * Returns safe defaults if missing or malformed.
 */
export function getCustomizationConfig() {
  const defaults = {
    feedback_enabled: true,
    feedback_mode: "metadata_only",
    feedback_endpoint: "",
    require_consent: true,
    dry_run: false,
  };

  if (!existsSync(CONFIG_PATH)) return defaults;

  try {
    const config = JSON.parse(readFileSync(CONFIG_PATH, "utf-8"));
    const cust = config.customization || {};
    return {
      feedback_enabled: cust.feedback_enabled ?? defaults.feedback_enabled,
      feedback_mode: FEEDBACK_MODES.includes(cust.feedback_mode) ? cust.feedback_mode : defaults.feedback_mode,
      feedback_endpoint: cust.feedback_endpoint ?? defaults.feedback_endpoint,
      require_consent: cust.require_consent ?? defaults.require_consent,
      dry_run: cust.dry_run ?? defaults.dry_run,
    };
  } catch {
    return defaults;
  }
}

/**
 * Build a customization feedback payload.
 *
 * @param {object} options
 * @param {object} options.metadata       -- Customization metadata record
 * @param {string} options.diffSummary    -- Human-readable diff summary
 * @param {string} options.diffText       -- Full unified diff text
 * @param {string} options.modifiedContent -- Full modified SKILL.md content
 * @param {object} options.diffStats      -- { added, removed, unchanged }
 * @param {string[]} options.sectionsChanged -- Affected section headings
 * @param {string} options.pluginVersion
 * @param {boolean} options.wantsUpstreamConsideration
 * @param {boolean} options.consentedToContent -- User explicitly consented to send content
 * @returns {object} The feedback payload
 */
export function buildPayload(options) {
  const {
    metadata,
    diffSummary = "",
    diffText = "",
    modifiedContent = "",
    diffStats = {},
    sectionsChanged = [],
    pluginVersion = "unknown",
    wantsUpstreamConsideration = false,
    consentedToContent = false,
  } = options;

  return {
    schema_version: "1.0",
    feedback_id: `cfb_${randomUUID().replace(/-/g, "").slice(0, 16)}`,
    feedback_type: "customization_feedback",
    timestamp: new Date().toISOString(),
    plugin_version: pluginVersion,
    platform: platform(),

    // Skill identification
    skill_slug: metadata.skill_slug,
    customization_id: metadata.customization_id,

    // What changed
    base_content_hash: metadata.base_content_hash,
    modified_content_hash: metadata.modified_content_hash,
    change_categories: metadata.change_categories || [],
    diff_stats: diffStats,
    sections_changed: sectionsChanged,

    // Why it changed
    rationale: metadata.rationale || null,
    notes: metadata.notes || null,

    // Extended data (controlled by privacy mode)
    diff_summary: diffSummary,
    diff_text: diffText,
    modified_content: modifiedContent,

    // Upstream intent
    wants_upstream_consideration: wantsUpstreamConsideration,

    // Consent tracking
    consented_to_content: consentedToContent,
    consent_timestamp: consentedToContent ? new Date().toISOString() : null,
  };
}

/**
 * Apply privacy mode filtering to a payload.
 * Strips fields that exceed the configured sharing level.
 *
 * @param {object} payload
 * @param {string} mode - One of FEEDBACK_MODES
 * @returns {object} Filtered payload
 */
export function filterByMode(payload, mode) {
  const filtered = { ...payload };

  // Always strip content unless explicitly allowed
  if (mode !== "metadata_and_content" || !payload.consented_to_content) {
    filtered.modified_content = null;
  }

  // Strip diff text unless mode allows it
  if (mode !== "metadata_and_diff" && mode !== "metadata_and_content") {
    filtered.diff_text = null;
  }

  // Strip diff summary unless mode allows it
  if (mode === "metadata_only" || mode === "off") {
    filtered.diff_summary = null;
    filtered.diff_stats = null;
    filtered.sections_changed = null;
  }

  return filtered;
}

/**
 * Preview what would be sent at a given privacy mode.
 * Returns the filtered payload as a formatted string.
 *
 * @param {object} payload
 * @param {string} mode
 * @returns {string} Preview text
 */
export function previewPayload(payload, mode) {
  const filtered = filterByMode(payload, mode);
  const lines = [
    `Feedback ID: ${filtered.feedback_id}`,
    `Skill: ${filtered.skill_slug}`,
    `Categories: ${(filtered.change_categories || []).join(", ") || "(none)"}`,
    `Rationale: ${filtered.rationale || "(none)"}`,
    `Hashes: base=${filtered.base_content_hash?.slice(0, 8)}... modified=${filtered.modified_content_hash?.slice(0, 8)}...`,
    `Upstream consideration: ${filtered.wants_upstream_consideration ? "yes" : "no"}`,
  ];

  if (filtered.diff_stats) {
    lines.push(`Diff stats: +${filtered.diff_stats.added} -${filtered.diff_stats.removed} =${filtered.diff_stats.unchanged}`);
  }
  if (filtered.sections_changed) {
    lines.push(`Sections changed: ${filtered.sections_changed.join(", ")}`);
  }
  if (filtered.diff_summary) {
    lines.push(`Diff summary: ${filtered.diff_summary}`);
  }
  if (filtered.diff_text) {
    lines.push(`Full diff: (${filtered.diff_text.split("\n").length} lines)`);
  }
  if (filtered.modified_content) {
    lines.push(`Full content: (${filtered.modified_content.split("\n").length} lines)`);
  }

  return lines.join("\n");
}

/**
 * Save feedback payload to local log.
 *
 * @param {object} payload
 */
export function savePayloadLocally(payload) {
  mkdirSync(CRE_DIR, { recursive: true });
  appendFileSync(FEEDBACK_LOG, JSON.stringify(payload) + "\n");
}

/**
 * Enqueue a payload for remote retry if the initial send fails.
 *
 * @param {object} payload
 */
export function enqueueForRetry(payload) {
  mkdirSync(CRE_DIR, { recursive: true });
  const record = {
    ...payload,
    _outbox: {
      queued_at: new Date().toISOString(),
      attempts: 0,
      last_attempt_at: null,
    },
  };
  appendFileSync(OUTBOX_PATH, JSON.stringify(record) + "\n");
}

/**
 * Attempt to send a payload to the configured endpoint.
 *
 * @param {object} payload
 * @param {string} endpoint
 * @param {number} timeoutMs
 * @returns {Promise<{ sent: boolean, error?: string }>}
 */
// ── Upstream Suggestion ──────────────────────────────────────────────────────

/**
 * Build a structured upstream suggestion from a customization.
 * Produces a GitHub-issue-ready object with title, body, and labels.
 *
 * @param {object} metadata - Customization metadata
 * @param {string} diffSummary - Human-readable diff summary
 * @param {string} diffText - Full diff text
 * @returns {{ title: string, body: string, labels: string[] }}
 */
export function buildUpstreamSuggestion(metadata, diffSummary, diffText) {
  const cats = (metadata.change_categories || []).join(", ") || "general";
  const body = [
    "## Skill Customization Report",
    "",
    `**Skill:** \`${metadata.skill_slug}\``,
    `**Categories:** ${cats}`,
    `**Rationale:** ${metadata.rationale || "(not provided)"}`,
    `**Plugin version:** ${metadata.plugin_version || "unknown"}`,
    `**Platform:** ${metadata.platform || "unknown"}`,
    "",
    "### Change Summary",
    diffSummary || "No summary available.",
    "",
    "### Diff",
    "```diff",
    diffText || "(no diff available)",
    "```",
    "",
    metadata.notes ? `### Additional Notes\n${metadata.notes}\n` : "",
    "---",
    "_This suggestion was generated from a local skill customization via the CRE Skills Plugin._",
  ].filter(Boolean).join("\n");

  return {
    title: `[Skill Improvement] ${metadata.skill_slug}: ${cats}`,
    body,
    labels: ["skill-improvement", ...(metadata.change_categories || [])],
  };
}

// ── Analytics ────────────────────────────────────────────────────────────────

/**
 * Analyze customization feedback from the local log.
 * Produces aggregated insights for the maintainer or enterprise admin.
 *
 * @returns {object} Aggregated analytics
 */
export function analyzeCustomizationFeedback() {
  const entries = readFeedbackLog().filter(e => e.feedback_type === "customization_feedback");

  if (entries.length === 0) {
    return { total: 0, message: "No customization feedback recorded yet." };
  }

  // Skill frequency
  const skillCounts = {};
  for (const e of entries) {
    skillCounts[e.skill_slug] = (skillCounts[e.skill_slug] || 0) + 1;
  }

  // Category distribution
  const categoryCounts = {};
  for (const e of entries) {
    for (const cat of (e.change_categories || [])) {
      categoryCounts[cat] = (categoryCounts[cat] || 0) + 1;
    }
  }

  // Upstream requests
  const upstreamCount = entries.filter(e => e.wants_upstream_consideration).length;

  // Top changed sections (from entries that have sections_changed)
  const sectionCounts = {};
  for (const e of entries) {
    for (const sec of (e.sections_changed || [])) {
      sectionCounts[sec] = (sectionCounts[sec] || 0) + 1;
    }
  }

  // Timeline (by month)
  const monthCounts = {};
  for (const e of entries) {
    const month = (e.timestamp || "").slice(0, 7);
    if (month) monthCounts[month] = (monthCounts[month] || 0) + 1;
  }

  return {
    total: entries.length,
    unique_skills: Object.keys(skillCounts).length,
    skills_by_frequency: Object.entries(skillCounts).sort((a, b) => b[1] - a[1]).map(([slug, count]) => ({ slug, count })),
    category_distribution: Object.entries(categoryCounts).sort((a, b) => b[1] - a[1]).map(([cat, count]) => ({ category: cat, count })),
    upstream_requests: upstreamCount,
    upstream_rate: entries.length > 0 ? Math.round(upstreamCount / entries.length * 100) : 0,
    sections_most_changed: Object.entries(sectionCounts).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([sec, count]) => ({ section: sec, count })),
    monthly_trend: Object.entries(monthCounts).sort().map(([month, count]) => ({ month, count })),
  };
}

/**
 * Read the feedback log file.
 * @returns {Array<object>}
 */
function readFeedbackLog() {
  if (!existsSync(FEEDBACK_LOG)) return [];
  try {
    return readFileSync(FEEDBACK_LOG, "utf-8")
      .replace(/\r\n/g, "\n").split("\n")
      .filter(line => line.trim())
      .map(line => { try { return JSON.parse(line); } catch { return null; } })
      .filter(Boolean);
  } catch {
    return [];
  }
}

// ── Remote send ──────────────────────────────────────────────────────────────

export async function sendPayload(payload, endpoint, timeoutMs = 5000) {
  if (!endpoint) return { sent: false, error: "No endpoint configured" };

  // Validate endpoint is HTTPS to prevent SSRF
  let url;
  try { url = new URL(endpoint); } catch { return { sent: false, error: "Invalid endpoint URL" }; }
  if (url.protocol !== "https:") return { sent: false, error: "Endpoint must use HTTPS" };

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Plugin-Version": payload.plugin_version || "unknown",
        "X-Feedback-Type": "customization",
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    clearTimeout(timer);

    if (res.ok) return { sent: true };
    return { sent: false, error: `HTTP ${res.status}` };
  } catch (err) {
    return { sent: false, error: err.message || "Network error" };
  }
}
