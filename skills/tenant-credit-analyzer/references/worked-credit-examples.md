# Worked Credit Examples

Three full walkthroughs for the tenant-credit-analyzer skill. Each example covers a distinct asset configuration: single-tenant NNN industrial, multi-tenant retail, and multi-tenant office. All calculations shown step by step.

---

## Example 1: Single-Tenant NNN Industrial -- FedEx Ground (Rated BBB)

### Asset Profile

| Parameter | Value |
|---|---|
| Property type | Industrial / Distribution |
| GLA | 185,000 SF |
| Location | Suburban Indianapolis (Tier 2 market) |
| Lease type | NNN (absolute net) |
| Tenant | FedEx Ground Package System, Inc. |
| Parent | FedEx Corporation |
| Tenant rating | S&P BBB / Moody's Baa2 (as of underwriting) |
| Annual base rent | $1,295,000 ($7.00/SF) |
| Lease commencement | January 2021 |
| Lease expiration | December 2035 (15-year initial term) |
| Remaining term at acquisition | 11.5 years |
| Renewal options | Two 5-year options at fair market rent |
| Guaranty | Corporate guaranty from FedEx Corporation (S&P BBB) |
| Acquisition price | $18,500,000 |
| Going-in cap rate | 7.0% ($1,295,000 / $18,500,000) |

---

### Step 1: Tier Assignment

FedEx Ground is a subsidiary of FedEx Corporation. Confirm:
- Operating entity: FedEx Ground Package System, Inc. (subsidiary)
- Guarantor: FedEx Corporation (parent)
- Parent rating: S&P BBB, Moody's Baa2

Tiering: Tier A (Investment Grade) via parent corporate guaranty.

Key consideration: The operating entity (FedEx Ground) does not itself carry a public rating, but the parent guaranty from rated FedEx Corp elevates the credit to parent level. This is standard for national logistics operators who franchise or subsidiary their real estate obligations.

### Step 2: Concentration Risk (Single-Tenant)

Single tenant = 100% of rent. HHI = 10,000 (maximum possible).

This asset must be underwritten as a single-tenant NNN. The valuation is entirely driven by: (a) FedEx Corp credit quality, (b) remaining lease term, and (c) dark value (re-leaseability of the building if FedEx vacates).

HHI = 10,000. Treat as single-tenant NNN throughout.

### Step 3: WALT

Single tenant. WALT = remaining lease term = 11.5 years.

WALT-Weighted Credit Score = 90 (Tier A score, 11.5-year duration).

Equivalent: Investment Grade (BBB equivalent). This is the strongest possible WALT-weighted score for a single-tenant asset.

### Step 4: Rent Coverage Analysis

FedEx Corp (consolidated financials, fiscal year 2024):
- Revenue: $87.7 billion
- EBITDA: ~$8.5 billion (margin ~9.7%)
- Annual rent at this property: $1,295,000

OCR (property-level): $1,295,000 / $87,700,000,000 = 0.0015% of corporate revenue.

This metric is economically meaningless at the corporate level for a BBB-rated company. For single-tenant NNN IG assets, the relevant coverage question is: can FedEx service its entire real estate portfolio obligations? The answer is yes for a BBB-rated company at this scale.

Industrial OCR benchmark (logistics): 2-5% of gross revenue. FedEx Ground's gross revenue attributable to the Indianapolis hub is not disclosed but estimated at $200-500M based on facility size and throughput. Implied OCR: 0.3-0.6%. Well below the 7% flag threshold.

Rent Coverage Ratio: Not computable at facility level. Default to rating-implied assessment: BBB-rated parent, systemically important logistics operation, rent coverage assumed adequate. No flag.

### Step 5: Default Probability

Rating: S&P BBB (equivalent Baa2) for parent guarantor.

From credit-rating-methodology.md:
```
Baa2/BBB cumulative default probabilities:
  1-year:  0.18%
  3-year:  0.65%
  5-year:  1.10%
  10-year: 2.50%
  11.5-yr: ~2.80% (interpolated)
```

