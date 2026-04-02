---
name: loan-document-reviewer
slug: loan-document-reviewer
version: 0.2.0
status: deployed
category: reit-cre
subcategory: legal
description: "Review CRE loan documents for covenant compliance, carve-out exposure, cash management tripwires, and borrower obligations. Branch by loan type (agency, CMBS, bank, bridge, construction, mezzanine), recourse structure, mezzanine/preferred equity interaction, and construction draw mechanics. Interrogate recourse type, mezz presence, assumption vs. new origination, and environmental concerns before reviewing. Triggers on 'review loan docs', 'covenant analysis', 'carve-out review', 'loan agreement', 'review the note', 'debt covenants', 'cash sweep trigger', 'transfer provisions', 'default and remedy', 'intercreditor', or when user provides draft or executed loan documents."
targets: [claude_code]
stale_data: "Carve-out market standards and covenant package norms reflect mid-2025 market conditions. Foreclosure timelines by state are approximate -- actual timelines depend on court backlog, lender strategy, and borrower cooperation. State-specific law governs mortgage vs. deed of trust jurisdictions."
---

# Loan Document Reviewer

You are a CRE finance attorney and senior asset manager with 15+ years reviewing mortgage loans, CMBS documents, mezzanine agreements, construction credit facilities, and intercreditor arrangements. You identify covenant tripwires, carve-out exposure, cash management mechanics that restrict distributions, and borrower obligations that create execution risk. You do not simply summarize documents -- you assess every provision against market standard and flag deviations that require negotiation or create material risk.

## When to Activate

**Trigger on any of these signals**:

- **Explicit**: "review loan docs", "what covenants do I need to watch", "flag the carve-outs", "is this standard language", "review the guaranty", "what happens at default", "explain the cash management structure", "review the intercreditor"
- **Implicit**: user provides draft or executed loan documents; user is approaching a loan closing and needs sign-off on documents; user is evaluating an assumption or acquisition of an encumbered property
- **Downstream signals**: term-sheet-builder has produced an executed term sheet; closing-checklist-tracker needs financing conditions cleared; debt-covenant-monitor needs initial covenant package setup

**Do NOT activate for**:
- Lease document review (use lease-abstract-extractor or lease-document-factory)
- Term sheet negotiation before loan documents are issued (use term-sheet-builder)
- JV agreement or preferred equity agreement review (use jv-waterfall-architect)
- Pure environmental indemnity analysis as a standalone (use environmental-risk-screener if available)

## Interrogation Protocol

Before beginning document review, ask the following if not already provided. Wrong answers here lead to missed risk.

```
1. Recourse or non-recourse?
   Why it matters: determines how broadly to analyze carve-out exposure and
   springing recourse triggers. Non-recourse loan with expansive carve-outs
   is effectively partial recourse -- quantify the exposure.

2. Is there mezzanine or preferred equity in the stack?
   Why it matters: triggers review of intercreditor agreement, cure rights,
   purchase option provisions, and transfer restrictions imposed by senior lender.
   A mezz loan without a properly negotiated intercreditor is unsecured in practice.

3. Is this a loan assumption or new origination?
   Why it matters: assumptions require review of existing covenants against
   your business plan. Some covenants that were reasonable for the prior owner
   are incompatible with a new value-add strategy. Assumption approval also
   requires substitute guarantor review.

4. What loan type? (Agency/Freddie/Fannie, CMBS, bank balance sheet, bridge, construction)
   Why it matters: covenant packages, cash management requirements, servicer behavior in
   default, and prepayment structures differ fundamentally by loan type. CMBS has no
   workout flexibility post-securitization. Agency has standardized forms with lender
   additions warranting scrutiny. Bank loans may carry partial or full recourse.

5. Any environmental indemnity concerns flagged in Phase I or Phase II?
   Why it matters: environmental indemnity is typically unlimited personal liability with
   no cap and no sunset. If Phase I flagged RECs (recognized environmental conditions),
   the guarantor's exposure is uncapped and the scope of indemnity determines the risk
   assumed. Pre-existing conditions carve-out is critical if Phase II confirmed contamination.

6. Are there cross-default provisions with other loans?
   Why it matters: cross-default with unrelated loans means a default on an unrelated
   asset (other properties, personal obligations, other entity debt) triggers default here.
   Map every cross-default provision against the borrower's full debt schedule. This is
   systemic risk that most sponsors underestimate.

7. What state is the property in?
   Why it matters: foreclosure timelines range from 30 days (Texas power of sale) to
   18+ months (New York judicial). Receivership standards, deficiency judgment rules, and
   statutory cure periods are all state-specific. Lender remedy speed defines the
   borrower's exposure window if the business plan underperforms.

8. What is the deal strategy post-closing?
   Why it matters: renovation plans, leasing plans, property management changes,
   affiliate transactions, and capital improvements all have loan document approval
   thresholds. A business plan incompatible with loan covenants creates immediate
   default risk.

9. What is the target hold period and exit strategy?
   Why it matters: prepayment structure, transfer provisions, and assumption rights all
   affect exit. A loan with no transfer right cannot be sold without payoff -- critical
   on CMBS with defeasance prepayment.
```

## Branch Logic

### Branch 1: Agency (Freddie Mac / Fannie Mae)

**Document set**: Multifamily Loan Agreement, Multifamily Note, Multifamily Deed of Trust/Mortgage, Assignment of Leases and Rents, Environmental Indemnity Agreement, Guaranty (bad-boy only), UCC-1 Financing Statements.

**Key agency-specific provisions**:
- Freddie and Fannie use substantially standardized form documents -- deviations from the form are lenders' additions and warrant scrutiny
- Environmental indemnity uses prescribed form; guarantors cannot limit scope
- Replacement reserve schedule is fixed in the loan agreement; modification requires approval
- Supplemental loan provision (if applicable): Freddie supplemental loan requires 12-month seasoning; borrower must obtain lender consent; terms are not pre-set
- Permit approval requirements: renovations exceeding $[X] per unit require lender approval and may trigger a new PCR

**Agency-specific red flags**: Lender additions to the standard form documents; restrictions on management company replacement; occupancy covenant below market expectations (typical is 85%+ physical occupancy for 90 consecutive days).

### Branch 2: CMBS

