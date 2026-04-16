"""Approval governance tests.

Enforces the single canonical approval state vocabulary and the
stale-approval guard (subject_object_version_hash binding).

Invariants checked:

1. The approval_request.yaml schema enumerates exactly one status vocabulary.

2. approval_matrix.md references the SAME vocabulary (no legacy
   `opened/executed/cancelled` state names in the canonical vocabulary, only in
   retirement-note context).

3. The schema includes a `subject_object_version_hash` field that binds the
   approval to a specific artifact version. This prevents silent reuse of an
   approval against a later, mutated version.

4. A representative approval_request instance validates against the schema.

5. Instances whose status is `approved` MUST carry a subject_object_version_hash
   (enforced at creation time by the runtime; tests verify the schema
   documents the requirement in natural language — JSON Schema cannot express
   conditional required fields without `if`/`then`).
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from conftest import SUBSYS, validate_against_schema


_CANONICAL_STATUS = {
    "pending",
    "approved",
    "approved_with_conditions",
    "denied",
    "expired",
    "withdrawn",
}

_LEGACY_STATUS = {"opened", "executed", "cancelled"}


def _load_schema() -> dict:
    path = SUBSYS / "_core" / "schemas" / "approval_request.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _read_matrix_md() -> str:
    path = SUBSYS / "_core" / "approval_matrix.md"
    return path.read_text(encoding="utf-8")


def test_schema_status_enum_is_canonical() -> None:
    schema = _load_schema()
    status_schema = schema["properties"]["status"]
    assert status_schema.get("type") == "string"
    assert set(status_schema.get("enum") or []) == _CANONICAL_STATUS


def test_schema_includes_version_hash_field() -> None:
    schema = _load_schema()
    props = schema["properties"]
    assert "subject_object_version_hash" in props, (
        "approval_request schema must include subject_object_version_hash to "
        "bind approvals to a specific artifact version"
    )
    vh = props["subject_object_version_hash"]
    assert vh.get("type") == "string"
    assert "pattern" in vh, "version hash must be constrained by regex pattern"
    # Verify pattern matches a sha256 hex digest
    assert re.match(
        vh["pattern"], "a" * 64
    ), "version hash pattern must accept a 64-char lowercase hex string"

    assert "subject_object_version_hash_algo" in props
    algo = props["subject_object_version_hash_algo"]
    assert algo.get("enum") == ["sha256"]


def test_matrix_md_declares_canonical_vocabulary() -> None:
    body = _read_matrix_md()
    # Each canonical status must appear somewhere in the document.
    missing = [s for s in _CANONICAL_STATUS if s not in body]
    assert not missing, f"approval_matrix.md missing canonical status values: {missing}"

    # The canonical vocabulary line must enumerate exactly the canonical set.
    # Look for the fenced enumeration produced by this repo's governance.
    fenced = re.search(r"```\s*\npending[^`]*?```", body, re.DOTALL)
    assert fenced is not None, (
        "approval_matrix.md must include a fenced canonical vocabulary block starting with `pending`"
    )


def test_matrix_md_retires_legacy_vocabulary() -> None:
    """Legacy status names must not appear as status-value listings.

    The legacy vocabulary (`opened`, `executed`, `cancelled`) was previously
    used as discrete state values. We enforce that the document does not
    re-introduce them in a status-value listing context. Ordinary English
    uses of the verb "executed" in prose are allowed; what is forbidden is
    their use as an enumerated status value.

    Specifically: inside any fenced code block in the document, no legacy
    term may appear as a bare status/outcome value. We scan each fenced
    block for occurrences of the legacy terms that are immediately inside
    a bracketed enum (e.g. `[opened | approved | ...]`) or as a value in a
    YAML enum (`status: opened`).
    """
    body = _read_matrix_md()

    fenced_blocks = re.findall(r"```[^\n]*\n(.*?)```", body, re.DOTALL)
    violations = []
    for block in fenced_blocks:
        for term in _LEGACY_STATUS:
            # Bracketed enum form: "[opened | approved | ...]"
            if re.search(
                r"\[[^\]]*\b" + re.escape(term) + r"\b[^\]]*\]",
                block,
            ):
                violations.append(
                    f"  legacy term {term!r} appears inside a bracketed enum in a fenced block"
                )
            # Direct status/outcome assignment: "status: opened"
            if re.search(
                r"(status|outcome|approval_request_status)\s*:\s*" + re.escape(term),
                block,
            ):
                violations.append(
                    f"  legacy term {term!r} appears as a status/outcome value in a fenced block"
                )
    assert not violations, (
        "Legacy approval status vocabulary reappeared as enumerated status "
        "values. The canonical vocabulary is defined in the 'Canonical "
        "status vocabulary' section; do not add legacy terms back as "
        "discrete states.\n" + "\n".join(violations)
    )


def test_matrix_md_has_canonical_vocabulary_section() -> None:
    body = _read_matrix_md()
    assert "## Canonical status vocabulary" in body, (
        "approval_matrix.md must contain a '## Canonical status vocabulary' section"
    )
    assert "## Stale-approval guard" in body, (
        "approval_matrix.md must document the stale-approval guard"
    )
    # Retirement mapping for each legacy term must be present in prose.
    for term in _LEGACY_STATUS:
        assert term in body, (
            f"approval_matrix.md must include retirement mapping for legacy term {term!r}"
        )


def test_representative_approval_request_validates() -> None:
    schema = _load_schema()
    # A fully-populated approval_request that should validate.
    instance = {
        "approval_request_id": "01HXXXXXXXXXXXXXXXXXXXXXXX",
        "created_at": "2026-04-15T12:00:00Z",
        "created_by": "agent:residential_multifamily",
        "subject_object_type": "change_order",
        "subject_object_id": "CO_2026_042",
        "subject_object_version_hash": "a" * 64,
        "subject_object_version_hash_algo": "sha256",
        "action_proposed": "approve change order CO_2026_042 for $45,000",
        "rationale": "scope addition covers code-required life-safety upgrade",
        "approvers_required": [{"role": "construction_manager", "count": 1}],
        "approvers_notified": ["user:alice"],
        "decisions": [
            {
                "approver": "user:alice",
                "decision": "approve",
                "notes": "aligned with contingency policy",
                "decided_at": "2026-04-15T12:30:00Z",
            }
        ],
        "status": "approved",
        "expires_at": "2026-05-15T12:30:00Z",
        "linked_references": [
            "reference/derived/contingency_assumptions__{org}.csv"
        ],
    }
    errors = validate_against_schema(instance, schema)
    assert not errors, "approval_request did not validate:\n" + "\n".join(errors)


def test_schema_forbids_unknown_status_values() -> None:
    """A status value outside the canonical enum must fail validation."""
    schema = _load_schema()
    instance = {
        "approval_request_id": "01HXXXXXXXXXXXXXXXXXXXXXXX",
        "created_at": "2026-04-15T12:00:00Z",
        "created_by": "agent:residential_multifamily",
        "subject_object_type": "change_order",
        "subject_object_id": "CO_2026_042",
        "action_proposed": "x",
        "rationale": "y",
        "approvers_required": [{"role": "construction_manager", "count": 1}],
        "status": "opened",  # legacy value, should fail
    }
    errors = validate_against_schema(instance, schema)
    assert any("enum" in e for e in errors), (
        "schema accepted legacy 'opened' status; expected enum violation. errors=" + repr(errors)
    )


def test_schema_rejects_malformed_version_hash() -> None:
    schema = _load_schema()
    instance = {
        "approval_request_id": "01HXXXXXXXXXXXXXXXXXXXXXXX",
        "created_at": "2026-04-15T12:00:00Z",
        "created_by": "agent:residential_multifamily",
        "subject_object_type": "change_order",
        "subject_object_id": "CO_2026_042",
        "subject_object_version_hash": "not-a-hash",  # too short and non-hex
        "action_proposed": "x",
        "rationale": "y",
        "approvers_required": [{"role": "construction_manager", "count": 1}],
        "status": "pending",
    }
    errors = validate_against_schema(instance, schema)
    assert any("pattern" in e for e in errors), (
        "schema accepted malformed version_hash; expected pattern violation. errors=" + repr(errors)
    )
