# Tax Characterization Guide

Reference for the distribution-notice-generator skill. Covers the methodology for determining whether a CRE fund distribution is return of capital, ordinary income, or capital gain, and how to prepare a K-1 preview for each LP. This is a practitioner guide, not legal or tax advice. Always confirm with fund tax counsel before issuing LP notices with tax characterization language.

---

## Overview: The Three Characterization Questions

For every LP distribution, answer three questions in order:

1. **How much (if any) of this distribution is a return of the LP's own capital?**
   - Non-taxable to the extent it does not exceed the LP's adjusted outside basis
   - Reduces LP's outside basis dollar-for-dollar

2. **How much (if any) is ordinary income?**
   - Ordinary income: operating income not sheltered by depreciation, Section 1250 recapture on sale, interest income passed through
   - Taxed at ordinary income rates (up to 37% federal for individuals)

3. **How much (if any) is capital gain?**
   - Long-term capital gain: appreciation on assets held > 12 months (Section 1231 gain)
   - Section 1250 unrecaptured gain: portion of LTCG attributable to prior depreciation deductions (capped at 25% federal rate)
   - Short-term gain: assets held < 12 months (ordinary income rates)

---

## Part I: Return of Capital Determination

### What Is Outside Basis?

A limited partner's outside basis in a partnership interest is their after-tax cost basis. It starts at capital contributed and is adjusted each year:

```
Outside basis increases from:
  + Capital contributions
  + Allocable share of partnership income (ordinary and capital)
  + Allocable share of partnership liabilities (if LP guarantees or bears economic risk)

Outside basis decreases from:
  - Cash distributions received
  - Allocable share of partnership losses (limited to basis; excess is suspended)
  - Allocable share of partnership deductions (depreciation, Section 179, etc.)
  - Allocable share of liabilities released
```

**The basis floor rule**: outside basis cannot go below zero. Once it reaches zero, the LP cannot deduct further losses (they are suspended) and any cash distribution triggers taxable gain.

### Depreciation and Basis Erosion

Real estate partnerships are heavy depreciators. In a leveraged fund with cost segregation, it is common for depreciation allocations to erode LP outside basis faster than cash distributions.

```
Year 1 example (illustrative):
  LP contributes $500,000 capital
  LP's share of liabilities (nonrecourse): $300,000 (increases basis)
  Opening outside basis: $500,000 + $300,000 = $800,000

  Year 1 activity:
    + Allocable ordinary income:    $20,000
    - Depreciation allocated:      ($120,000)  <- cost segregation aggressive
    - Cash distribution:            ($40,000)
  Net basis change: $20,000 - $120,000 - $40,000 = ($140,000)
  Closing outside basis: $800,000 - $140,000 = $660,000

  After 5 years of similar activity:
    Basis could fall below $500,000 even though capital has not been returned
    At basis = $0: any further cash distribution triggers gain
    LP has been receiving tax shelter (distributing cash while claiming losses)
    At sale: recapture -- all that sheltered gain comes back as Section 1250 or Section 1231 gain
```

### Basis Deficiency Warning

```
Screen each LP before distributing:
  1. Retrieve LP's estimated adjusted outside basis from fund records or CPA
  2. Compare distribution amount to remaining outside basis
  3. If distribution > basis:
     a. Notify LP immediately (before wiring, if possible)
     b. Quantify taxable portion: distribution_amount - outside_basis
     c. Character of excess: typically Section 731 gain (capital gain if LP interest
        held > 12 months, ordinary if short-term)
     d. Flag in K-1 preview and distribution notice

  Common causes of basis deficiency:
    - Extended holding period with heavy depreciation (cost seg + bonus depreciation)
    - Prior years of cash distributions reducing basis
    - Debt paydown events that release nonrecourse liabilities (reduces basis)
    - Prior suspended losses that were later allowed reducing future basis room
```

---

## Part II: Ordinary Income Determination

### What Creates Ordinary Income at the LP Level?

Ordinary income flows to LPs through the K-1 when the partnership generates income that is not sheltered by deductions:

```
K-1 Box 1 (Ordinary business income) -- non-rental activities
K-1 Box 2 (Net rental real estate income) -- rental real estate

Operating distributions are funded by rental income (gross rents minus operating expenses
and debt service). The taxable component is what remains after depreciation:

  Gross rental income:                    $2,000,000
  Operating expenses:                    ($800,000)
  Depreciation (straight-line):          ($600,000)
  Depreciation (cost segregation):       ($400,000)
  Net taxable income per partnership:     $200,000  <- allocated to LPs pro-rata

  But partnership distributed:          $1,000,000 in cash
  Cash distributed vs. taxable income: $1,000,000 vs. $200,000
  -> LP received $1,000,000 but only $200,000 is taxable (the rest is return of basis from depreciation)
```

