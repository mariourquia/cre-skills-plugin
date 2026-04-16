"""Smoke test: manual MCP handshake for Claude Desktop Chat tab.

The manual MCP path requires `.mcp.json` + `mcp-server.mjs` with a
working JSON-RPC handshake. Today we validate structurally:

- .mcp.json is valid JSON.
- mcp-server.mjs parses (node --check if available).
- The server responds to an `initialize` request over stdio.

The stdio handshake requires node on PATH; if absent the test skips.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent


class TestMcpArtifactsPresent(unittest.TestCase):
    def test_mcp_json_exists(self) -> None:
        self.assertTrue((PLUGIN_ROOT / ".mcp.json").is_file())

    def test_mcp_server_exists(self) -> None:
        self.assertTrue((PLUGIN_ROOT / "src" / "mcp-server.mjs").is_file())

    def test_mcp_json_is_valid(self) -> None:
        data = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        self.assertIn("mcpServers", data)


class TestMcpServerSyntax(unittest.TestCase):
    def test_node_check_parses_server(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")
        proc = subprocess.run(
            ["node", "--check", str(PLUGIN_ROOT / "src" / "mcp-server.mjs")],
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)


class TestMcpInitializeHandshake(unittest.TestCase):
    """Actual stdio handshake. The server must respond to `initialize`
    with server info within 3 seconds. Any crash or hang means the
    Claude Desktop Chat tab would fail to load tools."""

    def test_initialize_request_responds(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")
        server = PLUGIN_ROOT / "src" / "mcp-server.mjs"
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "install-smoke", "version": "1.0"},
            },
        }
        payload = json.dumps(req).encode("utf-8")
        proc = subprocess.run(
            ["node", str(server)],
            input=payload + b"\n",
            capture_output=True,
            timeout=5,
        )
        out = proc.stdout.decode("utf-8", errors="replace")
        self.assertIn("serverInfo", out, msg=f"stderr={proc.stderr.decode(errors='replace')}")


if __name__ == "__main__":
    unittest.main()
