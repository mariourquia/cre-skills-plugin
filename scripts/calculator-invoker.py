#!/usr/bin/env python3
"""
Calculator Invoker
==================
Zero-dependency CLI that dispatches calculations to registered calculator scripts.
Loads calculator-registry.json, validates inputs, invokes the target script via
subprocess, and returns structured JSON output.

Usage:
    python3 scripts/calculator-invoker.py <slug> --json '{...}'
    python3 scripts/calculator-invoker.py --list
    python3 scripts/calculator-invoker.py --info <slug>
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = SCRIPT_DIR / "calculator-registry.json"


# ---------------------------------------------------------------------------
# Registry loader
# ---------------------------------------------------------------------------

def load_registry() -> dict:
    """Load calculator registry from JSON file."""
    if not REGISTRY_PATH.exists():
        print(
            json.dumps({"error": f"Registry not found at {REGISTRY_PATH}"}),
            file=sys.stderr,
        )
        sys.exit(1)
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_inputs(slug: str, calc_def: dict, user_inputs: dict) -> list[str]:
    """
    Validate that all required inputs are present.
    Returns a list of error messages (empty if valid).
    """
    errors: list[str] = []
    inputs_schema = calc_def.get("inputs", {})

    for field_name, field_def in inputs_schema.items():
        # Skip non-dict entries (e.g. _note strings)
        if not isinstance(field_def, dict):
            continue
        if field_def.get("required", False) and field_name not in user_inputs:
            desc = field_def.get("description", "")
            errors.append(
                f"Missing required input '{field_name}' for calculator '{slug}'"
                + (f" ({desc})" if desc else "")
            )

    return errors


# ---------------------------------------------------------------------------
# Script resolution
# ---------------------------------------------------------------------------

def resolve_script_path(script_relative: str) -> Path:
    """
    Resolve the calculator script path relative to the plugin root.
    The plugin root is two levels up from this script (scripts/ -> plugin root).
    """
    plugin_root = SCRIPT_DIR.parent
    script_path = plugin_root / script_relative
    return script_path.resolve()


# ---------------------------------------------------------------------------
# Invocation
# ---------------------------------------------------------------------------

def invoke_calculator(
    slug: str,
    calc_def: dict,
    user_inputs: dict,
    extra_args: list[str] | None = None,
) -> dict:
    """
    Invoke a calculator script via subprocess and return parsed JSON output.
    """
    script_path = resolve_script_path(calc_def["script"])

    if not script_path.exists():
        return {
            "error": f"Calculator script not found: {script_path}",
            "slug": slug,
        }

    cmd = [sys.executable, str(script_path), "--json", json.dumps(user_inputs)]

    # Append any extra CLI args (e.g. --command, --format)
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(script_path.parent),
        )
    except subprocess.TimeoutExpired:
        return {
            "error": f"Calculator '{slug}' timed out after 120 seconds",
            "slug": slug,
        }
    except OSError as e:
        return {
            "error": f"Failed to execute calculator '{slug}': {e}",
            "slug": slug,
        }

    if result.returncode != 0:
        return {
            "error": f"Calculator '{slug}' exited with code {result.returncode}",
            "slug": slug,
            "stderr": result.stderr.strip() if result.stderr else None,
        }

    # Try to parse JSON from stdout
    stdout = result.stdout.strip()
    if not stdout:
        return {
            "error": f"Calculator '{slug}' produced no output",
            "slug": slug,
            "stderr": result.stderr.strip() if result.stderr else None,
        }

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        # If output is not JSON, return it as raw text
        return {
            "slug": slug,
            "raw_output": stdout,
            "note": "Output was not valid JSON; returned as raw text",
        }


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_list(registry: dict) -> None:
    """Print all registered calculator slugs with descriptions."""
    calculators = registry.get("calculators", {})
    result = []
    for slug, defn in sorted(calculators.items()):
        result.append({
            "slug": slug,
            "description": defn.get("description", ""),
            "script": defn.get("script", ""),
            "used_by": defn.get("used_by", []),
        })
    print(json.dumps({"calculators": result, "count": len(result)}, indent=2))


def cmd_info(registry: dict, slug: str) -> None:
    """Print full schema info for a single calculator."""
    calculators = registry.get("calculators", {})
    if slug not in calculators:
        print(json.dumps({"error": f"Unknown calculator: '{slug}'"}))
        sys.exit(1)
    calc_def = calculators[slug]
    print(json.dumps({slug: calc_def}, indent=2))


def cmd_run(
    registry: dict,
    slug: str,
    json_input: str,
    extra_args: list[str] | None = None,
) -> None:
    """Validate inputs, invoke calculator, and print result."""
    calculators = registry.get("calculators", {})

    if slug not in calculators:
        available = ", ".join(sorted(calculators.keys()))
        print(
            json.dumps({
                "error": f"Unknown calculator: '{slug}'",
                "available": available,
            }),
        )
        sys.exit(1)

    calc_def = calculators[slug]

    # Parse user input JSON
    try:
        user_inputs = json.loads(json_input)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}))
        sys.exit(1)

    # Validate required inputs
    errors = validate_inputs(slug, calc_def, user_inputs)
    if errors:
        print(json.dumps({"validation_errors": errors, "slug": slug}))
        sys.exit(1)

    # Invoke
    result = invoke_calculator(slug, calc_def, user_inputs, extra_args)
    print(json.dumps(result, indent=2))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="CRE Calculator Invoker -- dispatches to registered calculator scripts",
    )
    parser.add_argument(
        "slug",
        nargs="?",
        help="Calculator slug to invoke (e.g. quick_screen, debt_sizing)",
    )
    parser.add_argument(
        "--json",
        dest="json_input",
        help="JSON input string for the calculator",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all registered calculators",
    )
    parser.add_argument(
        "--info",
        metavar="SLUG",
        help="Show full schema for a specific calculator",
    )

    args, extra = parser.parse_known_args()
    registry = load_registry()

    if args.list:
        cmd_list(registry)
        return

    if args.info:
        cmd_info(registry, args.info)
        return

    if not args.slug:
        parser.print_help()
        sys.exit(1)

    if not args.json_input:
        print(json.dumps({"error": "Missing --json argument"}))
        sys.exit(1)

    cmd_run(registry, args.slug, args.json_input, extra or None)


if __name__ == "__main__":
    main()