### Section 1250 Recapture -- The Depreciation Payback

Section 1250 recapture is the IRS mechanism for recovering the tax benefit of depreciation deductions when a property is sold. It converts what would otherwise be capital gain into a higher-tax category.

```
Two components:

1. Unrecaptured Section 1250 gain (most common):
   - Applies to straight-line depreciation on real property (buildings, improvements)
   - Taxed at a maximum federal rate of 25% for individuals (vs. 20% LTCG rate)
   - Does NOT trigger ordinary income rates -- it is still technically a capital gain
   - Amount: total accumulated straight-line depreciation claimed on the real property

2. Section 1245 recapture (personal property and cost seg components):
   - Applies to accelerated depreciation on personal property and short-life components
   - Taxed at ordinary income rates (up to 37%)
   - Amount: the lesser of (a) gain on sale and (b) depreciation claimed on the component
   - For cost segregation 5/7/15-year components with bonus depreciation: this can be significant

Example (sale after 5 years):
  Purchase price:                        $10,000,000
    Building (39-year):                   $7,500,000
    Land:                                 $2,000,000
    Cost seg components (5/7/15-year):      $500,000

  Depreciation claimed over 5 years:
    Building: $7,500,000 / 39 * 5 = $961,538 (Section 1250)
    Cost seg: $500,000 (mostly/fully deducted via bonus depreciation in Year 1) (Section 1245)

  Sale price: $12,000,000
  Adjusted basis: $10,000,000 - $961,538 - $500,000 = $8,538,462
  Total gain: $12,000,000 - $8,538,462 = $3,461,538

  Character breakdown:
    Section 1245 recapture (ordinary income): $500,000
    Section 1250 unrecaptured gain (25%):     $961,538
    Section 1231 gain (LTCG at 20%):          $2,000,000
    Total gain:                               $3,461,538

  LP001 (15% ownership):
    Ordinary income (Sec 1245):  $500,000 * 15% = $75,000
    Sec 1250 unrecaptured:       $961,538 * 15% = $144,231 (Box 9c)
    LTCG (Sec 1231):             $2,000,000 * 15% = $300,000 (Box 9a / Box 10)
```

---

## Part III: Capital Gain Determination

### Section 1231 Gain

Most CRE appreciation is characterized as Section 1231 gain for assets held more than 12 months. Section 1231 gain is taxed at long-term capital gain rates (0%, 15%, or 20% for individuals depending on income).

```
Section 1231 gain applies when:
  - Depreciable real or personal property used in a trade or business
  - Held more than 12 months
  - Gain exceeds any Section 1245 or Section 1250 recapture

Net Section 1231 position:
  If LP has Section 1231 losses from prior years (within the last 5 years):
    Section 1231 gain is first recharacterized as ordinary income to offset
    prior Section 1231 losses (the "lookback rule")
    This can be material for LPs who received loss allocations in early years

  Check for Section 1231 loss carryforward: ask LP or LP's tax advisor
```

### Long-Term vs. Short-Term

```
LP holding period = LP's holding period in the partnership interest
  Typically starts when LP made their capital contribution

If LP invested less than 12 months before sale:
  Gain allocated to that LP may be short-term (ordinary rates)
  Check LP's subscription date vs. sale date

For fund-level assets held > 12 months:
  The partnership's gain is long-term; passes through to all LPs
  regardless of how long each LP has held their interest
  Exception: LP's own holding period matters for certain purposes;
  consult fund counsel if any LP has held their interest < 12 months
```

### Net Investment Income Tax (NIIT)

```
Section 1411 imposes a 3.8% tax on net investment income for high-income individuals:
  Threshold: $250,000 (MFJ) / $200,000 (single) / $125,000 (MFS) in MAGI

Applies to:
  - Ordinary income from passive activities (most LP interests are passive)
  - Capital gains from passive activities
  - Rental income (if LP is passive -- typically yes)

Does NOT apply to:
  - Active trade or business income (rare for LP interests in real estate)
  - Wages, self-employment income

Practical impact:
  High-income LP effective rate on real estate gain:
    LTCG: 20% federal + 3.8% NIIT = 23.8%
    Sec 1250: 25% + 3.8% NIIT = 28.8%
    Ordinary income: 37% + 3.8% NIIT = 40.8%
  State income tax is additional.

In K-1 preview:
  Flag the NIIT exposure but do not calculate it per LP -- NIIT depends on
  each LP's total income and is calculated on their individual return.
  Include a note: "Depending on your total income, you may be subject to
  the 3.8% Net Investment Income Tax on passive income from the Fund."
```

