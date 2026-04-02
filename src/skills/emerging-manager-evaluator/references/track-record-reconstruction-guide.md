# Track Record Reconstruction Guide
# Reference for emerging-manager-evaluator skill
# How to attribute deals from prior platforms, discount methodology, and survivorship bias controls

---

## Purpose

When a first-time or second-time fund manager presents a track record, that record typically consists of deals executed at a prior employer or employers. The raw deal metrics (MOIC, IRR) belong to the fund, not to the individual. This guide provides the methodology for extracting a fair and conservative estimate of the GP's personal contribution to those results.

The goal is not to give the GP as much credit as possible. The goal is to construct a track record that accurately reflects the GP's decision-making capacity -- the input that will determine the new fund's outcomes.

---

## Step 1: Raw Deal List Construction

Request from the GP a complete deal list with the following fields for each deal. If the GP omits any field, request it before proceeding.

### Required Fields per Deal

| Field | Description | Acceptable Formats |
|-------|-------------|-------------------|
| Deal identifier | Property name or address | Any unique reference |
| Property type | Asset class | MF, industrial, office, retail, hotel, mixed-use |
| Market | City and submarket | e.g., "Atlanta -- Buckhead" |
| Vintage year | Year of acquisition | YYYY |
| Exit year | Year of disposition or current status | YYYY or "Unrealized as of [date]" |
| Invested equity | Total equity invested (at fund level) | $ |
| Exit value or current value | Realized proceeds or current mark | $ |
| Gross MOIC | Fund-level gross MOIC | x |
| Gross IRR | Fund-level gross IRR (annualized) | % |
| GP's role | Self-described role on this deal | See role definitions below |
| Confirmation source | Who can confirm this role? | Name, title, firm |

### Role Definitions

The GP must self-classify each deal. Do not accept ambiguous descriptions.

| Role Code | Title | Meaning |
|-----------|-------|---------|
| SL | Sole Lead | GP was the only decision-maker. No supervisor approval required for execution. |
| CL_E | Co-Lead, Equal | Two principals shared authority equally. |
| CL_J | Co-Lead, Junior | GP participated in leadership but the other party was primary. |
| DTL | Deal Team Lead | GP managed execution (diligence, closing, operations) but did not set strategy. Another principal made investment decision. |
| DTM | Deal Team Member | GP was part of the deal team. Decisions were made by others. |
| ANA | Analytical/Support | GP provided analysis or support. No material decision-making involvement. |

---

## Step 2: Confirmation Protocol

Attribution is only as reliable as the confirmation behind it. Unconfirmed attributions are excluded from the adjusted track record.

### Confirmation Hierarchy (strongest to weakest)

