/**
 * Hooks normalizer: emits full or portable hooks.json depending on target variant.
 *
 * Portable (Cowork): synthesized SessionStart prompt, no command-type hooks.
 * Full (Claude Code): Copy hooks/ as-is.
 */
import { readFileSync, writeFileSync, mkdirSync, cpSync } from "node:fs";
import { resolve } from "node:path";
import { type TargetName, type TargetProfile, SRC_DIR, buildDir } from "../lib.js";

export interface NormalizeResult {
  variant: string;
  warnings: string[];
}

interface HookEntry {
  type: "prompt" | "command";
  prompt?: string;
  command?: string;
}

interface HookMatcher {
  matcher: string;
  hooks: HookEntry[];
}

interface HooksJson {
  hooks: Record<string, HookMatcher[]>;
}

const PORTABLE_SESSION_CONTEXT =
  "CRE Skills is active. For CRE tasks, use " +
  "${CLAUDE_PLUGIN_ROOT}/src/routing/CRE-ROUTING.md to select one skill, " +
  "then load only that skill and its references. Use /cre-skills:cre-route " +
  "when routing is unclear.";

export function normalizeHooks(target: TargetName, profile: TargetProfile): NormalizeResult {
  const srcHooks = resolve(SRC_DIR, "hooks");
  const outHooks = resolve(buildDir(target), "hooks");
  mkdirSync(outHooks, { recursive: true });

  const warnings: string[] = [];

  if (profile.hooks.variant === "full") {
    // Copy entire hooks directory as-is...
    cpSync(srcHooks, outHooks, { recursive: true });
    // ...then re-point the ${CLAUDE_PLUGIN_ROOT}-relative paths. The SOURCE hooks.json uses
    // src/-prefixed paths so the repo/marketplace install (CLAUDE_PLUGIN_ROOT = repo root,
    // scripts under src/hooks, routing under src/routing) resolves correctly. This build
    // FLATTENS src/hooks -> hooks/ and src/routing -> routing/ (build-target.ts), so rewrite
    // the copied hooks.json to the flat layout or every command/prompt path would 404.
    const builtHooksJson = resolve(outHooks, "hooks.json");
    const rewritten = readFileSync(builtHooksJson, "utf-8")
      .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/hooks/", "${CLAUDE_PLUGIN_ROOT}/hooks/")
      .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/routing/", "${CLAUDE_PLUGIN_ROOT}/routing/");
    writeFileSync(builtHooksJson, rewritten);
    return { variant: "full", warnings };
  }

  // Portable targets cannot execute command hooks. Synthesize the same concise
  // SessionStart guidance as a prompt without putting an unsupported prompt
  // handler in the source manifest consumed by Codex and Claude Code.
  const portable: HooksJson = {
    hooks: {
      SessionStart: [
        {
          matcher: "",
          hooks: [{ type: "prompt", prompt: PORTABLE_SESSION_CONTEXT }],
        },
      ],
    },
  };

  // The synthesized prompt still uses the source-layout path, while portable
  // packages flatten src/routing -> routing.
  const rewritten = JSON.stringify(portable, null, 2)
    .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/hooks/", "${CLAUDE_PLUGIN_ROOT}/hooks/")
    .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/routing/", "${CLAUDE_PLUGIN_ROOT}/routing/");
  writeFileSync(resolve(outHooks, "hooks.json"), rewritten + "\n");
  // Do not copy .mjs script files for portable variant
  return { variant: "portable", warnings };
}
