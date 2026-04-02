#!/usr/bin/env node
/**
 * workspace-state.mjs — Persistent workspace state manager
 *
 * Local JSON storage for CRE workspace continuity across sessions.
 * No external dependencies. Node stdlib only.
 *
 * Usage:
 *   node scripts/workspace-state.mjs create --type deal --name "123 Main St" --stage screening
 *   node scripts/workspace-state.mjs get <workspace_id>
 *   node scripts/workspace-state.mjs update <workspace_id> --stage underwriting --fact "NOI: $2.6M"
 *   node scripts/workspace-state.mjs list
 *   node scripts/workspace-state.mjs list --type deal
 *   node scripts/workspace-state.mjs delete <workspace_id>
 *   node scripts/workspace-state.mjs add-artifact <workspace_id> --name "IC Memo" --path "./ic-memo.md"
 *   node scripts/workspace-state.mjs add-action <workspace_id> --action "Run sensitivity analysis"
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { randomUUID } from "node:crypto";
import { homedir } from "node:os";

const WORKSPACE_DIR = join(homedir(), ".cre-skills", "workspaces");

// ---------------------------------------------------------------------------
// Schema
// ---------------------------------------------------------------------------

/**
 * @typedef {Object} Workspace
 * @property {string} workspace_id
 * @property {string} workspace_type - deal, asset, fund, lease, loan, project
 * @property {string} entity_name
 * @property {string} stage
 * @property {Object<string,string>} facts
 * @property {Object<string,string>} assumptions
 * @property {string[]} missing_inputs
 * @property {Array<{name: string, path: string, created_at: string}>} artifacts
 * @property {Array<{decision: string, rationale: string, timestamp: string}>} decision_log
 * @property {string[]} next_actions
 * @property {string} last_skill
 * @property {string} created_at
 * @property {string} updated_at
 */

function createWorkspace(type, name, stage) {
  const now = new Date().toISOString();
  return {
    workspace_id: `ws_${randomUUID().slice(0, 8)}`,
    workspace_type: type,
    entity_name: name,
    stage: stage || "intake",
    facts: {},
    assumptions: {},
    missing_inputs: [],
    artifacts: [],
    decision_log: [],
    next_actions: [],
    last_skill: null,
    created_at: now,
    updated_at: now,
  };
}

// ---------------------------------------------------------------------------
// Storage
// ---------------------------------------------------------------------------

function ensureDir() {
  mkdirSync(WORKSPACE_DIR, { recursive: true });
}

function wsPath(id) {
  return join(WORKSPACE_DIR, `${id}.json`);
}

function readWorkspace(id) {
  const p = wsPath(id);
  if (!existsSync(p)) return null;
  try {
    return JSON.parse(readFileSync(p, "utf-8"));
  } catch {
    return null;
  }
}

function writeWorkspace(ws) {
  ensureDir();
  ws.updated_at = new Date().toISOString();
  writeFileSync(wsPath(ws.workspace_id), JSON.stringify(ws, null, 2) + "\n", "utf-8");
}

function listWorkspaces(typeFilter) {
  ensureDir();
  const files = readdirSync(WORKSPACE_DIR).filter((f) => f.endsWith(".json"));
  const workspaces = files
    .map((f) => {
      try {
        return JSON.parse(readFileSync(join(WORKSPACE_DIR, f), "utf-8"));
      } catch {
        return null;
      }
    })
    .filter(Boolean);

  if (typeFilter) {
    return workspaces.filter((w) => w.workspace_type === typeFilter);
  }
  return workspaces;
}

function deleteWorkspace(id) {
  const p = wsPath(id);
  if (existsSync(p)) {
    unlinkSync(p);
    return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function parseArgs(args) {
  const result = { _: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      result[key] = args[i + 1] || true;
      i++;
    } else {
      result._.push(args[i]);
    }
  }
  return result;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];

  switch (cmd) {
    case "create": {
      const type = args.type || "deal";
      const name = args.name || "Untitled";
      const stage = args.stage || "intake";
      const ws = createWorkspace(type, name, stage);
      writeWorkspace(ws);
      console.log(JSON.stringify(ws, null, 2));
      break;
    }

    case "get": {
      const id = args._[1];
      if (!id) {
        console.error(JSON.stringify({ error: "workspace_id required" }));
        process.exit(1);
      }
      const ws = readWorkspace(id);
      if (!ws) {
        console.error(JSON.stringify({ error: `Workspace ${id} not found` }));
        process.exit(1);
      }
      console.log(JSON.stringify(ws, null, 2));
      break;
    }

    case "update": {
      const id = args._[1];
      if (!id) {
        console.error(JSON.stringify({ error: "workspace_id required" }));
        process.exit(1);
      }
      const ws = readWorkspace(id);
      if (!ws) {
        console.error(JSON.stringify({ error: `Workspace ${id} not found` }));
        process.exit(1);
      }
      if (args.stage) ws.stage = args.stage;
      if (args.fact) {
        const [k, ...v] = args.fact.split(":");
        ws.facts[k.trim()] = v.join(":").trim();
      }
      if (args.assumption) {
        const [k, ...v] = args.assumption.split(":");
        ws.assumptions[k.trim()] = v.join(":").trim();
      }
      if (args.missing) {
        ws.missing_inputs.push(args.missing);
      }
      if (args.last_skill) ws.last_skill = args.last_skill;
      if (args.decision) {
        ws.decision_log.push({
          decision: args.decision,
          rationale: args.rationale || "",
          timestamp: new Date().toISOString(),
        });
      }
      writeWorkspace(ws);
      console.log(JSON.stringify(ws, null, 2));
      break;
    }

    case "list": {
      const workspaces = listWorkspaces(args.type);
      const summary = workspaces.map((w) => ({
        workspace_id: w.workspace_id,
        type: w.workspace_type,
        name: w.entity_name,
        stage: w.stage,
        last_skill: w.last_skill,
        updated_at: w.updated_at,
      }));
      console.log(JSON.stringify({ count: summary.length, workspaces: summary }, null, 2));
      break;
    }

    case "delete": {
      const id = args._[1];
      if (!id) {
        console.error(JSON.stringify({ error: "workspace_id required" }));
        process.exit(1);
      }
      const deleted = deleteWorkspace(id);
      console.log(JSON.stringify({ deleted, workspace_id: id }));
      break;
    }

    case "add-artifact": {
      const id = args._[1];
      if (!id) {
        console.error(JSON.stringify({ error: "workspace_id required" }));
        process.exit(1);
      }
      const ws = readWorkspace(id);
      if (!ws) {
        console.error(JSON.stringify({ error: `Workspace ${id} not found` }));
        process.exit(1);
      }
      ws.artifacts.push({
        name: args.name || "unnamed",
        path: args.path || "",
        created_at: new Date().toISOString(),
      });
      writeWorkspace(ws);
      console.log(JSON.stringify(ws, null, 2));
      break;
    }

    case "add-action": {
      const id = args._[1];
      if (!id) {
        console.error(JSON.stringify({ error: "workspace_id required" }));
        process.exit(1);
      }
      const ws = readWorkspace(id);
      if (!ws) {
        console.error(JSON.stringify({ error: `Workspace ${id} not found` }));
        process.exit(1);
      }
      if (args.action) ws.next_actions.push(args.action);
      writeWorkspace(ws);
      console.log(JSON.stringify(ws, null, 2));
      break;
    }

    default:
      console.error(JSON.stringify({
        error: "Unknown command",
        usage: "create | get <id> | update <id> | list | delete <id> | add-artifact <id> | add-action <id>",
      }));
      process.exit(1);
  }
}

main();
