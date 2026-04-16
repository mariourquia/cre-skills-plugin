"""Placeholder/TBD scanner for reference data read by final-marked workflows.

See _core/reference_data_integrity.md for the rule. This test implements the
scanner and applies it to every reference path declared in the
reference_manifest.yaml of every final-marked workflow.

Failing this test means a reference row contains a placeholder token
(TBD, TODO, FIXME, XXX, PLACEHOLDER, TKTK) without any explicit
placeholder-label marker — a silent hole through which undetected
placeholder data could reach an executive / LP / lender / board
artifact.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

import yaml

from conftest import SUBSYS


_FM_PATH = SUBSYS / "_core" / "final_marked_workflows.yaml"

_PLACEHOLDER_TOKENS = {
    "TBD",
    "TODO",
    "FIXME",
    "XXX",
    "PLACEHOLDER",
    "TKTK",
    "TKTKTK",
}

_LABEL_COLUMNS: Dict[str, Set[str]] = {
    "status": {"placeholder", "tbd", "todo", "deferred"},
    "confidence": {"placeholder", "low_placeholder"},
    "source_type": {"placeholder"},
    "placeholder": {"true"},
    "placeholder_row": {"true"},
}


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _final_marked_slugs() -> List[str]:
    fm = _load_yaml(_FM_PATH).get("final_marked_workflows") or {}
    return list(fm.keys())


def _manifest_reads(slug: str) -> List[str]:
    manifest = SUBSYS / "workflows" / slug / "reference_manifest.yaml"
    if not manifest.exists():
        return []
    data = _load_yaml(manifest)
    return [r["path"] for r in (data.get("reads") or []) if isinstance(r, dict) and r.get("path")]


def _resolve_paths(raw_path: str) -> List[Path]:
    """Resolve a manifest path, expanding {market}/{org}/etc templates.

    If the path contains a curly-brace template, treat as a glob substitution —
    scan every concrete file that matches the templated prefix. A path with no
    concrete match simply yields no files and the scanner skips it (that is
    the job of test_reference_manifests to catch).
    """
    abs_root = SUBSYS
    if "{" not in raw_path:
        return [abs_root / raw_path] if (abs_root / raw_path).exists() else []
    # Replace {anything} with a * glob
    import re

    glob_pattern = re.sub(r"\{[^}]+\}", "*", raw_path)
    return list(abs_root.glob(glob_pattern))


def _row_has_label(row: Dict[str, str]) -> bool:
    for col_name, allowed_values in _LABEL_COLUMNS.items():
        val = (row.get(col_name) or "").strip().lower()
        if val in allowed_values:
            return True
    return False


def _row_has_placeholder_token(row: Dict[str, str]) -> bool:
    for _, val in row.items():
        if not isinstance(val, str):
            continue
        tokens_in_cell = {
            tok.strip(".,;:\"'()[]{}").upper()
            for tok in val.split()
            if tok
        }
        if tokens_in_cell & _PLACEHOLDER_TOKENS:
            return True
    return False


def scan_csv_file(path: Path) -> List[Tuple[int, Dict[str, str]]]:
    """Return list of (line_number, row) for rows with unlabeled placeholders."""
    offenses: List[Tuple[int, Dict[str, str]]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # line 1 is header
            if _row_has_placeholder_token(row) and not _row_has_label(row):
                offenses.append((idx, row))
    return offenses


def test_scanner_flags_unlabeled_placeholder(tmp_path: Path) -> None:
    """Synthetic test — verify scanner correctness on crafted input."""
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "reference_id,value,unit,status\n"
        "row-001,TBD,ratio,approved\n"  # unlabeled placeholder — should flag
    )
    offenses = scan_csv_file(bad)
    assert len(offenses) == 1


def test_scanner_accepts_labeled_placeholder(tmp_path: Path) -> None:
    """Synthetic test — placeholder with explicit status label is fine."""
    ok = tmp_path / "ok.csv"
    ok.write_text(
        "reference_id,value,unit,status\n"
        "row-002,TBD,ratio,placeholder\n"  # labeled — OK
    )
    offenses = scan_csv_file(ok)
    assert offenses == []


def test_scanner_ignores_non_placeholder_rows(tmp_path: Path) -> None:
    """Synthetic test — real rows are never flagged."""
    ok = tmp_path / "real.csv"
    ok.write_text(
        "reference_id,value,unit,status\n"
        "row-003,0.75,ratio,approved\n"
        "row-004,1.25,x,approved\n"
    )
    assert scan_csv_file(ok) == []


def test_final_marked_workflow_refs_are_placeholder_clean() -> None:
    """Every CSV read by a final-marked workflow is placeholder-clean.

    Enforces _core/reference_data_integrity.md on the paths that matter.
    """
    failures: List[str] = []
    for slug in _final_marked_slugs():
        for raw_path in _manifest_reads(slug):
            for concrete in _resolve_paths(raw_path):
                if concrete.suffix.lower() != ".csv":
                    continue
                for line_no, row in scan_csv_file(concrete):
                    rel = concrete.relative_to(SUBSYS)
                    # Keep the message compact — first two columns of the row
                    cols = list(row.items())[:3]
                    preview = ", ".join(f"{k}={v!r}" for k, v in cols)
                    failures.append(
                        f"{slug} -> {rel}:{line_no}: unlabeled placeholder ({preview})"
                    )
    assert not failures, (
        "Unlabeled placeholder rows in finance-critical reference data. "
        "Either populate real values or label the row via one of: "
        "status=placeholder, confidence=placeholder, source_type=placeholder, "
        "placeholder=true. See _core/reference_data_integrity.md.\n  "
        + "\n  ".join(failures)
    )
