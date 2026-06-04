#!/usr/bin/env python3
"""Behavioral tests for the tenant credit scorer (v5 -- new file).

Covers: single-tenant HHI = 10000, n equal tenants HHI = 10000/n, unrated
tenant -> D tier / conservative PD, expected loss = pd * (1 - recovery) * EAD,
OCR flag firing above the property-type threshold, a pinned regression
snapshot, a scale unit-sanity check, and degenerate REFUSALS (empty tenant
list, zero total rent) now returned as the typed envelope.
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from tenant_credit_scorer import calculate_tenant_credit  # noqa: E402


def _is_refusal(out: dict) -> bool:
    return isinstance(out, dict) and out.get("refused") is True and bool(out.get("error"))


class TestTenantCreditHHI(unittest.TestCase):
    def test_single_tenant_hhi_is_10000(self) -> None:
        out = calculate_tenant_credit({"tenants": [
            {"name": "Solo", "annual_rent": 500_000, "sf": 10_000,
             "lease_remaining_years": 7, "credit_rating": "BBB",
             "property_type": "retail"},
        ]})
        self.assertEqual(out["hhi"], 10_000.0)

    def test_n_equal_tenants_hhi_is_10000_over_n(self) -> None:
        tenants = [
            {"name": f"T{i}", "annual_rent": 100_000, "sf": 2_000,
             "lease_remaining_years": 5, "credit_rating": "A",
             "property_type": "office"}
            for i in range(4)
        ]
        out = calculate_tenant_credit({"tenants": tenants})
        self.assertAlmostEqual(out["hhi"], 10_000.0 / 4, delta=1.0)


class TestTenantCreditUnrated(unittest.TestCase):
    def test_unrated_tenant_is_d_tier_conservative_pd(self) -> None:
        out = calculate_tenant_credit({"tenants": [
            {"name": "NR", "annual_rent": 300_000, "sf": 5_000,
             "lease_remaining_years": 4, "credit_rating": None,
             "property_type": "retail"},
        ]})
        t = out["tenants"][0]
        self.assertEqual(t["tier"], "D")
        self.assertGreaterEqual(t["default_probability_5yr"], 0.40)


class TestTenantCreditExpectedLoss(unittest.TestCase):
    def test_expected_loss_equals_pd_lgd_ead(self) -> None:
        out = calculate_tenant_credit({"tenants": [
            {"name": "NR", "annual_rent": 300_000, "sf": 5_000,
             "lease_remaining_years": 4, "credit_rating": None,
             "property_type": "retail"},
        ]})
        t = out["tenants"][0]
        pd = t["default_probability_5yr"]
        recovery = t["recovery_rate"]
        ead = 300_000 * min(4, 5)
        expected = pd * (1 - recovery) * ead
        self.assertAlmostEqual(t["expected_loss_5yr"], expected, delta=1.0)


class TestTenantCreditOCR(unittest.TestCase):
    def test_ocr_flag_fires_above_threshold(self) -> None:
        # 120k / 800k = 0.15 OCR > 0.12 retail threshold -> flagged.
        out = calculate_tenant_credit({"tenants": [
            {"name": "Rst", "annual_rent": 120_000, "sf": 2_000,
             "lease_remaining_years": 5, "credit_rating": "BB",
             "revenue": 800_000, "property_type": "retail"},
        ]})
        t = out["tenants"][0]
        self.assertAlmostEqual(t["occupancy_cost_ratio"], 0.15, delta=0.001)
        self.assertTrue(t["ocr_flagged"])


class TestTenantCreditRegressionSnapshot(unittest.TestCase):
    def test_pinned_two_tenant(self) -> None:
        out = calculate_tenant_credit({"tenants": [
            {"name": "Walgreens", "annual_rent": 378_000, "sf": 14_700,
             "lease_remaining_years": 6.5, "credit_rating": "Baa2",
             "revenue": 2_500_000, "property_type": "retail"},
            {"name": "Local Restaurant", "annual_rent": 128_000, "sf": 3_200,
             "lease_remaining_years": 1.5, "credit_rating": None,
             "revenue": 850_000, "property_type": "retail"},
        ]})
        self.assertAlmostEqual(out["hhi"], 6_221.0, delta=2.0)
        self.assertAlmostEqual(out["walt_years"], 5.24, delta=0.05)
        self.assertAlmostEqual(out["walt_weighted_credit_score"], 84.6, delta=0.5)
        self.assertEqual(out["total_annual_rent"], 506_000)


class TestTenantCreditUnitSanity(unittest.TestCase):
    def test_hhi_in_index_scale(self) -> None:
        out = calculate_tenant_credit({"tenants": [
            {"name": "A", "annual_rent": 300_000, "sf": 5_000,
             "lease_remaining_years": 5, "credit_rating": "A",
             "property_type": "office"},
            {"name": "B", "annual_rent": 200_000, "sf": 4_000,
             "lease_remaining_years": 5, "credit_rating": "BBB",
             "property_type": "office"},
        ]})
        # HHI is on the 0-10000 index scale.
        self.assertGreater(out["hhi"], 0.0)
        self.assertLessEqual(out["hhi"], 10_000.0)


class TestTenantCreditDegenerateRefusals(unittest.TestCase):
    def test_empty_tenants_refuses(self) -> None:
        out = calculate_tenant_credit({"tenants": []})
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_zero_rent_refuses(self) -> None:
        out = calculate_tenant_credit({"tenants": [
            {"name": "ZeroRent", "annual_rent": 0, "sf": 1_000,
             "lease_remaining_years": 3, "credit_rating": "A",
             "property_type": "office"},
        ]})
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_refusal_is_typed(self) -> None:
        out = calculate_tenant_credit({"tenants": []})
        self.assertEqual(out.get("code"), "tenant_credit_scorer_degenerate")


if __name__ == "__main__":
    unittest.main()
