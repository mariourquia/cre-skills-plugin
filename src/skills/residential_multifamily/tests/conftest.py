"""Shared fixtures and helpers for the residential_multifamily subsystem test suite.

All paths are resolved relative to the subsystem root (computed from this file's
location, not from CWD or a hard-coded absolute path).

Only stdlib + PyYAML are used.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

import pytest
import yaml


# ---------------------------------------------------------------------------
# Subsystem root
# ---------------------------------------------------------------------------

# tests/ is a sibling of _core/, roles/, workflows/, overlays/, templates/, etc.
SUBSYS = Path(__file__).resolve().parents[1]
assert SUBSYS.name == "residential_multifamily", (
    f"SUBSYS must resolve to residential_multifamily, got {SUBSYS}"
)


# ---------------------------------------------------------------------------
# Schemas (loaded once at module import time)
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path} did not parse to a mapping"
    return data


METRIC_CONTRACT_SCHEMA = _load_yaml(SUBSYS / "_core" / "schemas" / "metric_contract.yaml")
REFERENCE_RECORD_SCHEMA = _load_yaml(SUBSYS / "_core" / "schemas" / "reference_record.yaml")
SKILL_MANIFEST_SCHEMA = _load_yaml(SUBSYS / "_core" / "schemas" / "skill_manifest.yaml")
OVERLAY_MANIFEST_SCHEMA = _load_yaml(SUBSYS / "_core" / "schemas" / "overlay_manifest.yaml")
REFERENCE_MANIFEST_SCHEMA = _load_yaml(SUBSYS / "_core" / "schemas" / "reference_manifest.yaml")
CHANGE_LOG_ENTRY_SCHEMA = _load_yaml(SUBSYS / "_core" / "schemas" / "change_log_entry.yaml")


# ---------------------------------------------------------------------------
# Lightweight JSON-Schema validator (subset needed for these tests)
# ---------------------------------------------------------------------------

def validate_against_schema(instance: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    """Return a list of error strings. Empty list = valid.

    Supports the subset of JSON Schema used by this subsystem's schemas:
    - type: object|array|string|number|integer|boolean
    - required
    - properties
    - enum
    - const
    - pattern (string regex)
    - items (single schema)
    - minItems
    - additionalProperties (bool)
    """
    errors: List[str] = []
    if schema is None:
        return errors

    if "const" in schema:
        if instance != schema["const"]:
            errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
        return errors

    if "enum" in schema:
        if instance not in schema["enum"]:
            errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")
        # fall through to type checks

    t = schema.get("type")
    if t == "object":
        if not isinstance(instance, dict):
            errors.append(f"{path}: expected object, got {type(instance).__name__}")
            return errors
        required = schema.get("required", []) or []
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required field '{key}'")
        props = schema.get("properties", {}) or {}
        additional = schema.get("additionalProperties", True)
        for key, val in instance.items():
            if key in props:
                # Optional (non-required) fields may be null to indicate "not applicable".
                if val is None and key not in required:
                    continue
                errors.extend(validate_against_schema(val, props[key], f"{path}.{key}"))
            elif additional is False:
                errors.append(f"{path}: unexpected field '{key}'")
        return errors
    if t == "array":
        if not isinstance(instance, list):
            errors.append(f"{path}: expected array, got {type(instance).__name__}")
            return errors
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            errors.append(f"{path}: array length {len(instance)} < minItems {min_items}")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(instance):
                errors.extend(validate_against_schema(item, item_schema, f"{path}[{idx}]"))
        return errors
    if t == "string":
        if not isinstance(instance, str):
            errors.append(f"{path}: expected string, got {type(instance).__name__}")
            return errors
        pat = schema.get("pattern")
        if pat and not re.match(pat, instance):
            errors.append(f"{path}: string {instance!r} does not match pattern {pat!r}")
        return errors
    if t == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            errors.append(f"{path}: expected integer, got {type(instance).__name__}")
        return errors
    if t == "number":
        if not isinstance(instance, (int, float)) or isinstance(instance, bool):
            errors.append(f"{path}: expected number, got {type(instance).__name__}")
        return errors
    if t == "boolean":
        if not isinstance(instance, bool):
            errors.append(f"{path}: expected boolean, got {type(instance).__name__}")
        return errors
    # No type declared: accept any (other keywords like enum/const already handled).
    return errors


# ---------------------------------------------------------------------------
# Helpers to parse metrics.md fenced yaml blocks
# ---------------------------------------------------------------------------

_FENCED_YAML_RE = re.compile(r"```yaml\s*\n(?P<body>.*?)\n```", re.DOTALL)


def extract_yaml_blocks(md_text: str) -> List[Dict[str, Any]]:
    """Extract every ```yaml fenced code block, parsing each as YAML.

    Raises AssertionError on any block that does not parse. The test that
    directly validates metric contracts relies on this strict behavior.
    """
    blocks = []
    for match in _FENCED_YAML_RE.finditer(md_text):
        body = match.group("body")
        try:
            parsed = yaml.safe_load(body)
        except yaml.YAMLError as exc:
            raise AssertionError(f"Invalid YAML block: {exc}\n---\n{body}")
        if parsed is not None:
            blocks.append(parsed)
    return blocks


_SLUG_LINE_RE = re.compile(r"^slug:\s*([a-z][a-z0-9_]*)\s*$", re.MULTILINE)


def extract_yaml_blocks_lenient(md_text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Like extract_yaml_blocks, but collects parse errors instead of raising.

    Returns (parsed_blocks, list_of_error_strings). Useful for tests that want
    to avoid cascading failures from a single malformed block elsewhere.

    When a block fails to parse, the extractor still attempts a regex recovery
    of the block's `slug:` line so downstream tests that need the slug (e.g.
    alias-registry cross-references) can find it. Recovered blocks are emitted
    as `{"slug": <slug>, "_recovered_from_parse_error": True}`.
    """
    blocks: List[Dict[str, Any]] = []
    errors: List[str] = []
    for match in _FENCED_YAML_RE.finditer(md_text):
        body = match.group("body")
        try:
            parsed = yaml.safe_load(body)
        except yaml.YAMLError as exc:
            snippet = body[:200].replace("\n", " | ")
            errors.append(f"YAML parse error: {exc} :: body starts with: {snippet}")
            # Best-effort slug recovery so downstream tests don't cascade-fail.
            slug_match = _SLUG_LINE_RE.search(body)
            if slug_match:
                blocks.append(
                    {"slug": slug_match.group(1), "_recovered_from_parse_error": True}
                )
            continue
        if parsed is not None:
            blocks.append(parsed)
    return blocks, errors


# ---------------------------------------------------------------------------
# Helpers to parse frontmatter
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(?P<body>.*?)\n---\s*\n(?P<rest>.*)$", re.DOTALL)


def split_frontmatter(md_text: str) -> Tuple[Dict[str, Any], str]:
    """Return (frontmatter_dict, remaining_body). Raises if frontmatter absent."""
    m = _FRONTMATTER_RE.match(md_text)
    if not m:
        raise AssertionError("Markdown file has no YAML frontmatter block")
    frontmatter = yaml.safe_load(m.group("body")) or {}
    body = m.group("rest")
    return frontmatter, body


# ---------------------------------------------------------------------------
# Helpers to iterate packs
# ---------------------------------------------------------------------------

def iter_role_pack_skill_paths() -> Iterator[Path]:
    roles_dir = SUBSYS / "roles"
    for child in sorted(roles_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("_"):
            continue
        sk = child / "SKILL.md"
        if sk.exists():
            yield sk


def iter_workflow_pack_skill_paths() -> Iterator[Path]:
    wf_dir = SUBSYS / "workflows"
    for child in sorted(wf_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("_"):
            continue
        sk = child / "SKILL.md"
        if sk.exists():
            yield sk


def iter_pack_reference_manifests() -> Iterator[Path]:
    for skill_path in list(iter_role_pack_skill_paths()) + list(iter_workflow_pack_skill_paths()):
        rm = skill_path.parent / "reference_manifest.yaml"
        if rm.exists():
            yield rm


def iter_overlay_manifests() -> Iterator[Path]:
    overlays_root = SUBSYS / "overlays"
    for p in overlays_root.rglob("overlay.yaml"):
        yield p


# ---------------------------------------------------------------------------
# Helpers for prose scanning (strip fenced code, skip "Example outputs" sections)
# ---------------------------------------------------------------------------

_FENCED_ANY_RE = re.compile(r"```.*?```", re.DOTALL)


def strip_fenced_code_blocks(md_text: str) -> str:
    return _FENCED_ANY_RE.sub("", md_text)


def strip_example_output_sections(md_text: str) -> str:
    """Remove any section whose heading line matches one of the example-section headings.

    The section runs from the heading to the next heading of the same or higher level
    (or end of file). If that next heading is also an example-section heading, the skip
    continues uninterrupted.
    """
    example_heading_patterns = [
        r"^##\s+Example outputs\s*$",
        r"^##\s+Example invocations\s*$",
    ]

    def _is_example_heading(line: str) -> bool:
        return any(re.match(pat, line.strip()) for pat in example_heading_patterns)

    lines = md_text.splitlines(keepends=True)
    out: List[str] = []
    skipping = False
    skip_depth: int | None = None
    for line in lines:
        heading_match = re.match(r"^(#+)\s+", line)
        if skipping:
            if heading_match:
                depth = len(heading_match.group(1))
                assert skip_depth is not None
                if depth <= skip_depth:
                    # Exit skip. But if the new heading is itself an example heading,
                    # transition straight back into skipping without emitting the line.
                    if _is_example_heading(line):
                        skip_depth = depth
                        continue
                    skipping = False
                    skip_depth = None
                    out.append(line)
                    continue
            # inside example section; skip
            continue
        if _is_example_heading(line):
            skipping = True
            skip_depth = len(heading_match.group(1)) if heading_match else 2
            continue
        out.append(line)
    return "".join(out)


# ---------------------------------------------------------------------------
# Pytest fixtures exposing the key objects
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def subsys_root() -> Path:
    return SUBSYS


@pytest.fixture(scope="session")
def metric_contract_schema() -> Dict[str, Any]:
    return METRIC_CONTRACT_SCHEMA


@pytest.fixture(scope="session")
def reference_record_schema() -> Dict[str, Any]:
    return REFERENCE_RECORD_SCHEMA


@pytest.fixture(scope="session")
def skill_manifest_schema() -> Dict[str, Any]:
    return SKILL_MANIFEST_SCHEMA


@pytest.fixture(scope="session")
def overlay_manifest_schema() -> Dict[str, Any]:
    return OVERLAY_MANIFEST_SCHEMA


@pytest.fixture(scope="session")
def reference_manifest_schema() -> Dict[str, Any]:
    return REFERENCE_MANIFEST_SCHEMA


@pytest.fixture(scope="session")
def change_log_entry_schema() -> Dict[str, Any]:
    return CHANGE_LOG_ENTRY_SCHEMA
