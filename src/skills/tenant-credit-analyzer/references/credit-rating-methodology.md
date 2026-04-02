# Credit Rating Methodology Reference

## Rating Scale Equivalency

The three major rating agencies use similar but not identical scales. This table provides cross-agency equivalencies and the corresponding internal tier used in tenant-credit-analyzer.

| S&P | Moody's | Fitch | Internal Tier | Description |
|---|---|---|---|---|
| AAA | Aaa | AAA | Tier A | Highest quality; near-zero default probability |
| AA+ | Aa1 | AA+ | Tier A | Very high quality |
| AA | Aa2 | AA | Tier A | Very high quality |
| AA- | Aa3 | AA- | Tier A | Very high quality |
| A+ | A1 | A+ | Tier A | High quality; some sensitivity to economic conditions |
| A | A2 | A | Tier A | High quality |
| A- | A3 | A- | Tier A | High quality |
| BBB+ | Baa1 | BBB+ | Tier A | Investment grade; adequate protection |
| BBB | Baa2 | BBB | Tier A | Investment grade; moderate credit risk |
| BBB- | Baa3 | BBB- | Tier A (IG floor) | Lowest investment grade; more sensitive to conditions |
| BB+ | Ba1 | BB+ | Near-IG | Speculative; substantial credit risk |
| BB | Ba2 | BB | Tier B | Speculative; substantial credit risk |
| BB- | Ba3 | BB- | Tier B | Speculative; substantial credit risk |
| B+ | B1 | B+ | Tier C | Speculative; high credit risk |
| B | B2 | B | Tier C | Speculative; high credit risk |
| B- | B3 | B- | Tier C | Speculative; very high credit risk |
| CCC+ | Caa1 | CCC+ | Tier D | Near distress; dependent on favorable conditions |
| CCC | Caa2 | CCC | Tier D | Near distress |
| CCC- | Caa3 | CCC- | Tier D | Near distress |
| CC | Ca | CC | Tier D | Highly speculative |
| C | C | C | Tier D | Imminent default |
| D | C | D | Tier D | In default |
| NR | NR | NR | Tier C or D | Not rated -- assess via shadow rating |

**Notes:**
- Walgreens example: Moody's Baa2 = S&P BBB equivalent = Tier A (IG floor)
- Dollar General: S&P BBB = Tier A
- AMC Theatres: historically B/CCC range = Tier C/D
- Local businesses without ratings: Shadow-rate using financial ratios (see SKILL.md Workflow 2)

---

## Cumulative Default Probability Tables

Source: Moody's Average Cumulative Default Rates (1970-2023) and S&P Global Default Studies. These are average rates across a full credit cycle; actual rates vary significantly by economic regime.

### Investment Grade

| Rating | 1-Year | 2-Year | 3-Year | 5-Year | 7-Year | 10-Year |
|---|---|---|---|---|---|---|
| Aaa/AAA | 0.00% | 0.01% | 0.01% | 0.07% | 0.10% | 0.20% |
| Aa/AA | 0.02% | 0.04% | 0.07% | 0.15% | 0.25% | 0.40% |
| A/A | 0.06% | 0.13% | 0.20% | 0.40% | 0.65% | 0.90% |
| Baa1/BBB+ | 0.12% | 0.30% | 0.52% | 0.85% | 1.40% | 2.00% |
| Baa2/BBB | 0.18% | 0.42% | 0.65% | 1.10% | 1.80% | 2.50% |
| Baa3/BBB- | 0.25% | 0.55% | 0.90% | 1.50% | 2.40% | 3.50% |

**Practical note for CRE underwriting:** BBB-rated tenants (Walgreens, Dollar General, many national retailers) have a 5-year cumulative default probability of roughly 1-1.5%. In a CMBS underwriting context, this maps to a probability-weighted income haircut of well under 2% -- effectively treated as credit-certain for base case. The risk is refinancing/renewal risk at lease end, not mid-lease default.

### High Yield (Speculative Grade)

