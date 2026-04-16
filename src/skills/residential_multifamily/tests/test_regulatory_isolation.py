"""Regulatory isolation tests.

Enforces the boundary between conventional market-positioning segments
(middle_market, luxury) and the regulatory affordable-housing overlay family.

Specifically:
- The routing axes catalog must declare a `regulatory_program` axis with
  `none` as the default and the seven canonical values.
- The routing defaults must pin `regulatory_program: none` so no route
  silently pulls regulatory content.
- The routing rules must contain r011 (explicit regulatory invocation) and
  r012 (defensive: conventional routes never auto-load regulatory).
- The `overlays/regulatory/` family exists with the expected scaffolding.
- The `overlays/regulatory/affordable/programs/` family has the required
  program sub-overlays.
- Conventional segment overlays (middle_market, luxury) contain no regulatory
  program tokens (LIHTC, HUD Section 8, AMI band, rent limit, etc.).
- Conventional workflows never read from regulatory overlay paths unless
  they explicitly declare a non-`none` `regulatory_program` in `applies_to`.
- The legacy `overlays/segments/affordable/DEPRECATED.md` marker is in place.

See docs/plans/residential-multifamily-refinement-2026-04-15.md section 5.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import pytest
import yaml

try:
    from conftest import SUBSYS, iter_workflow_pack_skill_paths, split_frontmatter
except ImportError:  # pragma: no cover - belt and suspenders
    SUBSYS = Path(__file__).resolve().parents[1]
    raise


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REQUIRED_REGULATORY_PROGRAM_VALUES = {
    "none",
    "lihtc",
    "hud_section_8",
    "hud_202_811",
    "usda_rd",
    "state_program",
    "mixed_income",
}

# Regulatory tokens that must not appear in conventional overlay files.
# Word-boundary regex patterns so 'reac' does not match 'breach' / 'outreach',
# and so generic English substrings do not false-positive. Matched case-insensitive.
REGULATORY_TOKENS = [
    r"\blihtc\b",
    r"\bhud[\s-]section[\s-]?8\b",
    r"\bhap contract\b",
    r"\bvoucher eligibility\b",
    r"\bami band\b",
    r"\brent limit schedule\b",
    r"\bincome limit schedule\b",
    r"\butility allowance schedule\b",
    r"\btracs submission\b",
    r"\breac inspection\b",
    r"\bnspire inspection\b",
    r"\b8609\b",
    r"\bextended use covenant\b",
]


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path} did not parse to a mapping"
    return data


def _axes_by_slug(axes_doc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for axis in axes_doc.get("axes") or []:
        slug = axis.get("slug")
        if slug:
            out[slug] = axis
    return out


def _scan_for_tokens(path: Path, tokens: Iterable[str]) -> List[str]:
    """Return [(token, path)] hits for the given file. Tokens are regex patterns;
    matching is case-insensitive with word boundaries to avoid substring false
    positives like 'reac' in 'breach' / 'outreach'."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{path}: unreadable ({exc})"]
    hits: List[str] = []
    for tok in tokens:
        if re.search(tok, text, flags=re.IGNORECASE):
            hits.append(f"{path.relative_to(SUBSYS)}: contains regulatory token {tok!r}")
    return hits


# ---------------------------------------------------------------------------
# Axes, defaults, and rules
# ---------------------------------------------------------------------------

def test_axes_has_regulatory_program():
    axes_path = SUBSYS / "_core" / "routing" / "axes.yaml"
    assert axes_path.exists(), f"missing axes catalog: {axes_path}"
    axes_doc = _load_yaml(axes_path)
    axes = _axes_by_slug(axes_doc)
    assert "regulatory_program" in axes, (
        f"{axes_path.relative_to(SUBSYS)}: missing required axis slug "
        f"'regulatory_program'. Axes present: {sorted(axes.keys())}"
    )
    axis = axes["regulatory_program"]
    assert axis.get("required") == "conditional", (
        f"{axes_path.relative_to(SUBSYS)}: regulatory_program axis must be "
        f"required: conditional, got required={axis.get('required')!r}"
    )
    assert axis.get("default") == "none", (
        f"{axes_path.relative_to(SUBSYS)}: regulatory_program axis default must be "
        f"'none', got {axis.get('default')!r}"
    )
    values = axis.get("values") or []
    missing = REQUIRED_REGULATORY_PROGRAM_VALUES - set(values)
    assert not missing, (
        f"{axes_path.relative_to(SUBSYS)}: regulatory_program values missing "
        f"required members {sorted(missing)}; got {values!r}"
    )


