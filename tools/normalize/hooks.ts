/**
 * Hooks normalizer: emits full or portable hooks.json depending on target variant.
 *
 * Portable (Cowork): SessionStart prompt only, no command-type hooks.
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

  // Portable variant: only prompt-type hooks from SessionStart
  const hooksJson: HooksJson = JSON.parse(
    readFileSync(resolve(srcHooks, "hooks.json"), "utf-8"),
  );

  const portable: HooksJson = { hooks: {} };

  for (const [event, matchers] of Object.entries(hooksJson.hooks)) {
    const filteredMatchers: HookMatcher[] = [];

    for (const matcher of matchers) {
      const promptHooks = matcher.hooks.filter((h) => h.type === "prompt");
      if (promptHooks.length > 0) {
        filteredMatchers.push({ matcher: matcher.matcher, hooks: promptHooks });
      } else {
        warnings.push(`${event}: dropped all hooks (no prompt-type hooks in matcher)`);
      }
    }

    if (filteredMatchers.length > 0) {
      portable.hooks[event] = filteredMatchers;
    } else {
      warnings.push(`${event}: entire event removed (no portable hooks)`);
    }
  }

  // Prompt-type hooks carry ${CLAUDE_PLUGIN_ROOT}-relative paths in their prompt TEXT (e.g.
  // the SessionStart prompt telling the reader where to find CRE-ROUTING.md), not just in
  // command fields -- build-target.ts flattens src/routing -> routing/ for every target
  // (portable included), so this needs the same rewrite the full branch applies, or the
  // portable prompt keeps pointing at a src/-prefixed path that doesn't exist in this layout.
  const rewritten = JSON.stringify(portable, null, 2)
    .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/hooks/", "${CLAUDE_PLUGIN_ROOT}/hooks/")
    .replaceAll("${CLAUDE_PLUGIN_ROOT}/src/routing/", "${CLAUDE_PLUGIN_ROOT}/routing/");
  writeFileSync(resolve(outHooks, "hooks.json"), rewritten + "\n");
  // Do not copy .mjs script files for portable variant
  return { variant: "portable", warnings };
}
