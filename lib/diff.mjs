/**
 * CRE Skills Plugin -- Diff Engine
 *
 * Line-based diff using LCS (Longest Common Subsequence).
 * Produces structured hunks, human-readable summaries, and content hashes.
 *
 * Zero external dependencies.
 */

import { createHash } from "node:crypto";

/**
 * SHA-256 hex hash of a string.
 */
export function contentHash(text) {
  return createHash("sha256").update(text, "utf-8").digest("hex");
}

/**
 * Compute a line-based diff between two strings.
 *
 * @param {string} original
 * @param {string} modified
 * @returns {{ hunks: Array, stats: { added: number, removed: number, unchanged: number }, sections_changed: string[] }}
 */
export function computeDiff(original, modified) {
  // Normalize CRLF to LF for cross-platform consistency (Windows editors)
  const origLines = original.replace(/\r\n/g, "\n").split("\n");
  const modLines = modified.replace(/\r\n/g, "\n").split("\n");

  const ops = lcsBacktrack(origLines, modLines);
  const hunks = buildHunks(ops);
  const sections = detectSectionsChanged(ops);

  let added = 0, removed = 0, unchanged = 0;
  for (const op of ops) {
    if (op.type === "add") added++;
    else if (op.type === "remove") removed++;
    else unchanged++;
  }

  return { hunks, stats: { added, removed, unchanged }, sections_changed: sections };
}

/**
 * Human-readable summary of a diff result.
 *
 * @param {{ stats: object, sections_changed: string[], hunks: Array }} diffResult
 * @returns {string}
 */
export function summarizeDiff(diffResult) {
  const { stats, sections_changed, hunks } = diffResult;
  const parts = [];

  if (stats.added === 0 && stats.removed === 0) {
    return "No changes detected.";
  }

  if (stats.added > 0) parts.push(`${stats.added} line${stats.added !== 1 ? "s" : ""} added`);
  if (stats.removed > 0) parts.push(`${stats.removed} line${stats.removed !== 1 ? "s" : ""} removed`);
  parts.push(`${stats.unchanged} unchanged`);

  let summary = parts.join(", ") + ".";

  if (sections_changed.length > 0) {
    summary += ` Sections affected: ${sections_changed.join(", ")}.`;
  }

  if (hunks.length > 0) {
    summary += ` ${hunks.length} change region${hunks.length !== 1 ? "s" : ""}.`;
  }

  return summary;
}

/**
 * Format diff as a unified-style text block for human review.
 *
 * @param {{ hunks: Array }} diffResult
 * @returns {string}
 */
export function formatDiffText(diffResult) {
  const lines = [];
  for (const hunk of diffResult.hunks) {
    lines.push(`@@ -${hunk.origStart},${hunk.origCount} +${hunk.modStart},${hunk.modCount} @@`);
    for (const op of hunk.ops) {
      if (op.type === "remove") lines.push(`- ${op.line}`);
      else if (op.type === "add") lines.push(`+ ${op.line}`);
      else lines.push(`  ${op.line}`);
    }
  }
  return lines.join("\n");
}

// ── LCS algorithm ────────────────────────────────────────────────────────────

function lcsBacktrack(a, b) {
  const m = a.length;
  const n = b.length;

  // Build DP table. Uint16Array is faster for typical skill files (100-300 lines)
  // but overflows at 65536. Fall back to Uint32Array for larger files.
  const ArrayType = (m <= 65535 && n <= 65535) ? Uint16Array : Uint32Array;
  const dp = Array.from({ length: m + 1 }, () => new ArrayType(n + 1));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // Backtrack to produce edit operations
  const ops = [];
  let i = m, j = n;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && a[i - 1] === b[j - 1]) {
      ops.unshift({ type: "equal", line: a[i - 1], origLine: i, modLine: j });
      i--; j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      ops.unshift({ type: "add", line: b[j - 1], modLine: j });
      j--;
    } else {
      ops.unshift({ type: "remove", line: a[i - 1], origLine: i });
      i--;
    }
  }
  return ops;
}

// ── Hunk construction ────────────────────────────────────────────────────────

const CONTEXT_LINES = 3;

function buildHunks(ops) {
  // Find change regions and group with context
  const changeIndices = [];
  for (let i = 0; i < ops.length; i++) {
    if (ops[i].type !== "equal") changeIndices.push(i);
  }
  if (changeIndices.length === 0) return [];

  // Group consecutive changes (within CONTEXT_LINES of each other)
  const groups = [];
  let groupStart = changeIndices[0];
  let groupEnd = changeIndices[0];

  for (let k = 1; k < changeIndices.length; k++) {
    if (changeIndices[k] - groupEnd <= CONTEXT_LINES * 2 + 1) {
      groupEnd = changeIndices[k];
    } else {
      groups.push([groupStart, groupEnd]);
      groupStart = changeIndices[k];
      groupEnd = changeIndices[k];
    }
  }
  groups.push([groupStart, groupEnd]);

  // Build hunks with context
  const hunks = [];
  for (const [gs, ge] of groups) {
    const start = Math.max(0, gs - CONTEXT_LINES);
    const end = Math.min(ops.length - 1, ge + CONTEXT_LINES);
    const hunkOps = ops.slice(start, end + 1);

    let origStart = 1, modStart = 1, origCount = 0, modCount = 0;
    let foundFirst = false;
    for (const op of hunkOps) {
      if (!foundFirst) {
        origStart = op.origLine || 1;
        modStart = op.modLine || 1;
        foundFirst = true;
      }
      if (op.type === "equal") { origCount++; modCount++; }
      else if (op.type === "add") { modCount++; }
      else { origCount++; }
    }

    hunks.push({ origStart, origCount, modStart, modCount, ops: hunkOps });
  }
  return hunks;
}

// ── Section detection ────────────────────────────────────────────────────────

/**
 * Detect which markdown sections (## headings) were affected by changes.
 */
function detectSectionsChanged(ops) {
  const sections = new Set();
  let currentSection = null;

  for (const op of ops) {
    const line = op.line || "";
    const headingMatch = line.match(/^#{1,3}\s+(.+)/);
    if (headingMatch) {
      currentSection = headingMatch[1].trim();
    }
    if (op.type !== "equal" && currentSection) {
      sections.add(currentSection);
    }
  }
  return [...sections];
}
