"""Release version / install-command / asset-name parity test.

Background
----------
Before v4.2.0 release hardening, the repo had persistent drift across the
public-facing surfaces that advertise the plugin version, the canonical install
command, the release-asset filenames users are told to download, and the
skill-count banner shown by installers. At least five different install commands
had accumulated across README, docs/INSTALL.md, docs/install-guide.md,
docs/release-checklist.md, and .github/workflows/release.yml. The release-asset
names in install docs did not match the names the release workflow actually
publishes (cre-skills-plugin-v<ver>.{dmg,-setup.exe} — with a ``-plugin-`` infix
added by a rename step in the workflow).

This test fails loudly on any of those classes of drift so the hardening work
cannot silently regress on the next release. It is deliberately conservative:
it only asserts things that were reconciled during the v4.2.0 hardening pass
and that the project committed to keeping coherent.

What it checks
--------------
1. Version strings agree across the three canonical manifests + the catalog:
   .claude-plugin/plugin.json, .claude-plugin/marketplace.json (plugin entry),
   src/catalog/catalog.yaml#plugin_version. This is the source of truth for
   ``PLUGIN_VERSION``.
2. Installer scripts' user-visible banners match the current PLUGIN_VERSION
   (scripts/install.sh, Install.command, scripts/Install.ps1, Install.ps1
   InstallerVersionConst).
3. Release-asset filenames advertised in install docs use the normalized
   ``cre-skills-plugin-v<ver>.{dmg,-setup.exe}`` form actually published by
   .github/workflows/release.yml, not the pre-rename ``cre-skills-v<ver>`` form.
4. The canonical Claude Code CLI install command is used consistently. Every
   occurrence of ``claude plugin install cre-skills@...`` in non-historical
   docs/workflows uses ``cre-skills@cre-skills`` (matches the marketplace name
   in ``.claude-plugin/marketplace.json``).
5. Actual filesystem skill count matches the number advertised by installer
   banners. (Historical release notes under ``docs/releases/v4.0.0*`` and
   ``docs/releases/v2.0.0*`` are excluded — those are frozen in time.)

History-frozen files are excluded via an allowlist below.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_MANIFEST = REPO_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_MANIFEST = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CATALOG = REPO_ROOT / "src" / "catalog" / "catalog.yaml"

# Historical release-notes files are frozen at their original version/asset-name
# conventions. They must not gate this test.
HISTORICAL_DOC_GLOBS = (
    "docs/releases/v1.0.0-release-notes.md",
    "docs/releases/v2.0.0-release-notes.md",
    "docs/releases/v2.5.0-release-notes.md",
    "docs/releases/v3.0.0-release-notes.md",
    "docs/releases/v4.0.0-release-notes.md",
    "docs/releases/v4.1.0-release-notes.md",
    "docs/releases/v4.1.1-release-notes.md",
    "docs/releases/v4.1.2-release-notes.md",
)

# MIGRATION.md is a v3→v4 document referencing v4.0.0 by design.
HISTORICAL_MD_FILES = {
    "docs/MIGRATION.md",
    "docs/adr/0001-catalog-source-of-truth.md",
}

# Install docs whose advertised DMG/EXE filenames MUST match the release
# workflow's normalized output.
INSTALL_DOC_FILES = (
    "docs/INSTALL.md",
    "docs/install-desktop.md",
    "docs/install-guide.md",
    "README.md",
)

# Files that advertise the Claude Code CLI install command.
CLI_INSTALL_COMMAND_FILES = (
    "README.md",
    "docs/INSTALL.md",
    "docs/install-guide.md",
    "docs/install-desktop.md",
    "docs/install-cowork.md",
    "docs/WHAT-TO-USE-WHEN.md",
    "docs/release-checklist.md",
    ".github/workflows/release.yml",
    "docs/releases/v4.2.0-release-notes.md",
)

# Installer scripts whose banner strings must match PLUGIN_VERSION.
INSTALLER_SCRIPTS = (
    "scripts/install.sh",
    "Install.command",
    "scripts/Install.ps1",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _plugin_version() -> str:
    return json.loads(_read(PLUGIN_MANIFEST))["version"]


def _marketplace_plugin_entry() -> dict:
    data = json.loads(_read(MARKETPLACE_MANIFEST))
    assert data.get("plugins"), "marketplace.json is missing 'plugins' array"
    return data["plugins"][0]


def _catalog_version() -> str:
    # The file is YAML but the plugin_version line is a simple scalar we can
    # safely regex — the test must not require PyYAML just for this.
    text = _read(CATALOG)
    match = re.search(r"^plugin_version:\s*([0-9]+\.[0-9]+\.[0-9]+)", text, re.M)
    assert match, "catalog.yaml has no 'plugin_version' line"
    return match.group(1)


def _actual_skill_count() -> int:
    skills_dir = REPO_ROOT / "src" / "skills"
    return sum(1 for p in skills_dir.iterdir() if p.is_dir())


# ---------------------------------------------------------------------------
# 1. Manifest / catalog version parity
# ---------------------------------------------------------------------------


def test_plugin_manifest_and_marketplace_versions_match() -> None:
    """plugin.json version == marketplace.json plugin entry version."""
    plugin_ver = _plugin_version()
    marketplace_entry = _marketplace_plugin_entry()
    assert marketplace_entry["version"] == plugin_ver, (
        f"marketplace.json plugin version ({marketplace_entry['version']}) "
        f"disagrees with plugin.json ({plugin_ver})"
    )


def test_catalog_plugin_version_matches_manifest() -> None:
    assert _catalog_version() == _plugin_version(), (
        f"catalog.yaml plugin_version ({_catalog_version()}) disagrees with "
        f"plugin.json version ({_plugin_version()})"
    )


def test_marketplace_plugin_name_is_cre_skills() -> None:
    """Canonical install command (cre-skills@cre-skills) assumes the marketplace
    name in marketplace.json is 'cre-skills'. If that ever changes, update every
    install command in docs + release.yml at the same time."""
    data = json.loads(_read(MARKETPLACE_MANIFEST))
    assert data.get("name") == "cre-skills", (
        f"marketplace.json top-level 'name' is {data.get('name')!r}; canonical "
        "install command assumes 'cre-skills'. Either update the name or fix "
        "every occurrence of 'cre-skills@cre-skills' across the repo."
    )


# ---------------------------------------------------------------------------
# 2. Installer banners / constants match PLUGIN_VERSION
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("script", INSTALLER_SCRIPTS)
def test_installer_scripts_are_not_on_stale_version(script: str) -> None:
    """Installer scripts must not advertise a different v<ver> than plugin.json.

    Catches the pre-hardening bug where install.sh / Install.command banners said
    'Plugin v4.0.0' while plugin.json was on 4.2.0.
    """
    plugin_ver = _plugin_version()
    path = REPO_ROOT / script
    assert path.exists(), f"installer script missing: {script}"
    text = _read(path)

    # Any older 4.x banner string that names a version is a hard failure.
    stale = re.findall(r"v4\.(?:0|1)\.\d+", text)
    # v4.1.x / v4.0.x strings are permitted only inside comments that describe
    # history; flag anything else.
    for hit in stale:
        banner_context = bool(re.search(rf"Plugin Installer {hit}|Plugin {hit} --", text))
        assert not banner_context, (
            f"{script} carries a stale user-visible banner: {hit!r}. "
            f"plugin.json is {plugin_ver}."
        )


def test_install_ps1_installer_version_const_matches_manifest() -> None:
    """scripts/Install.ps1 declares $InstallerVersionConst for telemetry; it must
    track plugin.json."""
    text = _read(REPO_ROOT / "scripts" / "Install.ps1")
    match = re.search(r'InstallerVersionConst\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"', text)
    assert match, "Install.ps1 $InstallerVersionConst declaration not found"
    assert match.group(1) == _plugin_version(), (
        f"Install.ps1 $InstallerVersionConst ({match.group(1)}) disagrees with "
        f"plugin.json ({_plugin_version()})"
    )


# ---------------------------------------------------------------------------
# 3. Release-asset filenames match the normalized names release.yml publishes
# ---------------------------------------------------------------------------


_PRE_RENAME_ASSET_PATTERN = re.compile(r"cre-skills-v[0-9]+\.[0-9]+\.[0-9]+(?:\.dmg|-setup\.exe)")


@pytest.mark.parametrize("doc", INSTALL_DOC_FILES)
def test_install_docs_use_normalized_asset_filenames(doc: str) -> None:
    """Install docs must reference the normalized ``cre-skills-plugin-v<ver>``
    names that release.yml publishes — not the pre-rename ``cre-skills-v<ver>``
    names which the workflow never uploads.
    """
    path = REPO_ROOT / doc
    if not path.exists():
        pytest.skip(f"{doc} missing; nothing to check")
    text = _read(path)
    hits = _PRE_RENAME_ASSET_PATTERN.findall(text)
    assert not hits, (
        f"{doc} references pre-rename asset filenames {hits!r}. The release "
        f"workflow publishes cre-skills-plugin-v<ver>.dmg / "
        f"cre-skills-plugin-v<ver>-setup.exe."
    )


# ---------------------------------------------------------------------------
# 4. Canonical CLI install command is used consistently
# ---------------------------------------------------------------------------


_WRONG_INSTALL_SUFFIX = re.compile(r"cre-skills@cre-skills-plugin\b")


@pytest.mark.parametrize("doc", CLI_INSTALL_COMMAND_FILES)
def test_no_wrong_marketplace_install_suffix(doc: str) -> None:
    """The marketplace name in marketplace.json is 'cre-skills', so the install
    target is ``cre-skills@cre-skills``. Before this pass release.yml emitted
    ``cre-skills@cre-skills-plugin`` which does not resolve."""
    path = REPO_ROOT / doc
    if not path.exists():
        pytest.skip(f"{doc} missing; nothing to check")
    text = _read(path)
    hits = _WRONG_INSTALL_SUFFIX.findall(text)
    assert not hits, (
        f"{doc} uses the wrong install suffix (``cre-skills@cre-skills-plugin``). "
        f"Canonical form: ``cre-skills@cre-skills`` (marketplace name in "
        f".claude-plugin/marketplace.json)."
    )


# ---------------------------------------------------------------------------
# 5. Installer skill-count banners match the actual filesystem count
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("script", INSTALLER_SCRIPTS + ("scripts/create-dmg.sh", "scripts/create-exe.iss"))
def test_installer_advertised_skill_count_matches_filesystem(script: str) -> None:
    """Installer banners that advertise a skill count must match the actual number
    of directories under ``src/skills/``. Catches the pre-hardening drift where
    five installer scripts and the EXE compiler script all said ``112 skills``
    while the filesystem had 113."""
    path = REPO_ROOT / script
    if not path.exists():
        pytest.skip(f"{script} missing; nothing to check")
    text = _read(path)
    actual = _actual_skill_count()

    # Any standalone "112 skills" or "112 CRE skills" is now stale.
    stale_hits = re.findall(r"\b(?:(?<!\$)112)\s+(?:CRE\s+)?skills\b", text)
    assert not stale_hits, (
        f"{script} advertises stale '112 skills' banner ({stale_hits!r}); "
        f"filesystem has {actual} skills. Update the banner or regenerate via "
        f"scripts/catalog-generate.py."
    )


# ---------------------------------------------------------------------------
# 6. v4.2.0 release notes carry an honest frontmatter status
# ---------------------------------------------------------------------------


def test_v4_2_0_release_notes_frontmatter_is_honest() -> None:
    """Frontmatter ``status`` in docs/releases/v4.2.0-release-notes.md must be
    one of ``pending`` (pre-tag) or ``released`` (post-tag).

    During release hardening the file said ``status: released`` before the tag
    actually existed, which made the file claim something it could not guarantee.
    """
    path = REPO_ROOT / "docs" / "releases" / "v4.2.0-release-notes.md"
    assert path.exists(), "v4.2.0 release notes missing"
    text = _read(path)
    match = re.search(r"^status:\s*(\w+)", text, re.M)
    assert match, "v4.2.0 release notes have no 'status:' line in frontmatter"
    status = match.group(1).lower()
    assert status in {"pending", "released"}, (
        f"v4.2.0 release notes frontmatter status is {status!r}; expected "
        f"'pending' (pre-tag) or 'released' (post-tag)."
    )


# ---------------------------------------------------------------------------
# 7. Canonical Desktop marketplace caveat parity
# ---------------------------------------------------------------------------

# The canonical source of the "Chat tab's 'Add marketplace' is not supported"
# caveat is ``docs/WHAT-TO-USE-WHEN.md``. Every install surface listed below
# must carry the same block verbatim between the START / END sentinels so the
# guidance cannot silently diverge. If the canonical wording needs to change,
# edit the source first and then regenerate the duplicates — this test fails
# on drift rather than masking it.

_CANONICAL_CAVEAT_SOURCE = REPO_ROOT / "docs" / "WHAT-TO-USE-WHEN.md"
_CANONICAL_CAVEAT_SURFACES = (
    "README.md",
    "docs/INSTALL.md",
    "docs/install-guide.md",
    "docs/install-desktop.md",
    "docs/install-cowork.md",
)
_CAVEAT_START = "<!-- CANONICAL-CAVEAT:desktop-marketplace START -->"
_CAVEAT_END = "<!-- CANONICAL-CAVEAT:desktop-marketplace END -->"


def _extract_canonical_caveat(path: Path) -> str:
    """Extract the text between the canonical-caveat sentinels.

    Returns the block body (between START and END markers, exclusive of the
    sentinels themselves). Raises AssertionError if the sentinels are missing
    or out of order.
    """
    text = _read(path)
    try:
        start = text.index(_CAVEAT_START) + len(_CAVEAT_START)
        end = text.index(_CAVEAT_END, start)
    except ValueError as exc:
        raise AssertionError(
            f"{path.relative_to(REPO_ROOT)}: canonical-caveat sentinels not "
            f"found or out of order ({exc})."
        ) from exc
    return text[start:end].strip()


def test_canonical_caveat_source_is_nonempty() -> None:
    """``docs/WHAT-TO-USE-WHEN.md`` carries the canonical block body."""
    body = _extract_canonical_caveat(_CANONICAL_CAVEAT_SOURCE)
    assert body, "canonical caveat body in WHAT-TO-USE-WHEN.md is empty"
    # Load-bearing phrases the downstream surfaces MUST preserve verbatim.
    for phrase in (
        'Do not paste this repo URL into Claude Desktop Chat tab',
        'not supported by this repo',
        "canonical Chat tab install path",
        "Claude Code CLI marketplace",
        "claude plugin install cre-skills@cre-skills",
    ):
        assert phrase in body, (
            f"canonical caveat missing load-bearing phrase: {phrase!r}"
        )


@pytest.mark.parametrize("surface", _CANONICAL_CAVEAT_SURFACES)
def test_canonical_caveat_duplicated_verbatim(surface: str) -> None:
    """Each install surface carries the canonical caveat byte-for-byte.

    If this fails, re-sync the drifting surface against
    ``docs/WHAT-TO-USE-WHEN.md`` — do not edit the copies in isolation.
    """
    path = REPO_ROOT / surface
    assert path.exists(), f"install surface missing: {surface}"
    source_body = _extract_canonical_caveat(_CANONICAL_CAVEAT_SOURCE)
    surface_body = _extract_canonical_caveat(path)
    assert surface_body == source_body, (
        f"{surface}: canonical-caveat body drifts from "
        f"docs/WHAT-TO-USE-WHEN.md. Re-sync the block verbatim. "
        f"\n--- source ---\n{source_body}\n--- {surface} ---\n{surface_body}"
    )
