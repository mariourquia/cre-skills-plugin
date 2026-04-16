"""Catalog claim integrity.

Catches drift between published count claims (README, build-artifact hook
prompts) and the actual generated catalog. A drift audit found a stale "112"
count in README prose and in `builds/claude-code/hooks/hooks.json` while the
catalog and rest of the README said 113. This test prevents that class of
regression.

Source of truth: `src/catalog/catalog.yaml`. Every claim below is checked
against counts derived from that file.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
_CATALOG_PATH = _REPO_ROOT / "src" / "catalog" / "catalog.yaml"


def _load_catalog() -> Dict:
    with _CATALOG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _count_entries_by_type() -> Dict[str, int]:
    data = _load_catalog()
    # Catalog uses `items:` as the list of entries (not `entries:`).
    items = data.get("items") or data.get("entries") or []
    counts: Dict[str, int] = {}
    for entry in items:
        t = entry.get("type")
        if t:
            counts[t] = counts.get(t, 0) + 1
    return counts


def _actual_skill_count() -> int:
    """Every entry with type == 'skill' in the catalog."""
    return _count_entries_by_type().get("skill", 0)


def _scan_text_for_count(path: Path, pattern: re.Pattern) -> List[int]:
    """Return all integer captures of `pattern` in the file.

    Each pattern must have exactly one capturing group that captures the
    integer.
    """
    if not path.exists():
        return []
    body = path.read_text(encoding="utf-8", errors="ignore")
    return [int(m.group(1)) for m in pattern.finditer(body)]


_README_SKILL_CLAIMS = re.compile(
    r"\b(\d{2,4})\s+(?:CRE\s+skills|skills,|skill\b|institutional-grade\s+commercial\s+real\s+estate\s+skills|institutional-grade\s+CRE\s+skills|commercial\s+real\s+estate\s+skills)",
)

_README_EXACT_NUMBERED_BOLD = re.compile(r"\*\*(\d{2,4})\*\*")


def test_readme_prose_skill_count_matches_catalog() -> None:
    actual = _actual_skill_count()
    readme = _REPO_ROOT / "README.md"
    claims = _scan_text_for_count(readme, _README_SKILL_CLAIMS)
    assert claims, "README.md has no skill-count claim to verify"
    drift = sorted({c for c in claims if c != actual})
    assert not drift, (
        f"README.md contains skill-count claim(s) {drift} that disagree with "
        f"catalog ({actual}). Fix the prose to match the catalog or regenerate "
        f"docs via scripts/catalog-generate.py."
    )


def test_build_artifact_hook_prompts_match_catalog() -> None:
    """Every build-artifact hook prompt that cites a skill count must match."""
    actual = _actual_skill_count()
    pattern = re.compile(r"with\s+(\d{2,4})\s+CRE\s+skills")
    build_hooks = list(_REPO_ROOT.glob("builds/**/hooks/hooks.json"))
    assert build_hooks, "expected at least one build-artifact hook prompt"
    drifted: List[str] = []
    for hook_path in build_hooks:
        for claimed in _scan_text_for_count(hook_path, pattern):
            if claimed != actual:
                drifted.append(
                    f"  {hook_path.relative_to(_REPO_ROOT)}: claims {claimed}, catalog is {actual}"
                )
    assert not drifted, (
        "Build-artifact hook prompts have stale skill counts. Regenerate via "
        "scripts/catalog-build.py + scripts/catalog-generate.py.\n"
        + "\n".join(drifted)
    )


def test_catalog_has_expected_type_distribution() -> None:
    """Catalog must contain the headline entry types (sanity check).

    If any of these drops to zero, something in the catalog generator broke.
    """
    counts = _count_entries_by_type()
    for required_type in ("skill", "agent", "command"):
        assert counts.get(required_type, 0) > 0, (
            f"catalog has zero entries of type {required_type!r}; "
            "the catalog generator is likely broken"
        )


def test_readme_release_maturity_section_exists() -> None:
    readme = (_REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Release Maturity" in readme, (
        "README.md must include a '## Release Maturity' section. Users need "
        "to see surface-by-surface maturity before using the plugin."
    )
    assert "## Known Limitations" in readme, (
        "README.md must include a '## Known Limitations' section that lists "
        "scaffolding routes, tailoring gaps, and install caveats."
    )
