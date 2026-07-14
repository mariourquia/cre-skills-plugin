#!/usr/bin/env node
/**
 * Cross-harness SessionStart context for Claude Code and Codex.
 *
 * Both harnesses support command-hook stdout as additional SessionStart
 * context. Codex currently skips Claude-style `type: "prompt"` handlers, so
 * keeping this as a command avoids startup warnings without losing routing
 * guidance. The text is deliberately short because it is injected into every
 * session where the plugin is enabled.
 */

import { existsSync, readFileSync } from 'fs';
import { resolve } from 'path';

function drainHookInput() {
  try {
    readFileSync(0, 'utf8');
  } catch {
    // A missing/closed stdin is harmless for manual invocations and tests.
  }
}

function main() {
  drainHookInput();
  const pluginRoot = process.env.PLUGIN_ROOT || process.env.CLAUDE_PLUGIN_ROOT || '.';
  const sourceRoutingPath = resolve(pluginRoot, 'src', 'routing', 'CRE-ROUTING.md');
  const routingPath = existsSync(sourceRoutingPath)
    ? sourceRoutingPath
    : resolve(pluginRoot, 'routing', 'CRE-ROUTING.md');
  process.stdout.write(
    `CRE Skills is active. For CRE tasks, use ${routingPath} ` +
      'to select one skill, then load only that skill and its references. ' +
      'Use /cre-skills:cre-route when routing is unclear.\n'
  );
}

main();
