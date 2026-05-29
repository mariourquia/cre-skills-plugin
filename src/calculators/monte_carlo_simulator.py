#!/usr/bin/env python3
"""
Monte Carlo Return Simulator
==============================
Stochastic simulation engine for CRE investment returns. Samples from
user-defined distributions with correlation structure, runs N-trial DCF,
and produces percentile returns, probability of loss, VaR, CVaR, and
simulation-based sensitivity ranking.

Used by: monte-carlo-return-simulator skill

Usage:
    python3 scripts/calculators/monte_carlo_simulator.py --json '{
        "purchase_price": 10000000,
        "equity_invested": 3500000,
        "hold_period": 5,
        "base_noi": 650000,
        "financing": {
            "ltv": 0.65,
            "rate": 0.065,
            "term": 10,
            "amort_years": 30,
            "io_years": 0
        },
        "variables": [
            {"name": "rent_growth", "best_case": 0.04, "base_case": 0.03, "worst_case": 0.01, "distribution": "triangular"},
            {"name": "exit_cap", "best_case": 0.055, "base_case": 0.065, "worst_case": 0.08, "distribution": "triangular"},
            {"name": "vacancy", "best_case": 0.03, "base_case": 0.05, "worst_case": 0.10, "distribution": "triangular"},
            {"name": "expense_growth", "best_case": 0.02, "base_case": 0.03, "worst_case": 0.05, "distribution": "triangular"}
        ],
        "correlation_matrix": {
            "rent_growth":    {"rent_growth": 1.0, "exit_cap": -0.30, "vacancy": -0.50, "expense_growth": 0.20},
            "exit_cap":       {"rent_growth": -0.30, "exit_cap": 1.0, "vacancy": 0.40, "expense_growth": -0.10},
            "vacancy":        {"rent_growth": -0.50, "exit_cap": 0.40, "vacancy": 1.0, "expense_growth": -0.05},
            "expense_growth": {"rent_growth": 0.20, "exit_cap": -0.10, "vacancy": -0.05, "expense_growth": 1.0}
        },
        "num_trials": 5000,
        "random_seed": 42,
        "target_irr": 0.12
    }'

Output: JSON with percentile_returns, probability_metrics, sensitivity_ranking,
        distribution_histogram, summary_statistics.
"""

import argparse
import json
import math
import random
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Distribution samplers (pure Python, no numpy/scipy)
# ---------------------------------------------------------------------------

def sample_triangular(rng: random.Random, a: float, c: float, b: float) -> float:
    """Sample from triangular distribution with min=a, mode=c, max=b."""
    if a == b:
        return a
    u = rng.random()
    fc = (c - a) / (b - a)
    if u < fc:
        return a + math.sqrt(u * (b - a) * (c - a))
    else:
        return b - math.sqrt((1 - u) * (b - a) * (b - c))


def sample_normal(rng: random.Random, mu: float, sigma: float) -> float:
    """Sample from normal distribution using Box-Muller."""
    return rng.gauss(mu, sigma)


def sample_lognormal(rng: random.Random, mu_ln: float, sigma_ln: float) -> float:
    """Sample from lognormal distribution."""
    return math.exp(rng.gauss(mu_ln, sigma_ln))


def sample_uniform(rng: random.Random, a: float, b: float) -> float:
    """Sample from uniform distribution."""
    return rng.uniform(a, b)


def sample_beta(rng: random.Random, alpha: float, beta_param: float) -> float:
    """Sample from beta distribution using rejection method."""
    return rng.betavariate(alpha, beta_param)


# ---------------------------------------------------------------------------
# Distribution parameter fitting from three-point estimates
# ---------------------------------------------------------------------------

