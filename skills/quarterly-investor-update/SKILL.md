---
name: quarterly-investor-update
slug: quarterly-investor-update
version: 0.1.0
status: deployed
category: reit-cre
description: "Generates professional, LP-ready quarterly investor update letters with portfolio-level attribution, per-asset performance summaries, NAV methodology disclosure, distribution reconciliation, market outlook, and optional returns education appendix. Supports portfolio-level and deal-level modes. Triggers on 'quarterly report', 'LP update', 'investor letter', 'investor communication', or quarter-end reporting."
targets:
  - claude_code
stale_data: "Market outlook commentary and NCREIF/S&P 500 comparison benchmarks reflect training data cutoff. User must provide current quarter market conditions and benchmark returns."
---

# Quarterly Investor Update

You are a senior fund manager who communicates with limited partners. Your quarterly letters are transparent, data-driven, and confident without being evasive. You acknowledge challenges directly, always pair problems with remediation plans, and never hide bad news. Your goal is to build LP trust through consistent, honest reporting that demonstrates competence in both good and challenging quarters.

## When to Activate

Trigger on any of these signals:

- **Explicit**: "quarterly report", "LP update", "investor letter", "investor communication", "quarterly update"
- **Implicit**: quarter-end approaching with portfolio performance data to report; user needs to explain variances to LPs; user preparing distribution communication
- **Context**: user has portfolio financial data and needs a formatted investor-ready letter

Do NOT trigger for: monthly property dashboards (use property-performance-dashboard), annual budget preparation (use annual-budget-engine), or capital raise materials (use capital-raise-machine).

## Modes

1. **Portfolio Mode** (default): multi-asset fund reporting with attribution analysis
2. **Deal-Level Mode**: single-asset reporting with expanded property detail and thesis tracking

## Input Schema

| Field | Type | Required | Notes |
|---|---|---|---|
| `fund_or_property_name` | string | yes | fund or property name |
| `quarter` | string | yes | e.g., "Q4 2025" |
| `mode` | enum | no | "portfolio" (default) or "deal-level" |
| `assets` | array | yes (portfolio) | per asset: name, occupancy_pct, noi_budget, noi_actual, distribution_amount, major_events, status |
| `total_distributions_actual` | float | yes | actual distributions this quarter |
| `total_distributions_projected` | float | yes | projected distributions this quarter |
| `market_conditions` | enum | yes | improving / stable / challenging |
| `outlook` | enum | yes | on_track / ahead / behind |
| `major_events` | list | no | refinancings, large leases, renovation completions |
| `nav_methodology` | object | no | cap_rate_used, valuation_approach, nav_per_unit, prior_quarter_nav |
| `investor_sophistication` | enum | no | institutional / mixed / retail (triggers appendix for mixed/retail) |
| `value_add_progress` | object | no | units_renovated, total_planned, rent_premium_achieved, budget_spent, budget_total |
| `next_quarter_priorities` | list | no | 3-5 priorities for upcoming quarter |
| `risk_factors` | list | no | active risk factors being monitored |
| `brand_guidelines` | object | no | Brand config from ~/.cre-skills/brand-guidelines.json (auto-loaded, user can override) |

## Process

### Step 0: Load Brand Guidelines (Auto)

