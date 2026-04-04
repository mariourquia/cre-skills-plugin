#!/usr/bin/env tsx
/**
 * Package the Portable build into a distributable artifact.
 * Usage: npx tsx tools/package/package-portable.ts
 */
import { statSync } from "node:fs";
import { resolve } from "node:path";
import { ensureBuildExists, createZip, writeChecksum, formatSize, DIST_DIR } from "./shared.js";

const buildDir = ensureBuildExists("portable", "portable");
const outputPath = resolve(DIST_DIR, "cre-skills-portable.zip");

console.log("PACKAGE portable");
console.log(`  source: ${buildDir}`);
console.log(`  output: ${outputPath}`);

createZip(buildDir, outputPath);

const size = statSync(outputPath).size;
const hash = writeChecksum(outputPath);

console.log(`\n  cre-skills-portable.zip`);
console.log(`    size:   ${formatSize(size)}`);
console.log(`    sha256: ${hash}`);
console.log(`\n  Done.`);
