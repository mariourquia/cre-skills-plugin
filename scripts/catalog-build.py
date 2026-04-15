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
