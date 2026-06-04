#!/usr/bin/env python3
"""
catalog-build.py — Scan the repo and produce catalog/catalog.yaml.

This is the ONE-TIME backfill script that also serves as the ongoing
catalog refresh tool. It reads:
  - skills/*/SKILL.md frontmatter
  - agents/**/*.md frontmatter
  - commands/*.md frontmatter
  - scripts/calculators/*.py
  - orchestrators/configs/*.json
  - routing/CRE-ROUTING.md (workflow chains + intent triggers)
  - registry.yaml (chains_to/chains_from, priority, category)

And produces catalog/catalog.yaml — the canonical source of truth.

Usage:
    python scripts/catalog-build.py              # build catalog
    python scripts/catalog-build.py --validate   # validate existing catalog
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Optional: pyyaml
try:
    import yaml
except ImportError:
    print("ERROR: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"

# ---------------------------------------------------------------------------
# YAML frontmatter parser (no external deps beyond pyyaml)
# ---------------------------------------------------------------------------

def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def extract_first_heading(filepath: Path) -> str:
    """Extract the first # heading from a markdown file."""
    try:
        for line in filepath.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Registry loader
# ---------------------------------------------------------------------------

def load_registry() -> dict:
    """Load registry.yaml and index by slug."""
    reg_path = REPO_ROOT / "registry.yaml"
    if not reg_path.exists():
        return {}
    data = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    if not data or "skills" not in data:
        return {}
    return {s["slug"]: s for s in data["skills"]}


# ---------------------------------------------------------------------------
# Routing table parser (intent triggers)
# ---------------------------------------------------------------------------

def parse_routing_triggers() -> dict:
    """Parse CRE-ROUTING.md and return {slug: [trigger phrases]}."""
    routing_path = SRC_DIR / "routing" / "CRE-ROUTING.md"
    if not routing_path.exists():
        return {}
    triggers = {}
    for line in routing_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| User says") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        trigger_text = parts[1]
        slug_text = parts[2]
        slug_match = re.search(r"`/([a-z0-9-]+)`", slug_text)
        if not slug_match:
            continue
        slug = slug_match.group(1)
        phrases = [
            p.strip().strip('"').strip("'")
            for p in re.split(r'[,"]', trigger_text)
            if p.strip().strip('"').strip("'")
        ]
        triggers.setdefault(slug, []).extend(phrases)
    return triggers


def parse_workflow_chains() -> list:
    """Parse workflow chains from CRE-ROUTING.md."""
    routing_path = SRC_DIR / "routing" / "CRE-ROUTING.md"
    if not routing_path.exists():
        return []
    text = routing_path.read_text(encoding="utf-8")
    chains = []
    in_chains = False
    for line in text.splitlines():
        if "## Workflow Chains" in line:
            in_chains = True
            continue
        if in_chains and line.startswith("##"):
            break
        if in_chains and line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.")):
            match = re.match(r'\d+\.\s+\*\*(.+?)\*\*:\s*(.*)', line.strip())
            if match:
                name = match.group(1).strip()
                steps_text = match.group(2).strip()
                chain_id = name.lower().replace(" ", "-").replace("&", "and")
                steps = [
                    s.strip().strip("[]")
                    for s in re.split(r'\s*->\s*', steps_text)
                    if s.strip()
                ]
                chains.append({
                    "id": chain_id,
                    "display_name": name,
                    "steps": steps,
                })
    return chains


# ---------------------------------------------------------------------------
# Category -> lifecycle_phase mapping
# ---------------------------------------------------------------------------

CATEGORY_TO_PHASE = {
    "existing-deployed": "cross-cutting",
    "01-deal-screening": "screening",
    "02-underwriting-analysis": "underwriting",
    "03-deal-structuring": "structuring",
    "04-due-diligence": "due-diligence",
    "05-capital-markets": "capital-markets",
    "06-market-research": "market-research",
    "07-asset-management": "asset-management",
    "08-leasing": "leasing",
    "09-investor-relations": "investor-relations",
    "10-development": "development",
    "11-disposition": "disposition",
    "12-deal-sourcing": "sourcing",
    "13-tax-entity": "tax-entity",
    "14-esg-climate": "esg-climate",
    "15-portfolio-strategy": "portfolio-strategy",
    "16-daily-operations": "daily-operations",
    "legal": "legal",
    "closing": "closing",
    "investor-relations": "investor-relations",
}

