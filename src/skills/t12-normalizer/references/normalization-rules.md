# T-12 Normalization Rules Reference

Standard adjustments for trailing twelve-month operating statement normalization. Each rule includes rationale, calculation method, and worked examples using a 120-unit multifamily property with $2,400,000 GPR.

---

## 1. One-Time / Non-Recurring Item Removal

### Rule

Remove any revenue or expense item that is non-recurring and will not repeat under new ownership. These distort the trailing income stream.

### Common Items to Remove

**Revenue side:**
- Lease termination fees (one-time buyouts)
- Insurance proceeds from casualty events
- Legal settlement income
- Below-market lease buyouts

**Expense side:**
- Casualty repair costs (covered by insurance)
- Litigation costs / legal settlements
- Capital expenditure misclassified as operating expense
- Owner personal expenses run through the property
- One-time consulting fees (branding, repositioning studies)

### Worked Example

```
Reported T-12 Other Income: $185,000

Breakdown:
  Late fees:                $22,000  (recurring -- keep)
  Application fees:         $18,000  (recurring -- keep)
  Lease termination fee:    $75,000  (tenant bought out of lease -- remove)
  Insurance settlement:     $45,000  (roof damage claim -- remove)
  Pet fees:                 $25,000  (recurring -- keep)

Normalized other income: $185,000 - $75,000 - $45,000 = $65,000
Adjustment: -$120,000 (-64.9%)
```

```
Reported T-12 Repairs & Maintenance: $310,000

Breakdown:
  Routine maintenance:      $180,000  (recurring -- keep)
  Unit turns (15 units):    $52,500   (recurring -- keep, but check vs. average)
  Roof repair (storm):      $45,000   (one-time, insured -- remove)
  Parking lot repaving:     $32,500   (capital item -- remove, should be capex)

Normalized R&M: $310,000 - $45,000 - $32,500 = $232,500
Adjustment: -$77,500 (-25.0%)
```

---

## 2. Management Fee Restatement

### Rule

Restate the management fee to the market rate that a new owner will actually pay. Seller's fee may be below market (self-managed) or above market (related-party management company).

### Formula

```
Normalized management fee = Effective Gross Income * Market management fee rate

Market rates (multifamily):
  Institutional (200+ units):  2.5-3.5% of EGI
  Mid-size (50-200 units):     3.5-5.0% of EGI
  Small (< 50 units):          5.0-8.0% of EGI
  Single-family rental:        8.0-10.0% of gross rent
```

### Worked Example

```
Seller is self-managed. T-12 shows $0 management fee.

Reported EGI: $2,280,000
Market management fee rate: 3.5% (120-unit property)

Normalized management fee = $2,280,000 * 0.035 = $79,800

T-12 shows: $0
Normalized: $79,800
Adjustment: +$79,800 expense (reduces NOI)
```

```
Alternatively: Seller uses a related-party management company at 6.0%.

Reported fee: $2,280,000 * 0.06 = $136,800
Market rate: $2,280,000 * 0.035 = $79,800

Adjustment: -$57,000 expense (increases NOI)
```

---

## 3. Real Estate Tax Reassessment

### Rule

Real estate taxes must be restated to reflect the post-acquisition assessed value. Most jurisdictions reassess upon sale, often at or near the purchase price. The seller's tax bill reflects their (often lower) basis.

### Formula

```
Normalized taxes = (Purchase_price * Assessment_ratio * Millage_rate) + Special_assessments

Or if the jurisdiction provides a direct calculation:
Normalized taxes = Assessed_value * Tax_rate
```

### Worked Example

```
Seller purchased the property 12 years ago for $8,400,000.
Current assessed value: $9,200,000 (modest appreciation in assessments)
Current tax bill: $184,000 (millage: 20.0 mills = 2.0%)

Buyer's purchase price: $16,800,000
Jurisdiction reassesses at 100% of sale price.

New assessed value: $16,800,000
Normalized taxes: $16,800,000 * 0.020 = $336,000

Adjustment: +$152,000 expense ($336,000 - $184,000)
Impact: NOI reduced by $152,000

Note: Some jurisdictions cap annual assessment increases (e.g., California Prop 13
limits to 2%/year). In those cases, reassessment upon sale can be even more dramatic.
Check jurisdiction-specific rules.
```

