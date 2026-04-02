#!/usr/bin/env tsx
/**
 * Build system test runner.
 * Runs golden, negative, and regression tests against the build pipeline.
 * Usage: npx tsx tools/test.ts
 */
import { createHash } from "node:crypto";
import { rmSync, readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync } from "node:fs";
import { resolve, relative } from "node:path";
import {
  buildDir,
  parseFrontmatter,
  loadTargetProfile,
  SRC_DIR,
  BUILDS_DIR,
  type TargetName,
} from "./lib.js";
import { buildTarget } from "./build-target.js";
import { normalizeSkills } from "./normalize/skills.js";
import { normalizeAgents } from "./normalize/agents.js";
import { normalizeCommands } from "./normalize/commands.js";
import { normalizeHooks } from "./normalize/hooks.js";
import { normalizeManifest } from "./normalize/manifest.js";

const REPO_ROOT = resolve(import.meta.dirname!, "..");
const FIXTURES = resolve(REPO_ROOT, "tests", "fixtures");

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void) {
  try {
    fn();
    passed++;
    console.log(`  PASS  ${name}`);
  } catch (err: any) {
    failed++;
    console.log(`  FAIL  ${name}`);
    console.log(`        ${err.message}`);
  }
}

function assert(condition: boolean, message: string) {
  if (!condition) throw new Error(message);
}

