"""Integration-layer security artifact tests.

Validates the presence of the security and privacy documentation suite under
reference/connectors/_core/security/, and performs a coarse no-secrets-in-repo
scan across every file added by the integration layer.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

import pytest


SUBSYS = Path(__file__).resolve().parents[1]
SECURITY_ROOT = SUBSYS / "reference" / "connectors" / "_core" / "security"
CONNECTORS_ROOT = SUBSYS / "reference" / "connectors"

EXPECTED_SECURITY_DOCS = [
    "README.md",
    "security_model.md",
    "pii_classification.md",
    "secrets_handling.md",
    "masking_and_redaction.md",
    "config_templates.md",
    "pii_sample_policy.md",
    "fair_housing_controls.md",
    "legal_hold_and_retention.md",
    "audit_trail.md",
    "unsafe_defaults_registry.md",
    "approval_gates_for_integration_actions.md",
    "least_privilege_guidance.md",
    "config_overlay_interaction.md",
    "security_testing_guidance.md",
]

# Rough secret-ish patterns. Intentionally conservative: we expect zero hits
# across the integration-layer tree because every credential must stay out of
# the repo. Allow-list placeholder strings that operators carry forward.
SECRET_REGEX = re.compile(
    r"(?i)\b(aws_secret_access_key|aws_access_key_id|private[_-]?key|"
    r"begin\s+rsa\s+private|-----begin[\s\w]+private\s+key-----|"
    r"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9]{24,}|"
    r"secret\s*[:=]\s*['\"][A-Za-z0-9]{24,})"
)

ALLOWLIST_SUBSTRINGS = (
    "_placeholder",
    "placeholder",
    "<redacted>",
    "example",
    "sample",
    "stub",
    "template",
)


def test_security_family_present():
    missing = [
        str((SECURITY_ROOT / name).relative_to(SUBSYS))
        for name in EXPECTED_SECURITY_DOCS
        if not (SECURITY_ROOT / name).exists()
    ]
    assert not missing, "security doc family missing:\n  - " + "\n  - ".join(missing)


def test_security_docs_are_nonempty():
    failures: List[str] = []
    for name in EXPECTED_SECURITY_DOCS:
        p = SECURITY_ROOT / name
        if not p.exists():
            continue
        if p.stat().st_size < 400:
            failures.append(f"{p.relative_to(SUBSYS)}: suspiciously short")
    assert not failures, "security doc length check failed:\n  - " + "\n  - ".join(failures)


def test_no_secret_strings_in_integration_layer():
    """Walk the integration layer looking for high-confidence credential leak
    patterns. Allowlisted placeholder substrings short-circuit; anything else
    fails the test with a pointer."""
    hits: List[str] = []
    for path in CONNECTORS_ROOT.rglob("*"):
        if path.is_dir():
            continue
        if path.suffix not in {".yaml", ".yml", ".md", ".json", ".jsonl", ".py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in SECRET_REGEX.finditer(text):
            context = text[max(0, match.start() - 40): match.end() + 40].lower()
            if any(token in context for token in ALLOWLIST_SUBSTRINGS):
                continue
            hits.append(f"{path.relative_to(SUBSYS)}: match {match.group(0)!r}")
    assert not hits, "potential secrets detected:\n  - " + "\n  - ".join(hits)


def test_security_unsafe_defaults_registry_mentions_core_items():
    """Spot-check that the unsafe-defaults registry calls out the most
    important forbidden defaults."""
    text = (SECURITY_ROOT / "unsafe_defaults_registry.md").read_text(encoding="utf-8").lower()
    required_mentions = [
        "credential", "approval", "fair", "pii", "classification",
    ]
    missing = [t for t in required_mentions if t not in text]
    assert not missing, f"unsafe_defaults_registry.md missing mentions: {missing}"
