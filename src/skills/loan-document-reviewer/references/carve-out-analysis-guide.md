# Carve-Out Analysis Guide

Standard vs. non-standard bad-boy carve-outs with language examples, exposure quantification methodology, and negotiation positions. Used in Workflow 4 of the loan-document-reviewer skill.

---

## Background: Carve-Out Structure

A non-recourse real estate loan protects the borrower (and guarantor) from personal liability if the loan defaults -- the lender's only remedy is foreclosure on the property. However, non-recourse loans always include "carve-outs" (also called "bad-boy guarantees" or "non-recourse carve-outs") that impose personal liability on the guarantor for specific events. These carve-outs fall into two types:

**Type 1: Actual damages carve-outs** -- guarantor is liable only for damages caused by the specific bad act.
**Type 2: Full recourse carve-outs** -- the occurrence of the event converts the entire loan to full recourse, regardless of causation.

The distinction matters enormously. A borrower misappropriating $50,000 in rents (Type 1: ~$50,000 guarantor liability) vs. triggering a full recourse conversion (Type 2: $[full loan amount] guarantor liability) are categorically different outcomes.

---

## Standard Carve-Outs (Accept Without Negotiation)

The following carve-outs represent the industry standard and are in every non-recourse loan. Guarantors should understand them but should not spend negotiating capital trying to remove them.

### 1. Environmental Indemnity (Unlimited Actual Damages)

**Standard language**:
> "Notwithstanding the non-recourse provisions of this Agreement, Guarantor shall be personally liable for all losses, costs, damages, and liabilities arising from or related to any Hazardous Materials present on, at, or emanating from the Property, including without limitation remediation costs, governmental fines and penalties, and third-party claims."

**Scope**: Property boundary (contamination on or migrating from the property).

**Exposure**: Unlimited; no cap. Environmental remediation costs can exceed the loan amount.

**Annotation**: Unlimited environmental carve-out is non-negotiable. Lenders will not close without it. Mitigate through Phase I/II due diligence before closing, not through guaranty negotiation. If Phase II reveals material contamination, negotiate indemnity scope to exclude known pre-existing conditions (seller indemnifies borrower for pre-closing conditions; borrower/guarantor covers post-closing).

### 2. Fraud or Intentional Misrepresentation (Full Loan Amount)

**Standard language**:
> "Guarantor shall be personally liable for the full outstanding principal balance and all accrued interest upon: (i) any fraud or intentional misrepresentation by Borrower, Guarantor, or any Key Principal in connection with the Loan, the Loan Documents, or the Property, including without limitation fraud in the loan application, financial statements, rent rolls, or operating histories."

**Scope**: Any intentional misrepresentation. Includes misrepresented rent rolls, fabricated financial statements, false representations in the loan application.

**Exposure**: Full outstanding loan amount + accrued interest.

**Annotation**: Non-negotiable. Guarantors should be focused on providing accurate information, not limiting this carve-out.

### 3. Waste or Intentional Physical Damage (Actual Damages)

**Standard language**:
> "Guarantor shall be personally liable for actual losses, costs, and expenses arising from any intentional waste, physical destruction, or removal of any material portion of the Property, or any failure to maintain the Property in a commercially reasonable manner that materially and adversely affects the value of the Property."

**Scope**: Intentional physical damage. Not ordinary wear and tear. Not deferred maintenance (although deferred maintenance that rises to the level of "failure to maintain" can be included).

**Exposure**: Actual repair/replacement costs; diminution in property value.

**Annotation**: Negotiate to limit "failure to maintain" to situations where the failure is intentional or constitutes gross negligence. Ordinary deferred maintenance during a value-add renovation should not trigger waste carve-outs.

### 4. Misappropriation of Rents, Insurance Proceeds, or Condemnation Awards (Actual Damages)

**Standard language**:
> "Guarantor shall be personally liable for actual damages arising from: (i) the misappropriation of any rents, security deposits, insurance proceeds, or condemnation awards that are required by the Loan Documents to be paid to Lender or deposited into any Reserve Account; or (ii) the failure to apply any such proceeds in accordance with the requirements of the Loan Documents."

**Scope**: Diverting rents or proceeds that should go to the lender or into reserves.

**Exposure**: Actual amount misappropriated.

