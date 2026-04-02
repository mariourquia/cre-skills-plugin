#!/usr/bin/env node
/**
 * CRE Skills Plugin -- MCP Server (stdio)
 *
 * Zero-dependency Model Context Protocol server that exposes the CRE skills
 * catalog, router, and workspace state as tools for Claude Desktop.
 *
 * Protocol: JSON-RPC 2.0 over stdin/stdout (MCP stdio transport)
 *
 * Tools:
 *   cre_route          - Route a CRE query to the right skill
 *   cre_list_skills    - List available skills with optional filter
 *   cre_skill_detail   - Get full SKILL.md content for a skill
 *   cre_workspace_create - Create a persistent workspace
 *   cre_workspace_get    - Get workspace state
 *   cre_workspace_list   - List all workspaces
 *   cre_workspace_update - Update workspace state
 *   cre_send_feedback    - Submit feedback or bug report
 */

import { readFileSync, writeFileSync, appendFileSync, mkdirSync, existsSync, readdirSync, unlinkSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createInterface } from "node:readline";
import { randomUUID } from "node:crypto";
import { homedir } from "node:os";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const CATALOG_PATH = join(__dirname, "dist", "catalog.json");
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
  const skillPath = join(SKILLS_DIR, slug, "SKILL.md");
  if (!existsSync(skillPath)) return { error: `Skill '${slug}' not found` };
  return { slug, content: readFileSync(skillPath, "utf-8") };
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