STATUS_MAP = {
    "deployed": "stable",
    "planned": "stable",  # all planned items actually have SKILL.md files deployed
    "stub": "stub",
    "deprecated": "deprecated",
    "draft": "experimental",  # SKILL.md draft-status skills surface as experimental
    "experimental": "experimental",
}

AGENT_DOMAIN_MAP = {
    "research": "market-research",
    "disposition": "disposition",
    "lp": "investor-relations",
    "asset-management": "asset-management",
    "portfolio": "portfolio-strategy",
    "strategy": "portfolio-strategy",
    "fund": "fund-management",
}


# ---------------------------------------------------------------------------
# Skill -> calculator mapping
# ---------------------------------------------------------------------------

SKILL_CALCULATOR_MAP = {
    "deal-quick-screen": "src/calculators/quick_screen.py",
    "loan-sizing-engine": "src/calculators/debt_sizing.py",
    "debt-covenant-monitor": "src/calculators/covenant_tester.py",
    "lease-trade-out-analyzer": "src/calculators/npv_trade_out.py",
    "lease-option-structurer": "src/calculators/option_valuation.py",
    "jv-waterfall-architect": "src/calculators/waterfall_calculator.py",
    "tenant-credit-analyzer": "src/calculators/tenant_credit_scorer.py",
    "closing-checklist-tracker": "src/calculators/proration_calculator.py",
    "transfer-document-preparer": "src/calculators/transfer_tax.py",
    "monte-carlo-return-simulator": "src/calculators/monte_carlo_simulator.py",
    "fund-raise-negotiation-engine": "src/calculators/fund_fee_modeler.py",
    "construction-cost-estimator": "src/calculators/construction_estimator.py",
}


# ---------------------------------------------------------------------------
# v5 classification + governance metadata (see
# docs/architecture/v5-micro-skill-architecture.md §2, §3, §10/M-A1)
# ---------------------------------------------------------------------------

# True multi-phase conductors only (NOT every "command center" by name). The
# description-prefix heuristic below also catches conductors that open with
# "orchestrator"/"conductor"/"command center" but are not in this explicit set.
ORCHESTRATOR_SLUGS = {
    "amos-icomm-demo-orchestrator",
    "document-to-database",
    "document-to-warehouse-pipeline",
    "property-management-orchestrator",
    "sourcing-outreach-system",
}

# Frontmatter-overridable governance keys flowed verbatim into the catalog item.
_HUMAN_GATE_DEFAULT = "none"

# classification -> runtime_role default projection (§2). Frontmatter
# `runtime_role:` overrides this derived value.
CLASSIFICATION_TO_RUNTIME_ROLE = {
    "orchestrator": "workflow_conductor",
    "workspace": "workspace_router",
    "calculator": "deterministic_calculator",
    "agent": "agent_persona",
    "micro": "callable_tool",
    "normal": "callable_tool",
}


def derive_classification(slug: str, item_type: str, category: str,
                          pack_type, description: str) -> str:
    """Derive a default classification when frontmatter omits it (§2, §10).

    workspace  if category == 'workspace' or pack_type == 'router'
    orchestrator if slug in ORCHESTRATOR_SLUGS or description opens with a
                 conductor cue ('orchestrator'/'conductor'/'command center')
    calculator/agent mirror the item type
    else        normal
    """
    if item_type == "calculator":
        return "calculator"
    if item_type == "agent":
        return "agent"
    if category == "workspace" or pack_type == "router":
        return "workspace"
    if slug in ORCHESTRATOR_SLUGS:
        return "orchestrator"
    desc_lead = (description or "").strip().lower()
    if desc_lead.startswith(("orchestrator", "conductor", "command center")):
        return "orchestrator"
    return "normal"


def derive_runtime_role(classification: str) -> str:
    """Project classification -> runtime_role (§2). Overridable in frontmatter."""
    return CLASSIFICATION_TO_RUNTIME_ROLE.get(classification, "callable_tool")


