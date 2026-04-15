"""Template rendering smoke tests.

For every .md file under templates/ (excluding README.md):
- Frontmatter parses as YAML.
- At least one {{placeholder}} token exists in the body (smoke test — every template
  must have fillable fields).
- Frontmatter must declare required top-level keys per templates/README.md:
    template_slug, title, applies_to, legal_review_required, jurisdiction_sensitive,
    status, references_used, produced_by.
- `status` is one of: starter | sample | placeholder | approved | illustrative.
- `template_slug` matches the file stem (basename without .md).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator, List

from conftest import SUBSYS, split_frontmatter


_PLACEHOLDER_RE = re.compile(r"\{\{\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\}\}")
_ALLOWED_STATUS = {"starter", "sample", "placeholder", "approved", "illustrative"}
_REQUIRED_FRONTMATTER_KEYS = {
    "template_slug",
    "title",
    "applies_to",
    "legal_review_required",
    "jurisdiction_sensitive",
    "status",
    "references_used",
    "produced_by",
}


def _iter_template_files() -> Iterator[Path]:
    templates_root = SUBSYS / "templates"
    assert templates_root.exists(), "templates/ directory missing"
    for md in templates_root.rglob("*.md"):
        if md.name == "README.md":
            continue
        yield md


def test_at_least_one_template_present():
    assert list(_iter_template_files()), "no templates/**/*.md files found"


def test_template_frontmatter_parses_and_is_complete():
    errors: List[str] = []
    for tpl in _iter_template_files():
        text = tpl.read_text(encoding="utf-8")
        try:
            fm, _body = split_frontmatter(text)
        except AssertionError as exc:
            errors.append(f"{tpl.relative_to(SUBSYS)}: {exc}")
            continue
        missing = _REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
        if missing:
            errors.append(f"{tpl.relative_to(SUBSYS)}: missing frontmatter keys {sorted(missing)}")
            continue
        status = fm.get("status")
        if status not in _ALLOWED_STATUS:
            errors.append(
                f"{tpl.relative_to(SUBSYS)}: status {status!r} not in {_ALLOWED_STATUS}"
            )
        slug = fm.get("template_slug")
        if slug != tpl.stem:
            errors.append(
                f"{tpl.relative_to(SUBSYS)}: template_slug {slug!r} != file stem {tpl.stem!r}"
            )
    assert not errors, "\n".join(errors)


def test_every_template_has_at_least_one_placeholder():
    offenders: List[str] = []
    for tpl in _iter_template_files():
        text = tpl.read_text(encoding="utf-8")
        try:
            _fm, body = split_frontmatter(text)
        except AssertionError:
            offenders.append(f"{tpl.relative_to(SUBSYS)}: frontmatter missing")
            continue
        if not _PLACEHOLDER_RE.search(body):
            offenders.append(
                f"{tpl.relative_to(SUBSYS)}: no {{{{placeholder}}}} tokens in body "
                f"(template should declare at least one fillable field)"
            )
    assert not offenders, "\n".join(offenders)


def test_placeholder_tokens_are_well_formed():
    """Surface malformed {{ tokens }} with extraneous characters (e.g., dots, hyphens)."""
    bad: List[str] = []
    rough_token_re = re.compile(r"\{\{([^}]*)\}\}")
    for tpl in _iter_template_files():
        text = tpl.read_text(encoding="utf-8")
        for m in rough_token_re.finditer(text):
            inner = m.group(1).strip()
            # Require snake_case-ish identifier.
            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", inner):
                bad.append(
                    f"{tpl.relative_to(SUBSYS)}: malformed placeholder token "
                    f"{{{{{inner}}}}}"
                )
    assert not bad, "\n".join(bad)
