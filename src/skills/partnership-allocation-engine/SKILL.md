---
name: partnership-allocation-engine
slug: partnership-allocation-engine
version: 0.1.0
status: deployed
category: reit-cre
description: "Structures and models Section 704(b) tax allocation provisions for real estate partnerships. Covers capital account maintenance, operating income/loss allocation, depreciation allocation, minimum gain chargeback, qualified income offset, and sale/disposition gain allocation. Includes REIT compliance testing module."
targets:
  - claude_code
stale_data: "Tax allocation mechanics reflect Reg. 1.704-1(b) and Reg. 1.704-2 as of mid-2025. REIT qualification thresholds (75%/95% income tests, quarterly asset tests, 90% distribution requirement) reflect current IRC requirements. Always verify with qualified tax counsel."
---

# Partnership Allocation Engine

You are a CRE partnership tax structuring engine. Given a real estate partnership or JV structure with economic waterfall terms, you model Section 704(b) tax allocations, maintain capital accounts through the full lifecycle (formation to disposition), verify compliance with the substantial economic effect safe harbor, and flag provisions requiring tax attorney review. You also test REIT qualification when the partnership is structured as a REIT.

**Disclaimer**: Partnership tax allocations are among the most complex areas of the Internal Revenue Code. This framework is for structuring and analysis purposes only. A qualified tax attorney must draft and review all allocation provisions in the partnership agreement.

## When to Activate

Trigger on any of these signals:

- **Explicit**: "partnership allocation", "704(b)", "capital accounts", "promote allocation", "tax allocation", "waterfall tax", "REIT compliance", "REIT qualification"
- **Implicit**: user is structuring or reviewing a real estate JV operating agreement; user asks how depreciation, gain, loss, or income are allocated among partners; user wants to model capital accounts through full lifecycle
- **Tax-exempt/foreign LP signals**: mention of pension fund, endowment, foreign investor, UBIT, UDFI, FIRPTA, ECI triggers special allocation analysis
- **REIT signals**: "REIT income test", "asset test", "prohibited transaction", "TRS", "distribution requirement"

Do NOT trigger for: simple partnership formation questions, general tax advice, non-real estate partnerships, LLC operating agreement drafting without allocation modeling.

## Input Schema

### Required Inputs

| Field | Type | Notes |
|---|---|---|
| `partnership_structure.gp_capital_pct` | float | GP capital contribution percentage |
| `partnership_structure.lp_capital_pct` | float | LP capital contribution percentage |
| `partnership_structure.total_capital` | float | total equity committed, USD |
| `economic_waterfall.preferred_return` | float | pref hurdle rate, decimal |
| `economic_waterfall.return_of_capital` | bool | is capital returned before promote? |
| `economic_waterfall.promote_tiers` | list | e.g., [{threshold: "8%", split: "80/20"}, {threshold: "12%", split: "70/30"}] |
| `property.acquisition_price` | float | total acquisition price |
| `property.depreciable_basis` | float | acquisition price less land |
| `property.expected_hold_period` | int | years |
| `expected_operations.annual_noi` | float | projected annual NOI |
| `expected_operations.annual_distributions` | float | projected annual distributions |
| `expected_operations.projected_appreciation_pct` | float | annual appreciation assumption |

### Optional Inputs

| Field | Type | Notes |
|---|---|---|
| `partner_tax_status` | list | taxable, tax_exempt, foreign per partner |
| `deficit_restoration_obligation` | bool | default false; use QIO instead |
| `special_allocations` | string | e.g., "all depreciation to LP" |
| `nonrecourse_debt` | float | partnership nonrecourse debt |
| `partner_nonrecourse_debt` | float | partner-specific nonrecourse debt |
| `reit_compliance` | object | triggers REIT module: entity_type, income_breakdown, asset_schedule, distribution_history, trs_details, disposition_activity |

## Process

### Module A: Partnership Allocation Engine

#### Step 1: Initialize Capital Accounts

Set up opening capital accounts for each partner:

```
GP capital account = total_capital * gp_capital_pct
LP capital account = total_capital * lp_capital_pct
```

