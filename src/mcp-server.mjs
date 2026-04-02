#!/usr/bin/env node
/**
 * CRE Skills Plugin -- MCP Server (stdio)
 *
 * Zero-dependency Model Context Protocol server that exposes the CRE skills
 * catalog, router, and workspace state as tools for Claude Desktop.
 *
 * Protocol: JSON-RPC 2.0 over stdin/stdout (MCP stdio transport)
 *
 * Tools (21):
 *   cre_route          - Route a CRE query to the right skill
 *   cre_list_skills    - List available skills with optional filter
 *   cre_skill_detail   - Get full SKILL.md content (resolves local overrides first)
 *   cre_workspace_create - Create a persistent workspace
 *   cre_workspace_get    - Get workspace state
 *   cre_workspace_list   - List all workspaces
 *   cre_workspace_update - Update workspace state
 *   cre_send_feedback    - Submit feedback or bug report
 *   cre_customize_skill  - Initialize a local skill customization
 *   cre_save_customization - Save customization content and metadata
 *   cre_list_customizations - List all active local customizations
 *   cre_customization_detail - Get customization metadata and diff
 *   cre_revert_customization - Remove a local customization
 *   cre_submit_customization_feedback - Submit structured customization feedback
 *   cre_export_customization - Export customization as portable bundle
 *   cre_import_customization - Import customization from bundle
 *   cre_customization_health_check - Check for base skill drift
 *   cre_list_templates   - List available customization templates
 *   cre_apply_template   - Apply a pre-built customization template
 *   cre_upstream_suggestion - Generate upstream improvement suggestion
 *   cre_customization_analytics - Analyze customization patterns
 */

import { readFileSync, writeFileSync, appendFileSync, mkdirSync, existsSync, readdirSync, unlinkSync } from "node:fs";
import { dirname, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { createInterface } from "node:readline";
import { randomUUID } from "node:crypto";
import { homedir } from "node:os";
import {
  hasCustomization, createCustomization, saveCustomization,
  getCustomization, listCustomizations, revertCustomization,
  resolveSkillPath, CHANGE_CATEGORIES,
  exportCustomization, importCustomization, healthCheck, healthCheckAll,
  listTemplates, createFromTemplate,
} from "./lib/customization.mjs";
import { computeDiff, summarizeDiff, formatDiffText } from "./lib/diff.mjs";
import {
  buildPayload, filterByMode, previewPayload,
  savePayloadLocally, enqueueForRetry, getCustomizationConfig,
  buildUpstreamSuggestion, analyzeCustomizationFeedback,
} from "./lib/feedback-payload.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// In installed plugin: dist/ is at same level as mcp-server.mjs
// In repo: dist/ is at repo root (two levels up from src/)
const CATALOG_PATH = existsSync(join(__dirname, "dist", "catalog.json"))
  ? join(__dirname, "dist", "catalog.json")
  : join(__dirname, "..", "dist", "catalog.json");
const SKILLS_DIR = join(__dirname, "skills");
const WORKSPACE_DIR = join(homedir(), ".cre-skills", "workspaces");
const CONFIG_DIR = join(homedir(), ".cre-skills");

// ---------------------------------------------------------------------------
// Catalog
// ---------------------------------------------------------------------------

let catalogCache = null;

function loadCatalog() {
  if (catalogCache) return catalogCache;
  if (!existsSync(CATALOG_PATH)) {
    // Try building from catalog.yaml
    const yamlPath = join(__dirname, "catalog", "catalog.yaml");
    if (!existsSync(yamlPath)) return { items: [] };
    return { items: [] };
  }
  catalogCache = JSON.parse(readFileSync(CATALOG_PATH, "utf-8"));
  return catalogCache;
}

// ---------------------------------------------------------------------------
// Stop words + tokenizer (shared with router)
// ---------------------------------------------------------------------------

const STOP_WORDS = new Set([
  "a","an","the","this","that","is","it","in","on","at","to","for","of",
  "with","and","or","my","me","i","we","our","do","does","can","how",
  "what","should","would","could","please","help","want","need","like",
]);

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s/-]/g, " ").split(/\s+/)
    .filter(t => t.length > 1 && !STOP_WORDS.has(t));
}