Recovery rate (NNN industrial, IG tenant, Tier 2 market):
- Base rate: 70-80%
- Market tier adjustment (Tier 2): 0%
- Expected recovery: 75%

Expected loss over remaining lease term (11.5 years):
```
PD (11.5yr): ~2.80%
Recovery: 75%
Annual rent: $1,295,000
Exposure: $1,295,000 * 11.5 = $14,892,500 (undiscounted)
Expected Loss: 2.80% * (1 - 75%) * $14,892,500 = $104,248
Annualized: $9,065
As % of annual rent: 0.7%
```

Underwriting implication: Credit loss reserve of ~$9,000/year (less than 1% of rent) is adequate. The risk is not mid-lease default -- it is renewal risk at expiration in 2035.

### Step 6: Renewal Risk Analysis

FedEx has two 5-year renewal options at fair market rent. Key renewal risk factors:
- Industrial demand in Indianapolis remains strong (Tier 2 logistics hub)
- FedEx Ground occupies this facility within its network; voluntarily exiting would require operational restructuring
- However, 11.5 years is long -- FedEx could restructure its network hub strategy over that time

Renewal sensitivity: If FedEx does not renew at lease expiration (2035), dark period estimated at 6-9 months for a Class A industrial asset in Indianapolis. Re-leasing at market rent ($6.50-7.50/SF, assuming modest growth) is achievable.

Dark value estimate: $1,295,000 * 11-12 months dark / 12 = $1,186,000-$1,295,000 in lost rent + $10-15 PSF TI for new tenant + 5% LC = $2.5-3.5M total re-leasing cost against $18.5M acquisition price (13-19% of value at risk in worst-case non-renewal).

### Step 7: Guaranty Analysis

Parent guaranty from FedEx Corporation (BBB rated).
- Guaranty coverage ratio: FedEx EBITDA ($8.5B) / annual rent ($1.295M) = 6,563x. Immaterial.
- Guaranty quality: A (corporate parent, IG rated, full guaranty of lease obligations)
- Burn-off: No burn-off provision -- guaranty runs to lease expiration

### Red Flags: None

This is a textbook investment-grade single-tenant NNN industrial credit. The only risk is renewal risk at expiration.

### Underwriting Output Summary

| Metric | Value | Assessment |
|---|---|---|
| Tenant Tier | A (Investment Grade) | BBB parent guaranty |
| WALT | 11.5 years | Strong |
| WALT-Weighted Score | 90 | Investment Grade equivalent |
| HHI | 10,000 | Single-tenant risk |
| 5-Year Default Prob | 1.10% | Very low |
| 11.5-Year Default Prob | 2.80% | Low |
| Expected Loss (annual) | $9,065 | 0.7% of rent |
| Recovery Rate | 75% | Strong (IG + industrial) |
| OCR | 0.0015% (consolidated) | Not a binding constraint |
| Guaranty Quality | A | Full corporate guaranty |
| Recommended Credit Reserve | 0.5-1.0% of EGI | ~$6,500-$13,000/yr |

---

## Example 2: Multi-Tenant Retail -- Grocery-Anchored Strip with 4 Inline Tenants

### Asset Profile

| Parameter | Value |
|---|---|
| Property type | Neighborhood Retail Strip (Grocery-Anchored) |
| GLA | 52,000 SF |
| Location | Suburban Atlanta (Tier 2 market) |
| Lease type | Modified gross (anchor NNN; inline modified gross) |
| Acquisition price | $9,750,000 |
| Total occupied GLA | 46,200 SF (89% occupancy) |
| Total base rent | $621,000 annually |
| Vacancy | 5,800 SF (inline) |

### Tenant Rent Roll

