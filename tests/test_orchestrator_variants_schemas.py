#!/usr/bin/env python3
"""v4.4 scaffold: validate orchestrator variant files + new schemas.

Narrow scope: the variant + schema files added in v4.4 must be well-
formed, internally consistent, and reference only phases that the
base orchestrator declares. Full executor integration tests land in
a later PR (see docs/orchestrator-v0-design.md section 5).

Checked here:
- deal_state.schema.json + approval_gate.schema.json parse as JSON.
- acquisition value_add variant phases.json references only phases
  present in the base acquisition.json.
- Variant approval_matrix.yaml overrides are numeric and strictly
  tighter than the base (lower thresholds — value-add is MORE
  conservative, not less).
- Variant example_deal.json has the required shape.
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
ORCH = PLUGIN_ROOT / "src" / "orchestrators"


class SchemaFilesLoad(unittest.TestCase):
    def test_deal_state_schema_loads(self) -> None:
        schema = json.loads((ORCH / "schemas" / "deal_state.schema.json").read_text())
        self.assertEqual(schema["type"], "object")
        self.assertIn("deal_id", schema["required"])
        self.assertIn("pipeline", schema["properties"])
        self.assertIn("acquisition", schema["properties"]["pipeline"]["enum"])

    def test_approval_gate_schema_loads(self) -> None:
        schema = json.loads((ORCH / "schemas" / "approval_gate.schema.json").read_text())
        self.assertEqual(schema["type"], "object")
        self.assertIn("gate_id", schema["required"])
        self.assertIn("pending", schema["properties"]["status"]["enum"])
        self.assertIn("approved_with_conditions", schema["properties"]["status"]["enum"])


class AcquisitionValueAddVariantFiles(unittest.TestCase):
    def setUp(self) -> None:
        self.variant = ORCH / "configs" / "acquisition" / "variants" / "value_add"
        self.base = json.loads((ORCH / "configs" / "acquisition.json").read_text())

    def test_phases_json_valid(self) -> None:
        phases = json.loads((self.variant / "phases.json").read_text())
        self.assertEqual(phases["variant"], "value_add")
        self.assertIn("phase_weight_overrides", phases)

    def test_phases_weights_sum_to_one(self) -> None:
        phases = json.loads((self.variant / "phases.json").read_text())
        total = sum(phases["phase_weight_overrides"].values())
        self.assertAlmostEqual(total, 1.0, delta=0.0001)

    def test_phases_reference_only_base_phases(self) -> None:
        base_phase_ids = {p["phaseId"] for p in self.base["phases"]}
        phases = json.loads((self.variant / "phases.json").read_text())
        variant_phase_ids = set(phases["phase_weight_overrides"].keys())
        unknown = variant_phase_ids - base_phase_ids
        self.assertFalse(
            unknown,
            f"variant references phases that are not in base acquisition.json: {unknown}",
        )

    @unittest.skipIf(yaml is None, "PyYAML not installed")
    def test_approval_matrix_tighter_than_base(self) -> None:
        mat_path = self.variant / "approval_matrix.yaml"
        data = yaml.safe_load(mat_path.read_text(encoding="utf-8"))
        overrides = data["overrides"]
        # Sanity: every override is numeric.
        for k, v in overrides.items():
            self.assertIsInstance(v, (int, float), f"override {k} must be numeric")
        # Capex must be tighter (lower) than the base-core's nominal 250K.
        self.assertLess(overrides["capex_approval_threshold_usd"], 250000)

    def test_example_deal_well_formed(self) -> None:
        ex = json.loads((self.variant / "example_deal.json").read_text())
        required = {
            "deal_id",
            "variant",
            "asset_class",
            "purchase_price_usd",
            "going_in_cap_rate",
            "stabilized_cap_rate",
            "hold_years",
            "financing",
        }
        missing = required - set(ex.keys())
        self.assertFalse(missing, f"example_deal.json missing keys: {missing}")
        self.assertEqual(ex["variant"], "value_add")
        self.assertGreater(ex["stabilized_cap_rate"], ex["going_in_cap_rate"])


class DesignDocExists(unittest.TestCase):
    """The design doc is the source of truth for the v4.4 work. It
    must exist so reviewers can evaluate PRs against a concrete spec."""

    def test_design_doc_exists(self) -> None:
        self.assertTrue((PLUGIN_ROOT / "docs" / "orchestrator-v0-design.md").is_file())

    def test_design_doc_references_schemas(self) -> None:
        body = (PLUGIN_ROOT / "docs" / "orchestrator-v0-design.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("deal_state.schema.json", body)
        self.assertIn("approval_gate.schema.json", body)


if __name__ == "__main__":
    unittest.main()