function scoreEntry(queryTokens, entryTokens) {
  if (!queryTokens.length || !entryTokens.length) return 0;
  const entrySet = new Set(entryTokens);
  let match = 0, partial = 0;
  for (const qt of queryTokens) {
    if (entrySet.has(qt)) { match++; }
    else { for (const et of entryTokens) { if (et.startsWith(qt) || qt.startsWith(et)) { partial += 0.6; break; } } }
  }
  return (match + partial) / queryTokens.length * 0.7 + match / Math.min(entryTokens.length, 10) * 0.3;
}

// ---------------------------------------------------------------------------
// Workspace path safety
// ---------------------------------------------------------------------------

function assertSafeWorkspaceId(id) {
  if (!id || typeof id !== 'string') throw new Error('workspace_id is required');
  if (/[\/\\]/.test(id) || id.includes('..')) throw new Error('Invalid workspace_id');
  const resolved = resolve(WORKSPACE_DIR, `${id}.json`);
  if (!resolved.startsWith(resolve(WORKSPACE_DIR) + sep)) {
    throw new Error('workspace_id escapes directory');
  }
}

// ---------------------------------------------------------------------------
// Tool implementations
// ---------------------------------------------------------------------------

function toolRoute(args) {
  const query = args.query || "";
  const catalog = loadCatalog();
  const queryTokens = tokenize(query);
  if (!queryTokens.length) return { error: "Query produced no searchable tokens" };

  const skills = catalog.items
    .filter(i => i.type === "skill" && !i.hidden_from_default_catalog)
    .map(item => {
      const allText = [...(item.intent_triggers || []), ...(item.aliases || []),
        item.display_name, item.id.replace(/-/g, " "), item.persona || ""].join(" ");
      const score = scoreEntry(queryTokens, tokenize(allText));
      return { ...item, score };
    })
    .filter(s => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5);

  const top = skills[0];
  return {
    recommendation: top ? {
      skill: top.id, display_name: top.display_name,
      score: Math.round(top.score * 1000) / 1000,
      downstream: (top.downstream_items || []).slice(0, 3),
    } : null,
    alternatives: skills.slice(1, 4).map(s => ({
      skill: s.id, display_name: s.display_name,
      score: Math.round(s.score * 1000) / 1000,
    })),
    confidence: top ? (top.score >= 0.6 ? "high" : top.score >= 0.35 ? "medium" : "low") : "none",
  };
}

function toolListSkills(args) {
  const catalog = loadCatalog();
  const filter = (args.filter || "").toLowerCase();
  const typeFilter = args.type || "skill";
  let items = catalog.items.filter(i => i.type === typeFilter);
  if (!args.include_hidden) items = items.filter(i => !i.hidden_from_default_catalog);
  if (filter) items = items.filter(i =>
    i.id.includes(filter) || i.display_name.toLowerCase().includes(filter) ||
    (i.lifecycle_phase || "").includes(filter));
  return {
    count: items.length,
    items: items.map(i => ({ id: i.id, display_name: i.display_name, phase: i.lifecycle_phase, status: i.status })),
  };
}

function toolSkillDetail(args) {
  const slug = args.slug || "";
  const { path, source } = resolveSkillPath(slug, SKILLS_DIR);
  if (!existsSync(path)) return { error: `Skill '${slug}' not found` };
  return { slug, content: readFileSync(path, "utf-8"), source };
}

function toolWorkspaceCreate(args) {
  mkdirSync(WORKSPACE_DIR, { recursive: true });
  const ws = {
    workspace_id: `ws_${randomUUID().slice(0, 8)}`,
    workspace_type: args.type || "deal",
    entity_name: args.name || "Untitled",
    stage: args.stage || "intake",
    facts: {}, assumptions: {}, missing_inputs: [], artifacts: [],
    decision_log: [], next_actions: [], last_skill: null,
    created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
  };
  writeFileSync(join(WORKSPACE_DIR, `${ws.workspace_id}.json`), JSON.stringify(ws, null, 2) + "\n");
  return ws;
}