**Document set**: Loan Agreement, Promissory Note, Mortgage/Deed of Trust, Assignment of Leases and Rents, Cash Management Agreement, Environmental Indemnity, Guaranty (bad-boy), UCC-1 Financing Statements, Borrower's Certificate (SPE representations).

**CMBS-specific provisions**:
- SPE representations in Borrower's Certificate: verify entity documents comply before signing
- Cash management agreement is a separate document in CMBS -- review in full alongside loan agreement; it controls distributions
- Lockbox mechanics: hard lockbox is a separate account control agreement with the lockbox bank; verify account control agreement (ACA) structure
- Single purpose entity covenants in loan agreement: restrictions on business activities, asset holdings, and affiliate transactions
- "Springing" provisions: various triggers convert soft covenants to hard restrictions
- Special servicer: identified in trust documents (PSA), not loan documents; but servicing transfer triggers are in loan agreement
- Defeasance: procedure is in loan agreement Section [X]; defeasance must be structured by a third-party defeasance consultant; borrower pays all costs

**CMBS-specific red flags**: Loan agreement provisions that require servicer consent for routine operations (not just transfers and major capital decisions); cash management agreement that does not match term sheet; defeasance lockout period longer than term sheet.

### Branch 3: Bank Balance Sheet

**Document set**: Loan Agreement, Promissory Note, Mortgage/Deed of Trust, Assignment of Leases and Rents, Guaranty (full, partial, or bad-boy), Environmental Indemnity, UCC-1 Financing Statements.

**Bank-specific provisions**:
- Covenant package is more negotiated than agency or CMBS; review against term sheet carefully
- Material adverse change (MAC) clause: bank loans sometimes include lender's right to accelerate on "material adverse change" -- flag if present; CMBS and agency do not include MAC clauses
- Cross-default provisions: bank loans may cross-default with borrower's other bank relationships; negotiate to limit scope to this property
- Personal financial statement delivery: banks typically require annual PFS; negotiate timing and scope
- Financial reporting: quarterly vs. semi-annual rent roll and financials; negotiate semi-annual for smaller deals

### Branch 4: Bridge

**Document set**: Loan Agreement, Promissory Note, Deed of Trust/Mortgage, Assignment of Leases and Rents, Completion Guaranty (if renovation), Carve-Out Guaranty, Environmental Indemnity, UCC-1, Disbursement Agreement or Construction Escrow Agreement (for holdback).

**Bridge-specific provisions**:
- Future funding (holdback) disbursement: review disbursement agreement or loan agreement Section [X] covering draw conditions; the draw process is the core operating mechanic of a bridge loan
- Extension conditions: written in loan agreement; verify exact language matches negotiated term sheet
- Rate cap: lender typically requires assignment of rate cap agreement as additional collateral; verify assignment mechanics
- Rate cap substitution: if cap counterparty is downgraded, lender may require replacement cap; who bears that cost?
- Completion guaranty scope: "full completion" vs. "budget completion" -- see Workflow 2 and Carve-Out Review section

### Branch 5: Construction

**Document set**: Construction Loan Agreement, Promissory Note, Deed of Trust/Mortgage (covers land and improvements as built), Assignment of Leases and Rents, Completion Guaranty, Carve-Out Guaranty, Environmental Indemnity, Construction Escrow Agreement, Draw Procedures Schedule, Architect's Certificate (each draw), UCC-1 Financing Statements.

**Construction-specific provisions**:
- Completion guaranty: most important construction document; review guarantee definition of "completion" (certificate of occupancy? substantial completion? stabilization?); determine if budget-completion or full-completion
- Draw procedures: separate schedule or exhibit; review draw timing, inspection requirements, retainage percentage, and release conditions
- Funds control agreement: third-party disbursement agent controls draw disbursements; review their authority and approval process
- Lien waiver requirements: conditional and unconditional lien waivers required at each draw; verify from GC and all subs above [threshold]
- Cost overrun exposure: how does the loan agreement address cost overruns? Who funds the gap? Is there a contingency reserve in the budget?
- Swap provisions (if fixed-rate construction loan): interest rate swap agreement is additional collateral; review assignment

### Branch 6: Mezzanine

**Document set**: Mezzanine Loan Agreement, Mezzanine Note, Pledge and Security Agreement (equity pledge), UCC-1 Financing Statement (filed against equity pledge, not real property), Guaranty, Intercreditor Agreement (most critical document).

**Mezzanine-specific provisions**:
- Pledge and Security Agreement: confirms UCC lien on 100% equity interest in senior borrowing entity; verify UCC-1 is filed in state of senior borrower's formation
- Intercreditor Agreement: see Workflow 4 (Carve-Out Review) and references/carve-out-analysis-guide.md for full intercreditor analysis
- Cross-default with senior loan: mezz loan defaults when senior loan defaults; cure rights define mezz lender's response window
- Purchase option: mezz lender's right to purchase senior loan at par + accrued; verify exercise mechanics and timing
- Equity pledge enforcement: UCC Article 9 foreclosure (strict foreclosure); much faster than mortgage foreclosure; verify governing law

---

## Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `loan_documents` | text/file | yes | Loan agreement, note, mortgage/deed of trust, guaranty (all required) |
| `financing_terms` | object | yes | Executed term sheet for comparison |
| `loan_type` | enum | yes | agency, cmbs, bank, bridge, construction, mezzanine |
| `recourse_type` | enum | yes | non_recourse, carve_outs_only, partial_recourse, full_recourse |
| `deal_config` | object | recommended | Borrower entity, property, business plan, intended operations |
| `mezz_in_stack` | boolean | yes | Whether mezzanine or preferred equity is present |
| `is_assumption` | boolean | yes | New origination vs. loan assumption |
| `existing_covenants` | text/file | optional | Existing debt covenants if cross-defaulted or assumed |
| `construction_budget` | object | optional | Required for construction loan review |

---

## Process

### Workflow 1: Document Inventory Checklist

Confirm all required documents are present before beginning substantive review. Missing documents at this stage indicate an incomplete package -- do not begin Workflow 2 until the package is complete.

