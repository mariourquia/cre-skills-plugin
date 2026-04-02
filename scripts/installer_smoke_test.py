#!/usr/bin/env python3
"""
installer_smoke_test.py -- Validates post-install state of the CRE Skills Plugin.

Checks:
  1. Plugin cache directory exists with expected files
  2. installed_plugins.json is valid and has correct registration
  3. settings.json has the plugin enabled
  4. Claude Desktop config has MCP server entry (if config dir exists)
  5. mcp-server.mjs parses via node --check (if node available)
  6. Version in registration matches .claude-plugin/plugin.json

Usage:
    python3 scripts/installer_smoke_test.py [--claude-home PATH] [--install-dir PATH]

Exit codes:
    0 -- all checks passed (or skipped)
    1 -- one or more checks failed
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------

_failures = 0
_passes = 0
_skips = 0


def _pass(msg: str) -> None:
    global _passes
    _passes += 1
    print(f"  PASS  {msg}")


def _fail(msg: str) -> None:
    global _failures
    _failures += 1
    print(f"  FAIL  {msg}")


def _skip(msg: str) -> None:
    global _skips
    _skips += 1
    print(f"  SKIP  {msg}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict | None:
    """Load a JSON file, return None on any error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def get_plugin_version(install_dir: Path) -> str:
    """Read version from .claude-plugin/plugin.json."""
    pj = install_dir / ".claude-plugin" / "plugin.json"
    data = load_json(pj)
    if data and "version" in data:
        return data["version"]
    return ""


def desktop_config_path() -> Path | None:
    """Return the Claude Desktop config path for the current platform."""
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif system == "Linux":
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    return None


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_cache_dir(claude_home: Path, version: str) -> None:
    """Check 1: Plugin cache directory exists with required files."""
    print()
    print("  1. Plugin cache directory")
    print("  " + "-" * 50)

    cache_dir = claude_home / "plugins" / "cache" / "local" / "cre-skills-plugin" / version

    if not cache_dir.is_dir():
        _fail(f"Cache directory does not exist: {cache_dir}")
        return

    _pass(f"Cache directory exists: {cache_dir}")

    plugin_json = cache_dir / ".claude-plugin" / "plugin.json"
    if plugin_json.is_file():
        _pass(".claude-plugin/plugin.json present in cache")
    else:
        _fail(f".claude-plugin/plugin.json missing from cache: {plugin_json}")

    mcp_server = cache_dir / "mcp-server.mjs"
    if mcp_server.is_file():
        _pass("mcp-server.mjs present in cache")
    else:
        _fail(f"mcp-server.mjs missing from cache: {mcp_server}")


def check_installed_plugins(claude_home: Path, version: str) -> None:
    """Check 2: installed_plugins.json is valid and has correct registration."""
    print()
    print("  2. installed_plugins.json")
    print("  " + "-" * 50)

    ip_file = claude_home / "plugins" / "installed_plugins.json"

    if not ip_file.is_file():
        _fail(f"installed_plugins.json does not exist: {ip_file}")
        return

    data = load_json(ip_file)
    if data is None:
        _fail(f"installed_plugins.json is not valid JSON: {ip_file}")
        return

    _pass("installed_plugins.json is valid JSON")

    plugin_key = "cre-skills@local"
    plugins = data.get("plugins", {})

    if plugin_key not in plugins:
        _fail(f"Key '{plugin_key}' not found in installed_plugins.json")
        return

    _pass(f"Key '{plugin_key}' found in installed_plugins.json")

    entry = plugins[plugin_key]
    # Entry is a list with one element per the installer logic
    if isinstance(entry, list) and len(entry) > 0:
        entry = entry[0]

    registered_version = entry.get("version", "")
    if registered_version == version:
        _pass(f"Registered version matches plugin.json: {version}")
    else:
        _fail(f"Version mismatch: registered={registered_version}, plugin.json={version}")

    install_path = entry.get("installPath", "")
    if install_path:
        _pass(f"installPath is set: {install_path}")
    else:
        _fail("installPath is not set in registration entry")


def check_settings(claude_home: Path) -> None:
    """Check 3: settings.json has the plugin enabled."""
    print()
    print("  3. settings.json")
    print("  " + "-" * 50)

    settings_file = claude_home / "settings.json"

    if not settings_file.is_file():
        _fail(f"settings.json does not exist: {settings_file}")
        return

    data = load_json(settings_file)
    if data is None:
        _fail(f"settings.json is not valid JSON: {settings_file}")
        return

    _pass("settings.json is valid JSON")

    plugin_key = "cre-skills@local"
    enabled = data.get("enabledPlugins", {})

    if enabled.get(plugin_key) is True:
        _pass(f"enabledPlugins['{plugin_key}'] = true")
    else:
        _fail(f"enabledPlugins['{plugin_key}'] is not true (got: {enabled.get(plugin_key, '<missing>')})")