function toolWorkspaceGet(args) {
  try { assertSafeWorkspaceId(args.workspace_id); } catch (e) { return { error: e.message }; }
  const p = join(WORKSPACE_DIR, `${args.workspace_id}.json`);
  if (!existsSync(p)) return { error: `Workspace ${args.workspace_id} not found` };
  return JSON.parse(readFileSync(p, "utf-8"));
}

function toolWorkspaceList(args) {
  mkdirSync(WORKSPACE_DIR, { recursive: true });
  const files = readdirSync(WORKSPACE_DIR).filter(f => f.endsWith(".json"));
  const workspaces = files.map(f => {
    try { return JSON.parse(readFileSync(join(WORKSPACE_DIR, f), "utf-8")); } catch { return null; }
  }).filter(Boolean);
  const filtered = args.type ? workspaces.filter(w => w.workspace_type === args.type) : workspaces;
  return {
    count: filtered.length,
    workspaces: filtered.map(w => ({
      workspace_id: w.workspace_id, type: w.workspace_type, name: w.entity_name,
      stage: w.stage, last_skill: w.last_skill, updated_at: w.updated_at,
    })),
  };
}

function toolWorkspaceUpdate(args) {
  try { assertSafeWorkspaceId(args.workspace_id); } catch (e) { return { error: e.message }; }
  const p = join(WORKSPACE_DIR, `${args.workspace_id}.json`);
  if (!existsSync(p)) return { error: `Workspace ${args.workspace_id} not found` };
  const ws = JSON.parse(readFileSync(p, "utf-8"));
  if (args.stage) ws.stage = args.stage;
  if (args.last_skill) ws.last_skill = args.last_skill;
  if (args.fact_key && args.fact_value) ws.facts[args.fact_key] = args.fact_value;
  if (args.decision) {
    ws.decision_log.push({ decision: args.decision, rationale: args.rationale || "", timestamp: new Date().toISOString() });
  }
  if (args.next_action) ws.next_actions.push(args.next_action);
  ws.updated_at = new Date().toISOString();
  writeFileSync(p, JSON.stringify(ws, null, 2) + "\n");
  return ws;
}

function toolSendFeedback(args) {
  mkdirSync(CONFIG_DIR, { recursive: true });
  const record = {
    submission_id: `fb_${randomUUID().replace(/-/g, "").slice(0, 16)}`,
    submission_type: args.type || "general",
    timestamp: new Date().toISOString(),
    plugin_version: "4.0.0",
    message: (args.message || "").slice(0, 5000),
    rating: args.rating || null,
    severity: args.severity || null,
    skill_slug: args.skill_slug || null,
  };
  appendFileSync(join(CONFIG_DIR, "feedback-log.jsonl"), JSON.stringify(record) + "\n");
  return { saved: true, submission_id: record.submission_id };
}

// ---------------------------------------------------------------------------
// Skill customization tools
// ---------------------------------------------------------------------------

function toolCustomizeSkill(args) {
  const slug = args.slug || "";
  if (hasCustomization(slug)) {
    return { error: `Customization already exists for '${slug}'. Use cre_save_customization to update or cre_revert_customization to start fresh.` };
  }
  const basePath = join(SKILLS_DIR, slug, "SKILL.md");
  if (!existsSync(basePath)) return { error: `Skill '${slug}' not found in base catalog` };
  const baseContent = readFileSync(basePath, "utf-8");
  const record = createCustomization(slug, baseContent, SERVER_INFO.version);
  return { ...record, message: `Customization initialized for '${slug}'. Use cre_save_customization to save changes.` };
}

function toolSaveCustomization(args) {
  const slug = args.slug || "";
  if (!hasCustomization(slug)) return { error: `No customization exists for '${slug}'. Use cre_customize_skill first.` };
  const content = args.content;
  if (!content) return { error: "content is required" };
  const updates = {};
  if (args.rationale !== undefined) updates.rationale = args.rationale;
  if (args.change_categories !== undefined) updates.change_categories = args.change_categories;
  if (args.notes !== undefined) updates.notes = args.notes;
  const record = saveCustomization(slug, content, updates);
  return { ...record, message: `Customization saved for '${slug}'.` };
}