**Annotation**: Standard and non-negotiable. Borrowers should have proper internal controls to ensure rents are applied per the loan agreement. Using rents for operating expenses when debt service is past due is the most common trigger of this carve-out.

### 5. Voluntary Bankruptcy Filing (Springing Full Recourse)

**Standard language**:
> "The limitation on personal liability of Guarantor shall not apply, and Guarantor shall be fully liable for the entire outstanding Indebtedness, if Borrower (i) files a voluntary petition in bankruptcy; (ii) makes a general assignment for the benefit of creditors; or (iii) is complicit in or facilitates a collusive involuntary petition."

**Scope**: Borrower entity filing voluntary bankruptcy. Does not include creditor-initiated involuntary bankruptcy.

**Exposure**: Full outstanding loan amount.

**Annotation**: Non-negotiable and appropriate. The automatic stay in bankruptcy prevents lender from foreclosing -- springing full recourse is the lender's offset to this risk. Guarantors should understand this means a borrower entity bankruptcy is effectively prohibited.

### 6. Transfer in Violation of Loan Documents (Springing Full Recourse)

**Standard language**:
> "Guarantor shall be personally liable for the full outstanding Indebtedness if Borrower sells, transfers, conveys, assigns, mortgages, pledges, or encumbers the Property or any direct or indirect interest in Borrower without the prior written consent of Lender as required by this Agreement."

**Scope**: Unauthorized transfer of the property or ownership interests.

**Exposure**: Full outstanding loan amount.

**Annotation**: Non-negotiable. Lenders have approval rights on transfers for security and underwriting reasons. However, negotiate that "permitted transfers" (affiliate transfers, estate planning transfers, minor indirect ownership changes) are explicitly carved out of this provision.

---

## Non-Standard Carve-Outs (Negotiate Removal or Limitation)

The following carve-outs appear with some frequency but are not market standard. Flag each and negotiate against acceptance.

### 7. Operating Loss or DSCR Trigger (Springing Full Recourse)

**Non-standard language**:
> "Guarantor shall be personally liable for the full outstanding Indebtedness if the Debt Service Coverage Ratio falls below [1.10x / 1.15x / 1.20x] for any [two / three / four] consecutive calendar quarters."

**Why it is non-standard**: DSCR falling below a threshold is an operational condition, not a bad act. A property undergoing renovation will routinely have DSCR below 1.0x -- that is by design. This provision converts a non-recourse loan to a full recourse loan whenever business plan execution is occurring. On a $20M loan, a routine DSCR dip during lease-up creates $20M of guarantor exposure.

**Negotiation position**:
- First preference: remove entirely. DSCR covenant should trigger cash management (sweep), not personal liability.
- Second preference: limit to actual damages caused by borrower's intentional actions that led to the DSCR decline (narrows it to a bad-act carve-out).
- Third preference: raise the trigger threshold to 0.85x or lower so it only applies in true distress.

**Negotiation script**:
> "Our business plan projects DSCR below 1.20x during the 12-month renovation and lease-up period. This is not a distress condition -- it is the value-creation phase. Converting a $[X]M loan to full recourse based on a routine, planned DSCR dip is not appropriate for a value-add deal. We request removal of this provision. Cash management (sweep) is the appropriate consequence for DSCR below covenant. Full recourse should be limited to bad-boy acts."

### 8. Failure to Pay Taxes (Full Loan Amount)

**Non-standard language**:
> "Guarantor shall be personally liable for the full outstanding Indebtedness if Borrower fails to pay any real property taxes when due, resulting in a tax lien being filed against the Property."

**Why it is non-standard**: Failure to pay taxes is a covenant breach, not a bad act. The appropriate consequence is: (1) lender pays the taxes, (2) borrower reimburses lender, (3) the advance accrues interest. Market standard does not impose full recourse for a tax payment failure.

**Negotiation position**: Remove. Replace with actual damages carve-out covering lender's costs to pay the taxes plus any penalty. Alternatively, propose a longer cure period (30 days) so a processing error doesn't immediately trigger the provision.

### 9. Failure to Maintain Insurance (Full Loan Amount or Actual Damages)

**Non-standard language (full recourse version)**:
> "Guarantor shall be personally liable for the full outstanding Indebtedness if Borrower fails to maintain property insurance as required by this Agreement."

