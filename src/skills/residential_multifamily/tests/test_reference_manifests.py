"""Reference manifest validation.

For every pack's reference_manifest.yaml:
- Shape validates against reference_manifest schema.
- Every `reads[].path` either:
    (a) contains a template placeholder token like {market}, {region}, {submarket},
        or {org_id}, in which case existence is NOT required for now (live references
        will be authored at tailoring time), OR
    (b) is concrete (no placeholder), in which case the file must exist on disk.
- `writes[]` entries are checked only for shape.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

import yaml

from conftest import (
    SUBSYS,
    iter_pack_reference_manifests,
    validate_against_schema,
)


_PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def _has_placeholder(path_str: str) -> bool:
    return bool(_PLACEHOLDER_RE.search(path_str))


def _load_manifest(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{p} did not parse to a mapping"
    return data


def test_at_least_one_reference_manifest():
    manifests = list(iter_pack_reference_manifests())
    assert manifests, "no pack reference_manifest.yaml files found"


def test_every_manifest_validates_against_schema(reference_manifest_schema):
    errors: List[str] = []
    for rm in iter_pack_reference_manifests():
        data = _load_manifest(rm)
        err = validate_against_schema(
            data, reference_manifest_schema, path=str(rm.relative_to(SUBSYS))
        )
        errors.extend(err)
    assert not errors, "\n".join(errors)


def test_every_read_path_exists_or_is_templated():
    errors: List[str] = []
    for rm in iter_pack_reference_manifests():
        data = _load_manifest(rm)
        for read_entry in data.get("reads") or []:
            path_str = read_entry.get("path")
            if not path_str:
                errors.append(f"{rm.relative_to(SUBSYS)}: reads entry missing path")
                continue
            if _has_placeholder(path_str):
                # Templated; existence not required for Phase 1.
                continue
            candidate = SUBSYS / path_str
            if not candidate.exists():
                errors.append(
                    f"{rm.relative_to(SUBSYS)}: read path {path_str!r} does not exist "
                    f"and contains no template placeholder"
                )
    assert not errors, "\n".join(errors)


def test_every_write_path_is_well_formed():
    errors: List[str] = []
    for rm in iter_pack_reference_manifests():
        data = _load_manifest(rm)
        for write_entry in data.get("writes") or []:
            if not write_entry.get("path"):
                errors.append(f"{rm.relative_to(SUBSYS)}: writes entry missing path")
            if not write_entry.get("category"):
                errors.append(f"{rm.relative_to(SUBSYS)}: writes entry missing category")
    assert not errors, "\n".join(errors)


def test_manifest_pack_slug_matches_folder():
    errors: List[str] = []
    for rm in iter_pack_reference_manifests():
        data = _load_manifest(rm)
        declared = data.get("pack_slug")
        folder = rm.parent.name
        if declared != folder:
            errors.append(
                f"{rm.relative_to(SUBSYS)}: pack_slug {declared!r} != folder {folder!r}"
            )
    assert not errors, "\n".join(errors)
