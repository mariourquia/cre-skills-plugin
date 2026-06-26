#!/usr/bin/env node
// Root-level entrypoint so ${PLUGIN_ROOT}/mcp-server.mjs resolves in every
// install layout.  The real implementation lives in src/mcp-server.mjs; this
// wrapper just re-exports it.  In ES modules, import.meta.url is module-local,
// so __dirname inside src/mcp-server.mjs always resolves to the src/ directory
// regardless of how this wrapper is invoked.
import "./src/mcp-server.mjs";