### Tax Abatement Consideration

```
If the property has a tax abatement (e.g., 421-a in NYC):
  Year 7 of 25-year abatement: taxes = $50,000 (vs. $336,000 full assessment)

  Underwriting approach:
    Year 1-18 (remaining abatement): Use abated amount, stepping up per schedule
    Year 19+: Use full unabated assessment (reversion must reflect this)

  For T-12 normalization: Use the current abated tax bill if abatement transfers to buyer.
  Flag the abatement expiration year and the step-up schedule in the memo.
```

---

## 4. Insurance Repricing

### Rule

Restate insurance to current market rates. Seller may have a legacy policy at below-market rates, or may be overinsured or underinsured. Obtain actual quotes from the buyer's broker.

### Formula

```
Normalized insurance = Current market rate * Insurable value (replacement cost)

Market rates (per unit, multifamily, 2025-2026):
  Non-catastrophe zone:  $400-$700/unit
  Hurricane zone:        $800-$1,500/unit
  Earthquake zone:       $600-$1,200/unit
  Flood zone:            $300-$600/unit (supplemental)
```

### Worked Example

```
Seller's T-12 insurance: $48,000 ($400/unit)
Property is in a hurricane-prone coastal market.
Current quotes from buyer's broker: $1,100/unit = $132,000

Adjustment: +$84,000 expense ($132,000 - $48,000)

Common reasons seller's insurance is low:
  - Legacy policy with long-term carrier (no longer available to new buyers)
  - Umbrella policy across a portfolio (seller has 5,000 units, amortizes)
  - Higher deductible ($50K vs buyer's $25K)
  - Underinsured (not covering replacement cost)
```

---

## 5. Vacancy Gross-Up (Physical and Economic)

### Rule

If the property is above or below market occupancy, normalize to a stabilized vacancy rate. Also adjust for concessions and non-revenue units.

### Formulas

```
Physical vacancy = Vacant units / Total units
Economic vacancy = 1 - (Actual collected rent / Gross potential rent)

Gross potential rent = Total units * Market rent * 12

Normalized EGI = GPR * (1 - Stabilized_vacancy_rate) - Concessions - Credit_loss
```

### Worked Example

```
120 units. Current occupancy: 98.3% (118 units occupied).
Market stabilized vacancy: 5.0%.
Average in-place rent: $1,650/month.
Market rent: $1,700/month.

Step 1: Gross potential rent at market
  GPR = 120 * $1,700 * 12 = $2,448,000

Step 2: Physical vacancy normalization
  Stabilized vacancy (5%): $2,448,000 * 0.05 = $122,400

Step 3: Reported vs. normalized
  Reported vacancy loss: 2 units * $1,650 * 12 = $39,600
  Normalized vacancy loss: $122,400
  Adjustment: +$82,800 vacancy loss (reduces EGI)

Step 4: Loss-to-lease adjustment
  In-place average: $1,650. Market: $1,700. Gap: $50/unit/month.
  Loss to lease: 120 * $50 * 12 = $72,000

  Decision: If leases roll within the projection period, the loss-to-lease
  closes naturally. For T-12 normalization, keep in-place rents but flag
  the $72,000 upside as mark-to-market potential.

Step 5: Credit loss
  Reported bad debt: $14,400 (0.6% of GPR)
  Market credit loss: 1.0% of GPR = $24,480
  Adjustment: +$10,080

Normalized EGI: $2,448,000 - $122,400 - $24,480 = $2,301,120
Reported EGI:   $2,400,000 - $39,600 - $14,400 = $2,346,000
Net adjustment: -$44,880
```

---

## 6. Lease Adjustments (Commercial / Mixed-Use)

### Rule

For properties with commercial tenants (ground-floor retail, office components), normalize for:
- Lease expirations and renewal probability
- Below/above-market leases
- Free rent periods (amortize over lease term)
- Tenant improvement amortization
- Percentage rent (retail)

