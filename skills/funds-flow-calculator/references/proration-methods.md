# Proration Methods Reference

Reference for the funds-flow-calculator skill. Covers the three standard proration conventions used in commercial real estate closings: per diem actual/365, actual/360 (bank method), and 30/360. Includes worked examples for property taxes, rent, CAM, and insurance for each method.

---

## Overview: When to Use Each Method

| Method | Description | Most Common Use |
|---|---|---|
| Actual/365 (per diem) | Divide annual amount by actual days in year; multiply by actual days in period | Property taxes in most states; default for CRE closings |
| Actual/360 (bank method) | Divide annual amount by 360; multiply by actual calendar days | Mortgage interest, some loan payoffs |
| 30/360 | Assume 12 months of 30 days; use 30-day months for day count | Bond interest, some rent prorations by PSA election; simplifies month-end closings |

**PSA controls**: if the PSA specifies a method, use it. If silent, default to actual/365 for property taxes and rent. Check with title company -- some jurisdictions use local convention regardless of PSA.

---

## Method 1: Actual/365 (Per Diem)

### Mechanics

```
Daily rate = Annual amount / 365
           (or / 366 in a leap year for the leap-year period)

Seller's share = Daily rate * days seller is responsible
Buyer's share  = Daily rate * days buyer is responsible

Convention for closing day:
  Seller owns through the day BEFORE closing (or through closing day per PSA).
  Buyer owns FROM closing day.
  Standard: seller through Day -1; buyer from Day 0.
  Verify: some PSAs say "seller is responsible through and including closing date."
```

### Worked Example 1A: Property Tax (Paid in Arrears)

```
Facts:
  Closing date: March 15, 2026
  Annual property tax bill: $180,000 (calendar year Jan 1 - Dec 31, 2026)
  Payment status: Not yet billed or paid (taxes paid in arrears after year-end)
  Method: Actual/365

Calculation:
  Daily rate: $180,000 / 365 = $493.15 per day

  Seller's period: January 1, 2026 through March 14, 2026
  Day count: Jan has 31 days (31), Feb has 28 days (non-leap year: 28), Mar 1-14 = 14 days
  Total seller days: 31 + 28 + 14 = 73 days

  Seller's share: 73 * $493.15 = $36,000 (rounded to nearest dollar)

  Result: Seller CREDITS buyer $36,000 at closing.
  Buyer will receive the full 2026 tax bill when it arrives (typically early 2027)
  and will be responsible for the full payment, having received credit for seller's portion.

True-up clause:
  If the actual 2026 bill differs from the $180,000 estimate used, parties re-prorate.
  Typical PSA: "If actual tax differs by more than 5% from estimate, parties re-prorate within
  30 days of actual bill receipt."
```

### Worked Example 1B: Property Tax (Paid in Advance)

```
Facts:
  Closing date: July 1, 2026
  Annual property tax: $240,000 (fiscal year July 1, 2026 - June 30, 2027)
  Payment status: Seller paid full fiscal-year bill on July 1, 2026 (same day as closing)

Calculation:
  Buyer's period: July 1, 2026 through June 30, 2027 = full fiscal year = 365 days
  Seller's period: July 1 only (closing day) = 1 day (if convention is seller owns through closing)

  Seller paid $240,000 for period buyer will own.
  Buyer owes seller: $240,000 * 364/365 = $239,342

  Result: Buyer CREDITS seller $239,342 at closing.

  Note: In most forward-paid jurisdictions (CA, FL), if seller paid full year, buyer gets a
  large credit to seller. Confirm actual payment status before calculating.
```

### Worked Example 1C: Rent Proration

```
Facts:
  Closing date: March 15, 2026
  Tenant: ABC Corp, monthly rent $10,000
  Rent collected: March 1 (full month paid by tenant)
  Convention: seller owns through March 14; buyer owns March 15-31

Calculation:
  Days in March: 31
  Seller's days: March 1-14 = 14 days
  Buyer's days: March 15-31 = 17 days

  Seller's share: $10,000 * 14/31 = $4,516 (rounded)
  Buyer's share: $10,000 * 17/31 = $5,484 (rounded)

  Since seller collected full month: Seller CREDITS buyer $5,484 at closing.

Delinquent rent alternative:
  If March rent NOT collected at closing:
  - Do not prorate -- no money to split.
  - Assign collection rights to buyer for March (partial-month owed to buyer).
  - Or: seller retains right to pursue March rent from tenant (requires coordination with buyer/PM).
  - Document in closing memo which approach applies.
```