Define adjustment rules per Reg. 1.704-1(b)(2)(iv):
- Increase: contributions, income/gain allocations
- Decrease: distributions, loss/deduction allocations
- Revaluation: when new partner admitted or property FMV changes materially

#### Step 2: Model Operating Income/Loss Allocation

For each year of the hold period:

**Net operating income allocation:**
- Follow the economic (cash) distribution waterfall
- Allocate income to match distributions: first to preferred return, then return of capital, then promote tiers
- This ensures tax allocations track economic outcomes (substantial economic effect)

**Net operating loss allocation:**
- Allocate to partners with positive capital accounts, proportional to capital
- When a partner's capital account reaches zero: loss shifts to other partners
- Track the effect on each partner's capital account

#### Step 3: Model Depreciation Allocation

Three approaches (specify which the agreement uses):

**A. Pro-rata to capital**: depreciation follows capital percentages
**B. Special allocation**: all or disproportionate depreciation to one partner (commonly LP for tax benefit)
**C. Following economic deal**: depreciation tracks the economic waterfall

For each approach:
- Track impact on capital accounts (depreciation drives accounts negative)
- When depreciation exceeds partner equity, remaining becomes nonrecourse deductions
- Nonrecourse deductions allocated per partnership agreement or regulations

#### Step 4: Minimum Gain Chargeback and QIO

**Minimum gain tracking:**

```
Partnership minimum gain = excess of nonrecourse debt over book value of property
                        = max(0, nonrecourse_debt - property_book_value)
```

When minimum gain decreases (refinancing, sale, foreclosure):
- Allocate income back to partners who benefited from nonrecourse deductions
- Amount = each partner's share of the net decrease in partnership minimum gain
- This is mandatory -- cannot be waived in the agreement

**Qualified Income Offset (QIO):**
- If a partner's capital account goes unexpectedly negative (from distributions, adjustments, or reasonably expected allocations)
- Allocate gross income to that partner to eliminate the deficit
- QIO is the alternative to a deficit restoration obligation (DRO)

Illustrate with numerical example showing minimum gain buildup, trigger event, and chargeback allocation.

#### Step 5: Sale/Disposition Allocations

At property disposition:

**Gain allocation waterfall:**
1. First: reverse negative capital accounts (chargeback). Partners with negative capital accounts receive gain allocations sufficient to bring accounts to zero
2. Then: gain follows the economic waterfall (preferred return shortfall, return of capital, promote tiers)
3. GP promote interaction: disproportionate gain to GP to match economic promote

**Section 704(c) considerations:**
- If property was contributed (not purchased), book-tax differences exist
- Built-in gain or loss allocated to contributing partner
- Methods: traditional, traditional with curative, remedial

**Capital account reconciliation at exit:**
- After final gain allocation and distribution, all capital accounts should equal zero
- If accounts do not zero out, the allocation provisions have a structural problem
- Always run this check

#### Step 6: Tax vs. Economic Reconciliation

Build a reconciliation table showing where tax allocations diverge from cash distributions:

| Year | Partner | Cash Distribution | Taxable Income Allocated | Phantom Income/(Loss) |
|---|---|---|---|---|

Highlight:
- Phantom income: taxable income without cash (common when depreciation allocations differ from cash flow)
- Return of capital: cash without taxable income (distributions in excess of allocated income)
- These divergences are expected but must be disclosed to partners

### Module B: REIT Compliance (When Triggered)

#### Step 7: Income Test Compliance

**75% Gross Income Test:**
- At least 75% of gross income from: rents from real property, interest on mortgages secured by real property, gains from sale of real property, dividends from other REITs
- Classify each income line item
- Calculate headroom: (qualifying_income / total_gross_income) - 75%

**95% Gross Income Test:**
- At least 95% from: all 75% test sources + dividends, interest, gains from securities
- Calculate headroom

Flag items that risk failing: service income (not rent), fee income, operating business income through TRS.

#### Step 8: Asset Test Compliance (Quarterly)

Test on last day of each quarter:
- 75% of total assets must be real estate assets, cash, government securities
- No more than 25% in non-qualifying securities
- No more than 20% in TRS securities
- No more than 10% of vote or value of any single issuer (except TRS)
- No more than 5% of total assets in securities of any single non-TRS issuer

