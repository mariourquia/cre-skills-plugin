"""Boundary-rule tests.

Enforces the layered boundary contract from `_core/BOUNDARIES.md`:

- `_core/` is segment-agnostic and free of regulated-program tokens.
- Conventional middle-market segment overlays never contain regulatory tokens.
- Regulatory overlays never contain market-positioning (luxury/brand) tokens.
  This last check is a review cue (warnings, not hard fail) EXCEPT when the
  token appears inside a regulatory override's `target_kind` field — that is
  a hard fail because it indicates a structural misclassification.
- Role and workflow pack `applies_to.segment` declarations that claim both
  'middle_market' and 'affordable' are surfaced as a warning so the next
  refinement wave can narrow them (not a failure in this pass).

See docs/plans/residential-multifamily-refinement-2026-04-15.md section 4.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pytest
import yaml

try:
    from conftest import (
        SUBSYS,
        iter_role_pack_skill_paths,
        iter_workflow_pack_skill_paths,
        split_frontmatter,
    )
except ImportError:  # pragma: no cover
    SUBSYS = Path(__file__).resolve().parents[1]
    raise


BOUNDARIES_MD = SUBSYS / "_core" / "BOUNDARIES.md"

# Case-insensitive substrings that must appear in BOUNDARIES.md.
REQUIRED_BOUNDARIES_HEADINGS = [
    "conventional middle-market core",
    "middle-market segment overlay",
    "affordable overlay family",
    "luxury segment overlay",
    "market overlays",
    "org overlays",
]

# Regulated-program COMPLIANCE-CONTENT tokens that must not appear in _core/ or
# middle-market overlays. These target actual program-content leakage, not mere
# enumeration of program names (axes.yaml rightly lists program values; that is
# not leakage). Matched as case-insensitive word-boundary regexes.
REGULATORY_TOKENS = [
    r"\brent limit schedule\b",
    r"\bincome limit schedule\b",
    r"\butility allowance schedule\b",
    r"\breac inspection\b",
    r"\bnspire inspection\b",
    r"\btracs submission\b",
    r"\bhap contract\b",
    r"\b8609\b",
    r"\bami band\b",
    r"\bextended use covenant\b",
    r"\bqualified contract\b",
    r"\brecertification cycle\b",
    r"\bagency inspection readiness\b",
]

# Market-positioning / brand tokens that signal the wrong layer when found in
# regulatory overlays. Presence is a review warning unless it lands in a
# regulatory override's target_kind field, where it is a hard failure.
MARKET_POSITIONING_TOKENS = [
    "brand",
    "hospitality",
    "concierge",
    "luxury",
    "stone countertop",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _scan_tokens(path: Path, tokens: Iterable[str]) -> List[str]:
    """Scan a file for regulatory-content tokens. Tokens are regex strings with
    word boundaries; matching is case-insensitive. Substring false positives
    (e.g. 'reac' inside 'breach' / 'outreach') are avoided by design."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{path.relative_to(SUBSYS)}: unreadable ({exc})"]
    hits: List[str] = []
    for tok in tokens:
        if re.search(tok, text, flags=re.IGNORECASE):
            hits.append(f"{path.relative_to(SUBSYS)}: contains token {tok!r}")
    return hits


def _iter_core_files(skip_boundaries: bool = True) -> List[Path]:
    """Files directly under _core/, _core/routing/, _core/schemas/ with .md/.yaml/.yml."""
    core = SUBSYS / "_core"
    out: List[Path] = []
    if not core.exists():
        return out
    for sub in (core, core / "routing", core / "schemas"):
        if not sub.exists():
            continue
        for p in sub.iterdir():
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".md", ".yaml", ".yml"}:
                continue
            if skip_boundaries and p == BOUNDARIES_MD:
                continue
            out.append(p)
    return out


def _iter_middle_market_files() -> List[Path]:
    mm = SUBSYS / "overlays" / "segments" / "middle_market"
    out: List[Path] = []
    if not mm.exists():
        return out
    for p in mm.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml"}:
            out.append(p)
    return out


def _iter_regulatory_files() -> List[Path]:
    reg = SUBSYS / "overlays" / "regulatory"
    out: List[Path] = []
    if not reg.exists():
        return out
    for p in reg.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml"}:
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# BOUNDARIES.md
# ---------------------------------------------------------------------------

def test_boundaries_md_present():
    assert BOUNDARIES_MD.exists(), (
        f"{BOUNDARIES_MD.relative_to(SUBSYS)}: _core/BOUNDARIES.md is required "
        f"per section 4 of the refinement plan"
    )
    text = BOUNDARIES_MD.read_text(encoding="utf-8").lower()
    missing: List[str] = []
    for heading in REQUIRED_BOUNDARIES_HEADINGS:
        if heading.lower() not in text:
            missing.append(heading)
    assert not missing, (
        f"{BOUNDARIES_MD.relative_to(SUBSYS)}: missing required headings "
        f"(case-insensitive substring match): {missing}"
    )


# ---------------------------------------------------------------------------
# _core has no program tokens
# ---------------------------------------------------------------------------

