"""PII classification, pseudonymization, and leak scanning.

The executable ingestion layer must be NO WEAKER than the prose layer it sits
beneath. It mirrors the hard-stop boundary in
``src/skills/document-to-data-room-extractor/references/pii-redaction-policy.yaml``:

- natural-person names, per-unit actual rent tied to a named person, guarantor
  / signatory names, SSNs, and bank routing/account numbers are NEVER emitted
  as values. The unit/tenant grain is kept, but identities are pseudonymized
  (``Tenant A``, a salted unit hash); a verbatim ``source_text_span`` is only
  ever retained for non-PII fields (the locator -- cell address -- is kept for
  PII fields, never the value).
- a detected leak is a CRITICAL, non-overridable grade failure (see
  ``rubric.CRITICAL_FAILURES``), mirroring the policy's hard_stop semantics:
  halt, report the offending field ids (never their values), do not deliver a
  partially redacted payload.

stdlib-only; no value is ever printed by these helpers.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

PII_POLICY_PATH = "src/skills/document-to-data-room-extractor/references/pii-redaction-policy.yaml"

# Mirrors pii-redaction-policy.yaml never_emit. Parity enforced by the sync test.
NEVER_EMIT = {
    "natural_person": (
        "tenant_individual_name",
        "guarantor_name",
        "signatory_name",
        "occupant_name",
        "emergency_contact",
    ),
    "identifiers": ("ssn", "ein_of_natural_person", "drivers_license_number", "passport_number"),
    "contact": ("personal_phone", "personal_email", "notice_address_of_individual"),
    "financial": (
        "bank_routing_number",
        "bank_account_number",
        "credit_score",
        "guarantor_personal_balance_sheet_detail",
        "personal_tax_return_figures",
    ),
    "rent_roll_unit_level": (
        "per_unit_tenant_name",
        "per_unit_actual_rent",
        "per_unit_lease_dates_tied_to_named_person",
        "named_delinquency",
    ),
}

# Field-name substrings that classify a field as carrying PII (the value must
# not be emitted verbatim). Maps substring -> pii_class.
_FIELD_CLASS_RULES = (
    ("natural_person", ("tenant_name", "resident_name", "occupant", "guarantor", "signatory", "contact_name", "lessee_name")),
    ("identifier", ("ssn", "tax_id", "ein", "license", "passport")),
    ("contact", ("phone", "email", "notice_address", "mailing_address")),
    ("financial", ("bank_account", "routing", "credit_score")),
)

# Shapes used to catch obviously-sensitive VALUES leaking into output.
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_BANK_RE = re.compile(r"\b\d{9,17}\b")


def classify_field(field_name: str) -> str:
    """Return the pii_class for a field name: one of natural_person |
    identifier | contact | financial | aggregate_safe."""
    low = (field_name or "").strip().lower()
    for pii_class, needles in _FIELD_CLASS_RULES:
        for needle in needles:
            if needle in low:
                return pii_class
    return "aggregate_safe"


def is_pii_field(field_name: str) -> bool:
    return classify_field(field_name) != "aggregate_safe"


def pseudonymize(natural_value: str, run_id: str, prefix: str = "Tenant") -> str:
    """Deterministic, salted pseudonym. The same value within one run maps to a
    stable token; the salt is the run_id so tokens are not trivially linkable
    across exports unless the consumer reuses the run_id."""
    salt = str(run_id or "RUN-UNSET")
    digest = hashlib.sha256((salt + "|" + str(natural_value)).encode("utf-8")).hexdigest()
    # 6 hex chars -> short, stable, opaque label.
    return "%s %s" % (prefix, digest[:6].upper())


def assert_safe_tenant_id(tenant_id: Any) -> list:
    """Path-safety validation for the tenancy label (ports
    assertSafeWorkspaceId semantics from src/mcp-server.mjs). Returns error
    strings; never raises. The label is NOT an auth token."""
    errs: list = []
    if tenant_id in (None, ""):
        errs.append("tenant_id/workspace_id is required (a tenancy label, not an auth token).")
        return errs
    s = str(tenant_id)
    if "/" in s or "\\" in s or ".." in s:
        errs.append("tenant_id must not contain '/', '\\\\', or '..' (no path components).")
    if len(s) > 128:
        errs.append("tenant_id too long (max 128 chars).")
    return errs


def scan_for_leaks(payload: Any, banned_values: list) -> list:
    """Walk a JSON-able structure and return the field PATHS whose value
    contains any banned synthetic-PII value or matches an SSN/bank shape.
    Returns PATHS ONLY -- never the offending value -- mirroring hard_stop
    (report leaking field ids, not their contents)."""
    banned = [str(b) for b in (banned_values or []) if b not in (None, "")]
    hits: list = []

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + "." + str(k) if path else str(k))
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                walk(v, path + "[" + str(i) + "]")
        elif isinstance(node, str):
            for b in banned:
                if b and b in node:
                    hits.append(path)
                    return
            if _SSN_RE.search(node) or _BANK_RE.search(node):
                hits.append(path)

    walk(payload, "")
    # de-dup, stable order
    seen: set = set()
    out: list = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out


def hard_stop(payload: Any, banned_values: list) -> dict:
    """The fail-closed gate. If any banned value or sensitive shape leaks,
    return a halt directive naming the field paths (never the values)."""
    leaks = scan_for_leaks(payload, banned_values)
    return {
        "ok": not leaks,
        "leaking_field_paths": leaks,
        "directive": (
            "Halt emission; do not deliver a partially redacted payload."
            if leaks
            else "clear"
        ),
    }
