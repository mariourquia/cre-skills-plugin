#!/usr/bin/env node
/**
 * CRE Skill Dispatcher
 * ====================
 * Zero-dependency Node.js ESM script that reads CRE-ROUTING.md, parses the
 * Quick Routing Table, and fuzzy-matches a user query against skill triggers.
 *
 * Usage:
 *   node routing/skill-dispatcher.mjs "underwrite a deal"
 *   node routing/skill-dispatcher.mjs "waterfall promote GP/LP split"
 *   node routing/skill-dispatcher.mjs --list
 *
 * Output: JSON with top 3 matches, scores, and confidence level.
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROUTING_MD_PATH = join(__dirname, "CRE-ROUTING.md");

const STOP_WORDS = new Set([
  "a", "an", "the", "this", "that", "is", "it", "in", "on", "at", "to",
  "for", "of", "with", "and", "or", "my", "me", "i", "we", "our", "do",
  "does", "can", "how", "what", "should", "would", "could", "please",
  "help", "want", "need", "like",
]);

// ---------------------------------------------------------------------------
// Routing table parser
// ---------------------------------------------------------------------------

/**
 * Parse CRE-ROUTING.md and extract the Quick Routing Table rows.
 * Each row has: triggers (text from "User says..." column) and skill slug.
 *
 * Table format:
 *   | "screen this deal", "should I look at this", new OM/listing | `/deal-quick-screen` |
 *
 * @returns {Array<{triggers: string, slug: string, tokens: string[]}>}
 */