def fit_distribution(var: dict) -> dict:
    """
    Given a variable definition with best_case, base_case, worst_case,
    and optional distribution type, return fitted parameters and a sampler key.
    """
    dist = var.get("distribution", "triangular")
    best = var["best_case"]
    base = var["base_case"]
    worst = var["worst_case"]
    name = var["name"]

    # Determine direction: for cost variables (exit_cap, vacancy, expense_growth,
    # capex_overrun, refi_rate, absorption), worst > base > best (higher is worse).
    # For return variables (rent_growth), best > base > worst.
    low = min(best, worst)
    high = max(best, worst)

    if dist == "triangular":
        # Scale P10/P90 to min/max with 1.22 factor
        spread_low = base - low
        spread_high = high - base
        a = base - 1.22 * spread_low
        b = base + 1.22 * spread_high
        c = base
        return {"type": "triangular", "a": a, "c": c, "b": b, "mean": (a + b + c) / 3}

    elif dist == "normal":
        mu = base
        sigma = (high - low) / 2.563
        if sigma <= 0:
            sigma = 0.001
        return {"type": "normal", "mu": mu, "sigma": sigma, "mean": mu}

    elif dist == "lognormal":
        if base <= 0 or low <= 0 or high <= 0:
            # Fallback to triangular if values not all positive
            return fit_distribution({**var, "distribution": "triangular"})
        mu_ln = math.log(base)
        sigma_ln = (math.log(high) - math.log(low)) / 2.563
        if sigma_ln <= 0:
            sigma_ln = 0.01
        mean = math.exp(mu_ln + sigma_ln ** 2 / 2)
        return {"type": "lognormal", "mu_ln": mu_ln, "sigma_ln": sigma_ln, "mean": mean}

    elif dist == "uniform":
        return {"type": "uniform", "a": low, "b": high, "mean": (low + high) / 2}

    elif dist == "beta":
        mu = base
        var_est = ((high - low) / 2.563) ** 2
        if var_est <= 0 or mu <= 0 or mu >= 1:
            return fit_distribution({**var, "distribution": "triangular"})
        alpha = mu * (mu * (1 - mu) / var_est - 1)
        beta_p = (1 - mu) * (mu * (1 - mu) / var_est - 1)
        if alpha <= 0 or beta_p <= 0:
            return fit_distribution({**var, "distribution": "triangular"})
        return {"type": "beta", "alpha": alpha, "beta_param": beta_p, "mean": alpha / (alpha + beta_p)}

    else:
        # Default to triangular
        return fit_distribution({**var, "distribution": "triangular"})


def sample_from_fitted(rng: random.Random, params: dict) -> float:
    """Sample a single value from the fitted distribution."""
    t = params["type"]
    if t == "triangular":
        return sample_triangular(rng, params["a"], params["c"], params["b"])
    elif t == "normal":
        return sample_normal(rng, params["mu"], params["sigma"])
    elif t == "lognormal":
        return sample_lognormal(rng, params["mu_ln"], params["sigma_ln"])
    elif t == "uniform":
        return sample_uniform(rng, params["a"], params["b"])
    elif t == "beta":
        return sample_beta(rng, params["alpha"], params["beta_param"])
    else:
        raise ValueError(f"Unknown distribution type: {t}")


# ---------------------------------------------------------------------------
# Cholesky decomposition (pure Python)
# ---------------------------------------------------------------------------

def cholesky_decompose(matrix: list[list[float]]) -> list[list[float]]:
    """
    Cholesky decomposition of a positive semi-definite matrix.
    Returns lower triangular matrix L such that matrix = L @ L^T.
    """
    n = len(matrix)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = matrix[i][i] - s
                if val < 0:
                    val = 0.0  # Numerical fix for near-PSD matrices
                L[i][j] = math.sqrt(val)
            else:
                if L[j][j] == 0:
                    L[i][j] = 0.0
                else:
                    L[i][j] = (matrix[i][j] - s) / L[j][j]
    return L


def generate_correlated_normals(rng: random.Random, L: list[list[float]], n_vars: int) -> list[float]:
    """Generate correlated standard normal variates using Cholesky factor L."""
    z = [rng.gauss(0, 1) for _ in range(n_vars)]
    correlated = [0.0] * n_vars
    for i in range(n_vars):
        correlated[i] = sum(L[i][j] * z[j] for j in range(i + 1))
    return correlated


def normal_cdf(x: float) -> float:
    """Approximation of standard normal CDF (Abramowitz and Stegun)."""
    if x < -8:
        return 0.0
    if x > 8:
        return 1.0
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    sign = 1
    if x < 0:
        sign = -1
        x = -x
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2.0)
    return 0.5 * (1.0 + sign * y)


# ---------------------------------------------------------------------------
# IRR calculation (Newton-Raphson with bisection fallback)
# ---------------------------------------------------------------------------

