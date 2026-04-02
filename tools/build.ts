#!/usr/bin/env tsx
/**
 * Build pipeline entry point.
 * Usage: npx tsx tools/build.ts --target <cowork|claude-code|all>
 */
import { parseTarget, resolveTargets } from "./lib.js";
import { buildTarget } from "./build-target.js";

const target = parseTarget(process.argv);
const targets = resolveTargets(target);
let allOk = true;

for (const t of targets) {
  if (!buildTarget(t)) {
    allOk = false;
  }
}

if (!allOk) {
  console.log("\nBuild completed with errors.");
  process.exit(1);
}
console.log("\nBuild completed successfully.");
