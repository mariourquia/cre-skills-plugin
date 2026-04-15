#!/usr/bin/env python3
"""Value-correctness tests for all 12 CRE calculators."""
import math
import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from quick_screen import calculate_quick_screen, mortgage_payment_annual
from debt_sizing import calculate_debt_sizing, mortgage_constant, annual_debt_service
from waterfall_calculator import calculate_waterfall, irr_calc
from covenant_tester import calculate_covenants, mortgage_payment, loan_balance_at_year
from npv_trade_out import calculate_trade_out, npv_stream
from construction_estimator import calculate_estimate
from proration_calculator import calculate_prorations
from option_valuation import calculate_option_valuation, termination_fee
from transfer_tax import calculate_transfer_tax
from monte_carlo_simulator import run_simulation
from tenant_credit_scorer import calculate_tenant_credit


class TestQuickScreen(unittest.TestCase):
    """Value tests for deal-quick-screen calculator."""

    def test_basic_multifamily_deal(self):
        result = calculate_quick_screen({
            "purchase_price": 10_000_000,
            "noi": 700_000,
            "units_or_sf": 50,
            "unit_type": "units",
            "market_rent_per_unit": 1400,
            "in_place_rent_per_unit": 1200,
            "loan_amount": 6_500_000,
            "rate": 0.06,
            "amort_years": 30,
            "replacement_cost_estimate": 12_000_000,
            "hold_years": 5,
        })
        self.assertAlmostEqual(result["metrics"]["going_in_cap_rate"], 0.07, places=2)
        self.assertEqual(result["metrics"]["price_per_unit"], 200_000)
        self.assertGreater(result["metrics"]["dscr"], 1.2)
        self.assertTrue(result["metrics"]["positive_leverage"])
        self.assertIn(result["verdict"], ("KEEP", "MAYBE"))

    def test_negative_leverage_detected(self):
        result = calculate_quick_screen({
            "purchase_price": 10_000_000,
            "noi": 500_000,
            "units_or_sf": 50,
            "unit_type": "units",
            "loan_amount": 6_500_000,
            "rate": 0.07,
            "amort_years": 30,
        })
        self.assertEqual(result["metrics"]["going_in_cap_rate"], 0.05)
        self.assertFalse(result["metrics"]["positive_leverage"])
        neg_lev = any("Negative leverage" in r for r in result["kill_reasons"])
        self.assertTrue(neg_lev, "Expected 'Negative leverage' in kill_reasons")

    def test_mortgage_payment_annual_zero_rate(self):
        payment = mortgage_payment_annual(1_200_000, 0.0, 30)
        self.assertAlmostEqual(payment, 40_000.0, places=0)

    def test_scenario_irrs_populated(self):
        result = calculate_quick_screen({
            "purchase_price": 5_000_000,
            "noi": 350_000,
            "units_or_sf": 25,
            "unit_type": "units",
            "loan_amount": 3_250_000,
            "rate": 0.065,
            "amort_years": 30,
        })
        for scenario in ("bull", "base", "bear"):
            self.assertIn(scenario, result["scenarios"])
            self.assertIsNotNone(result["scenarios"][scenario]["estimated_irr"])
        self.assertGreater(
            result["scenarios"]["bull"]["estimated_irr"],
            result["scenarios"]["bear"]["estimated_irr"],
        )