---

## Part IV: K-1 Preview Methodology

### What a K-1 Preview Covers

A K-1 preview is an estimate issued alongside the distribution notice to help LPs plan estimated tax payments. It is clearly labeled as preliminary and not final.

```
Key K-1 boxes for real estate partnerships:

Box 1: Ordinary business income (loss)
  - Net rental income after depreciation and expenses
  - Most common for operating distributions

Box 2: Net rental real estate income (loss)
  - Specifically for rental real estate activities
  - Same concept as Box 1 but for passive rental activities

Box 9a: Net long-term capital gain (loss)
  - Section 1231 gains from property sales
  - Reported as LTCG on LP's individual return (Schedule D)

Box 9c: Unrecaptured Section 1250 gain
  - Subset of Box 9a representing accumulated straight-line depreciation
  - Taxed at 25% max rate
  - Does not appear separately on Schedule D for the LP; LP must track separately

Box 10: Net Section 1231 gain (loss)
  - Redundant with 9a in many cases; may capture different Section 1231 items
  - LP uses Form 4797 to report Section 1231 activity

Box 19A: Distributions (cash and marketable securities)
  - Total cash distributions during the year
  - Not income itself; basis tracking determines taxability

Box 20W: Unrelated business taxable income (UBTI)
  - Critical for tax-exempt LPs (pension funds, endowments, IRAs)
  - UBTI triggers tax on an otherwise exempt entity
  - Common sources: debt-financed income, operating income from certain activities

Box 20N: Business interest expense limitation (Section 163(j))
  - Limits deductibility of business interest for certain partnerships
  - Post-TCJA issue for highly leveraged real estate funds
  - May create disallowed interest expense passed to LP
```

### K-1 Preview Calculation Steps

```
Step 1: Obtain fund-level preliminary tax figures from CPA
  - Total rental income
  - Total operating expenses (cash)
  - Total depreciation (straight-line + cost seg + bonus)
  - Net Section 1231 gain (if sale occurred)
  - Section 1250 recapture (if sale occurred)
  - Total distributions

Step 2: Allocate fund-level figures to each LP by ownership percentage
  LP share = fund-level amount * LP_ownership_pct

Step 3: Populate K-1 boxes per LP
  Box 2: LP share of net rental income (fund income less depreciation)
  Box 9a: LP share of Section 1231 gain
  Box 9c: LP share of Section 1250 unrecaptured gain
  Box 19A: LP's actual cash distributions this year

Step 4: Add advisory language
  "This is a preliminary estimate. Final K-1 will be issued by [date].
  Consult your tax advisor for your specific tax treatment."

Step 5: Flag special situations
  - LP with negative basis: note gain recognition on distribution
  - Tax-exempt LP (pension fund): UBTI analysis required
  - Foreign LP: FIRPTA withholding may apply on sale proceeds
  - LP with Section 1231 loss carryforward: note potential recharacterization
```

### FIRPTA Considerations for Foreign LPs

```
If any LP is a non-US person (individual or entity), special rules apply on sale proceeds:

FIRPTA (Foreign Investment in Real Property Tax Act):
  - Requires withholding of 15% of the gross sale proceeds allocable to the foreign LP
  - Withholding is the buyer's/partnership's obligation
  - Applies when the partnership disposes of US real property interests

Practical impact on distribution:
  Foreign LP's gross distribution: $[AMOUNT]
  FIRPTA withholding (15% of gross sale price attributable to LP): $[AMOUNT]
  Net distribution to foreign LP: $[NET]
  Withholding remitted to IRS: $[AMOUNT]

  Note: 15% withholding is on the LP's share of gross sale price,
  NOT on the distribution amount. Can exceed the LP's distribution
  if leverage is high and gain is a large portion of gross proceeds.

Action items:
  1. Identify any foreign LPs before distributing sale proceeds
  2. Engage qualified tax counsel for FIRPTA analysis
  3. File Form 8288-A for each foreign LP within 20 days of withholding
  4. Gross-up foreign LP's notice to show gross distribution and withholding separately
```

---

## Part V: Distribution Type Quick Reference

### Operating Cash Flow

