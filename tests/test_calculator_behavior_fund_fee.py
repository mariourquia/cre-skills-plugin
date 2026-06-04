#!/usr/bin/env python3
"""Behavioral tests for the fund fee modeler (v5 -- new file).

This was the largest coverage gap: ~58 KB, the most complex financial module,
and ZERO automated tests. Unlike the pure ``calculate_x(dict)`` calculators it
is CLI-command-dispatched (``run_command`` with dashboard/scenario/mfn-audit/
export-csv), so this file exercises BOTH the core fee functions and the command
surface.

Covers: commitment-weighted tiered effective rate (hand-checked), full-waiver
override, fee-holiday amortization, blended-rate aggregation, the dashboard and
scenario CLI commands, breakeven fund size, a degenerate empty-LP set, a pinned
regression snapshot, and a bps unit-sanity check.
"""
from __future__ import annotations

import json
import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from fund_fee_modeler import (  # noqa: E402
    _effective_fee_rate,
    blended_fee,
    breakeven_fund_size,
    run_command,
    COMMITTED_STATUSES,
)


def _state() -> dict:
    return {
        "fundName": "Test Fund I",
        "fundId": "fund-001",
        "standardTerms": {
            "managementFee": 0.015,
            "fundTerm": 10,
            "investmentPeriod": 5,
            "preferredReturn": 0.08,
            "carry": 0.20,
        },
        "targetRaise": 200_000_000,
        "hardCap": 250_000_000,
        "mfnProvisions": {"enabled": True, "minimumCommitmentForMFN": 10_000_000},
        "investors": [
            {
                "lpId": "lp-001", "name": "Anchor LP", "commitment": 50_000_000,
                "status": "signed", "tier": "anchor",
                "negotiatedTerms": {"managementFee": 0.0125},
            },
            {
                "lpId": "lp-002", "name": "Tiered LP", "commitment": 75_000_000,
                "status": "signed", "tier": "standard",
                "negotiatedTerms": {"managementFeeTiers": [
                    {"upTo": 25_000_000, "rate": 0.015},
                    {"upTo": 1e18, "rate": 0.010},
                ]},
            },
            {
                "lpId": "lp-003", "name": "Seed LP", "commitment": 10_000_000,
                "status": "funded", "tier": "seed",
                "negotiatedTerms": {"feeWaiver": {"type": "full"}},
            },
            {
                "lpId": "lp-004", "name": "Prospect LP", "commitment": 20_000_000,
                "status": "prospect", "tier": "standard",
            },
        ],
    }


class TestEffectiveFeeRate(unittest.TestCase):
    def test_tiered_rate_is_commitment_weighted_marginal(self) -> None:
        state = _state()
        tiered = state["investors"][1]
        # (25M*1.5% + 50M*1.0%) / 75M
        expected = (25_000_000 * 0.015 + 50_000_000 * 0.010) / 75_000_000
        self.assertAlmostEqual(_effective_fee_rate(tiered, state), expected, delta=1e-9)

    def test_flat_negotiated_rate(self) -> None:
        state = _state()
        self.assertAlmostEqual(
            _effective_fee_rate(state["investors"][0], state), 0.0125, delta=1e-9
        )

    def test_full_waiver_overrides_everything(self) -> None:
        state = _state()
        self.assertEqual(_effective_fee_rate(state["investors"][2], state), 0.0)

    def test_fee_holiday_amortizes_rate_down(self) -> None:
        state = _state()
        inv = {
            "lpId": "lp-hol", "commitment": 30_000_000, "status": "signed",
            "negotiatedTerms": {
                "managementFee": 0.015,
                "feeHoliday": {"months": 12},
            },
        }
        # 0.015 * (120 - 12) / 120
        expected = 0.015 * (120 - 12) / 120
        self.assertAlmostEqual(_effective_fee_rate(inv, state), expected, delta=1e-9)
        self.assertLess(_effective_fee_rate(inv, state), 0.015)