function parseRoutingTable(mdContent) {
  const lines = mdContent.split("\n");
  const entries = [];
  let inTable = false;

  for (const line of lines) {
    const trimmed = line.trim();

    // Detect table start (header row)
    if (trimmed.startsWith("| User says")) {
      inTable = true;
      continue;
    }

    // Skip separator row
    if (inTable && trimmed.startsWith("|---")) {
      continue;
    }

    // End of table: non-pipe line after table started
    if (inTable && !trimmed.startsWith("|")) {
      // Could be blank line between table sections, keep going
      if (trimmed === "") continue;
      // If it's a heading or other content, we've left the table
      if (trimmed.startsWith("#") || trimmed.startsWith(">")) {
        inTable = false;
        continue;
      }
      continue;
    }

    if (!inTable) continue;

    // Parse table row: | triggers | skill |
    const cells = trimmed
      .split("|")
      .map((c) => c.trim())
      .filter((c) => c.length > 0);

    if (cells.length < 2) continue;

    const triggersRaw = cells[0];
    const skillRaw = cells[1];

    // Extract skill slug from backtick format: `/slug`
    const slugMatch = skillRaw.match(/`\/([^`]+)`/);
    if (!slugMatch) continue;

    const slug = slugMatch[1];

    // Clean trigger text: remove quotes, split on commas
    const triggerText = triggersRaw
      .replace(/"/g, "")
      .replace(/'/g, "")
      .toLowerCase();

    const tokens = tokenize(triggerText);

    entries.push({
      triggers: triggersRaw,
      slug,
      tokens,
    });
  }

  return entries;
}

// ---------------------------------------------------------------------------
// Tokenization and scoring
// ---------------------------------------------------------------------------

/**
 * Tokenize a string into lowercase words, removing stop words and
 * punctuation.
 * @param {string} text
 * @returns {string[]}
 */
function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s/-]/g, " ")
    .split(/\s+/)
    .filter((t) => t.length > 1 && !STOP_WORDS.has(t));
}

/**
 * Compute a fuzzy match score between a query and a routing entry.
 * Uses token overlap with length normalization and exact-phrase bonus.
 *
 * @param {string[]} queryTokens
 * @param {{triggers: string, slug: string, tokens: string[]}} entry
 * @returns {number} Score between 0 and 1
 */
function score(queryTokens, entry) {
  if (queryTokens.length === 0 || entry.tokens.length === 0) return 0;

  const entrySet = new Set(entry.tokens);
  let matchCount = 0;
  let partialCount = 0;

  for (const qt of queryTokens) {
    if (entrySet.has(qt)) {
      matchCount += 1;
    } else {
      // Partial match: check if query token is a substring of any entry token
      // or vice versa (handles "underwrite" matching "underwriting")
      for (const et of entry.tokens) {
        if (et.startsWith(qt) || qt.startsWith(et)) {
          partialCount += 0.6;
          break;
        }
      }
    }
  }

  // Jaccard-like: matched tokens / union size, but weighted toward query coverage
  const queryCoverage = (matchCount + partialCount) / queryTokens.length;
  const entryCoverage = matchCount / entry.tokens.length;

  // Weighted combination: query coverage matters more (user intent)
  return queryCoverage * 0.7 + entryCoverage * 0.3;
}

/**
 * Classify confidence level from score.
 * @param {number} topScore
 * @returns {string}
 */
function confidenceLevel(topScore) {
  if (topScore >= 0.6) return "high";
  if (topScore >= 0.35) return "medium";
  if (topScore >= 0.15) return "low";
  return "none";
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

/**
 * List all skill slugs from the routing table.
 * @param {Array} entries
 */
function cmdList(entries) {
  const slugs = entries.map((e) => e.slug);
  const unique = [...new Set(slugs)].sort();
  const result = {
    skills: unique,
    count: unique.length,
  };
  console.log(JSON.stringify(result, null, 2));
}

/**
 * Match a query against the routing table and return top 3 results.
 * @param {string} query
 * @param {Array} entries
 */
function cmdMatch(query, entries) {
  const queryTokens = tokenize(query);

  if (queryTokens.length === 0) {
    console.log(
      JSON.stringify(
        {
          error: "Query produced no searchable tokens after filtering",
          query,
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }

  // Score all entries
  const scored = entries
    .map((entry) => ({
      slug: entry.slug,
      triggers: entry.triggers,
      score: Math.round(score(queryTokens, entry) * 1000) / 1000,
    }))
    .filter((e) => e.score > 0)
    .sort((a, b) => b.score - a.score);

  // Deduplicate by slug (some slugs appear multiple times in routing table)
  const seen = new Set();
  const deduped = [];
  for (const item of scored) {
    if (!seen.has(item.slug)) {
      seen.add(item.slug);
      deduped.push(item);
    }
  }

  const top3 = deduped.slice(0, 3);
  const topScore = top3.length > 0 ? top3[0].score : 0;

  const result = {
    query,
    tokens: queryTokens,
    matches: top3.map((m) => ({
      skill: m.slug,
      invoke: `/${m.slug}`,
      score: m.score,
      matched_triggers: m.triggers,
    })),
    confidence: confidenceLevel(topScore),
    total_skills_searched: entries.length,
  };

  console.log(JSON.stringify(result, null, 2));
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);

  // Load and parse routing table
  let mdContent;
  try {
    mdContent = readFileSync(ROUTING_MD_PATH, "utf-8");
  } catch (err) {
    console.error(
      JSON.stringify({
        error: `Failed to read routing file: ${err.message}`,
        path: ROUTING_MD_PATH,
      }),
    );
    process.exit(1);
  }

  const entries = parseRoutingTable(mdContent);

  if (entries.length === 0) {
    console.error(
      JSON.stringify({
        error: "No routing entries parsed from CRE-ROUTING.md",
      }),
    );
    process.exit(1);
  }

  // Dispatch command
  if (args.includes("--list")) {
    cmdList(entries);
    return;
  }

  const query = args.filter((a) => !a.startsWith("--")).join(" ").trim();

  if (!query) {
    console.error(
      JSON.stringify({
        error: "No query provided",
        usage: 'node routing/skill-dispatcher.mjs "underwrite a deal"',
        flags: "--list: print all skill slugs",
      }),
    );
    process.exit(1);
  }

  cmdMatch(query, entries);
}

main();