```
Characterization:
  Primary: ordinary income (rental income less cash expenses and depreciation)
  Secondary: return of capital if depreciation exceeds taxable income (common in early years)

Typical K-1 treatment:
  Heavy depreciation (cost segregation) years:
    Box 2 shows a loss -> LP gets cash distribution but shows paper loss
    Cash distribution reduces basis; loss further reduces basis
    Both reduce LP's future taxable exposure (or create deferred gain)

  Mature stabilized property (minimal remaining depreciation):
    Box 2 shows income -> LP receives cash AND taxable income
    Fully taxable distribution; no sheltering

Tax planning note for LPs:
  In early years: LP benefits from cash + paper losses (tax shelter)
  In later years: LP receives cash + income (fully taxable)
  At sale: accumulated depreciation creates recapture (gain comes back)
  The total tax bill is deferred, not eliminated
```

### Refinance Proceeds

```
Characterization:
  Return of capital first (up to LP's outside basis)
  Gain if distribution exceeds outside basis

Why refinancing is not a taxable event (generally):
  A loan is not income -- borrowed money creates a liability, not income
  LP's share of the new loan INCREASES their outside basis (if nonrecourse)
  The distribution DECREASES their outside basis
  Net impact: basis often unchanged or modestly reduced

When refinancing DOES trigger gain:
  Excess nonrecourse debt scenario: if the new loan plus prior distributions
  have pushed the LP's outside basis to near zero, the distribution may exceed
  remaining basis -> taxable gain

  Example:
    LP contributed $500,000 three years ago
    LP's share of new nonrecourse loan: $750,000 (increases basis)
    LP's depreciation allocations (3 years): ($450,000) (decreases basis)
    LP's prior distributions: ($200,000) (decreases basis)
    LP's outside basis: $500,000 + $750,000 - $450,000 - $200,000 = $600,000
    Refi distribution: $150,000
    Taxable? No -- $150,000 < $600,000 basis. Non-taxable.

    New outside basis: $600,000 - $150,000 = $450,000
```

### Sale Proceeds

```
Full characterization hierarchy:

1. Return of basis (non-taxable)
   Amount: LP's adjusted outside basis at time of sale
   Reduces basis to zero

2. Section 1245 recapture (ordinary income)
   Amount: accelerated depreciation on personal property components
   Taxed at ordinary income rates

3. Section 1250 unrecaptured gain (25% rate)
   Amount: straight-line depreciation on real property
   Reports on K-1 Box 9c
   25% federal rate maximum

4. Section 1231 gain (LTCG rates)
   Amount: remaining gain after recapture and basis recovery
   Reports on K-1 Box 9a and Box 10
   LTCG rates (0/15/20% depending on LP's income)

5. Section 1231 lookback recharacterization
   If LP received net Section 1231 losses in prior 5 years:
   Current Section 1231 gain first recharacterizes as ordinary income
   until prior losses are offset (Form 4797)

Total tax example (high-income LP, 20% LTCG rate):
  Section 1245 ordinary income: $X * 40.8% (37% + 3.8% NIIT)
  Section 1250 unrecaptured: $X * 28.8% (25% + 3.8% NIIT)
  Section 1231 LTCG: $X * 23.8% (20% + 3.8% NIIT)
  Blended effective rate on total gain: typically 24-30% for high-income individual LPs
```

### Return of Capital (Non-Disposition)

```
Characterization: non-taxable return of capital in virtually all cases
  (assuming LP's basis is positive and sufficient)

K-1 treatment:
  Box 19A: full distribution amount
  No income items unless basis is deficient

Basis tracking:
  Each dollar returned reduces LP's outside basis by one dollar
  At basis = $0: future distributions trigger gain
  At basis = $0: future loss allocations are suspended (cannot deduct)

Importance of basis tracking:
  For LPs who have received multiple return-of-capital distributions
  over several years, their basis may be very low
  A large operating distribution or sale could cause unexpected taxable gain
  Fund administrator should track and communicate estimated basis annually
```

---

## Part VI: Disclaimer Language for LP Notices

Always include the following (or substantially similar) language in any distribution notice that includes tax characterization:

```
TAX DISCLAIMER

The tax information contained in this distribution notice is a preliminary
estimate provided for informational and tax-planning purposes only. It does
not constitute tax advice, and [Fund Manager Name] makes no representation
as to the accuracy or completeness of the tax characterization for any
individual investor's specific circumstances.

The final Schedule K-1 for tax year [YYYY] will be prepared by [CPA Firm Name]
and is expected to be delivered by [March 15 / September 15 if extended].

Each limited partner should consult their own qualified tax advisor regarding
the federal, state, and local tax implications of this distribution, including
the determination of adjusted outside basis, characterization of gain or loss,
and any applicable withholding requirements for non-US investors.

[Fund Manager Name] and its affiliates do not assume any responsibility for
tax liabilities arising from the treatment of this distribution.
```
