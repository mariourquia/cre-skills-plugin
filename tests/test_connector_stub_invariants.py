"""Top-level connector no-live invariants (CI-runnable).

The richer connector contract tests live under
src/skills/residential_multifamily/tests/, but CI runs `pytest tests/`, which does
NOT collect that subtree (the testpaths in pyproject.toml restrict a bare pytest,
and the CLI path overrides them). This file pins the load-bearing no-live
guarantees at the TOP level so a "looks live" regression cannot ship through CI:

  - every connector DOMAIN manifest stays status:stub (the connector_manifest
    schema permits 'stable', and nothing else asserts the value);
  - every ADAPTER manifest stays status:stub;
  - no domain entity declares source_class: connector_live;
  - the connector source_class enum matches its canonical list (order-included).

Note on auth_kind: several stub connectors declare a future auth_kind (api_key,
sftp) — that is a forward declaration of the INTENDED adapter auth, not a
liveness signal. Liveness is governed solely by `status: stub` + no live adapter,
which the tests below pin; auth_kind alone never makes a stub connector live.
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONN = REPO_ROOT / "src" / "skills" / "residential_multifamily" / "reference" / "connectors"


def _domain_manifests():
    return [p for p in sorted(CONN.glob("*/manifest.yaml")) if not p.parent.name.startswith("_")]


def _adapter_manifests():
    return sorted((CONN / "adapters").glob("*/manifest.yaml"))


def _load(p):
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def test_every_connector_domain_manifest_is_stub():
    mans = _domain_manifests()
    assert mans, "no connector domain manifests found"
    bad = [f"{p.parent.name}: status={_load(p).get('status')!r}"
           for p in mans if _load(p).get("status") != "stub"]
    assert not bad, "connector domain manifests not stub:\n  " + "\n  ".join(bad)


def test_every_adapter_manifest_is_stub():
    mans = _adapter_manifests()
    assert mans, "no adapter manifests found"
    bad = [f"{p.parent.name}: status={_load(p).get('status')!r}"
           for p in mans if _load(p).get("status") != "stub"]
    assert not bad, "adapter manifests not stub:\n  " + "\n  ".join(bad)


def test_no_entity_declares_connector_live():
    """No domain file may ASSIGN source_class: connector_live (the enum definition
    in _schema/ legitimately lists it as an allowed value; domain entities must
    not select it)."""
    bad = []
    for dom in _domain_manifests():
        for f in list(dom.parent.glob("*.yaml")) + list(dom.parent.glob("*.json")):
            text = f.read_text(encoding="utf-8")
            if ("source_class: connector_live" in text
                    or '"source_class": "connector_live"' in text):
                bad.append(str(f.relative_to(CONN)))
    assert not bad, "entity declares source_class: connector_live:\n  " + "\n  ".join(bad)


def test_connector_source_class_enum_matches_canonical_list():
    canonical = yaml.safe_load(
        (CONN / "_schema" / "source_class.yaml").read_text(encoding="utf-8")
    )["source_class_values"]
    schema = yaml.safe_load(
        (CONN / "_schema" / "entity_contract.schema.yaml").read_text(encoding="utf-8")
    )
    enum = schema["properties"]["source_class"]["enum"]
    assert enum == canonical, (
        f"connector source_class enum {enum} != canonical {canonical} (order-included)"
    )
