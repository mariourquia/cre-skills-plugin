#!/usr/bin/env tsx
/**
 * Package the Cowork build into a distributable artifact.
 * Usage: npx tsx tools/package/package-cowork.ts
 */
import { statSync } from "node:fs";
import { resolve } from "node:path";
import { ensureBuildExists, createZip, writeChecksum, formatSize, DIST_DIR } from "./shared.js";

const buildDir = ensureBuildExists("cowork", "cowork-plugin");
const outputPath = resolve(DIST_DIR, "cre-skills-cowork.zip");

console.log("PACKAGE cowork");
console.log(`  source: ${buildDir}`);
console.log(`  output: ${outputPath}`);

createZip(buildDir, outputPath);

const size = statSync(outputPath).size;
const hash = writeChecksum(outputPath);

console.log(`\n  cre-skills-cowork.zip`);
console.log(`    size:   ${formatSize(size)}`);
console.log(`    sha256: ${hash}`);
console.log(`\n  Done.`);