| Rating | 1-Year | 2-Year | 3-Year | 5-Year | 7-Year | 10-Year |
|---|---|---|---|---|---|---|
| Ba1/BB+ | 0.60% | 1.70% | 3.00% | 5.00% | 8.00% | 11.00% |
| Ba2/BB | 0.90% | 2.30% | 3.90% | 6.50% | 10.00% | 14.00% |
| Ba3/BB- | 1.20% | 3.00% | 5.00% | 8.00% | 12.00% | 17.00% |
| B1/B+ | 2.50% | 6.00% | 9.00% | 13.00% | 18.00% | 24.00% |
| B2/B | 3.50% | 7.50% | 10.50% | 15.00% | 20.00% | 26.00% |
| B3/B- | 5.00% | 10.00% | 14.00% | 19.00% | 25.00% | 32.00% |
| Caa1/CCC+ | 9.00% | 18.00% | 25.00% | 35.00% | 44.00% | 53.00% |
| Caa2/CCC | 15.00% | 25.00% | 33.00% | 44.00% | 53.00% | 61.00% |
| Caa3/CCC- | 22.00% | 32.00% | 40.00% | 52.00% | 60.00% | 68.00% |

### Shadow-Rated (Non-Rated Tenants Assessed via Financial Ratios)

These are internally assigned probabilities calibrated to match similarly-rated historical cohorts. Use as base case; apply qualitative adjustments (+/- 5 percentage points) for business quality, market position, and local competitive dynamics.

| Shadow Rating | Assigned On | 1-Year | 3-Year | 5-Year | 10-Year |
|---|---|---|---|---|---|
| Shadow A | Strong financials, healthy ratios, positive trends | 0.10% | 0.50% | 1.00% | 2.50% |
| Shadow B | Adequate financials, stable ratios, flat trends | 1.00% | 4.00% | 8.00% | 15.00% |
| Shadow C | Weak financials, stressed ratios, any declining trend | 5.00% | 14.00% | 22.00% | 35.00% |
| Shadow D | Thin financials, failed ratio thresholds | 12.00% | 25.00% | 35.00% | 50.00% |
| No Data / Unrated Assumed | No financials, no rating | 20.00% | 35.00% | 45.00% | 60.00% |

**Important caveat:** Shadow ratings for small local businesses (restaurants, salons, specialty retail) should incorporate sector-level stress. Individual business default rates for small retail are structurally higher than shadow rating tables imply. In periods of macroeconomic stress, small business default rates can reach 15-25% in a single year. The "No Data / Unrated Assumed" row reflects this conservatism.

---

## Recovery Rate Assumptions

Recovery rates represent the percentage of lost rent income recovered through re-leasing, guaranty enforcement, or bankruptcy settlement after a tenant default. These are underwriting assumptions, not contractual guarantees.

### By Lease Type and Property Type

| Asset Type | Tenant Quality | Recovery Rate | Key Drivers |
|---|---|---|---|
| NNN Single-Tenant Retail (freestanding) | IG (BBB- or better) | 75-85% | Low dark period, strong re-leasing demand for credit-tenant shell |
| NNN Single-Tenant Retail (freestanding) | HY / Non-rated | 45-65% | Dark period 9-18 months; re-leasing may require conversion |
| Multi-Tenant Strip Retail (anchor) | IG anchor | 70-80% | Anchor space highly marketable to replacement anchor |
| Multi-Tenant Strip Retail (anchor) | HY/NR anchor | 35-55% | Replacement timeline 12-24 months; co-tenancy cascade risk |
| Multi-Tenant Strip Retail (inline) | Any | 30-55% | Inline space has shallow demand pool; concessions required |
| Grocery-Anchored Retail (anchor) | IG (grocery) | 80-90% | Grocery anchor spaces highly sought-after |
| Power Center (big box) | IG | 60-75% | Big box conversions common but lengthy |
| Power Center (big box) | HY/NR | 25-50% | Dark value significant; conversion cost high |
| Class A Office | IG tenant | 65-80% | Core CBD office retains demand in quality assets |
| Class A Office | HY/NR tenant | 45-60% | Longer dark period in soft office markets |
| Class B/C Office | Any | 30-55% | Elevated re-leasing risk; TI concessions required |
| Industrial (Class A logistics) | IG tenant | 70-85% | High demand; logistics space re-leases quickly |
| Industrial (Class A logistics) | HY/NR tenant | 55-70% | Functional space; lease-up timeline 3-9 months |
| Industrial (specialty: cold storage, data center shell) | Any | 50-70% | Specialty re-leasing to limited tenant pool |

### By Dark Period and TI/LC Costs

Recovery rate is reduced by the economic cost of:
1. **Dark period carrying costs**: Operating expenses (NNN) or lost NOI (gross), taxes, insurance during vacancy
2. **TI allowance**: New tenant improvement allowance for replacement tenant
3. **Leasing commissions**: Broker fees for re-leasing (typically 4-6% of aggregate rent)
4. **Rent concessions**: Free rent periods granted to replacement tenant