1. **Written confirmation from prior employer principal** (former supervisor or partner who can verify the GP's role). Request via email or call. Accept: signed letter, written email, or confirmed call notes.

2. **Written confirmation from co-investor** (institutional LP or co-GP who co-invested on the deal and interacted with this GP directly).

3. **Written confirmation from lender** (bank or debt fund that originated the loan, spoke with GP directly as the borrower representative).

4. **Public records cross-reference** (property ownership records, public deed filings confirming the entity, press releases, broker marketing materials naming the principal). Public records can confirm deal existence and timing but cannot confirm role.

5. **GP self-certification only (no third-party confirmation)** -- accepted only for deals where the GP was the sole owner/operator (personal deals). All fund-level deals require third-party confirmation.

### Minimum Confirmation Requirement

For the adjusted track record to be usable:
- At least 50% of attributed equity must be confirmed by sources #1-#3 above
- Deals with only GP self-certification are excluded from the adjusted track record
- Deals confirmed only by public records are downgraded to DTM role (50% discount minimum)

### Confirmation Request Script

When requesting confirmation from a prior employer:

> "We are conducting reference due diligence on [GP Name], who is raising [Fund Name]. We understand [GP Name] was involved in [Deal Name / Address]. Could you confirm: (1) the nature of [GP Name]'s role on this deal, (2) whether they were the lead decision-maker or a participant, and (3) the approximate dollar amount of equity the deal involved? We are not asking you to evaluate their performance, only to confirm their role."

---

## Step 3: Attribution Discount Schedule

Once the role is confirmed, apply the attribution weight.

### Primary Discount Schedule

| Role | Attribution Weight | Rationale |
|------|--------------------|-----------|
| SL -- Sole Lead | 100% | GP made all material decisions independently |
| CL_E -- Co-Lead, Equal | 60% | GP shared authority; both parties contributed equally |
| CL_J -- Co-Lead, Junior | 40% | GP was secondary; primary principal drove outcome |
| DTL -- Deal Team Lead | 50% | GP executed deal but did not set investment thesis |
| DTM -- Deal Team Member | 20% | GP participated; decisions made by others |
| ANA -- Analytical/Support | 5% | GP contributed analysis; no decision-making role |

### Adjustment Factors

**Confirmation quality discount:**

| Confirmation Source | Adjustment to Attribution Weight |
|---------------------|----------------------------------|
| Written confirmation from prior employer (source #1) | No adjustment (full weight) |
| Written confirmation from co-investor (source #2) | No adjustment |
| Written confirmation from lender (source #3) | -5 percentage points |
| Public records only (source #4) | Cap at DTM weight (20% maximum) |
| GP self-certification only | Excluded (0%) |

**Vintage recency discount:**

Older deals may reflect a different market environment or team structure than the current opportunity. Apply an additional discount for deals more than 10 years before the fund launch:

| Deal Age at Fund Launch | Vintage Discount |
|------------------------|-----------------|
| 0-5 years | 0% (no discount) |
| 5-10 years | -5 percentage points |
| > 10 years | -15 percentage points |

Note: Vintage discount is additive to confirmation quality discount but does not reduce attribution below 5% for confirmed lead deals.

**Size mismatch discount:**

If the attributed deal equity is more than 3x the proposed fund's target deal equity, the deal may have required platform resources not replicable at the new fund:

| Deal Size vs Proposed Fund Deal Size | Size Discount |
|-------------------------------------|--------------|
| Within 3x | 0% (no discount) |
| 3x-5x larger | -10 percentage points |
| > 5x larger | -20 percentage points |

---

## Step 4: Adjusted Track Record Computation

Apply all discounts to compute the attribution-adjusted deal metrics.

### Calculation

```
For each deal:
  Final Attribution Weight = Role Weight * (1 - Confirmation Discount) * (1 - Vintage Discount) * (1 - Size Discount)

  Note: Discounts are multiplicative, not additive.
  Example: Role = CL_E (60%), Confirmation = lender (-5%), Vintage = 7 years old (-5%), Size = 2x (0%)
  Final Weight = 60% * (1 - 0.05) * (1 - 0.05) * (1 - 0.00) = 60% * 0.95 * 0.95 = 54.15%

  Adjusted Equity = Deal Equity * Final Attribution Weight
  Adjusted Proceeds = Exit Value * Final Attribution Weight
  Adjusted Cash Flows = [(-Adjusted Equity, acquisition_date), (Adjusted Proceeds, exit_date)]
```

### Portfolio-Level Statistics

```
Adjusted MOIC = Sum(Adjusted Proceeds for realized deals) / Sum(Adjusted Equity for realized deals)

Adjusted IRR = XIRR(all adjusted cash flows for all deals)
  Note: Use deal-level cash flows, not a single portfolio MOIC. XIRR reflects timing.

Adjusted Weighted Average Alpha:
  For each deal:
    Benchmark IRR = NCREIF NPI total return for [property type, region] over [hold period]
    Deal Alpha = Adjusted IRR - Benchmark IRR

  Weighted Average Alpha = Sum(Deal Alpha * Adjusted Equity) / Sum(Adjusted Equity)

Hit Rate = Confirmed deals with Adjusted MOIC > 1.0x / Total confirmed deals

Loss Ratio = Sum(Adjusted Equity for deals with Adjusted MOIC < 1.0x) / Sum(Total Adjusted Equity)
```

---

## Step 5: Survivorship Bias Check

The single most common form of track record fraud is omission -- the GP presents only winning deals. A rigorous survivorship bias check is mandatory.

### Protocol

1. Ask directly: "Is the list you provided the complete set of deals you were involved with at [prior employer]? Are there any deals you were involved with that are not on this list?"

2. Cross-reference with prior employer (if willing): request the full list of deals the GP participated in from the reference contact at the prior firm.

3. Review public records: for the GP's tenure at each firm, search for press releases, deal announcements, property records, and industry news that may reference deals not on the GP's list.

4. Ask co-investors and lenders: "Are there other deals you worked with [GP Name] on that they did not mention?"

### Bias Assessment

```
Survivorship bias score:
  No evidence of omissions (explicit confirmation from reference contact): Low bias, full credit
  Minor possible omissions (1-2 deals referenced by third parties not on GP list): Moderate bias
    Action: Request explanation; if GP cannot explain, include those deals at DTM attribution
  Confirmed omissions (GP admitted or evidence confirms): High bias
    Action: Include all omitted deals at full attribution weight
    If survivorship-adjusted alpha differs from presented track record by > 150 bps:
      RED FLAG: Track record credibility is materially impaired.
      Reduce confidence score by 20 points (overlapping with SKILL.md guidance).

Survivorship bias documentation:
  Record in evaluation report:
    - Number of deals in GP-presented list: [X]
    - Number of deals in third-party-confirmed list: [Y]
    - Difference: [Z deals, representing $[M] in equity]
    - Survivorship-adjusted alpha: [bps]
    - Adjustment to alpha vs presented alpha: [bps]
```

---

## Step 6: Benchmark Selection

### NCREIF NPI Benchmarks by Property Type

Use the appropriate NCREIF NPI subindex for each deal's property type and region. The benchmark represents a passively managed, unlevered institutional property return. The GP's alpha is the incremental return above this passive benchmark, after adjusting for attribution.

**Default benchmark sources (in order of preference):**
1. NCREIF NPI by property type and region (NCREIF quarterly data)
2. Cambridge Associates Real Estate benchmark by strategy (value-add, opportunistic) and vintage
3. CoStar market total return index by submarket (for secondary market deals where NCREIF coverage is thin)

**Benchmark application:**
- Match benchmark to deal vintage (hold period) and property type
- Match geography: NCREIF reports by region (East, Midwest, South, West). Use regional NPI, not national.
- If deal is in a secondary or tertiary market where NCREIF coverage is limited: use regional NPI and note the limitation

### Leverage Adjustment

NCREIF NPI returns are unlevered. The GP's track record returns are levered. To compare fairly, adjust the benchmark for leverage:

```
Levered Benchmark Return = Unlevered Benchmark Return + (Unlevered Benchmark Return - Cost of Debt) * (LTV / (1 - LTV))

Note: Cost of Debt = weighted average cost of debt on the deal during the hold period

This gives the expected levered return for a passive manager with the same leverage.
The GP's alpha = Adjusted Deal IRR - Levered Benchmark Return
```

---

## Step 7: Interpretation Standards

### Adjusted Track Record Quality Tiers

| Metric | Strong | Acceptable | Weak |
|--------|--------|-----------|------|
| Number of confirmed deals | 5+ | 3-4 | < 3 |
| Confirmed attributed equity | > $50M | $20-$50M | < $20M |
| Weighted avg alpha (adjusted) | > 200 bps | 100-200 bps | 0-100 bps |
| Alpha vs presented (unadjusted) | < 150 bps reduction | 150-300 bps reduction | > 300 bps reduction |
| Hit rate (deals > 1.0x MOIC) | > 80% | 60-80% | < 60% |
| Loss ratio | < 10% | 10-20% | > 20% |
| Survivorship bias evidence | None | Minor | Confirmed |

### Reporting Requirements

The adjusted track record summary in the evaluation report must include:

1. Total deals in GP's presented list vs. confirmed deals
2. Total presented equity vs. confirmed attributed equity
3. Unadjusted (raw GP-presented) metrics: MOIC and IRR
4. Attribution-adjusted metrics: MOIC and IRR
5. Alpha vs. applicable NCREIF benchmark (levered-adjusted)
6. Hit rate and loss ratio (attribution-adjusted)
7. Survivorship bias assessment and impact
8. Confidence statement: "This adjusted track record is based on [X] confirmed deals representing [$M] in attributed equity, confirmed by [N] reference sources. Confidence: [High/Medium/Low]."

---

## Common Fraud and Manipulation Patterns

### Pattern 1: Role Inflation

GP describes every deal as "co-led" or "led" regardless of actual contribution. Counter: Request prior employer confirmation with specific role question. Ask co-investors: "Who made the final investment decision on this deal -- the [prior employer] team as a whole, or [GP Name] specifically?"

### Pattern 2: Portfolio Selection Bias

GP selects only top-performing deals for inclusion. Counter: Survivorship bias protocol in Step 5. Request full deal list from reference contacts at prior employer.

### Pattern 3: Attribution Creep

GP attributes the full deal return to their contribution without discount. Counter: Apply the discount schedule in Step 3 rigorously. A 100% attribution claim on a deal where the GP was one of five partners is not credible.

### Pattern 4: Benchmark Cherry-Picking

GP selects a weak benchmark to inflate alpha. Example: comparing value-add multifamily returns to a core benchmark. Counter: Match benchmark to actual strategy (use Cambridge VA benchmark for value-add deals, not NCREIF core).

### Pattern 5: Vintage Manipulation

GP presents a track record that includes only favorable vintage years (e.g., 2012-2019) and excludes deals from 2020 or 2022. Counter: Verify that the deal list covers the GP's complete tenure at each employer, not a curated vintage window.

### Pattern 6: Leverage Omission

GP presents unlevered deal returns to make results look more stable. Counter: Always request deal-level debt terms (LTV and rate). If the GP cannot provide them, apply a conservative levered return adjustment.

---

## Template: Attribution Summary Table

Use this format in the evaluation report.

| Deal ID | Property Type | Market | Role | Final Attribution % | Equity ($M) | Adj Equity ($M) | Gross MOIC | Adj MOIC | Deal Alpha (bps) | Confirmed By |
|---------|-------------|--------|------|---------------------|-------------|-----------------|-----------|---------|-----------------|-------------|
| Deal 1 | MF | Atlanta, GA | SL | 95% | 12.5 | 11.9 | 1.92x | 1.87x | +220 | Prior employer |
| Deal 2 | MF | Nashville, TN | CL_E | 57% | 22.0 | 12.5 | 1.61x | 1.55x | +140 | Co-investor |
| Deal 3 | MF | Charlotte, NC | DTL | 50% | 18.0 | 9.0 | 1.45x | 1.43x | +80 | Lender |
| Deal 4 | Industrial | Nashville, TN | CL_J | 38% | 35.0 | 13.3 | 2.10x | 2.05x | +310 | Prior employer |
| Deal 5 | MF | Tampa, FL | SL | 100% | 8.5 | 8.5 | 1.82x | 1.82x | +190 | Public records (deed) |
| **Total** | | | | **Wtd avg 73%** | **96.0** | **55.2** | **1.78x** | **1.71x** | **+188 bps** | |

**Confidence:** High -- 4 of 5 deals confirmed by direct reference; 1 confirmed by public records only.

**Survivorship bias:** Prior employer reference confirmed this is a complete list of deals for the GP's tenure.