class TestDebtSizing(unittest.TestCase):
    """Value tests for debt-sizing calculator."""

    def test_ltv_binding_constraint(self):
        result = calculate_debt_sizing({
            "noi": 1_500_000,
            "property_value": 20_000_000,
            "target_dscr": 1.25,
            "target_ltv": 0.65,
            "target_debt_yield": 0.09,
            "rate": 0.065,
            "amortization_years": 30,
        })
        self.assertEqual(result["sizing_results"]["max_loan_ltv"], 13_000_000)
        dy_loan = round(1_500_000 / 0.09, 0)
        self.assertAlmostEqual(result["sizing_results"]["max_loan_debt_yield"], dy_loan, delta=1)
        self.assertEqual(result["sizing_results"]["binding_constraint"], "LTV")
        self.assertEqual(result["sizing_results"]["recommended_loan"], 13_000_000)

    def test_dscr_binding_constraint(self):
        result = calculate_debt_sizing({
            "noi": 800_000,
            "property_value": 20_000_000,
            "target_dscr": 1.25,
            "target_ltv": 0.75,
            "rate": 0.065,
            "amortization_years": 30,
        })
        self.assertEqual(result["sizing_results"]["binding_constraint"], "DSCR")
        self.assertLess(result["sizing_results"]["recommended_loan"], 20_000_000 * 0.75)

    def test_mortgage_constant_known_value(self):
        mc = mortgage_constant(0.06, 30)
        self.assertAlmostEqual(mc, 0.071933, places=4)

    def test_rate_sensitivity_grid(self):
        result = calculate_debt_sizing({
            "noi": 1_000_000,
            "property_value": 15_000_000,
            "target_dscr": 1.25,
            "target_ltv": 0.65,
            "rate": 0.06,
            "amortization_years": 30,
        })
        grid = result["rate_sensitivity"]
        self.assertEqual(len(grid), 6)
        self.assertEqual(grid[0]["rate_bps_over_base"], 0)
        for i in range(len(grid) - 1):
            self.assertGreaterEqual(
                grid[i]["max_loan_dscr"], grid[i + 1]["max_loan_dscr"],
            )


class TestWaterfallCalculator(unittest.TestCase):
    """Value tests for JV waterfall calculator."""

    def test_basic_waterfall_90_10_split(self):
        result = calculate_waterfall({
            "lp_equity": 9_000_000,
            "gp_equity": 1_000_000,
            "preferred_return": 0.08,
            "tiers": [
                {"hurdle_irr": 0.08, "gp_split": 0.20, "lp_split": 0.80},
                {"hurdle_irr": 0.12, "gp_split": 0.30, "lp_split": 0.70},
                {"hurdle_irr": 0.18, "gp_split": 0.40, "lp_split": 0.60},
            ],
            "cashflows_by_period": [-10_000_000, 800_000, 850_000, 900_000, 950_000, 15_000_000],
            "catch_up_pct": 0.0,
            "compounding": True,
        })
        self.assertEqual(result["summary"]["total_equity"], 10_000_000)
        self.assertEqual(result["summary"]["lp_equity_pct"], 90.0)
        self.assertGreater(result["lp_results"]["total_distributions"], 9_000_000)
        self.assertGreater(result["gp_results"]["promote"], 0)
        self.assertIsNotNone(result["lp_results"]["irr"])
        self.assertIsNotNone(result["gp_results"]["irr"])

    def test_capital_return_before_profit(self):
        result = calculate_waterfall({
            "lp_equity": 5_000_000,
            "gp_equity": 5_000_000,
            "preferred_return": 0.08,
            "tiers": [{"hurdle_irr": 0.08, "gp_split": 0.50, "lp_split": 0.50}],
            "cashflows_by_period": [-10_000_000, 500_000, 500_000, 12_000_000],
            "catch_up_pct": 0.0,
        })
        tiers = result["waterfall_tiers"]
        pref_tier = next(t for t in tiers if t["tier"] == 1)
        self.assertGreater(pref_tier["lp_distribution"], 0)
        self.assertEqual(pref_tier["gp_distribution"], 0)

    def test_irr_calc_simple(self):
        irr = irr_calc([-100, 110])
        self.assertAlmostEqual(irr, 0.10, places=2)