### Below-Market Lease Adjustment

```
Tenant A: 5,000 SF retail, paying $25/SF NNN. Market: $35/SF NNN.
Lease expires in 18 months.

Approach:
  Year 1 (T-12): Use in-place rent ($125,000/year)
  Year 2 (month 7+): Mark to market ($175,000/year, prorated)

  For T-12 normalization: Keep in-place unless the lease expires within
  the T-12 period. If it expires mid-T-12, use blended rate.

  Flag the $50,000/year upside for the investment memo.
```

### Above-Market Lease Adjustment

```
Tenant B: 3,000 SF retail, paying $45/SF NNN. Market: $35/SF NNN.
Lease expires in 8 months.

Risk: Tenant may not renew at $45/SF. Normalize to market upon expiration.
  Current annual rent: $135,000
  Market rent: $105,000
  At-risk premium: $30,000/year

  Probability-weighted adjustment:
    80% renewal at $38/SF: $114,000
    20% vacancy (6 months to re-lease): $105,000 * 0.5 = $52,500
    Expected: 0.80 * $114,000 + 0.20 * $52,500 = $101,700

  Adjustment: -$33,300 from reported ($135,000 - $101,700)
```

---

## 7. Utility Restatement (RUBS / Submeter)

### Rule

If the seller pays all utilities but the buyer plans to implement a ratio utility billing system (RUBS) or submetering, the T-12 should reflect the post-implementation economics.

### Worked Example

```
Seller's T-12 utilities: $216,000 ($1,800/unit/year, all owner-paid)

Buyer plans RUBS implementation:
  Water/sewer: $720/unit/year, recover 85% = $612 recovered
  Electric (common area only after submeter): $400/unit/year owner cost
  Gas: $360/unit/year, recover 75% = $270 recovered
  Trash: $180/unit/year, recover 90% = $162 recovered

Post-RUBS utility expense:
  Total utility cost: $216,000 (unchanged -- cost is the same)
  RUBS recovery: 120 * ($612 + $270 + $162) = $125,280 (new revenue)
  Remaining owner cost: $216,000 - $125,280 = $90,720

  Net utility expense: $90,720 (vs $216,000 reported)
  Adjustment: -$125,280 (adds to revenue or reduces expense)

Implementation note: RUBS can only be implemented on new leases or renewals.
  Full implementation takes 12-18 months for a typical 120-unit property.
  Underwrite a 6-month ramp to full recovery in year 1.
```

---

## 8. Payroll / On-Site Staff Normalization

### Rule

Seller's staffing levels may not match the buyer's operating plan. Normalize to the buyer's intended staffing model.

### Market Staffing Benchmarks

```
Multifamily staffing ratios (units per FTE):
  Property manager:    150-200 units per manager
  Leasing agent:       100-150 units per agent
  Maintenance tech:    75-100 units per tech
  Grounds/porter:      150-250 units per porter

120-unit property typical staff:
  1 property manager   ($55,000-$70,000 + benefits)
  1 leasing agent      ($40,000-$50,000 + benefits)
  1.5 maintenance      ($45,000-$55,000 each + benefits)
  Benefits load: 25-35% of salary
```

### Worked Example

```
Seller's T-12 payroll: $285,000 (overstaffed -- 2 maintenance, 2 leasing)

Buyer's plan: 1 PM, 1 leasing, 1.5 maintenance
  PM: $62,000 * 1.30 (benefits) = $80,600
  Leasing: $45,000 * 1.30 = $58,500
  Maintenance: $50,000 * 1.5 * 1.30 = $97,500
  Total: $236,600

Adjustment: -$48,400 expense (reduces payroll, increases NOI)
```

---

## 9. Capital Reserve / Replacement Reserve

### Rule

Ensure a capital reserve is included in normalized NOI even if the seller does not fund one. Lenders and appraisers require this.

### Benchmarks

