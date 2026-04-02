import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { parse as parseYaml } from "yaml";

const __dirname = dirname(fileURLToPath(import.meta.url));

export const REPO_ROOT = resolve(__dirname, "..");
export const SRC_DIR = resolve(REPO_ROOT, "src");
export const CONFIG_DIR = resolve(REPO_ROOT, "config");
export const BUILDS_DIR = resolve(REPO_ROOT, "builds");

export const VALID_TARGETS = ["cowork", "claude-code"] as const;
export type TargetName = (typeof VALID_TARGETS)[number];

export interface TargetProfile {
  name: string;
  description: string;
  skills: {
    allowed_frontmatter: string[] | "all";
    strip_fields: string[];
  };
  agents: {
    required_fields: string[];
    defaults_file?: string;
  };
  commands: {
    forbidden_fields: string[];
  };
  hooks: {
    variant: "full" | "portable";
  };
  manifest: {
    strip_fields: string[];
    overrides_file?: string;
  };
  orchestrators: { include: boolean };
  mcp_server: { include: boolean };
  calculators: { include: boolean };
}

export interface AgentDefaults {
  defaults: { model: string; color: string };
  overrides: Record<string, { model?: string; color?: string }>;
}

export function loadTargetProfile(target: TargetName): TargetProfile {
  const path = resolve(CONFIG_DIR, "targets", `${target}.yaml`);
  return parseYaml(readFileSync(path, "utf-8"));
}

export function loadAgentDefaults(): AgentDefaults {
  const path = resolve(CONFIG_DIR, "defaults", "agent-defaults.yaml");
  return parseYaml(readFileSync(path, "utf-8"));
}

export function parseTarget(argv: string[]): TargetName | "all" {
  const idx = argv.indexOf("--target");
  if (idx === -1 || !argv[idx + 1]) {
    console.error("Usage: --target <cowork|claude-code|all>");
    process.exit(1);
  }
  const val = argv[idx + 1];
  if (val === "all") return "all";
  if (!VALID_TARGETS.includes(val as TargetName)) {
    console.error(`Unknown target: ${val}. Valid: ${VALID_TARGETS.join(", ")}`);
    process.exit(1);
  }
  return val as TargetName;
}

export function resolveTargets(target: TargetName | "all"): TargetName[] {
  return target === "all" ? [...VALID_TARGETS] : [target];
}

/** Parse YAML frontmatter from a markdown file. Returns { frontmatter, body }. */
export function parseFrontmatter(content: string): {
  frontmatter: Record<string, unknown>;
  body: string;
} {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!match) {
    return { frontmatter: {}, body: content };
  }
  let frontmatter: Record<string, unknown>;
  try {
    frontmatter = parseYaml(match[1]) ?? {};
  } catch {
    return { frontmatter: {}, body: content };
  }
  return { frontmatter, body: match[2] };
}

/** Serialize frontmatter + body back to markdown. */
export function serializeFrontmatter(
  frontmatter: Record<string, unknown>,
  body: string,
): string {
  const yaml = Object.entries(frontmatter)
    .map(([k, v]) => {
      if (typeof v === "string" && (v.includes(":") || v.includes('"') || v.includes("'"))) {
        return `${k}: ${JSON.stringify(v)}`;
      }
      if (Array.isArray(v)) {
        return `${k}:\n${v.map((item) => `  - ${item}`).join("\n")}`;
      }
      return `${k}: ${v}`;
    })
    .join("\n");
  return `---\n${yaml}\n---\n\n${body}`;
}

export function buildDir(target: TargetName): string {
  const dirName = target === "cowork" ? "cowork-plugin" : "claude-code";
  return resolve(BUILDS_DIR, dirName);
}