def governance_from_frontmatter(fm: dict, slug: str, item_type: str,
                                category: str, pack_type, description: str) -> dict:
    """Read the v5 governance keys from frontmatter and apply derivation
    defaults for classification/runtime_role (§10/M-A1). Returns a dict of the
    eight catalog fields ready to merge into an item.

    `final_marked` (frontmatter, NOT renamed — §10/M-A3) projects to the catalog
    `decision_grade` field.
    """
    fm = fm or {}
    classification = fm.get("classification") or derive_classification(
        slug, item_type, category, pack_type, description
    )
    runtime_role = fm.get("runtime_role") or derive_runtime_role(classification)
    return {
        "classification": classification,
        "runtime_role": runtime_role,
        "decision_grade": bool(fm.get("final_marked", False)),
        "human_gate": fm.get("human_gate", _HUMAN_GATE_DEFAULT),
        "source_ref_policy": fm.get("source_ref_policy"),
        "amos_surface": fm.get("amos_surface") or [],
        "decomposes_to": fm.get("decomposes_to") or [],
        "composed_from": fm.get("composed_from") or [],
    }


# ---------------------------------------------------------------------------
# v5.2 consumer-contract forward-compat fields (produces_artifact_kind,
# pii_policy, workspace_scope, outputs). Derived with frontmatter override.
# These are rendering/consumer hints, NOT liability gates — the governance
# scanner keys liability rules off explicit governance fields, never these.
# See docs/integrations/amos-skill-manifest.md and
# docs/architecture/v5-micro-skill-architecture.md.
# ---------------------------------------------------------------------------

# Plugin-namespaced artifact kind -> human label, used to seed outputs[] when a
# skill declares no explicit `outputs:`. Keys MUST match the catalog/manifest
# `produces_artifact_kind` enum.
ARTIFACT_KIND_LABEL = {
    "memo": "Investment memo",
    "model_output": "Model output",
    "calculator_result": "Calculator result",
    "diligence_report": "Diligence report",
    "source_map": "Source map",
    "tie_out_report": "Tie-out report",
    "investor_report": "Investor report",
    "lender_package": "Lender package",
    "valuation_support": "Valuation support",
    "checklist": "Checklist",
    "workflow_plan": "Workflow plan",
    "advisory_note": "Advisory note",
}

# Explicit subcategory -> workspace_scope (reliable; checked first).
_SUBCATEGORY_SCOPE = {
    "investor-relations": "investor_relations",
    "fund-management": "fund",
    "due-diligence": "data_room",
    "leasing": "leasing",
    "legal": "governance",
    "closing": "deal",
    "daily-operations": "property_management",
    "financing": "debt",
    "portfolio-strategy": "portfolio",
    "tax-entity": "governance",
    "underwriting-analysis": "deal",
}

# Ordered (scope, keyword-tuple). First match wins; specific scopes precede
# the broad `deal` catch so e.g. a debt or leasing skill is not bucketed deal.
# Every scope value here MUST be in the workspace_scope enum.
_WORKSPACE_SCOPE_KEYWORDS = [
    ("debt", ("debt", "loan", "covenant", "mezz", "refi", "lender", "mortgage")),
    ("leasing", ("lease", "leasing", "tenant", "estoppel", "stacking", "rent-roll", "cam", "coi", "delinquency")),
    ("investor_relations", ("investor", "lp-", "lp_", "fund-raise", "capital-raise", "pitch", "quarterly-investor")),
    ("fund", ("fund-formation", "fund-operations", "partnership-allocation", "waterfall", "jv-")),
    ("property_management", ("property-management", "work-order", "vendor", "maintenance", "building-systems", "operations", "noi", "tenant-event")),
    ("data_room", ("data-room", "diligence", "dd-", "document-to", "warehouse", "lease-abstract", "exhibit")),
    ("governance", ("compliance", "regulatory", "audit", "tax-appeal", "1031", "cost-seg", "opportunity-zone", "insurance", "legal", "carbon")),
    ("market", ("market", "comp", "submarket", "supply-demand", "reit", "cycle")),
    ("portfolio", ("portfolio", "performance-attribution", "allocator")),
    ("deal", ("acquisition", "underwriting", "deal", "loi", "psa", "offer", "om-", "disposition", "closing", "ic-memo", "ic-red", "sourcing", "screen", "sensitivity", "land-residual", "entitlement")),
]