function toolListCustomizations() {
  const items = listCustomizations();
  return { count: items.length, customizations: items };
}

function toolCustomizationDetail(args) {
  const slug = args.slug || "";
  const cust = getCustomization(slug);
  if (!cust) return { error: `No customization found for '${slug}'` };
  let diffResult = null, diffSummary = null, diffText = null;
  if (cust.base) {
    diffResult = computeDiff(cust.base, cust.content);
    diffSummary = summarizeDiff(diffResult);
    diffText = formatDiffText(diffResult);
  }
  return {
    slug,
    metadata: cust.metadata,
    diff_summary: diffSummary,
    diff_text: args.include_diff ? diffText : null,
    diff_stats: diffResult ? diffResult.stats : null,
    sections_changed: diffResult ? diffResult.sections_changed : null,
    content: args.include_content ? cust.content : null,
    base_content: args.include_base ? cust.base : null,
  };
}

function toolRevertCustomization(args) {
  const slug = args.slug || "";
  const removed = revertCustomization(slug);
  if (!removed) return { error: `No customization found for '${slug}'` };
  return { slug, reverted: true, message: `Customization for '${slug}' removed. Base skill is now active.` };
}

function toolSubmitCustomizationFeedback(args) {
  const slug = args.slug || "";
  const cust = getCustomization(slug);
  if (!cust) return { error: `No customization found for '${slug}'` };
  const config = getCustomizationConfig();
  if (!config.feedback_enabled || config.feedback_mode === "off") {
    return { error: "Customization feedback is disabled in config" };
  }
  let diffResult = null, diffSummaryText = null, diffTextStr = null;
  if (cust.base) {
    diffResult = computeDiff(cust.base, cust.content);
    diffSummaryText = summarizeDiff(diffResult);
    diffTextStr = formatDiffText(diffResult);
  }
  const payload = buildPayload({
    metadata: cust.metadata,
    diffSummary: diffSummaryText || "",
    diffText: diffTextStr || "",
    modifiedContent: cust.content,
    diffStats: diffResult ? diffResult.stats : {},
    sectionsChanged: diffResult ? diffResult.sections_changed : [],
    pluginVersion: SERVER_INFO.version,
    wantsUpstreamConsideration: args.wants_upstream ?? false,
    consentedToContent: args.consented_to_content ?? false,
  });
  const filtered = filterByMode(payload, config.feedback_mode);

  // Enforce require_consent: return preview for caller to show user first
  if (config.require_consent && !args.user_confirmed) {
    return {
      requires_consent: true,
      preview: previewPayload(filtered, config.feedback_mode),
      feedback_id: filtered.feedback_id,
      message: "User must confirm before sending. Call again with user_confirmed: true after showing preview.",
    };
  }

  if (args.dry_run || config.dry_run) {
    return { preview: previewPayload(filtered, config.feedback_mode), dry_run: true, payload: filtered };
  }
  savePayloadLocally(filtered);
  if (config.feedback_endpoint) {
    enqueueForRetry(filtered);
    return { saved: true, queued_for_remote: true, feedback_id: filtered.feedback_id, preview: previewPayload(filtered, config.feedback_mode) };
  }
  return { saved: true, queued_for_remote: false, feedback_id: filtered.feedback_id, preview: previewPayload(filtered, config.feedback_mode) };
}

function toolExportCustomization(args) {
  const slug = args.slug || "";
  const bundle = exportCustomization(slug);
  if (!bundle) return { error: `No customization found for '${slug}'` };
  return bundle;
}

function toolImportCustomization(args) {
  if (!args.bundle) return { error: "bundle is required (JSON object)" };
  try {
    const bundle = typeof args.bundle === "string" ? JSON.parse(args.bundle) : args.bundle;
    const result = importCustomization(bundle);
    return { ...result, message: `Customization imported for '${result.slug}'.` };
  } catch (err) {
    return { error: err.message };
  }
}

