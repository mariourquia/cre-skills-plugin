/**
 * Shared packaging utilities.
 */
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { resolve, basename } from "node:path";
import { execFileSync } from "node:child_process";
import { REPO_ROOT, BUILDS_DIR } from "../lib.js";

export const DIST_DIR = resolve(REPO_ROOT, "dist");

export function ensureBuildExists(target: string, dirName: string): string {
  const dir = resolve(BUILDS_DIR, dirName);
  if (!existsSync(dir)) {
    console.error(`Build output not found: ${dir}`);
    console.error(`Run: npx tsx tools/build.ts --target ${target}`);
    process.exit(1);
  }
  return dir;
}

export function createZip(sourceDir: string, outputPath: string): void {
  mkdirSync(resolve(outputPath, ".."), { recursive: true });
  execFileSync("zip", ["-r", "-q", outputPath, "."], { cwd: sourceDir });
}

export function writeChecksum(filePath: string): string {
  const content = readFileSync(filePath);
  const hash = createHash("sha256").update(content).digest("hex");
  const checksumFile = `${filePath}.sha256`;
  const name = basename(filePath);
  writeFileSync(checksumFile, `${hash}  ${name}\n`);
  return hash;
}

export function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