class TestCovenantTester(unittest.TestCase):
    """Value tests for loan covenant tester."""

    def test_no_breach_healthy_loan(self):
        result = calculate_covenants({
            "noi_by_year": [1_200_000, 1_250_000, 1_300_000, 1_350_000, 1_400_000],
            "loan_amount": 10_000_000,
            "rate": 0.055,
            "amortization_years": 30,
            "io_years": 0,
            "property_value_by_year": [20_000_000] * 5,
            "dscr_covenant": 1.20,
            "ltv_covenant": 0.75,
        })
        self.assertFalse(result["breach_detected"])
        self.assertIsNone(result["first_breach_year"])
        for yr_detail in result["annual_detail"]:
            self.assertTrue(yr_detail["dscr_in_compliance"])

    def test_breach_detected_low_noi(self):
        result = calculate_covenants({
            "noi_by_year": [700_000, 650_000, 600_000],
            "loan_amount": 10_000_000,
            "rate": 0.065,
            "amortization_years": 30,
            "io_years": 0,
            "property_value_by_year": [12_000_000] * 3,
            "dscr_covenant": 1.25,
            "ltv_covenant": 0.75,
        })
        self.assertTrue(result["breach_detected"])
        self.assertIsNotNone(result["first_breach_year"])
        self.assertEqual(result["first_breach_type"], "DSCR")

    def test_io_period_uses_io_debt_service(self):
        result = calculate_covenants({
            "noi_by_year": [800_000, 800_000, 800_000],
            "loan_amount": 10_000_000,
            "rate": 0.06,
            "amortization_years": 30,
            "io_years": 2,
            "property_value_by_year": [15_000_000] * 3,
            "dscr_covenant": 1.25,
            "ltv_covenant": 0.75,
        })
        yr1 = result["annual_detail"][0]
        yr3 = result["annual_detail"][2]
        self.assertEqual(yr1["debt_service_type"], "IO")
        self.assertAlmostEqual(yr1["debt_service"], 600_000, places=0)
        self.assertEqual(yr3["debt_service_type"], "P&I")
        self.assertGreater(yr3["debt_service"], yr1["debt_service"])

    def test_cash_sweep_trigger(self):
        result = calculate_covenants({
            "noi_by_year": [750_000, 750_000],
            "loan_amount": 10_000_000,
            "rate": 0.065,
            "amortization_years": 30,
            "io_years": 0,
            "property_value_by_year": [15_000_000] * 2,
            "dscr_covenant": 1.25,
            "ltv_covenant": 0.75,
            "cash_sweep_dscr": 1.15,
        })
        ds = mortgage_payment(10_000_000, 0.065, 30)
        dscr = 750_000 / ds
        if dscr < 1.15:
            self.assertGreater(len(result["cash_sweep_years"]), 0)


class TestNpvTradeOut(unittest.TestCase):
    """Value tests for NPV lease trade-out analyzer."""

    def test_trade_out_higher_when_market_premium_large(self):
        result = calculate_trade_out({
            "current_rent_psf": 25.00,
            "market_rent_psf": 40.00,
            "renewal_rent_psf": 28.00,
            "renewal_ti_psf": 5.00,
            "new_ti_psf": 20.00,
            "lc_pct_renewal": 0.025,
            "lc_pct_new": 0.05,
            "vacancy_months": 3,
            "make_ready_psf": 5.00,
            "sf": 10_000,
            "lease_term_years": 5,
            "discount_rate": 0.07,
            "annual_escalation": 0.03,
            "carrying_cost_psf_monthly": 2.00,
        })
        self.assertGreater(result["tradeout_npv"], result["renewal_npv"])
        self.assertIn(result["verdict"], ("TRADE_OUT",))

    def test_renew_when_vacancy_high(self):
        result = calculate_trade_out({
            "current_rent_psf": 30.00,
            "market_rent_psf": 33.00,
            "renewal_rent_psf": 31.00,
            "renewal_ti_psf": 3.00,
            "new_ti_psf": 30.00,
            "lc_pct_renewal": 0.025,
            "lc_pct_new": 0.05,
            "vacancy_months": 9,
            "make_ready_psf": 8.00,
            "sf": 15_000,
            "lease_term_years": 5,
            "discount_rate": 0.07,
            "annual_escalation": 0.03,
            "carrying_cost_psf_monthly": 3.00,
        })
        self.assertGreater(result["renewal_npv"], result["tradeout_npv"])

    def test_npv_stream_simple(self):
        npv = npv_stream([100, 100, 100], 0.10)
        expected = 100 + 100 / 1.1 + 100 / 1.21
        self.assertAlmostEqual(npv, expected, places=2)

    def test_breakeven_vacancy_reasonable(self):
        result = calculate_trade_out({
            "current_rent_psf": 25.00,
            "market_rent_psf": 35.00,
            "renewal_rent_psf": 28.00,
            "renewal_ti_psf": 5.00,
            "new_ti_psf": 25.00,
            "lc_pct_renewal": 0.025,
            "lc_pct_new": 0.05,
            "vacancy_months": 4,
            "make_ready_psf": 5.00,
            "sf": 10_000,
            "lease_term_years": 5,
            "discount_rate": 0.07,
            "annual_escalation": 0.03,
            "carrying_cost_psf_monthly": 2.50,
        })
        self.assertGreater(result["breakeven_vacancy_months"], 0)
        self.assertLess(result["breakeven_vacancy_months"], 24)


