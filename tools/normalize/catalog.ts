/**
 * Catalog normalizer: copies catalog.yaml to build output.
 * Future: filter entries per target capabilities.
 */
import { cpSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { type TargetName, SRC_DIR, buildDir } from "../lib.js";

export interface NormalizeResult {
  copied: boolean;
  warnings: string[];
}

export function normalizeCatalog(target: TargetName): NormalizeResult {
  const srcCatalog = resolve(SRC_DIR, "catalog");
  const outCatalog = resolve(buildDir(target), "catalog");
  mkdirSync(outCatalog, { recursive: true });

  try {
    cpSync(srcCatalog, outCatalog, { recursive: true });
    return { copied: true, warnings: [] };
  } catch (err) {
    return { copied: false, warnings: [`Failed to copy catalog: ${err}`] };
  }
}