def test_core_has_no_program_tokens():
    files = _iter_core_files(skip_boundaries=True)
    assert files, "no _core files discovered for token scan"
    hits: List[str] = []
    for p in files:
        hits.extend(_scan_tokens(p, REGULATORY_TOKENS))
    assert not hits, (
        "_core files must be program-agnostic; offending tokens found:\n  - "
        + "\n  - ".join(hits)
    )


# ---------------------------------------------------------------------------
# Middle-market has no regulatory tokens
# ---------------------------------------------------------------------------

def test_middle_market_has_no_regulatory_tokens():
    files = _iter_middle_market_files()
    if not files:
        pytest.fail(
            "overlays/segments/middle_market/ has no files; expected a populated "
            "middle-market overlay"
        )
    hits: List[str] = []
    for p in files:
        hits.extend(_scan_tokens(p, REGULATORY_TOKENS))
    assert not hits, (
        "middle-market segment overlay must be free of regulatory tokens; "
        "offending tokens found:\n  - " + "\n  - ".join(hits)
    )


# ---------------------------------------------------------------------------
# Regulatory must not carry market-positioning tokens in target_kind fields;
# elsewhere, a hit is a soft warning that gets captured via capsys output.
# ---------------------------------------------------------------------------

def _iter_overlay_yaml_overrides(path: Path) -> List[Dict[str, Any]]:
    """Return the list of override mappings in a regulatory overlay.yaml. Tolerates
    files that do not declare `overrides:`.
    """
    if path.name != "overlay.yaml":
        return []
    try:
        data = _load_yaml(path)
    except yaml.YAMLError:
        return []
    if not isinstance(data, dict):
        return []
    overrides = data.get("overrides") or []
    return [o for o in overrides if isinstance(o, dict)]


def test_regulatory_has_no_market_positioning_tokens(capsys):
    files = _iter_regulatory_files()
    if not files:
        pytest.fail(
            "overlays/regulatory/ is empty; expected regulatory overlay family "
            "scaffolding"
        )
    warnings: List[str] = []
    hard_failures: List[str] = []
    for p in files:
        soft_hits = _scan_tokens(p, MARKET_POSITIONING_TOKENS)
        warnings.extend(soft_hits)
        # Hard check: any override_value whose target_kind names a market-positioning
        # token. Surfaces a structural misclassification.
        for idx, override in enumerate(_iter_overlay_yaml_overrides(p)):
            target_kind = str(override.get("target_kind") or "").lower()
            for tok in MARKET_POSITIONING_TOKENS:
                if tok in target_kind:
                    hard_failures.append(
                        f"{p.relative_to(SUBSYS)}: overrides[{idx}].target_kind "
                        f"{override.get('target_kind')!r} names market-positioning "
                        f"token {tok!r}; regulatory overlays may not target "
                        f"market-positioning fields"
                    )
    if warnings:
        # Review cue — surface via captured stdout so the reviewer can read them.
        print("REGULATORY_WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
    assert not hard_failures, (
        "regulatory overlays target market-positioning fields (structural "
        "misclassification):\n  - " + "\n  - ".join(hard_failures)
    )


# ---------------------------------------------------------------------------
# SKILL.md applies_to.segment narrowness (warning, not failure)
# ---------------------------------------------------------------------------

# Packs with an explicitly cross-cutting charter are allowed to span both
# market-positioning segments and the regulatory compliance regime.
_CROSS_CUTTING_PACK_SLUGS = {
    "tailoring",
    "router",
}


def _is_cross_cutting(fm: Dict[str, Any]) -> bool:
    slug = str(fm.get("slug") or "").lower()
    if slug in _CROSS_CUTTING_PACK_SLUGS:
        return True
    if fm.get("pack_type") in {"tailoring", "router"}:
        return True
    # Guardrail / executive-summary packs are explicit cross-cuts.
    if "guardrail" in slug or slug == "executive_operating_summary_generation":
        return True
    return False


def test_skill_md_applies_to_segment_is_narrow(capsys):
    warnings: List[str] = []
    failures: List[str] = []
    for sk in list(iter_role_pack_skill_paths()) + list(iter_workflow_pack_skill_paths()):
        try:
            fm, _ = split_frontmatter(sk.read_text(encoding="utf-8"))
        except AssertionError as exc:
            failures.append(f"{sk.relative_to(SUBSYS)}: frontmatter unreadable ({exc})")
            continue
        applies = fm.get("applies_to") or {}
        segment = applies.get("segment")
        if segment is None or (isinstance(segment, list) and not segment):
            failures.append(
                f"{sk.relative_to(SUBSYS)}: applies_to.segment must be a non-empty list"
            )
            continue
        seg_list = segment if isinstance(segment, list) else [segment]
        if "middle_market" in seg_list and "affordable" in seg_list:
            if _is_cross_cutting(fm):
                continue
            warnings.append(
                f"{sk.relative_to(SUBSYS)}: applies_to.segment includes both "
                f"'middle_market' and 'affordable' ({seg_list}); consider "
                f"narrowing — this is a cue for the next refinement wave, not "
                f"a blocker"
            )
    if warnings:
        print("SEGMENT_NARROWNESS_WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
    # Structural failures are hard (missing/empty applies_to.segment).
    assert not failures, (
        "applies_to.segment structural errors:\n  - " + "\n  - ".join(failures)
    )
