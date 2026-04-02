# T-12 Normalization Guide

Step-by-step methodology for normalizing trailing twelve-month (T-12) operating statements to produce a reliable underwriting base. All examples use a 50-unit multifamily property with reported T-12 revenue of $1,680,000 and expenses of $756,000.

---

## 1. Why Normalize

A T-12 statement reflects what happened, not what will happen under new ownership. One-time items, below-market management, deferred insurance, and stale tax assessments distort the reported NOI. The goal is an adjusted NOI that represents the property's sustainable cash generation on a forward basis.

The normalized T-12 becomes the starting point for the Year 1 proforma. Errors here propagate through every year of the hold and compound into the reversion.

---

## 2. Normalization Sequence

Process in this order. Each step feeds the next.

```
Step 1: Gross Potential Rent (GPR) validation
Step 2: Vacancy and concession restatement
Step 3: Other income normalization
Step 4: One-time income/expense removal
Step 5: Management fee restatement
Step 6: Real estate tax reassessment
Step 7: Insurance repricing
Step 8: R&M and contract normalization
Step 9: Utility restatement (if submetered)
Step 10: Final adjusted NOI
```

---

## 3. Step-by-Step Methodology

### Step 1: GPR Validation

Compare rent roll contract rents to the T-12 reported rental income. Discrepancies indicate mid-year rent bumps, move-in/out timing, or data errors.

```
Rent roll shows 50 units at weighted avg $2,850/month
Implied annual GPR = 50 * $2,850 * 12 = $1,710,000

T-12 reported rental income: $1,596,000
Difference: $114,000

Sources of difference:
  Vacancy loss (3 units avg):   $102,600  (3 * $2,850 * 12)
  Concessions given:             $18,000  (6 units * $3,000 each)
  Late fees credited back:       -$6,600
  Total explained:              $114,000  (reconciles)
```

If the gap does not reconcile, flag the data quality and request unit-level monthly collections.

### Step 2: Vacancy and Concession Restatement

Replace reported vacancy with market vacancy for the submarket and vintage.

```
Reported physical vacancy:  6.0%  (3 units)
Market vacancy (submarket): 4.5%
Underwritten vacancy:       5.0%  (conservative, between reported and market)

GPR:                        $1,710,000
Less vacancy at 5.0%:         -$85,500
Less concessions at 1.5%:     -$25,650  (market norm for lease-up incentives)
Effective Gross Income:     $1,598,850
```

### Step 3: Other Income Normalization

Review each line for sustainability. Common items and treatment:

| Line Item | T-12 Amount | Adjustment | Normalized |
|---|---|---|---|
| Laundry income | $36,000 | Sustainable, keep | $36,000 |
| Parking (25 spaces @ $100) | $30,000 | Keep, confirm lease | $30,000 |
| Pet fees (20 pets @ $50/mo) | $12,000 | Keep | $12,000 |
| Late fees | $8,400 | Reduce to 60% | $5,040 |
| Insurance claim proceeds | $22,000 | Remove (one-time) | $0 |
| Application fees | $3,600 | Reduce to 75% | $2,700 |

```
T-12 other income:         $112,000
Normalized other income:    $85,740
Adjustment:                -$26,260
```

### Step 4: One-Time Item Removal

Scan every expense line for non-recurring charges.

```
T-12 reported expenses include:
  Legal (eviction, one tenant):  $18,500  -> normalize to $5,000/year
  Roof emergency repair:         $34,000  -> remove (capex, not operating)
  Fire code remediation:         $12,000  -> remove (one-time)
  Broker leasing commissions:    $24,000  -> normalize to $8,000/year

Total one-time removals:  $75,500
Normalized additions:     $13,000
Net adjustment:          -$62,500 reduction in expenses
```

### Step 5: Management Fee Restatement

Seller may self-manage or use a below-market fee. Restate to market.

