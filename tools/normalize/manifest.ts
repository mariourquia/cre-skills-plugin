/**
 * Manifest normalizer: compiles target-specific plugin.json from source.
 * Strips fields and applies overrides per target profile.
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { parse as parseYaml } from "yaml";
import { type TargetName, type TargetProfile, REPO_ROOT, buildDir, CONFIG_DIR } from "../lib.js";

export interface NormalizeResult {
  stripped: string[];
  warnings: string[];
}

export function normalizeManifest(target: TargetName, profile: TargetProfile): NormalizeResult {
  const srcManifest = resolve(REPO_ROOT, ".claude-plugin", "plugin.json");
  const outDir = resolve(buildDir(target), ".claude-plugin");
  mkdirSync(outDir, { recursive: true });

  const manifest = JSON.parse(readFileSync(srcManifest, "utf-8"));
  const stripped: string[] = [];
  const warnings: string[] = [];

  for (const field of profile.manifest.strip_fields) {
    if (field in manifest) {
      delete manifest[field];
      stripped.push(field);
    }
  }

  if (profile.manifest.overrides_file) {
    const overridesPath = resolve(CONFIG_DIR, "targets", profile.manifest.overrides_file);
    try {
      const overrides = parseYaml(readFileSync(overridesPath, "utf-8"));
      const targetOverrides = overrides?.[target];
      if (targetOverrides && typeof targetOverrides === "object") {
        for (const [key, value] of Object.entries(targetOverrides)) {
          if (Object.prototype.hasOwnProperty.call(targetOverrides, key)) {
            manifest[key] = value;
          }
        }
      }
    } catch {
      warnings.push(`Could not load overrides from ${profile.manifest.overrides_file}`);
    }
  }

  writeFileSync(resolve(outDir, "plugin.json"), JSON.stringify(manifest, null, 2) + "\n");
  return { stripped, warnings };
}
