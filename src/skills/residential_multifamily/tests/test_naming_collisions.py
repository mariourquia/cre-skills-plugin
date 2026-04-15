"""Naming collision tests.

- No duplicate metric slugs across _core/metrics.md and any pack's metrics.md.
- No canonical object name in _core/ontology.md collides with an alias-registry entry.
- No metric slug collides with a pack slug or workflow slug (those are tracked separately
  but should be unambiguous for human reviewers).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Set

import yaml

from conftest import (
    SUBSYS,
    extract_yaml_blocks_lenient,
    iter_role_pack_skill_paths,
    iter_workflow_pack_skill_paths,
    split_frontmatter,
)


def _core_metrics_slugs() -> Dict[str, Path]:
    metrics_path = SUBSYS / "_core" / "metrics.md"
    text = metrics_path.read_text(encoding="utf-8")
    out: Dict[str, Path] = {}
    blocks, _errors = extract_yaml_blocks_lenient(text)
    for block in blocks:
        slug = block.get("slug")
        if slug:
            out[slug] = metrics_path
    return out


# Pack metrics.md files use table rows like "| `metric_slug` | ... |".
_PACK_METRIC_ROW_RE = re.compile(r"^\|\s*`([a-z_][a-z0-9_]*)`\s*\|", re.MULTILINE)


def _pack_metrics_slugs() -> List[tuple]:
    """Return list of (slug, source_path)."""
    entries: List[tuple] = []
    for pack_dir in list((SUBSYS / "roles").glob("*")) + list((SUBSYS / "workflows").glob("*")):
        if not pack_dir.is_dir():
            continue
        if pack_dir.name.startswith("_"):
            continue
        mf = pack_dir / "metrics.md"
        if not mf.exists():
            continue
        text = mf.read_text(encoding="utf-8")
        for m in _PACK_METRIC_ROW_RE.finditer(text):
            entries.append((m.group(1), mf))
    return entries


def _ontology_objects() -> Set[str]:
    ontology_path = SUBSYS / "_core" / "ontology.md"
    text = ontology_path.read_text(encoding="utf-8")
    objects: Set[str] = set()
    for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE):
        heading = m.group(1).strip()
        for part in heading.split("/"):
            name = part.strip()
            if not name or name.lower().startswith("null handling"):
                continue
            objects.add(name)
    return objects


def _alias_registry_keys() -> Set[str]:
    path = SUBSYS / "_core" / "alias_registry.yaml"
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    keys: Set[str] = set()
    for section in ("metric_aliases", "object_aliases"):
        for k in (data.get(section) or {}).keys():
            keys.add(k)
    return keys


def test_no_canonical_metric_slug_collides_with_pack_metric_slug_redefinition():
    """Pack metrics.md files *reference* canonical slugs. A pack is not allowed to
    introduce a slug that does NOT exist in _core/metrics.md."""
    canonical = set(_core_metrics_slugs().keys())
    unknown: List[str] = []
    for slug, src in _pack_metrics_slugs():
        if slug not in canonical:
            unknown.append(f"{src.relative_to(SUBSYS)}: slug {slug!r} is not in _core/metrics.md")
    assert not unknown, "\n".join(unknown)


def test_canonical_metric_slugs_unique():
    """Uniqueness check across parseable metric blocks.

    Uses the lenient extractor so this test does not cascade-fail on an unrelated
    malformed block; the metric-contracts test suite surfaces parse errors separately.
    """
    metrics_path = SUBSYS / "_core" / "metrics.md"
    text = metrics_path.read_text(encoding="utf-8")
    slugs: List[str] = []
    blocks, _errors = extract_yaml_blocks_lenient(text)
    for block in blocks:
        slug = block.get("slug")
        if slug:
            slugs.append(slug)
    duplicates = [s for s in set(slugs) if slugs.count(s) > 1]
    assert not duplicates, f"duplicate canonical metric slugs in _core/metrics.md: {duplicates}"


def test_ontology_object_names_do_not_collide_with_registered_aliases():
    objs = _ontology_objects()
    aliases = _alias_registry_keys()
    # Both name spaces are allowed to coexist in principle, but if a registered alias KEY
    # happens to literally equal a canonical object name, the registry entry is a redundant
    # self-alias only if the canonical_object/canonical_slug points back. We surface the
    # intersection for reviewer awareness.
    collisions = objs & aliases
    # For Phase 1, only fail if a collision exists where the alias key is the same as the
    # canonical object BUT the registered entry does not point back to that canonical object.
    if not collisions:
        return
    path = SUBSYS / "_core" / "alias_registry.yaml"
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    obj_entries = data.get("object_aliases") or {}
    bad: List[str] = []
    for name in collisions:
        entry = obj_entries.get(name)
        if entry is None:
            # Collision is with a metric_alias key; unusual but not fatal if unique.
            continue
        if entry.get("canonical_object") != name:
            bad.append(
                f"alias key {name!r} collides with canonical object {name!r} "
                f"but entry.canonical_object != name"
            )
    assert not bad, "\n".join(bad)


def test_pack_slugs_do_not_collide_with_canonical_metric_slugs():
    canonical = set(_core_metrics_slugs().keys())
    clashes: List[str] = []
    for sk in list(iter_role_pack_skill_paths()) + list(iter_workflow_pack_skill_paths()):
        text = sk.read_text(encoding="utf-8")
        try:
            fm, _ = split_frontmatter(text)
        except AssertionError:
            continue
        slug = fm.get("slug")
        if slug and slug in canonical:
            clashes.append(
                f"{sk.relative_to(SUBSYS)}: pack slug {slug!r} collides with canonical metric slug"
            )
    assert not clashes, "\n".join(clashes)
