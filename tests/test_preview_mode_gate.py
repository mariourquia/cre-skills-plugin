"""Repo-wide preview-mode enforcement.

Walks every ``src/skills/**/SKILL.md`` and asserts that preview-status skills
(``beta_rc``, ``experimental``, ``stable_pending_shakedown``) carry the
``## Release maturity`` section defined in ``docs/PREVIEW_MODE.md`` with the
banner text appropriate to their sub-status.

The residential_multifamily subsystem has its own subsystem-scoped counterpart
at ``src/skills/residential_multifamily/tests/test_preview_mode_gate.py`` with
stricter assertions; this test runs repo-wide so a new top-level preview-status
skill landing elsewhere also gets caught.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "src" / "skills"
PREVIEW_MODE_DOC = REPO_ROOT / "docs" / "PREVIEW_MODE.md"

_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)
_PREVIEW_STATUSES = frozenset({"beta_rc", "experimental", "stable_pending_shakedown"})
_STAMP_STATUSES = frozenset({"beta_rc", "experimental"})
_SHAKEDOWN_STATUSES = frozenset({"stable_pending_shakedown"})
_SECTION_HEADER = "## Release maturity"
_REQUIRED_MARKERS = (
    "**Status:**",
    "**Preview mode:**",
    "**What to verify before trusting the output:**",
)
_STAMP_BANNER_TOKEN = "PREVIEW / STAGING"
_SHAKEDOWN_BANNER_TOKEN = "Stable, awaiting shakedown"


def _split_frontmatter(body: str) -> Tuple[str, str]:
    if not body.startswith("---\n"):
        return "", body
    try:
        end = body.index("\n---\n", 4)
    except ValueError:
        return "", body
    return body[4:end], body[end + 5 :]


def _status_of(frontmatter: str) -> str | None:
    m = _STATUS_RE.search(frontmatter)
    if not m:
        return None
    return m.group(1).lower().strip().strip('"\'')


def _iter_top_level_skill_files() -> List[Path]:
    """Every SKILL.md under ``src/skills/``.

    We include subsystem SKILL.md files too (e.g., residential_multifamily),
    because a repo-wide test should not silently miss a subsystem when the
    subsystem-scoped test is disabled. Duplication with the subsystem test is
    intentional and cheap.
    """
    return sorted(SKILLS_ROOT.rglob("SKILL.md"))


def _release_maturity_section(body: str) -> str | None:
    if _SECTION_HEADER not in body:
        return None
    section_idx = body.index(_SECTION_HEADER)
    next_header_idx = body.find("\n## ", section_idx + 1)
    return body[section_idx : next_header_idx if next_header_idx != -1 else None]


def test_preview_mode_doc_defines_all_sub_statuses() -> None:
    """The canonical doc enumerates every admitted sub-status."""
    assert PREVIEW_MODE_DOC.exists(), "docs/PREVIEW_MODE.md must exist"
    body = PREVIEW_MODE_DOC.read_text(encoding="utf-8")
    for status in sorted(_PREVIEW_STATUSES):
        assert status in body, (
            f"docs/PREVIEW_MODE.md does not define sub-status {status!r}; "
            "update the doc or shrink _PREVIEW_STATUSES in this test."
        )
    # Shakedown banner + its 'no second refusal layer' semantics must be named.
    for token in (
        _SHAKEDOWN_BANNER_TOKEN,
        "awaiting shakedown",
        "refusal-on-missing-input",
    ):
        assert token.lower() in body.lower(), (
            f"docs/PREVIEW_MODE.md missing expected token {token!r}"
        )


def test_every_preview_skill_has_release_maturity_section_and_markers() -> None:
    failures: List[str] = []
    preview_count = 0
    for skill in _iter_top_level_skill_files():
        text = skill.read_text(encoding="utf-8")
        front, body = _split_frontmatter(text)
        status = _status_of(front)
        if status not in _PREVIEW_STATUSES:
            continue
        preview_count += 1
        section = _release_maturity_section(body)
        rel = skill.relative_to(REPO_ROOT)
        if section is None:
            failures.append(
                f"{rel}: status={status!r} requires '{_SECTION_HEADER}' section"
            )
            continue
        missing = [m for m in _REQUIRED_MARKERS if m not in section]
        if missing:
            failures.append(f"{rel}: Release maturity section missing markers {missing}")
    assert preview_count > 0, (
        "No preview-status skills found repo-wide. If every skill has graduated "
        "to stable, this test should be removed; otherwise verify the scanner "
        "picks up frontmatter correctly."
    )
    assert not failures, (
        "Preview-mode markers missing. See docs/PREVIEW_MODE.md.\n  "
        + "\n  ".join(failures)
    )


def test_preview_banner_matches_status_repo_wide() -> None:
    """beta_rc / experimental carry the PREVIEW / STAGING stamp; shakedown
    skills carry the 'Stable, awaiting shakedown' banner instead.

    A shakedown-status skill that still carries PREVIEW / STAGING language is
    a regression — it would layer a second refusal on top of the existing
    contract machinery, which is explicitly not the shakedown contract per
    docs/PREVIEW_MODE.md.
    """
    failures: List[str] = []
    for skill in _iter_top_level_skill_files():
        text = skill.read_text(encoding="utf-8")
        front, body = _split_frontmatter(text)
        status = _status_of(front)
        if status not in _PREVIEW_STATUSES:
            continue
        section = _release_maturity_section(body)
        rel = skill.relative_to(REPO_ROOT)
        if section is None:
            continue  # covered by the other test
        if status in _STAMP_STATUSES:
            if _STAMP_BANNER_TOKEN not in section:
                failures.append(
                    f"{rel}: status={status!r} must carry banner token "
                    f"{_STAMP_BANNER_TOKEN!r}"
                )
        elif status in _SHAKEDOWN_STATUSES:
            if _SHAKEDOWN_BANNER_TOKEN not in section:
                failures.append(
                    f"{rel}: status={status!r} must carry banner token "
                    f"{_SHAKEDOWN_BANNER_TOKEN!r}"
                )
            if _STAMP_BANNER_TOKEN in section:
                failures.append(
                    f"{rel}: status=stable_pending_shakedown must NOT carry "
                    f"{_STAMP_BANNER_TOKEN!r} (shakedown does not layer a "
                    "second refusal on top of the existing contracts)."
                )
    assert not failures, (
        "Preview banner mismatch. See docs/PREVIEW_MODE.md.\n  "
        + "\n  ".join(failures)
    )
