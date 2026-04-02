/**
 * Agent normalizer: injects required fields from defaults for targets that need them.
 */
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import {
  type TargetName,
  type TargetProfile,
  SRC_DIR,
  buildDir,
  loadAgentDefaults,
  parseFrontmatter,
  serializeFrontmatter,
} from "../lib.js";

export interface NormalizeResult {
  processed: number;
  warnings: string[];
  errors: string[];
}

export function normalizeAgents(target: TargetName, profile: TargetProfile): NormalizeResult {
  const srcAgents = resolve(SRC_DIR, "agents");
  const outAgents = resolve(buildDir(target), "agents");
  mkdirSync(outAgents, { recursive: true });

  const defaults = loadAgentDefaults();
  const warnings: string[] = [];
  const errors: string[] = [];
  let processed = 0;

  const files = readdirSync(srcAgents).filter((f) => f.endsWith(".md"));

  for (const file of files) {
    const slug = file.replace(/\.md$/, "");
    const content = readFileSync(resolve(srcAgents, file), "utf-8");
    const { frontmatter, body } = parseFrontmatter(content);

    // Inject missing required fields from defaults
    for (const field of profile.agents.required_fields) {
      if (frontmatter[field] === undefined || frontmatter[field] === "") {
        // Check overrides first, then global defaults
        const override = defaults.overrides[slug];
        const value =
          (override as Record<string, unknown>)?.[field] ??
          (defaults.defaults as Record<string, unknown>)[field];

        if (value !== undefined) {
          frontmatter[field] = value;
          warnings.push(`${file}: injected ${field}=${value} from defaults`);
        } else {
          errors.push(`${file}: missing required field '${field}' with no default available`);
        }
      }
    }

    writeFileSync(resolve(outAgents, file), serializeFrontmatter(frontmatter, body));
    processed++;
  }

  return { processed, warnings, errors };
}