| Tenant | SF | % GLA | Annual Rent | Rent/SF | Lease End | Rating | Type |
|---|---|---|---|---|---|---|---|
| Publix Super Markets | 28,000 | 53.8% | $308,000 | $11.00 | 2032 (7.5yr) | A- (S&P) | NNN Anchor |
| Chipotle Mexican Grill | 2,400 | 4.6% | $96,000 | $40.00 | 2029 (4.5yr) | BB+ (S&P) | NNN Modified Gross |
| Regional Bank Branch | 3,200 | 6.2% | $115,200 | $36.00 | 2027 (2.5yr) | NR (private bank) | NNN |
| Hair Salon (owner-operated) | 1,800 | 3.5% | $54,000 | $30.00 | 2026 (1.5yr) | No data | Modified Gross |
| Nail Salon (owner-operated) | 1,800 | 3.5% | $47,700 | $26.50 | 2025 (0.5yr) | No data | Modified Gross |
| Vacant | 5,800 | 11.2% | $0 | -- | -- | -- | -- |
| **TOTAL (occupied)** | **46,200** | | **$620,900** | | | | |

---

### Step 1: Tier Assignment

| Tenant | Tier | Basis |
|---|---|---|
| Publix (49.6% of rent) | Tier A | S&P A-; essential grocery; strong financials |
| Chipotle (15.5% of rent) | Tier B | S&P BB+; near-IG; strong brand and unit economics |
| Regional Bank (18.6% of rent) | Tier B (shadow) | Private bank; financials available; solid ratios assumed (request) |
| Hair Salon (8.7% of rent) | Tier C | Owner-operated; financials requested; established 7 years |
| Nail Salon (7.7% of rent) | Tier D | Owner-operated; lease expiring in 6 months; no data |

Note: Nail salon lease expires in 0.5 years. Treat as effectively vacant for underwriting purposes unless renewal is confirmed.

### Step 2: Concentration Risk

**HHI Calculation (occupied tenants, treating Nail Salon as at risk):**

Using 4 confirmed tenants + vacancy allocation:
```
Publix:          49.6% -> 0.496^2 * 10,000 = 2,460
Chipotle:        15.5% -> 0.155^2 * 10,000 = 240
Regional Bank:   18.6% -> 0.186^2 * 10,000 = 346
Hair Salon:       8.7% -> 0.087^2 * 10,000 = 76
Nail Salon:       7.7% -> 0.077^2 * 10,000 = 59

HHI = 3,181 (high concentration; Publix is the dominant driver)
```

Interpretation: Despite having 5 tenants, this strip is effectively Publix-dependent. HHI > 2,500 means Publix's credit and renewal decision drives ~75% of asset value.

**Lease expiration schedule:**
```
2025 (0.5yr):   Nail Salon   $47,700  7.7%  Imminent rollover risk
2026 (1.5yr):   Hair Salon   $54,000  8.7%
2027 (2.5yr):   Regional Bk  $115,200 18.6%
2029 (4.5yr):   Chipotle     $96,000  15.5%
2032 (7.5yr):   Publix       $308,000 49.6%
```

Flag: 35% of occupied rent rolls within 2.5 years (Nail Salon + Hair Salon + Regional Bank). Lease expiration clustering risk is elevated. Any buyer must underwrite sequential re-leasing of 3 tenants.

**Co-tenancy check:** Confirm whether any inline tenant leases contain co-tenancy provisions linked to Publix. In grocery-anchored centers, co-tenancy clauses are common for inline food/beverage tenants.

Assume (pending lease abstract review):
- Chipotle: likely has co-tenancy provision tying to "grocery anchor operating and open." If Publix closes, Chipotle can reduce rent or terminate.
- Regional Bank: unlikely to have co-tenancy provision; bank branches are destination traffic.
- Hair Salon / Nail Salon: confirm. Local operators often lack leverage to negotiate co-tenancy but some older leases may include them.

### Step 3: WALT Calculation

Treating Nail Salon as confirmed renewal (optimistic):
```
Publix:         $308,000 * 7.5 = 2,310,000
Chipotle:       $96,000  * 4.5 = 432,000
Regional Bank:  $115,200 * 2.5 = 288,000
Hair Salon:     $54,000  * 1.5 = 81,000
Nail Salon:     $47,700  * 0.5 = 23,850

Total weighted: 3,134,850
Total rent:     620,900
WALT:           3,134,850 / 620,900 = 5.05 years
```