---

## Method 2: Actual/360 (Bank Method)

### Mechanics

```
Daily rate = Annual amount / 360
Days = Actual calendar days elapsed

This method produces a higher daily rate than actual/365 (same annual amount divided by
fewer days = higher daily rate). Result: calculations slightly favor the creditor.

Common in:
  - Mortgage and loan interest calculations
  - Payoff letter per diem calculations (confirm with lender -- some use actual/365)
  - Construction loan interest
```

### Worked Example 2A: Mortgage Per Diem Interest

```
Facts:
  Loan balance: $11,250,000
  Note rate: 5.50% per annum
  Payoff letter good-through date: March 10, 2026
  Actual closing date: March 15, 2026 (5 days after good-through)

Per diem calculation (actual/360 bank method):
  Annual interest: $11,250,000 * 5.50% = $618,750
  Daily rate (360-day year): $618,750 / 360 = $1,718.75 per day

  Additional days: 5
  Additional interest: 5 * $1,718.75 = $8,594 (rounded)

  Adjusted payoff: payoff letter amount + $8,594

Comparison (if lender used actual/365):
  Daily rate (365-day year): $618,750 / 365 = $1,694.52 per day
  Additional interest: 5 * $1,694.52 = $8,473

  Difference: $8,594 vs. $8,473 = $121 over 5 days.
  On large loan amounts, the method matters. Confirm with payoff letter which method lender uses.
```

### Worked Example 2B: Prepaid Interest at Closing

```
Facts:
  New loan: $11,250,000 at 5.50%
  Closing date: March 15, 2026
  First payment date: May 1, 2026 (first P&I payment at beginning of second full month)
  Lender requires prepaid interest from closing through March 31 (16 days)

Per diem calculation (actual/360):
  Daily rate: $11,250,000 * 5.50% / 360 = $1,718.75 per day
  Days of prepaid interest: March 15 through March 31 = 17 days (count closing day)
  Prepaid interest: 17 * $1,718.75 = $29,219

  This appears as a buyer debit in the settlement statement and is funded at closing.
  Reduces buyer's equity contribution by corresponding amount in sources/uses.
```

---

## Method 3: 30/360

### Mechanics

```
Assumes each month has exactly 30 days and each year has exactly 360 days.

Day count between two dates (D1 to D2):
  Let D1 = start date (Y1/M1/d1) and D2 = end date (Y2/M2/d2)

  Adjust d1 and d2:
    If d1 = 31, set d1 = 30
    If d2 = 31 AND d1 is 30 or 31, set d2 = 30

  Days = (Y2-Y1)*360 + (M2-M1)*30 + (d2-d1)

Daily rate = Annual amount / 360

This eliminates the variable of different month lengths and simplifies calculations
especially for closings at month-end.
```

### Worked Example 3A: Rent Proration (30/360 Method)

```
Facts:
  Closing date: March 15, 2026
  Monthly rent: $10,000 (collected March 1)
  Method: 30/360 per PSA election

Calculation:
  Under 30/360, March has 30 days.
  Seller's days: March 1-14 = 14 days
  Buyer's days: March 15-30 = 16 days (30 - 14 = 16; March has 30 days under 30/360)
  Total: 30 days

  Seller's share: $10,000 * 14/30 = $4,667 (rounded)
  Buyer's share: $10,000 * 16/30 = $5,333 (rounded)

Comparison to Actual/365:
  Actual/365: Seller's share = $4,516 (14 days of 31 actual March days)
  30/360: Seller's share = $4,667 (14 days of 30 assumed days)
  Difference: $151 per tenant per month; multiplied across 45 units = $6,795 total difference

  The 30/360 method slightly favors buyer in this example (seller pays more).
  Depends on closing day within the month -- varies by deal.
```