```
T-12 reported management fee:  $33,600  (2.0% of EGI, self-managed)
Market management fee:          4.5% of EGI for 50-unit property

Normalized management fee = $1,598,850 * 0.045 = $71,948
Adjustment: +$38,348 increase in expenses
```

Market management fee ranges:

| Unit Count | Market Fee Range |
|---|---|
| < 30 units | 5.0-7.0% |
| 30-75 units | 4.0-5.5% |
| 75-150 units | 3.5-4.5% |
| 150-300 units | 3.0-4.0% |
| 300+ units | 2.5-3.5% |

### Step 6: Real Estate Tax Reassessment

Most jurisdictions reassess property value on sale. The current tax bill reflects the seller's basis, not the buyer's.

```
Current assessed value:     $8,200,000
Current tax rate (mill rate): 2.15%
Current annual tax:         $176,300

Purchase price:             $12,000,000
Expected reassessment ratio: 85% of sale price (jurisdiction-specific)
New assessed value:         $10,200,000
Projected annual tax:       $10,200,000 * 0.0215 = $219,300

Tax adjustment: +$43,000 increase in expenses
```

States with reassessment on sale: most states except California (Prop 13 limits increases to 2%/year until sale). Always verify the specific jurisdiction.

For jurisdictions with assessment caps or phase-in periods, model the year-by-year trajectory:

```
Year 1 (phase-in 50%):  ($176,300 + $219,300) / 2 = $197,800
Year 2 (full):           $219,300
Year 3+:                 $219,300 * (1 + annual_increase)
```

### Step 7: Insurance Repricing

Insurance markets harden and soften. Request current quotes rather than relying on the seller's renewal.

```
T-12 insurance premium:     $42,000  ($840/unit)
Current market quote:       $62,500  ($1,250/unit)
Adjustment: +$20,500 increase in expenses
```

Typical per-unit insurance costs (2025):

| Market | Per Unit |
|---|---|
| Non-coastal | $800-$1,200 |
| Coastal (non-FL/TX) | $1,200-$1,800 |
| Florida | $1,800-$3,500 |
| Texas (wind zones) | $1,500-$2,500 |

### Step 8: R&M and Contract Normalization

Check if R&M is abnormally low (deferred maintenance) or high (catch-up repairs).

```
T-12 R&M per unit:  $2,400  ($120,000 total)
Market benchmark:    $1,800-$2,200/unit for 1990s vintage garden
Normalized R&M:     $2,000/unit = $100,000
Adjustment: -$20,000 reduction in expenses
```

Also normalize contracts (landscaping, pest, elevator, trash) to current market bids.

### Step 9: Utility Restatement

If submetering is partial or the property pays utilities, normalize to current rate schedules.

```
T-12 water/sewer:   $54,000  (owner-paid)
Rate increase (8%): $54,000 * 1.08 = $58,320
Adjustment: +$4,320 increase in expenses
```

---

## 4. Full Worked Example: Normalized T-12

Starting with the messy T-12 and applying all adjustments:

```
                              T-12 Reported    Adjustments    Normalized
REVENUE
  Gross Potential Rent         $1,710,000              --    $1,710,000
  Less: Vacancy                  -$114,000       +$28,500      -$85,500
  Less: Concessions               -$18,000        -$7,650      -$25,650
  Other Income                    $112,000       -$26,260       $85,740
EFFECTIVE GROSS INCOME (EGI)   $1,690,000       -$5,410     $1,684,590

EXPENSES
  Management Fee                   $33,600       +$38,348       $71,948
  Real Estate Taxes               $176,300       +$43,000      $219,300
  Insurance                        $42,000       +$20,500       $62,500
  R&M                             $120,000       -$20,000      $100,000
  Utilities (owner-paid)           $54,000        +$4,320       $58,320
  Payroll                          $96,000              --       $96,000
  General & Admin                  $28,000              --       $28,000
  Legal (normalized)               $18,500       -$13,500        $5,000
  Landscaping/Contracts            $24,000              --       $24,000
  Leasing commissions              $24,000       -$16,000        $8,000
  Roof repair (one-time)           $34,000       -$34,000            $0
  Fire remediation (one-time)      $12,000       -$12,000            $0
TOTAL EXPENSES                    $662,400       +$10,668      $673,068

NET OPERATING INCOME              $924,000       -$16,078    $1,011,522*
```

