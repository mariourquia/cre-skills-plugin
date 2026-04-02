/**
 * CRE Skills Plugin -- Skill Customization Engine
 *
 * Manages local overrides of base skills. Users adapt skills to their
 * workplace workflow without modifying shipped files.
 *
 * Storage layout:
 *   ~/.cre-skills/customizations/index.json       -- master index
 *   ~/.cre-skills/customizations/<slug>/SKILL.md   -- editable override
 *   ~/.cre-skills/customizations/<slug>/base-snapshot.md -- frozen base copy
 *   ~/.cre-skills/customizations/<slug>/metadata.json    -- structured info
 *
 * Override resolution: customization > base skill
 *
 * Zero external dependencies.
 */

import { readFileSync, writeFileSync, renameSync, mkdirSync, existsSync, rmSync, readdirSync } from "node:fs";
import { join, resolve, sep } from "node:path";
import { homedir, platform } from "node:os";
import { randomUUID } from "node:crypto";
import { contentHash, computeDiff, summarizeDiff } from "./diff.mjs";

const CRE_DIR = join(homedir(), ".cre-skills");
const CUSTOMIZATIONS_DIR = join(CRE_DIR, "customizations");
const INDEX_PATH = join(CUSTOMIZATIONS_DIR, "index.json");

// ── Exports for testing (path overrides) ─────────────────────────────────────

let _customizationsDir = CUSTOMIZATIONS_DIR;
let _indexPath = INDEX_PATH;

export function _setTestPaths(custDir, idxPath) {
  _customizationsDir = custDir;
  _indexPath = idxPath;
}

export function _resetPaths() {
  _customizationsDir = CUSTOMIZATIONS_DIR;
  _indexPath = INDEX_PATH;
}

// ── Slug validation (path traversal prevention) ─────────────────────────────

/**
 * Validate that a slug is safe to use as a directory name.
 * Rejects path separators, dot-segments, and any value that would
 * resolve outside the customizations directory.
 *
 * @param {string} slug
 * @throws {Error} if slug is unsafe
 */
function assertSafeSlug(slug) {
  if (!slug || typeof slug !== "string") {
    throw new Error("slug must be a non-empty string");
  }
  if (/[/\\]/.test(slug) || slug === ".." || slug === "." || slug.includes("..")) {
    throw new Error(`Invalid slug: '${slug}' contains path separators or dot-segments`);
  }
  const resolved = resolve(_customizationsDir, slug);
  if (!resolved.startsWith(_customizationsDir + sep) && resolved !== _customizationsDir) {
    throw new Error(`Slug '${slug}' escapes the customizations directory`);
  }
}

/**
 * Validate a template ID is safe for path construction.
 */
function assertSafeId(id, label = "id") {
  if (!id || typeof id !== "string") {
    throw new Error(`${label} must be a non-empty string`);
  }
  if (/[/\\]/.test(id) || id === ".." || id === "." || id.includes("..")) {
    throw new Error(`Invalid ${label}: '${id}'`);
  }
}

// ── Index management ─────────────────────────────────────────────────────────

export function readIndex() {
  if (!existsSync(_indexPath)) return { customizations: {} };
  try {
    return JSON.parse(readFileSync(_indexPath, "utf-8"));
  } catch {
    return { customizations: {} };
  }
}

function writeIndex(index) {
  mkdirSync(_customizationsDir, { recursive: true });
  const tmp = _indexPath + ".tmp." + randomUUID().slice(0, 8);
  writeFileSync(tmp, JSON.stringify(index, null, 2) + "\n");
  renameSync(tmp, _indexPath);
}

// ── Path helpers ─────────────────────────────────────────────────────────────

function custDir(slug) {
  return join(_customizationsDir, slug);
}

function custSkillPath(slug) {
  return join(custDir(slug), "SKILL.md");
}

function custBasePath(slug) {
  return join(custDir(slug), "base-snapshot.md");
}

function custMetaPath(slug) {
  return join(custDir(slug), "metadata.json");
}

// ── Override resolution ──────────────────────────────────────────────────────

/**
 * Check if a skill has a local customization.
 */
export function hasCustomization(slug) {
  assertSafeSlug(slug);
  return existsSync(custSkillPath(slug));
}