class TestBlendedFee(unittest.TestCase):
    def test_blended_rate_committed(self) -> None:
        state = _state()
        bf = blended_fee(state["investors"], state, COMMITTED_STATUSES)
        # committed = signed + funded: 50M@1.25%, 75M@1.1667%, 10M@0%
        expected = (
            50_000_000 * 0.0125
            + 75_000_000 * ((25_000_000 * 0.015 + 50_000_000 * 0.010) / 75_000_000)
            + 10_000_000 * 0.0
        ) / 135_000_000
        self.assertAlmostEqual(bf["blended_rate"], expected, delta=1e-6)
        self.assertEqual(bf["lp_count"], 3)
        self.assertEqual(bf["total_commitment"], 135_000_000.0)

    def test_blended_below_standard_due_to_concessions(self) -> None:
        state = _state()
        bf = blended_fee(state["investors"], state, COMMITTED_STATUSES)
        self.assertLess(bf["blended_rate"], bf["standard_rate"])
        self.assertLess(bf["concession_cost"], 0)  # blended revenue < standard


class TestCommandSurface(unittest.TestCase):
    def test_dashboard_json(self) -> None:
        out = run_command("dashboard", _state(), output_format="json")
        d = json.loads(out)
        self.assertEqual(d["command"], "dashboard")
        self.assertAlmostEqual(d["progressPct"], 67.5, delta=0.1)
        self.assertIn("blendedFee", d)
        self.assertIn("mfnCascade", d)

    def test_scenario_requires_lp_id(self) -> None:
        out = run_command("scenario", _state(), output_format="json")
        self.assertIn("error", json.loads(out))

    def test_scenario_with_lp_id_runs(self) -> None:
        out = run_command(
            "scenario", _state(), lp_id="lp-001", proposed_fee=0.011,
            output_format="json",
        )
        d = json.loads(out)
        self.assertNotIn("error", d)

    def test_mfn_audit_runs(self) -> None:
        out = run_command("mfn-audit", _state(), output_format="json")
        d = json.loads(out)
        self.assertNotIn("error", d)


class TestBreakevenFundSize(unittest.TestCase):
    def test_breakeven_is_concession_over_one_bp(self) -> None:
        be = breakeven_fund_size(50_000, 135_000_000)
        # 1 bps of fund size == concession -> size = concession / 0.0001
        self.assertAlmostEqual(be["breakeven_size"], 500_000_000.0, delta=1.0)
        self.assertFalse(be["is_immaterial"])

    def test_zero_concession_is_immaterial(self) -> None:
        be = breakeven_fund_size(0, 100_000_000)
        self.assertTrue(be["is_immaterial"])


class TestFundFeeDegenerate(unittest.TestCase):
    def test_empty_lps_blended_falls_back_to_standard(self) -> None:
        state = {
            "standardTerms": {"managementFee": 0.015, "fundTerm": 10},
            "investors": [], "targetRaise": 0,
        }
        bf = blended_fee([], state, COMMITTED_STATUSES)
        self.assertEqual(bf["lp_count"], 0)
        self.assertEqual(bf["total_commitment"], 0.0)
        self.assertEqual(bf["blended_rate"], 0.015)

    def test_empty_lps_dashboard_does_not_crash(self) -> None:
        state = {
            "standardTerms": {"managementFee": 0.015, "fundTerm": 10},
            "investors": [], "targetRaise": 0,
        }
        out = run_command("dashboard", state, output_format="json")
        d = json.loads(out)
        self.assertEqual(d["command"], "dashboard")

    def test_zero_commitment_lps_excluded(self) -> None:
        state = _state()
        for inv in state["investors"]:
            inv["commitment"] = 0
        bf = blended_fee(state["investors"], state, COMMITTED_STATUSES)
        self.assertEqual(bf["total_commitment"], 0.0)
        self.assertEqual(bf["lp_count"], 0)


class TestFundFeeRegressionSnapshot(unittest.TestCase):
    def test_pinned_blended_and_committed(self) -> None:
        bf = blended_fee(_state()["investors"], _state(), COMMITTED_STATUSES)
        self.assertAlmostEqual(bf["blended_rate"], 0.011111, delta=1e-5)
        self.assertEqual(bf["total_commitment"], 135_000_000.0)
        self.assertEqual(bf["lp_count"], 3)


class TestFundFeeUnitSanity(unittest.TestCase):
    def test_delta_bps_scale(self) -> None:
        bf = blended_fee(_state()["investors"], _state(), COMMITTED_STATUSES)
        # delta_bps is in basis points: blended ~1.11% vs standard 1.5% -> about
        # -39 bps. Must be a tens-of-bps figure, not a raw fraction.
        self.assertLess(bf["delta_bps"], 0)
        self.assertGreater(bf["delta_bps"], -100)


if __name__ == "__main__":
    unittest.main()