def derive_workspace_scope(slug: str, subcategory, category, description: str):
    """Conservative workspace_scope derivation. Subcategory (explicit, reliable)
    first, then SLUG substring match only — the slug is a curated identifier, so
    it avoids description false-positives like 'comp' inside 'decomposition' or a
    stray 'diligence' in a screening tool. Returns a valid enum value or None
    (honest 'unscoped'); explicit frontmatter `workspace_scope:` overrides.
    Non-liability hint."""
    if subcategory and subcategory in _SUBCATEGORY_SCOPE:
        return _SUBCATEGORY_SCOPE[subcategory]
    hay = (slug or "").lower()
    for scope, kws in _WORKSPACE_SCOPE_KEYWORDS:
        if any(k in hay for k in kws):
            return scope
    return None


def forward_compat_from(fm: dict, slug: str, item_type: str, classification: str,
                        calculator_file, subcategory, description: str,
                        category) -> dict:
    """Derive the four v5.2 forward-compat fields with frontmatter override.

    produces_artifact_kind: calculator_file/calculator -> calculator_result;
      orchestrator -> workflow_plan; else frontmatter or None.
    pii_policy: conservative default 'none', explicit frontmatter opt-in.
    workspace_scope: derived (subcategory/keywords) or frontmatter, else None.
    outputs: frontmatter list, else a single label seeded from artifact kind.
    """
    fm = fm or {}
    pak = fm.get("produces_artifact_kind")
    if pak is None:
        if item_type == "calculator" or calculator_file:
            pak = "calculator_result"
        elif classification == "orchestrator":
            pak = "workflow_plan"
    pii = fm.get("pii_policy") or "none"
    ws = fm.get("workspace_scope") or derive_workspace_scope(
        slug, subcategory, category, description)
    outputs = fm.get("outputs")
    if not outputs:
        outputs = [ARTIFACT_KIND_LABEL[pak]] if pak in ARTIFACT_KIND_LABEL else []
    return {
        "produces_artifact_kind": pak,
        "pii_policy": pii,
        "workspace_scope": ws,
        "outputs": outputs,
    }


# ---------------------------------------------------------------------------
# Scanners
# ---------------------------------------------------------------------------

def scan_skills(registry: dict, triggers: dict) -> list:
    """Scan skills/ directory and produce catalog items."""
    items = []
    skills_dir = SRC_DIR / "skills"
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        slug = skill_dir.name
        fm = parse_frontmatter(skill_md)
        reg = registry.get(slug, {})
        raw_status = fm.get("status", reg.get("status", "deployed"))
        status = STATUS_MAP.get(raw_status, "stable")
        category = reg.get("category", "cross-cutting")
        phase = CATEGORY_TO_PHASE.get(category, "cross-cutting")
        desc = fm.get("description", "")
        heading = extract_first_heading(skill_md)

        # Determine input artifacts from description
        input_artifacts = []
        desc_lower = desc.lower() if desc else ""
        for artifact in ["om", "rent roll", "lease", "t-12", "budget", "term sheet", "psa", "loi"]:
            if artifact in desc_lower:
                input_artifacts.append(artifact.upper() if len(artifact) <= 3 else artifact.title())

        item = {
            "id": slug,
            "display_name": heading or fm.get("name", slug),
            "type": "skill",
            "status": status,
            "source_path": f"src/skills/{slug}/SKILL.md",
            "domain": category,
            "persona": desc[:200] if desc else "",
            "lifecycle_phase": phase,
            "aliases": [],
            "intent_triggers": triggers.get(slug, []),
            "input_artifacts": input_artifacts,
            "outputs": [],
            "downstream_items": reg.get("chains_to", []),
            "upstream_items": reg.get("chains_from", []),
            "hidden_from_default_catalog": status in ("stub", "deprecated"),
            "legacy_wrapper_for": None,
            "owner": "Mario Urquia",
            "last_reviewed_at": None,
            "notes": "",
            "calculator_file": SKILL_CALCULATOR_MAP.get(slug),
            "priority": reg.get("priority"),
            "version": fm.get("version"),
        }
        gov = governance_from_frontmatter(
            fm, slug, "skill", category, fm.get("pack_type"), desc
        )
        item.update(gov)
        item.update(forward_compat_from(
            fm, slug, "skill", gov["classification"],
            SKILL_CALCULATOR_MAP.get(slug), fm.get("subcategory"), desc, category,
        ))
        items.append(item)
    return items


