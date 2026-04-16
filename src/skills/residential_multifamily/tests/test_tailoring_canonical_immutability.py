"""Tailoring canonical-immutability tests.

Ensures the tailoring pack cannot silently mutate canonical core, segment
overlays, regulatory overlays, or the reference layer.

Assertions:
- tailoring/reference_manifest.yaml writes[] targets are confined to
  tailoring/** or overlays/org/{org_id}/**.
- tailoring/SKILL.md frontmatter references.writes are likewise confined.
- tailoring/question_banks/*.yaml never inject `override_value` entries that
  would redefine a canonical metric's numerator, denominator, rollup_rule,
  filters_default, inclusions, or exclusions (silent-redefinition guard).
- tailoring/AUDIENCE_MAP.md, DIFF_APPROVAL_PREVIEW.md, and MISSING_DOC_MATRIX.md
  are present (new spec artifacts from section 7).
- The 8-audience question_banks layout is present (executive, regional_ops,
  asset_mgmt, finance_reporting, development, construction, compliance_risk,
  site_ops).
- Legacy banks (coo.yaml, cfo.yaml, reporting.yaml) — if retained — declare
  a deprecation/redirect header.

See docs/plans/residential-multifamily-refinement-2026-04-15.md section 7.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import pytest
import yaml

try:
    from conftest import SUBSYS, extract_yaml_blocks_lenient, split_frontmatter
except ImportError:  # pragma: no cover
    SUBSYS = Path(__file__).resolve().parents[1]
    raise


TAILORING_ROOT = SUBSYS / "tailoring"

FORBIDDEN_WRITE_PREFIXES = (
    "_core/",
    "overlays/segments/",
    "overlays/regulatory/",
    "reference/raw/",
    "reference/normalized/",
    "reference/derived/",
)

# Paths under these prefixes are permitted writes for the tailoring pack.
# `{org_id}` is a template placeholder that resolves at session time.
ALLOWED_WRITE_PREFIXES = (
    "tailoring/",
    "overlays/org/",  # includes overlays/org/{org_id}/**
)

REQUIRED_QUESTION_BANKS = [
    "executive.yaml",
    "regional_ops.yaml",
    "asset_mgmt.yaml",
    "finance_reporting.yaml",
    "development.yaml",
    "construction.yaml",
    "compliance_risk.yaml",
    "site_ops.yaml",
]

LEGACY_BANKS = ["coo.yaml", "cfo.yaml", "reporting.yaml"]

# Keywords that must appear in a legacy-bank header comment to confirm a
# human reader is redirected to the new bank.
REDIRECT_MARKERS = ("deprecated", "superseded", "moved", "redirect")

# Canonical-metric aspect tokens. A pattern of `<metric_slug>.<aspect>` in a
# question bank indicates an attempt to redefine a canonical metric.
CANONICAL_METRIC_ASPECTS = (
    "numerator",
    "denominator",
    "rollup_rule",
    "filters_default",
    "inclusions",
    "exclusions",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_yaml_lenient(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _canonical_metric_slugs() -> Set[str]:
    """Pull every metric slug from _core/metrics.md fenced YAML blocks."""
    text = (SUBSYS / "_core" / "metrics.md").read_text(encoding="utf-8")
    blocks, _errors = extract_yaml_blocks_lenient(text)
    return {b.get("slug") for b in blocks if b.get("slug")}


def _resolve_path_template(path_str: str) -> str:
    """Strip obvious template placeholders for prefix comparison."""
    # Replace any {…} with an empty string so 'overlays/org/{org_id}/' resolves
    # to 'overlays/org/' which matches ALLOWED_WRITE_PREFIXES.
    return re.sub(r"\{[^}]+\}", "", path_str)


def _walk_strings(obj: Any) -> Iterable[str]:
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v)


def _has_forbidden_prefix(path_str: str) -> str | None:
    resolved = _resolve_path_template(path_str).lstrip("./")
    for bad in FORBIDDEN_WRITE_PREFIXES:
        if resolved.startswith(bad):
            return bad
    return None


def _has_allowed_prefix(path_str: str) -> bool:
    resolved = _resolve_path_template(path_str).lstrip("./")
    return any(resolved.startswith(p) for p in ALLOWED_WRITE_PREFIXES)


# ---------------------------------------------------------------------------
# reference_manifest.yaml writes
# ---------------------------------------------------------------------------

def test_tailoring_writes_never_hit_core():
    manifest_path = TAILORING_ROOT / "reference_manifest.yaml"
    if not manifest_path.exists():
        pytest.skip(
            f"{manifest_path.relative_to(SUBSYS)}: optional manifest not present"
        )
    data = _load_yaml_lenient(manifest_path) or {}
    writes = data.get("writes") or []
    failures: List[str] = []
    for idx, entry in enumerate(writes):
        if not isinstance(entry, dict):
            failures.append(
                f"{manifest_path.relative_to(SUBSYS)}: writes[{idx}] is not a mapping"
            )
            continue
        path_str = str(entry.get("path") or "")
        if not path_str:
            failures.append(
                f"{manifest_path.relative_to(SUBSYS)}: writes[{idx}] missing 'path'"
            )
            continue
        bad = _has_forbidden_prefix(path_str)
        if bad:
            failures.append(
                f"{manifest_path.relative_to(SUBSYS)}: writes[{idx}].path {path_str!r} "
                f"targets forbidden prefix {bad!r}"
            )
        elif not _has_allowed_prefix(path_str):
            failures.append(
                f"{manifest_path.relative_to(SUBSYS)}: writes[{idx}].path {path_str!r} "
                f"is outside allowed prefixes {ALLOWED_WRITE_PREFIXES}"
            )
    assert not failures, "tailoring reference_manifest writes violation:\n  - " + "\n  - ".join(failures)


# ---------------------------------------------------------------------------
# SKILL.md frontmatter references.writes
# ---------------------------------------------------------------------------

def test_tailoring_skill_md_writes_scope():
    skill_path = TAILORING_ROOT / "SKILL.md"
    assert skill_path.exists(), (
        f"{skill_path.relative_to(SUBSYS)}: tailoring SKILL.md is required"
    )
    text = skill_path.read_text(encoding="utf-8")
    fm, _body = split_frontmatter(text)
    references = fm.get("references") or {}
    writes = references.get("writes") or []
    failures: List[str] = []
    for idx, path_str in enumerate(writes):
        if not isinstance(path_str, str):
            failures.append(
                f"{skill_path.relative_to(SUBSYS)}: references.writes[{idx}] is not a string"
            )
            continue
        bad = _has_forbidden_prefix(path_str)
        if bad:
            failures.append(
                f"{skill_path.relative_to(SUBSYS)}: references.writes[{idx}] {path_str!r} "
                f"targets forbidden prefix {bad!r}"
            )
        elif not _has_allowed_prefix(path_str):
            failures.append(
                f"{skill_path.relative_to(SUBSYS)}: references.writes[{idx}] {path_str!r} "
                f"is outside allowed prefixes {ALLOWED_WRITE_PREFIXES}"
            )
    assert not failures, "tailoring SKILL.md writes violation:\n  - " + "\n  - ".join(failures)


# ---------------------------------------------------------------------------
# Question bank canonical-metric redefinition guard
# ---------------------------------------------------------------------------

def test_question_banks_do_not_redefine_canonical_metrics():
    qb_root = TAILORING_ROOT / "question_banks"
    if not qb_root.exists():
        pytest.skip(f"{qb_root.relative_to(SUBSYS)}: question_banks/ not present")
    metric_slugs = _canonical_metric_slugs()
    if not metric_slugs:
        pytest.skip("no canonical metric slugs discovered in _core/metrics.md")
    # Build a regex that matches '<slug>.<aspect>' for any canonical slug +
    # aspect. We require word boundaries on the slug so partial matches fail.
    slug_group = "|".join(sorted(re.escape(s) for s in metric_slugs))
    aspect_group = "|".join(CANONICAL_METRIC_ASPECTS)
    redefine_re = re.compile(
        rf"\b({slug_group})\.({aspect_group})\b", re.IGNORECASE
    )
    # Secondary heuristic: any occurrence of 'override_value:' in the same file
    # that also names a canonical metric slug is flagged.
    failures: List[str] = []
    for path in sorted(qb_root.glob("*.yaml")):
        try:
            data = _load_yaml_lenient(path)
        except yaml.YAMLError as exc:
            failures.append(f"{path.relative_to(SUBSYS)}: unparseable ({exc})")
            continue
        values = list(_walk_strings(data)) if data is not None else []
        # Aspect pattern: strongest signal of canonical redefinition.
        for v in values:
            for m in redefine_re.finditer(v):
                failures.append(
                    f"{path.relative_to(SUBSYS)}: canonical metric redefinition pattern "
                    f"{m.group(0)!r} found (metric.aspect pairing is reserved for "
                    f"_core/metrics.md)"
                )
        # Weaker combined signal: override_value plus a metric slug in the same value.
        for v in values:
            if "override_value:" in v.lower():
                for slug in metric_slugs:
                    if re.search(rf"\b{re.escape(slug)}\b", v):
                        failures.append(
                            f"{path.relative_to(SUBSYS)}: value contains 'override_value:' "
                            f"alongside canonical metric slug {slug!r}"
                        )
                        break
    assert not failures, "question bank canonical-metric redefinitions:\n  - " + "\n  - ".join(failures)


# ---------------------------------------------------------------------------
# New spec artifacts
# ---------------------------------------------------------------------------

def test_audience_map_is_present():
    p = TAILORING_ROOT / "AUDIENCE_MAP.md"
    assert p.exists(), (
        f"{p.relative_to(SUBSYS)}: tailoring AUDIENCE_MAP.md is required "
        f"per section 7 of the refinement plan"
    )


def test_diff_approval_preview_spec_present():
    p = TAILORING_ROOT / "DIFF_APPROVAL_PREVIEW.md"
    assert p.exists(), (
        f"{p.relative_to(SUBSYS)}: tailoring DIFF_APPROVAL_PREVIEW.md is required "
        f"per section 7 of the refinement plan"
    )


def test_missing_doc_matrix_present():
    p = TAILORING_ROOT / "MISSING_DOC_MATRIX.md"
    assert p.exists(), (
        f"{p.relative_to(SUBSYS)}: tailoring MISSING_DOC_MATRIX.md is required "
        f"per section 7 of the refinement plan"
    )


# ---------------------------------------------------------------------------
# Question bank layout
# ---------------------------------------------------------------------------

def test_required_question_banks_present():
    qb_root = TAILORING_ROOT / "question_banks"
    assert qb_root.exists(), (
        f"{qb_root.relative_to(SUBSYS)}: tailoring/question_banks/ directory missing"
    )
    missing: List[str] = []
    for name in REQUIRED_QUESTION_BANKS:
        p = qb_root / name
        if not p.exists():
            missing.append(name)
    assert not missing, (
        "required question banks are missing from "
        f"{qb_root.relative_to(SUBSYS)}/: {missing}"
    )


def test_legacy_question_banks_redirect():
    qb_root = TAILORING_ROOT / "question_banks"
    if not qb_root.exists():
        pytest.skip(f"{qb_root.relative_to(SUBSYS)}: question_banks/ not present")
    inspected = False
    failures: List[str] = []
    for name in LEGACY_BANKS:
        p = qb_root / name
        if not p.exists():
            continue  # legacy file already removed — acceptable
        inspected = True
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            failures.append(f"{p.relative_to(SUBSYS)}: unreadable ({exc})")
            continue
        # Look within the top-of-file comment block. Non-comment YAML content
        # or a blank line terminates the header.
        header: List[str] = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if header:
                    break
                continue
            if not stripped.startswith("#"):
                break
            header.append(stripped.lower())
        if not header:
            failures.append(
                f"{p.relative_to(SUBSYS)}: legacy bank retained but has no "
                f"top-of-file comment header. Add a '# deprecated/superseded/"
                f"moved' banner pointing readers at the new bank."
            )
            continue
        joined = " ".join(header)
        if not any(marker in joined for marker in REDIRECT_MARKERS):
            failures.append(
                f"{p.relative_to(SUBSYS)}: legacy bank retained but header does "
                f"not contain any of {REDIRECT_MARKERS}. Add a redirect banner."
            )
    if not inspected:
        pytest.skip("no legacy question banks remain — nothing to redirect")
    assert not failures, "\n  - ".join(["legacy redirect violations:"] + failures)
