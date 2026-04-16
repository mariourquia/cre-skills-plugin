"""Preview-mode enforcement for beta_rc / experimental skills.

Per `docs/PREVIEW_MODE.md`, every SKILL.md with `status: beta_rc` or
`status: experimental` MUST carry a `## Release maturity` section whose body
contains the expected markers so operators know the skill is preview and
cannot route its output to a final-marked terminal without acknowledgement.

This test scans the subsystem's SKILL.md tree and fails if any preview-status
skill is missing the section or its required markers.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

from conftest import SUBSYS


_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)
_PREVIEW_STATUSES = {"beta_rc", "experimental"}
_SECTION_HEADER = "## Release maturity"
_REQUIRED_MARKERS = (
    "**Status:**",
    "**Preview mode:**",
    "**What to verify before trusting the output:**",
)


def _is_preview_skill(frontmatter: str) -> bool:
    m = _STATUS_RE.search(frontmatter)
    return bool(m and m.group(1).lower().strip().strip('"\'') in _PREVIEW_STATUSES)


def _split_frontmatter(body: str) -> Tuple[str, str]:
    """Return (frontmatter, body_rest). If no frontmatter, ("", body)."""
    if not body.startswith("---\n"):
        return "", body
    try:
        end = body.index("\n---\n", 4)
    except ValueError:
        return "", body
    return body[4:end], body[end + 5 :]


def _iter_skill_files() -> List[Path]:
    """Every SKILL.md under the residential_multifamily tree."""
    return sorted(SUBSYS.rglob("SKILL.md"))


def test_preview_skills_have_release_maturity_section() -> None:
    failures: List[str] = []
    skill_files = _iter_skill_files()
    preview_count = 0
    for skill in skill_files:
        text = skill.read_text(encoding="utf-8")
        front, body = _split_frontmatter(text)
        if not _is_preview_skill(front):
            continue
        preview_count += 1
        if _SECTION_HEADER not in body:
            rel = skill.relative_to(SUBSYS)
            failures.append(
                f"{rel}: missing '{_SECTION_HEADER}' section (preview skill requires it)"
            )
            continue
        section_idx = body.index(_SECTION_HEADER)
        next_header_idx = body.find("\n## ", section_idx + 1)
        section = body[section_idx : next_header_idx if next_header_idx != -1 else None]
        missing = [m for m in _REQUIRED_MARKERS if m not in section]
        if missing:
            rel = skill.relative_to(SUBSYS)
            failures.append(
                f"{rel}: Release maturity section missing markers {missing}"
            )
    assert preview_count > 0, (
        "No preview-status (beta_rc / experimental) skills found. If every "
        "skill has graduated to stable, this test can be removed; otherwise "
        "verify the scanner picks up frontmatter correctly."
    )
    assert not failures, (
        "Preview-mode markers missing. See docs/PREVIEW_MODE.md.\n  "
        + "\n  ".join(failures)
    )


def test_preview_mode_doc_exists() -> None:
    doc = SUBSYS.parent.parent.parent / "docs" / "PREVIEW_MODE.md"
    assert doc.exists(), "docs/PREVIEW_MODE.md is referenced by this test and must exist"
    body = doc.read_text(encoding="utf-8")
    for rule_marker in ("Preview mode", "output stamp", "final-marked gate"):
        assert rule_marker.lower() in body.lower(), (
            f"docs/PREVIEW_MODE.md missing expected marker {rule_marker!r}"
        )