function toolHealthCheck(args) {
  if (args.all) {
    return { results: healthCheckAll(SKILLS_DIR) };
  }
  const slug = args.slug || "";
  return healthCheck(slug, SKILLS_DIR);
}

function toolListTemplates() {
  const TEMPLATES_DIR = join(__dirname, "templates");
  return { templates: listTemplates(TEMPLATES_DIR) };
}

function toolApplyTemplate(args) {
  const templateId = args.template_id || "";
  const TEMPLATES_DIR = join(__dirname, "templates");
  try {
    const record = createFromTemplate(templateId, SKILLS_DIR, TEMPLATES_DIR, SERVER_INFO.version);
    return { ...record, message: `Template '${templateId}' applied to '${record.skill_slug}'.` };
  } catch (err) {
    return { error: err.message };
  }
}

function toolUpstreamSuggestion(args) {
  const slug = args.slug || "";
  const cust = getCustomization(slug);
  if (!cust) return { error: `No customization found for '${slug}'` };
  let diffSummaryText = "", diffTextStr = "";
  if (cust.base) {
    const diffResult = computeDiff(cust.base, cust.content);
    diffSummaryText = summarizeDiff(diffResult);
    diffTextStr = formatDiffText(diffResult);
  }
  return buildUpstreamSuggestion(cust.metadata, diffSummaryText, diffTextStr);
}

function toolCustomizationAnalytics() {
  return analyzeCustomizationFeedback();
}

// ---------------------------------------------------------------------------
// Tool registry
// ---------------------------------------------------------------------------