/**
 * Resolve the SKILL.md path: local override first, then base.
 * @param {string} slug
 * @param {string} skillsDir - Path to the plugin's skills/ directory
 * @returns {{ path: string, source: "customized"|"base" }}
 */
export function resolveSkillPath(slug, skillsDir) {
  assertSafeSlug(slug);
  const cp = custSkillPath(slug);
  if (existsSync(cp)) {
    return { path: cp, source: "customized" };
  }
  return { path: join(skillsDir, slug, "SKILL.md"), source: "base" };
}

// ── CRUD ─────────────────────────────────────────────────────────────────────

/**
 * Supported change category tags.
 */
export const CHANGE_CATEGORIES = [
  "terminology",
  "approval_chain",
  "required_steps",
  "compliance_governance",
  "deliverable_format",
  "tone_style",
  "missing_fields",
  "output_structure",
  "calculation_method",
  "regional_market",
  "other",
];

/**
 * Initialize a new customization. Copies the base SKILL.md as both
 * the editable version and a frozen snapshot for later diffing.
 *
 * @param {string} slug
 * @param {string} baseContent - The base SKILL.md content
 * @param {string} pluginVersion
 * @returns {object} Customization metadata record
 */
export function createCustomization(slug, baseContent, pluginVersion = "unknown") {
  assertSafeSlug(slug);
  const dir = custDir(slug);
  mkdirSync(dir, { recursive: true });

  writeFileSync(custSkillPath(slug), baseContent);
  writeFileSync(custBasePath(slug), baseContent);

  const hash = contentHash(baseContent);
  const record = {
    customization_id: `cust_${randomUUID().replace(/-/g, "").slice(0, 12)}`,
    skill_slug: slug,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    base_content_hash: hash,
    modified_content_hash: hash,
    status: "draft",
    rationale: null,
    change_categories: [],
    notes: null,
    plugin_version: pluginVersion,
    platform: platform(),
  };

  writeFileSync(custMetaPath(slug), JSON.stringify(record, null, 2) + "\n");

  const index = readIndex();
  index.customizations[slug] = {
    customization_id: record.customization_id,
    created_at: record.created_at,
    updated_at: record.updated_at,
    status: record.status,
  };
  writeIndex(index);

  return record;
}

/**
 * Save updated content and metadata for an existing customization.
 *
 * @param {string} slug
 * @param {string} content - Modified SKILL.md content
 * @param {object} updates - Partial metadata updates
 * @returns {object} Updated metadata record
 */
export function saveCustomization(slug, content, updates = {}) {
  assertSafeSlug(slug);
  if (!hasCustomization(slug)) {
    throw new Error(`No customization exists for '${slug}'`);
  }

  writeFileSync(custSkillPath(slug), content);

  const meta = readMetadata(slug);
  meta.modified_content_hash = contentHash(content);
  meta.updated_at = new Date().toISOString();
  if (meta.base_content_hash !== meta.modified_content_hash) {
    meta.status = "active";
  }
  if (updates.rationale !== undefined) meta.rationale = updates.rationale;
  if (updates.change_categories !== undefined) meta.change_categories = updates.change_categories;
  if (updates.notes !== undefined) meta.notes = updates.notes;

  writeFileSync(custMetaPath(slug), JSON.stringify(meta, null, 2) + "\n");

  const index = readIndex();
  if (index.customizations[slug]) {
    index.customizations[slug].updated_at = meta.updated_at;
    index.customizations[slug].status = meta.status;
    writeIndex(index);
  }

  return meta;
}

/**
 * Read a customization's content and metadata.
 *
 * @param {string} slug
 * @returns {{ content: string, base: string, metadata: object }|null}
 */
export function getCustomization(slug) {
  assertSafeSlug(slug);
  if (!hasCustomization(slug)) return null;
  return {
    content: readFileSync(custSkillPath(slug), "utf-8"),
    base: existsSync(custBasePath(slug)) ? readFileSync(custBasePath(slug), "utf-8") : null,
    metadata: readMetadata(slug),
  };
}

/**
 * Read metadata for a customization.
 */
export function readMetadata(slug) {
  assertSafeSlug(slug);
  const p = custMetaPath(slug);
  if (!existsSync(p)) return null;
  try {
    return JSON.parse(readFileSync(p, "utf-8"));
  } catch {
    return null;
  }
}