WALT-Weighted Credit Score:
```
Publix (Tier A, score 90):        $308,000 * 7.5 * 90 = 207,900,000
Chipotle (near-IG, score 70):     $96,000  * 4.5 * 70 = 30,240,000
Regional Bank (shadow B, score 55): $115,200 * 2.5 * 55 = 15,840,000
Hair Salon (Tier C, score 35):    $54,000  * 1.5 * 35 = 2,835,000
Nail Salon (Tier D, score 15):    $47,700  * 0.5 * 15 = 357,750

Total score-weighted:  257,172,750
Total rent-term:       3,134,850
WALT-Weighted Score:   257,172,750 / 3,134,850 = 82.0
Equivalent: Investment Grade equivalent (score 80-100)
```

Score of 82.0 is strong for a multi-tenant retail asset, driven by Publix's dominant rent share and long lease. However, this masks the inline tenant rollover risk concentrated in 2025-2027.

**Renewal sensitivity:** If Regional Bank does not renew in 2027 (18.6% of rent):
```
Recalculate excluding Regional Bank:
  Publix (post-2027):    $308,000 * 5.0 * 90 = 138,600,000
  Chipotle (post-2027):  $96,000  * 2.0 * 70 = 13,440,000
  Hair Salon (expired):  $0
  Nail Salon (expired):  $0
  Score-weighted total:  152,040,000
  Rent-term total:       1,732,000 (Publix + Chipotle only)
  WALT-Weighted Score:   87.8
```
Post-rollover score actually increases slightly because Publix and Chipotle (higher credit scores) remain. But the absolute rent base drops 26%, and HHI rises to ~7,400 (Publix becomes 76% of remaining rent). This is the real risk: inline tenant non-renewal concentrates risk further in the anchor.

### Step 4: Default Probability and Expected Loss

| Tenant | 5-Yr PD | Recovery | Annual Rent | Expected Loss (5yr) | Annual EL |
|---|---|---|---|---|---|
| Publix (A-) | 0.40% | 85% | $308,000 | $924 | $185 |
| Chipotle (BB+) | 5.00% | 70% | $96,000 | $7,200 | $1,440 |
| Regional Bank (Shadow B) | 8.00% | 65% | $115,200 | $21,139 | $4,228 |
| Hair Salon (Tier C) | 22.00% | 35% | $54,000 | $38,610 | $7,722 |
| Nail Salon (Tier D) | 45.00% | 35% | $47,700 | $69,476 | $13,895 |
| **TOTAL** | | | **$620,900** | **$137,349** | **$27,470** |

Total 5-year portfolio expected loss: $137,349 = 4.4% of 5-year rent income.
Annual expected loss: $27,470 = 4.4% of annual EGI.

Recommendation: Credit/bad debt reserve of 3-5% of EGI annually. Standard underwriting (1-2% of EGI) would understate risk given inline tenant profile.

### Step 5: Anchor Default Scenario (Publix)

Probability: Publix 7.5-year cumulative PD at A- = ~0.60%.

If Publix vacates (dark or default):
1. Publix rent loss: $308,000/yr
2. Anchor dark period: 12-18 months (grocery anchor replacement takes time)
3. Co-tenancy triggers: Chipotle (15.5% of rent) -- assume 50% rent reduction during dark period = $48,000/yr loss
4. Hair salon / nail salon kick-out rights (if present): worst case $101,700/yr additional loss
5. Total revenue at risk during dark period: $308,000 + $48,000 + $101,700 = $457,700/yr
6. Dark period NOI impact (18 months): $457,700 * 1.5 = $686,550
7. Probability-weighted loss: 0.60% * $686,550 = $4,119

This is a low-probability scenario but devastating if it occurs. Acquisition underwriting should include a Publix non-renewal sensitivity at exit cap rate.

