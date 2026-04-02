#!/usr/bin/env node
/**
 * CRE Skill Dispatcher (Catalog-Driven)
 * ======================================
 * Zero-dependency Node.js ESM router backed by the generated catalog
 * (dist/catalog.json). Replaces the old markdown-table parser with
 * machine-readable routing that supports:
 *   - intent trigger matching
 *   - alias resolution
 *   - domain weighting
 *   - artifact-aware routing (OM, rent roll, lease, etc.)
 *   - stable-first ordering (stub/experimental hidden by default)
 *
 * Usage:
 *   node routing/skill-dispatcher.mjs "underwrite a deal"
 *   node routing/skill-dispatcher.mjs "waterfall promote GP/LP split"
 *   node routing/skill-dispatcher.mjs --list
 *   node routing/skill-dispatcher.mjs --list --include-hidden
 *   node routing/skill-dispatcher.mjs --artifact "OM"
 *
 * Output: JSON with top 3 matches, scores, confidence, and reason.
 *
 * Fallback: If dist/catalog.json is missing, falls back to CRE-ROUTING.md.
 */

import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = join(__dirname, "..");
const CATALOG_PATH = join(REPO_ROOT, "dist", "catalog.json");
const ROUTING_MD_PATH = join(__dirname, "CRE-ROUTING.md");

// ---------------------------------------------------------------------------
// Stop words for tokenization
// ---------------------------------------------------------------------------

const STOP_WORDS = new Set([
  "a", "an", "the", "this", "that", "is", "it", "in", "on", "at", "to",
  "for", "of", "with", "and", "or", "my", "me", "i", "we", "our", "do",
  "does", "can", "how", "what", "should", "would", "could", "please",
  "help", "want", "need", "like",
]);

// ---------------------------------------------------------------------------
// Artifact synonyms for artifact-aware routing
// ---------------------------------------------------------------------------

const ARTIFACT_SYNONYMS = {
  om: ["offering memorandum", "om", "marketing package", "broker package"],
  "rent roll": ["rent roll", "rent-roll", "tenant roster", "unit mix"],
  lease: ["lease", "lease agreement", "lease document", "commercial lease"],
  "t-12": ["t-12", "t12", "trailing twelve", "operating statement"],
  budget: ["budget", "operating budget", "annual budget"],
  "term sheet": ["term sheet", "term-sheet", "lender term sheet"],
  psa: ["psa", "purchase agreement", "purchase and sale", "p&s"],
  loi: ["loi", "letter of intent", "offer letter"],
  "rent roll data": ["rent roll", "tenant schedule"],
  "loan docs": ["loan document", "promissory note", "security instrument"],
};

// ---------------------------------------------------------------------------
// Catalog loader
// ---------------------------------------------------------------------------

function loadCatalog() {
  if (!existsSync(CATALOG_PATH)) {
    return null;
  }
  try {
    return JSON.parse(readFileSync(CATALOG_PATH, "utf-8"));
  } catch {
    return null;
  }
}

/**
 * Build routing entries from catalog items.
 * Only includes skills by default (the primary routable type).
 */
function catalogToEntries(catalog, includeHidden = false) {
  return catalog.items
    .filter((item) => {
      if (item.type !== "skill") return false;
      if (!includeHidden && item.hidden_from_default_catalog) return false;
      return true;
    })
    .map((item) => {
      // Combine intent_triggers, aliases, display_name, and id into tokens
      const allText = [
        ...item.intent_triggers,
        ...item.aliases,
        item.display_name,
        item.id.replace(/-/g, " "),
        item.persona || "",
      ].join(" ");

      return {
        slug: item.id,
        displayName: item.display_name,
        status: item.status,
        domain: item.lifecycle_phase,
        triggers: item.intent_triggers.join(", "),
        inputArtifacts: item.input_artifacts || [],
        downstreamItems: item.downstream_items || [],
        tokens: tokenize(allText),
        calculatorFile: item.calculator_file || null,
      };
    });
}

// ---------------------------------------------------------------------------
// Markdown fallback (for backward compatibility)
// ---------------------------------------------------------------------------