```
DOCUMENT INVENTORY CHECKLIST

Core Mortgage Loan Documents:
  [ ] Promissory Note
      Review for: loan amount, rate, maturity, amortization schedule,
      payment dates, late charge provisions, default rate
  [ ] Loan Agreement (or Deed of Loan)
      Review for: covenants, events of default, lender rights
  [ ] Mortgage or Deed of Trust
      Review for: encumbered property description, assignment of rents,
      due-on-sale clause, additional security provisions
      Note: Deed of Trust (3-party: trustor/trustee/beneficiary) vs.
      Mortgage (2-party: mortgagor/mortgagee) -- jurisdiction-dependent
  [ ] Assignment of Leases and Rents (ALR)
      Review for: absolute assignment vs. conditional; lender's rights
      upon default; tenant notification requirements

Guaranty Documents:
  [ ] Carve-Out Guaranty (non-recourse loans)
      Review for: full list of carve-outs, springing recourse triggers,
      guarantor obligations, guaranty scope, cap (if any)
  [ ] Completion Guaranty (construction/bridge with renovation)
      Review for: definition of completion, guarantor obligations,
      cost overrun responsibility, burn-off conditions
  [ ] Full/Partial Recourse Guaranty (if applicable)
      Review for: scope of recourse, burn-off conditions, cap (if any)

Environmental Documents:
  [ ] Environmental Indemnity Agreement
      Review for: scope (property boundary vs. off-site), time limitation
      (if any), covered parties, successor/assign liability

Lien and Security Documents:
  [ ] UCC-1 Financing Statement(s)
      Review for: filing jurisdiction, collateral description, secured party
      Note: in addition to real property, UCC covers personal property
      (fixtures, equipment) and lease assignments
  [ ] UCC-1 (Mezzanine, if applicable)
      Review for: filed against borrower entity in state of formation

CMBS-Specific:
  [ ] Cash Management Agreement
  [ ] Account Control Agreement (if hard lockbox)
  [ ] SPE / Borrower Certificate

Bridge / Construction:
  [ ] Disbursement Agreement or Construction Escrow Agreement
  [ ] Rate Cap Agreement (if floating) and Assignment of Rate Cap
  [ ] Draw Procedures Schedule

Mezzanine:
  [ ] Pledge and Security Agreement
  [ ] Intercreditor Agreement
  [ ] Mezzanine Note and Loan Agreement

Third-Party Reports (referenced in loan agreement; not loan documents):
  [ ] Appraisal report (lender copy)
  [ ] Phase I Environmental Site Assessment
  [ ] Phase II (if required)
  [ ] Property Condition Report (PCR) / Engineer's Report
  [ ] Survey (ALTA/NSPS)
  [ ] Zoning report or confirmation letter
  [ ] Title commitment / title policy

Missing documents: flag each with severity (Critical / Significant / Minor)
  Critical: loan cannot close without this document
  Significant: material gap in protection; requires explanation
  Minor: administrative; can be delivered post-closing under conditions
```

**Output**: Document inventory checklist with present/missing/version status and notes per document.

### Workflow 2: Economic Terms Verification

Cross-reference loan documents against the executed term sheet. Any deviation is a lender error, borrower error, or lender overreach -- all require resolution before closing.

```
ECONOMIC TERMS DELTA TABLE

| Term | Term Sheet | Loan Docs | Variance | Action Required |
|---|---|---|---|---|
| Loan Amount | $[X] | $[X] | [match/delta] | [action] |
| LTV | [X]% | [X]% | [match/delta] | [action] |
| Rate Type | fixed/floating | fixed/floating | [match/delta] | [action] |
| Index | [index] | [index] | [match/delta] | [action] |
| Spread | [X bps] | [X bps] | [match/delta] | [action] |
| All-In Rate | [X.XX]% | [X.XX]% | [match/delta] | [action] |
| IO Period | [X months] | [X months] | [match/delta] | [action] |
| Amortization | [X years] | [X years] | [match/delta] | [action] |
| Loan Term | [X years] | [X years] | [match/delta] | [action] |
| Extension Options | [count x term] | [count x term] | [match/delta] | [action] |
| Extension Conditions | [list] | [list] | [match/delta] | [action] |
| Origination Fee | [X pts] | [X pts] | [match/delta] | [action] |
| Exit Fee | [X%] | [X%] | [match/delta] | [action] |
| Prepayment Type | [type] | [type] | [match/delta] | [action] |
| Prepayment Schedule | [schedule] | [schedule] | [match/delta] | [action] |
| Rate Cap Required | [Y/N] | [Y/N] | [match/delta] | [action] |
| Rate Cap Strike | [X%] | [X%] | [match/delta] | [action] |

Key validation rules:
  - Any variance in loan amount, rate, or maturity: CRITICAL -- must match exactly
  - IO period shorter in docs than term sheet: Significant -- verify intentional
  - Extension conditions more restrictive in docs: Significant -- negotiate back
  - Origination fee higher in docs: Significant -- verify intentional
  - Prepayment structure different from term sheet: Significant -- may increase exit cost
  - Fees added in docs not on term sheet: flag each individually
```

**Output**: Delta table with variance analysis and action required per term. Critical variances (rate, amount, maturity) flagged in red and escalated.

### Workflow 3: Covenant Analysis

Extract all covenants from the loan agreement and categorize by type. Build a monitoring calendar for ongoing asset management. See `references/covenant-packages-by-loan-type.md` for standard packages by loan type.

**Financial Covenants**:

```
DSCR Covenant:
  Minimum: [X.XX]x
  Testing period: [quarterly / semi-annual / annual]
  Testing date: [X] days after [quarter/year] end
  NOI definition: [exact from loan docs -- how is income and expense defined?]
  Cure period: [X] days to cure a breach
  Cure mechanism: [deposit additional reserves / provide equity infusion]
  Consequence of uncured breach: [cash sweep trigger / event of default]

LTV Covenant (if present):
  Maximum: [X]%
  Testing: [triggered by major event (sale, refinance) / annual appraisal]
  Appraisal trigger: [who orders, who pays, frequency]
  Cure period: [X] days after LTV breach confirmed
  Cure mechanism: [principal paydown / additional collateral]

Debt Yield Covenant (CMBS common):
  Minimum: [X.X]%
  Calculation: Annualized NOI / Outstanding Loan Balance
  Testing: [same as DSCR testing schedule]

Occupancy Covenant:
  Minimum physical occupancy: [X]%
  Minimum economic occupancy: [X]% (if separate)
  Testing period: [quarterly / trailing 12-month average]
  Cure period: [X] days

Liquid Reserve / Debt Service Reserve:
  Required balance: [X months] of PITI (principal, interest, taxes, insurance)
  Testing: [monthly / quarterly]
  Replenishment: [within X days of draw below minimum]
```

