"""Skill manifest validation.

For every roles/*/SKILL.md and workflows/*/SKILL.md:
- Parses the YAML frontmatter.
- Validates frontmatter against the skill_manifest schema.
- Asserts every slug in `metrics_used` is a canonical slug in _core/metrics.md.
"""
from __future__ import annotations

from typing import List, Set

from conftest import (
    SUBSYS,
    extract_yaml_blocks_lenient,
    iter_role_pack_skill_paths,
    iter_workflow_pack_skill_paths,
    split_frontmatter,
    validate_against_schema,
)


def _canonical_metric_slugs() -> Set[str]:
    text = (SUBSYS / "_core" / "metrics.md").read_text(encoding="utf-8")
    blocks, _errors = extract_yaml_blocks_lenient(text)
    return {b.get("slug") for b in blocks if b.get("slug")}


def _all_skill_paths() -> List:
    return list(iter_role_pack_skill_paths()) + list(iter_workflow_pack_skill_paths())


def test_at_least_one_role_pack():
    roles = list(iter_role_pack_skill_paths())
    assert roles, "no role pack SKILL.md files found"


def test_every_skill_has_frontmatter_and_validates(skill_manifest_schema):
    errors: List[str] = []
    for sk in _all_skill_paths():
        text = sk.read_text(encoding="utf-8")
        try:
            fm, _ = split_frontmatter(text)
        except AssertionError as exc:
            errors.append(f"{sk.relative_to(SUBSYS)}: {exc}")
            continue
        block_errors = validate_against_schema(
            fm, skill_manifest_schema, path=f"{sk.relative_to(SUBSYS)}"
        )
        errors.extend(block_errors)
    assert not errors, "skill manifest validation failed:\n" + "\n".join(errors)


def test_metrics_used_are_canonical():
    canonical = _canonical_metric_slugs()
    assert canonical, "no canonical metrics discovered"
    errors: List[str] = []
    for sk in _all_skill_paths():
        text = sk.read_text(encoding="utf-8")
        try:
            fm, _ = split_frontmatter(text)
        except AssertionError:
            continue
        used = fm.get("metrics_used") or []
        for slug in used:
            if slug not in canonical:
                errors.append(
                    f"{sk.relative_to(SUBSYS)}: metrics_used entry {slug!r} "
                    f"is not a canonical metric slug"
                )
    assert not errors, "\n".join(errors)


def test_slug_uniqueness_across_packs():
    seen: dict = {}
    errors: List[str] = []
    for sk in _all_skill_paths():
        text = sk.read_text(encoding="utf-8")
        try:
            fm, _ = split_frontmatter(text)
        except AssertionError:
            continue
        slug = fm.get("slug")
        if not slug:
            errors.append(f"{sk.relative_to(SUBSYS)}: frontmatter missing slug")
            continue
        if slug in seen:
            errors.append(
                f"pack slug collision: {slug!r} in {sk.relative_to(SUBSYS)} "
                f"and {seen[slug].relative_to(SUBSYS)}"
            )
        seen[slug] = sk
    assert not errors, "\n".join(errors)