function parseMdRoutingTable() {
  if (!existsSync(ROUTING_MD_PATH)) return [];
  const md = readFileSync(ROUTING_MD_PATH, "utf-8");
  const entries = [];
  let inTable = false;

  for (const line of md.split("\n")) {
    const trimmed = line.trim();
    if (trimmed.startsWith("| User says")) { inTable = true; continue; }
    if (inTable && trimmed.startsWith("|---")) continue;
    if (inTable && !trimmed.startsWith("|")) {
      if (trimmed === "") continue;
      if (trimmed.startsWith("#") || trimmed.startsWith(">")) { inTable = false; continue; }
      continue;
    }
    if (!inTable) continue;
    const cells = trimmed.split("|").map((c) => c.trim()).filter((c) => c.length > 0);
    if (cells.length < 2) continue;
    const slugMatch = cells[1].match(/`\/([^`]+)`/);
    if (!slugMatch) continue;
    entries.push({
      slug: slugMatch[1],
      displayName: slugMatch[1].replace(/-/g, " "),
      status: "stable",
      domain: "unknown",
      triggers: cells[0],
      inputArtifacts: [],
      downstreamItems: [],
      tokens: tokenize(cells[0].replace(/"/g, "").toLowerCase()),
      calculatorFile: null,
    });
  }
  return entries;
}

// ---------------------------------------------------------------------------
// Tokenization and scoring
// ---------------------------------------------------------------------------

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s/-]/g, " ")
    .split(/\s+/)
    .filter((t) => t.length > 1 && !STOP_WORDS.has(t));
}

/**
 * Score a query against a routing entry.
 * Combines token overlap, artifact matching, and status weighting.
 */
function scoreEntry(queryTokens, entry, artifactFilter) {
  if (queryTokens.length === 0 || entry.tokens.length === 0) return { score: 0, reason: "" };

  const entrySet = new Set(entry.tokens);
  let matchCount = 0;
  let partialCount = 0;
  const matchedTokens = [];

  for (const qt of queryTokens) {
    if (entrySet.has(qt)) {
      matchCount += 1;
      matchedTokens.push(qt);
    } else {
      for (const et of entry.tokens) {
        if (et.startsWith(qt) || qt.startsWith(et)) {
          partialCount += 0.6;
          matchedTokens.push(`~${qt}`);
          break;
        }
      }
    }
  }

  const queryCoverage = (matchCount + partialCount) / queryTokens.length;
  const entryCoverage = matchCount / Math.min(entry.tokens.length, 10);
  let baseScore = queryCoverage * 0.7 + entryCoverage * 0.3;

  // Artifact bonus: if query mentions an artifact type this skill accepts
  let artifactBonus = 0;
  if (artifactFilter && entry.inputArtifacts.length > 0) {
    const filterLower = artifactFilter.toLowerCase();
    for (const artifact of entry.inputArtifacts) {
      if (artifact.toLowerCase().includes(filterLower) || filterLower.includes(artifact.toLowerCase())) {
        artifactBonus = 0.15;
        break;
      }
    }
  }

  // Stable items get a small boost over experimental
  const statusBoost = entry.status === "stable" ? 0.02 : 0;

  const finalScore = Math.min(1, baseScore + artifactBonus + statusBoost);
  const reason = matchedTokens.length > 0
    ? `Matched: ${matchedTokens.slice(0, 4).join(", ")}${artifactBonus > 0 ? " + artifact match" : ""}`
    : "";

  return { score: Math.round(finalScore * 1000) / 1000, reason };
}

function confidenceLevel(topScore) {
  if (topScore >= 0.6) return "high";
  if (topScore >= 0.35) return "medium";
  if (topScore >= 0.15) return "low";
  return "none";
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

function cmdList(entries) {
  const slugs = [...new Set(entries.map((e) => e.slug))].sort();
  console.log(JSON.stringify({ skills: slugs, count: slugs.length }, null, 2));
}

function cmdMatch(query, entries, artifactFilter) {
  const queryTokens = tokenize(query);
  if (queryTokens.length === 0) {
    console.log(JSON.stringify({ error: "Query produced no searchable tokens", query }, null, 2));
    process.exit(1);
  }

  const scored = entries
    .map((entry) => {
      const { score, reason } = scoreEntry(queryTokens, entry, artifactFilter);
      return { ...entry, score, reason };
    })
    .filter((e) => e.score > 0)
    .sort((a, b) => b.score - a.score);

  // Deduplicate by slug
  const seen = new Set();
  const deduped = scored.filter((item) => {
    if (seen.has(item.slug)) return false;
    seen.add(item.slug);
    return true;
  });

  const top3 = deduped.slice(0, 3);
  const topScore = top3.length > 0 ? top3[0].score : 0;

  const result = {
    query,
    tokens: queryTokens,
    artifact_filter: artifactFilter || null,
    recommendation: top3.length > 0 ? {
      skill: top3[0].slug,
      invoke: `/${top3[0].slug}`,
      display_name: top3[0].displayName,
      score: top3[0].score,
      reason: top3[0].reason,
      has_calculator: !!top3[0].calculatorFile,
      downstream: top3[0].downstreamItems.slice(0, 3),
    } : null,
    alternatives: top3.slice(1).map((m) => ({
      skill: m.slug,
      invoke: `/${m.slug}`,
      display_name: m.displayName,
      score: m.score,
      reason: m.reason,
    })),
    confidence: confidenceLevel(topScore),
    source: existsSync(CATALOG_PATH) ? "catalog" : "routing-md-fallback",
    total_skills_searched: entries.length,
  };

  console.log(JSON.stringify(result, null, 2));
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);
  const includeHidden = args.includes("--include-hidden");
  const artifactIdx = args.indexOf("--artifact");
  const artifactFilter = artifactIdx >= 0 && args[artifactIdx + 1] ? args[artifactIdx + 1] : null;

  // Load from catalog (primary) or fallback to markdown
  const catalog = loadCatalog();
  let entries;
  if (catalog) {
    entries = catalogToEntries(catalog, includeHidden);
  } else {
    entries = parseMdRoutingTable();
    if (entries.length === 0) {
      console.error(JSON.stringify({ error: "No catalog or routing entries found" }));
      process.exit(1);
    }
  }

  if (args.includes("--list")) {
    cmdList(entries);
    return;
  }

  const query = args
    .filter((a) => !a.startsWith("--") && (artifactIdx < 0 || args.indexOf(a) !== artifactIdx + 1))
    .join(" ")
    .trim();

  if (!query) {
    console.error(JSON.stringify({
      error: "No query provided",
      usage: 'node routing/skill-dispatcher.mjs "underwrite a deal"',
      flags: "--list: print all skill slugs, --include-hidden: include stub/experimental, --artifact <type>: filter by input artifact",
    }));
    process.exit(1);
  }

  cmdMatch(query, entries, artifactFilter);
}

main();
