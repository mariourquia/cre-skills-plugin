"""Preview-mode enforcement for beta_rc / experimental / stable_pending_shakedown skills.

Per ``docs/PREVIEW_MODE.md``, every SKILL.md whose frontmatter ``status``
lands in the preview-status set MUST carry a ``## Release maturity`` section
whose body contains the expected markers plus the status-appropriate
Preview-mode banner.

Three preview sub-statuses are admitted:

- ``experimental`` — scaffolded; output is not trustworthy. Banner: PREVIEW / STAGING stamp.
- ``beta_rc`` — pre-operator RC. Banner: PREVIEW / STAGING stamp.
- ``stable_pending_shakedown`` — code complete, refusal contracts active,
  awaiting first operator shakedown log. Banner: ``Stable, awaiting
  shakedown``. Must NOT trigger the final-marked refusal layer — the
  existing refusal-on-missing-input contracts are load-bearing, not this
  preview-mode gate. (This file does not *enforce* final-marked refusal
  behavior; it enforces the banner contract. The gate tests below assert
  no ``PREVIEW / STAGING`` stamp language leaks into a ``shakedown``-mode
  skill, which is how a silent layering-on of a second refusal would
  manifest.)

This subsystem-scoped test walks the ``residential_multifamily`` tree. A
repo-wide counterpart lives at ``tests/test_preview_mode_gate.py``.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

from conftest import SUBSYS


_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)
_PREVIEW_STATUSES = {"beta_rc", "experimental", "stable_pending_shakedown"}
_STAMP_STATUSES = {"beta_rc", "experimental"}
_SHAKEDOWN_STATUSES = {"stable_pending_shakedown"}
_SECTION_HEADER = "## Release maturity"
_REQUIRED_MARKERS = (
    "**Status:**",
    "**Preview mode:**",
    "**What to verify before trusting the output:**",
)
_STAMP_BANNER_TOKENS = ("PREVIEW / STAGING", "without human acknowledgement")
_SHAKEDOWN_BANNER_TOKENS = (
    "Stable, awaiting shakedown",
    "Refusal-on-missing-input contracts are active",
)


def _status_of(frontmatter: str) -> str | None:
    m = _STATUS_RE.search(frontmatter)
    if not m:
        return None
    return m.group(1).lower().strip().strip('"\'')


def _is_preview_skill(frontmatter: str) -> bool:
    st = _status_of(frontmatter)
    return bool(st and st in _PREVIEW_STATUSES)


def _split_frontmatter(body: str) -> Tuple[str, str]:
    if not body.startswith("---\n"):
        return "", body
    try:
        end = body.index("\n---\n", 4)
    except ValueError:
        return "", body
    return body[4:end], body[end + 5 :]


def _iter_skill_files() -> List[Path]:
    return sorted(SUBSYS.rglob("SKILL.md"))


def _release_maturity_section(body: str) -> str | None:
    if _SECTION_HEADER not in body:
        return None
    section_idx = body.index(_SECTION_HEADER)
    next_header_idx = body.find("\n## ", section_idx + 1)
    return body[section_idx : next_header_idx if next_header_idx != -1 else None]


def test_preview_skills_have_release_maturity_section() -> None:
    failures: List[str] = []
    preview_count = 0
    for skill in _iter_skill_files():
        text = skill.read_text(encoding="utf-8")
        front, body = _split_frontmatter(text)
        if not _is_preview_skill(front):
            continue
        preview_count += 1
        section = _release_maturity_section(body)
        rel = skill.relative_to(SUBSYS)
        if section is None:
            failures.append(
                f"{rel}: missing '{_SECTION_HEADER}' section (preview skill requires it)"
            )
            continue
        missing = [m for m in _REQUIRED_MARKERS if m not in section]
        if missing:
            failures.append(f"{rel}: Release maturity section missing markers {missing}")
    assert preview_count > 0, (
        "No preview-status skills found. If every skill has graduated to "
        "stable, this test can be removed; otherwise verify the scanner picks "
        "up frontmatter correctly."
    )
    assert not failures, (
        "Preview-mode markers missing. See docs/PREVIEW_MODE.md.\n  "
        + "\n  ".join(failures)
    )


def test_preview_banner_matches_status() -> None:
    """Each preview-status skill carries the banner text for its sub-status.

    - beta_rc / experimental → PREVIEW / STAGING stamp language.
    - stable_pending_shakedown → 'Stable, awaiting shakedown' + explicit
      acknowledgement that refusal contracts are already active. A
      stable_pending_shakedown skill that still carries the PREVIEW / STAGING
      stamp language is a silent regression (would layer a second refusal
      on top of the existing contract machinery).
    """
    failures: List[str] = []
    for skill in _iter_skill_files():
        text = skill.read_text(encoding="utf-8")
        front, body = _split_frontmatter(text)
        status = _status_of(front)
        if status not in _PREVIEW_STATUSES:
            continue
        section = _release_maturity_section(body)
        rel = skill.relative_to(SUBSYS)
        if section is None:
            continue  # covered by the other test
        if status in _STAMP_STATUSES:
            for token in _STAMP_BANNER_TOKENS:
                if token not in section:
                    failures.append(
                        f"{rel}: status={status!r} must carry PREVIEW/STAGING "
                        f"stamp token {token!r}"
                    )
        elif status in _SHAKEDOWN_STATUSES:
            for token in _SHAKEDOWN_BANNER_TOKENS:
                if token not in section:
                    failures.append(
                        f"{rel}: status={status!r} must carry shakedown banner "
                        f"token {token!r}"
                    )
            for stamp_token in _STAMP_BANNER_TOKENS:
                if stamp_token in section:
                    failures.append(
                        f"{rel}: status=stable_pending_shakedown must NOT "
                        f"carry PREVIEW/STAGING stamp language {stamp_token!r} "
                        f"— that would layer a second refusal on top of the "
                        f"existing contract machinery."
                    )
    assert not failures, (
        "Preview banner mismatch. See docs/PREVIEW_MODE.md.\n  "
        + "\n  ".join(failures)
    )


def test_stable_pending_shakedown_does_not_trigger_final_marked_refusal() -> None:
    """The shakedown banner must explicitly disclaim a second refusal layer.

    docs/PREVIEW_MODE.md states that stable_pending_shakedown skills rely on
    the subsystem's existing refusal contracts (sealed-close, placeholder
    scanner, executive output contract) — the preview-mode gate does NOT add
    a second layer on top. If any stable_pending_shakedown SKILL.md accidentally
    re-imports the 'not eligible for final-marked use without human
    acknowledgement' language from the beta_rc banner, this test fails and
    points at the drift.
    """
    failures: List[str] = []
    for skill in _iter_skill_files():
        text = skill.read_text(encoding="utf-8")
        front, body = _split_frontmatter(text)
        if _status_of(front) not in _SHAKEDOWN_STATUSES:
            continue
        section = _release_maturity_section(body)
        rel = skill.relative_to(SUBSYS)
        if section and "not eligible for final-marked use without human acknowledgement" in section:
            failures.append(
                f"{rel}: stable_pending_shakedown skill imports the beta_rc "
                "'not eligible for final-marked use without human "
                "acknowledgement' phrase. Shakedown status must not layer a "
                "second final-marked refusal on top of the existing contract "
                "machinery."
            )
    assert not failures, "\n  ".join(failures)


def test_preview_mode_doc_exists() -> None:
    doc = SUBSYS.parent.parent.parent / "docs" / "PREVIEW_MODE.md"
    assert doc.exists(), "docs/PREVIEW_MODE.md is referenced by this test and must exist"
    body = doc.read_text(encoding="utf-8")
    for rule_marker in (
        "Preview mode",
        "output stamp",
        "final-marked gate",
        "stable_pending_shakedown",
        "Stable, awaiting shakedown",
    ):
        assert rule_marker.lower() in body.lower(), (
            f"docs/PREVIEW_MODE.md missing expected marker {rule_marker!r}"
        )