def scan_agents() -> list:
    """Scan agents/ directory (flat, no subdirs) and produce catalog items."""
    items = []
    agents_dir = SRC_DIR / "agents"
    for md_path in sorted(agents_dir.glob("*.md")):
        if md_path.name == "_index.md":
            continue
        rel = md_path.relative_to(REPO_ROOT)
        agent_id = md_path.stem
        fm = parse_frontmatter(md_path)
        heading = extract_first_heading(md_path)

        domain = "cross-cutting"
        phase = "cross-cutting"

        item = {
            "id": agent_id,
            "display_name": heading or agent_id.replace("-", " ").title(),
            "type": "agent",
            "status": "stable",
            "source_path": str(rel),
            "domain": domain,
            "persona": fm.get("description", "")[:200],
            "lifecycle_phase": phase,
            "aliases": [],
            "intent_triggers": [],
            "input_artifacts": [],
            "outputs": [],
            "downstream_items": [],
            "upstream_items": [],
            "hidden_from_default_catalog": False,
            "legacy_wrapper_for": None,
            "owner": "Mario Urquia",
            "last_reviewed_at": None,
            "notes": "",
            "calculator_file": None,
            "priority": None,
            "version": None,
        }
        gov = governance_from_frontmatter(
            fm, agent_id, "agent", domain, fm.get("pack_type"),
            fm.get("description", ""),
        )
        item.update(gov)
        item.update(forward_compat_from(
            fm, agent_id, "agent", gov["classification"], None,
            fm.get("subcategory"), fm.get("description", ""), domain,
        ))
        items.append(item)
    return items


def scan_commands() -> list:
    """Scan commands/ directory."""
    items = []
    commands_dir = SRC_DIR / "commands"
    for md_path in sorted(commands_dir.iterdir()):
        if not md_path.suffix == ".md":
            continue
        slug = md_path.stem
        fm = parse_frontmatter(md_path)
        heading = extract_first_heading(md_path)
        item = {
            "id": slug,
            "display_name": heading or fm.get("name", slug),
            "type": "command",
            "status": "stable",
            "source_path": f"src/commands/{md_path.name}",
            "domain": "cross-cutting",
            "persona": fm.get("description", "")[:200],
            "lifecycle_phase": "cross-cutting",
            "aliases": [],
            "intent_triggers": [],
            "input_artifacts": [],
            "outputs": [],
            "downstream_items": [],
            "upstream_items": [],
            "hidden_from_default_catalog": False,
            "legacy_wrapper_for": None,
            "owner": "Mario Urquia",
            "last_reviewed_at": None,
            "notes": "",
            "calculator_file": None,
            "priority": None,
            "version": None,
        }
        gov = governance_from_frontmatter(
            fm, slug, "command", "cross-cutting", fm.get("pack_type"),
            fm.get("description", ""),
        )
        item.update(gov)
        item.update(forward_compat_from(
            fm, slug, "command", gov["classification"], None,
            fm.get("subcategory"), fm.get("description", ""), "cross-cutting",
        ))
        items.append(item)
    return items


def scan_calculators() -> list:
    """Scan scripts/calculators/ directory."""
    items = []
    calc_dir = SRC_DIR / "calculators"
    for py_path in sorted(calc_dir.iterdir()):
        if py_path.suffix != ".py" or py_path.name == "__init__.py":
            continue
        calc_id = py_path.stem
        # Extract first docstring line
        desc = ""
        try:
            text = py_path.read_text(encoding="utf-8")
            match = re.search(r'"""(.+?)"""', text, re.DOTALL)
            if match:
                desc = match.group(1).strip().split("\n")[0]
        except Exception:
            pass

        item = {
            "id": calc_id,
            "display_name": calc_id.replace("_", " ").title(),
            "type": "calculator",
            "status": "stable",
            "source_path": f"src/calculators/{py_path.name}",
            "domain": "cross-cutting",
            "persona": desc[:200],
            "lifecycle_phase": "cross-cutting",
            "aliases": [],
            "intent_triggers": [],
            "input_artifacts": [],
            "outputs": [],
            "downstream_items": [],
            "upstream_items": [],
            "hidden_from_default_catalog": False,
            "legacy_wrapper_for": None,
            "owner": "Mario Urquia",
            "last_reviewed_at": None,
            "notes": "",
            "calculator_file": None,
            "priority": None,
            "version": None,
        }
        gov = governance_from_frontmatter(
            {}, calc_id, "calculator", "cross-cutting", None, desc
        )
        item.update(gov)
        item.update(forward_compat_from(
            {}, calc_id, "calculator", gov["classification"],
            f"src/calculators/{py_path.name}", None, desc, "cross-cutting",
        ))
        items.append(item)
    return items