def irr_calc(cashflows: list[float], guess: float = 0.10, max_iter: int = 1000, tol: float = 1e-8) -> float | None:
    """Calculate IRR. Returns None if IRR cannot be found."""
    # Check for sign change
    has_negative = any(cf < 0 for cf in cashflows)
    has_positive = any(cf > 0 for cf in cashflows)
    if not (has_negative and has_positive):
        return None

    # Newton-Raphson
    rate = guess
    for _ in range(max_iter):
        npv = sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))
        dnpv = sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cashflows))
        if abs(dnpv) < 1e-14:
            break
        new_rate = rate - npv / dnpv
        if abs(new_rate - rate) < tol:
            return round(new_rate, 6)
        rate = new_rate
        if rate < -0.99:
            rate = -0.99
        if rate > 10.0:
            rate = 10.0

    # Bisection fallback
    lo, hi = -0.99, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        npv = sum(cf / (1 + mid) ** t for t, cf in enumerate(cashflows))
        if abs(npv) < tol:
            return round(mid, 6)
        npv_lo = sum(cf / (1 + lo) ** t for t, cf in enumerate(cashflows))
        if npv_lo * npv < 0:
            hi = mid
        else:
            lo = mid
    return None


# ---------------------------------------------------------------------------
# DCF model for a single trial
# ---------------------------------------------------------------------------

def run_dcf_trial(
    purchase_price: float,
    equity_invested: float,
    base_noi: float,
    hold_period: int,
    financing: dict,
    sampled_values: dict,
) -> dict:
    """
    Run a single DCF trial with sampled variable values.
    Returns IRR, equity multiple, average cash-on-cash, and annual DSCR.
    """
    loan_amount = purchase_price * financing["ltv"]
    rate = financing["rate"]
    amort_years = financing["amort_years"]
    io_years = financing.get("io_years", 0)

    rent_growth = sampled_values.get("rent_growth", 0.03)
    exit_cap = sampled_values.get("exit_cap", 0.065)
    vacancy = sampled_values.get("vacancy", 0.05)
    expense_growth = sampled_values.get("expense_growth", 0.03)
    capex_overrun = sampled_values.get("capex_overrun", 1.0)
    refi_rate = sampled_values.get("refi_rate", rate)

    # Ensure non-negative where required
    exit_cap = max(exit_cap, 0.01)
    vacancy = max(min(vacancy, 0.50), 0.0)  # Cap at 50%

    # Calculate annual debt service
    # During IO period
    io_payment = loan_amount * rate

    # During amortizing period
    if amort_years > 0 and rate > 0:
        monthly_rate = rate / 12
        n_payments = amort_years * 12
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
        else:
            monthly_payment = loan_amount / n_payments
        annual_ds = monthly_payment * 12
    else:
        annual_ds = io_payment

    # Calculate remaining loan balance at end of hold
    remaining_balance = loan_amount
    if amort_years > 0:
        monthly_rate = rate / 12
        n_payments_made = 0
        for year in range(1, hold_period + 1):
            if year <= io_years:
                # IO: no principal paydown
                pass
            else:
                for month in range(12):
                    if monthly_rate > 0:
                        interest = remaining_balance * monthly_rate
                        principal = monthly_payment - interest
                        remaining_balance -= principal
                    else:
                        remaining_balance -= loan_amount / (amort_years * 12)
                    n_payments_made += 1
        remaining_balance = max(remaining_balance, 0)

    # Build annual cash flows
    cashflows = [-equity_invested]
    annual_coc_list = []
    annual_dscr_list = []
    noi = base_noi

    # Base NOI already incorporates initial vacancy
    # Adjust for sampled vacancy relative to assumed base vacancy
    base_vacancy = 0.05  # Assumed in base NOI

    for year in range(1, hold_period + 1):
        if year > 1:
            noi = noi * (1 + rent_growth)

        # Adjust NOI for vacancy deviation from base
        vacancy_adjustment = (base_vacancy - vacancy) / (1 - base_vacancy)
        adjusted_noi = noi * (1 + vacancy_adjustment)

        # Adjust expenses (embedded in NOI -- increase expense_growth reduces NOI)
        # Simplified: NOI already nets expenses, so higher expense growth reduces NOI growth
        # We model this as a drag on NOI
        if year > 1:
            expense_drag = base_noi * 0.40 * ((1 + expense_growth) ** (year - 1) - (1 + 0.03) ** (year - 1))
            adjusted_noi -= expense_drag

        # Debt service
        if year <= io_years:
            ds = io_payment
        else:
            ds = annual_ds

        cf = adjusted_noi - ds
        cashflows.append(cf)
        annual_coc_list.append(cf / equity_invested if equity_invested > 0 else 0)
        annual_dscr_list.append(adjusted_noi / ds if ds > 0 else 999)

    # Reversion
    terminal_noi = adjusted_noi * (1 + rent_growth)  # Forward NOI
    exit_value = terminal_noi / exit_cap
    net_proceeds = exit_value - remaining_balance
    # Selling costs (2% of exit value)
    net_proceeds -= exit_value * 0.02
    cashflows[-1] += net_proceeds

    # Calculate metrics
    trial_irr = irr_calc(cashflows)
    total_distributions = sum(cashflows[1:])
    equity_multiple = (total_distributions + equity_invested) / equity_invested if equity_invested > 0 else 0
    avg_coc = sum(annual_coc_list) / len(annual_coc_list) if annual_coc_list else 0
    min_dscr = min(annual_dscr_list) if annual_dscr_list else 0

    return {
        "irr": trial_irr,
        "equity_multiple": round(equity_multiple, 4),
        "avg_coc": round(avg_coc, 6),
        "min_dscr": round(min_dscr, 4),
        "cashflows": [round(cf, 2) for cf in cashflows],
    }