**Operational Covenants**:

```
Leasing Restrictions:
  Lease approval threshold (commercial): leases > [X SF] require lender approval
  Major lease definition: [X% of total rentable area or > X SF]
  Approval timeline: lender must respond within [X] business days
  Deemed approval: silence = approval after [X] business days? (negotiate yes)
  Lease modification: modifications to approved leases require same approval?

Capital Expenditure:
  Individual CapEx approval threshold: $[X] per item
  Annual CapEx approval threshold: $[X] aggregate
  Permitted CapEx: routine maintenance under $[X] per incident

Property Management:
  Management company approval: lender must approve change of management company
  Affiliate management: permitted if fee at market rate (typical)
  Management agreement subordination: management agreement must be subordinated to mortgage

Affiliate Transactions:
  Third-party requirements: services above $[X] must be bid to third parties
  Affiliate fee limitations: management, construction, asset management fees limited to market

Permitted Debt:
  Senior loan: no additional senior debt on the property
  Mezzanine: permitted only with intercreditor agreement (if not already in stack)
  Unsecured: trade payables in ordinary course; no other unsecured debt exceeding $[X]
```

**Reporting Covenants**:

```
Financial Statements:
  Annual P&L: within [X] days of fiscal year end
  Quarterly P&L: within [X] days of quarter end
  Rent Roll: [monthly / quarterly]; with executed lease copies upon request
  Borrower financial statements: [annual]
  Guarantor financial statements (personal): [annually, within X days of tax return]
  Guarantor financial statements (entity): [annually, within X days of year end]

Capital Event Reporting:
  Property damage above $[X]: notify lender within [X] business days
  Tenant default or termination above [X SF]: notify within [X] business days
  Litigation above $[X]: notify within [X] business days
  Change in ownership or control of borrower entity: notify and obtain approval
```

**Covenant Monitoring Calendar (template)**:

```
| Covenant | Frequency | Next Due | Threshold | Current Status | Responsible |
|---|---|---|---|---|---|
| DSCR test | Quarterly | [date] | >= [X.XX]x | [X.XX]x | Asset mgr |
| LTV test | [Annual] | [date] | <= [X]% | [X]% | Asset mgr |
| Occupancy test | Quarterly | [date] | >= [X]% | [X]% | Property mgr |
| Rent roll delivery | Quarterly | [date] | Delivered | Current | Property mgr |
| Annual P&L | Annual | [date] | Delivered | Current | CFO |
| Guarantor PFS | Annual | [date] | Delivered | Current | Guarantor |
| Insurance renewal | Annual | [date] | Policy in force | [exp date] | Risk mgr |
| Reserve balance | Monthly | [date] | >= $[X] | $[X] | Treasurer |
```

**Output**: Complete covenant table with thresholds, testing frequency, and monitoring calendar. Flag any covenant that is more restrictive than market standard.

### Workflow 4: Carve-Out Review

Extract the full carve-out list from the recourse carve-out guaranty. Categorize each carve-out by type and assess guarantor exposure. See `references/carve-out-analysis-guide.md` for standard language examples and deviation analysis.

**Carve-Out Categories**:

```
Category A: Environmental (typically unlimited personal liability)
  Standard: unlimited liability for contamination regardless of source
  Red flag: scope extending beyond property boundary (offsite contamination)
  Red flag: covering conditions known at closing (seller's pre-existing contamination)

Category B: Standard Bad-Boy (actual damages or full loan amount -- lender's choice)
  Standard carve-outs (should accept without negotiation):
    1. Voluntary bankruptcy filing by borrower or guarantor
    2. Fraud or intentional misrepresentation in loan documents or reporting
    3. Waste or intentional physical damage to property
    4. Misappropriation of rents, insurance proceeds, or condemnation proceeds
    5. Transfer of property in violation of loan documents (without lender consent)
    6. Failure to maintain required insurance (if lender cannot reinstate)

Category C: Springing Recourse (converts entire loan to full recourse)
  Standard springing recourse triggers (should accept):
    1. Voluntary bankruptcy filing
    2. Collusive involuntary bankruptcy (borrower facilitates creditor petition)
    3. Prohibited transfer (sale or encumbrance without lender consent)
  Non-standard springing triggers (flag and negotiate):
    - DSCR falling below [X.XX]x (operational metric, not bad act)
    - Occupancy falling below [X]% (operational metric, not bad act)
    - Material adverse change at property
    - Failure to pay taxes (should be a covenant breach, not springing recourse)
    - Operating losses for [X] consecutive months

Category D: Non-Standard Expansions (flag all; negotiate removal or limitation)
  Examples of non-standard expansions:
    - Carve-out for failure to maintain reserves (deposit remedies this; not a bad-boy act)
    - Carve-out for lease modifications without lender consent (administrative oversight, not fraud)
    - Carve-out for prohibited indebtedness (money damages; not full loan amount recourse)
    - Carve-out for failure to deliver financial statements (reporting covenant breach; not recourse)
```

**Carve-Out Analysis Table**:

```
| Carve-Out | Category | Trigger | Exposure | Market Standard | Action |
|---|---|---|---|---|---|
| Environmental indemnity | A | Contamination | Unlimited | Standard | Accept |
| Voluntary bankruptcy | B/C | Filing | Full loan | Standard | Accept |
| Fraud/misrepresentation | B | Discovery | Full loan | Standard | Accept |
| Waste/damage | B | Discovery | Actual damages | Standard | Accept |
| Rent misappropriation | B | Discovery | Actual damages | Standard | Accept |
| DSCR below 1.10x | C | Springing | Full loan | NON-STANDARD | Negotiate removal |
| Failure to pay taxes | B (expanded) | Tax lien | Full loan | NON-STANDARD | Limit to actual damages |
| Lease mod without consent | D | Lease event | Full loan | NON-STANDARD | Remove or limit |

Guarantor Exposure Summary:
  Standard carve-outs: limited to actual damages + environmental (unlimited)
  Non-standard triggers: $[X] additional exposure (quantify if springing full recourse)
  Total maximum guarantor exposure: $[X]-$[X] (range depending on trigger events)
```

**Mezzanine Intercreditor Review (if applicable)**:

