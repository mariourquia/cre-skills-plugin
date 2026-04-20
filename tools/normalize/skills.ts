/**
 * Skill normalizer: strips/transforms SKILL.md frontmatter per target profile.
 * Copies references/ unchanged.
 */
import { readFileSync, writeFileSync, mkdirSync, cpSync, readdirSync } from "node:fs";
import { resolve, join } from "node:path";
import { globSync } from "glob";
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

export function normalizeSkills(target: TargetName, profile: TargetProfile): NormalizeResult {
  const srcSkills = resolve(SRC_DIR, "skills");
  const outSkills = resolve(buildDir(target), "skills");
  const warnings: string[] = [];
  let processed = 0;

  const skillDirs = readdirSync(srcSkills, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  const excluded = new Set(profile.skills.exclude_skills ?? []);

  for (const slug of skillDirs) {
    if (excluded.has(slug)) {
      continue;
    }
    const skillSrc = resolve(srcSkills, slug);
    const skillOut = resolve(outSkills, slug);
    mkdirSync(skillOut, { recursive: true });

    const skillFile = resolve(skillSrc, "SKILL.md");
    let content: string;
    try {
      content = readFileSync(skillFile, "utf-8");
    } catch {
      warnings.push(`${slug}: SKILL.md not found, skipped`);
      continue;
    }

    const { frontmatter, body } = parseFrontmatter(content);

    if (profile.skills.allowed_frontmatter === "all") {
      // Keep everything
      writeFileSync(resolve(skillOut, "SKILL.md"), content);
    } else {
      // Keep only allowed fields
      const allowed = new Set(profile.skills.allowed_frontmatter);
      const filtered: Record<string, unknown> = {};
      for (const key of Object.keys(frontmatter)) {
        if (allowed.has(key)) {
          filtered[key] = frontmatter[key];
        }
      }
      writeFileSync(resolve(skillOut, "SKILL.md"), serializeFrontmatter(filtered, body));
    }

    // Copy references/ if present
    const refsDir = resolve(skillSrc, "references");
    try {
      cpSync(refsDir, resolve(skillOut, "references"), { recursive: true });
    } catch {
      // No references dir -- that's fine
    }

    processed++;
  }

  return { processed, warnings };
}