def test_defaults_include_regulatory_program_none():
    defaults_path = SUBSYS / "_core" / "routing" / "defaults.yaml"
    assert defaults_path.exists(), f"missing defaults: {defaults_path}"
    defaults_doc = _load_yaml(defaults_path)
    defaults = defaults_doc.get("defaults") or {}
    assert "regulatory_program" in defaults, (
        f"{defaults_path.relative_to(SUBSYS)}: defaults must pin "
        f"'regulatory_program' (expected value: none). Keys present: "
        f"{sorted(defaults.keys())}"
    )
    val = defaults.get("regulatory_program")
    assert val == "none", (
        f"{defaults_path.relative_to(SUBSYS)}: defaults.regulatory_program must "
        f"be 'none' (safe default), got {val!r}"
    )


def test_rules_contain_regulatory_guard():
    rules_path = SUBSYS / "_core" / "routing" / "rules.yaml"
    assert rules_path.exists(), f"missing rules: {rules_path}"
    rules_doc = _load_yaml(rules_path)
    rules = rules_doc.get("rules") or []
    ids = [r.get("id", "") for r in rules]

    r011s = [r for r in rules if str(r.get("id", "")).startswith("r011")]
    r012s = [r for r in rules if str(r.get("id", "")).startswith("r012")]
    assert r011s, (
        f"{rules_path.relative_to(SUBSYS)}: no rule with id starting with 'r011' "
        f"found. Rule ids: {ids}"
    )
    assert r012s, (
        f"{rules_path.relative_to(SUBSYS)}: no rule with id starting with 'r012' "
        f"found. Rule ids: {ids}"
    )

    # r012 must name segment: [middle_market, luxury] and null out regulatory_overlay.
    # The condition may be a bare list or a {any_of: [...]} dict — normalize.
    r012 = r012s[0]
    conditions = r012.get("conditions") or {}
    seg = conditions.get("segment")
    if isinstance(seg, dict):
        seg_list = seg.get("any_of") or seg.get("oneOf") or []
    elif isinstance(seg, list):
        seg_list = seg
    elif seg is None:
        seg_list = []
    else:
        seg_list = [seg]
    required_segments = {"middle_market", "luxury"}
    assert required_segments.issubset({v for v in seg_list if isinstance(v, str)}), (
        f"{rules_path.relative_to(SUBSYS)}: r012 conditions.segment must include "
        f"both 'middle_market' and 'luxury' (bare list or any_of); got {seg!r}"
    )
    selects = r012.get("selects") or {}
    assert "regulatory_overlay" in selects and selects.get("regulatory_overlay") is None, (
        f"{rules_path.relative_to(SUBSYS)}: r012 selects must set "
        f"'regulatory_overlay: null'; got {selects.get('regulatory_overlay')!r}"
    )


# ---------------------------------------------------------------------------
# Regulatory overlay family scaffolding
# ---------------------------------------------------------------------------

def test_overlays_regulatory_family_exists():
    reg_root = SUBSYS / "overlays" / "regulatory"
    missing: List[str] = []
    if not reg_root.exists():
        pytest.fail(f"missing overlays/regulatory/ directory at {reg_root}")
    for rel in ("README.md", "OVERLAY_FAMILY.md", "_shared", "affordable/overlay.yaml"):
        p = reg_root / rel
        if not p.exists():
            missing.append(str(p.relative_to(SUBSYS)))
    assert not missing, (
        "regulatory overlay family missing expected scaffolding:\n  - "
        + "\n  - ".join(missing)
    )


def test_overlays_regulatory_programs_present():
    programs_root = SUBSYS / "overlays" / "regulatory" / "affordable" / "programs"
    if not programs_root.exists():
        pytest.fail(
            f"missing regulatory programs root: "
            f"{programs_root.relative_to(SUBSYS)}"
        )
    required_programs = ["lihtc", "hud_section_8", "state_program", "mixed_income"]
    failures: List[str] = []
    for prog in required_programs:
        prog_dir = programs_root / prog
        overlay_yaml = prog_dir / "overlay.yaml"
        if not prog_dir.is_dir():
            failures.append(
                f"{programs_root.relative_to(SUBSYS)}/{prog}/: directory missing"
            )
            continue
        if not overlay_yaml.exists():
            failures.append(
                f"{overlay_yaml.relative_to(SUBSYS)}: overlay.yaml missing"
            )
            continue
        try:
            data = _load_yaml(overlay_yaml)
        except (AssertionError, yaml.YAMLError) as exc:
            failures.append(
                f"{overlay_yaml.relative_to(SUBSYS)}: did not parse ({exc})"
            )
            continue
        kind = str(data.get("overlay_kind", ""))
        parent = str(data.get("parent_overlay", ""))
        kind_ok = kind.startswith("regulatory.program") or kind == "regulatory"
        parent_ok = parent == "regulatory.affordable"
        if not (kind_ok or parent_ok):
            failures.append(
                f"{overlay_yaml.relative_to(SUBSYS)}: overlay_kind "
                f"({kind!r}) does not match 'regulatory.program' and "
                f"parent_overlay ({parent!r}) is not 'regulatory.affordable'"
            )
    assert not failures, "\n".join(failures)