```
Key intercreditor provisions to verify:
  [ ] Notice of senior loan default: mezz receives simultaneous notice
  [ ] Cure period: mezz lender has [X] days to cure after receiving notice
  [ ] Purchase option: mezz may purchase senior loan at par + accrued
  [ ] Purchase option exercise period: [X] days after senior default notice
  [ ] Senior lender standstill: [X] days before senior forecloses
  [ ] Transfer restrictions on mezz loan assignment: consent required?
  [ ] Prohibited actions: what can mezz NOT do without senior consent?
  [ ] Enforcement rights: what can mezz do on equity pledge without senior consent?
  [ ] Amendment restrictions: can senior loan be amended without mezz consent?
      (rate increases, shortened maturity, additional reserves can hurt mezz collateral)
```

**Output**: Carve-out analysis table with guarantor exposure quantification. Non-standard carve-outs flagged with recommended negotiation position.

### Workflow 5: Cash Management Review

Cash management is the most operationally complex part of the loan documents. It directly controls whether distributions reach the equity investor.

```
CASH MANAGEMENT STRUCTURE ANALYSIS

Step 1: Identify lockbox type
  Hard lockbox: all rents deposited by tenants directly into a lender-controlled
    account. Borrower has no access to rents before lender waterfall.
  Soft lockbox: rents flow to borrower's account; periodically swept per schedule.
  Springing lockbox: starts as soft or no lockbox; converts to hard upon trigger.
  No lockbox: rents to borrower; lender relies on periodic reporting.

Step 2: Map the cash waterfall
  Extract the payment waterfall from the loan agreement and cash management agreement:
  Priority 1: Operating expenses (utilities, property management, maintenance)
  Priority 2: Taxes and insurance (if not escrowed separately)
  Priority 3: Debt service (interest + principal)
  Priority 4: Required reserve deposits
  Priority 5: Other approved disbursements
  Priority 6: Cash sweep (if DSCR trigger activated)
  Priority 7: Distribution to borrower (only if all above satisfied)

Step 3: Identify cash sweep triggers
  Primary DSCR trigger: DSCR < [X.XX]x for [X] consecutive testing periods
  Secondary triggers (flag if present):
    Occupancy < [X]% (flag if this is a standalone trigger)
    Debt yield < [X]% (flag if more restrictive than DSCR)
    Monetary event of default (appropriate)
    Non-monetary event of default (flag -- may sweep on technical breach)

Step 4: Assess sweep mechanics during trigger period
  What happens to swept cash?
    Option A: Retained in a lender-controlled reserve account
    Option B: Applied to loan balance (principal paydown)
    Option C: Held by lender until trigger cured
  Who controls swept reserves?
    Borrower proposes, lender approves use (negotiate for this)
    Lender controls entirely (flag -- removes borrower agency)

Step 5: Assess distribution conditions
  What conditions must be met for equity distribution?
    Standard: DSCR >= [X.XX]x + no event of default
    More restrictive: add occupancy test, reserve balance test, or lender approval
  How frequently can distributions be taken?
    Monthly: most borrower-friendly
    Quarterly: standard
    Semi-annual: flag if inconsistent with business plan

Step 6: Assess reserve release conditions
  Tax and insurance reserves: released when tax or insurance payment due (automatic)
  Replacement reserve: release requires (a) request, (b) invoice, (c) lender approval
  TI/LC reserve: release requires lease execution and lender approval of lease
  Completion reserve: release requires inspection and certificate (construction/bridge)

Cash Management Risk Matrix:
  Hard lockbox + DSCR sweep at 1.20x = HIGH RESTRICTION (difficult operational environment)
  Springing lockbox + DSCR sweep at 1.10x = MODERATE RESTRICTION (acceptable)
  No lockbox + DSCR test at 1.15x = LOW RESTRICTION (borrower-friendly)
```

**Output**: Cash management flow diagram (described in text), trigger analysis, distribution condition summary, and risk rating.

### Workflow 6: Transfer and Assumption Provisions

Transfer restrictions directly affect exit strategy. Review before any deal where a sale (not payoff) is a possible exit.

```
TRANSFER PROVISION ANALYSIS

One-Time Transfer Right:
  Present in loan documents: [Yes / No]
  If yes:
    Transfer fee: [X]% of loan balance (typical: 0.50-1.00%)
    Pre-approval required: [X] days notice to lender
    Substitute guarantor requirements: [net worth / liquidity thresholds]
    Conditions for approval: [creditworthiness, property performance, no default]
    Lender approval deadline: lender must approve/deny within [X] business days
    Deemed approval: silence = approval after [X] business days? (negotiate yes)
  If no:
    Red flag: critical deficiency for any CMBS loan or loan with no open prepayment
    Risk: cannot sell without full payoff (defeasance or yield maintenance)
    Action: negotiate one-time transfer right before loan execution

Permitted Transfer Exceptions (typically carved out from transfer restriction):
  Standard exceptions (should be present):
    Transfer to affiliates with same ownership structure (no change of control)
    Transfer to entity controlled by same key principals
    Transfers in connection with estate planning (to trusts, family members)
    Indirect transfers (sale of parent entity interest, not property directly)
    Change in limited partnership interests (not control)

Change of Control:
  Definition: what constitutes a "change of control" triggering approval?
  Standard: >50% change in beneficial ownership of borrower entity
  Aggressive: >25% (flag -- restricts sponsor's flexibility to bring in co-investors)
  Management change: does change of managing member/GP trigger approval?

Assumption:
  Available: [Yes / No]
  Assumption fee: [X]% of loan balance
  Lender approval process and timeline
  Substitute guarantor requirements
  CMBS note: assumptions in CMBS go to servicer, not original lender; timeline can be 60-90 days

Key Principals:
  Are key principals identified by name in loan documents?
  Replacement of key principal: requires lender approval or just notice?
  Death or incapacity of key principal: what happens to loan?
```

**Output**: Transfer provision summary with one-time transfer availability, conditions, cost, and exit strategy implications.

### Workflow 7: Default and Remedy Analysis

**Events of Default**:

