"""v5 micro-skill classification + governance enforcement.

Companion to the v5 architecture (docs/architecture/v5-micro-skill-architecture.md,
especially §4 validation rules and §10 the AUTHORITATIVE post-review revisions).

This is the REAL validator the spec calls for in §10/M-A2: extending the schema
alone protects nothing, so this module

  1. jsonschema-validates EVERY item in dist/catalog.json against the
     ``CatalogItem`` subschema of src/catalog/catalog.schema.json (nothing did
     this before — the schema was unenforced); and
  2. enforces the §4 governance rules on an explicit ALLOWLIST of decision-grade
     and AMOS-facing slugs (§10/M-D1 — membership enforcement, not field
     presence, so an omission on a listed slug is a CI failure while
     non-listed skills stay advisory and the suite stays honest about scope).

The catalog is the generated source of truth (run scripts/catalog-build.py).
Frontmatter is read directly (NOT via the catalog) only where the rule is about
a frontmatter field the catalog does not project (refusal_trigger,
calculator_bridge), mirroring tests/test_skill_v5_contract.py so a stale catalog
cannot mask a missing frontmatter field.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_JSON = REPO_ROOT / "dist" / "catalog.json"
SCHEMA_PATH = REPO_ROOT / "src" / "catalog" / "catalog.schema.json"
SKILLS_ROOT = REPO_ROOT / "src" / "skills"
CALCULATOR_REGISTRY = REPO_ROOT / "scripts" / "calculator-registry.json"


# ---------------------------------------------------------------------------
# Allowlists (§10/M-D1). These are the v5 pilot: the 8 priority skills plus the
# decision-grade / AMOS-facing slugs that v5.0.0 commits to. Membership here is
# load-bearing: a listed slug MISSING its governance metadata is a CI failure.
# ---------------------------------------------------------------------------
DECISION_GRADE_SLUGS = {
    "amos-icomm-demo-orchestrator",
    "acquisition-underwriting-engine",
    "ic-memo-generator",
    "fund-lp-reporting",
    "jv-waterfall-architect",
    "comp-snapshot",
    "opportunity-zone-underwriter",
    "cost-segregation-analyzer",
}

AMOS_FACING_SLUGS = {
    "amos-icomm-demo-orchestrator",
    "document-to-database",
    "document-to-warehouse-pipeline",
    "acquisition-underwriting-engine",
    "ic-memo-generator",
    "comp-snapshot",
    "fund-lp-reporting",
}

# Subsystem routers whose decomposition is internal (taxonomy/routing packs or
# runtime engine phases), NOT a flat list of catalog skill ids. They are
# explicitly exempt from rule §4.1's non-empty `decomposes_to` requirement
# (the spec authorizes this exemption for subsystem routers; see §5 RMF row,
# §9/A2, and §10). residential_multifamily routes via its taxonomy axes; the
# `type: orchestrator` engine configs declare runtime `phases`; `type: workflow`
# chains are documented routing descriptions. None of these present as atomic
# tools, which is what rule §4.1 actually guards against.
SUBSYSTEM_ROUTER_EXEMPT_IDS = {"residential_multifamily"}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def _load_catalog() -> Dict:
    assert CATALOG_JSON.exists(), (
        "dist/catalog.json missing — run scripts/catalog-build.py first."
    )
    return json.loads(CATALOG_JSON.read_text(encoding="utf-8"))


def _load_item_schema() -> Dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return schema["$defs"]["CatalogItem"]


def _items() -> List[Dict]:
    return _load_catalog().get("items", [])


def _items_by_id() -> Dict[str, Dict]:
    return {i["id"]: i for i in _items()}


def _skill_frontmatter(slug: str) -> Dict:
    """Parse the frontmatter of src/skills/<slug>/SKILL.md (direct, not catalog)."""
    path = SKILLS_ROOT / slug / "SKILL.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}
    data = yaml.safe_load(text[4:end]) or {}
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------------------
# (M-A2 part a) Schema enforcement — every catalog item validates
# ---------------------------------------------------------------------------
def test_every_catalog_item_validates_against_schema():
    item_schema = _load_item_schema()
    failures: List[str] = []
    for item in _items():
        try:
            jsonschema.validate(item, item_schema)
        except jsonschema.ValidationError as exc:
            failures.append(f"{item.get('id', '<no-id>')} ({item.get('type')}): {exc.message}")
    assert not failures, (
        "Catalog items violate src/catalog/catalog.schema.json CatalogItem:\n  "
        + "\n  ".join(failures)
    )


def test_new_v5_fields_present_on_every_item():
    """catalog-build.py must EMIT the eight governance keys onto every item
    (§10/M-A1) — without emission the rules below are vacuous."""
    required = (
        "classification", "runtime_role", "decision_grade", "human_gate",
        "source_ref_policy", "amos_surface", "decomposes_to", "composed_from",
    )
    missing: List[str] = []
    for item in _items():
        for key in required:
            if key not in item:
                missing.append(f"{item['id']}: missing '{key}'")
    assert not missing, "Catalog items missing v5 governance keys:\n  " + "\n  ".join(missing)


# ---------------------------------------------------------------------------
# (M-A2 part b) §4 governance rules
# ---------------------------------------------------------------------------
def test_decision_grade_slugs_are_gated():
    """§4.2 on the allowlist (§10/M-D1): every DECISION_GRADE slug's catalog
    item has decision_grade true, a real human_gate, and a source_ref_policy."""
    by_id = _items_by_id()
    failures: List[str] = []
    for slug in sorted(DECISION_GRADE_SLUGS):
        item = by_id.get(slug)
        if item is None:
            failures.append(f"{slug}: not present in catalog")
            continue
        if item.get("decision_grade") is not True:
            failures.append(f"{slug}: decision_grade must be true (frontmatter final_marked: true)")
        if item.get("human_gate", "none") == "none":
            failures.append(f"{slug}: decision-grade skill must declare human_gate != none")
        if not item.get("source_ref_policy"):
            failures.append(f"{slug}: decision-grade skill must declare source_ref_policy")
    assert not failures, "decision-grade governance violations:\n  " + "\n  ".join(failures)


def test_amos_facing_slugs_are_source_grounded_and_fail_closed():
    """§4.3 on the allowlist: every AMOS_FACING slug has a non-empty
    source_ref_policy AND a refusal_trigger in its SKILL.md frontmatter."""
    by_id = _items_by_id()
    failures: List[str] = []
    for slug in sorted(AMOS_FACING_SLUGS):
        item = by_id.get(slug)
        if item is None:
            failures.append(f"{slug}: not present in catalog")
            continue
        srp = item.get("source_ref_policy")
        if not srp or not srp.get("emits"):
            failures.append(f"{slug}: AMOS-facing skill must declare a non-empty source_ref_policy.emits")
        fm = _skill_frontmatter(slug)
        rt = fm.get("refusal_trigger")
        if not (isinstance(rt, str) and rt.strip()):
            failures.append(f"{slug}: AMOS-facing skill must declare a refusal_trigger in SKILL.md frontmatter")
    assert not failures, "AMOS-facing governance violations:\n  " + "\n  ".join(failures)


def test_source_ref_policy_shape_when_present():
    """§10/M-D2: source_ref_policy is an OBJECT with emits (list),
    on_unresolvable (enum), forbids_fabricated_model_ref (bool)."""
    valid_unresolvable = {"refuse", "warn", "cite_best_effort"}
    failures: List[str] = []
    for item in _items():
        srp = item.get("source_ref_policy")
        if srp is None:
            continue
        if not isinstance(srp, dict):
            failures.append(f"{item['id']}: source_ref_policy must be an object or null")
            continue
        if not isinstance(srp.get("emits"), list):
            failures.append(f"{item['id']}: source_ref_policy.emits must be a list")
        if srp.get("on_unresolvable") not in valid_unresolvable:
            failures.append(f"{item['id']}: source_ref_policy.on_unresolvable must be one of {sorted(valid_unresolvable)}")
        if not isinstance(srp.get("forbids_fabricated_model_ref"), bool):
            failures.append(f"{item['id']}: source_ref_policy.forbids_fabricated_model_ref must be bool")
    assert not failures, "source_ref_policy shape violations:\n  " + "\n  ".join(failures)


def test_orchestrator_and_workspace_declare_decomposition():
    """§4.1: classification in {orchestrator, workspace} => decomposes_to
    non-empty, so a conductor/router never presents as an atomic tool. Subsystem
    routers (RMF, runtime engine configs, workflow chains) are explicitly
    exempt — their decomposition is internal, not a flat catalog-skill list."""
    failures: List[str] = []
    for item in _items():
        cls = item.get("classification")
        if cls not in {"orchestrator", "workspace"}:
            continue
        if item["id"] in SUBSYSTEM_ROUTER_EXEMPT_IDS:
            continue
        # The runtime orchestrator engine configs (type: orchestrator) and the
        # documented workflow chains (type: workflow) are subsystem routers too.
        if item.get("type") in {"orchestrator", "workflow"}:
            continue
        if not item.get("decomposes_to"):
            failures.append(
                f"{item['id']} (classification={cls}): must declare a non-empty "
                f"decomposes_to (or be an explicit subsystem-router exemption)"
            )
    assert not failures, "orchestrator/workspace decomposition violations:\n  " + "\n  ".join(failures)


def test_decompose_and_compose_ids_resolve():
    """§4.5: every id in decomposes_to / composed_from resolves to a real
    catalog item id — CI fails on a dangling id (§9/A3)."""
    ids = set(_items_by_id())
    failures: List[str] = []
    for item in _items():
        for field in ("decomposes_to", "composed_from"):
            for ref in item.get(field, []):
                if ref not in ids:
                    failures.append(f"{item['id']}.{field} -> '{ref}' does not resolve to a catalog item")
    assert not failures, "dangling decompose/compose references:\n  " + "\n  ".join(failures)


def test_calculator_bridge_slugs_resolve():
    """§4.4: every calculator_bridge slug (read from SKILL.md frontmatter)
    resolves to a real calculator in scripts/calculator-registry.json."""
    reg = json.loads(CALCULATOR_REGISTRY.read_text(encoding="utf-8"))
    calcs = reg.get("calculators", {})
    known = set(calcs.keys()) if isinstance(calcs, dict) else {
        (c.get("slug") or c.get("id") or c.get("name")) for c in calcs
    }
    failures: List[str] = []
    for skill_dir in sorted(SKILLS_ROOT.iterdir()):
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
            continue
        fm = _skill_frontmatter(skill_dir.name)
        for slug in fm.get("calculator_bridge") or []:
            if slug not in known:
                failures.append(f"{skill_dir.name}: calculator_bridge '{slug}' not in calculator-registry.json")
    assert not failures, "unresolved calculator_bridge slugs:\n  " + "\n  ".join(failures)


def test_amos_surface_values_are_valid():
    """amos_surface entries are AMOS RoomTabKey + landing (§3, §10/M-AM1)."""
    allowed = {"model", "leasing", "t12", "debt", "market", "diligence",
               "sources", "memo", "feedback", "decision", "landing"}
    failures: List[str] = []
    for item in _items():
        for surface in item.get("amos_surface", []):
            if surface not in allowed:
                failures.append(f"{item['id']}: invalid amos_surface '{surface}'")
    assert not failures, "invalid amos_surface values:\n  " + "\n  ".join(failures)


def test_allowlists_are_classified_in_pilot():
    """Every allowlisted slug exists, has a classification, and (for the
    decision-grade set) carries a refusal_trigger — they are the v5 pilot, so an
    un-annotated member is a setup error, not an advisory miss."""
    by_id = _items_by_id()
    failures: List[str] = []
    for slug in sorted(DECISION_GRADE_SLUGS | AMOS_FACING_SLUGS):
        item = by_id.get(slug)
        if item is None:
            failures.append(f"{slug}: allowlisted but absent from catalog")
            continue
        if not item.get("classification"):
            failures.append(f"{slug}: allowlisted but has no classification")
    for slug in sorted(DECISION_GRADE_SLUGS):
        fm = _skill_frontmatter(slug)
        rt = fm.get("refusal_trigger")
        if not (isinstance(rt, str) and rt.strip()):
            failures.append(f"{slug}: decision-grade pilot skill missing refusal_trigger")
    assert not failures, "v5 pilot annotation gaps:\n  " + "\n  ".join(failures)