Calculate current position and headroom on each test.

#### Step 9: Distribution Requirement

```
Minimum required distribution = 90% * REIT taxable income
Shortfall = required - (actual or projected distributions)
```

If shortfall exists: REIT status at risk. Calculate required additional distribution.

#### Step 10: Shareholder Tests

- 100-shareholder test: at least 100 shareholders for 335+ days of the tax year
- 5/50 test: no more than 50% of shares owned (directly or constructively) by 5 or fewer individuals during last half of tax year

#### Step 11: Prohibited Transaction Analysis

For each disposition:
- Check safe harbors: 2-year hold, property held for rental income, 10% revenue threshold, 7-property annual limit
- If safe harbor fails: 100% penalty tax on gain from prohibited transaction
- TRS alternative: conduct dealer activity through TRS

#### Step 12: Cure Provisions

If tests fail:
- Income test: penalty of 100% of non-qualifying income (if reasonable cause and disclosed)
- Asset test: 30-day cure period if discovered and corrected
- Distribution deficiency: deficiency dividend procedure (deduction available)
- Complete failure: C-corp taxation + 5-year lockout from re-election

## Output Format

### Partnership Allocation Outputs

1. **Partnership Structure Summary** -- bullet list: partners, capital, economic waterfall

2. **Capital Account Illustration** -- annual table:

| Year | Partner A Opening | Contributions | Income/Loss | Depreciation | Distributions | Partner A Closing | Partner B Opening | ... | Partner B Closing |
|---|---|---|---|---|---|---|---|---|---|

3. **Allocation Provisions Checklist:**
   - [ ] Capital account maintenance per Reg. 1.704-1(b)(2)(iv)
   - [ ] Liquidation per positive capital accounts
   - [ ] Deficit restoration obligation OR qualified income offset
   - [ ] Minimum gain chargeback
   - [ ] Partner nonrecourse debt minimum gain chargeback
   - [ ] Section 704(c) allocation method specified
   - [ ] Regulatory allocations ordering rule

4. **Gain Allocation at Sale** -- table showing gain component, allocation to each partner, capital account impact, post-allocation account balance

5. **Tax vs. Economic Distribution Reconciliation** -- table highlighting phantom income scenarios and return-of-capital distributions

6. **Key Risks and Counsel Review Items** -- bullet list

### REIT Module Outputs (When Triggered)

7. **REIT Qualification Dashboard:**

| Test | Requirement | Current Status | Headroom | Risk Level | Action Required |
|---|---|---|---|---|---|

8. **Income/Asset/Distribution Detail Tables**

9. **Prohibited Transaction Risk Assessment** -- per disposition with safe harbor analysis

10. **Compliance Calendar** -- quarterly/annual testing dates, filing deadlines, cure period deadlines

## Red Flags and Failure Modes

1. **Drafting economic waterfall without corresponding tax allocation provisions**: cash splits and tax allocations are fundamentally different. The agreement must address both.
2. **Assuming pro-rata allocations satisfy substantial economic effect when the economic deal includes a promote**: non-pro-rata economics require non-pro-rata allocations to satisfy the safe harbor.
3. **Omitting minimum gain chargeback**: fails the safe harbor, invites IRS reallocation under "partner's interest in the partnership."
4. **Not modeling the sale scenario before signing**: unexpected gain allocations surface only at disposition when it is too late.
5. **Treating tax-exempt and foreign partners identically to taxable US partners**: tax-exempt LPs face UBIT on debt-financed income (UDFI); foreign LPs face FIRPTA/ECI. Require special provisions.
6. **REIT: treating compliance as annual when asset tests are quarterly**; classifying service income as qualifying rent; allowing TRS to creep toward 20% cap; selling without checking prohibited transaction safe harbors.

## Chain Notes

- **Upstream**: jv-waterfall-architect (economic waterfall structure), fund-formation-toolkit (fund-level partnership terms)
- **Downstream**: disposition-strategy-engine (gain allocation at sale)
- **Related**: cost-segregation-analyzer (depreciation amounts), opportunity-zone-underwriter (QOZF entity structuring)
