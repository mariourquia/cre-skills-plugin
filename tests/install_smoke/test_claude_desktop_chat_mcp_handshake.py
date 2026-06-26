"""Smoke test: MCP handshake across all supported install layouts.

Validates that ${PLUGIN_ROOT}/mcp-server.mjs resolves and starts correctly in:
  1. Repo-root / dynamic-plugin mode (PLUGIN_ROOT = repo root)
  2. Marketplace-cache mode (cache mirrors repo; src/ is a subdirectory)
  3. Local-installer-cache mode (install.sh copies whole repo, preserving src/)

Checks performed:
  - .mcp.json is valid JSON with mcpServers.args[0] = ${PLUGIN_ROOT}/mcp-server.mjs
  - Root-level mcp-server.mjs exists (the entrypoint wrapper)
  - src/mcp-server.mjs exists (the real implementation)
  - node --check passes on both files
  - JSON-RPC initialize returns serverInfo.name = "cre-skills"
  - tools/list includes cre_route
  - Root-level entrypoint (${PLUGIN_ROOT}/mcp-server.mjs) works from repo root
  - Simulated cache layout (wrapper + src/ subdirectory) works

The stdio handshake tests require node on PATH; they skip otherwise.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent
INIT_REQ = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "install-smoke", "version": "1.0"},
    },
}).encode("utf-8")


def _run_server(server_path: Path, timeout: int = 5) -> str:
    """Send initialize + tools/list to `server_path`, return combined stdout."""
    tools_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}).encode("utf-8")
    proc = subprocess.run(
        ["node", str(server_path)],
        input=INIT_REQ + b"\n" + tools_req + b"\n",
        capture_output=True,
        timeout=timeout,
    )
    return proc.stdout.decode("utf-8", errors="replace")


class TestMcpJsonStructure(unittest.TestCase):
    def test_mcp_json_exists(self) -> None:
        self.assertTrue((PLUGIN_ROOT / ".mcp.json").is_file())

    def test_mcp_json_is_valid(self) -> None:
        data = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        self.assertIn("mcpServers", data)

    def test_mcp_json_args_point_to_plugin_root(self) -> None:
        """${PLUGIN_ROOT}/mcp-server.mjs must be the configured path."""
        data = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        servers = data.get("mcpServers", {})
        self.assertTrue(servers, ".mcp.json has no mcpServers")
        first = next(iter(servers.values()))
        args = first.get("args", [])
        self.assertTrue(args, "mcpServers entry has no args")
        self.assertIn("${PLUGIN_ROOT}/mcp-server.mjs", args[0],
                      "args[0] must reference ${PLUGIN_ROOT}/mcp-server.mjs")

    def test_mcp_json_args_resolve_from_repo_root(self) -> None:
        """After substituting ${PLUGIN_ROOT} with repo root, the file must exist."""
        data = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        first = next(iter(data["mcpServers"].values()))
        resolved = Path(first["args"][0].replace("${PLUGIN_ROOT}", str(PLUGIN_ROOT)))
        self.assertTrue(resolved.is_file(),
                        f"${{{PLUGIN_ROOT}}}/mcp-server.mjs resolved to {resolved} which does not exist")


class TestMcpServerFiles(unittest.TestCase):
    def test_root_entrypoint_exists(self) -> None:
        """mcp-server.mjs must exist at the plugin root (the ${PLUGIN_ROOT} entrypoint)."""
        self.assertTrue((PLUGIN_ROOT / "mcp-server.mjs").is_file(),
                        "Root-level mcp-server.mjs missing; create it as a wrapper that imports ./src/mcp-server.mjs")

    def test_src_implementation_exists(self) -> None:
        """src/mcp-server.mjs must exist (the real implementation)."""
        self.assertTrue((PLUGIN_ROOT / "src" / "mcp-server.mjs").is_file())

    def test_root_entrypoint_imports_src(self) -> None:
        """Root wrapper must re-export the src/ implementation."""
        content = (PLUGIN_ROOT / "mcp-server.mjs").read_text(encoding="utf-8")
        self.assertIn("./src/mcp-server.mjs", content,
                      "Root mcp-server.mjs must import './src/mcp-server.mjs'")


class TestMcpServerSyntax(unittest.TestCase):
    def test_node_check_root_wrapper(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")
        proc = subprocess.run(
            ["node", "--check", str(PLUGIN_ROOT / "mcp-server.mjs")],
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)

    def test_node_check_src_implementation(self) -> None:
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
    """JSON-RPC handshake tests. Any crash or hang means Claude Code would
    fail to reconnect (-32000)."""

    def test_src_implementation_initializes(self) -> None:
        """src/mcp-server.mjs (direct invocation) responds to initialize."""
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")
        out = _run_server(PLUGIN_ROOT / "src" / "mcp-server.mjs")
        self.assertIn("serverInfo", out,
                      f"src/mcp-server.mjs did not return serverInfo.\nOutput: {out!r}")
        self.assertIn("cre-skills", out)

    def test_root_entrypoint_initializes(self) -> None:
        """mcp-server.mjs at plugin root (the ${PLUGIN_ROOT} path) responds to initialize.

        This is the exact path Claude Code uses.  Failure here produces -32000.
        """
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")
        out = _run_server(PLUGIN_ROOT / "mcp-server.mjs")
        self.assertIn("serverInfo", out,
                      f"Root mcp-server.mjs did not return serverInfo.\nOutput: {out!r}")
        self.assertIn("cre-skills", out)

    def test_root_entrypoint_returns_tools(self) -> None:
        """tools/list via root entrypoint must include cre_route."""
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")
        out = _run_server(PLUGIN_ROOT / "mcp-server.mjs")
        self.assertIn("cre_route", out,
                      f"Root entrypoint tools/list missing cre_route.\nOutput: {out!r}")

    def test_no_stdout_noise_during_init(self) -> None:
        """Nothing non-JSON must appear on stdout during MCP operation."""
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")
        proc = subprocess.run(
            ["node", str(PLUGIN_ROOT / "mcp-server.mjs")],
            input=INIT_REQ + b"\n",
            capture_output=True,
            timeout=5,
        )
        out = proc.stdout.decode("utf-8", errors="replace").strip()
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError:
                self.fail(f"Non-JSON on stdout during MCP init: {line!r}")


class TestSimulatedInstalledLayout(unittest.TestCase):
    """Simulate the installed cache layout (whole-repo copy, src/ preserved)
    and verify the root wrapper resolves correctly inside it."""

    def test_cache_layout_initializes(self) -> None:
        """A cache directory with mcp-server.mjs + src/ must respond to initialize."""
        if shutil.which("node") is None:
            self.skipTest("node not on PATH")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            src_dir = tmp / "src"
            src_dir.mkdir()

            # Copy the real server implementation into the simulated cache
            impl_src = (PLUGIN_ROOT / "src" / "mcp-server.mjs").read_text(encoding="utf-8")
            (src_dir / "mcp-server.mjs").write_text(impl_src, encoding="utf-8")

            # Copy lib/ dependencies (customization, diff, feedback-payload)
            lib_src = PLUGIN_ROOT / "src" / "lib"
            lib_dst = src_dir / "lib"
            lib_dst.mkdir()
            for f in lib_src.glob("*.mjs"):
                (lib_dst / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")

            # Root-level wrapper (the file install.sh now preserves via whole-repo rsync)
            wrapper = (PLUGIN_ROOT / "mcp-server.mjs").read_text(encoding="utf-8")
            (tmp / "mcp-server.mjs").write_text(wrapper, encoding="utf-8")

            out = _run_server(tmp / "mcp-server.mjs")
            self.assertIn("serverInfo", out,
                          f"Simulated cache layout did not return serverInfo.\nOutput: {out!r}")


if __name__ == "__main__":
    unittest.main()