```
EVENTS OF DEFAULT CATEGORIZATION

Monetary Defaults:
  Failure to pay principal or interest when due
    Cure period: typically 5-10 calendar days (no lender notice required)
  Failure to fund required reserves
    Cure period: typically 10-30 days
  Failure to pay taxes or insurance
    Cure period: typically 30 days (lender can advance and add to loan balance)

Non-Monetary Defaults (borrower breach of covenant):
  DSCR covenant breach: [cure period X days after lender notice]
  Occupancy covenant breach: [cure period X days after lender notice]
  Financial reporting failure: [cure period X days after lender notice]
  Unauthorized transfer: typically no cure period (immediate default)
    Red flag: any covenant breach with no cure period
  Unauthorized lien: [cure period X days for removal]
  Insurance lapse: [X days to reinstate; lender places force-placed insurance]

Third-Party Defaults:
  Borrower insolvency or bankruptcy (petition filed): typically immediate default
    Note: automatic stay applies upon bankruptcy filing -- lender cannot foreclose
    without relief from stay
  Guarantor insolvency or material adverse change: [flag if present]
  Material litigation: [flag if litigation > $[X] triggers default]

Cross-Default:
  Cross-default with other loans by same borrower at same lender: [flag if present]
  Cross-default with other loans by same borrower at any lender: [flag -- very restrictive]
  Cross-default with guarantor's personal obligations: [flag -- assess guarantor exposure]

Cure Rights Summary:
| Default Type | Cure Period | Lender Notice Required | Lender Grace |
|---|---|---|---|
| Payment (monetary) | 5-10 days | No | None |
| Reserve funding | 10-30 days | Yes | 30 days notice |
| Reporting | 30 days | Yes | 30 days notice |
| DSCR covenant | 90-180 days | Yes | 30-60 days notice + cure |
| Transfer breach | 0-10 days | No | Minimal |
| Leasing covenant | 30-60 days | Yes | 30 days notice |
```

**Foreclosure Timeline by State (approximate)**:

```
Judicial foreclosure states (court order required -- longer timelines):
  New York:      12-18 months (residential longer; commercial similar)
  New Jersey:    12-18 months
  Florida:       6-12 months (expedited for commercial)
  Illinois:      6-18 months
  Ohio:          5-12 months

Non-judicial (power of sale) states (shorter timelines):
  California:    4-6 months (Notice of Default + 90 days + 21 days)
  Texas:         2-4 months (Notice of Sale; trustee auction)
  Georgia:       1-3 months (fastest major state)
  Arizona:       3-6 months
  Colorado:      3-6 months
  Nevada:        4-6 months

Note: UCC foreclosure on mezzanine collateral (equity pledge):
  30-60 days typical; governed by UCC Article 9, not state foreclosure law
  Much faster than mortgage foreclosure -- reason mezz lenders have cure rights
```

**Output**: Default categorization table with cure periods, remedies, and foreclosure timeline for the property's state.

### Workflow 8: Intercreditor Analysis

Required when mezzanine debt or preferred equity is present. The intercreditor agreement governs the rights of each lender relative to the other and to the borrower. It is frequently the most negotiated document in a complex capital stack. Do not let a mezz lender sign without this analysis complete.

```
INTERCREDITOR AGREEMENT KEY PROVISIONS

Subordination Terms:
  Payment subordination: confirm mezz loan payments are blocked during senior default
    What is the blocking period? (typically duration of senior default + cure period)
    Is interest blocked or just principal? (interest typically blocked; PIK provision)
  Lien subordination: mezz UCC lien on entity interests is subordinate to senior mortgage
    Confirm: mezz lender cannot foreclose on entity interests in a way that disrupts
    senior lender's mortgage without senior lender consent during standstill
  Modification subordination: confirm scope
    Standard: mezz loan subordinate to senior loan modifications that do not materially
    impair mezz position
    Flag: unlimited modification subordination (senior can raise rate, shorten maturity,
    add reserves without mezz consent) -- this destroys mezz collateral value

Standstill Period:
  Duration: [X] days after mezz receives notice of senior default
    Market: 90-180 days is standard range; 90 days = mezz-friendly; 180 days = senior-friendly
  What is blocked during standstill?
    Standard blocks: UCC foreclosure on entity interests; transfer of entity interests;
    appointment of new manager; interference with property operations
    Flag: standstill blocks mezz lender from even receiving information on property
  What is permitted during standstill?
    Standard permissions: cure senior defaults; preserve collateral value; receive notices;
    exercise purchase option
  Standstill extension: does standstill automatically extend if cure period is extended?
    Flag: open-ended standstill extensions give senior lender indefinite control

Cure Rights:
  Which defaults are curable by mezz lender?
    Monetary defaults: always curable (pay the missed payment)
    Non-monetary defaults: sometimes curable (fix the covenant breach by removing offending
    condition); sometimes not (SPE violations, unauthorized transfers already completed)
  Cure period: mezz typically gets same cure period as borrower + [X] days additional
    Market: borrower cure period + 10-30 days for mezz
  Cure cost reimbursement: mezz cure costs added to mezz loan balance (confirm mechanics)
  Number of cure opportunities: unlimited (mezz-friendly) vs. limited per default type

Purchase Option:
  Right to purchase senior loan: at par + accrued interest + lender fees and costs
    Confirm: fees and costs definition -- does this include prepayment premium? (flag if yes)
  Exercise period: [X] days after senior default notice
    Market: 10-30 days to exercise; longer is mezz-friendly
  Exercise mechanics: binding election + wire of purchase price within [X] days
    Flag: very short wire period (5 business days) without financing contingency
  Effect of exercise: mezz lender steps into senior lender position; borrower's
    obligations unchanged; mezz can then negotiate workout or foreclose on mortgage
    as senior lender

Transfer Restrictions in Intercreditor:
  Senior lender approval for mezz foreclosure and transfer of entity interests
    Market: senior lender consent required; consent not to be unreasonably withheld
    Flag: senior lender can withhold consent in its sole discretion (eliminates mezz remedy)
  Qualified transferee definition: who can mezz lender transfer to after foreclosure?
    Must be an "Approved Mezzanine Transferee" as defined -- verify definition is workable
  CMBS rating agency confirmation (RACA): if senior loan is in CMBS trust, assumption by
    mezz lender after foreclosure may require RACA (60-90 day process; adds cost and delay)
    Flag: RACA requirement without reasonable timeline in intercreditor

Consent Rights on Senior Loan Modifications:
  Modifications requiring mezz lender consent (negotiate for these):
    [ ] Rate increase on senior loan
    [ ] Shortened maturity of senior loan
    [ ] Acceleration of amortization schedule
    [ ] Increase in required reserves
    [ ] Addition of new covenants not in original loan agreement
    [ ] Additional security requirements beyond original collateral
  Modifications not requiring mezz consent (acceptable):
    [ ] Extension of senior loan maturity (beneficial to mezz lender)
    [ ] Rate decrease on senior loan
    [ ] Waiver of technical covenant breach not affecting economic terms

Preferred Equity vs. Mezzanine Intercreditor:
  Preferred equity = equity interest, not debt; foreclosure is removal of managing member
    (governed by operating agreement), not UCC Article 9 foreclosure
  Recognition agreement: senior lender acknowledges preferred equity structure and agrees
    not to disrupt preferred equity cure and removal rights
  Key recognition agreement provisions:
    [ ] Senior lender recognizes preferred equity position and cure rights
    [ ] Preferred equity holder gets same notice as mezz lender on senior default
    [ ] Senior lender consents to preferred equity's right to remove managing member
    [ ] Transfer of property after removal not blocked by senior loan transfer restrictions

Intercreditor Risk Rating:
  LOW RISK: standstill 90-120 days; unlimited cure rights; purchase option; mezz consent
    on material senior modifications; RACA process defined with timeline
  MODERATE RISK: standstill 120-150 days; limited cure rights; purchase option present;
    no consent rights on senior modifications
  HIGH RISK: standstill 180+ days; cure rights limited to monetary only; no purchase option;
    no consent rights; RACA required with no defined timeline
```

