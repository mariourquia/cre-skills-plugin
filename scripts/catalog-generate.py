#!/usr/bin/env python3
"""
catalog-generate.py — Generate all public surfaces from the canonical catalog.

Reads catalog/catalog.yaml (or dist/catalog.json) and generates:
  1. README.md count sections (between markers)
  2. registry.yaml (compatibility layer)
  3. hooks.json SessionStart prompt (with accurate counts)
  4. plugin.json description (with accurate counts)
  5. routing/CRE-ROUTING.md quick routing table (from intent_triggers)

All public-facing counts come from the catalog. No hardcoded numbers.

Usage:
    python scripts/catalog-generate.py           # generate all surfaces
    python scripts/catalog-generate.py --dry-run  # show what would change
    python scripts/catalog-generate.py --check    # CI mode: fail if surfaces drift
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"


def load_catalog() -> dict:
    """Load catalog from YAML (primary) or JSON (fallback)."""
    yaml_path = SRC_DIR / "catalog" / "catalog.yaml"
    json_path = REPO_ROOT / "dist" / "catalog.json"
    if yaml_path.exists():
        return yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if json_path.exists():
        return json.loads(json_path.read_text(encoding="utf-8"))
    print("ERROR: No catalog found. Run catalog-build.py first.", file=sys.stderr)
    sys.exit(1)


def catalog_counts(catalog: dict) -> dict:
    """Derive all counts from catalog items."""
    items = catalog["items"]
    counts = {
        "skills": sum(1 for i in items if i["type"] == "skill"),
        "skills_stable": sum(1 for i in items if i["type"] == "skill" and i["status"] == "stable"),
        "skills_stub": sum(1 for i in items if i["type"] == "skill" and i["status"] == "stub"),
        "agents": sum(1 for i in items if i["type"] == "agent"),
        "commands": sum(1 for i in items if i["type"] == "command"),
        "calculators": sum(1 for i in items if i["type"] == "calculator"),
        "orchestrators": sum(1 for i in items if i["type"] == "orchestrator"),
        "workflows": sum(1 for i in items if i["type"] == "workflow"),
        "total": len(items),
    }

    # Count reference files
    ref_count = 0
    skills_dir = SRC_DIR / "skills"
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        refs_dir = skill_dir / "references"
        if refs_dir.exists():
            ref_count += sum(1 for f in refs_dir.rglob("*") if f.is_file())
    counts["reference_files"] = ref_count

    # Count categories (unique lifecycle phases for skills, excluding cross-cutting)
    skill_phases = set(
        i["lifecycle_phase"] for i in items
        if i["type"] == "skill" and i["lifecycle_phase"] != "cross-cutting"
    )
    counts["categories"] = len(skill_phases)

    return counts


# ---------------------------------------------------------------------------
# README.md generator
# ---------------------------------------------------------------------------

README_STATS_START = "<!-- CATALOG:STATS:START -->"
README_STATS_END = "<!-- CATALOG:STATS:END -->"
README_SKILLS_TABLE_START = "<!-- CATALOG:SKILLS_TABLE:START -->"
README_SKILLS_TABLE_END = "<!-- CATALOG:SKILLS_TABLE:END -->"


def generate_readme_stats(counts: dict) -> str:
    return (
        "| Metric | Count |\n"
        "|--------|-------|\n"
        f"| Skills | **{counts['skills']}** |\n"
        f"| Expert Agents | **{counts['agents']}** |\n"
        f"| Reference Files | **{counts['reference_files']}** |\n"
        f"| Python Calculators | **{counts['calculators']}** |\n"
        f"| Workflow Chains | **{counts['workflows']}** |\n"
        f"| Orchestrator Pipelines | **{counts['orchestrators']}** |\n"
        f"| Slash Commands | **{counts['commands']}** |\n"
        f"| Skill Categories | **{counts['categories']}** |"
    )


def generate_skills_table(catalog: dict) -> str:
    """Generate a markdown table of skills grouped by lifecycle phase."""
    items = [i for i in catalog["items"] if i["type"] == "skill" and not i["hidden_from_default_catalog"]]

    # Group by lifecycle_phase
    groups = {}
    for item in items:
        phase = item["lifecycle_phase"]
        groups.setdefault(phase, []).append(item)

    PHASE_ORDER = [
        "screening", "underwriting", "structuring", "due-diligence",
        "capital-markets", "market-research", "asset-management", "leasing",
        "investor-relations", "development", "disposition", "sourcing",
        "tax-entity", "esg-climate", "portfolio-strategy", "daily-operations",
        "legal", "closing", "fund-management", "cross-cutting",
    ]

    PHASE_LABELS = {
        "screening": "Deal Screening",
        "underwriting": "Underwriting & Analysis",
        "structuring": "Deal Structuring",
        "due-diligence": "Due Diligence",
        "capital-markets": "Capital Markets",
        "market-research": "Market Research",
        "asset-management": "Asset Management",
        "leasing": "Leasing",
        "investor-relations": "Investor Relations",
        "development": "Development",
        "disposition": "Disposition",
        "sourcing": "Deal Sourcing",
        "tax-entity": "Tax & Entity Structure",
        "esg-climate": "ESG & Climate",
        "portfolio-strategy": "Portfolio Strategy",
        "daily-operations": "Daily Operations",
        "legal": "Legal",
        "closing": "Closing",
        "fund-management": "Fund Management",
        "cross-cutting": "Cross-Cutting",
    }

    lines = ["| Category | Skills | Count |", "|---|---|---|"]
    for phase in PHASE_ORDER:
        if phase not in groups:
            continue
        skills = sorted(groups[phase], key=lambda s: s["id"])
        label = PHASE_LABELS.get(phase, phase.replace("-", " ").title())
        skill_names = ", ".join(f"`{s['id']}`" for s in skills)
        lines.append(f"| {label} | {skill_names} | {len(skills)} |")

    return "\n".join(lines)


def update_readme(catalog: dict, counts: dict, dry_run: bool = False) -> bool:
    """Update README.md with catalog-derived content. Returns True if changed."""
    readme_path = REPO_ROOT / "README.md"
    text = readme_path.read_text(encoding="utf-8")
    original = text

    # Update stats section
    stats_block = generate_readme_stats(counts)
    if README_STATS_START in text and README_STATS_END in text:
        pattern = re.escape(README_STATS_START) + r".*?" + re.escape(README_STATS_END)
        replacement = f"{README_STATS_START}\n{stats_block}\n{README_STATS_END}"
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)

    # Update skills table
    skills_table = generate_skills_table(catalog)
    if README_SKILLS_TABLE_START in text and README_SKILLS_TABLE_END in text:
        pattern = re.escape(README_SKILLS_TABLE_START) + r".*?" + re.escape(README_SKILLS_TABLE_END)
        replacement = f"{README_SKILLS_TABLE_START}\n{skills_table}\n{README_SKILLS_TABLE_END}"
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)

    changed = text != original
    if changed and not dry_run:
        readme_path.write_text(text, encoding="utf-8")
    return changed


# ---------------------------------------------------------------------------
# hooks.json updater
# ---------------------------------------------------------------------------

def update_hooks(counts: dict, dry_run: bool = False) -> bool:
    """Update hooks.json SessionStart prompt with accurate counts."""
    hooks_path = SRC_DIR / "hooks" / "hooks.json"
    data = json.loads(hooks_path.read_text(encoding="utf-8"))
    original = json.dumps(data, indent=2)

    prompt = (
        f"The CRE Skills plugin is active with {counts['skills']} CRE skills, "
        f"{counts['agents']} expert agents, {counts['workflows']} workflow chains, "
        f"and {counts['orchestrators']} orchestrator pipelines. "
        f"For any CRE task, read the routing index at "
        f"${{CLAUDE_PLUGIN_ROOT}}/routing/CRE-ROUTING.md to find the right skill. "
        f"Do NOT load all SKILL.md files -- use the routing index to identify the "
        f"correct one, then load only that skill's SKILL.md and references/. "
        f"Available commands: /cre-skills:cre-route (find a skill), "
        f"/cre-skills:cre-workflows (workflow chains), "
        f"/cre-skills:cre-agents (expert agents), "
        f"/cre-skills:orchestrate (run a pipeline), "
        f"/cre-skills:usage-stats (telemetry summary), "
        f"/cre-skills:feedback-summary (skill feedback log), "
        f"/cre-skills:send-feedback (share feedback), "
        f"/cre-skills:report-problem (report a bug). "
        f"Telemetry and feedback are opt-in. Configure at ~/.cre-skills/config.json."
    )

    for hook_group in data.get("hooks", {}).get("SessionStart", []):
        for hook in hook_group.get("hooks", []):
            if hook.get("type") == "prompt":
                hook["prompt"] = prompt

    updated = json.dumps(data, indent=2)
    changed = updated != original
    if changed and not dry_run:
        hooks_path.write_text(updated + "\n", encoding="utf-8")
    return changed


# ---------------------------------------------------------------------------
# plugin.json updater
# ---------------------------------------------------------------------------

def update_plugin_json(counts: dict, dry_run: bool = False) -> bool:
    """Update plugin.json description with accurate counts."""
    pj_path = SRC_DIR / "plugin" / "plugin.json"
    data = json.loads(pj_path.read_text(encoding="utf-8"))
    original = json.dumps(data, indent=2)

    data["description"] = (
        f"{counts['skills']} institutional-grade CRE skills covering ~97% of commercial "
        f"real estate workflow steps. Deal screening, underwriting, structuring, due "
        f"diligence, capital markets, market research, asset management, leasing, investor "
        f"relations, development, disposition, sourcing, tax, ESG, portfolio strategy, and "
        f"daily operations. Includes Monte Carlo simulation, SEC Reg D compliance, property "
        f"management ops, deal attribution tracking, 1031 pipeline management, distribution "
        f"notice generation, fund-raise LP negotiation tracking, and emerging manager "
        f"evaluation. {counts['agents']} expert subagents, {counts['reference_files']} "
        f"reference files, {counts['calculators']} Python calculators, "
        f"{counts['workflows']} workflow chains, {counts['orchestrators']} orchestrator "
        f"pipelines, and orchestrator integration for multi-agent acquisition pipelines."
    )

    updated = json.dumps(data, indent=2)
    changed = updated != original
    if changed and not dry_run:
        pj_path.write_text(updated + "\n", encoding="utf-8")
    return changed


# ---------------------------------------------------------------------------
# Routing index updater (regenerate intent trigger table)
# ---------------------------------------------------------------------------

def update_routing_index(catalog: dict, counts: dict, dry_run: bool = False) -> bool:
    """Regenerate the Quick Routing Table in CRE-ROUTING.md from catalog triggers."""
    routing_path = SRC_DIR / "routing" / "CRE-ROUTING.md"
    text = routing_path.read_text(encoding="utf-8")
    original = text

    # Build new table from catalog
    skills_with_triggers = [
        i for i in catalog["items"]
        if i["type"] == "skill" and i["intent_triggers"] and not i["hidden_from_default_catalog"]
    ]

    header_line = "| User says... | Invoke this skill |"
    sep_line = "|---|---|"
    rows = []
    for skill in sorted(skills_with_triggers, key=lambda s: s["id"]):
        triggers = ", ".join(f'"{t}"' for t in skill["intent_triggers"][:5])
        rows.append(f'| {triggers} | `/{skill["id"]}` |')

    new_table = "\n".join([header_line, sep_line] + rows)

    # Replace existing table
    lines = text.split("\n")
    new_lines = []
    in_table = False
    table_replaced = False
    for line in lines:
        if line.strip().startswith("| User says"):
            if not table_replaced:
                new_lines.append(new_table)
                in_table = True
                table_replaced = True
            continue
        if in_table:
            if line.strip().startswith("|"):
                continue
            in_table = False
        new_lines.append(line)

    text = "\n".join(new_lines)

    # Update count in header
    text = re.sub(
        r">\s*\d+\s+CRE skills",
        f"> {counts['skills']} CRE skills",
        text,
    )

    changed = text != original
    if changed and not dry_run:
        routing_path.write_text(text, encoding="utf-8")
    return changed


# ---------------------------------------------------------------------------
# Registry compatibility layer
# ---------------------------------------------------------------------------

def generate_registry_compat(catalog: dict, dry_run: bool = False) -> bool:
    """Generate registry.yaml from catalog for backward compatibility."""
    reg_path = REPO_ROOT / "registry.yaml"
    original = reg_path.read_text(encoding="utf-8") if reg_path.exists() else ""

    skills = [i for i in catalog["items"] if i["type"] == "skill"]

    header = (
        "# CRE Skills Registry\n"
        f"# GENERATED from catalog/catalog.yaml — do not edit manually\n"
        f"# Run: python scripts/catalog-generate.py\n"
        f"# Generated: {catalog['generated_at'][:10]}\n"
        f"# Total Skills: {len(skills)}\n\n"
        f"metadata:\n"
        f'  version: "2.0"\n'
        f'  generated: "{catalog["generated_at"][:10]}"\n'
        f"  total_skills: {len(skills)}\n"
        f"  source: catalog/catalog.yaml\n\n"
        f"skills:\n"
    )

    STATUS_REVERSE = {"stable": "deployed", "stub": "stub", "experimental": "experimental", "deprecated": "deprecated"}

    entries = []
    for s in sorted(skills, key=lambda x: x["id"]):
        entry = {
            "slug": s["id"],
            "name": s["display_name"],
            "category": s["domain"],
            "priority": s.get("priority") or "P1",
            "status": STATUS_REVERSE.get(s["status"], s["status"]),
            "chains_to": s.get("downstream_items", []),
            "chains_from": s.get("upstream_items", []),
        }
        entries.append(entry)

    content = header + yaml.dump(entries, default_flow_style=False, sort_keys=False, allow_unicode=True)
    changed = content != original
    if changed and not dry_run:
        reg_path.write_text(content, encoding="utf-8")
    return changed


def main():
    parser = argparse.ArgumentParser(description="Generate public surfaces from catalog")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--check", action="store_true", help="CI mode: fail if any surface would change")
    args = parser.parse_args()

    catalog = load_catalog()
    counts = catalog_counts(catalog)

    changes = {}
    changes["README.md"] = update_readme(catalog, counts, dry_run=args.dry_run or args.check)
    changes["hooks.json"] = update_hooks(counts, dry_run=args.dry_run or args.check)
    changes["plugin.json"] = update_plugin_json(counts, dry_run=args.dry_run or args.check)
    changes["CRE-ROUTING.md"] = update_routing_index(catalog, counts, dry_run=args.dry_run or args.check)
    changes["registry.yaml"] = generate_registry_compat(catalog, dry_run=args.dry_run or args.check)

    print(f"Catalog: {counts['total']} items")
    print(f"  skills: {counts['skills']} ({counts['skills_stable']} stable, {counts['skills_stub']} stub)")
    print(f"  agents: {counts['agents']}")
    print(f"  commands: {counts['commands']}")
    print(f"  calculators: {counts['calculators']}")
    print(f"  orchestrators: {counts['orchestrators']}")
    print(f"  workflows: {counts['workflows']}")
    print(f"  reference_files: {counts['reference_files']}")
    print()

    any_changed = any(changes.values())
    for surface, changed in changes.items():
        status = "CHANGED" if changed else "ok"
        print(f"  {surface}: {status}")

    if args.check and any_changed:
        print("\nFAIL: Surfaces have drifted from catalog. Run: python scripts/catalog-generate.py")
        sys.exit(1)
    elif args.dry_run:
        print("\nDry run — no files written.")
    elif any_changed:
        print("\nSurfaces updated.")
    else:
        print("\nAll surfaces up to date.")


if __name__ == "__main__":
    main()