def check_desktop_config() -> None:
    """Check 4: Claude Desktop config has MCP server entry (if config dir exists)."""
    print()
    print("  4. Claude Desktop config")
    print("  " + "-" * 50)

    config_path = desktop_config_path()
    if config_path is None:
        _skip("Cannot determine Claude Desktop config path for this platform")
        return

    if not config_path.parent.is_dir():
        _skip(f"Claude Desktop config directory does not exist: {config_path.parent}")
        return

    if not config_path.is_file():
        _skip(f"Claude Desktop config file does not exist: {config_path}")
        return

    data = load_json(config_path)
    if data is None:
        _fail(f"Claude Desktop config is not valid JSON: {config_path}")
        return

    _pass("Claude Desktop config is valid JSON")

    mcp_servers = data.get("mcpServers", {})
    if "cre-skills" in mcp_servers:
        _pass("mcpServers['cre-skills'] entry exists")
    else:
        _fail("mcpServers['cre-skills'] entry missing from Claude Desktop config")


def check_mcp_server_syntax(install_dir: Path) -> None:
    """Check 5: mcp-server.mjs parses via node --check."""
    print()
    print("  5. MCP server syntax")
    print("  " + "-" * 50)

    mcp_file = install_dir / "mcp-server.mjs"
    if not mcp_file.is_file():
        _fail(f"mcp-server.mjs not found at: {mcp_file}")
        return

    if not shutil.which("node"):
        _skip("Node.js not available; cannot run node --check")
        return

    try:
        result = subprocess.run(
            ["node", "--check", str(mcp_file)],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            _pass("mcp-server.mjs passes node --check")
        else:
            stderr = result.stderr.strip()
            _fail(f"mcp-server.mjs failed node --check: {stderr}")
    except subprocess.TimeoutExpired:
        _fail("node --check timed out")
    except OSError as e:
        _skip(f"Could not run node --check: {e}")


def check_version_consistency(claude_home: Path, install_dir: Path, version: str) -> None:
    """Check 6: Version in registration matches .claude-plugin/plugin.json."""
    print()
    print("  6. Version consistency")
    print("  " + "-" * 50)

    # Already checked version match in check_installed_plugins, but also
    # verify the cached copy's plugin.json matches the source.
    ip_file = claude_home / "plugins" / "installed_plugins.json"
    data = load_json(ip_file)
    if data is None:
        _skip("Cannot verify version consistency: installed_plugins.json unreadable")
        return

    plugin_key = "cre-skills@local"
    plugins = data.get("plugins", {})
    entry = plugins.get(plugin_key)
    if entry is None:
        _skip("Cannot verify version consistency: plugin not registered")
        return

    if isinstance(entry, list) and len(entry) > 0:
        entry = entry[0]

    install_path = entry.get("installPath", "")
    if not install_path:
        _skip("Cannot verify version consistency: installPath empty")
        return

    cached_pj = Path(install_path) / ".claude-plugin" / "plugin.json"
    cached_data = load_json(cached_pj)
    if cached_data is None:
        _skip(f"Cannot read cached plugin.json at {cached_pj}")
        return

    cached_version = cached_data.get("version", "")
    if cached_version == version:
        _pass(f"Cached plugin.json version matches source: {version}")
    else:
        _fail(f"Cached version ({cached_version}) does not match source ({version})")

    registered_version = entry.get("version", "")
    if registered_version == cached_version:
        _pass(f"Registration version matches cached plugin.json: {registered_version}")
    else:
        _fail(f"Registration version ({registered_version}) does not match cached ({cached_version})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate post-install state of the CRE Skills Plugin."
    )
    parser.add_argument(
        "--claude-home",
        type=str,
        default=os.path.expanduser("~/.claude"),
        help="Path to Claude home directory (default: ~/.claude)",
    )
    parser.add_argument(
        "--install-dir",
        type=str,
        default=None,
        help="Path to the plugin repo root (default: auto-detect from script location)",
    )
    args = parser.parse_args()

    claude_home = Path(args.claude_home).resolve()

    if args.install_dir:
        install_dir = Path(args.install_dir).resolve()
    else:
        # Auto-detect: this script is at scripts/installer_smoke_test.py
        install_dir = Path(__file__).resolve().parent.parent

    print()
    print("  CRE Skills Plugin -- Installer Smoke Test")
    print("  " + "=" * 50)
    print(f"  Claude home:  {claude_home}")
    print(f"  Install dir:  {install_dir}")

    version = get_plugin_version(install_dir)
    if not version:
        print()
        _fail(f"Cannot read version from {install_dir / '.claude-plugin' / 'plugin.json'}")
        print()
        print(f"  Results: 0 passed, 1 failed, 0 skipped")
        return 1

    print(f"  Version:      {version}")

    check_cache_dir(claude_home, version)
    check_installed_plugins(claude_home, version)
    check_settings(claude_home)
    check_desktop_config()
    check_mcp_server_syntax(install_dir)
    check_version_consistency(claude_home, install_dir, version)

    # Summary
    print()
    print("  " + "=" * 50)
    print(f"  Results: {_passes} passed, {_failures} failed, {_skips} skipped")
    print()

    if _failures > 0:
        print("  OVERALL: FAIL")
        return 1
    else:
        print("  OVERALL: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