### Worked Example 3B: Property Tax (30/360 for Mid-Year Closing)

```
Facts:
  Closing date: June 15, 2026
  Annual property tax: $180,000 (calendar year)
  Method: 30/360

Calculation:
  Seller's period: January 1 through June 14
  Under 30/360:
    Months: January (30) + February (30) + March (30) + April (30) + May (30) = 5 full months = 150 days
    Plus June 1-14: 14 days
    Total seller days: 150 + 14 = 164 days

  Daily rate: $180,000 / 360 = $500.00 per day
  Seller's share: 164 * $500 = $82,000

Comparison to Actual/365:
  Actual seller days: Jan (31) + Feb (28) + Mar (31) + Apr (30) + May (31) + Jun 1-14 (14) = 165 days
  Daily rate actual: $180,000 / 365 = $493.15
  Seller's share actual: 165 * $493.15 = $81,370

  Difference: $82,000 - $81,370 = $630 (30/360 slightly higher seller cost in this case)
```

---

## Method Comparison Summary Table

For a $15M multifamily with $180,000 annual taxes, $125,000/month rent, 45 units, closing March 15:

| Line Item | Actual/365 | Actual/360 | 30/360 | Notes |
|---|---|---|---|---|
| Property tax proration (seller debit) | $36,000 | $36,667 | $36,500 | 360/360 yields higher daily rate |
| Rent proration (seller debit, 1 unit, $10K rent) | $5,484 | N/A | $5,333 | 30/360 slightly lower buyer credit |
| Total rent proration (45 units, pro-rata) | $68,548 | N/A | $66,667 | ~$1,900 swing across portfolio |
| Mortgage per diem (5 days, $11.25M at 5.5%) | $8,473 | $8,594 | N/A | Bank method yields higher per diem |

---

## CAM / Operating Expense Proration

For commercial properties with triple-net leases, CAM collections from tenants must be prorated between buyer and seller for the current calendar year.

```
Year-end CAM reconciliation for current year:
  Estimated CAM charged to tenants for current year: [annual estimate]
  Actual CAM expenses incurred (seller's period): [actual expenses Jan 1 through closing]
  Buyer will administer year-end reconciliation for full calendar year

Approach 1: Escrow until year-end reconciliation
  Seller deposits estimated liability into escrow at closing.
  After year-end reconciliation: escrow released to appropriate party.
  Safest for both parties.

Approach 2: Credit at closing based on estimate
  Calculate seller's share of estimated annual CAM based on proportion of year owned.
  True-up after year-end based on actuals.
  Common for institutional transactions.

Approach 3: Buyer takes as-is
  Buyer assumes full year-end CAM obligation with no credit from seller.
  Only appropriate if CAM collections and expenses are estimated to be in balance.

Example:
  CAM year: January 1 - December 31, 2026
  Total estimated CAM expenses for 2026: $360,000
  Closing date: March 15, 2026 (seller owns 73/365 of the year)
  Estimated CAM collected from tenants Jan 1 - Mar 14: $65,000
  Estimated actual expenses Jan 1 - Mar 14: $72,000
  Seller's estimated shortfall: $7,000

  If Approach 2: Seller credits buyer $7,000 at closing; buyer reconciles full year with tenants.
```

---

## Insurance Proration

```
Scenario: Buyer assumes existing insurance policy (rare in commercial transactions)

Annual premium: $60,000
Policy year: January 1 - December 31, 2026
Closing date: March 15, 2026

Days remaining in policy year after closing (buyer's period):
  March 15 - December 31 = 291 days

Buyer credits seller:
  Method actual/365: $60,000 * 291/365 = $47,836

  Method 30/360:
  March 15 - December 31 under 30/360:
  Months: April-December = 9 full months = 270 days
  Plus March 15-30 = 16 days
  Total: 286 days
  Buyer credit: $60,000 * 286/360 = $47,667

Standard practice:
  Buyer obtains a new policy effective at closing. No insurance proration needed.
  Seller cancels existing policy and receives prorated return premium from insurer.
  Prorated return premium goes to seller, not to closing statement.
```
