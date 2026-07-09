/**
 * Command normalizer: strips forbidden frontmatter fields per target profile.
 */
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import {
  type TargetName,
  type TargetProfile,
  SRC_DIR,
  buildDir,
  parseFrontmatter,
  serializeFrontmatter,
} from "../lib.js";

export interface NormalizeResult {
  processed: number;
  warnings: string[];
}

export function normalizeCommands(target: TargetName, profile: TargetProfile): NormalizeResult {
  const srcCommands = resolve(SRC_DIR, "commands");
  const outCommands = resolve(buildDir(target), "commands");
  mkdirSync(outCommands, { recursive: true });

  const warnings: string[] = [];
  let processed = 0;

  const files = readdirSync(srcCommands).filter((f) => f.endsWith(".md"));
  const forbidden = new Set(profile.commands.forbidden_fields);

  for (const file of files) {
    const content = readFileSync(resolve(srcCommands, file), "utf-8");
    const { frontmatter, body } = parseFrontmatter(content);

    if (forbidden.size > 0) {
      for (const field of forbidden) {
        if (field in frontmatter) {
          delete frontmatter[field];
          warnings.push(`${file}: removed forbidden field '${field}'`);
        }
      }
    }

    // Source command files use src/-prefixed ${CLAUDE_PLUGIN_ROOT} paths so the
    // repo/marketplace install (CLAUDE_PLUGIN_ROOT == repo root) resolves routing under
    // src/routing. This build flattens src/routing -> routing/, so rewrite the body to the
    // flat layout, mirroring the hooks normalizer (otherwise the built command references 404).
    const flatBody = body
      .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/routing/", "${CLAUDE_PLUGIN_ROOT}/routing/")
      .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/hooks/", "${CLAUDE_PLUGIN_ROOT}/hooks/")
      .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/agents/", "${CLAUDE_PLUGIN_ROOT}/agents/");

    if (Object.keys(frontmatter).length > 0) {
      writeFileSync(resolve(outCommands, file), serializeFrontmatter(frontmatter, flatBody));
    } else {
      // No frontmatter left -- write plain markdown
      writeFileSync(resolve(outCommands, file), flatBody);
    }
    processed++;
  }

  return { processed, warnings };
}