*Note: The T-12 NOI was $1,027,600 ($1,690,000 - $662,400). After normalization, NOI decreases slightly because the management fee restatement and tax reassessment outweigh the removal of one-time expenses. This is a common outcome. The raw T-12 NOI was flattering because of self-management and stale taxes.

Corrected calculation:

```
Normalized EGI:       $1,684,590
Normalized Expenses:    $673,068
Normalized NOI:       $1,011,522
```

---

## 5. Common Errors

1. **Using seller's management fee**: Self-managed properties show artificially low expenses. Always restate to market third-party fee. Failing to do this overstates NOI by 2-3% of EGI.

2. **Ignoring tax reassessment**: In a rising market, the gap between current assessed value and purchase price can be enormous. A $4M assessed-to-purchase gap at a 2% mill rate is $80,000/year in additional taxes. This is the single largest normalization item on most deals.

3. **Keeping one-time revenue**: Insurance proceeds, legal settlements, and retroactive utility credits are non-recurring. Including them inflates EGI.

4. **Normalizing to zero vacancy**: Even stabilized assets have frictional vacancy. Use 3-5% minimum for stabilized multifamily, even if the rent roll shows 100% occupied today.

5. **Failing to annualize partial-year items**: If insurance renewed mid-year at a higher rate, the T-12 blends the old and new premium. Annualize the current rate.

6. **Confusing capex with operating expense**: Roof replacements, HVAC unit replacements, and parking lot resurfacing are capital expenditures, not operating expenses. Remove them from the T-12 and budget them separately in the proforma capex schedule.

7. **Accepting seller's trailing rent roll as current**: Verify against the most recent month's collections, not the rent roll effective date. Tenants in arrears, month-to-month holdovers, and pending evictions distort the snapshot.

---

## 6. Benchmarks for Reasonableness Check

After normalization, verify the expense ratio and per-unit metrics against market comps.

| Metric | Garden MF (50 units) | Mid-Rise MF | High-Rise MF |
|---|---|---|---|
| Expense ratio (OpEx/EGI) | 38-45% | 42-50% | 48-58% |
| OpEx per unit | $5,500-$7,500 | $7,000-$10,000 | $10,000-$15,000 |
| Mgmt fee (% EGI) | 4.0-5.5% | 3.5-4.5% | 3.0-4.0% |
| Insurance per unit | $800-$1,500 | $1,000-$2,000 | $1,200-$2,500 |
| R&M per unit | $1,500-$2,500 | $2,000-$3,500 | $2,500-$4,500 |
| RE tax per unit | $2,000-$5,000 | $3,000-$8,000 | $5,000-$12,000 |

If your normalized T-12 falls outside these ranges, investigate. A 50-unit garden property with an expense ratio below 35% likely has underestimated taxes, insurance, or management. Above 50% suggests inefficiencies or high-cost market (NYC, SF).

---

## 7. Normalization Checklist

Before finalizing the normalized T-12, confirm:

- [ ] GPR reconciles to rent roll within 2%
- [ ] Vacancy uses market rate, not trailing
- [ ] All one-time items removed with documentation
- [ ] Management fee restated to market third-party rate
- [ ] Taxes projected for post-sale reassessment
- [ ] Insurance repriced with current market quote
- [ ] R&M within market per-unit range
- [ ] Utilities adjusted for known rate changes
- [ ] Other income items individually validated
- [ ] Final expense ratio within expected range for property type
