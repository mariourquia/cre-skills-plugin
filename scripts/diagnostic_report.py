#!/usr/bin/env python3
"""
Diagnostic report generator for cre-skills-plugin installer failures.

Collects system info, Claude state, and error context, then:
  1. Writes a report to ~/.claude/cre-skills-diagnostic.txt
  2. Builds a pre-filled GitHub issue URL
  3. Copies URL to clipboard (best-effort)
  4. Opens URL in browser (best-effort, unless --no-browser)

Usage:
  python3 scripts/diagnostic_report.py --error "message" --step "install"
  python3 scripts/diagnostic_report.py --error "message" --step "install" --no-browser
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import textwrap
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ───────────────────────────────────────────────────────────

REPO_OWNER = "mariourquia"
REPO_NAME = "cre-skills-plugin"
PLUGIN_NAME = "cre-skills"
PLUGIN_KEY = "cre-skills@local"
ISSUES_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new"
MAX_URL_LENGTH = 8000  # GitHub rejects URLs much beyond ~8200 chars
MAX_BODY_CHARS = 6000  # Leave room for title, labels, URL overhead

# ── Diagnostics collection ──────────────────────────────────────────────


def _run(cmd: list[str], timeout: int = 5) -> str:
    """Run a command and return stdout, or an error string."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip() or result.stderr.strip() or "(empty)"
    except FileNotFoundError:
        return "(not found)"
    except subprocess.TimeoutExpired:
        return "(timeout)"
    except Exception as exc:
        return f"(error: {exc})"


def collect_system_info() -> dict:
    """Collect OS, Python, Node, and Claude CLI info."""
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "arch": platform.machine(),
        "python_version": platform.python_version(),
        "python_path": sys.executable,
    }

    # Node version
    info["node_version"] = _run(["node", "--version"])

    # Claude CLI
    claude_path = shutil.which("claude")
    info["claude_cli_path"] = claude_path or "(not found)"
    if claude_path:
        info["claude_cli_version"] = _run([claude_path, "--version"])
    else:
        info["claude_cli_version"] = "(n/a)"

    return info


def collect_claude_state() -> dict:
    """Check ~/.claude directory state."""
    claude_home = Path.home() / ".claude"
    state = {
        "claude_home_exists": claude_home.is_dir(),
    }

    # installed_plugins.json
    plugins_file = claude_home / "installed_plugins.json"
    if plugins_file.is_file():
        try:
            data = json.loads(plugins_file.read_text(encoding="utf-8"))
            state["installed_plugins_keys"] = list(data.keys()) if isinstance(data, dict) else str(type(data))
            state["plugin_registered"] = PLUGIN_KEY in data if isinstance(data, dict) else False
        except Exception as exc:
            state["installed_plugins_error"] = str(exc)
    else:
        state["installed_plugins_exists"] = False

    # settings.json enabledPlugins
    settings_file = claude_home / "settings.json"
    if settings_file.is_file():
        try:
            data = json.loads(settings_file.read_text(encoding="utf-8"))
            enabled = data.get("enabledPlugins", [])
            state["enabled_plugins"] = enabled
            state["plugin_enabled"] = PLUGIN_KEY in enabled
        except Exception as exc:
            state["settings_error"] = str(exc)
    else:
        state["settings_exists"] = False

    return state


# ── Report generation ───────────────────────────────────────────────────