const TOOLS = [
  {
    name: "cre_route",
    description: "Route a CRE query to the right specialist skill. Returns the best match with confidence score and alternatives.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "The CRE task or question to route (e.g. 'underwrite a deal', 'screen this OM', 'size a loan')" },
      },
      required: ["query"],
    },
  },
  {
    name: "cre_list_skills",
    description: "List available CRE skills with optional filtering by name, phase, or type.",
    inputSchema: {
      type: "object",
      properties: {
        filter: { type: "string", description: "Filter skills by name, slug, or lifecycle phase" },
        type: { type: "string", enum: ["skill", "agent", "calculator", "orchestrator", "workflow"], description: "Item type to list (default: skill)" },
        include_hidden: { type: "boolean", description: "Include stub/experimental items" },
      },
    },
  },
  {
    name: "cre_skill_detail",
    description: "Get the full SKILL.md content for a specific skill, including its process, inputs, outputs, and chain connections.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "The skill slug (e.g. 'deal-quick-screen', 'acquisition-underwriting-engine')" },
      },
      required: ["slug"],
    },
  },
  {
    name: "cre_workspace_create",
    description: "Create a persistent workspace for tracking a deal, asset, fund, or project across sessions.",
    inputSchema: {
      type: "object",
      properties: {
        type: { type: "string", enum: ["deal", "asset", "fund", "lease", "loan", "project"], description: "Workspace type" },
        name: { type: "string", description: "Entity name (e.g. '240-Unit Raleigh MF')" },
        stage: { type: "string", description: "Current stage (e.g. 'screening', 'underwriting', 'closing')" },
      },
      required: ["name"],
    },
  },
  {
    name: "cre_workspace_get",
    description: "Get the current state of a workspace by ID.",
    inputSchema: {
      type: "object",
      properties: {
        workspace_id: { type: "string", description: "Workspace ID (e.g. 'ws_abc12345')" },
      },
      required: ["workspace_id"],
    },
  },
  {
    name: "cre_workspace_list",
    description: "List all active workspaces, optionally filtered by type.",
    inputSchema: {
      type: "object",
      properties: {
        type: { type: "string", enum: ["deal", "asset", "fund", "lease", "loan", "project"], description: "Filter by workspace type" },
      },
    },
  },
  {
    name: "cre_workspace_update",
    description: "Update a workspace with new stage, facts, decisions, or next actions.",
    inputSchema: {
      type: "object",
      properties: {
        workspace_id: { type: "string", description: "Workspace ID" },
        stage: { type: "string", description: "New stage" },
        last_skill: { type: "string", description: "Last skill used" },
        fact_key: { type: "string", description: "Fact key to add/update" },
        fact_value: { type: "string", description: "Fact value" },
        decision: { type: "string", description: "Decision to log" },
        rationale: { type: "string", description: "Rationale for decision" },
        next_action: { type: "string", description: "Next action to add" },
      },
      required: ["workspace_id"],
    },
  },
  {
    name: "cre_send_feedback",
    description: "Submit feedback or a bug report about a CRE skill.",
    inputSchema: {
      type: "object",
      properties: {
        message: { type: "string", description: "Feedback message" },
        type: { type: "string", enum: ["general", "bug", "feature"], description: "Feedback type" },
        rating: { type: "number", description: "Rating 1-5" },
        severity: { type: "string", enum: ["low", "medium", "high", "critical"], description: "Bug severity" },
        skill_slug: { type: "string", description: "Related skill slug" },
      },
      required: ["message"],
    },
  },
  // ── Skill customization tools ──────────────────────────────────────────────
  {
    name: "cre_customize_skill",
    description: "Initialize a local customization of a CRE skill. Creates an editable override copy without modifying the base skill. Returns the customization record.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug to customize (e.g. 'deal-quick-screen')" },
      },
      required: ["slug"],
    },
  },
  {
    name: "cre_save_customization",
    description: "Save updated content and metadata for an existing skill customization.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug" },
        content: { type: "string", description: "The full modified SKILL.md content" },
        rationale: { type: "string", description: "Why the user made this change" },
        change_categories: {
          type: "array",
          items: { type: "string", enum: CHANGE_CATEGORIES },
          description: "Category tags: terminology, approval_chain, required_steps, compliance_governance, deliverable_format, tone_style, missing_fields, output_structure, calculation_method, regional_market, other",
        },
        notes: { type: "string", description: "Additional notes" },
      },
      required: ["slug", "content"],
    },
  },
  {
    name: "cre_list_customizations",
    description: "List all active local skill customizations with their status and timestamps.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "cre_customization_detail",
    description: "Get detailed information about a skill customization including metadata, diff summary, and optionally the full diff or content.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug" },
        include_diff: { type: "boolean", description: "Include the full unified diff text" },
        include_content: { type: "boolean", description: "Include the full customized SKILL.md content" },
        include_base: { type: "boolean", description: "Include the original base SKILL.md content" },
      },
      required: ["slug"],
    },
  },
  {
    name: "cre_revert_customization",
    description: "Remove a local skill customization, restoring the base skill as the active version.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug to revert" },
      },
      required: ["slug"],
    },
  },
  {
    name: "cre_submit_customization_feedback",
    description: "Build and submit structured feedback about a skill customization. Respects privacy config. Use dry_run to preview without sending.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug" },
        wants_upstream: { type: "boolean", description: "Whether user wants maintainer to consider incorporating this change" },
        consented_to_content: { type: "boolean", description: "Explicit consent to include full content (only relevant in metadata_and_content mode)" },
        dry_run: { type: "boolean", description: "Preview the payload without sending" },
        user_confirmed: { type: "boolean", description: "Set to true after showing the user a preview and getting their consent. Required when require_consent is enabled." },
      },
      required: ["slug"],
    },
  },
  {
    name: "cre_export_customization",
    description: "Export a skill customization as a portable JSON bundle for sharing with teammates or backup.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug to export" },
      },
      required: ["slug"],
    },
  },
  {
    name: "cre_import_customization",
    description: "Import a skill customization from a JSON bundle previously created by cre_export_customization.",
    inputSchema: {
      type: "object",
      properties: {
        bundle: { type: "object", description: "The customization bundle JSON object" },
      },
      required: ["bundle"],
    },
  },
  {
    name: "cre_customization_health_check",
    description: "Check if base skills have been updated since customizations were created. Detects drift between your customization and the current plugin version.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug to check (omit for all)" },
        all: { type: "boolean", description: "Check all customizations" },
      },
    },
  },
  {
    name: "cre_list_templates",
    description: "List available customization templates -- pre-built starting points for common enterprise needs.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "cre_apply_template",
    description: "Create a customization from a pre-built template. Templates provide common adaptations for specific markets, property types, or regulatory regimes.",
    inputSchema: {
      type: "object",
      properties: {
        template_id: { type: "string", description: "Template identifier" },
      },
      required: ["template_id"],
    },
  },
  {
    name: "cre_upstream_suggestion",
    description: "Generate a structured upstream improvement suggestion from a customization, suitable for filing as a GitHub issue.",
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Skill slug" },
      },
      required: ["slug"],
    },
  },
  {
    name: "cre_customization_analytics",
    description: "Analyze local customization feedback patterns -- which skills are customized most, what categories of changes are common, upstream request rate.",
    inputSchema: { type: "object", properties: {} },
  },
];