```
Multifamily:         $250-$350/unit/year (newer vintage)
                     $400-$600/unit/year (1980s-2000s vintage)
                     $600-$1,000/unit/year (pre-1980, deferred maintenance)
Office:              $0.15-$0.30/SF/year
Retail:              $0.10-$0.20/SF/year
Industrial:          $0.05-$0.15/SF/year
```

### Worked Example

```
Seller's T-12: No capital reserve line item.
Property vintage: 1998. 120 units.

Normalized reserve: $500/unit/year = $60,000

Adjustment: +$60,000 expense (reduces NOI)

Note: This is distinct from actual capex budgeted by the buyer. The reserve in
the normalized T-12 is a lender/appraiser convention, not the buyer's actual
renovation budget.
```

---

## 10. Normalization Summary Checklist

### Step-by-Step Process

```
1. Obtain raw T-12 from seller (monthly detail preferred)
2. Tie out T-12 totals to bank statements or rent roll
3. Apply adjustments in this order:

   REVENUE ADJUSTMENTS
   [ ] Remove one-time income items (termination fees, insurance proceeds)
   [ ] Gross-up vacancy to market stabilized rate
   [ ] Adjust credit loss to market rate
   [ ] Add RUBS/submeter revenue if planned
   [ ] Flag loss-to-lease (mark-to-market upside)
   [ ] Adjust commercial lease income for expirations/renewals

   EXPENSE ADJUSTMENTS
   [ ] Remove one-time expense items (casualty repairs, litigation)
   [ ] Restate management fee to market rate
   [ ] Reassess real estate taxes to post-acquisition basis
   [ ] Reprice insurance to current quotes
   [ ] Normalize payroll to buyer's staffing plan
   [ ] Add capital reserve if missing
   [ ] Remove capital items misclassified as operating expense
   [ ] Restate utility expense for RUBS/submeter plan
   [ ] Normalize contract services (landscaping, pest, elevator)

4. Compute normalized NOI
5. Reconcile: document each adjustment with source and rationale
```

### Full Worked Normalization: 120-Unit Multifamily

```
Line Item              | Reported T-12 | Adjustment | Normalized  | Notes
-----------------------|---------------|------------|-------------|------
Gross Potential Rent   | $2,376,000    | +$72,000   | $2,448,000  | Mark to market rent
Vacancy Loss           | ($39,600)     | ($82,800)  | ($122,400)  | 5% stabilized
Other Income           | $185,000      | ($120,000) | $65,000     | Remove one-time items
Credit Loss            | ($14,400)     | ($10,080)  | ($24,480)   | 1% of GPR
RUBS Recovery          | $0            | +$125,280  | $125,280    | New implementation
-----------------------|---------------|------------|-------------|------
Effective Gross Income | $2,507,000    | ($15,600)  | $2,491,400  |
                       |               |            |             |
Real Estate Taxes      | ($184,000)    | ($152,000) | ($336,000)  | Reassessment
Insurance              | ($48,000)     | ($84,000)  | ($132,000)  | Current quotes
Management Fee         | $0            | ($79,800)  | ($79,800)   | 3.5% market rate
Payroll                | ($285,000)    | +$48,400   | ($236,600)  | Right-size staff
Repairs & Maintenance  | ($310,000)    | +$77,500   | ($232,500)  | Remove one-time
Utilities              | ($216,000)    | +$125,280  | ($90,720)   | Net of RUBS offset
Contract Services      | ($72,000)     | $0         | ($72,000)   | No change
Admin / Marketing      | ($45,000)     | $0         | ($45,000)   | No change
Capital Reserve        | $0            | ($60,000)  | ($60,000)   | $500/unit
-----------------------|---------------|------------|-------------|------
Total Operating Exp    | ($1,160,000)  | ($124,620) | ($1,284,620)|
-----------------------|---------------|------------|-------------|------
Net Operating Income   | $1,347,000    | ($140,220) | $1,206,780  |
                       |               |            |             |
Reported cap (at $16.8M): 8.02%
Normalized cap:           7.19%

The $140,220 NOI reduction translates to $2,335,000 in value at a 6.0% cap rate.
This is the risk of underwriting to a seller's un-normalized T-12.
```