**Quick estimation formula:**
```
Effective Recovery Rate = 1 - (Dark Period Months / 12) * (Operating Cost % of Annual Rent)
                            - (TI Cost / Annual Rent)
                            - (LC Rate * Total New Rent)

Example: Inline retail, 12-month dark period, $25/SF TI, 5% LC on $30/SF * 5-year lease
  Dark period cost: 12/12 * 15% = 15%
  TI cost: $25 / ($30 * 5) = 16.7% of total rent
  LC: 5% * $30 * 5 = 7.5 / $150 = 5%
  Total cost: 36.7%
  Recovery rate: 63.3% (before guaranty)
```

---

## Assessing Non-Rated Tenants: Financial Ratio Scoring

When no credit rating is available, use this structured scoring matrix to assign a shadow rating. Score each factor and sum to determine tier.

### Scoring Matrix (100 points total)

| Factor | Weight | Score Criteria |
|---|---|---|
| Current Ratio | 20 pts | > 2.0 = 20, 1.5-2.0 = 15, 1.0-1.5 = 8, < 1.0 = 0 |
| Debt-to-EBITDA | 20 pts | < 2.0x = 20, 2.0-3.5x = 15, 3.5-5.0x = 8, > 5.0x = 0 |
| Revenue Trend (3yr) | 20 pts | > 10% CAGR = 20, 0-10% = 15, -5-0% = 8, < -5% = 0 |
| EBITDA Margin | 20 pts | > 20% = 20, 10-20% = 15, 5-10% = 8, < 5% = 0 |
| Rent Coverage (EBITDA/Rent) | 15 pts | > 3.0x = 15, 2.0-3.0x = 11, 1.5-2.0x = 6, < 1.5x = 0 |
| Business Tenure | 5 pts | > 10 years = 5, 5-10 years = 4, 3-5 years = 2, < 3 years = 0 |

**Total score to shadow rating:**
```
80-100: Shadow A (equivalent ~BBB performance)
60-79:  Shadow B (equivalent ~BB performance)
35-59:  Shadow C (equivalent ~B performance)
0-34:   Shadow D (equivalent ~CCC performance)
```

### Qualitative Adjustments (apply after scoring)

Add or subtract points (max +/- 10) for:

| Adjustment | Points |
|---|---|
| Essential services business (pharmacy, medical, grocery, auto service) | +5 |
| Exclusive territorial rights (franchise with protected territory) | +3 |
| Long-term established location (> 15 years at this address) | +5 |
| Secular decline industry (video rental, legacy print, traditional department store) | -8 |
| Single-location dependent (all revenue from this one location) | -5 |
| Key-person dependency (owner-operated; no succession plan) | -3 |
| Recently opened (< 2 years at this location, still in ramp-up) | -5 |
| Active litigation or regulatory action | -8 |

### Data Quality Flags

If financial data is available but of poor quality, apply a data quality discount:

| Data Quality | Adjustment |
|---|---|
| CPA-audited financial statements | No discount |
| CPA-reviewed statements (not audited) | -5 points |
| Internally prepared statements | -10 points |
| Tax returns only (no prepared statements) | -8 points |
| Verbal / partial data only | Assign Tier D automatically |

---

## Rating Action Monitoring

For rated tenants, track the following events that warrant reassessment of credit tier:

| Event | Action Required |
|---|---|
| Downgrade crossing IG/HY boundary (BBB- to BB+) | Immediate reassessment; update default probability; review co-tenancy triggers |
| Rating placed on CreditWatch Negative | Treat as one notch worse for underwriting purposes |
| Rating placed on CreditWatch Positive | No change until confirmed upgrade |
| Downgrade of 2+ notches in 12 months | Flag as fallen angel risk; trigger co-tenancy and guaranty review |
| Parent entity downgrade (where subsidiary is tenant) | Reassess parent guaranty quality |
| Bankruptcy filing (Chapter 11) | Lease is at risk; initiate recovery analysis; consult counsel on rejection risk |
| Bankruptcy filing (Chapter 7) | Assume lease rejection; model re-leasing scenario immediately |

**Rating source hierarchy for CRE underwriting:**
1. S&P senior unsecured long-term issuer credit rating
2. Moody's long-term issuer rating
3. Fitch issuer default rating
4. NRSRO ratings from Kroll, DBRS (Morningstar) if S&P/Moody's/Fitch unavailable
5. D&B PAYDEX score (use only as supplementary data, not primary credit assessment)

When ratings differ across agencies, use the lower of the two primary ratings (S&P and Moody's) for underwriting conservatism.