**Why partial recourse version is more appropriate**: Insurance lapse is a covenant breach that creates real risk -- but full recourse is disproportionate unless the lapse led to actual damage. The standard remedy is: lender places force-placed insurance; borrower reimburses.

**Negotiation position**: Limit to actual damages (lender's cost to place force-placed insurance + any uninsured casualty loss). Remove full recourse trigger.

### 10. Lease Modification Without Lender Consent (Full Loan Amount)

**Non-standard language**:
> "Guarantor shall be personally liable for the full outstanding Indebtedness if Borrower modifies, amends, or terminates any Major Lease without the prior written consent of Lender."

**Why it is non-standard**: Lease modifications are operational decisions that should trigger an approval requirement (covenant breach), not full personal liability. A missed notification of a non-material lease amendment should not create $[X]M of guarantor exposure.

**Negotiation position**: Convert from springing full recourse to actual damages (value impact of the unauthorized modification). Alternatively, narrow "Major Lease" definition to raise the approval threshold.

### 11. Failure to Deliver Financial Reports (Any Recourse)

**Non-standard language**:
> "Guarantor shall be personally liable for actual damages arising from any failure to deliver financial reports within the time periods required by this Agreement."

**Why it is non-standard**: Financial reporting failures are administrative covenant breaches. There are no actual damages to the lender from a 30-day-late rent roll. This carve-out has no legitimate economic basis.

**Negotiation position**: Remove entirely. Reporting failures should be subject to cure periods and, if persistent, loan acceleration -- not personal liability.

### 12. Material Adverse Change at Borrower or Guarantor (Springing Full Recourse)

**Non-standard language**:
> "Guarantor shall be personally liable for the full outstanding Indebtedness if any Material Adverse Change occurs with respect to Borrower or any Guarantor."

**Why it is non-standard**: "Material adverse change" is undefined in most loan documents and gives the lender unilateral discretion to declare full recourse whenever the lender believes conditions have deteriorated. This is essentially a demand loan disguised as non-recourse.

**Negotiation position**: Remove entirely. If the lender insists on a MAC provision, negotiate an objective definition (e.g., guarantor net worth falls below $[X] or guarantor files bankruptcy). Vague MAC clauses are unacceptable.

---

## Intercreditor Agreement Analysis (Mezzanine Deals)

The intercreditor agreement governs the relationship between the senior lender and the mezz lender. It defines who has what rights when either loan is in default. The following provisions are the critical negotiation points.

### Intercreditor Provision 1: Notice of Senior Loan Default

**Adequate**:
> "Senior Lender shall provide simultaneous written notice to Mezzanine Lender of any Senior Loan Default at the same time and in the same manner as notice is provided to Borrower."

**Inadequate** (flag):
> "Senior Lender shall provide written notice to Mezzanine Lender of any Senior Loan Default within [10 / 15 / 30] days after Senior Lender provides notice to Borrower."

**Why it matters**: Mezz lender's cure period runs from notice. A 30-day delay in notice eats into the cure period. Simultaneous notice is the market standard.

### Intercreditor Provision 2: Cure Rights

**Adequate**:
> "Mezzanine Lender shall have the right, but not the obligation, to cure any Senior Loan Default within the following periods after Mezzanine Lender's receipt of written notice thereof:
> (a) Monetary Default: 30 days (or, if longer, 5 days after the expiration of Borrower's cure period)
> (b) Non-Monetary Default: 60 days (or, if longer, 10 days after the expiration of Borrower's cure period)"

**Inadequate** (flag):
> Cure periods shorter than the above, or cure rights conditioned on Senior Lender's approval.

**Why it matters**: Mezz lender needs time to evaluate whether to cure and to arrange funding. 30/60 days is the market minimum.

### Intercreditor Provision 3: Purchase Option

**Adequate**:
> "Mezzanine Lender shall have the option, exercisable within 30 days of the occurrence of any uncured Senior Loan Event of Default, to purchase the Senior Loan for the Purchase Price. The Purchase Price shall equal the outstanding principal balance of the Senior Loan, plus accrued and unpaid interest at the non-default rate, plus any protective advances made by Senior Lender, minus any unapplied amounts in reserve accounts."

**Inadequate** (flag):
- Purchase option window shorter than 30 days
- Purchase price includes default rate interest (punishes mezz lender for senior default)
- Purchase price includes all fees, expenses, and prepayment premium (makes option economically unfeasible)

**Why it matters**: The purchase option is the mezz lender's ultimate protection. If the senior loan defaults, the mezz lender can buy the senior loan at par and take control of the situation. A purchase option that is economically impractical (high purchase price) or has too short an exercise window is no protection at all.

### Intercreditor Provision 4: Senior Loan Amendments

**Adequate**:
> "Senior Lender shall not modify or amend the Senior Loan Documents in any manner that: (i) increases the interest rate or fees; (ii) shortens the maturity date; (iii) increases the outstanding principal; (iv) imposes additional reserve requirements; or (v) otherwise materially and adversely affects the Mezzanine Lender, without the prior written consent of Mezzanine Lender."

**Inadequate** (flag):
- No restriction on senior loan amendments
- Senior lender can increase reserves or fees without mezz consent (dilutes mezz collateral)

**Why it matters**: A senior lender amendment that shortens the maturity date, increases the interest rate, or adds reserves effectively subordinates the mezz lender's position without the mezz lender's agreement.

---

## Guarantor Exposure Quantification Template

Use the following to quantify total guarantor exposure under the signed guaranty.

```
GUARANTOR EXPOSURE ANALYSIS
Loan: [property name], $[X] outstanding balance
Guarantor(s): [names]
Analysis Date: [date]

STANDARD CARVE-OUTS:
  Environmental: Unlimited (capped at cost of actual remediation)
    Phase I findings: [clean / RECs noted / Phase II required]
    Estimated environmental exposure: $[X]-$[X] (from Phase I/II)
  Fraud: Full loan amount ($[X]) if triggered
  Waste: Actual damages (estimated $[X] based on property value)
  Rent misappropriation: Actual amount (estimated $[X] based on monthly rent roll)
  Voluntary bankruptcy: Full loan amount ($[X]) if triggered
  Unauthorized transfer: Full loan amount ($[X]) if triggered

NON-STANDARD CARVE-OUTS (flagged in document review):
  [List each non-standard carve-out]:
    Carve-out: [description]
    Trigger: [what causes it]
    Exposure: [amount or "full loan amount"]
    Probability of trigger: [Low / Medium / High based on business plan]
    Negotiation status: [Removed / Modified to: X / Accepted with risk note]

TOTAL MAXIMUM GUARANTOR EXPOSURE:
  If only standard carve-outs triggered: $[X]-$[X] (environmental + actual damages)
  If one springing full recourse trigger fires: $[X] (full outstanding loan amount)
  If environmental catastrophe: Unlimited

RISK MITIGATION:
  Phase II environmental: [Not required / Required and completed]
  Title insurance: $[X] policy
  Contractual protections: [seller environmental indemnity / prior owner indemnity]
  Entity structuring: [guaranty is at level of [individual / holding company / portfolio entity]]
```

---

## Carve-Out Language Red Flag Summary

Quick reference for document review. Flag any of these in the loan documents.

| Red Flag | Type | Severity | Action |
|---|---|---|---|
| DSCR below threshold = springing full recourse | Operational trigger | Critical | Negotiate removal |
| Occupancy below threshold = springing full recourse | Operational trigger | Critical | Negotiate removal |
| MAC clause triggering full recourse | Undefined trigger | Critical | Negotiate removal |
| Environmental indemnity extends beyond property boundary | Scope expansion | Critical | Limit to property boundary |
| Failure to pay taxes = full loan amount | Disproportionate remedy | Significant | Limit to actual damages |
| Failure to maintain insurance = full loan amount | Disproportionate remedy | Significant | Limit to actual damages |
| Lease modification without consent = full loan amount | Disproportionate remedy | Significant | Limit to actual damages |
| Financial reporting failure = personal liability | No economic basis | Significant | Remove entirely |
| Cross-default with other properties | Portfolio scope | Significant | Limit to this property |
| Cure period < 5 days for monetary default | Too short | Significant | Negotiate to 10 days minimum |
| Guaranteed obligations include prepayment premium | Scope expansion | Moderate | Negotiate exclusion |
| Guaranty of future advances without cap | Open-ended | Moderate | Cap to original loan amount |
| No deemed approval for lease approvals | Operational restriction | Moderate | Add 15-day deemed approval |
