#!/usr/bin/env tsx
/**
 * Health check for the build environment.
 * Usage: npx tsx tools/doctor.ts
 */
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { REPO_ROOT, SRC_DIR, BUILDS_DIR } from "./lib.js";
import { resolve } from "node:path";

interface Check {
  label: string;
  value: string;
  ok: boolean;
}

const checks: Check[] = [];

function check(label: string, fn: () => { value: string; ok: boolean }) {
  try {
    const result = fn();
    checks.push({ label, ...result });
  } catch {
    checks.push({ label, value: "not found", ok: false });
  }
}

check("Node.js", () => {
  const v = execFileSync("node", ["--version"], { encoding: "utf-8" }).trim();
  return { value: v, ok: true };
});

check("tsx", () => {
  execFileSync("npx", ["tsx", "--version"], {
    encoding: "utf-8",
    cwd: resolve(REPO_ROOT, "tools"),
  });
  return { value: "available", ok: true };
});

check("Python 3", () => {
  const v = execFileSync("python3", ["--version"], { encoding: "utf-8" })
    .trim()
    .replace("Python ", "");
  return { value: v, ok: true };
});

check("src/ directory", () => {
  const exists = existsSync(SRC_DIR);
  return { value: exists ? "exists" : "missing", ok: exists };
});

check("config/ directory", () => {
  const exists = existsSync(resolve(REPO_ROOT, "config"));
  return { value: exists ? "exists" : "missing", ok: exists };
});

check("builds/ directory", () => {
  const exists = existsSync(BUILDS_DIR);
  return { value: exists ? "exists" : "not yet built", ok: true };
});

check(".gitignore has builds/", () => {
  const giPath = resolve(REPO_ROOT, ".gitignore");
  if (!existsSync(giPath)) return { value: "no .gitignore", ok: false };
  const content = readFileSync(giPath, "utf-8");
  const has = content.includes("builds/");
  return { value: has ? "yes" : "missing", ok: has };
});

console.log("\nDOCTOR -- cre-skills-plugin health check\n");
const maxLabel = Math.max(...checks.map((c) => c.label.length));
for (const c of checks) {
  const status = c.ok ? "OK" : "FAIL";
  console.log(`  ${c.label.padEnd(maxLabel + 2)} ${c.value.padEnd(16)} ${status}`);
}

const failures = checks.filter((c) => !c.ok);
if (failures.length > 0) {
  console.log(`\n  ${failures.length} issue(s) found.`);
  process.exit(1);
} else {
  console.log("\n  All checks passed.");
}