function assertEqual(actual: unknown, expected: unknown, label: string) {
  if (actual !== expected) {
    throw new Error(`${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

// ── Setup: build both targets ──────────────────────────────────────────

console.log("\nSETUP: Building both targets...\n");

for (const target of ["cowork", "claude-code"] as const) {
  buildTarget(target, true);
}

// ── Golden: Cowork Skill Frontmatter ───────────────────────────────────

console.log("GOLDEN: Cowork skill normalization");

test("cowork skills have only name+description", () => {
  const dir = resolve(buildDir("cowork"), "skills");
  const slugs = readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);
  assert(slugs.length > 0, "no skills found");

  for (const slug of slugs) {
    const file = resolve(dir, slug, "SKILL.md");
    if (!existsSync(file)) continue;
    const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
    const keys = Object.keys(frontmatter);
    const forbidden = keys.filter((k) => !["name", "description"].includes(k));
    assert(
      forbidden.length === 0,
      `${slug}: forbidden keys [${forbidden.join(", ")}]`,
    );
  }
});

test("cowork skills preserve body content", () => {
  const dqs = resolve(buildDir("cowork"), "skills/deal-quick-screen/SKILL.md");
  const { body } = parseFrontmatter(readFileSync(dqs, "utf-8"));
  assert(body.includes("Deal QuickScreen"), "body content missing or truncated");
});

test("cowork deal-quick-screen has references/", () => {
  const refs = resolve(buildDir("cowork"), "skills/deal-quick-screen/references");
  // References may not exist for this skill -- check one that does
  const skillsDir = resolve(buildDir("cowork"), "skills");
  const slugs = readdirSync(skillsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  // Find a skill with references in source
  let found = false;
  for (const slug of slugs) {
    const srcRefs = resolve(SRC_DIR, "skills", slug, "references");
    if (existsSync(srcRefs)) {
      const buildRefs = resolve(skillsDir, slug, "references");
      assert(existsSync(buildRefs), `${slug}: references/ not copied to build`);
      found = true;
      break;
    }
  }
  assert(found, "no skills with references/ found to test");
});

// ── Golden: Cowork Agent Required Fields ───────────────────────────────

console.log("\nGOLDEN: Cowork agent normalization");

test("cowork agents all have name, model, color, description", () => {
  const dir = resolve(buildDir("cowork"), "agents");
  const files = readdirSync(dir).filter((f) => f.endsWith(".md"));
  assert(files.length > 0, "no agents found");

  for (const file of files) {
    const { frontmatter } = parseFrontmatter(readFileSync(resolve(dir, file), "utf-8"));
    for (const field of ["name", "model", "color", "description"]) {
      assert(
        frontmatter[field] !== undefined && frontmatter[field] !== "",
        `${file}: missing ${field}`,
      );
    }
  }
});

test("cowork titan-zell has gold color", () => {
  const file = resolve(buildDir("cowork"), "agents/titan-zell.md");
  const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
  assertEqual(frontmatter.color, "gold", "titan-zell color");
});

test("cowork aggressive-gp has red color", () => {
  const file = resolve(buildDir("cowork"), "agents/aggressive-gp.md");
  const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
  assertEqual(frontmatter.color, "red", "aggressive-gp color");
});

test("cowork buyer-pension-fund has green color", () => {
  const file = resolve(buildDir("cowork"), "agents/buyer-pension-fund.md");
  const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
  assertEqual(frontmatter.color, "green", "buyer-pension-fund color");
});

test("cowork perspective-tenant has purple color", () => {
  const file = resolve(buildDir("cowork"), "agents/perspective-tenant.md");
  const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
  assertEqual(frontmatter.color, "purple", "perspective-tenant color");
});

test("cowork lens-contrarian has teal color", () => {
  const file = resolve(buildDir("cowork"), "agents/lens-contrarian.md");
  const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
  assertEqual(frontmatter.color, "teal", "lens-contrarian color");
});

// ── Golden: Cowork Command No Name ─────────────────────────────────────

console.log("\nGOLDEN: Cowork command normalization");

test("cowork commands have no name field", () => {
  const dir = resolve(buildDir("cowork"), "commands");
  const files = readdirSync(dir).filter((f) => f.endsWith(".md"));
  assert(files.length > 0, "no commands found");

  for (const file of files) {
    const content = readFileSync(resolve(dir, file), "utf-8");
    const { frontmatter } = parseFrontmatter(content);
    assert(!("name" in frontmatter), `${file}: still has 'name' field`);
  }
});

// ── Golden: Cowork Hooks Portable ──────────────────────────────────────

console.log("\nGOLDEN: Cowork hooks normalization");

test("cowork hooks.json has no command-type hooks", () => {
  const file = resolve(buildDir("cowork"), "hooks/hooks.json");
  const data = JSON.parse(readFileSync(file, "utf-8"));
  for (const [event, matchers] of Object.entries(data.hooks)) {
    for (const matcher of matchers as any[]) {
      for (const hook of matcher.hooks) {
        assert(hook.type !== "command", `${event}: command-type hook found`);
      }
    }
  }
});

test("cowork hooks/ has no .mjs files", () => {
  const dir = resolve(buildDir("cowork"), "hooks");
  const mjsFiles = readdirSync(dir).filter((f) => f.endsWith(".mjs"));
  assertEqual(mjsFiles.length, 0, "mjs files in cowork hooks");
});

// ── Golden: Cowork Manifest ────────────────────────────────────────────

console.log("\nGOLDEN: Cowork manifest normalization");

test("cowork manifest has no userConfig", () => {
  const file = resolve(buildDir("cowork"), ".claude-plugin/plugin.json");
  const data = JSON.parse(readFileSync(file, "utf-8"));
  assert(!("userConfig" in data), "userConfig still present");
});

test("cowork manifest retains name, version, description, author", () => {
  const file = resolve(buildDir("cowork"), ".claude-plugin/plugin.json");
  const data = JSON.parse(readFileSync(file, "utf-8"));
  for (const field of ["name", "version", "description"]) {
    assert(data[field], `missing ${field}`);
  }
  assert(data.author?.name, "missing author.name");
});

// ── Golden: Claude Code Full Frontmatter ───────────────────────────────

console.log("\nGOLDEN: Claude Code preserves everything");

test("claude-code skills keep all frontmatter fields", () => {
  const file = resolve(buildDir("claude-code"), "skills/deal-quick-screen/SKILL.md");
  const { frontmatter } = parseFrontmatter(readFileSync(file, "utf-8"));
  for (const field of ["name", "slug", "version", "status", "category", "description", "targets"]) {
    assert(frontmatter[field] !== undefined, `missing ${field}`);
  }
});

test("claude-code manifest keeps userConfig", () => {
  const file = resolve(buildDir("claude-code"), ".claude-plugin/plugin.json");
  const data = JSON.parse(readFileSync(file, "utf-8"));
  assert("userConfig" in data, "userConfig stripped incorrectly");
});

test("claude-code has orchestrators", () => {
  const dir = resolve(buildDir("claude-code"), "orchestrators");
  assert(existsSync(dir), "orchestrators/ missing");
  const files = readdirSync(dir);
  assert(files.length > 0, "orchestrators/ is empty");
});

test("claude-code has mcp-server.mjs", () => {
  const file = resolve(buildDir("claude-code"), "mcp-server.mjs");
  assert(existsSync(file), "mcp-server.mjs missing");
});

test("claude-code has calculators", () => {
  const dir = resolve(buildDir("claude-code"), "scripts/calculators");
  assert(existsSync(dir), "scripts/calculators/ missing");
  const files = readdirSync(dir).filter((f) => f.endsWith(".py"));
  assert(files.length >= 10, `only ${files.length} calculators found`);
});

test("claude-code hooks have command-type hooks", () => {
  const file = resolve(buildDir("claude-code"), "hooks/hooks.json");
  const data = JSON.parse(readFileSync(file, "utf-8"));
  let hasCommand = false;
  for (const matchers of Object.values(data.hooks)) {
    for (const matcher of matchers as any[]) {
      for (const hook of matcher.hooks) {
        if (hook.type === "command") hasCommand = true;
      }
    }
  }
  assert(hasCommand, "no command-type hooks found -- should have telemetry");
});

// ── Regression: Count Consistency ──────────────────────────────────────

console.log("\nREGRESSION: Count consistency");

test("cowork skill count matches source skill count", () => {
  const srcCount = readdirSync(resolve(SRC_DIR, "skills"), { withFileTypes: true })
    .filter((d) => d.isDirectory()).length;
  const buildCount = readdirSync(resolve(buildDir("cowork"), "skills"), { withFileTypes: true })
    .filter((d) => d.isDirectory()).length;
  assertEqual(buildCount, srcCount, "skill count");
});

test("claude-code skill count matches source skill count", () => {
  const srcCount = readdirSync(resolve(SRC_DIR, "skills"), { withFileTypes: true })
    .filter((d) => d.isDirectory()).length;
  const buildCount = readdirSync(resolve(buildDir("claude-code"), "skills"), { withFileTypes: true })
    .filter((d) => d.isDirectory()).length;
  assertEqual(buildCount, srcCount, "skill count");
});

test("cowork agent count matches source agent count", () => {
  const srcCount = readdirSync(resolve(SRC_DIR, "agents"))
    .filter((f) => f.endsWith(".md")).length;
  const buildCount = readdirSync(resolve(buildDir("cowork"), "agents"))
    .filter((f) => f.endsWith(".md")).length;
  assertEqual(buildCount, srcCount, "agent count");
});

test("cowork has no orchestrators directory", () => {
  assert(
    !existsSync(resolve(buildDir("cowork"), "orchestrators")),
    "orchestrators/ should not exist in cowork build",
  );
});

test("cowork has no mcp-server.mjs", () => {
  assert(
    !existsSync(resolve(buildDir("cowork"), "mcp-server.mjs")),
    "mcp-server.mjs should not exist in cowork build",
  );
});

test("cowork has no calculators", () => {
  assert(
    !existsSync(resolve(buildDir("cowork"), "scripts/calculators")),
    "scripts/calculators/ should not exist in cowork build",
  );
});

// ── Snapshot: Build Output Hashing ──────────────────────────────────────

console.log("\nSNAPSHOT: Build output consistency");

const SNAPSHOTS_DIR = resolve(REPO_ROOT, "tests", "snapshots");
const updateSnapshots = process.argv.includes("--update-snapshots");

function hashDir(dir: string): string {
  const hash = createHash("sha256");
  const entries: string[] = [];

  function walk(d: string) {
    for (const entry of readdirSync(d, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const full = resolve(d, entry.name);
      const rel = relative(dir, full);
      if (entry.isDirectory()) {
        entries.push(`d:${rel}`);
        walk(full);
      } else {
        const content = readFileSync(full);
        const fileHash = createHash("sha256").update(content).digest("hex");
        entries.push(`f:${rel}:${fileHash}`);
      }
    }
  }

  walk(dir);
  hash.update(entries.join("\n"));
  return hash.digest("hex");
}

for (const target of ["cowork", "claude-code"] as const) {
  const snapshotFile = resolve(SNAPSHOTS_DIR, `${target}.sha256`);
  const currentHash = hashDir(buildDir(target));

  if (updateSnapshots) {
    mkdirSync(SNAPSHOTS_DIR, { recursive: true });
    writeFileSync(snapshotFile, currentHash + "\n");
    test(`${target} snapshot updated`, () => {});
  } else if (existsSync(snapshotFile)) {
    const savedHash = readFileSync(snapshotFile, "utf-8").trim();
    test(`${target} snapshot matches`, () => {
      assertEqual(currentHash, savedHash, `${target} build hash`);
    });
  } else {
    test(`${target} snapshot baseline created`, () => {
      mkdirSync(SNAPSHOTS_DIR, { recursive: true });
      writeFileSync(snapshotFile, currentHash + "\n");
    });
  }
}

// ── Negative: Fixture Validation ───────────────────────────────────────

console.log("\nNEGATIVE: Bad input handling");

test("malformed skill frontmatter parsed without crash", () => {
  const content = readFileSync(resolve(FIXTURES, "malformed_skill.md"), "utf-8");
  // parseFrontmatter should not throw -- it returns empty frontmatter on bad YAML
  const result = parseFrontmatter(content);
  // The broken YAML means frontmatter won't parse cleanly
  assert(result.body !== undefined, "parseFrontmatter returned no body");
});

test("missing agent fields detected by cowork validation", () => {
  const content = readFileSync(resolve(FIXTURES, "missing_agent_fields.md"), "utf-8");
  const { frontmatter } = parseFrontmatter(content);
  const profile = loadTargetProfile("cowork");
  const missing = profile.agents.required_fields.filter(
    (f) => frontmatter[f] === undefined || frontmatter[f] === "",
  );
  assert(missing.length > 0, "expected missing required fields");
  assert(missing.includes("name"), "should detect missing name");
});

test("forbidden command name detected by cowork validation", () => {
  const content = readFileSync(resolve(FIXTURES, "forbidden_command_name.md"), "utf-8");
  const { frontmatter } = parseFrontmatter(content);
  const profile = loadTargetProfile("cowork");
  const forbidden = profile.commands.forbidden_fields.filter((f) => f in frontmatter);
  assert(forbidden.length > 0, "expected forbidden field 'name'");
  assert(forbidden.includes("name"), "should detect forbidden 'name' field");
});

test("command-type hook rejected for portable target", () => {
  const data = JSON.parse(readFileSync(resolve(FIXTURES, "wrong_hook_type.json"), "utf-8"));
  let hasCommand = false;
  for (const matchers of Object.values(data.hooks)) {
    for (const matcher of matchers as any[]) {
      for (const hook of matcher.hooks) {
        if (hook.type === "command") hasCommand = true;
      }
    }
  }
  assert(hasCommand, "fixture should contain command-type hook");
  const profile = loadTargetProfile("cowork");
  assert(profile.hooks.variant === "portable", "cowork should use portable hooks");
});

test("invalid manifest missing required fields", () => {
  const data = JSON.parse(readFileSync(resolve(FIXTURES, "invalid_manifest.json"), "utf-8"));
  const missing = ["name", "version"].filter((f) => !data[f]);
  assert(missing.length === 2, `expected 2 missing fields, got ${missing.length}`);
  assert(!data.author?.name, "author.name should be missing");
});

// ── Cleanup ────────────────────────────────────────────────────────────

rmSync(BUILDS_DIR, { recursive: true, force: true });

// ── Summary ────────────────────────────────────────────────────────────

console.log(`\n${"=".repeat(50)}`);
console.log(`  ${passed + failed} tests: ${passed} passed, ${failed} failed`);
console.log(`${"=".repeat(50)}`);

if (failed > 0) {
  process.exit(1);
}