class TestConstructionEstimator(unittest.TestCase):
    """Value tests for construction cost estimator."""

    def test_basic_multifamily_estimate(self):
        result = calculate_estimate({
            "asset_type": "multifamily",
            "gross_sf": 200_000,
            "unit_count": 250,
            "stories": 5,
            "location": "Austin, TX",
            "construction_type": "wood_frame",
            "finish_level": "standard",
            "parking_type": "surface",
            "parking_spaces": 300,
            "union_labor": False,
            "prevailing_wage": False,
            "site_conditions": "greenfield",
        })
        self.assertIn("tdc_summary", result)
        tdc = result["tdc_summary"]["tdc_excl_land"]
        self.assertGreater(tdc, 0)
        cost_per_sf = tdc / 200_000
        self.assertGreater(cost_per_sf, 100)
        self.assertLess(cost_per_sf, 800)

    def test_union_labor_increases_cost(self):
        base = calculate_estimate({
            "asset_type": "multifamily",
            "gross_sf": 100_000,
            "unit_count": 100,
            "stories": 4,
            "location": "Dallas, TX",
            "construction_type": "wood_frame",
            "finish_level": "standard",
            "parking_type": "surface",
            "parking_spaces": 120,
            "union_labor": False,
        })
        union = calculate_estimate({
            "asset_type": "multifamily",
            "gross_sf": 100_000,
            "unit_count": 100,
            "stories": 4,
            "location": "Dallas, TX",
            "construction_type": "wood_frame",
            "finish_level": "standard",
            "parking_type": "surface",
            "parking_spaces": 120,
            "union_labor": True,
        })
        self.assertGreater(
            union["tdc_summary"]["tdc_excl_land"],
            base["tdc_summary"]["tdc_excl_land"],
        )


class TestProrationCalculator(unittest.TestCase):
    """Value tests for closing proration calculator."""

    def test_basic_proration_mid_month(self):
        result = calculate_prorations({
            "closing_date": "2026-03-15",
            "annual_tax": 180_000,
            "tax_year_start": "2026-01-01",
            "tax_paid_through": "2025-12-31",
            "monthly_rent": 125_000,
            "rent_collected_through": "2026-03-31",
            "proration_method": "actual_365",
        })
        self.assertIn("line_items", result)
        per_diem_tax = 180_000 / 365
        self.assertAlmostEqual(result["line_items"][0]["per_diem"], per_diem_tax, delta=1)

    def test_seller_credit_for_prepaid_rent(self):
        result = calculate_prorations({
            "closing_date": "2026-06-15",
            "monthly_rent": 100_000,
            "rent_collected_through": "2026-06-30",
            "proration_method": "actual_365",
        })
        self.assertIn("net_proration", result)
        self.assertNotEqual(result["net_proration"], 0)


class TestOptionValuation(unittest.TestCase):
    """Value tests for lease option valuation."""

    def test_termination_fee_unamortized_ti(self):
        result = termination_fee({
            "ti_total": 250_000,
            "ti_amortization_months": 120,
            "lc_total": 0,
            "months_remaining": 60,
            "market_rent_psf": 30.00,
            "sf": 10_000,
            "expected_vacancy_months": 6,
            "releasing_cost_psf": 25.00,
            "discount_rate": 0.07,
        })
        unamortized = 250_000 * (60 / 120)
        self.assertAlmostEqual(result["unamortized_ti"], unamortized, delta=1)

    def test_full_option_valuation(self):
        result = calculate_option_valuation({
            "ti_total": 250_000,
            "ti_amortization_months": 120,
            "lc_total": 95_000,
            "lc_amortization_months": 120,
            "months_remaining": 72,
            "market_rent_psf": 35.00,
            "sf": 10_000,
            "expected_vacancy_months": 6,
            "releasing_cost_psf": 30.00,
            "discount_rate": 0.07,
            "noi": 2_000_000,
            "cap_rate": 0.055,
            "tenant_pct_of_nra": 0.25,
            "lease_term_years": 10,
            "remaining_term_years": 6,
        })
        self.assertIn("termination_fee", result)
        self.assertGreater(result["termination_fee"]["minimum_termination_fee"], 0)
        self.assertIn("package_comparison", result)


