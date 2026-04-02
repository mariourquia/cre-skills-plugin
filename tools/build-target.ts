/**
 * Core build function for a single target. Importable by build.ts and test.ts.
 */
import { rmSync, mkdirSync, cpSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import {
  loadTargetProfile,
  buildDir,
  SRC_DIR,
  type TargetName,
} from "./lib.js";
import { normalizeSkills } from "./normalize/skills.js";
import { normalizeAgents } from "./normalize/agents.js";
import { normalizeCommands } from "./normalize/commands.js";
import { normalizeHooks } from "./normalize/hooks.js";
import { normalizeManifest } from "./normalize/manifest.js";
import { normalizeCatalog } from "./normalize/catalog.js";

export function buildTarget(target: TargetName, quiet = false): boolean {
  const profile = loadTargetProfile(target);
  const outDir = buildDir(target);
  const log = quiet ? () => {} : (msg: string) => console.log(msg);

  log(`\nBUILD ${target}`);
  log(`  output: ${outDir}`);

  if (existsSync(outDir)) rmSync(outDir, { recursive: true });
  mkdirSync(outDir, { recursive: true });

  const skills = normalizeSkills(target, profile);
  log(`  skills:        ${skills.processed} processed`);

  const agents = normalizeAgents(target, profile);
  log(`  agents:        ${agents.processed} processed`);
  if (agents.errors.length > 0) {
    for (const err of agents.errors) log(`    ERROR: ${err}`);
    return false;
  }

  const commands = normalizeCommands(target, profile);
  log(`  commands:      ${commands.processed} processed`);

  const hooks = normalizeHooks(target, profile);
  log(`  hooks:         ${hooks.variant} variant`);

  const manifest = normalizeManifest(target, profile);
  log(`  manifest:      stripped=[${manifest.stripped.join(", ") || "none"}]`);

  const srcRouting = resolve(SRC_DIR, "routing");
  if (existsSync(srcRouting)) {
    cpSync(srcRouting, resolve(outDir, "routing"), { recursive: true });
    log(`  routing:       copied`);
  }

  const catalog = normalizeCatalog(target);
  log(`  catalog:       ${catalog.copied ? "copied" : "FAILED"}`);

  if (profile.orchestrators.include) {
    const srcOrch = resolve(SRC_DIR, "orchestrators");
    if (existsSync(srcOrch)) {
      cpSync(srcOrch, resolve(outDir, "orchestrators"), { recursive: true });
      log(`  orchestrators: copied`);
    }
  } else {
    log(`  orchestrators: skipped`);
  }

  if (profile.mcp_server.include) {
    const srcMcp = resolve(SRC_DIR, "mcp-server.mjs");
    const srcMcpJson = resolve(SRC_DIR, "plugin", ".mcp.json");
    if (existsSync(srcMcp)) cpSync(srcMcp, resolve(outDir, "mcp-server.mjs"));
    if (existsSync(srcMcpJson)) cpSync(srcMcpJson, resolve(outDir, ".mcp.json"));
    log(`  mcp-server:    copied`);
  } else {
    log(`  mcp-server:    skipped`);
  }

  if (profile.calculators.include) {
    const srcCalc = resolve(SRC_DIR, "calculators");
    if (existsSync(srcCalc)) {
      mkdirSync(resolve(outDir, "scripts/calculators"), { recursive: true });
      cpSync(srcCalc, resolve(outDir, "scripts/calculators"), { recursive: true });
      log(`  calculators:   copied`);
    }
  } else {
    log(`  calculators:   skipped`);
  }

  const srcTemplates = resolve(SRC_DIR, "templates");
  if (existsSync(srcTemplates)) {
    cpSync(srcTemplates, resolve(outDir, "templates"), { recursive: true });
    log(`  templates:     copied`);
  }

  const srcSchemas = resolve(SRC_DIR, "schemas");
  if (existsSync(srcSchemas)) {
    cpSync(srcSchemas, resolve(outDir, "schemas"), { recursive: true });
    log(`  schemas:       copied`);
  }

  const srcLib = resolve(SRC_DIR, "lib");
  if (existsSync(srcLib)) {
    cpSync(srcLib, resolve(outDir, "lib"), { recursive: true });
    log(`  lib:           copied`);
  }

  const totalWarnings =
    skills.warnings.length + agents.warnings.length + commands.warnings.length +
    hooks.warnings.length + manifest.warnings.length + catalog.warnings.length;

  log(`\n  DONE: ${skills.processed} skills, ${agents.processed} agents, ${commands.processed} commands`);
  log(`  ${totalWarnings} warnings, ${agents.errors.length} errors`);
  return agents.errors.length === 0;
}
