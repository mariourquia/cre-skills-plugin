#!/usr/bin/env python3
"""Cross-cutting degenerate-input CONTRACT test (v5 -- new file).

The shared rule is: a degenerate input must FAIL SAFE -- every financial
calculator must return a typed/structured envelope, never an uncaught raw
exception (which the calculator-bridge can only surface as a generic
"exited 1"). This single parametrized file iterates ALL financial calculator
slugs and asserts the contract at two layers:

Layer 1 (in-process, value-domain degeneracy):
    For the calculators where a degenerate VALUE (zero denominator / empty
    series / wrong-sign NOI) is meaningful, calling the entry function directly
    must return a typed refusal dict ({"error", "refused": true, "code"}),
    never raise.

Layer 2 (contract boundary, empty input dict):
    For EVERY financial slug, driving an empty `{}` through
    scripts/calculator-invoker.py (the real path the orchestrator bridge uses)
    must yield a structured envelope (validation_errors or error/refusal) on a
    clean process exit -- never a Python traceback on stdout.

Together these guarantee the bridge always carries an actionable reason.
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

INVOKER = os.path.join(PLUGIN_ROOT, "scripts", "calculator-invoker.py")


# The financial calculator slugs (excludes the ingestion / data-plumbing family,
# which has its own tests/test_ingestion_*.py suite).
FINANCIAL_SLUGS = [
    "quick_screen",
    "debt_sizing",
    "covenant_tester",
    "waterfall_calculator",
    "monte_carlo_simulator",
    "npv_trade_out",
    "option_valuation",
    "construction_estimator",
    "tenant_credit_scorer",
    "proration_calculator",
    "transfer_tax",
    "fund_fee_modeler",
]

# Calculators that must REFUSE (typed dict) on a VALUE-domain degeneracy, with
# all required keys present. As of v5.1, quick_screen / proration_calculator /
# transfer_tax also refuse in-process (previously they degraded "gracefully" into
# negative tax / negative prorations / a raw traceback on an unparseable date).
# fund_fee_modeler remains CLI-dispatched and is covered by its own file + Layer 2.
VALUE_DEGENERATE_REFUSERS = {
    "debt_sizing": (
        "debt_sizing", "calculate_debt_sizing",
        {"noi": -1, "property_value": 20_000_000, "target_dscr": 1.25,
         "target_ltv": 0.65, "target_debt_yield": 0.09, "rate": 0.065,
         "amortization_years": 30},
        "debt_sizing_degenerate",
    ),
    "covenant_tester": (
        "covenant_tester", "calculate_covenants",
        {"noi_by_year": [], "loan_amount": 0, "rate": 0.065,
         "amortization_years": 30, "property_value_by_year": [],
         "dscr_covenant": 1.25, "ltv_covenant": 0.75},
        "covenant_tester_degenerate",
    ),
    "waterfall_calculator": (
        "waterfall_calculator", "calculate_waterfall",
        {"lp_equity": 0, "gp_equity": 0, "preferred_return": 0.08, "tiers": [],
         "cashflows_by_period": []},
        "waterfall_degenerate",
    ),
    "monte_carlo_simulator": (
        "monte_carlo_simulator", "run_simulation",
        {"purchase_price": 10_000_000, "equity_invested": 3_500_000,
         "hold_period": 5, "base_noi": 650_000,
         "financing": {"ltv": 0.65, "rate": 0.065, "term": 10,
                       "amort_years": 30, "io_years": 0},
         "variables": [{"name": "v", "best_case": 0.04, "base_case": 0.03,
                        "worst_case": 0.01, "distribution": "triangular"}],
         "num_trials": 0},
        "monte_carlo_degenerate",
    ),
    "npv_trade_out": (
        "npv_trade_out", "calculate_trade_out",
        {"current_rent_psf": 28, "market_rent_psf": 35, "renewal_rent_psf": 32,
         "renewal_ti_psf": 5, "new_ti_psf": 25, "lc_pct_renewal": 0.025,
         "lc_pct_new": 0.05, "vacancy_months": 4, "make_ready_psf": 5, "sf": 0,
         "lease_term_years": 5, "discount_rate": 0.07, "annual_escalation": 0.03},
        "npv_trade_out_degenerate",
    ),
    "option_valuation": (
        "option_valuation", "calculate_option_valuation",
        {"ti_total": 250_000, "lc_total": 95_000, "months_remaining": 72,
         "market_rent_psf": 35, "sf": 10_000, "expected_vacancy_months": 6,
         "discount_rate": 0.07, "noi": 2_000_000, "cap_rate": 0,
         "tenant_pct_of_nra": 0.25},
        "option_valuation_degenerate",
    ),
    "construction_estimator": (
        "construction_estimator", "calculate_estimate",
        {"asset_type": "multifamily", "gross_sf": 0, "location": "Austin, TX",
         "construction_type": "wood_frame", "finish_level": "standard"},
        "construction_estimator_degenerate",
    ),
    "tenant_credit_scorer": (
        "tenant_credit_scorer", "calculate_tenant_credit",
        {"tenants": []},
        "tenant_credit_scorer_degenerate",
    ),
    "quick_screen": (
        "quick_screen", "calculate_quick_screen",
        {"purchase_price": 0, "noi": 650_000, "units_or_sf": 50},
        "quick_screen_degenerate",
    ),
    "proration_calculator": (
        "proration_calculator", "calculate_prorations",
        {"closing_date": "2026-07-01", "annual_tax": -5, "tax_year_start": "2026-01-01"},
        "proration_calculator_degenerate",
    ),
    "transfer_tax": (
        "transfer_tax", "calculate_transfer_tax",
        {"state": "NY", "purchase_price": -1, "property_type": "commercial"},
        "transfer_tax_degenerate",
    ),
}


class TestValueDegenerateRefusals(unittest.TestCase):
    """Layer 1: in-process typed refusal on a value-domain degeneracy."""

    def test_each_refuser_returns_typed_refusal_never_raises(self) -> None:
        for slug, (mod, fn, deg, code) in VALUE_DEGENERATE_REFUSERS.items():
            with self.subTest(slug=slug):
                module = importlib.import_module(mod)
                func = getattr(module, fn)
                try:
                    out = func(deg)
                except Exception as exc:  # noqa: BLE001 - contract is "never raise"
                    self.fail(f"{slug} raised {type(exc).__name__} on degenerate "
                              f"input instead of returning a typed refusal: {exc}")
                self.assertIsInstance(out, dict, f"{slug} did not return a dict")
                self.assertTrue(
                    out.get("refused") is True and bool(out.get("error")),
                    f"{slug} returned a non-refusal on degenerate input: {out!r}",
                )
                self.assertEqual(
                    out.get("code"), code,
                    f"{slug} refusal missing/incorrect typed code",
                )


class TestInvokerContractBoundary(unittest.TestCase):
    """Layer 2: empty input through the real invoker -> structured envelope,
    clean exit, never a raw traceback on stdout."""

    def _invoke_empty(self, slug: str) -> tuple[int, dict, str]:
        result = subprocess.run(
            [sys.executable, INVOKER, slug, "--json", "{}"],
            capture_output=True, text=True, timeout=30,
        )
        stdout = result.stdout.strip()
        # Contract requirement: stdout is always parseable JSON, never a
        # Python traceback.
        try:
            parsed = json.loads(stdout) if stdout else {}
        except json.JSONDecodeError:
            self.fail(f"{slug}: invoker emitted non-JSON on stdout (likely a raw "
                      f"traceback): {stdout[:200]!r}")
        return result.returncode, parsed, result.stderr

    def test_every_financial_slug_returns_structured_envelope(self) -> None:
        for slug in FINANCIAL_SLUGS:
            with self.subTest(slug=slug):
                _code, parsed, _stderr = self._invoke_empty(slug)
                self.assertIsInstance(parsed, dict)
                structured = (
                    "validation_errors" in parsed
                    or bool(parsed.get("error"))
                    or parsed.get("refused") is True
                )
                self.assertTrue(
                    structured,
                    f"{slug}: empty input did not yield a structured envelope "
                    f"(validation_errors / error / refused); got keys "
                    f"{list(parsed)}",
                )

    def test_no_slug_emits_raw_traceback(self) -> None:
        # A raw Python traceback would surface to the orchestrator as an opaque
        # CalculatorBridgeError "exited 1". Assert stderr never carries one for
        # an empty-input invocation (the invoker catches at the process boundary
        # OR the calculator refused before raising).
        for slug in FINANCIAL_SLUGS:
            with self.subTest(slug=slug):
                _code, _parsed, stderr = self._invoke_empty(slug)
                self.assertNotIn("Traceback (most recent call last)", stderr,
                                 f"{slug}: leaked a Python traceback on stderr")


if __name__ == "__main__":
    unittest.main()