const TOOL_HANDLERS = {
  cre_route: toolRoute,
  cre_list_skills: toolListSkills,
  cre_skill_detail: toolSkillDetail,
  cre_workspace_create: toolWorkspaceCreate,
  cre_workspace_get: toolWorkspaceGet,
  cre_workspace_list: toolWorkspaceList,
  cre_workspace_update: toolWorkspaceUpdate,
  cre_send_feedback: toolSendFeedback,
  cre_customize_skill: toolCustomizeSkill,
  cre_save_customization: toolSaveCustomization,
  cre_list_customizations: toolListCustomizations,
  cre_customization_detail: toolCustomizationDetail,
  cre_revert_customization: toolRevertCustomization,
  cre_submit_customization_feedback: toolSubmitCustomizationFeedback,
  cre_export_customization: toolExportCustomization,
  cre_import_customization: toolImportCustomization,
  cre_customization_health_check: toolHealthCheck,
  cre_list_templates: toolListTemplates,
  cre_apply_template: toolApplyTemplate,
  cre_upstream_suggestion: toolUpstreamSuggestion,
  cre_customization_analytics: toolCustomizationAnalytics,
};

// ---------------------------------------------------------------------------
// MCP JSON-RPC server (stdio transport)
// ---------------------------------------------------------------------------

const SERVER_INFO = {
  name: "cre-skills",
  version: "4.0.0",
};

const CAPABILITIES = {
  tools: {},
};

function handleRequest(method, params) {
  switch (method) {
    case "initialize":
      return { protocolVersion: "2024-11-05", capabilities: CAPABILITIES, serverInfo: SERVER_INFO };

    case "notifications/initialized":
      return undefined; // notification, no response

    case "tools/list":
      return { tools: TOOLS };

    case "tools/call": {
      const toolName = params?.name;
      const handler = TOOL_HANDLERS[toolName];
      if (!handler) {
        return { content: [{ type: "text", text: JSON.stringify({ error: `Unknown tool: ${toolName}` }) }], isError: true };
      }
      try {
        const result = handler(params?.arguments || {});
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (err) {
        return { content: [{ type: "text", text: JSON.stringify({ error: err.message }) }], isError: true };
      }
    }

    case "ping":
      return {};

    default:
      throw { code: -32601, message: `Method not found: ${method}` };
  }
}

function sendResponse(id, result) {
  const msg = JSON.stringify({ jsonrpc: "2.0", id, result });
  process.stdout.write(msg + "\n");
}

function sendError(id, code, message) {
  const msg = JSON.stringify({ jsonrpc: "2.0", id, error: { code, message } });
  process.stdout.write(msg + "\n");
}

// Pre-build the catalog on startup
loadCatalog();

const rl = createInterface({ input: process.stdin, terminal: false });

rl.on("line", (line) => {
  if (!line.trim()) return;
  let parsed;
  try {
    parsed = JSON.parse(line);
  } catch {
    sendError(null, -32700, "Parse error");
    return;
  }

  const { id, method, params } = parsed;

  // Notifications (no id) don't get responses
  if (id === undefined || id === null) {
    try { handleRequest(method, params); } catch {}
    return;
  }

  try {
    const result = handleRequest(method, params);
    if (result !== undefined) sendResponse(id, result);
  } catch (err) {
    sendError(id, err.code || -32603, err.message || "Internal error");
  }
});

rl.on("close", () => process.exit(0));