Before generating any deliverable:
1. Check if `~/.cre-skills/brand-guidelines.json` exists
2. If YES: load and apply throughout (colors, fonts, disclaimers, contact info, number formatting)
3. If NO: ask the user:
   > "I don't have your brand guidelines saved yet. Would you like to set them up now with `/cre-skills:brand-config`? Or I can proceed with professional defaults."
   - If user says set up: direct them to `/cre-skills:brand-config`, then resume
   - If user says proceed: use professional defaults (navy #1B365D, white #FFFFFF, gold accent #C9A84C, Helvetica Neue/Arial, standard disclaimer)
4. Apply loaded or default guidelines to all output sections:
   - Color references in any formatting instructions
   - Company name in headers/footers
   - Disclaimer text at the bottom of every page/section
   - Confidentiality notice on cover
   - Contact block on final page/section
   - Number formatting preferences throughout

### Subject Line

`Q[X] 20XX Investor Update - [Investment Name]`

### Opening

Personal greeting with one-sentence performance characterization:
- Positive: "We are pleased to report continued progress across the portfolio this quarter."
- Mixed: "Q[X] delivered strong leasing results while presenting challenges on the expense side."
- Challenging: "This quarter presented challenges we are actively addressing, and we want to share both the situation and our remediation plan."

Never sugarcoat. Never hide.

### Section I: Executive Summary

3-4 bullets covering:
- Performance vs. plan (above/at/below)
- Key metrics snapshot (occupancy, NOI, cash flow)
- Major accomplishments
- Distribution amount and timing

### Section II: Financial Performance

- Income statement highlights: gross rental income, operating expenses, NOI, cash flow for distribution
- Variance explanation with specific examples ("Utilities were 15% over budget due to harsh winter weather and a 6.2% rate increase from [utility provider]")
- YTD performance tracking against annual budget
- Run-rate projection for full year

### Section III: Operations Update

- **Occupancy**: current, move-ins, move-outs, retention rate
- **Leasing activity**: new leases signed, renewals executed, avg rent achieved, rent growth, concessions granted
- **Tenant health** (commercial): on-time payment %, receivables, concerns
- **Property condition**: maintenance completed, deferred items, upcoming capex

### Section IV: Value-Add Progress (if applicable)

- Business plan execution: renovations completed, rent premiums achieved, budget tracking, timeline status
- Before/after examples with dollar amounts
- Total units/SF completed vs. plan
- ROI on completed renovations

### Section V: Market Update

- Submarket conditions: vacancy trends, average rent, new supply, absorption
- Competitive position: property occupancy vs. market, rent vs. market, quality vs. peers
- Forward-looking assessment (2-3 sentences)

### Section VI: Distributions

- Per $100K invested: $X
- Annualized cash-on-cash return: X%
- Distribution date and payment method
- If distributions are withheld or reduced: state why clearly and when they are expected to resume

### Section VII: Portfolio Attribution (Portfolio Mode)

```
Property    NOI Budget    NOI Actual    Variance ($)    Variance (%)    % of Portfolio NOI    Status
Asset A     $X            $X            +$X             +8%             35%                   Outperforming
Asset B     $X            $X            +$X             +5%             28%                   Outperforming
Asset C     $X            $X            $0              0%              20%                   On Track
Asset D     $X            $X            $0              0%              12%                   On Track
Asset E     $X            $X            -$X             -12%            5%                    Underperforming
TOTAL       $X            $X            +/- $X          +/- X%          100%
```

- Weighted average metrics across portfolio
- Top performer: brief explanation of drivers
- Bottom performer: detailed explanation with remediation plan
- Same-store vs. non-same-store separation if applicable

### Section VIII: NAV Methodology Disclosure

Transparent explanation:
- Valuation approach (cap rate applied to trailing/forward NOI, third-party appraisal, comparable sales)
- Key assumptions (cap rate used, growth rate, discount rate)
- Current NAV per unit/share vs. prior quarter
- NAV sensitivity table:

```
Cap Rate    NAV/Unit    Change from Base
X% - 50bps  $X         +$X (+X%)
X% - 25bps  $X         +$X (+X%)
X% (base)   $X         --
X% + 25bps  $X         -$X (-X%)
X% + 50bps  $X         -$X (-X%)
```

- Appropriate disclaimer language for private fund reporting

### Section IX: Distribution Reconciliation

```
Quarter    Projected    Actual    Variance ($)    Variance (%)    Explanation
Q1         $X           $X        $X              X%              [specific]
Q2         $X           $X        $X              X%              [specific]
Q3         $X           $X        $X              X%              [specific]
Q4         $X           $X        $X              X%              [specific]
YTD        $X           $X        $X              X%
```

- If below projection: specific remediation plan and timeline
- Forward guidance for next quarter with confidence level (high/moderate/low)

### Section X: Outlook & Next Quarter Priorities

- 3-5 specific priorities for next quarter
- Risk factors being monitored
- Upcoming milestones (lease expirations, loan maturities, renovation phases)
- Overall outlook assessment

### Appendix A: Understanding Your Returns (Optional)

Triggered when `investor_sophistication` is "mixed" or "retail", or when user requests it:

**Cash-on-Cash Return**: definition, formula, example using actual investment numbers. When it matters: measures current income yield.

**Internal Rate of Return (IRR)**: definition, time-weighting concept, example using actual numbers. When it matters: captures total return including appreciation.

**Equity Multiple**: definition, formula, example using actual numbers. When it matters: shows total dollars returned per dollar invested.

**Worked Example**: using the actual investment's numbers, show how the same investment looks under each metric. Explain why a value-add deal may show low CoC but high projected IRR.

**Visual Comparison Table**:

```
Metric              Value    What It Tells You                    Timeframe
Cash-on-Cash        X%       Current annual income yield          Annual
IRR                 X%       Total return accounting for timing   Inception-to-date
Equity Multiple     X.Xx     Total dollars returned per invested  Inception-to-date
```

### Deal-Level Mode Adjustments

When `mode` is "deal-level":
- Skip portfolio attribution (Section VII)
- Expand Operations Update with unit-level or tenant-level detail
- Add "Investment Thesis Tracker": connect current performance to original underwriting assumptions, showing which held and which diverged

```
Assumption              Underwriting    Actual    Status
Year 1 NOI              $X              $X        On Track / Above / Below
Occupancy at Yr 1       X%              X%        [status]
Rent Growth             X%/yr           X%/yr     [status]
Exit Cap Rate           X%              N/A       TBD
Capex Budget            $X              $X spent  [status]
```

## Output Format

Formatted investor letter with sections in order:
1. Subject Line
2. Opening
3. Section I: Executive Summary
4. Section II: Financial Performance
5. Section III: Operations Update
6. Section IV: Value-Add Progress
7. Section V: Market Update
8. Section VI: Distributions
9. Section VII: Portfolio Attribution (portfolio mode)
10. Section VIII: NAV Methodology
11. Section IX: Distribution Reconciliation
12. Section X: Outlook & Priorities
13. Appendix A: Returns Education (optional)

## Red Flags & Failure Modes

- **Hiding bad news in positive framing**: if an asset underperformed by 12%, state it directly. "Asset E experienced a 12% NOI shortfall driven by unexpected vacancy. Here is our remediation plan." Never bury it in a footnote.
- **Vague variance explanations**: "Expenses were higher than expected" is not an explanation. "Insurance renewed at +18% due to CAT market hardening, contributing $45K to the $62K total variance" is.
- **Missing distribution explanation**: if distributions are below projection, explain why before explaining what is being done about it. LPs tolerate variance; they do not tolerate surprises without context.
- **NAV without methodology**: never present a NAV number without disclosing the cap rate and valuation approach. LPs will (correctly) dismiss unsupported NAV claims.
- **Boilerplate market commentary**: "The multifamily market remains strong" is useless. Cite specific submarket data: vacancy rate, rent growth, new supply numbers.
- **Inconsistent quarterly formatting**: use the same section structure every quarter so LPs can compare periods easily.

## Chain Notes

- **Upstream**: lease-up-war-room (lease-up progress feeds operations and value-add sections). market-cycle-positioner (market context for outlook). property-performance-dashboard (financial data feeds all sections).
- **Downstream**: capital-raise-machine (quarterly updates maintain LP confidence during raises). Annual report aggregation (future skill).
- **Lateral**: capital-raise-machine (shared LP communication tone and format conventions).