### Underwriting Output Summary

| Metric | Value | Assessment |
|---|---|---|
| Tenant Tier (Publix) | A (A-) | IG; anchor; drives asset value |
| Tenant Tier (Chipotle) | B (BB+) | Near-IG; strong brand economics |
| Tenant Tier (Regional Bank) | B (Shadow) | Adequate; short term remaining |
| Tenant Tier (Hair Salon) | C | Marginal; request financials |
| Tenant Tier (Nail Salon) | D | Imminent rollover; underwrite as vacant |
| HHI | 3,181 | High; Publix-dependent |
| WALT | 5.05 years | Adequate |
| WALT-Weighted Score | 82.0 | Investment Grade equivalent |
| Annual Expected Loss | $27,470 | 4.4% of EGI |
| Recommended Bad Debt Reserve | 4-5% of EGI | Higher than standard |
| Near-Term Rollover Risk | 35% of rent within 2.5yr | Elevated; budget TI/LC |

---

## Example 3: Multi-Tenant Office -- Law Firm Anchor + 3 Small Tenants

### Asset Profile

| Parameter | Value |
|---|---|
| Property type | Suburban Office (Class B) |
| Rentable Area | 38,500 SF |
| Location | Downtown Denver (Tier 2 market) |
| Lease type | Full-service gross (FSG) |
| Acquisition price | $7,350,000 |
| Occupancy | 82% (31,500 SF occupied) |
| Total base rent | $1,008,000 annually |

### Tenant Rent Roll

| Tenant | SF | % Rent | Annual Rent | Lease End | NAICS | Type |
|---|---|---|---|---|---|---|
| Hartley & Webb LLP (law firm) | 18,500 | 58.0% | $585,000 | 2030 (5.5yr) | 541110 | FSG |
| Regional Wealth Mgmt Firm | 7,000 | 22.0% | $221,760 | 2027 (2.5yr) | 523930 | FSG |
| Technology Startup | 3,500 | 10.0% | $100,800 | 2026 (1.5yr) | 541512 | FSG |
| Consulting Firm (2 employees) | 2,500 | 10.0% | $100,800 | 2025 (0.5yr) | 541611 | FSG |
| Vacant | 7,000 | -- | -- | -- | -- | -- |
| **TOTAL (occupied)** | **31,500** | | **$1,008,360** | | | |

---

### Step 1: Tier Assignment

| Tenant | Tier | Basis |
|---|---|---|
| Hartley & Webb LLP (58% of rent) | Tier B (shadow A) | Law firm 45+ attorneys; 20+ year establishment; request financials |
| Regional Wealth Mgmt | Tier B (shadow) | 12-yr established; AUM-based revenue; request financials |
| Technology Startup | Tier C | Series B funded; 3 years operating; venture-backed but no profits |
| Consulting Firm (2-person) | Tier D | Minimal presence; 0.5yr to expiry; no data |

### Step 2: Concentration Risk

```
HHI:
Hartley & Webb:  58.0% -> 0.58^2 * 10,000 = 3,364
Wealth Mgmt:     22.0% -> 0.22^2 * 10,000 = 484
Tech Startup:    10.0% -> 0.10^2 * 10,000 = 100
Consulting:      10.0% -> 0.10^2 * 10,000 = 100

HHI = 4,048 (high; Hartley & Webb dominates)
```

Interpretation: With 58% of rent, Hartley & Webb is the dominant tenant. This is a law-firm-anchored office asset; underwrite accordingly.

**Industry sector risk check:**
- Hartley & Webb: Legal services (NAICS 541110). Stable; essential services; remote work impact lower for litigation/transactional law than knowledge-work generalist firms. No sector risk flag.
- Wealth Management: Financial services (NAICS 523930). Stable; AUM-based revenue has market exposure but not operational disruption.
- Technology Startup: Software (NAICS 541512). Applies -5 sector adjustment (remote work substitution risk; startup churn).
- Consulting (2-person): Management consulting (NAICS 541611). High key-person dependency.

