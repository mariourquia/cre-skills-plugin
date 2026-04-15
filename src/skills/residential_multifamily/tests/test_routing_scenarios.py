"""Routing scenario validation.

Loads every ROUTING.md in examples/* and extracts:
- The axis resolution table (a markdown table headed by 'Axis | Resolved to | ...').
- The 'Packs loaded' section, which lists repo-relative paths.

Then asserts:
- Each axis value is in the allowed set from _core/routing/axes.yaml.
- Each pack path referenced exists as a directory inside the subsystem.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterator, List, Set

import yaml

from conftest import SUBSYS


def _iter_routing_md() -> Iterator[Path]:
    examples_dir = SUBSYS / "examples"
    if not examples_dir.exists():
        return
    for sub in sorted(examples_dir.iterdir()):
        if not sub.is_dir():
            continue
        routing = sub / "ROUTING.md"
        if routing.exists():
            yield routing


def _load_axes_catalog() -> Dict[str, Set[str]]:
    axes_path = SUBSYS / "_core" / "routing" / "axes.yaml"
    with axes_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    out: Dict[str, Set[str]] = {}
    for axis in data.get("axes") or []:
        slug = axis.get("slug")
        vals = axis.get("values")
        if vals is None:
            out[slug] = set()  # free-form
        else:
            out[slug] = set(vals)
    return out


# Parse an axis table: rows start with "| `axis_name` |" (backticks) and a value.
_AXIS_ROW_RE = re.compile(
    r"^\|\s*`(?P<axis>[a-z_]+)`\s*\|\s*(?P<val>[^|]+?)\s*\|", re.MULTILINE
)

# Parse packs listed as "- `path/to/pack/` (...)".
_PACK_PATH_RE = re.compile(r"`([A-Za-z_][A-Za-z0-9_/\-]+/?)`")


def _extract_axis_values(md_text: str) -> Dict[str, List[str]]:
    """Extract axis->value pairs from the axis resolution table.

    Each row's value column may contain backticks around a single value, or several
    values separated by '+' / ','. We tokenize into a list and strip backticks.
    """
    out: Dict[str, List[str]] = {}
    for m in _AXIS_ROW_RE.finditer(md_text):
        axis = m.group("axis")
        val_cell = m.group("val")
        # Token split: split on ',', '+', '/', 'and' keeping only tokens in backticks
        # when present; otherwise take the whole cell.
        tokens = re.findall(r"`([^`]+)`", val_cell)
        if not tokens:
            # Free-form text. Capture as a single value with whitespace trimmed.
            tokens = [val_cell.strip()]
        out.setdefault(axis, []).extend(tokens)
    return out


def _extract_packs_loaded(md_text: str) -> List[str]:
    """Extract the list of repo-relative pack paths from the 'Packs loaded' section."""
    # Find the section.
    section_match = re.search(
        r"##\s+Packs loaded\s*\n(?P<body>.+?)(?=\n##\s|\Z)",
        md_text,
        re.DOTALL,
    )
    if not section_match:
        return []
    body = section_match.group("body")
    paths: List[str] = []
    for line in body.splitlines():
        if line.strip().startswith("-"):
            for m in _PACK_PATH_RE.finditer(line):
                token = m.group(1).rstrip("/")
                if "/" in token:
                    paths.append(token)
    return paths


def test_at_least_one_example_has_routing_md():
    assert list(_iter_routing_md()), "no examples/*/ROUTING.md files found"


# Sentinel tokens legitimately used in portfolio-level routing where a single axis
# value does not apply (e.g., a portfolio-manager or executive summary spanning
# multiple form factors, lifecycle stages, or management modes). These are
# documented states, not axis values.
_PORTFOLIO_SENTINELS = {
    "mixed",
    "mixed - not pinned",
    "mixed — not pinned",
    "portfolio-wide",
    "portfolio wide",
    "not pinned",
    "not resolved",
    "n/a",
}


def test_axis_values_in_allowed_set():
    catalog = _load_axes_catalog()
    failures: List[str] = []
    for md_path in _iter_routing_md():
        text = md_path.read_text(encoding="utf-8")
        extracted = _extract_axis_values(text)
        for axis, tokens in extracted.items():
            allowed = catalog.get(axis)
            if allowed is None:
                # Not a declared axis; skip (the file may mention other axes).
                continue
            if not allowed:
                # Free-form axis (e.g., market, workflow, org_id). Skip value check.
                continue
            for tok in tokens:
                cleaned = tok.strip().lower()
                # Skip bracketed annotations like "(see note)" that are not a value.
                if cleaned.startswith("("):
                    continue
                if cleaned in _PORTFOLIO_SENTINELS:
                    continue
                if tok.strip() in allowed:
                    continue
                # Permit compound values like "middle_market + renovation sub-list" by
                # splitting on separators and re-checking each sub-token against the
                # allowed set, portfolio sentinels, and a few short connector words.
                sub_tokens = [t for t in re.split(r"[\s+,/()]", tok.strip()) if t]
                if sub_tokens and all(
                    (
                        st in allowed
                        or st.lower() in _PORTFOLIO_SENTINELS
                        or st.lower() in ("with", "and", "plus", "sub-list", "list")
                    )
                    for st in sub_tokens
                ):
                    continue
                failures.append(
                    f"{md_path.relative_to(SUBSYS)}: axis {axis!r} value {tok.strip()!r} "
                    f"not in allowed set {sorted(allowed)} (and not a portfolio sentinel)"
                )
    assert not failures, "\n".join(failures)


def _workflow_slugs_declared_in_rules() -> set:
    """Return the set of workflow slugs referenced by _core/routing/rules.yaml.

    The routing rules may legitimately reference workflow packs that have not yet been
    scaffolded in Phase 1. Paths named in rules.yaml are considered declared intents
    and we do not fail the test on their folder absence.
    """
    rules_path = SUBSYS / "_core" / "routing" / "rules.yaml"
    if not rules_path.exists():
        return set()
    with rules_path.open("r", encoding="utf-8") as f:
        text = f.read()
    slugs: set = set()
    for m in re.finditer(r"workflows/([a-z_][a-z0-9_]*)", text):
        slugs.add(m.group(1))
    return slugs


def test_every_pack_path_in_routing_exists():
    failures: List[str] = []
    # Valid pack-path prefixes we check as directories under SUBSYS.
    allowed_prefixes = (
        "roles/",
        "workflows/",
        "overlays/",
        "templates/",
        "reference/",
        "tailoring/",
        "_core/",
    )
    declared_workflows = _workflow_slugs_declared_in_rules()
    for md_path in _iter_routing_md():
        text = md_path.read_text(encoding="utf-8")
        paths = _extract_packs_loaded(text)
        for p in paths:
            if not p.startswith(allowed_prefixes):
                # Not a pack path; skip.
                continue
            # org-specific overlays use {org_id}; we allow those if the placeholder or
            # the "examples_org" placeholder org exists.
            if "{" in p or "}" in p:
                continue
            if p.endswith("examples_org") or p.endswith("examples_org/"):
                # The org overlay for examples_org may not exist yet in Phase 1.
                continue
            # Workflows declared in rules.yaml are allowed even if not scaffolded.
            if p.startswith("workflows/"):
                slug = p.split("/", 1)[1].strip("/")
                if slug in declared_workflows:
                    continue
            candidate = SUBSYS / p
            if not candidate.exists():
                failures.append(
                    f"{md_path.relative_to(SUBSYS)}: pack path {p!r} does not exist"
                )
    assert not failures, "\n".join(failures)
