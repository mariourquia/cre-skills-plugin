"""Behavior tests for scripts/release-bump.py on a fixture tree (no repo mutation)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "release-bump.py"


def make_fixture(root: Path, version: str = "1.0.0") -> None:
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "cre-skills", "version": version}, indent=2) + "\n",
        encoding="utf-8",
    )
    (root / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(
            {"name": "cre-skills", "plugins": [{"name": "cre-skills", "version": version}]},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "scripts").mkdir()
    (root / "scripts" / "install.sh").write_text(
        f"# installer for Plugin v{version}\n"
        f'plugin_version="$(true || echo "{version}")"\n'
        f"echo 'Plugin v{version} -- Installed'\n",
        encoding="utf-8",
    )
    (root / "Install.command").write_text(
        f'INSTALLER_VERSION_CONST="{version}"\n'
        f'printf "Plugin Installer v{version}\\n"\n'
        f'PLUGIN_VERSION="$(true || echo "{version}")"\n',
        encoding="utf-8",
    )
    (root / "scripts" / "Install.ps1").write_text(
        f'$InstallerVersionConst = "{version}"\n', encoding="utf-8"
    )
    (root / "docs").mkdir()
    (root / "docs" / "INSTALL.md").write_text(
        f"[`cre-skills-plugin-v{version}.dmg`](x) [`cre-skills-plugin-v{version}-setup.exe`](x)\n",
        encoding="utf-8",
    )
    (root / "docs" / "install-desktop.md").write_text(
        f"cre-skills-plugin-v{version}.dmg cre-skills-plugin-v{version}-setup.exe\n",
        encoding="utf-8",
    )
    (root / "docs" / "install-guide.md").write_text(
        f"Version {version} | Apache 2.0\n", encoding="utf-8"
    )
    (root / "README.md").write_text(f"banner\n  v{version}  ·  tagline\n", encoding="utf-8")


def run_bump(root: Path, new: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--version", new, "--root", str(root), "--no-regen"],
        capture_output=True,
        text=True,
    )


def test_bump_rewrites_every_pin(tmp_path):
    make_fixture(tmp_path)
    result = run_bump(tmp_path, "1.1.0")
    assert result.returncode == 0, result.stderr
    assert json.loads((tmp_path / ".claude-plugin" / "plugin.json").read_text())["version"] == "1.1.0"
    marketplace = json.loads((tmp_path / ".claude-plugin" / "marketplace.json").read_text())
    assert marketplace["plugins"][0]["version"] == "1.1.0"
    for rel in (
        "scripts/install.sh",
        "Install.command",
        "scripts/Install.ps1",
        "docs/INSTALL.md",
        "docs/install-desktop.md",
        "docs/install-guide.md",
        "README.md",
    ):
        text = (tmp_path / rel).read_text(encoding="utf-8")
        assert "1.0.0" not in text, f"{rel} kept a stale literal"
        assert "1.1.0" in text, f"{rel} was not bumped"
    assert "Manual follow-ups" in result.stdout


def test_bump_fails_loudly_when_marketplace_json_disagrees(tmp_path):
    make_fixture(tmp_path)
    (tmp_path / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps({"name": "cre-skills", "plugins": [{"name": "cre-skills", "version": "9.9.9"}]}),
        encoding="utf-8",
    )
    result = run_bump(tmp_path, "1.1.0")
    assert result.returncode != 0
    assert "marketplace.json" in (result.stderr + result.stdout)


def test_bump_refuses_same_version(tmp_path):
    make_fixture(tmp_path)
    result = run_bump(tmp_path, "1.0.0")
    assert result.returncode != 0
    assert "already at" in (result.stderr + result.stdout)


def test_bump_refuses_invalid_semver(tmp_path):
    make_fixture(tmp_path)
    result = run_bump(tmp_path, "not-a-version")
    assert result.returncode != 0
    assert "not valid semver" in (result.stderr + result.stdout)


def test_bump_fails_loudly_when_a_pin_site_lost_its_literal(tmp_path):
    make_fixture(tmp_path)
    (tmp_path / "docs" / "install-guide.md").write_text("no pin here\n", encoding="utf-8")
    result = run_bump(tmp_path, "1.1.0")
    assert result.returncode != 0
    assert "install-guide.md" in (result.stderr + result.stdout)