# ---------------------------------------------------------------------------
# Conventional content must be free of regulatory tokens
# ---------------------------------------------------------------------------

def _iter_conventional_overlay_files() -> List[Path]:
    """Scan middle_market and luxury segment overlays; skip deprecated affordable."""
    candidates: List[Path] = []
    for seg in ("middle_market", "luxury"):
        seg_dir = SUBSYS / "overlays" / "segments" / seg
        if not seg_dir.exists():
            continue
        for p in seg_dir.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml"}:
                candidates.append(p)
    return candidates


def test_conventional_overlays_free_of_regulatory_tokens():
    hits: List[str] = []
    files = _iter_conventional_overlay_files()
    assert files, (
        "no conventional overlay files (middle_market / luxury) found under "
        "overlays/segments/"
    )
    for path in files:
        hits.extend(_scan_for_tokens(path, REGULATORY_TOKENS))
    assert not hits, (
        "conventional segment overlays contain regulatory tokens (these must "
        "live under overlays/regulatory/ instead):\n  - " + "\n  - ".join(hits)
    )


# ---------------------------------------------------------------------------
# Conventional workflows do not reference regulatory paths
# ---------------------------------------------------------------------------

_REGULATORY_READ_PREFIXES = (
    "overlays/regulatory/",
    "reference/normalized/rent_limits__",
    "reference/normalized/income_limits__",
)


def _applies_to_regulatory_programs(fm: Dict[str, Any]) -> Set[str]:
    """Return the set of regulatory_program values declared in applies_to (may be empty)."""
    applies = fm.get("applies_to") or {}
    vals = applies.get("regulatory_program")
    if vals is None:
        return set()
    if isinstance(vals, str):
        return {vals}
    return set(vals)


def _workflow_has_regulatory_scope(fm: Dict[str, Any]) -> bool:
    """A workflow is 'regulatory-aware' only if its applies_to declares a
    non-empty, non-{none} set of regulatory_program values."""
    declared = _applies_to_regulatory_programs(fm)
    if not declared:
        return False
    # Treat a declaration of exactly [none] as conventional-only.
    if declared == {"none"}:
        return False
    return True


def test_conventional_workflows_do_not_reference_regulatory_paths():
    failures: List[str] = []
    found_any = False
    for skill_path in iter_workflow_pack_skill_paths():
        found_any = True
        # Parse frontmatter to decide whether this workflow is regulatory-aware.
        try:
            text = skill_path.read_text(encoding="utf-8")
            fm, _ = split_frontmatter(text)
        except (AssertionError, OSError) as exc:
            failures.append(
                f"{skill_path.relative_to(SUBSYS)}: could not parse frontmatter ({exc})"
            )
            continue
        if _workflow_has_regulatory_scope(fm):
            continue  # regulatory-aware workflows may read regulatory paths
        manifest_path = skill_path.parent / "reference_manifest.yaml"
        if not manifest_path.exists():
            continue
        try:
            manifest = _load_yaml(manifest_path)
        except (AssertionError, yaml.YAMLError) as exc:
            failures.append(
                f"{manifest_path.relative_to(SUBSYS)}: unparseable ({exc})"
            )
            continue
        for idx, entry in enumerate(manifest.get("reads") or []):
            path_str = str(entry.get("path") or "")
            for bad_prefix in _REGULATORY_READ_PREFIXES:
                if bad_prefix in path_str:
                    failures.append(
                        f"{manifest_path.relative_to(SUBSYS)}: reads[{idx}].path "
                        f"{path_str!r} references regulatory-only substring "
                        f"{bad_prefix!r} but the workflow is not regulatory-scoped"
                    )
    assert found_any, "no workflow SKILL.md files found"
    assert not failures, (
        "conventional workflows pull regulatory references:\n  - "
        + "\n  - ".join(failures)
    )


# ---------------------------------------------------------------------------
# Deprecated marker for segments/affordable
# ---------------------------------------------------------------------------

def test_segments_affordable_deprecated_marker_present():
    dep = SUBSYS / "overlays" / "segments" / "affordable" / "DEPRECATED.md"
    assert dep.exists(), (
        f"{dep.relative_to(SUBSYS)}: migration stub is missing. The "
        f"'overlays/segments/affordable/' directory must carry a DEPRECATED.md "
        f"pointing users at 'overlays/regulatory/affordable/'."
    )