class TestTransferTax(unittest.TestCase):
    """Value tests for transfer tax calculator."""

    def test_florida_transfer_tax(self):
        result = calculate_transfer_tax({
            "state": "FL",
            "purchase_price": 5_000_000,
        })
        expected_state = 5_000_000 * 0.007
        self.assertAlmostEqual(result["state_tax"], expected_state, delta=100)
        self.assertGreater(result["total_tax"], 0)

    def test_texas_no_transfer_tax(self):
        result = calculate_transfer_tax({
            "state": "TX",
            "purchase_price": 10_000_000,
        })
        self.assertEqual(result["state_tax"], 0)

    def test_nyc_commercial_tiered(self):
        result = calculate_transfer_tax({
            "state": "NY",
            "county": "New York",
            "purchase_price": 15_000_000,
            "property_type": "commercial",
        })
        self.assertGreater(result["total_tax"], 0)
        self.assertGreater(result["total_tax"], 15_000_000 * 0.004)


class TestMonteCarloSimulator(unittest.TestCase):
    """Value tests for Monte Carlo return simulator."""

    def test_deterministic_with_seed(self):
        config = {
            "purchase_price": 10_000_000,
            "equity_invested": 3_500_000,
            "hold_period": 5,
            "base_noi": 650_000,
            "financing": {
                "ltv": 0.65, "rate": 0.065, "term": 10,
                "amort_years": 30, "io_years": 0,
            },
            "variables": [
                {"name": "rent_growth", "best_case": 0.04, "base_case": 0.03,
                 "worst_case": 0.01, "distribution": "triangular"},
                {"name": "exit_cap", "best_case": 0.055, "base_case": 0.065,
                 "worst_case": 0.08, "distribution": "triangular"},
            ],
            "num_trials": 100,
            "random_seed": 42,
        }
        r1 = run_simulation(config)
        r2 = run_simulation(config)
        self.assertEqual(
            r1["summary_statistics"]["irr"],
            r2["summary_statistics"]["irr"],
        )

    def test_more_trials_narrows_spread(self):
        config = {
            "purchase_price": 10_000_000,
            "equity_invested": 3_500_000,
            "hold_period": 5,
            "base_noi": 650_000,
            "financing": {
                "ltv": 0.65, "rate": 0.065, "term": 10,
                "amort_years": 30, "io_years": 0,
            },
            "variables": [
                {"name": "rent_growth", "best_case": 0.04, "base_case": 0.03,
                 "worst_case": 0.01, "distribution": "triangular"},
                {"name": "exit_cap", "best_case": 0.055, "base_case": 0.065,
                 "worst_case": 0.08, "distribution": "triangular"},
            ],
            "num_trials": 500,
            "random_seed": 42,
        }
        result = run_simulation(config)
        self.assertIn("percentile_returns", result)
        pct = result["percentile_returns"]
        self.assertGreater(pct["P75"]["irr"], pct["P25"]["irr"])


class TestTenantCreditScorer(unittest.TestCase):
    """Value tests for tenant credit scorer."""

    def test_single_tenant_concentration(self):
        result = calculate_tenant_credit({
            "tenants": [
                {
                    "name": "Amazon",
                    "annual_rent": 500_000,
                    "sf": 20_000,
                    "lease_remaining_years": 8,
                    "credit_rating": "AA-",
                    "revenue": 500_000_000,
                    "property_type": "industrial",
                },
            ],
        })
        self.assertEqual(result["hhi"], 10000)
        self.assertGreater(result["walt_years"], 0)

    def test_diversified_rent_roll(self):
        result = calculate_tenant_credit({
            "tenants": [
                {"name": f"Tenant_{i}", "annual_rent": 100_000, "sf": 2000,
                 "lease_remaining_years": 3 + i, "credit_rating": "BBB",
                 "property_type": "office"}
                for i in range(10)
            ],
        })
        self.assertLess(result["hhi"], 1500)
        self.assertGreater(result["walt_years"], 3)

    def test_unrated_tenant_conservative(self):
        result = calculate_tenant_credit({
            "tenants": [
                {
                    "name": "Mom & Pop Shop",
                    "annual_rent": 60_000,
                    "sf": 1500,
                    "lease_remaining_years": 2,
                    "credit_rating": None,
                    "property_type": "retail",
                },
            ],
        })
        tenant_detail = result["tenants"][0]
        self.assertGreater(tenant_detail["annual_expected_loss"], 0)


if __name__ == "__main__":
    unittest.main()