**Lease expiration schedule:**
```
0.5yr:  Consulting Firm     $100,800   10.0%  Treat as vacant
1.5yr:  Tech Startup        $100,800   10.0%  Near-term rollover
2.5yr:  Wealth Mgmt         $221,760   22.0%  Significant rollover
5.5yr:  Hartley & Webb      $585,000   58.0%  Anchor -- critical
```

Flag: 42% of rent rolls within 2.5 years (Consulting + Tech Startup + Wealth Mgmt). Office rollover risk is elevated given Class B positioning and Denver's elevated office vacancy post-2023 hybrid work shift.

**Remote work / office density risk:** Hartley & Webb's 18,500 SF for 45+ attorneys implies ~411 SF/attorney. This is on the higher end, suggesting potential space rationalization risk at renewal. Flag for discussion with tenant representatives.

### Step 3: WALT

Treating Consulting as vacant:
```
Hartley & Webb:    $585,000 * 5.5 = 3,217,500
Wealth Mgmt:       $221,760 * 2.5 = 554,400
Tech Startup:      $100,800 * 1.5 = 151,200
Total weighted:    3,923,100
Total rent:        907,560 (excluding Consulting)
WALT:              3,923,100 / 907,560 = 4.32 years
```

WALT-Weighted Credit Score:
```
Hartley & Webb (Shadow A, score 85):    $585,000 * 5.5 * 85 = 273,487,500
Wealth Mgmt (Shadow B, score 55):       $221,760 * 2.5 * 55 = 30,492,000
Tech Startup (Tier C, score 35):        $100,800 * 1.5 * 35 = 5,292,000

Total score-weighted:    309,271,500
Total rent-term:         3,923,100
WALT-Weighted Score:     309,271,500 / 3,923,100 = 78.8
Equivalent: Near Investment Grade (BB+/BB)
```

Benchmark comparison: Class A office CBD = 60-75. This asset scores 78.8, above benchmark, primarily because the law firm anchor is a high-quality credit. However, the asset is Class B -- the benchmark premium reflects tenant quality, not building quality.

Hartley & Webb renewal sensitivity:
```
Exclude Hartley & Webb post-year 5.5:
  Remaining tenants (if renewed): Wealth Mgmt and Tech Startup
  Score-weighted: 30,492,000 + 5,292,000 = 35,784,000
  Rent-term remaining: 554,400 + 151,200 = 705,600
  Score: 35,784,000 / 705,600 = 50.7 (Speculative Grade)
```

This sensitivity reveals the true risk: if Hartley & Webb exits at expiration, the portfolio credit quality collapses from Near-IG to Speculative Grade. The asset's investment thesis depends heavily on Hartley & Webb renewal.

### Step 4: Financial Statement Analysis -- Hartley & Webb LLP

Request: 3-year P&L, balance sheet, and partner capital statements.

Assumed data (illustrative):
- FY2024 Revenue: $9.8M (2% growth over FY2023)
- FY2024 EBITDA: $2.4M (EBITDA margin: 24.5%)
- Current ratio: 1.65
- Debt-to-equity: 0.9x (mostly partner capital structure)
- Rent-to-revenue: $585,000 / $9,800,000 = 5.97%
- EBITDA / Rent: $2,400,000 / $585,000 = 4.10x

Scoring:
```
Current ratio 1.65 (1.5-2.0):       15 pts
D/E 0.9x (< 1.0, strong):           Full 20 pts -> map to D/EBITDA: 2,400,000/9,800,000*0.9 ~N/A
Revenue trend (2% CAGR, positive):  15 pts
EBITDA margin 24.5% (> 20%):        20 pts
Rent coverage 4.10x (> 3.0x):       15 pts
Business tenure > 20 years:         5 pts

Subtotal: 90 pts
Qualitative: +5 (established 20+ years at this location)
Sector: Legal services -- stable, no adjustment

Total: 95 pts -> Shadow A
```

