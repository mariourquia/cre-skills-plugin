"""Alias registry validity.

- Every metric alias must map to a canonical slug that exists in _core/metrics.md.
- Every object alias must map to a canonical object that appears as an ontology section heading
  in _core/ontology.md.
- The registry itself must parse as YAML with the expected top-level keys.
"""
from __future__ import annotations

import re
from typing import List, Set

import yaml

from conftest import SUBSYS, extract_yaml_blocks_lenient


def _load_alias_registry() -> dict:
    path = SUBSYS / "_core" / "alias_registry.yaml"
    assert path.exists(), f"missing {path}"
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), "alias registry must be a mapping"
    return data


def _canonical_metric_slugs() -> Set[str]:
    """Collect every slug found in a parseable fenced yaml block in metrics.md.

    Uses the lenient extractor so that an unrelated malformed block in metrics.md
    does not cascade into a failure for alias-registry tests.
    """
    metrics_path = SUBSYS / "_core" / "metrics.md"
    text = metrics_path.read_text(encoding="utf-8")
    slugs: Set[str] = set()
    blocks, _errors = extract_yaml_blocks_lenient(text)
    for block in blocks:
        slug = block.get("slug")
        if slug:
            slugs.add(slug)
    return slugs


_OBJ_HEADING_RE = re.compile(r"^##\s+(?P<names>.+?)\s*$", re.MULTILINE)


def _canonical_ontology_objects() -> Set[str]:
    ontology_path = SUBSYS / "_core" / "ontology.md"
    assert ontology_path.exists(), f"missing {ontology_path}"
    text = ontology_path.read_text(encoding="utf-8")
    objects: Set[str] = set()
    for m in _OBJ_HEADING_RE.finditer(text):
        heading = m.group("names").strip()
        # Headings like "## Charge / Payment" or "## DevelopmentProject / ConstructionProject"
        # enumerate multiple canonical objects on one line.
        for part in heading.split("/"):
            name = part.strip()
            # Ignore generic end-note style headings.
            if not name or name.lower().startswith("null handling"):
                continue
            objects.add(name)
    return objects


def test_registry_structure():
    reg = _load_alias_registry()
    assert "metric_aliases" in reg, "alias registry missing metric_aliases"
    assert "object_aliases" in reg, "alias registry missing object_aliases"


def test_every_metric_alias_entry_points_at_existing_metric():
    reg = _load_alias_registry()
    canonical = _canonical_metric_slugs()
    errors: List[str] = []
    for key, entry in (reg.get("metric_aliases") or {}).items():
        canonical_slug = entry.get("canonical_slug")
        if not canonical_slug:
            errors.append(f"metric_aliases entry {key!r} has no canonical_slug")
            continue
        if canonical_slug not in canonical:
            errors.append(
                f"metric_aliases entry {key!r} points to canonical_slug {canonical_slug!r} "
                f"which is not in _core/metrics.md"
            )
    assert not errors, "\n".join(errors)


def test_every_object_alias_entry_points_at_existing_object():
    reg = _load_alias_registry()
    canonical_objs = _canonical_ontology_objects()
    errors: List[str] = []
    for key, entry in (reg.get("object_aliases") or {}).items():
        canonical_obj = entry.get("canonical_object")
        if not canonical_obj:
            errors.append(f"object_aliases entry {key!r} has no canonical_object")
            continue
        if canonical_obj not in canonical_objs:
            errors.append(
                f"object_aliases entry {key!r} points to canonical_object {canonical_obj!r} "
                f"which is not an ontology heading in _core/ontology.md"
            )
    assert not errors, "\n".join(errors)


def test_reserved_slots_do_not_collide_with_canonical():
    reg = _load_alias_registry()
    reserved = reg.get("reserved_slots") or {}
    canonical_metrics = _canonical_metric_slugs()
    canonical_objs = _canonical_ontology_objects()
    collisions: List[str] = []
    for slug in reserved.get("metrics", []) or []:
        if slug in canonical_metrics:
            collisions.append(f"reserved metric slot {slug!r} already exists as a canonical metric")
    for name in reserved.get("objects", []) or []:
        if name in canonical_objs:
            collisions.append(f"reserved object slot {name!r} already exists as a canonical object")
    assert not collisions, "\n".join(collisions)