def scan_orchestrators() -> list:
    """Scan orchestrators/configs/ directory."""
    items = []
    configs_dir = SRC_DIR / "orchestrators" / "configs"
    if not configs_dir.exists():
        return items
    for json_path in sorted(configs_dir.iterdir()):
        if json_path.suffix != ".json":
            continue
        orch_id = json_path.stem
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            display = data.get("name", orch_id.replace("-", " ").title())
            desc = data.get("description", "")
        except Exception:
            display = orch_id.replace("-", " ").title()
            desc = ""

        item = {
            "id": orch_id,
            "display_name": display,
            "type": "orchestrator",
            "status": "stable",
            "source_path": f"src/orchestrators/configs/{json_path.name}",
            "domain": orch_id,
            "persona": desc[:200],
            "lifecycle_phase": "cross-cutting",
            "aliases": [],
            "intent_triggers": [],
            "input_artifacts": [],
            "outputs": [],
            "downstream_items": [],
            "upstream_items": [],
            "hidden_from_default_catalog": False,
            "legacy_wrapper_for": None,
            "owner": "Mario Urquia",
            "last_reviewed_at": None,
            "notes": "",
            "calculator_file": None,
            "priority": None,
            "version": None,
        }
        # Runtime orchestrator engine configs are conductors by definition.
        # They declare runtime `phases` (agents + orchestratorFile), not a flat
        # list of catalog skill ids, so decomposes_to stays empty here; the
        # classification validator exempts these subsystem routers (§4.1).
        gov = governance_from_frontmatter({}, orch_id, "skill", orch_id, None, desc)
        gov["classification"] = "orchestrator"
        gov["runtime_role"] = "workflow_conductor"
        item.update(gov)
        item.update(forward_compat_from(
            {}, orch_id, "orchestrator", "orchestrator", None, None, desc, orch_id,
        ))
        items.append(item)
    return items


def build_workflow_items(chains: list) -> list:
    """Convert parsed workflow chains into catalog items."""
    items = []
    for chain in chains:
        item = {
            "id": chain["id"],
            "display_name": chain["display_name"],
            "type": "workflow",
            "status": "stable",
            "source_path": "src/routing/CRE-ROUTING.md",
            "domain": "cross-cutting",
            "persona": f"Workflow chain: {' -> '.join(chain['steps'][:5])}",
            "lifecycle_phase": "cross-cutting",
            "aliases": [],
            "intent_triggers": [],
            "input_artifacts": [],
            "outputs": [],
            "downstream_items": chain["steps"],
            "upstream_items": [],
            "hidden_from_default_catalog": False,
            "legacy_wrapper_for": None,
            "owner": "Mario Urquia",
            "last_reviewed_at": None,
            "notes": "",
            "calculator_file": None,
            "priority": None,
            "version": None,
        }
        # Workflow chains are documented routing descriptions (free-text steps
        # in CRE-ROUTING.md), not executable conductors. They carry no
        # resolvable decomposes_to; surface them as reference_only.
        gov = governance_from_frontmatter(
            {}, chain["id"], "workflow", "cross-cutting", None, ""
        )
        gov["runtime_role"] = "reference_only"
        item.update(gov)
        item.update(forward_compat_from(
            {}, chain["id"], "workflow", gov["classification"], None, None,
            chain.get("display_name", ""), "cross-cutting",
        ))
        items.append(item)
    return items


# ---------------------------------------------------------------------------
# Plugin version reader
# ---------------------------------------------------------------------------

def get_plugin_version() -> str:
    pj = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if pj.exists():
        data = json.loads(pj.read_text(encoding="utf-8"))
        return data.get("version", "0.0.0")
    return "0.0.0"


