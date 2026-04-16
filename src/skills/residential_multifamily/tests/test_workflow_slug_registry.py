"""Workflow slug registry integrity.

Fails if any reference to a workflow uses a slug that is not a canonical
workflow directory name and is not listed in the alias registry as an explicit
alias.

Sources scanned:
  - _core/routing/rules.yaml (workflow_hint, workflow_pack, workflow enum branches)
  - _core/alias_registry.yaml (workflow_aliases section, optional)
  - reference/connectors/_core/workflow_activation_map.yaml (top-level keys)
  - SKILL.md, README.md (prose mentions of `workflows/<slug>`)

The canonical set of slugs is the set of immediate subdirectories of
`workflows/` that contain a SKILL.md (i.e. runnable workflows), plus any slugs
explicitly declared as `phase1_scaffolding: true` in alias_registry.yaml
(regulatory placeholders).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

import yaml

from conftest import SUBSYS


def _canonical_workflow_slugs() -> Set[str]:
    wf_dir = SUBSYS / "workflows"
    slugs: Set[str] = set()
    for child in sorted(wf_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("_"):
            continue
        if (child / "SKILL.md").exists():
            slugs.add(child.name)
    return slugs


def _scaffolding_slugs_from_alias_registry() -> Set[str]:
    alias_path = SUBSYS / "_core" / "alias_registry.yaml"
    if not alias_path.exists():
        return set()
    with alias_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    scaff = data.get("workflow_scaffolding_slugs") or []
    return set(scaff)


def _registered_alias_map() -> Dict[str, str]:
    alias_path = SUBSYS / "_core" / "alias_registry.yaml"
    if not alias_path.exists():
        return {}
    with alias_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    aliases = data.get("workflow_aliases") or {}
    # aliases: { alias_name: canonical_slug }
    if not isinstance(aliases, dict):
        return {}
    return {str(k): str(v) for k, v in aliases.items()}


_WF_PATH_RE = re.compile(r"workflows/([a-z][a-z0-9_]*)")


def _scan_yaml_file_for_slugs(path: Path) -> List[Tuple[str, int]]:
    """Return (slug, line_number) pairs for every `workflows/<slug>` reference."""
    out: List[Tuple[str, int]] = []
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            for m in _WF_PATH_RE.finditer(line):
                out.append((m.group(1), lineno))
    return out


def _scan_activation_map_keys() -> List[Tuple[str, int]]:
    """Top-level workflow keys in workflow_activation_map.yaml."""
    path = (
        SUBSYS
        / "reference"
        / "connectors"
        / "_core"
        / "workflow_activation_map.yaml"
    )
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    workflows = data.get("workflows") or {}
    # We don't have line numbers from yaml.safe_load; return 0 as a stand-in.
    return [(str(k), 0) for k in workflows.keys()]


def _scan_routing_rules_explicit_enums() -> List[Tuple[str, int]]:
    """Pick up workflow names listed in any_of under `conditions.workflow`.

    These are not written as `workflows/<slug>` in the YAML so the regex scanner
    misses them. We parse the YAML structure instead.
    """
    path = SUBSYS / "_core" / "routing" / "rules.yaml"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    out: List[Tuple[str, int]] = []
    for rule in data.get("rules") or []:
        cond = rule.get("conditions") or {}
        wf = cond.get("workflow")
        if isinstance(wf, dict):
            vals = wf.get("any_of") or []
            for v in vals:
                out.append((str(v), 0))
        elif isinstance(wf, str):
            out.append((wf, 0))
    return out


def _all_references() -> Dict[str, List[Tuple[str, int]]]:
    """Returns {slug: [(source_path, lineno), ...]}.

    Collects from: rules.yaml, activation_map.yaml, SKILL.md, README.md.
    """
    refs: Dict[str, List[Tuple[str, int]]] = {}

    def _record(slug: str, source: str, lineno: int) -> None:
        refs.setdefault(slug, []).append((source, lineno))

    rules = SUBSYS / "_core" / "routing" / "rules.yaml"
    for slug, lineno in _scan_yaml_file_for_slugs(rules):
        _record(slug, str(rules.relative_to(SUBSYS)), lineno)
    for slug, lineno in _scan_routing_rules_explicit_enums():
        _record(slug, str(rules.relative_to(SUBSYS)), lineno)

    activation_map = (
        SUBSYS
        / "reference"
        / "connectors"
        / "_core"
        / "workflow_activation_map.yaml"
    )
    for slug, lineno in _scan_activation_map_keys():
        _record(slug, str(activation_map.relative_to(SUBSYS)), lineno)

    skill_md = SUBSYS / "SKILL.md"
    for slug, lineno in _scan_yaml_file_for_slugs(skill_md):
        _record(slug, str(skill_md.relative_to(SUBSYS)), lineno)

    readme = SUBSYS / "README.md"
    for slug, lineno in _scan_yaml_file_for_slugs(readme):
        _record(slug, str(readme.relative_to(SUBSYS)), lineno)

    # also scan tailoring routing / workflows docs
    tailoring_routing = SUBSYS / "tailoring" / "routing.yaml"
    for slug, lineno in _scan_yaml_file_for_slugs(tailoring_routing):
        _record(slug, str(tailoring_routing.relative_to(SUBSYS)), lineno)

    return refs


def test_every_workflow_reference_resolves() -> None:
    canonical = _canonical_workflow_slugs()
    scaffolding = _scaffolding_slugs_from_alias_registry()
    aliases = _registered_alias_map()

    references = _all_references()

    dead: List[str] = []
    for slug, sources in sorted(references.items()):
        if slug in canonical:
            continue
        if slug in scaffolding:
            continue
        if slug in aliases:
            target = aliases[slug]
            if target in canonical or target in scaffolding:
                continue
            dead.append(
                f"  {slug!r} -> alias target {target!r} not canonical; seen at {sources}"
            )
            continue
        dead.append(f"  {slug!r} seen at {sources}")

    assert not dead, (
        "Dead workflow slug references detected. Fix the slug, register an "
        "alias in _core/alias_registry.yaml#workflow_aliases, or mark the "
        "slug as scaffolding (_core/alias_registry.yaml#workflow_scaffolding_slugs).\n"
        + "\n".join(dead)
    )


def test_no_orphan_canonical_workflows() -> None:
    """Every canonical workflow directory must appear in workflow_activation_map.yaml.

    This catches the inverse drift: a workflow directory exists on disk but is
    not registered in the activation map, so the orchestrator cannot activate
    it deterministically.
    """
    canonical = _canonical_workflow_slugs()
    activation_map = (
        SUBSYS
        / "reference"
        / "connectors"
        / "_core"
        / "workflow_activation_map.yaml"
    )
    with activation_map.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    registered = set((data.get("workflows") or {}).keys())

    missing = sorted(canonical - registered)
    assert not missing, (
        f"Workflows present on disk but absent from workflow_activation_map.yaml: {missing}"
    )


def test_workflow_aliases_are_explicit() -> None:
    """If alias_registry.yaml declares workflow_aliases, each must resolve to a
    canonical slug and must not collide with a canonical slug.

    This prevents silent alias rot (an alias that still exists as an alias but
    also as a canonical folder creates confusion about which is authoritative).
    """
    aliases = _registered_alias_map()
    if not aliases:
        return
    canonical = _canonical_workflow_slugs()

    errors: List[str] = []
    for alias, target in sorted(aliases.items()):
        if alias in canonical:
            errors.append(
                f"  alias {alias!r} also exists as a canonical workflow directory"
            )
        if target not in canonical:
            errors.append(
                f"  alias {alias!r} -> {target!r} but {target!r} is not a canonical workflow"
            )
    assert not errors, (
        "Workflow alias registry inconsistencies:\n" + "\n".join(errors)
    )
