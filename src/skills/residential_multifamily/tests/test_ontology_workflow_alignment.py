"""Ontology <-> workflow alignment.

Every `required_normalized_objects` entry in
`reference/connectors/_core/workflow_activation_map.yaml` must be defined
somewhere in `_core/ontology.md`. Previously the deal-pipeline objects
(`Deal`, `Asset`, `DealMilestone`, `DealKeyDate`) were referenced by pipeline
workflows but had no ontology entry, leaving a data-contract gap.

The test is defensive: it checks that every required object name appears as
an `## H2` or `### H3` section in ontology.md. This is mechanical and will
catch any new workflow that introduces an undefined object.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Set

import yaml

from conftest import SUBSYS


def _required_objects_from_activation_map() -> Set[str]:
    path = (
        SUBSYS
        / "reference"
        / "connectors"
        / "_core"
        / "workflow_activation_map.yaml"
    )
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    required: Set[str] = set()
    for spec in (data.get("workflows") or {}).values():
        for obj in spec.get("required_normalized_objects") or []:
            required.add(str(obj))
    return required


def _defined_objects_from_ontology() -> Set[str]:
    """Extract every object name defined in ontology.md.

    Object names appear as `## Foo` (primary type) or `## Foo / Bar / Baz`
    (grouped types) or `### Foo` (subsections within a group).
    """
    path = SUBSYS / "_core" / "ontology.md"
    body = path.read_text(encoding="utf-8")
    defined: Set[str] = set()
    for m in re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE):
        heading = m.group(1).strip()
        # Group headings like "A / B / C"
        for name in re.split(r"\s*/\s*", heading):
            if re.match(r"^[A-Z][A-Za-z0-9_]*$", name):
                defined.add(name)
    for m in re.finditer(r"^###\s+(.+?)\s*$", body, re.MULTILINE):
        heading = m.group(1).strip()
        for name in re.split(r"\s*/\s*", heading):
            if re.match(r"^[A-Z][A-Za-z0-9_]*$", name):
                defined.add(name)
    return defined


def test_every_required_object_is_defined_in_ontology() -> None:
    required = _required_objects_from_activation_map()
    defined = _defined_objects_from_ontology()
    missing = sorted(required - defined)
    assert not missing, (
        "Workflow activation map references object(s) not defined in "
        f"_core/ontology.md: {missing}. Add an ## H2 or ### H3 section for "
        "each — or remove the reference if the object is not canonical."
    )


def test_ontology_defines_deal_pipeline_objects() -> None:
    """Regression guard: the four pipeline objects must remain defined.

    These were added in the 2026-04 hardening pass after an audit found them
    referenced by pipeline workflows with no ontology entry. Do not remove
    their sections without a change-log entry and an explicit decision to
    gate the pipeline workflows.
    """
    defined = _defined_objects_from_ontology()
    for required in ("Deal", "Asset", "DealMilestone", "DealKeyDate"):
        assert required in defined, (
            f"{required!r} must remain defined in _core/ontology.md. "
            "Pipeline workflows depend on it; removing it without gating "
            "those workflows silently breaks the data contract."
        )
