# CRE Computational Calculators

Standalone Python scripts for precise CRE calculations. Every script:

- Uses Python 3.10+ stdlib only (no pip install needed)
- Accepts input via `--json` CLI arg or piped stdin
- Outputs structured JSON
- Is self-documented with docstrings and usage examples

## Scripts

### proration_calculator.py
**Skill:** funds-flow-calculator
**Purpose:** Per diem prorations for property tax, rent, insurance, and CAM/OpEx at closing. Supports actual/365, actual/360, and 30/360 conventions.

```bash
python3 scripts/calculators/proration_calculator.py --json '{
    "closing_date": "2026-03-15",
    "annual_tax": 180000,
    "tax_year_start": "2026-01-01",
    "tax_paid_through": "2025-12-31",
    "monthly_rent": 125000,
    "rent_collected_through": "2026-03-31",
    "insurance_annual": 42000,
    "insurance_paid_through": "2026-06-30",
    "proration_method": "actual_365"
}'
```

**Input:** closing_date, annual_tax, tax_year_start, tax_paid_through, monthly_rent, rent_collected_through, insurance_annual, insurance_paid_through, cam_annual (optional), proration_method (actual_365|actual_360|30_360)
**Output:** line_items[], total_buyer_credit, total_seller_credit, net_proration, net_direction

---

### npv_trade_out.py
**Skill:** lease-trade-out-analyzer
**Purpose:** NPV comparison of renewal vs trade-out scenarios. Includes breakeven analysis and 2D sensitivity grid (vacancy x rent premium).

```bash
python3 scripts/calculators/npv_trade_out.py --json '{
    "current_rent_psf": 28.00,
    "market_rent_psf": 35.00,
    "renewal_rent_psf": 32.00,
    "renewal_ti_psf": 5.00,
    "new_ti_psf": 25.00,
    "lc_pct_renewal": 0.025,
    "lc_pct_new": 0.05,
    "vacancy_months": 4,
    "make_ready_psf": 5.00,
    "sf": 10000,
    "lease_term_years": 5,
    "discount_rate": 0.07,
    "annual_escalation": 0.03,
    "carrying_cost_psf_monthly": 2.50
}'
```

**Input:** current_rent_psf, market_rent_psf, renewal_rent_psf, renewal_ti_psf, new_ti_psf, lc_pct_renewal, lc_pct_new, vacancy_months, make_ready_psf, sf, lease_term_years, discount_rate, annual_escalation, carrying_cost_psf_monthly
**Output:** renewal_npv, tradeout_npv, npv_delta, verdict (RENEW|TRADE_OUT|MARGINAL), confidence, breakeven_vacancy_months, breakeven_rent_psf, breakeven_ti_psf, sensitivity_grid[]

---

### tenant_credit_scorer.py
**Skill:** tenant-credit-analyzer
**Purpose:** HHI concentration index, WALT-weighted credit score, expected annual loss by tenant, and occupancy cost ratios. Maps S&P/Moody's ratings to default probabilities and recovery rates.

```bash
python3 scripts/calculators/tenant_credit_scorer.py --json '{
    "tenants": [
        {"name": "Walgreens", "annual_rent": 378000, "sf": 14700, "lease_remaining_years": 6.5, "credit_rating": "Baa2", "revenue": 2500000, "property_type": "retail"},
        {"name": "Local Restaurant", "annual_rent": 128000, "sf": 3200, "lease_remaining_years": 1.5, "credit_rating": null, "revenue": 850000, "property_type": "retail"}
    ]
}'
```

