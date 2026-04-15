"""Change-log tests.

- Asserts CHANGELOG.md exists at the subsystem root.
- If reference/archives/change_log.jsonl exists, validates every line against the
  change_log_entry schema. An empty file is acceptable for Phase 1.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from conftest import SUBSYS, validate_against_schema


def test_subsystem_changelog_exists():
    # Either a CHANGELOG.md at the subsystem root, or an equivalent inside _core.
    candidates = [
        SUBSYS / "CHANGELOG.md",
        SUBSYS / "_core" / "CHANGELOG.md",
    ]
    present = [c for c in candidates if c.exists()]
    assert present, (
        f"Expected a CHANGELOG.md at one of {[str(c) for c in candidates]}; "
        f"none found."
    )


def test_change_log_jsonl_if_present_validates(change_log_entry_schema):
    jsonl_path = SUBSYS / "reference" / "archives" / "change_log.jsonl"
    if not jsonl_path.exists():
        # Phase 1: archive may not exist yet.
        return
    errors: List[str] = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                entry: Dict[str, Any] = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{jsonl_path.relative_to(SUBSYS)}:{lineno}: invalid json: {exc}")
                continue
            line_errors = validate_against_schema(
                entry, change_log_entry_schema, path=f"{jsonl_path.name}:{lineno}"
            )
            errors.extend(line_errors)
    assert not errors, "\n".join(errors)
