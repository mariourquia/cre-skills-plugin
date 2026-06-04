"""Targeted finance-placeholder discipline guard (v5.0.0 — §10/M-G1).

This is a HONEST, TARGETED guard. It is a **presence-of-discipline check on a
named allowlist**, NOT a runtime scanner of emitted output. The fully
generalized, corpus-wide runtime data scanner (every cell of every skill checked
at emit time) is a v5.1 item; v5.0.0 ships the `residential_multifamily`
subsystem's deployed runtime enforcement (executive output contract +
fallback_resolver + period-seal) PLUS this named-allowlist discipline guard.

For each finance-critical, decision-grade skill on the allowlist, this asserts the
SKILL.md body:

  1. carries a ``## Refusal Behavior`` section; and
  2. states explicitly that unresolved ``$X`` / placeholder tokens must NOT appear
     in a final-marked output (they must resolve to a real value or the output
     refuses).

It also asserts the valuation / comp skills carry the "estimate, not an
appraisal" stamp (per 2026 case law distinguishing AI valuation estimates from
professional appraisals — see docs/plans/v5-analysis/06-security-governance.md B5
and docs/DATA_GRADES.md §4).

Enumerates the filesystem directly (NOT registry.yaml / catalog), so a stale
catalog cannot mask a missing discipline statement. This file does NOT weaken any
existing refusal / gate / preview control; it adds a presence assertion.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "src" / "skills"

# --------------------------------------------------------------------------- #
# Allowlist — the finance-critical, decision-grade slugs (§10/M-G1). Membership
# is load-bearing: a listed skill missing the discipline is a CI failure. This
# is the same finance-critical set the catalog classification allowlist gates,
# plus the WS-1a regulatory three (OZ, cost-seg) that already shipped it.
# --------------------------------------------------------------------------- #
FINANCE_PLACEHOLDER_ALLOWLIST = (
    "acquisition-underwriting-engine",
    "ic-memo-generator",
    "comp-snapshot",
    "fund-lp-reporting",
    "jv-waterfall-architect",
    "opportunity-zone-underwriter",
    "cost-segregation-analyzer",
)

# Valuation / comp skills that must additionally carry the "estimate, not an
# appraisal" stamp (B5 / DATA_GRADES §4).
NOT_AN_APPRAISAL_SLUGS = (
    "comp-snapshot",
    "om-reverse-pricing",
    "acquisition-underwriting-engine",
)

REFUSAL_SECTION = "## Refusal Behavior"

# The discipline statement must (a) name the placeholder/$X token shape AND
# (b) tie it to NOT appearing in a final-marked / final output. We match the
# intent flexibly so the prose can read naturally, but require both halves.
_PLACEHOLDER_TOKEN_RE = re.compile(r"(\$x\b|placeholder)", re.IGNORECASE)
_FINAL_MARKED_RE = re.compile(r"final[\s-]?marked|final\s+output|final\s+submission", re.IGNORECASE)
# A single sentence/line that ties an unresolved placeholder to a final output
# being forbidden. We scan the Refusal Behavior section line-by-line for a line
# that mentions the token AND (refuse|must not|never|block|forbidden) AND final.
_FORBID_RE = re.compile(
    r"(must not|never|may not|refuse|refus|block|forbid|withhold|shall not)",
    re.IGNORECASE,
)


def _split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return "", text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return "", text
    return text[4:end], text[end + 5:]


def _section(body: str, header: str) -> str:
    """Return the text of a ``## Header`` section (up to the next ``## `` or EOF)."""
    lines = body.splitlines()
    out: List[str] = []
    capturing = False
    for line in lines:
        if line.strip() == header:
            capturing = True
            continue
        if capturing and line.startswith("## "):
            break
        if capturing:
            out.append(line)
    return "\n".join(out)


def _read_body(slug: str) -> str:
    path = SKILLS_ROOT / slug / "SKILL.md"
    assert path.exists(), f"{slug}: SKILL.md not found at {path}"
    _, body = _split_frontmatter(path.read_text(encoding="utf-8"))
    return body


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_allowlisted_skills_exist():
    """Every allowlisted slug resolves to a real SKILL.md (setup guard)."""
    missing = [
        s for s in FINANCE_PLACEHOLDER_ALLOWLIST
        if not (SKILLS_ROOT / s / "SKILL.md").exists()
    ]
    assert not missing, "finance-placeholder allowlist references missing skills: " + ", ".join(missing)


def test_allowlisted_skills_have_refusal_behavior_section():
    """§10/M-G1: each finance-critical decision-grade skill carries a
    ``## Refusal Behavior`` section."""
    failures: List[str] = []
    for slug in FINANCE_PLACEHOLDER_ALLOWLIST:
        body = _read_body(slug)
        if REFUSAL_SECTION not in body:
            failures.append(f"{slug}: missing '{REFUSAL_SECTION}' section")
    assert not failures, "finance-placeholder refusal-section gaps:\n  " + "\n  ".join(failures)


def test_allowlisted_skills_forbid_unresolved_placeholder_in_final_output():
    """§10/M-G1: each listed skill states explicitly, inside its Refusal
    Behavior section, that an unresolved ``$X`` / placeholder token must not
    appear in a final-marked output (it must resolve to a real value or the
    output refuses)."""
    failures: List[str] = []
    for slug in FINANCE_PLACEHOLDER_ALLOWLIST:
        body = _read_body(slug)
        section = _section(body, REFUSAL_SECTION)
        if not section.strip():
            failures.append(f"{slug}: '{REFUSAL_SECTION}' section is empty")
            continue
        # Find a single line/sentence that ties placeholder + forbid + final.
        ok = False
        for chunk in re.split(r"(?<=[.;])\s+|\n", section):
            if (
                _PLACEHOLDER_TOKEN_RE.search(chunk)
                and _FORBID_RE.search(chunk)
                and _FINAL_MARKED_RE.search(chunk)
            ):
                ok = True
                break
        if not ok:
            failures.append(
                f"{slug}: Refusal Behavior must state that an unresolved $X/placeholder "
                f"token must not appear in a final-marked output"
            )
    assert not failures, "finance-placeholder discipline gaps:\n  " + "\n  ".join(failures)


def test_valuation_skills_carry_not_an_appraisal_stamp():
    """B5 / DATA_GRADES §4: valuation/comp skills carry the 'estimate, not an
    appraisal' stamp somewhere in the body (typically ## Confidence and
    Provenance)."""
    failures: List[str] = []
    for slug in NOT_AN_APPRAISAL_SLUGS:
        body = _read_body(slug).lower()
        if "not an appraisal" not in body:
            failures.append(f"{slug}: missing the 'not an appraisal' stamp")
    assert not failures, "valuation 'not an appraisal' stamp gaps:\n  " + "\n  ".join(failures)
