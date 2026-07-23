from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOKS_DIR = ROOT / "src" / "hooks"


def _write_large_stdin_without_broken_pipe(script: Path, tmp_path: Path) -> tuple[str, str]:
    env = dict(os.environ)
    env["HOME"] = str(tmp_path)
    env["PLUGIN_ROOT"] = str(ROOT)
    process = subprocess.Popen(
        ["node", str(script)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    assert process.stdin is not None
    try:
        process.stdin.write(b'{"payload":"' + (b"x" * 2_000_000) + b'"}')
        process.stdin.close()
    except BrokenPipeError as exc:  # pragma: no cover - regression message
        process.kill()
        raise AssertionError(f"{script.name} closed stdin before consuming the hook payload") from exc

    assert process.stdout is not None
    assert process.stderr is not None
    stdout = process.stdout.read().decode("utf-8")
    stderr = process.stderr.read().decode("utf-8")
    assert process.wait(timeout=10) == 0, stderr
    return stdout, stderr


def test_manifest_uses_only_cross_harness_command_hooks() -> None:
    manifest = json.loads((HOOKS_DIR / "hooks.json").read_text(encoding="utf-8"))
    handlers = [
        handler
        for groups in manifest["hooks"].values()
        for group in groups
        for handler in group["hooks"]
    ]
    assert handlers
    assert {handler["type"] for handler in handlers} == {"command"}
    assert any("session-context.mjs" in handler["command"] for handler in handlers)


def test_session_context_is_concise_and_consumes_stdin(tmp_path: Path) -> None:
    stdout, stderr = _write_large_stdin_without_broken_pipe(
        HOOKS_DIR / "session-context.mjs", tmp_path
    )
    assert stderr == ""
    assert "CRE-ROUTING.md" in stdout
    assert "/cre-skills:cre-route" in stdout
    assert len(stdout) < 500


def test_stop_hook_consumes_stdin_before_optional_telemetry_exit(tmp_path: Path) -> None:
    stdout, stderr = _write_large_stdin_without_broken_pipe(
        HOOKS_DIR / "session-summary.mjs", tmp_path
    )
    assert stdout == ""
    assert stderr == ""


def test_post_tool_hook_consumes_stdin_when_config_is_missing(tmp_path: Path) -> None:
    stdout, stderr = _write_large_stdin_without_broken_pipe(
        HOOKS_DIR / "telemetry-capture.mjs", tmp_path
    )
    assert stdout == ""
    assert stderr == ""