/**
 * List all customizations from the index.
 *
 * @returns {Array<{ slug: string, customization_id: string, status: string, created_at: string, updated_at: string }>}
 */
export function listCustomizations() {
  const index = readIndex();
  return Object.entries(index.customizations).map(([slug, entry]) => ({
    slug,
    ...entry,
  }));
}

/**
 * Remove a customization, restoring the base skill as the active version.
 *
 * @param {string} slug
 * @returns {boolean} true if removed, false if not found
 */
export function revertCustomization(slug) {
  assertSafeSlug(slug);
  const dir = custDir(slug);
  if (!existsSync(dir)) return false;

  rmSync(dir, { recursive: true, force: true });

  const index = readIndex();
  delete index.customizations[slug];
  writeIndex(index);

  return true;
}

/**
 * Read the frozen base snapshot for a customization.
 *
 * @param {string} slug
 * @returns {string|null}
 */
export function getBaseSnapshot(slug) {
  assertSafeSlug(slug);
  const p = custBasePath(slug);
  return existsSync(p) ? readFileSync(p, "utf-8") : null;
}

// ── Export / Import ──────────────────────────────────────────────────────────

const BUNDLE_FORMAT = "cre-skills-customization-v1";

/**
 * Export a customization as a self-contained JSON bundle.
 * Suitable for sharing with teammates or backing up.
 *
 * @param {string} slug
 * @returns {object|null} The bundle, or null if no customization exists
 */
export function exportCustomization(slug) {
  assertSafeSlug(slug);
  const cust = getCustomization(slug);
  if (!cust) return null;
  return {
    format: BUNDLE_FORMAT,
    exported_at: new Date().toISOString(),
    skill_slug: slug,
    metadata: cust.metadata,
    base_content: cust.base,
    customized_content: cust.content,
  };
}

/**
 * Import a customization from a JSON bundle.
 * Overwrites any existing customization for the same slug.
 *
 * @param {object} bundle - A bundle produced by exportCustomization
 * @returns {{ slug: string, customization_id: string, status: string }}
 */
export function importCustomization(bundle) {
  if (!bundle || bundle.format !== BUNDLE_FORMAT) {
    throw new Error(`Invalid bundle format. Expected '${BUNDLE_FORMAT}'.`);
  }
  const slug = bundle.skill_slug;
  if (!slug) throw new Error("Bundle missing skill_slug");
  assertSafeSlug(slug);

  const dir = join(_customizationsDir, slug);
  mkdirSync(dir, { recursive: true });

  writeFileSync(join(dir, "SKILL.md"), bundle.customized_content || "");
  if (bundle.base_content) {
    writeFileSync(join(dir, "base-snapshot.md"), bundle.base_content);
  }

  const meta = bundle.metadata || {};
  meta.customization_id = meta.customization_id || `cust_${randomUUID().replace(/-/g, "").slice(0, 12)}`;
  meta.skill_slug = slug;
  meta.updated_at = new Date().toISOString();
  meta.imported_at = new Date().toISOString();
  meta.base_content_hash = meta.base_content_hash || (bundle.base_content ? contentHash(bundle.base_content) : "unknown");
  meta.modified_content_hash = contentHash(bundle.customized_content || "");
  meta.status = meta.base_content_hash !== meta.modified_content_hash ? "active" : "draft";

  writeFileSync(join(dir, "metadata.json"), JSON.stringify(meta, null, 2) + "\n");

  const index = readIndex();
  index.customizations[slug] = {
    customization_id: meta.customization_id,
    created_at: meta.created_at || meta.updated_at,
    updated_at: meta.updated_at,
    status: meta.status,
    imported: true,
  };
  writeIndex(index);

  return { slug, customization_id: meta.customization_id, status: meta.status };
}

// ── Health Check ─────────────────────────────────────────────────────────────

/**
 * Check if the base skill has changed since the customization was created.
 * Compares the frozen base snapshot with the current base skill file.
 *
 * @param {string} slug
 * @param {string} skillsDir - Path to the plugin's skills/ directory
 * @returns {{ status: "current"|"drifted"|"base_missing"|"no_customization", drift_stats?: object, sections_affected?: string[], message: string }}
 */
