"""Release-pin tripwire: every mechanical version pin matches plugin.json.

scripts/release-bump.py rewrites these pins in one shot; this test enforces
that none is missed or hand-drifted. Motivation: the 5.2.0 -> 5.2.1 release
hand-bumped some files and left the committed AMOS sample at 5.2.0, which
broke tests/test_amos_manifest.py on every fresh checkout. Any pin this test
covers must also be listed in release-bump.py's pin map (and vice versa).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
SAMPLE_PATH = REPO_ROOT / "docs" / "integrations" / "amos-skill-manifest.sample.json"

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
VERSION = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"]

# Three-part versions that legitimately appear in install.sh as HISTORY, not
# as pins of the current release (upgrade-path notes). Grow deliberately.
INSTALL_SH_HISTORICAL = {"2.0.0"}


def test_plugin_json_version_is_valid_semver():
    assert SEMVER.match(VERSION), f"plugin.json version {VERSION!r} is not semver"


def test_install_sh_pins_only_the_current_version():
    text = (REPO_ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
    found = set(re.findall(r"\bv?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\b", text))
    stale = found - INSTALL_SH_HISTORICAL - {VERSION}
    assert not stale, (
        f"install.sh carries version literals {sorted(stale)} != current {VERSION}; "
        "bump with scripts/release-bump.py (or add a deliberate historical entry here)"
    )
    assert VERSION in found, "install.sh no longer pins the current version banner"
    assert f'|| echo "{VERSION}"' in text, "install.sh version fallback literal drifted"


def test_install_docs_binary_links_pin_the_current_version():
    for rel in ("docs/INSTALL.md", "docs/install-desktop.md"):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert f"cre-skills-plugin-v{VERSION}.dmg" in text, f"{rel}: dmg link not at {VERSION}"
        assert f"cre-skills-plugin-v{VERSION}-setup.exe" in text, f"{rel}: exe link not at {VERSION}"
        cores = set(re.findall(r"cre-skills-plugin-v(\d+\.\d+\.\d+)", text))
        assert cores == {VERSION}, f"{rel}: stale binary versions {sorted(cores - {VERSION})}"


def test_install_guide_version_line_is_current():
    text = (REPO_ROOT / "docs" / "install-guide.md").read_text(encoding="utf-8")
    assert f"Version {VERSION} |" in text, f"docs/install-guide.md header not at {VERSION}"


def test_readme_header_pins_the_current_version():
    head = "\n".join(
        (REPO_ROOT / "README.md").read_text(encoding="utf-8").splitlines()[:12]
    )
    assert f"v{VERSION}" in head, f"README.md header block does not mention v{VERSION}"


def test_committed_amos_sample_is_stamped_with_the_current_version():
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    assert sample["plugin_version"] == VERSION, (
        f"committed AMOS sample plugin_version {sample['plugin_version']!r} != {VERSION}; "
        "regenerate with: python3 scripts/amos-manifest-build.py --emit-sample"
    )