# ---------------------------------------------------------------------------
# MCP tool inventory (parsed from src/mcp-server.mjs)
# ---------------------------------------------------------------------------

def scan_mcp_tools() -> list:
    """Extract MCP tool definitions from src/mcp-server.mjs.

    Parses the TOOLS array via regex (cheap and dependency-free). Each tool
    must have a name and a description for the catalog entry to be valid.
    """
    mcp_file = SRC_DIR / "mcp-server.mjs"
    if not mcp_file.exists():
        return []
    src = mcp_file.read_text(encoding="utf-8")

    pattern = re.compile(
        r'\{\s*name:\s*"(cre_[a-z_]+)"\s*,\s*description:\s*"([^"]+)"',
        re.DOTALL,
    )
    tools = []
    for match in pattern.finditer(src):
        tools.append({
            "name": match.group(1),
            "description": match.group(2),
        })
    return tools


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_catalog() -> dict:
    registry = load_registry()
    triggers = parse_routing_triggers()
    chains = parse_workflow_chains()

    all_items = []
    all_items.extend(scan_skills(registry, triggers))
    all_items.extend(scan_agents())
    all_items.extend(scan_commands())
    all_items.extend(scan_calculators())
    all_items.extend(scan_orchestrators())
    all_items.extend(build_workflow_items(chains))

    catalog = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "plugin_version": get_plugin_version(),
        "items": all_items,
        "mcp_tools": scan_mcp_tools(),
    }
    return catalog


def validate_catalog(catalog: dict) -> list:
    """Basic validation checks. Returns list of issues."""
    issues = []
    ids_seen = {}
    for item in catalog.get("items", []):
        iid = item["id"]
        itype = item["type"]
        key = f"{itype}:{iid}"
        if key in ids_seen:
            issues.append(f"Duplicate {itype} id: {iid}")
        ids_seen[key] = True

        # Check source_path exists
        src = REPO_ROOT / item["source_path"]
        if not src.exists():
            issues.append(f"{itype} {iid}: source_path not found: {item['source_path']}")

        # Check required fields
        if not item.get("display_name"):
            issues.append(f"{itype} {iid}: missing display_name")
        if item["status"] not in ("stable", "experimental", "stub", "deprecated"):
            issues.append(f"{itype} {iid}: invalid status: {item['status']}")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Build or validate the CRE skills catalog")
    parser.add_argument("--validate", action="store_true", help="Validate existing catalog")
    parser.add_argument("--json", action="store_true", help="Output dist/catalog.json instead of YAML")
    args = parser.parse_args()

    if args.validate:
        catalog_path = SRC_DIR / "catalog" / "catalog.yaml"
        if not catalog_path.exists():
            print("ERROR: catalog/catalog.yaml not found. Run without --validate first.", file=sys.stderr)
            sys.exit(1)
        catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
        issues = validate_catalog(catalog)
        if issues:
            print(f"FAIL: {len(issues)} issues found:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print(f"OK: catalog valid ({len(catalog['items'])} items)")
        return

    catalog = build_catalog()

    # Validate before writing
    issues = validate_catalog(catalog)
    if issues:
        print(f"WARNING: {len(issues)} issues during build:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)

    # Write catalog.yaml
    catalog_yaml_path = SRC_DIR / "catalog" / "catalog.yaml"
    with open(catalog_yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(catalog, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)
    print(f"Wrote {catalog_yaml_path} ({len(catalog['items'])} items)")

    # Always generate dist/catalog.json
    dist_dir = REPO_ROOT / "dist"
    dist_dir.mkdir(exist_ok=True)
    dist_json_path = dist_dir / "catalog.json"
    with open(dist_json_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Wrote {dist_json_path}")

    # Summary
    by_type = {}
    by_status = {}
    for item in catalog["items"]:
        by_type[item["type"]] = by_type.get(item["type"], 0) + 1
        by_status[item["status"]] = by_status.get(item["status"], 0) + 1
    print("\nSummary:")
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")
    print(f"  total: {len(catalog['items'])}")
    print(f"\nBy status:")
    for s, c in sorted(by_status.items()):
        print(f"  {s}: {c}")


if __name__ == "__main__":
    main()