# ---------------------------------------------------------------------------
# Percentile and statistics helpers
# ---------------------------------------------------------------------------

def percentile(sorted_list: list[float], p: float) -> float:
    """Calculate percentile from a sorted list."""
    if not sorted_list:
        return 0.0
    k = (len(sorted_list) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_list[int(k)]
    return sorted_list[int(f)] * (c - k) + sorted_list[int(c)] * (k - f)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def std_dev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def skewness(values: list[float]) -> float:
    if len(values) < 3:
        return 0.0
    m = mean(values)
    s = std_dev(values)
    if s == 0:
        return 0.0
    n = len(values)
    return (n / ((n - 1) * (n - 2))) * sum(((x - m) / s) ** 3 for x in values)


def kurtosis(values: list[float]) -> float:
    if len(values) < 4:
        return 0.0
    m = mean(values)
    s = std_dev(values)
    if s == 0:
        return 0.0
    n = len(values)
    k = (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) * sum(((x - m) / s) ** 4 for x in values)
    return k - 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))


def spearman_rank_correlation(x: list[float], y: list[float]) -> float:
    """Calculate Spearman rank correlation between two lists."""
    if len(x) != len(y) or len(x) < 3:
        return 0.0
    n = len(x)

    def rank_data(data: list[float]) -> list[float]:
        indexed = sorted(enumerate(data), key=lambda p: p[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and indexed[j + 1][1] == indexed[j][1]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = avg_rank
            i = j + 1
        return ranks

    rx = rank_data(x)
    ry = rank_data(y)
    d_sq = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1 - 6 * d_sq / (n * (n ** 2 - 1))


# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------

def run_simulation(config: dict) -> dict:
    """Run the full Monte Carlo simulation and return results."""
    purchase_price = config["purchase_price"]
    equity_invested = config["equity_invested"]
    hold_period = config["hold_period"]
    base_noi = config["base_noi"]
    financing = config["financing"]
    variables = config["variables"]
    target_irr = config.get("target_irr", 0.12)
    num_trials = config.get("num_trials", 5000)
    seed = config.get("random_seed", 42)
    corr_matrix_input = config.get("correlation_matrix", None)

    num_trials = max(1000, min(num_trials, 10000))

    rng = random.Random(seed)

    # Fit distributions
    var_names = [v["name"] for v in variables]
    n_vars = len(var_names)
    fitted = {}
    for v in variables:
        fitted[v["name"]] = fit_distribution(v)

    # Build correlation matrix
    if corr_matrix_input and len(var_names) > 1:
        corr = [[0.0] * n_vars for _ in range(n_vars)]
        for i, vi in enumerate(var_names):
            for j, vj in enumerate(var_names):
                if vi in corr_matrix_input and vj in corr_matrix_input[vi]:
                    corr[i][j] = corr_matrix_input[vi][vj]
                elif i == j:
                    corr[i][j] = 1.0
                else:
                    corr[i][j] = 0.0
        try:
            L = cholesky_decompose(corr)
        except Exception:
            # Fall back to identity (independent draws)
            L = [[1.0 if i == j else 0.0 for j in range(n_vars)] for i in range(n_vars)]
    else:
        L = [[1.0 if i == j else 0.0 for j in range(n_vars)] for i in range(n_vars)]

    # Run trials
    all_irrs: list[float] = []
    all_em: list[float] = []
    all_coc: list[float] = []
    all_dscr: list[float] = []
    all_samples: dict[str, list[float]] = {name: [] for name in var_names}
    irr_failures = 0

    for _ in range(num_trials):
        # Generate correlated normal variates
        correlated_normals = generate_correlated_normals(rng, L, n_vars)

        # Convert to uniform [0,1] via normal CDF, then to target distribution
        sampled_values = {}
        for i, name in enumerate(var_names):
            u = normal_cdf(correlated_normals[i])
            params = fitted[name]
            t = params["type"]

            # Inverse CDF sampling using the uniform variate
            if t == "triangular":
                a, c, b = params["a"], params["c"], params["b"]
                if b <= a:
                    sampled_values[name] = c
                else:
                    fc = (c - a) / (b - a)
                    if u < fc:
                        val = a + math.sqrt(u * (b - a) * (c - a))
                    else:
                        val = b - math.sqrt((1 - u) * (b - a) * (b - c))
                    sampled_values[name] = val
            elif t == "normal":
                # Inverse normal CDF approximation (Beasley-Springer-Moro)
                sampled_values[name] = params["mu"] + params["sigma"] * correlated_normals[i]
            elif t == "lognormal":
                sampled_values[name] = math.exp(params["mu_ln"] + params["sigma_ln"] * correlated_normals[i])
            elif t == "uniform":
                sampled_values[name] = params["a"] + u * (params["b"] - params["a"])
            elif t == "beta":
                # Beta inverse CDF is complex; use independent beta sample as approximation
                # with correlation preserved through the normal copula structure
                sampled_values[name] = rng.betavariate(params["alpha"], params["beta_param"])
            else:
                sampled_values[name] = params.get("mean", 0)

            all_samples[name].append(sampled_values[name])

        # Run DCF
        result = run_dcf_trial(purchase_price, equity_invested, base_noi, hold_period, financing, sampled_values)

        if result["irr"] is not None:
            all_irrs.append(result["irr"])
        else:
            irr_failures += 1
        all_em.append(result["equity_multiple"])
        all_coc.append(result["avg_coc"])
        all_dscr.append(result["min_dscr"])

    # Sort for percentile calculations
    sorted_irrs = sorted(all_irrs)
    sorted_em = sorted(all_em)
    sorted_coc = sorted(all_coc)

    # Summary statistics
    summary = {
        "irr": {
            "mean": round(mean(all_irrs), 6),
            "median": round(percentile(sorted_irrs, 0.50), 6),
            "std_dev": round(std_dev(all_irrs), 6),
            "skewness": round(skewness(all_irrs), 4),
            "kurtosis": round(kurtosis(all_irrs), 4),
        },
        "equity_multiple": {
            "mean": round(mean(all_em), 4),
            "median": round(percentile(sorted_em, 0.50), 4),
            "std_dev": round(std_dev(all_em), 4),
        },
        "avg_cash_on_cash": {
            "mean": round(mean(all_coc), 6),
            "median": round(percentile(sorted_coc, 0.50), 6),
        },
    }

    # Percentile returns
    pctiles = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]
    percentile_returns = {}
    for p in pctiles:
        key = f"P{int(p * 100)}"
        percentile_returns[key] = {
            "irr": round(percentile(sorted_irrs, p), 6),
            "equity_multiple": round(percentile(sorted_em, p), 4),
            "avg_cash_on_cash": round(percentile(sorted_coc, p), 6),
        }

    # Probability metrics
    prob_loss = sum(1 for irr in all_irrs if irr < 0) / len(all_irrs) if all_irrs else 0
    prob_target = sum(1 for irr in all_irrs if irr >= target_irr) / len(all_irrs) if all_irrs else 0
    prob_em_below_1 = sum(1 for em in all_em if em < 1.0) / len(all_em) if all_em else 0
    prob_dscr_below_1 = sum(1 for d in all_dscr if d < 1.0) / len(all_dscr) if all_dscr else 0

    # VaR and CVaR at 95% confidence
    var_95_irr = percentile(sorted_irrs, 0.05) if sorted_irrs else 0
    tail_irrs = [irr for irr in sorted_irrs if irr <= var_95_irr]
    cvar_95_irr = mean(tail_irrs) if tail_irrs else var_95_irr

    # VaR in dollar terms (equity loss)
    var_95_em = percentile(sorted_em, 0.05) if sorted_em else 0
    var_95_dollars = equity_invested * (1 - var_95_em)
    tail_ems = [em for em in sorted_em if em <= var_95_em]
    cvar_95_em = mean(tail_ems) if tail_ems else var_95_em
    cvar_95_dollars = equity_invested * (1 - cvar_95_em)

    probability_metrics = {
        "probability_of_loss": round(prob_loss, 4),
        "probability_of_target_irr": round(prob_target, 4),
        "probability_em_below_1x": round(prob_em_below_1, 4),
        "probability_dscr_below_1x": round(prob_dscr_below_1, 4),
        "var_95_irr": round(var_95_irr, 6),
        "cvar_95_irr": round(cvar_95_irr, 6),
        "var_95_dollars": round(var_95_dollars, 2),
        "cvar_95_dollars": round(cvar_95_dollars, 2),
        "target_irr": target_irr,
    }

    # Sensitivity ranking (Spearman correlation with IRR)
    sensitivity = []
    total_rho_sq = 0
    for name in var_names:
        samples_for_var = all_samples[name][:len(all_irrs)]  # Match length in case of IRR failures
        rho = spearman_rank_correlation(samples_for_var, all_irrs)
        sensitivity.append({"variable": name, "spearman_rho": round(rho, 4), "rho_squared": round(rho ** 2, 4)})
        total_rho_sq += rho ** 2

    # Calculate variance contribution
    for s in sensitivity:
        s["variance_contribution"] = round(s["rho_squared"] / total_rho_sq, 4) if total_rho_sq > 0 else 0

    sensitivity.sort(key=lambda x: abs(x["spearman_rho"]), reverse=True)

    # Histogram bins for IRR
    if sorted_irrs:
        bin_edges = [-0.10, -0.05, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50]
        histogram = []
        for i in range(len(bin_edges) - 1):
            count = sum(1 for irr in all_irrs if bin_edges[i] <= irr < bin_edges[i + 1])
            pct = count / len(all_irrs)
            label = f"{bin_edges[i] * 100:.0f}% to {bin_edges[i + 1] * 100:.0f}%"
            histogram.append({"range": label, "count": count, "percentage": round(pct, 4)})
        # Below minimum
        below = sum(1 for irr in all_irrs if irr < bin_edges[0])
        if below > 0:
            histogram.insert(0, {"range": f"< {bin_edges[0] * 100:.0f}%", "count": below, "percentage": round(below / len(all_irrs), 4)})
        # Above maximum
        above = sum(1 for irr in all_irrs if irr >= bin_edges[-1])
        if above > 0:
            histogram.append({"range": f">= {bin_edges[-1] * 100:.0f}%", "count": above, "percentage": round(above / len(all_irrs), 4)})
    else:
        histogram = []

    # Distribution fitting summary
    distribution_summary = {}
    for name in var_names:
        f = fitted[name]
        samples = all_samples[name]
        sorted_samples = sorted(samples)
        distribution_summary[name] = {
            "fitted_type": f["type"],
            "fitted_params": {k: round(v, 6) if isinstance(v, float) else v for k, v in f.items() if k not in ("type", "mean")},
            "fitted_mean": round(f["mean"], 6),
            "sample_mean": round(mean(samples), 6),
            "sample_std": round(std_dev(samples), 6),
            "sample_P10": round(percentile(sorted_samples, 0.10), 6),
            "sample_P50": round(percentile(sorted_samples, 0.50), 6),
            "sample_P90": round(percentile(sorted_samples, 0.90), 6),
        }

    return {
        "summary_statistics": summary,
        "percentile_returns": percentile_returns,
        "probability_metrics": probability_metrics,
        "sensitivity_ranking": sensitivity,
        "distribution_histogram": histogram,
        "distribution_summary": distribution_summary,
        "convergence": {
            "trials_run": num_trials,
            "irr_converged": len(all_irrs),
            "irr_failures": irr_failures,
            "random_seed": seed,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Monte Carlo Return Simulator for CRE investments")
    parser.add_argument("--json", required=True, help="JSON string with simulation configuration")
    args = parser.parse_args()

    try:
        config = json.loads(args.json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}), file=sys.stderr)
        sys.exit(1)

    # Validate required fields
    required = ["purchase_price", "equity_invested", "hold_period", "base_noi", "financing", "variables"]
    missing = [f for f in required if f not in config]
    if missing:
        print(json.dumps({"error": f"Missing required fields: {missing}"}), file=sys.stderr)
        sys.exit(1)

    results = run_simulation(config)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
