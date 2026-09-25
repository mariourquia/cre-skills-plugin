#!/usr/bin/env python3
"""Regression gate for the Node.js floor warning in the shell installers.

install.sh's check_node() and verify-install.sh's inline "Check Node.js
version" block both WARN (never hard-fail) when the running Node major is
below the installable-package floor. These tests never reimplement that
comparison: they extract the *real*, current text of the script (the whole
file minus its trailing entrypoint call, for install.sh; a bounded prefix +
the check block itself, for verify-install.sh) and execute it in an isolated
bash subprocess with a real Node binary placed first on PATH, so the
assertions exercise actual runtime behavior, not a string match on source.

The Node binaries used are already installed via nvm on this machine (never
installed, uninstalled, or relinked here); a case is skipped, not failed, on
a machine that lacks one.
"""
import os
import re
import subprocess
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN_ROOT / "scripts"
INSTALL_SH = SCRIPTS / "install.sh"
VERIFY_INSTALL_SH = SCRIPTS / "verify-install.sh"

NVM_VERSIONS = Path.home() / ".nvm" / "versions" / "node"


def _node_bindir(major: int) -> str | None:
    """Absolute bin/ dir of an installed nvm Node matching `major`, or None."""
    if not NVM_VERSIONS.is_dir():
        return None
    for d in sorted(NVM_VERSIONS.iterdir()):
        if d.name.startswith(f"v{major}."):
            return str(d / "bin")
    return None


def _run_bash(
    preamble: str, call: str, node_bindir: str | None, timeout: int = 10
) -> subprocess.CompletedProcess:
    """Run `preamble` (real script text, functions/vars only) then `call` in
    a fresh bash subprocess, with `node_bindir` first on PATH. Returns the
    completed process (stdout/stderr captured as text)."""
    env = dict(os.environ)
    if node_bindir:
        env["PATH"] = f"{node_bindir}:{env.get('PATH', '')}"
    script = preamble + "\n" + call + "\n"
    return subprocess.run(
        ["bash", "-c", script],
        capture_output=True, text=True, env=env, timeout=timeout,
    )


class TestInstallShNodeFloor(unittest.TestCase):
    """install.sh's check_node(): warn-only Node-major floor.

    Sourcing the real file minus its trailing `main "$@"` call defines every
    function (including check_node, and the success()/warn() it calls) with
    zero side effects -- no install step runs, only function definitions.
    """

    @classmethod
    def setUpClass(cls):
        lines = INSTALL_SH.read_text(encoding="utf-8").splitlines()
        while lines and not lines[-1].strip():
            lines.pop()
        assert lines[-1].strip() == 'main "$@"', (
            f"install.sh's trailing line changed shape: {lines[-1]!r}; "
            "update this extraction before trusting the test."
        )
        cls.preamble = "\n".join(lines[:-1])

    def _check_node(self, major):
        bindir = _node_bindir(major)
        if bindir is None:
            self.skipTest(f"no nvm-installed Node {major}.x on this machine")
        proc = _run_bash(self.preamble, "check_node", bindir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def test_node_20_is_below_the_floor_and_only_warns(self):
        out = self._check_node(20)
        self.assertIn("WARN", out)
        self.assertIn("v22+", out, "warning text must cite the current floor (22)")
        self.assertNotIn("[FAIL]", out, "the check is warn-only, never a hard failure")

    def test_node_22_satisfies_the_floor(self):
        out = self._check_node(22)
        self.assertIn("[OK]", out)
        self.assertNotIn("WARN", out)

    def test_node_24_satisfies_the_floor(self):
        out = self._check_node(24)
        self.assertIn("[OK]", out)
        self.assertNotIn("WARN", out)


class TestVerifyInstallShNodeFloor(unittest.TestCase):
    """verify-install.sh's inline Node-version check: warn-only, same floor.

    Extracts (a) the color/helper/counter preamble (set -euo pipefail through
    the WARNINGS=0 init -- no check actually runs) and (b) the real "Check
    Node.js version" block verbatim, so checks 1-5 (plugin registration,
    file scans, ~/.cre-skills writes) never execute -- only the Node check.
    """

    @classmethod
    def setUpClass(cls):
        text = VERIFY_INSTALL_SH.read_text(encoding="utf-8")
        pre_m = re.search(r"(set -euo pipefail\n.*?\nWARNINGS=0\n)", text, re.S)
        assert pre_m, "verify-install.sh preamble shape changed; update this extraction"
        chk_m = re.search(r"(  # Check Node\.js version\n.*?\n  fi\n)", text, re.S)
        assert chk_m, "verify-install.sh's Node-version check block not found"
        cls.preamble = pre_m.group(1) + "\n" + chk_m.group(1)

    def _check(self, major):
        bindir = _node_bindir(major)
        if bindir is None:
            self.skipTest(f"no nvm-installed Node {major}.x on this machine")
        proc = _run_bash(self.preamble, "true", bindir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def test_node_20_is_below_the_floor_and_only_warns(self):
        out = self._check(20)
        self.assertIn("WARN", out)
        self.assertIn("v22+", out, "warning text must cite the current floor (22)")
        self.assertNotIn("FAIL", out, "the check is warn-only, never a hard failure")

    def test_node_22_satisfies_the_floor(self):
        out = self._check(22)
        self.assertEqual(out, "", "no warning at/above the floor")

    def test_node_24_satisfies_the_floor(self):
        out = self._check(24)
        self.assertEqual(out, "", "no warning at/above the floor")


if __name__ == "__main__":
    unittest.main()