**Input:** tenants[] with name, annual_rent, sf, lease_remaining_years, credit_rating (S&P or Moody's or null), revenue (optional), property_type
**Output:** hhi, walt_years, walt_weighted_credit_score, score_equivalent_rating, expected_loss_pct_of_egi, concentration_flags[], tenants[] with per-tenant detail

---

### covenant_tester.py
**Skill:** loan-document-reviewer
**Purpose:** Tests DSCR, LTV, and debt yield covenants against multi-year projections. Detects first breach year, cash sweep trigger activation, and stress tests at +200bps.

```bash
python3 scripts/calculators/covenant_tester.py --json '{
    "noi_by_year": [1200000, 1250000, 1300000, 1350000, 1400000],
    "loan_amount": 10000000,
    "rate": 0.065,
    "amortization_years": 30,
    "io_years": 2,
    "property_value_by_year": [16000000, 16500000, 17000000, 17500000, 18000000],
    "dscr_covenant": 1.25,
    "ltv_covenant": 0.75,
    "debt_yield_covenant": 0.08,
    "cash_sweep_dscr": 1.15
}'
```

**Input:** noi_by_year[], loan_amount, rate, amortization_years, io_years, property_value_by_year[], dscr_covenant, ltv_covenant, debt_yield_covenant, cash_sweep_dscr
**Output:** breach_detected, first_breach_year, first_breach_type, cash_sweep_years[], dscr_by_year[], ltv_by_year[], debt_yield_by_year[], annual_detail[], stressed_dscr

---

### option_valuation.py
**Skill:** lease-option-structurer
**Purpose:** Termination fee calculation (unamortized TI + LC + vacancy NPV + re-leasing cost), cap rate impact by option type, and conservative/moderate/aggressive package comparison.

```bash
python3 scripts/calculators/option_valuation.py --json '{
    "ti_total": 250000,
    "ti_amortization_months": 120,
    "lc_total": 95000,
    "lc_amortization_months": 120,
    "months_remaining": 72,
    "market_rent_psf": 35.00,
    "sf": 10000,
    "expected_vacancy_months": 6,
    "releasing_cost_psf": 30.00,
    "discount_rate": 0.07,
    "noi": 2000000,
    "cap_rate": 0.055,
    "tenant_pct_of_nra": 0.25,
    "lease_term_years": 10,
    "remaining_term_years": 6
}'
```

**Input:** ti_total, ti_amortization_months, lc_total, lc_amortization_months, months_remaining, market_rent_psf, sf, expected_vacancy_months, releasing_cost_psf, discount_rate, noi, cap_rate, tenant_pct_of_nra
**Output:** termination_fee{}, cap_rate_impact{impacts_by_option_type}, package_comparison{conservative, moderate, aggressive}

---

### waterfall_calculator.py
**Skill:** jv-waterfall-architect
**Purpose:** GP/LP distribution waterfall with preferred return accrual, multi-tier promote, catch-up, and IRR calculation via Newton-Raphson.

```bash
python3 scripts/calculators/waterfall_calculator.py --json '{
    "lp_equity": 9000000,
    "gp_equity": 1000000,
    "preferred_return": 0.08,
    "tiers": [
        {"hurdle_irr": 0.08, "gp_split": 0.20, "lp_split": 0.80},
        {"hurdle_irr": 0.12, "gp_split": 0.30, "lp_split": 0.70},
        {"hurdle_irr": 0.18, "gp_split": 0.40, "lp_split": 0.60}
    ],
    "cashflows_by_period": [-10000000, 800000, 850000, 900000, 950000, 15000000],
    "catch_up_pct": 0.50,
    "compounding": true
}'
```

**Input:** lp_equity, gp_equity, preferred_return, tiers[{hurdle_irr, gp_split, lp_split}], cashflows_by_period[], catch_up_pct, compounding
**Output:** lp_results{irr, equity_multiple, total_distributions}, gp_results{irr, promote, equity_multiple}, waterfall_tiers[], per-party cashflows

---

### debt_sizing.py
**Skill:** loan-sizing-engine
**Purpose:** Sizes loan against simultaneous DSCR, LTV, and debt yield constraints. Identifies binding constraint and produces rate sensitivity grid.

```bash
python3 scripts/calculators/debt_sizing.py --json '{
    "noi": 1500000,
    "property_value": 20000000,
    "target_dscr": 1.25,
    "target_ltv": 0.65,
    "target_debt_yield": 0.09,
    "rate": 0.065,
    "amortization_years": 30,
    "io_years": 2
}'
```

**Input:** noi, property_value, target_dscr, target_ltv, target_debt_yield, rate, amortization_years, io_years
**Output:** sizing_results{max_loan_dscr, max_loan_ltv, max_loan_dy, binding_constraint, recommended_loan}, loan_metrics{dscr, ltv, debt_yield, cash_on_cash}, rate_sensitivity[]

---

### transfer_tax.py
**Skill:** transfer-document-preparer, funds-flow-calculator, title-commitment-reviewer
**Purpose:** State and local transfer tax for all 50 states + DC. Handles tiered rates (NY mansion tax, NJ graduated fee, WA REET tiers, HI conveyance tax, DC recordation).

```bash
python3 scripts/calculators/transfer_tax.py --json '{
    "state": "NY",
    "county": "New York",
    "purchase_price": 15000000,
    "property_type": "commercial"
}'
```

**Input:** state (2-letter code), county (optional), purchase_price, property_type (commercial|residential)
**Output:** state_tax, city_tax, mansion_tax, total_tax, buyer_portion, seller_portion, effective_rate_pct, notes

---

### quick_screen.py
**Skill:** deal-quick-screen
**Purpose:** Back-of-napkin deal screening with KEEP/KILL/MAYBE verdict. Calculates cap rate, price per unit/SF, DSCR, cash-on-cash, replacement cost ratio, and 3-scenario IRR estimates (bull/base/bear).

```bash
python3 scripts/calculators/quick_screen.py --json '{
    "purchase_price": 8500000,
    "noi": 510000,
    "units_or_sf": 48,
    "unit_type": "units",
    "market_rent_per_unit": 1350,
    "in_place_rent_per_unit": 1100,
    "loan_amount": 5525000,
    "rate": 0.065,
    "amort_years": 30,
    "replacement_cost_estimate": 10500000,
    "property_type": "multifamily"
}'
```

**Input:** purchase_price, noi, units_or_sf, unit_type (units|sf), market_rent_per_unit, in_place_rent_per_unit, loan_amount, rate, amort_years, replacement_cost_estimate, hold_years, target_irr
**Output:** verdict (KEEP|KILL|MAYBE), kill_reasons[], keep_reasons[], metrics{}, scenarios{bull, base, bear}
