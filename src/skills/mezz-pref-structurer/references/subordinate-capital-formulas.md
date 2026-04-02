# Subordinate Capital Structuring Reference

Complete formulas, comparison matrices, and worked examples for mezzanine debt and preferred equity structuring. All examples use a baseline $30M acquisition with $20M senior debt and $5M subordinate capital tranche.

---

## 1. Mezz vs. Preferred Equity Comparison Matrix

| Dimension | Mezzanine Debt | Preferred Equity |
|---|---|---|
| Legal form | Loan (promissory note + pledge of equity) | Equity investment in the property-owning entity |
| Collateral | Pledge of borrower's membership interest in property LLC | No lien; contractual rights within JV/LLC operating agreement |
| Payment priority | Second lien; paid after senior debt, before equity | Preferred return paid before common equity distributions |
| Foreclosure rights | UCC foreclosure on pledged equity interests (30-60 days in most states) | No foreclosure; remedies are contractual (springing control, buyout rights) |
| Intercreditor agreement | Required with senior lender; governs cure rights, standstill, notice | Not typically party to intercreditor; senior lender may require recognition agreement |
| Tax treatment | Interest payments are tax-deductible to borrower | Preferred returns are NOT tax-deductible; treated as profit allocation |
| Balance sheet | Debt (increases leverage ratios) | Equity (does not increase debt metrics, but dilutes ownership) |
| Typical rate | 10-15% (current pay + accrual) | 12-18% (preferred return, often with participation) |
| Default remedy timeline | UCC foreclosure: 30-60 days | Negotiated remedy: springing control, forced sale, or dilution ratchet |
| Senior lender preference | Often restricted or prohibited in loan docs | Generally permitted; senior lender sees it as equity |
| Bankruptcy treatment | Mezzanine lender is a creditor with claims | Preferred equity holder is an equity interest, subordinate to all creditors |

### When to Use Each

- **Mezz**: Borrower wants tax-deductible interest; sponsor has strong intercreditor negotiation position; senior lender permits subordinate debt.
- **Pref equity**: Senior loan docs prohibit subordinate debt; sponsor willing to trade tax deductibility for faster/cleaner execution; sponsor wants to avoid covenant compliance on a second loan.

---

## 2. Capital Stack WACC with Subordinate Layers

### Notation

| Symbol | Definition |
|---|---|
| w_s | Senior debt weight (loan / total capitalization) |
| w_m | Mezz or pref weight (subordinate / total capitalization) |
| w_e | Common equity weight (equity / total capitalization) |
| k_s | Senior debt cost (interest rate) |
| k_m | Mezz/pref cost (coupon or preferred return) |
| k_e | Common equity required return (sponsor IRR target) |
| t | Marginal tax rate (applies to deductible interest only) |

### Formula

```
WACC = w_s * k_s * (1 - t) + w_m * k_m * (1 - t * D_flag) + w_e * k_e

where D_flag = 1 if subordinate layer is debt (mezz), 0 if equity (pref)
```

### Worked Example: $30M Deal

Capital stack:
```
Senior debt:    $20,000,000  (66.7%)  at 6.50%
Subordinate:     $5,000,000  (16.7%)  at 12.00%
Common equity:   $5,000,000  (16.7%)  target 18.00%
Total:          $30,000,000
```

Assume 37% marginal tax rate.

**Scenario A: Subordinate is mezzanine debt (interest deductible)**

```
WACC = 0.667 * 0.065 * (1 - 0.37) + 0.167 * 0.12 * (1 - 0.37) + 0.167 * 0.18
     = 0.667 * 0.04095 + 0.167 * 0.0756 + 0.167 * 0.18
     = 0.02731 + 0.01262 + 0.03006
     = 0.06999 = 7.00%
```

**Scenario B: Subordinate is preferred equity (not deductible)**

```
WACC = 0.667 * 0.065 * (1 - 0.37) + 0.167 * 0.12 * 1.0 + 0.167 * 0.18
     = 0.02731 + 0.02004 + 0.03006
     = 0.07741 = 7.74%
```