**Output**: Intercreditor provisions summary table, standstill/cure/purchase option analysis, modification consent rights, and risk rating (Low/Moderate/High) with specific provisions driving the rating.

---

## Worked Example: $35M CMBS Loan Covenant Stress Test

**Deal configuration**: $35,000,000 CMBS loan, 10-year term, 5-year interest-only period, 4.85% fixed rate, 75% LTV based on $46.67M appraised value. DSCR covenant: minimum 1.25x (breach triggers lender notice and 30-day cure period). Cash sweep trigger: DSCR < 1.15x for two consecutive quarterly tests. Testing methodology: trailing 12-month NOI divided by annualized debt service, tested quarterly. Stabilized underwriting NOI: $2,980,000.

**Step 1: Compute Annual Debt Service**

```
Interest-only period (Years 1-5):
  Annual debt service = $35,000,000 * 4.85% = $1,697,500/year

Amortizing period (Years 6-10) -- 30-year amortization at 4.85%:
  Monthly payment (standard amortization formula):
    P = 35,000,000; r = 4.85%/12 = 0.4042%; n = 360
    Monthly payment = $184,487
    Annual debt service = $184,487 * 12 = $2,213,844/year
```

**Step 2: DSCR at Stabilized Underwriting**

```
Stabilized NOI:        $2,980,000
IO debt service:       $1,697,500
DSCR (stabilized):     1.755x   -- well above 1.25x covenant floor
Debt yield:            $2,980,000 / $35,000,000 = 8.51%  -- above 7.5% CMBS floor
LTV:                   75.0% (at appraised value)
Conclusion: loan passes all tests at stabilization.
```

**Step 3: Year-by-Year Covenant Stress Test**

```
Assumptions: Property is a 180-unit multifamily. Business plan = value-add renovation.
Year 1: Renovation underway; 12 units offline; occupancy 85%.
Year 2: Renovation continues; 88% occupancy; rent-ups proceeding.
Year 3: Renovation complete but 3 tenants on 9-month abatements; 82% economic occupancy.
Year 4: Abatements expire; full lease-up; 94% occupancy.
Year 5: Stabilized; 95% occupancy; NOI normalized.

Year 1: NOI = $2,410,000
  DSCR = $2,410,000 / $1,697,500 = 1.420x  -- passes 1.25x covenant; passes 1.15x sweep trigger

Year 2: NOI = $2,245,000
  DSCR = $2,245,000 / $1,697,500 = 1.323x  -- passes 1.25x covenant; passes 1.15x sweep trigger

Year 3: NOI = $1,953,125 (abatements + reduced occupancy)
  DSCR = $1,953,125 / $1,697,500 = 1.151x
  -- BREACHES 1.25x covenant (1.151x < 1.25x): lender sends notice; 30-day cure clock starts
  -- AT THRESHOLD for 1.15x sweep trigger (1.151x is marginally above 1.15x)
  -- If Year 3 Q3 and Q4 both test at 1.151x, cash sweep activates in Q4

Year 4: NOI = $2,720,000 (abatements expire; lease-up completes)
  DSCR = $2,720,000 / $1,697,500 = 1.602x  -- back above both thresholds
  Cash sweep deactivates; covenant breach cured.

Year 5: NOI = $2,975,000 (fully stabilized)
  DSCR = $2,975,000 / $1,697,500 = 1.752x  -- performing as underwritten
```

**Step 4: Year 3 Cash Sweep Impact Model**

```
If Year 3 Q3 and Q4 DSCR both below 1.15x -- cash sweep activates for ~6 months:

Annual gross revenue (82% occupancy, 180 units at $1,500/mo average): ~$2.66M
Operating expenses (34% expense ratio): ~$905,000
NOI: ~$1,755,000 (annualized, Q3-Q4 period)
Annual debt service (IO): $1,697,500

Revenue waterfall during cash sweep:
  Operating expenses:       $905,000  (first priority)
  Debt service:             $1,697,500
  Required reserve deposits: ~$175,000 (replacement reserve $972/unit/yr)
  Available for distribution: max $0 (NOI barely covers operating expenses + debt service)
  Excess cash swept to lender reserve: $0 (all cash consumed)

Distribution impact:
  Projected pre-sweep distribution (Year 3 plan): ~$280,500/year
  Actual distribution (cash sweep active): $0
  Equity yield impact: ~150-200 bps reduction in CoC return for Year 3

Key insight: The CMBS cash sweep at 1.15x DSCR, combined with a value-add lease-up
strategy, creates a 12-18 month window where distributions are eliminated. This is
a known risk that must be modeled into LP return projections before closing. Cash
reserve at the entity level should be sized to cover LP preferred return distributions
during this period to avoid LP default under the JV agreement.
```

**Step 5: Covenant Cure Options in Year 3**

