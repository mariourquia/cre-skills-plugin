#!/usr/bin/env tsx
/**
 * Diff viewer: shows what the build pipeline changes per target.
 * Compares source frontmatter/hooks against what the normalizers would produce.
 * Usage: npx tsx tools/diff.ts --target <cowork|claude-code|all>
 */
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import {
  parseTarget,
  resolveTargets,
  loadTargetProfile,
  loadAgentDefaults,
  parseFrontmatter,
  SRC_DIR,
  type TargetName,
  type TargetProfile,
} from "./lib.js";

interface Change {
  file: string;
  removals: string[];
  injections: string[];
}

function diffSkills(profile: TargetProfile): Change[] {
  const changes: Change[] = [];
  if (profile.skills.allowed_frontmatter === "all") return changes;

  const allowed = new Set(profile.skills.allowed_frontmatter);
  const skillsDir = resolve(SRC_DIR, "skills");
  if (!existsSync(skillsDir)) return changes;

  const slugs = readdirSync(skillsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  for (const slug of slugs) {
    const file = resolve(skillsDir, slug, "SKILL.md");
    if (!existsSync(file)) continue;

    const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
    const removals: string[] = [];

    for (const [key, value] of Object.entries(frontmatter)) {
      if (!allowed.has(key)) {
        const display = Array.isArray(value) ? `[${value.join(", ")}]` : String(value);
        removals.push(`${key}: ${display}`);
      }
    }

    if (removals.length > 0) {
      changes.push({ file: `skills/${slug}/SKILL.md`, removals, injections: [] });
    }
  }

  return changes;
}

function diffAgents(profile: TargetProfile): Change[] {
  const changes: Change[] = [];
  const agentsDir = resolve(SRC_DIR, "agents");
  if (!existsSync(agentsDir)) return changes;

  const defaults = loadAgentDefaults();
  const files = readdirSync(agentsDir).filter((f) => f.endsWith(".md"));

  for (const file of files) {
    const slug = file.replace(/\.md$/, "");
    const { frontmatter } = parseFrontmatter(readFileSync(resolve(agentsDir, file), "utf-8"));
    const injections: string[] = [];

    for (const field of profile.agents.required_fields) {
      if (frontmatter[field] === undefined || frontmatter[field] === "") {
        const override = defaults.overrides[slug];
        const value =
          (override as Record<string, unknown>)?.[field] ??
          (defaults.defaults as Record<string, unknown>)[field];
        if (value !== undefined) {
          injections.push(`${field}: ${value} (from defaults)`);
        }
      }
    }

    if (injections.length > 0) {
      changes.push({ file: `agents/${file}`, removals: [], injections });
    }
  }

  return changes;
}

function diffCommands(profile: TargetProfile): Change[] {
  const changes: Change[] = [];
  if (profile.commands.forbidden_fields.length === 0) return changes;

  const forbidden = new Set(profile.commands.forbidden_fields);
  const commandsDir = resolve(SRC_DIR, "commands");
  if (!existsSync(commandsDir)) return changes;

  const files = readdirSync(commandsDir).filter((f) => f.endsWith(".md"));

  for (const file of files) {
    const { frontmatter } = parseFrontmatter(readFileSync(resolve(commandsDir, file), "utf-8"));
    const removals: string[] = [];

    for (const field of forbidden) {
      if (field in frontmatter) {
        removals.push(`${field}: ${frontmatter[field]}`);
      }
    }

    if (removals.length > 0) {
      changes.push({ file: `commands/${file}`, removals, injections: [] });
    }
  }

  return changes;
}

function diffHooks(profile: TargetProfile): Change[] {
  if (profile.hooks.variant === "full") return [];

  const hooksFile = resolve(SRC_DIR, "hooks", "hooks.json");
  if (!existsSync(hooksFile)) return [];

  const hooksData = JSON.parse(readFileSync(hooksFile, "utf-8"));
  const removals: string[] = [];

  for (const [event, matchers] of Object.entries(hooksData.hooks)) {
    for (const matcher of matchers as any[]) {
      for (const hook of matcher.hooks) {
        if (hook.type === "command") {
          const cmd = hook.command?.split("/").pop() || hook.command;
          removals.push(`${event} command hook: ${cmd}`);
        }
      }
    }
  }

  // Check for .mjs files that would be excluded
  const hooksDir = resolve(SRC_DIR, "hooks");
  const mjsFiles = readdirSync(hooksDir).filter((f) => f.endsWith(".mjs"));
  for (const mjs of mjsFiles) {
    removals.push(`script: ${mjs}`);
  }

  if (removals.length > 0) {
    return [{ file: "hooks/", removals, injections: [] }];
  }
  return [];
}

function diffManifest(profile: TargetProfile): Change[] {
  if (profile.manifest.strip_fields.length === 0) return [];

  const manifestFile = resolve(SRC_DIR, "plugin", "plugin.json");
  if (!existsSync(manifestFile)) return [];

  const manifest = JSON.parse(readFileSync(manifestFile, "utf-8"));
  const removals: string[] = [];

  for (const field of profile.manifest.strip_fields) {
    if (field in manifest) {
      removals.push(`${field} (${typeof manifest[field] === "object" ? "object" : String(manifest[field])})`);
    }
  }

  if (removals.length > 0) {
    return [{ file: ".claude-plugin/plugin.json", removals, injections: [] }];
  }
  return [];
}

function diffExclusions(profile: TargetProfile): string[] {
  const excluded: string[] = [];
  if (!profile.orchestrators.include) excluded.push("orchestrators/");
  if (!profile.mcp_server.include) excluded.push("mcp-server.mjs, .mcp.json");
  if (!profile.calculators.include) excluded.push("scripts/calculators/");
  return excluded;
}

function diffTarget(target: TargetName): void {
  const profile = loadTargetProfile(target);

  console.log(`\nDIFF ${target} (source -> build)\n`);

  const allChanges: Change[] = [
    ...diffSkills(profile),
    ...diffAgents(profile),
    ...diffCommands(profile),
    ...diffHooks(profile),
    ...diffManifest(profile),
  ];

  // Summarize by category
  const skillChanges = allChanges.filter((c) => c.file.startsWith("skills/"));
  const agentChanges = allChanges.filter((c) => c.file.startsWith("agents/"));
  const commandChanges = allChanges.filter((c) => c.file.startsWith("commands/"));
  const hookChanges = allChanges.filter((c) => c.file.startsWith("hooks/"));
  const manifestChanges = allChanges.filter((c) => c.file.startsWith(".claude-plugin/"));

  if (skillChanges.length > 0) {
    // Show first 3 in detail, then summary
    const show = skillChanges.slice(0, 3);
    for (const change of show) {
      console.log(`  ${change.file}`);
      for (const r of change.removals) console.log(`    - ${r.padEnd(40)} [REMOVED]`);
      for (const i of change.injections) console.log(`    + ${i.padEnd(40)} [INJECTED]`);
    }
    if (skillChanges.length > 3) {
      const totalRemovals = skillChanges.reduce((sum, c) => sum + c.removals.length, 0);
      console.log(`  ... and ${skillChanges.length - 3} more skills (${totalRemovals} total field removals)`);
    }
  }

  if (agentChanges.length > 0) {
    const show = agentChanges.slice(0, 3);
    for (const change of show) {
      console.log(`  ${change.file}`);
      for (const r of change.removals) console.log(`    - ${r.padEnd(40)} [REMOVED]`);
      for (const i of change.injections) console.log(`    + ${i.padEnd(40)} [INJECTED]`);
    }
    if (agentChanges.length > 3) {
      const totalInjections = agentChanges.reduce((sum, c) => sum + c.injections.length, 0);
      console.log(`  ... and ${agentChanges.length - 3} more agents (${totalInjections} total field injections)`);
    }
  }

  for (const change of [...commandChanges, ...hookChanges, ...manifestChanges]) {
    console.log(`  ${change.file}`);
    for (const r of change.removals) console.log(`    - ${r.padEnd(40)} [REMOVED]`);
    for (const i of change.injections) console.log(`    + ${i.padEnd(40)} [INJECTED]`);
  }

  const excluded = diffExclusions(profile);
  if (excluded.length > 0) {
    console.log(`\n  Excluded from build:`);
    for (const e of excluded) console.log(`    x ${e}`);
  }

  if (allChanges.length === 0 && excluded.length === 0) {
    console.log("  No changes (source matches build output).");
  }

  // Stats
  const totalRemovals = allChanges.reduce((sum, c) => sum + c.removals.length, 0);
  const totalInjections = allChanges.reduce((sum, c) => sum + c.injections.length, 0);
  console.log(`\n  SUMMARY: ${allChanges.length} files changed, ${totalRemovals} removals, ${totalInjections} injections`);
}

// Main
const target = parseTarget(process.argv);
const targets = resolveTargets(target);

for (const t of targets) {
  diffTarget(t);
}