**Tax shield value of mezz vs. pref**: 7.74% - 7.00% = 74bps WACC difference. On a $30M deal, this represents approximately $222,000/year in tax savings from choosing mezz over pref, assuming the full coupon is deductible.

---

## 3. Intercreditor Analysis: Key Provisions

### Standstill Period

The period during which the mezz lender cannot exercise remedies (UCC foreclosure) after a default. Typical: 60-120 days.

```
Standstill impact on mezz recovery:
  During standstill, mezz accrues default interest (typically +3-5% above contract rate).
  If resolved during standstill: mezz recovers par + accrued + default premium.
  If not resolved: mezz forecloses on equity, takes control of property LLC.
```

### Cure Rights

Mezz lender typically has the right to cure senior loan defaults to prevent senior foreclosure.

```
Cure cost to mezz lender:
  Monetary default cure = past-due payments + late fees + legal costs
  Example: 3 months of delinquent senior P&I = 3 * $131,659 = $394,977
           Late fees (5% of payment) = $19,749
           Legal costs (estimate) = $50,000
           Total cure cost = $464,726

  This is added to the mezz lender's basis and increases their total exposure.
```

### Buyout Right

Mezz lender may have the right to purchase the senior loan at par. This is negotiated in the intercreditor and represents the "nuclear option."

```
Senior loan buyout cost = outstanding principal + accrued interest + fees + prepayment penalty (if any)
Example: $19,500,000 principal + $105,625 accrued + $25,000 fees = $19,630,625
```

---

## 4. Loss Severity Waterfall

### Setup

$30M property value at origination. Capital stack: $20M senior, $5M mezz, $5M equity. Property value declines to distressed sale price.

### Formula

```
Loss severity for tranche i = max(0, (sum of all senior claims - recovery proceeds)) / tranche_i_face_value

Recovery waterfall:
  1. Selling costs (broker, legal, transfer tax) -- typically 3-5% of sale price
  2. Senior debt: principal + accrued interest + fees
  3. Mezzanine debt: principal + accrued interest + fees
  4. Preferred equity: invested capital + accrued preferred return
  5. Common equity: residual
```

### Worked Example: Distressed Disposition at Various Price Points

Original: $30M purchase. Senior: $20M at 6.5%. Mezz: $5M at 12%. Equity: $5M. Assume 2 years of accrual at default.

```
Senior claim at default:
  Principal: $20,000,000 (IO assumed)
  Accrued interest: $20M * 6.5% * (3/12) = $325,000  (3 months delinquent)
  Late fees + legal: $100,000
  Total senior claim: $20,425,000

Mezz claim at default:
  Principal: $5,000,000
  Accrued (current pay, so caught up through 3 months ago): $0
  Default interest: $5M * (12% + 4% default) * (3/12) = $200,000
  Total mezz claim: $5,200,000
```

| Sale Price | Selling Costs (4%) | Net Proceeds | Senior Recovery | Mezz Recovery | Equity Recovery | Mezz Loss Severity |
|---|---|---|---|---|---|---|
| $30,000,000 | $1,200,000 | $28,800,000 | $20,425,000 (100%) | $5,200,000 (100%) | $3,175,000 | 0% |
| $27,000,000 | $1,080,000 | $25,920,000 | $20,425,000 (100%) | $5,200,000 (100%) | $295,000 | 0% |
| $25,000,000 | $1,000,000 | $24,000,000 | $20,425,000 (100%) | $3,575,000 (69%) | $0 | 31% |
| $22,000,000 | $880,000 | $21,120,000 | $20,425,000 (100%) | $695,000 (13%) | $0 | 87% |
| $20,000,000 | $800,000 | $19,200,000 | $19,200,000 (94%) | $0 (0%) | $0 | 100% |
| $18,000,000 | $720,000 | $17,280,000 | $17,280,000 (85%) | $0 (0%) | $0 | 100% |

### Loss Severity Interpretation

Mezz hits 100% loss at any sale price where net proceeds fail to cover the full senior claim. The breakeven sale price for mezz is:

```
Breakeven_mezz = (senior_claim + mezz_claim) / (1 - selling_cost_rate)
               = ($20,425,000 + $5,200,000) / 0.96
               = $26,692,708

Value decline from origination to breakeven: ($30M - $26.69M) / $30M = 11.0%
```

This means the mezz lender is fully wiped out if the property declines more than ~14.6% from origination (point where net proceeds equal senior claim only):

```
Wipeout_mezz = senior_claim / (1 - selling_cost_rate) = $20,425,000 / 0.96 = $21,276,042
Value decline to total mezz wipeout: ($30M - $21.28M) / $30M = 29.1%
```

The mezz tranche absorbs losses between an 11% and 29% decline in property value -- a relatively narrow band.

---

## 5. Attachment and Detachment Points

### Formula

```
Attachment point = sum of all tranches senior to this tranche / total capitalization
Detachment point = (sum of all tranches senior to and including this tranche) / total capitalization

Loss to tranche = max(0, min(1, (total_loss - attachment_point) / (detachment_point - attachment_point)))
```

### Worked Example

```
Senior:  attachment = 0%, detachment = 66.7%  ($20M / $30M)
Mezz:    attachment = 66.7%, detachment = 83.3%  ($25M / $30M)
Equity:  attachment = 83.3%, detachment = 100%

If property value declines 20% ($6M loss):
  Total loss ratio = $6M / $30M = 20%

  Senior loss = max(0, min(1, (0.20 - 0) / (0.667 - 0))) = 0.30 -> 0% (fully protected by subordination)
  Wait -- this formula applies to portfolio CDO tranching. For single-asset waterfall, use the direct recovery waterfall above.
```

For single-asset CRE, the direct waterfall in Section 4 is the correct approach. Attachment/detachment points are more relevant for CMBS pool analysis.

---

## 6. Common Errors

| Error | Why It Matters |
|---|---|
| Treating pref equity returns as tax-deductible | Overstates after-tax returns by 200-400bps on the subordinate tranche cost |
| Ignoring intercreditor standstill in mezz recovery timing | UCC foreclosure is fast (30-60 days), but standstill can add 60-120 days of accruing default interest |
| Assuming mezz can foreclose on the property directly | Mezz forecloses on EQUITY INTERESTS, not the property. Senior loan stays in place. |
| Using WACC as hurdle rate for mezz deals | WACC is a blended cost; each tranche must clear its own return hurdle independently |
| Ignoring selling costs in loss severity | 3-5% selling costs reduce net recovery, pushing mezz losses higher than a naive calculation suggests |
| Modeling pref equity with a fixed coupon like debt | Pref equity is a profit allocation; it may be deferred or reduced if there is insufficient distributable cash, unlike debt where non-payment triggers default |

---

## 7. Quick Formulas

```
LTC (with subordinate capital) = (senior + mezz) / total_cost
LTCV (last-dollar leverage) = (senior + mezz) / as-complete_value
Equity cushion above mezz = (total_value - senior - mezz) / total_value
Mezz debt yield = NOI / mezz_loan_amount
Combined DSCR = NOI / (senior_debt_service + mezz_debt_service)
Senior-only DSCR = NOI / senior_debt_service
```

### Worked Example

```
NOI: $1,800,000
Senior DS (6.5%, 30yr amort, $20M): $1,517,280/year
Mezz DS (12% IO, $5M): $600,000/year

Senior DSCR = 1,800,000 / 1,517,280 = 1.19x
Combined DSCR = 1,800,000 / (1,517,280 + 600,000) = 0.85x  (negative carry after combined DS)
Mezz debt yield = 1,800,000 / 5,000,000 = 36.0%
Equity cushion = ($30M - $20M - $5M) / $30M = 16.7%
```

The combined DSCR of 0.85x indicates the property cannot service both tranches from current NOI alone -- the sponsor must fund the gap from equity reserves or the deal must have a credible path to higher NOI (value-add or lease-up). This is typical for transitional mezz deals.