export function healthCheck(slug, skillsDir) {
  assertSafeSlug(slug);
  if (!hasCustomization(slug)) {
    return { status: "no_customization", message: `No customization exists for '${slug}'` };
  }

  const currentBasePath = join(skillsDir, slug, "SKILL.md");
  if (!existsSync(currentBasePath)) {
    return { status: "base_missing", message: `Base skill '${slug}' no longer exists in the plugin. Your customization still works but cannot be compared.` };
  }

  const frozenBase = getBaseSnapshot(slug);
  if (!frozenBase) {
    return { status: "current", message: "No base snapshot available for comparison." };
  }

  const currentBase = readFileSync(currentBasePath, "utf-8");
  const frozenHash = contentHash(frozenBase);
  const currentHash = contentHash(currentBase);

  if (frozenHash === currentHash) {
    return { status: "current", message: "Base skill is unchanged since customization was created." };
  }

  const drift = computeDiff(frozenBase, currentBase);
  return {
    status: "drifted",
    message: `Base skill has been updated since your customization (${drift.stats.added} lines added, ${drift.stats.removed} removed). Review your customization to incorporate upstream improvements.`,
    drift_stats: drift.stats,
    drift_summary: summarizeDiff(drift),
    sections_affected: drift.sections_changed,
  };
}

/**
 * Run health check on all customizations.
 *
 * @param {string} skillsDir
 * @returns {Array<{ slug: string, status: string, message: string }>}
 */
export function healthCheckAll(skillsDir) {
  return listCustomizations().map(({ slug }) => ({
    slug,
    ...healthCheck(slug, skillsDir),
  }));
}

// ── Admin Templates ──────────────────────────────────────────────────────────

/**
 * List available customization templates from the plugin's templates directory.
 *
 * @param {string} templatesDir - Path to templates/customizations/ in the plugin
 * @returns {Array<{ id: string, name: string, description: string, target_skill: string, categories: string[] }>}
 */
export function listTemplates(templatesDir) {
  const dir = join(templatesDir, "customizations");
  if (!existsSync(dir)) return [];

  return readdirSync(dir)
    .filter(f => f.endsWith(".json"))
    .map(f => {
      try {
        const tmpl = JSON.parse(readFileSync(join(dir, f), "utf-8"));
        return {
          id: f.replace(".json", ""),
          name: tmpl.name || f,
          description: tmpl.description || "",
          target_skill: tmpl.target_skill || "",
          categories: tmpl.categories || [],
        };
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

/**
 * Create a customization from a template.
 * The template provides pre-filled content modifications and metadata.
 *
 * @param {string} templateId
 * @param {string} skillsDir
 * @param {string} templatesDir
 * @param {string} pluginVersion
 * @returns {object} Customization metadata record
 */
export function createFromTemplate(templateId, skillsDir, templatesDir, pluginVersion = "unknown") {
  assertSafeId(templateId, "template_id");
  const tmplPath = join(templatesDir, "customizations", `${templateId}.json`);
  if (!existsSync(tmplPath)) throw new Error(`Template '${templateId}' not found`);

  const tmpl = JSON.parse(readFileSync(tmplPath, "utf-8"));
  const slug = tmpl.target_skill;
  if (!slug) throw new Error("Template missing target_skill");

  const basePath = join(skillsDir, slug, "SKILL.md");
  if (!existsSync(basePath)) throw new Error(`Base skill '${slug}' not found`);

  // Revert AFTER confirming base exists (prevents data loss if base is missing)
  if (hasCustomization(slug)) revertCustomization(slug);

  const baseContent = readFileSync(basePath, "utf-8");
  const record = createCustomization(slug, baseContent, pluginVersion);

  // Apply template modifications
  let content = baseContent;
  if (tmpl.content) {
    content = tmpl.content;
  } else if (tmpl.replacements) {
    for (const { find, replace } of tmpl.replacements) {
      content = content.replaceAll(find, replace);
    }
  }

  return saveCustomization(slug, content, {
    rationale: tmpl.rationale || `Applied template: ${tmpl.name}`,
    change_categories: tmpl.categories || [],
    notes: `Created from template '${templateId}'`,
  });
}
