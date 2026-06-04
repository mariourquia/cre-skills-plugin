"""Guard: docs/COMPATIBILITY.md counts match the generated catalog.

The Component Availability table in docs/COMPATIBILITY.md advertises parenthetical
counts — "Skills (127)", "Agents (54)", "Calculators (21)", "Commands (11)",
"Orchestrators (10)". These had drifted (Skills (112), Calculators (12)) because
nothing checked them. This tiny guard ties each advertised count to the
type-count of dist/catalog.json (the generated source of truth), so the matrix
cannot silently go stale again.

Reads the catalog directly (the generated source of truth, run
scripts/catalog-build.py) and the doc text; no network, deterministic.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_JSON = REPO_ROOT / "dist" / "catalog.json"
COMPATIBILITY = REPO_ROOT / "docs" / "COMPATIBILITY.md"

# Map the doc's table label -> the catalog item `type` it counts.
LABEL_TO_TYPE = {
    "Skills": "skill",
    "Agents": "agent",
    "Calculators": "calculator",
    "Commands": "command",
    "Orchestrators": "orchestrator",
}


def _catalog_type_counts() -> Dict[str, int]:
    items = json.loads(CATALOG_JSON.read_text(encoding="utf-8")).get("items", [])
    counts: Dict[str, int] = {}
    for item in items:
        counts[item.get("type")] = counts.get(item.get("type"), 0) + 1
    return counts


def test_compatibility_counts_match_catalog():
    assert CATALOG_JSON.exists(), "dist/catalog.json missing — run scripts/catalog-build.py"
    text = COMPATIBILITY.read_text(encoding="utf-8")
    counts = _catalog_type_counts()
    failures = []
    for label, type_ in LABEL_TO_TYPE.items():
        # Match e.g. "Skills (127)" — the parenthetical count in the table cell.
        m = re.search(rf"\b{label}\s*\((\d+)\)", text)
        if not m:
            # The label may legitimately not advertise a count; skip if absent.
            continue
        advertised = int(m.group(1))
        expected = counts.get(type_, 0)
        if advertised != expected:
            failures.append(
                f"COMPATIBILITY.md '{label} ({advertised})' != catalog {type_} count {expected}"
            )
    assert not failures, "COMPATIBILITY.md count drift:\n  " + "\n  ".join(failures)
