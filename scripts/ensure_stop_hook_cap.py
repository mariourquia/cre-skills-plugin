#!/usr/bin/env python3
"""
ensure_stop_hook_cap.py -- Raise the Claude Code Stop-hook block cap for plugin users.

Claude Code Stop hooks may block a turn from ending up to
``CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`` consecutive times before the harness
force-ends the turn. The default is low (9), which truncates the long
agent-driven loops this plugin's skills and workflows rely on. This helper
ensures the cap is at least ``FLOOR`` (100) in the user's settings.json.

Behavior (idempotent, raise-only, safe):
  - Targets ``<claude-home>/settings.json`` where claude-home defaults to
    ``~/.claude`` (overridable via ``--claude-home`` or the CLAUDE_CONFIG_DIR
    env var, which is Claude Code's own config-dir convention).
  - Missing file        -> create as a minimal valid ``{}`` (parent dir too).
  - Invalid JSON        -> never overwrite/corrupt; warn to stderr, exit 0.
  - The cap value is stored as a STRING (env block values are strings).
    Unset / non-numeric / integer < FLOOR -> set to "100".
    Integer >= FLOOR                       -> left unchanged (RAISE-ONLY; this
    lets a higher value, e.g. cre-skills-pro's 500, win for users with both).
  - All other keys are preserved (load whole object, set one key, dump with
    indent=2). The write is ATOMIC (temp file + os.replace).
  - Never crashes the caller: every failure path warns to stderr and exits 0.

Usage:
    python3 scripts/ensure_stop_hook_cap.py
    python3 scripts/ensure_stop_hook_cap.py --claude-home /path/to/.claude

Exit code: always 0 (best-effort; must never abort an install or verify).
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ENV_KEY = "CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"
FLOOR = 100


def resolve_claude_home(explicit: str | None = None) -> Path:
    """Resolve the Claude Code config directory.

    Precedence: explicit --claude-home > $CLAUDE_CONFIG_DIR > ~/.claude.
    Defaulting to ~/.claude matches the rest of this repo's installers.
    """
    if explicit:
        return Path(explicit).expanduser()
    env_dir = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
    if env_dir:
        return Path(env_dir).expanduser()
    return Path.home() / ".claude"


def _load_settings(settings_file: Path) -> dict | None:
    """Load settings.json.

    Returns the parsed object, or ``{}`` if the file is missing. Returns
    ``None`` to signal "present but unparseable" (the caller must then leave
    the file untouched). Uses utf-8-sig so a BOM written by Windows PowerShell
    5.1 (Set-Content -Encoding UTF8) does not register as a parse failure --
    consistent with the other JSON readers in scripts/.
    """
    if not settings_file.exists():
        return {}
    try:
        with open(settings_file, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    # A valid JSON file whose top level is not an object (e.g. a list or a
    # scalar) is not something we can safely add a key to; treat as unparseable.
    if not isinstance(data, dict):
        return None
    return data


def _current_cap(data: dict) -> str | None:
    """Return the current cap value as found under env, or None if absent."""
    env = data.get("env")
    if not isinstance(env, dict):
        return None
    if ENV_KEY not in env:
        return None
    return env[ENV_KEY]


def _meets_floor(value) -> bool:
    """True iff ``value`` parses as an integer >= FLOOR.

    Anything non-numeric, fractional, or below the floor returns False so the
    caller raises it. Accepts both string ("500") and int (500) forms.
    """
    try:
        return int(str(value).strip()) >= FLOOR
    except (TypeError, ValueError):
        return False


def _atomic_write_json(settings_file: Path, data: dict) -> None:
    """Write ``data`` to ``settings_file`` atomically (temp + os.replace)."""
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=str(settings_file.parent),
        prefix=settings_file.name + ".",
        suffix=".tmp",
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp_path, settings_file)
    except BaseException:
        # Clean up the temp file on any failure; never leave litter behind.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def ensure_cap(claude_home: Path) -> int:
    """Ensure the Stop-hook block cap is >= FLOOR. Always returns 0.

    Prints exactly one status line on the happy path:
      ``stop-hook block cap: raised to 100 (was <old>)`` or
      ``stop-hook block cap: already <n> (>=100), left as-is``.
    """
    settings_file = claude_home / "settings.json"

    data = _load_settings(settings_file)
    if data is None:
        # Present but unparseable -- do NOT touch it. Warn and bow out.
        print(
            f"[WARN] {settings_file} is not valid JSON; leaving it untouched. "
            f"Set {ENV_KEY} >= {FLOOR} manually to avoid truncated agent loops.",
            file=sys.stderr,
        )
        return 0

    current = _current_cap(data)

    if _meets_floor(current):
        print(
            f"stop-hook block cap: already {current} (>={FLOOR}), left as-is"
        )
        return 0

    # Raise to the floor. Display the prior value as the original (unset shown
    # as 'unset'); store the new value as a STRING to match env-block typing.
    old_display = "unset" if current is None else current
    env = data.get("env")
    if not isinstance(env, dict):
        env = {}
        data["env"] = env
    env[ENV_KEY] = str(FLOOR)

    _atomic_write_json(settings_file, data)
    print(f"stop-hook block cap: raised to {FLOOR} (was {old_display})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Ensure CLAUDE_CODE_STOP_HOOK_BLOCK_CAP is >= 100 in the user's "
            "Claude Code settings.json (raise-only, never lowers)."
        )
    )
    parser.add_argument(
        "--claude-home",
        type=str,
        default=None,
        help="Path to the Claude config dir (default: $CLAUDE_CONFIG_DIR or ~/.claude)",
    )
    args = parser.parse_args()

    try:
        claude_home = resolve_claude_home(args.claude_home)
        return ensure_cap(claude_home)
    except Exception as exc:  # noqa: BLE001 -- must never crash the caller
        print(
            f"[WARN] Could not ensure {ENV_KEY}: {exc}. "
            "This is non-fatal; continuing.",
            file=sys.stderr,
        )
        return 0


if __name__ == "__main__":
    sys.exit(main())
