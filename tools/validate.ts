#!/usr/bin/env tsx
/**
 * Validation engine entry point.
 * Validates build output OR source against target schema rules.
 * Usage: npx tsx tools/validate.ts --target <cowork|claude-code|all> [--source]
 *
 * --source: validate src/ directly (pre-build, shows what would fail)
 * default: validate builds/<target>/ (post-build gate)
 */
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import {
  parseTarget,
  resolveTargets,
  loadTargetProfile,
  loadAgentDefaults,
  buildDir,
  parseFrontmatter,
  SRC_DIR,
  type TargetName,
  type TargetProfile,
} from "./lib.js";

interface Issue {
  file: string;
  level: "ERROR" | "WARN";
  message: string;
}

function validateSkills(
  skillsDir: string,
  profile: TargetProfile,
): Issue[] {
  const issues: Issue[] = [];
  if (!existsSync(skillsDir)) return issues;

  const slugs = readdirSync(skillsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  for (const slug of slugs) {
    const skillFile = resolve(skillsDir, slug, "SKILL.md");
    if (!existsSync(skillFile)) {
      issues.push({ file: `skills/${slug}/SKILL.md`, level: "ERROR", message: "SKILL.md not found" });
      continue;
    }

    const content = readFileSync(skillFile, "utf-8");
    const { frontmatter, body } = parseFrontmatter(content);

    // Check required fields
    if (!frontmatter.name || (typeof frontmatter.name === "string" && frontmatter.name.trim() === "")) {
      issues.push({ file: `skills/${slug}/SKILL.md`, level: "ERROR", message: "missing or empty 'name'" });
    }
    if (!frontmatter.description || (typeof frontmatter.description === "string" && frontmatter.description.trim() === "")) {
      issues.push({ file: `skills/${slug}/SKILL.md`, level: "ERROR", message: "missing or empty 'description'" });
    }

    // Check forbidden fields (if target restricts)
    if (profile.skills.allowed_frontmatter !== "all") {
      const allowed = new Set(profile.skills.allowed_frontmatter);
      for (const key of Object.keys(frontmatter)) {
        if (!allowed.has(key)) {
          issues.push({
            file: `skills/${slug}/SKILL.md`,
            level: "ERROR",
            message: `forbidden frontmatter field: ${key}`,
          });
        }
      }
    }

    // Check body not empty
    if (body.trim().length === 0) {
      issues.push({ file: `skills/${slug}/SKILL.md`, level: "WARN", message: "empty body content" });
    }
  }

  return issues;
}

function validateAgents(
  agentsDir: string,
  profile: TargetProfile,
): Issue[] {
  const issues: Issue[] = [];
  if (!existsSync(agentsDir)) return issues;

  const files = readdirSync(agentsDir).filter((f) => f.endsWith(".md"));

  for (const file of files) {
    const content = readFileSync(resolve(agentsDir, file), "utf-8");
    const { frontmatter } = parseFrontmatter(content);

    for (const field of profile.agents.required_fields) {
      if (frontmatter[field] === undefined || frontmatter[field] === "") {
        issues.push({
          file: `agents/${file}`,
          level: "ERROR",
          message: `missing required field: ${field}`,
        });
      }
    }
  }

  return issues;
}

function validateCommands(
  commandsDir: string,
  profile: TargetProfile,
): Issue[] {
  const issues: Issue[] = [];
  if (!existsSync(commandsDir)) return issues;

  const files = readdirSync(commandsDir).filter((f) => f.endsWith(".md"));
  const forbidden = new Set(profile.commands.forbidden_fields);

  for (const file of files) {
    const content = readFileSync(resolve(commandsDir, file), "utf-8");
    const { frontmatter } = parseFrontmatter(content);

    for (const field of forbidden) {
      if (field in frontmatter) {
        issues.push({
          file: `commands/${file}`,
          level: "ERROR",
          message: `forbidden field present: ${field}`,
        });
      }
    }
  }

  return issues;
}

function validateHooks(
  hooksDir: string,
  profile: TargetProfile,
): Issue[] {
  const issues: Issue[] = [];
  const hooksFile = resolve(hooksDir, "hooks.json");
  if (!existsSync(hooksFile)) return issues;

  const hooksData = JSON.parse(readFileSync(hooksFile, "utf-8"));

  if (profile.hooks.variant === "portable") {
    for (const [event, matchers] of Object.entries(hooksData.hooks)) {
      for (const matcher of matchers as any[]) {
        for (const hook of matcher.hooks) {
          if (hook.type === "command") {
            issues.push({
              file: "hooks/hooks.json",
              level: "ERROR",
              message: `command-type hook not allowed for portable target (event: ${event})`,
            });
          }
        }
      }
    }

    // Check no .mjs files in hooks dir
    if (existsSync(hooksDir)) {
      const mjsFiles = readdirSync(hooksDir).filter((f) => f.endsWith(".mjs"));
      for (const mjs of mjsFiles) {
        issues.push({
          file: `hooks/${mjs}`,
          level: "ERROR",
          message: ".mjs script files not allowed for portable target",
        });
      }
    }
  }

  return issues;
}

function validateManifest(
  manifestDir: string,
  profile: TargetProfile,
): Issue[] {
  const issues: Issue[] = [];
  const manifestFile = resolve(manifestDir, "plugin.json");
  if (!existsSync(manifestFile)) {
    issues.push({ file: ".claude-plugin/plugin.json", level: "ERROR", message: "plugin.json not found" });
    return issues;
  }

  const manifest = JSON.parse(readFileSync(manifestFile, "utf-8"));

  // Check required fields
  for (const field of ["name", "version", "description"]) {
    if (!manifest[field]) {
      issues.push({ file: ".claude-plugin/plugin.json", level: "ERROR", message: `missing required field: ${field}` });
    }
  }
  if (!manifest.author?.name) {
    issues.push({ file: ".claude-plugin/plugin.json", level: "ERROR", message: "missing author.name" });
  }

  // Check forbidden fields
  for (const field of profile.manifest.strip_fields) {
    if (field in manifest) {
      issues.push({
        file: ".claude-plugin/plugin.json",
        level: "ERROR",
        message: `forbidden field: ${field}`,
      });
    }
  }

  return issues;
}

function validateTarget(target: TargetName, useSource: boolean): number {
  const profile = loadTargetProfile(target);
  const baseDir = useSource ? SRC_DIR : buildDir(target);
  const label = useSource ? "source" : "build";

  if (!existsSync(baseDir)) {
    console.log(`\nVALIDATE ${target} (${label})`);
    console.log(`  ERROR: ${baseDir} does not exist. ${useSource ? "" : "Run build first."}`);
    return 1;
  }

  console.log(`\nVALIDATE ${target} (${label})`);

  const allIssues: Issue[] = [];

  // Skills
  allIssues.push(...validateSkills(resolve(baseDir, "skills"), profile));

  // Agents
  allIssues.push(...validateAgents(resolve(baseDir, "agents"), profile));

  // Commands
  allIssues.push(...validateCommands(resolve(baseDir, "commands"), profile));

  // Hooks
  allIssues.push(...validateHooks(resolve(baseDir, "hooks"), profile));

  // Manifest
  const manifestDir = useSource ? resolve(baseDir, "plugin") : resolve(baseDir, ".claude-plugin");
  allIssues.push(...validateManifest(manifestDir, profile));

  // Print issues grouped by file
  const byFile = new Map<string, Issue[]>();
  for (const issue of allIssues) {
    const existing = byFile.get(issue.file) ?? [];
    existing.push(issue);
    byFile.set(issue.file, existing);
  }

  for (const [file, issues] of byFile) {
    console.log(`  ${file}`);
    for (const issue of issues) {
      console.log(`    ${issue.level}  ${issue.message}`);
    }
  }

  const errors = allIssues.filter((i) => i.level === "ERROR").length;
  const warns = allIssues.filter((i) => i.level === "WARN").length;

  if (errors === 0 && warns === 0) {
    console.log("  All checks passed.");
  }

  console.log(`\nRESULT: ${errors} errors, ${warns} warnings`);
  return errors;
}

// Main
const target = parseTarget(process.argv);
const targets = resolveTargets(target);
const useSource = process.argv.includes("--source");

let totalErrors = 0;
for (const t of targets) {
  totalErrors += validateTarget(t, useSource);
}

if (totalErrors > 0) {
  process.exit(1);
}
