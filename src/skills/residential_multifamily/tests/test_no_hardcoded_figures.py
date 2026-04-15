"""Scan role/workflow/overlay markdown prose for hardcoded figures.

Rule 1 from _core/DESIGN_RULES.md prohibits embedding specific market rents,
concession benchmarks, fixed staffing ratios, approval-threshold dollars, or
percentage benchmarks in skill prose. All such figures must live in the
reference layer.

What this test scans:
- roles/*/SKILL.md
- workflows/*/SKILL.md
- overlays/**/*.md (overlay.yaml is YAML, not prose, so it is NOT scanned here)

What this test exempts from scanning:
- Fenced code blocks (```...```). These hold YAML frontmatter-style examples and
  structured snippets.
- "## Example outputs" sections and "## Example invocations" sections in
  role/workflow packs. Those are explicitly marked as illustrative examples
  per DESIGN_RULES rule 9.

Allow-list of permitted tokens in the remaining prose:
- Four-digit years (1900-2099).
- Version-like tokens (e.g., 0.1.0).
- Metric slug identifiers that happen to end in a number (e.g., delinquency_rate_30plus,
  row 1, row 13 approval matrix references, row 6-8 tiers).
- The phrase "100%" used as the renewal_offer_rate process-discipline target
  (single exempted phrase; any other percentage in prose fails).
- Approval matrix row references written as "row N" or "rows N-M".
- Form factor thresholds referenced textually by _core conventions (4-6 stories, 5-8 stories, 9+ stories).

Flagged patterns (fail):
- Dollar amounts: "$<digit>" or "\\$<digit>" that are not inside a fenced block.
- Percentages like "\\d+%" not in the allow-list.
- Unit ratios matching "1 per \\d+ units" or "\\d+ per \\d+ units" or similar.

If any un-allow-listed hit remains, the test fails with the file and snippet.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator, List, Set, Tuple

from conftest import (
    SUBSYS,
    strip_example_output_sections,
    strip_fenced_code_blocks,
)


# ---------------------------------------------------------------------------
# Files to scan
# ---------------------------------------------------------------------------

def _iter_prose_files() -> Iterator[Path]:
    # roles/*/SKILL.md
    for sk in (SUBSYS / "roles").glob("*/SKILL.md"):
        yield sk
    # workflows/*/SKILL.md
    for sk in (SUBSYS / "workflows").glob("*/SKILL.md"):
        yield sk
    # overlays/**/*.md
    overlays = SUBSYS / "overlays"
    if overlays.exists():
        for md in overlays.rglob("*.md"):
            yield md


# ---------------------------------------------------------------------------
# Allow-lists
# ---------------------------------------------------------------------------

# Percentages that are globally permitted. Keep this deliberately small.
_ALLOWED_PERCENT_TOKENS: Set[str] = {
    # Discipline: renewal_offer_rate target is procedural (not a benchmark).
    "100%",
}

# Prefixes that, if immediately preceding a percentage, allow-list the match.
# Example: "row 1", "row 6-8" -- these are approval-matrix references, not benchmarks.
_PERCENT_ROW_PREFIX_RE = re.compile(r"row\s+\d+", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Flag patterns
# ---------------------------------------------------------------------------

_DOLLAR_RE = re.compile(r"\$\d")  # any literal dollar amount
_PERCENT_RE = re.compile(r"\b\d+(?:\.\d+)?%")  # e.g., 5%, 4.8%, 100%
_UNIT_RATIO_RE = re.compile(
    r"\b\d+\s+per\s+\d+\s+units?\b",
    re.IGNORECASE,
)
_UNIT_RATIO_PER_X_RE = re.compile(
    r"\b1\s+per\s+\d+\s+(?:units?|doors?|homes?)\b",
    re.IGNORECASE,
)


def _is_allow_listed_percent(line_snippet: str, match_text: str) -> bool:
    if match_text in _ALLOWED_PERCENT_TOKENS:
        return True
    # "row N ... <percent>" is an approval-matrix reference block, not a benchmark.
    if _PERCENT_ROW_PREFIX_RE.search(line_snippet):
        return True
    return False


def _find_hits(scrubbed: str) -> List[Tuple[str, str]]:
    """Return a list of (pattern_name, matched_text) for un-allow-listed hits."""
    hits: List[Tuple[str, str]] = []
    for m in _DOLLAR_RE.finditer(scrubbed):
        hits.append(("dollar_amount", scrubbed[max(0, m.start() - 20):m.end() + 20]))
    for m in _PERCENT_RE.finditer(scrubbed):
        text = m.group(0)
        # Grab the local line context for allow-list check.
        start = scrubbed.rfind("\n", 0, m.start()) + 1
        end = scrubbed.find("\n", m.end())
        end = len(scrubbed) if end == -1 else end
        line = scrubbed[start:end]
        if _is_allow_listed_percent(line, text):
            continue
        hits.append(("percent", line.strip()))
    for m in _UNIT_RATIO_RE.finditer(scrubbed):
        hits.append(("unit_ratio", scrubbed[max(0, m.start() - 20):m.end() + 20]))
    for m in _UNIT_RATIO_PER_X_RE.finditer(scrubbed):
        hits.append(("unit_ratio_1_per_x", scrubbed[max(0, m.start() - 20):m.end() + 20]))
    return hits


def test_no_hardcoded_figures_in_prose():
    failures: List[str] = []
    for md_path in _iter_prose_files():
        text = md_path.read_text(encoding="utf-8")
        scrubbed = strip_fenced_code_blocks(text)
        scrubbed = strip_example_output_sections(scrubbed)
        hits = _find_hits(scrubbed)
        if hits:
            rel = md_path.relative_to(SUBSYS)
            for kind, snippet in hits:
                failures.append(f"{rel}: {kind}: {snippet!r}")
    assert not failures, (
        "Hardcoded figures found in skill prose (outside fenced code blocks and "
        "outside Example-outputs sections). Every numeric figure must live in the "
        "reference layer per DESIGN_RULES rule 1.\n\n" + "\n".join(failures)
    )
