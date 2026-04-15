"""Fair-housing banner enforcement on resident-facing templates.

- For every .md file under templates/resident_comms/:
    - If the filename contains any of {renewal_offer, delinquency, lease_violation,
      non_renewal, pay_or_quit, entry_notice}, frontmatter.legal_review_required
      must be true AND the body must contain a 'LEGAL REVIEW REQUIRED BEFORE SEND'
      banner.
    - Every resident-comms template body is scanned for a small list of forbidden
      phrases drawn from HUD fair-housing marketing guidance. Any hit fails the
      test with the specific phrase and file.

This is intentionally a small, explicit allow-list, not an attempt to mechanize
every form of discriminatory language. Operators must still run a human fair-
housing review before any resident-facing send.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator, List

from conftest import SUBSYS, split_frontmatter


_LEGAL_REVIEW_FILENAME_TRIGGERS = (
    "renewal_offer",
    "delinquency",
    "lease_violation",
    "non_renewal",
    "pay_or_quit",
    "entry_notice",
)


_BANNER_RE = re.compile(
    r"LEGAL\s+REVIEW\s+REQUIRED\s+BEFORE\s+SEND", re.IGNORECASE
)


# Explicit, small list of phrases that HUD marketing guidance has flagged as
# preference-signaling. Literal matches (case-insensitive). This is intentionally
# short and explicit. Operators must still run human fair-housing review.
# Rationale citations are provided for each.
_FORBIDDEN_PHRASES: List[tuple] = [
    # HUD marketing guidance: preference by familial status.
    ("families with children", "HUD guidance: preference by familial status"),
    ("no children", "HUD guidance: exclusion by familial status"),
    ("adult community", "HUD guidance: age-based preference outside lawful senior housing"),
    # HUD marketing guidance: preference by age/status.
    ("perfect for young professionals", "HUD guidance: age/familial preference signaling"),
    ("ideal for seniors", "HUD guidance: age preference outside lawful senior housing"),
    # HUD marketing guidance: preference by religion.
    ("christian community", "HUD guidance: preference by religion"),
    ("muslim community", "HUD guidance: preference by religion"),
    ("jewish community", "HUD guidance: preference by religion"),
    # HUD marketing guidance: preference by national origin / race.
    ("latino community", "HUD guidance: preference by national origin"),
    ("white neighborhood", "HUD guidance: preference by race"),
    # Steering language.
    ("you'd feel more comfortable in", "HUD guidance: steering language"),
]


def _iter_resident_comm_templates() -> Iterator[Path]:
    d = SUBSYS / "templates" / "resident_comms"
    if not d.exists():
        return
    for md in sorted(d.glob("*.md")):
        if md.name == "README.md":
            continue
        yield md


def test_at_least_one_resident_comm_template_present():
    assert list(_iter_resident_comm_templates()), (
        "no templates/resident_comms/*.md files found"
    )


def test_legal_review_required_flag_on_statutory_templates():
    errors: List[str] = []
    for tpl in _iter_resident_comm_templates():
        text = tpl.read_text(encoding="utf-8")
        try:
            fm, body = split_frontmatter(text)
        except AssertionError as exc:
            errors.append(f"{tpl.relative_to(SUBSYS)}: {exc}")
            continue
        stem = tpl.stem.lower()
        must_flag = any(trigger in stem for trigger in _LEGAL_REVIEW_FILENAME_TRIGGERS)
        lrr = fm.get("legal_review_required")
        if must_flag and lrr is not True:
            errors.append(
                f"{tpl.relative_to(SUBSYS)}: filename suggests statutory notice "
                f"(contains one of {_LEGAL_REVIEW_FILENAME_TRIGGERS}) but "
                f"legal_review_required is not true (got {lrr!r})"
            )
        if must_flag and not _BANNER_RE.search(body):
            errors.append(
                f"{tpl.relative_to(SUBSYS)}: missing 'LEGAL REVIEW REQUIRED BEFORE SEND' "
                f"banner in body"
            )
    assert not errors, "\n".join(errors)


def test_no_forbidden_marketing_phrases():
    failures: List[str] = []
    for tpl in _iter_resident_comm_templates():
        text = tpl.read_text(encoding="utf-8")
        lower = text.lower()
        for phrase, rationale in _FORBIDDEN_PHRASES:
            if phrase in lower:
                failures.append(
                    f"{tpl.relative_to(SUBSYS)}: forbidden phrase "
                    f"{phrase!r} ({rationale})"
                )
    assert not failures, "\n".join(failures)


def test_legal_review_flagged_templates_have_review_footer():
    """Templates with legal_review_required=true should also include a checklist
    of review dimensions (jurisdiction, notice period, delivery method, etc.)
    in a footer. This is a soft structural check: we look for the string
    'LEGAL REVIEW CHECKPOINTS' in the body."""
    failures: List[str] = []
    for tpl in _iter_resident_comm_templates():
        text = tpl.read_text(encoding="utf-8")
        try:
            fm, body = split_frontmatter(text)
        except AssertionError:
            continue
        if fm.get("legal_review_required") is True:
            if "LEGAL REVIEW CHECKPOINTS" not in body:
                failures.append(
                    f"{tpl.relative_to(SUBSYS)}: legal_review_required=true but body "
                    f"lacks a 'LEGAL REVIEW CHECKPOINTS' footer"
                )
    assert not failures, "\n".join(failures)