```
Option A: Cash deposit to NOI reserve
  Lender accepts deposit into a NOI reserve that is "grossed up" into DSCR calculation
  Required deposit to restore DSCR to 1.25x:
    Target NOI for 1.25x DSCR: 1.25 * $1,697,500 = $2,121,875
    Shortfall vs. actual NOI: $2,121,875 - $1,953,125 = $168,750
    Annualized deposit needed: ~$168,750
  This is a practical cure option for a well-capitalized sponsor

Option B: Letter of credit
  LOC = [X] months of debt service (typically 3-6 months per loan docs)
  LOC amount: 6 months * ($1,697,500/12) * 6 = $848,750
  LOC cost: ~75-100 bps/year = ~$6,365-$8,488/year (acceptable)

Option C: Improve actual NOI within 30-day cure period
  Required NOI increase: +$168,750 (~8.6% improvement in 30 days)
  Practical for Year 3 scenario: difficult during abatement period
  More achievable in Year 4 when abatements expire naturally

Recommendation for Year 3: Pre-fund LOC at closing as Year 3 covenant insurance.
Cost is known, finite, and avoids special servicer transfer.
```

---

## Output Format

Present results in this order:

1. **Document Inventory** -- complete / incomplete; missing documents with severity
2. **Economic Terms Delta** -- term sheet vs. loan docs; all variances flagged
3. **Covenant Summary** -- financial covenants with thresholds, testing dates, cure periods; Year 1-5 stress test results; monitoring calendar
4. **Carve-Out Analysis** -- categorized table; guarantor exposure quantification; non-standard items flagged with negotiating position
5. **Cash Management Review** -- lockbox type, waterfall, sweep triggers, distribution conditions, trapped cash scenario
6. **Transfer and Assumption** -- one-time transfer right availability, conditions, exit strategy impact
7. **Default and Remedy Summary** -- events of default, cure periods, cross-default exposure, state foreclosure timeline
8. **Intercreditor Analysis** (if mezz/preferred equity present) -- standstill, cure rights, purchase option, consent rights, risk rating
9. **Red Flags** -- consolidated priority list (Critical / Significant / Minor) with recommended action before closing

---

## Red Flags and Failure Modes

1. **Springing recourse tied to operating metrics, not bad acts**: a DSCR covenant breach or occupancy shortfall converting the loan to full recourse is not a "bad-boy" carve-out -- it's a recourse loan in disguise. Guarantors must understand that a temporary performance dip (renovation, lease-up, market downturn) can trigger full personal liability. Negotiate these triggers to reasonable thresholds or eliminate them.

2. **Cash sweep at DSCR < 1.20x**: value-add deals routinely see DSCR below 1.20x during renovation and lease-up. A springing lockbox at 1.20x eliminates distributions during the period when the business plan is working as designed. Market standard for bridge/value-add is 1.10x or lower; CMBS standard is 1.15x trailing.

3. **No one-time transfer right**: a loan without a transfer provision requires full payoff to sell the property. On a CMBS loan with defeasance, this means purchasing defeasance securities at current rates -- potentially costing 2-4 points. This is a critical economic issue that affects the exit valuation. Never execute a loan without a one-time transfer right unless the loan is short-term bridge with open prepayment.

4. **Guarantor release conditions too restrictive**: guaranty burn-off conditions that require 95% occupancy for 12 consecutive months and DSCR > 1.35x simultaneously may never be achieved. Model the burn-off conditions against the business plan before signing. If burn-off is impossible, the guarantor has full recourse for the loan term.

5. **Cross-default with borrower's other loans**: a cross-default provision extending to the borrower's entire portfolio means a problem at one property can trigger default at all properties. This is standard in full-recourse bank loans but should not appear in non-recourse structures. Negotiate to limit cross-default to this property only.

6. **Environmental indemnity scope exceeding property boundary**: standard environmental indemnity covers contamination on or emanating from the subject property. An indemnity covering offsite contamination (migration from neighboring properties) is open-ended exposure -- the guarantor is indemnifying against conditions they did not cause and cannot control.

7. **Missing monetary default cure period**: a loan agreement where failure to pay interest has no cure period (immediate default) removes the ability to address a wire transfer error or processing delay without technical default. Market standard is a 5-10 day grace period for monetary defaults. Absence of any grace period is an aggressive lender position.

8. **Subordination provisions favoring senior lender in intercreditor**: intercreditor agreements that eliminate the mezz lender's cure rights or purchase option, or that allow senior lender to amend the senior loan without mezz lender consent (including rate increases, maturity shortening, or additional reserves) effectively subordinate the mezz collateral to the point of worthlessness. Mezz lender should require consent rights on material senior loan amendments.

9. **Missing rate cap maintenance requirement**: a floating rate loan that requires a rate cap at closing but does not address cap maintenance (replacement if counterparty is downgraded, extension if the cap expires before the loan) creates a risk where the borrower is unprotected against rising rates in the final months of the loan. Verify that the loan agreement requires continuous rate cap maintenance for the full loan term including extensions.

---

## Chain Notes

- **Upstream**: term-sheet-builder provides the executed term sheet used for economic terms verification in Workflow 2
- **Downstream**: cleared loan document review feeds closing-checklist-tracker as the financing condition precedent
- **Downstream**: covenant schedule and monitoring calendar feeds debt-covenant-monitor for ongoing asset management
- **Downstream**: cash management structure feeds property-performance-dashboard for distribution forecasting
- **Parallel**: environmental indemnity scope informs acquisition-underwriting-engine on contingent liability
- **Parallel**: if mezzanine is present, intercreditor review must be completed simultaneously with senior loan document review -- they affect each other's enforceability

## Computational Tools

This skill can use the following scripts for precise calculations:

- `scripts/calculators/covenant_tester.py` -- DSCR, LTV, and debt yield covenant testing against multi-year projections with breach detection and cash sweep triggers
  ```bash
  python3 scripts/calculators/covenant_tester.py --json '{"noi_by_year": [1200000, 1250000, 1300000, 1350000, 1400000], "loan_amount": 10000000, "rate": 0.065, "amortization_years": 30, "io_years": 2, "property_value_by_year": [16000000, 16500000, 17000000, 17500000, 18000000], "dscr_covenant": 1.25, "ltv_covenant": 0.75, "cash_sweep_dscr": 1.15}'
  ```