def build_report(error_msg: str, step: str, sys_info: dict, claude_state: dict) -> str:
    """Build a human-readable diagnostic report."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"# {PLUGIN_NAME} Diagnostic Report",
        f"Generated: {ts}",
        "",
        "## Error",
        f"Step: {step}",
        f"Message: {error_msg}",
        "",
        "## System",
    ]
    for key, val in sys_info.items():
        lines.append(f"  {key}: {val}")

    lines.append("")
    lines.append("## Claude State")
    for key, val in claude_state.items():
        lines.append(f"  {key}: {val}")

    return "\n".join(lines)


def write_report(report: str) -> Path:
    """Write the report to ~/.claude/ and return the path."""
    claude_home = Path.home() / ".claude"
    claude_home.mkdir(parents=True, exist_ok=True)
    report_path = claude_home / f"{PLUGIN_NAME}-diagnostic.txt"
    report_path.write_text(report, encoding="utf-8")
    return report_path


def build_issue_url(error_msg: str, step: str, report: str) -> str:
    """Build a pre-filled GitHub issue URL."""
    title = f"[Installer] {step} failed: {error_msg[:80]}"

    body = textwrap.dedent(f"""\
    ## What happened

    The installer failed during the **{step}** step.

    ## Error message

    ```
    {error_msg}
    ```

    ## Diagnostic report

    <details>
    <summary>Click to expand</summary>

    ```
    {report}
    ```

    </details>

    ## Steps to reproduce

    1. Downloaded the installer
    2. Ran the installer
    3. Got the error above

    ## Additional context

    <!-- Add any other context here -->
    """)

    # Truncate body if needed to stay under URL limits
    if len(body) > MAX_BODY_CHARS:
        body = body[:MAX_BODY_CHARS] + "\n\n(truncated -- full report saved locally)"

    params = {
        "title": title,
        "body": body,
        "labels": "bug,installer",
    }
    url = f"{ISSUES_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"

    # Final safety check on total URL length
    if len(url) > MAX_URL_LENGTH:
        # Strip body down further
        short_body = f"Installer failed at step: {step}\nError: {error_msg}\n\n(Full diagnostic saved to ~/.claude/{PLUGIN_NAME}-diagnostic.txt)"
        params["body"] = short_body
        url = f"{ISSUES_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"

    return url


# ── Clipboard and browser helpers ───────────────────────────────────────


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard. Returns True on success."""
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True, timeout=5)
            return True
        elif system == "Windows":
            subprocess.run(["clip"], input=text.encode(), check=True, timeout=5)
            return True
        elif system == "Linux":
            # Try xclip first, then xsel
            for cmd in [["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]:
                try:
                    subprocess.run(cmd, input=text.encode(), check=True, timeout=5)
                    return True
                except FileNotFoundError:
                    continue
    except Exception:
        pass
    return False


def open_in_browser(url: str) -> bool:
    """Open URL in default browser. Returns True on success."""
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["open", url], check=True, timeout=10)
            return True
        elif system == "Windows":
            subprocess.run(["cmd", "/c", "start", "", url], check=True, timeout=10)
            return True
        elif system == "Linux":
            subprocess.run(["xdg-open", url], check=True, timeout=10)
            return True
    except Exception:
        pass
    return False


# ── Main ────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Generate a diagnostic report for {PLUGIN_NAME} installer failures."
    )
    parser.add_argument(
        "--error",
        required=True,
        help="The error message that occurred.",
    )
    parser.add_argument(
        "--step",
        required=True,
        help="The installer step that failed (e.g., install, venv, register).",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Skip opening the browser.",
    )
    args = parser.parse_args()

    # Collect diagnostics
    sys_info = collect_system_info()
    claude_state = collect_claude_state()

    # Build and write report
    report = build_report(args.error, args.step, sys_info, claude_state)
    report_path = write_report(report)

    # Build issue URL
    issue_url = build_issue_url(args.error, args.step, report)

    # Output
    print("")
    print(f"  Diagnostic report saved to: {report_path}")
    print("")

    # Clipboard
    if copy_to_clipboard(issue_url):
        print("  Bug report URL copied to clipboard.")
    else:
        print("  Could not copy to clipboard.")

    print("")
    print(f"  Submit a bug report: {issue_url[:120]}...")
    print("")

    # Browser
    if not args.no_browser:
        if open_in_browser(issue_url):
            print("  Opened bug report in browser.")
        else:
            print("  Could not open browser. Use the URL above to submit a report.")
    else:
        print("  (--no-browser flag set, skipping browser open)")


if __name__ == "__main__":
    main()