Confirmation: Hartley & Webb warrants Shadow A (score 90), consistent with initial tier assignment.

OCR check: 5.97% of revenue. Benchmark for law firms: 8-14%. At 5.97%, rent is easily serviceable. The firm is not stressed.

### Step 5: Default Probability and Expected Loss

| Tenant | 5-Yr PD | Recovery | Annual Rent | Expected Loss (5yr) | Annual EL |
|---|---|---|---|---|---|
| Hartley & Webb (Shadow A) | 1.00% | 65% | $585,000 | $10,238 | $2,048 |
| Wealth Mgmt (Shadow B) | 8.00% | 50% | $221,760 | $44,352 | $8,870 |
| Tech Startup (Tier C) | 22.00% | 40% | $100,800 | $26,611 | $5,322 |
| Consulting (Tier D) | 45.00% | 35% | $100,800 | $29,484 | $5,897 |
| **TOTAL** | | | **$1,008,360** | **$110,685** | **$22,137** |

Notes:
- Recovery rate for office (Class B): 50-65% depending on sublease market and TI requirements
- Denver office market showed elevated sublease availability in 2023-2025; apply conservative end of recovery range

Annual expected loss: $22,137 = 2.2% of annual EGI. Lower than retail example because law firm anchor recovery is higher and base PD is lower.

Recommended bad debt reserve: 2.5-3.0% of EGI (slightly above expected loss to account for model uncertainty).

### Step 6: Hartley & Webb Non-Renewal Scenario

If H&W exits at lease end (2030):
- Annual rent lost: $585,000
- Office dark period (Class B, Denver): 12-24 months estimated
- TI for replacement tenant: $40-60/SF * 18,500 SF = $740,000-$1,110,000
- LC: 5% * $585,000 * 5yr new lease = $146,250
- Total re-leasing cost: $886,250-$1,256,250

Present value impact (at 7.5% discount rate, costs incurred in year 5.5):
- Dark period NOI loss (18 months): $585,000 * 1.5 = $877,500
- PV of re-leasing costs: $886,250 / (1.075)^5.5 = $591,000 (midpoint)
- Total PV impact: ~$1.47M

As % of acquisition price ($7,350,000): 20.0%. This is a material risk that must be reflected in the underwriting hold period and exit cap rate assumptions.

Mitigation: Initiate renewal discussions with Hartley & Webb 24-30 months before expiration. Consider offering TI allowance to incentivize early renewal.

### Guaranty Analysis

- Hartley & Webb: No corporate parent. Partnership structure. Personal guaranty from managing partner (standard for law firm leases). Request managing partner net worth statement.
- Wealth Mgmt: No parent. Confirm personal guaranty of principal.
- Tech Startup: Confirm whether venture investors (lead VC) provide any guaranty. Unlikely but worth checking.

Assuming managing partner of H&W has confirmed net worth of $4.2M:
- Annual rent obligation: $585,000
- Guaranty coverage: $4.2M / $585,000 = 7.2x. Well above 2x minimum and 5x strong threshold.
- Guaranty quality: C (personal guaranty, but strong coverage ratio)

### Underwriting Output Summary

| Metric | Value | Assessment |
|---|---|---|
| Law Firm Tier | Shadow A | Strong; revenue-backed; stable sector |
| HHI | 4,048 | High; law firm-dependent |
| WALT | 4.32 years | Moderate |
| WALT-Weighted Score | 78.8 | Near-IG equivalent |
| Non-Renewal Sensitivity (H&W) | 50.7 score | Speculative Grade |
| Annual Expected Loss | $22,137 | 2.2% of EGI |
| Near-Term Rollover Risk | 42% within 2.5yr | Elevated |
| H&W Non-Renewal PV Risk | ~$1.47M | 20% of acquisition price |
| Recommended Reserve | 2.5-3.0% EGI | Standard plus margin |
| Key Action | Initiate H&W renewal 30 months before 2030 | Critical hold period task |
