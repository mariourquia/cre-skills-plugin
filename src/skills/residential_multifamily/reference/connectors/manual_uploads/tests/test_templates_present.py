"""Manual Uploads: every template slug declared in schema.yaml has a file_templates/ file."""
from __future__ import annotations

from pathlib import Path


CONNECTOR_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = CONNECTOR_DIR / "file_templates"


def test_every_declared_template_has_a_template_file(connector_helpers):
    """For each entity in schema.yaml, at least one file_templates/<entity>_template.<ext> exists."""
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    entities = connector_helpers["entities_of"](schema)
    # templates block (sibling of entities) holds per-template metadata
    templates_meta = schema.get("templates", {})
    missing = []
    for entity_name in entities:
        # Look for a file matching <entity_name>_template.* in file_templates/
        candidates = list(TEMPLATES_DIR.glob(f"{entity_name}_template.*"))
        # Also accept the configured template_path from templates_meta.
        configured = templates_meta.get(entity_name, {}).get("template_path")
        configured_exists = False
        if configured:
            configured_exists = (CONNECTOR_DIR / configured).exists()
        if not candidates and not configured_exists:
            missing.append(entity_name)
    assert not missing, f"Templates missing from file_templates/: {missing}"


def test_templates_carry_status_tag():
    """Every template file has a status: template reference somewhere in its body."""
    failing = []
    for path in TEMPLATES_DIR.iterdir():
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "status: template" not in text:
            failing.append(path.name)
    assert not failing, f"Templates missing 'status: template' tag: {failing}"


def test_templates_point_to_schema():
    """Every template file references the schema.yaml path as a pointer."""
    failing = []
    for path in TEMPLATES_DIR.iterdir():
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "schema.yaml" not in text:
            failing.append(path.name)
    assert not failing, f"Templates missing schema.yaml pointer: {failing}"
