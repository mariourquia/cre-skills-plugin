# Closing Conditions Guide: PSA Execution Through Wire Transfer

---

## PURPOSE

This guide covers the mechanics of closing a CRE acquisition: standard closing conditions, MAC clause analysis, deposit structures (hard vs. soft, day-one hard deposit negotiation), and title/survey exception categories. It is a reference for PSA negotiation and closing preparation.

---

## Part 1: Standard Closing Conditions

Closing conditions are the prerequisites each party must satisfy before the other is obligated to close. A failure of any condition entitles the non-failing party to terminate or extend.

### Buyer's Conditions to Closing (Buyer may refuse to close if any are unsatisfied)

| # | Condition | Standard | Notes |
|---|---|---|---|
| 1 | Title insurance commitment | ALTA owner's policy with no unacceptable exceptions | Buyer reviews and approves during DD; title company issues final commitment pre-closing |
| 2 | Survey | Current ALTA/NSPS survey with no unacceptable exceptions | Survey objections resolved during DD; updated at closing if changes occurred |
| 3 | Estoppel certificates | From tenants occupying 80%+ of units/SF | Must be dated within 30 days of closing; material discrepancies = termination right |
| 4 | Seller representations true at closing | All reps reaffirmed at closing via bring-down certificate | "No material adverse change" standard; Seller signs a closing certificate |
| 5 | No material adverse change | Property in substantially the same condition as at PSA execution | Casualty, condemnation, tenant default, environmental discovery triggers MAC analysis |
| 6 | Tenant leases in effect | No major tenant has terminated or given notice | "Major tenant" defined in PSA (typically 10%+ of revenue) |
| 7 | Environmental clearance | Phase I ESA identifies no RECs requiring Phase II | If Phase II triggered, closing delayed or terminated per DD provisions |
| 8 | Zoning confirmation | Property is legally conforming or legally non-conforming | Certificate of occupancy current; no pending violations |
| 9 | Financing | Buyer's lender has issued a closing commitment | Only if financing contingency was retained |
| 10 | Government approvals | No pending condemnation, rezoning, or regulatory action | Seller certifies via closing certificate |

### Seller's Conditions to Closing (Seller may refuse to close if unsatisfied)

| # | Condition | Standard | Notes |
|---|---|---|---|
| 1 | Purchase price delivered | Wire transfer of immediately available funds | Buyer's lender funds simultaneously |
| 2 | Buyer's closing documents | Signed and delivered per closing checklist | Assignment agreements, lender documents, entity authorizations |
| 3 | No Buyer default | Buyer has performed all obligations under PSA | Timely deposit delivery, timely DD completion |

---

## Part 2: MAC Clause Analysis Framework

### What Constitutes a Material Adverse Change

A MAC in CRE is any event between PSA execution and closing that materially reduces the value, income, or condition of the property. Unlike M&A MAC clauses (which are notoriously vague), CRE MAC clauses should be specific and quantified.

### MAC Event Categories

**Category A: Physical Condition**

| Event | MAC Threshold | Buyer's Rights |
|---|---|---|
| Fire/casualty | Repair cost > 2% of purchase price or $250K (whichever is less) | Terminate with full deposit refund OR proceed with insurance assignment + price credit for deductible |
| Flood damage | Any flooding in units or common areas | Same as fire/casualty |
| Structural discovery | Foundation, load-bearing, or building envelope issue not identified in PCA | Terminate or negotiate credit equal to remediation cost |
| Environmental discovery | Phase I REC confirmed by Phase II; remediation cost > $100K | Terminate or negotiate credit; Seller environmental indemnity may apply |

**Category B: Income/Tenancy**

| Event | MAC Threshold | Buyer's Rights |
|---|---|---|
| Major tenant default | Tenant representing > 10% of revenue defaults or files bankruptcy | Terminate or negotiate rent credit + vacancy reserve |
| Occupancy decline | Occupancy drops below [X]% (typically 5-10 points below PSA-date occupancy) | Terminate or negotiate credit for lost income during re-lease period |
| Rent concessions | Seller grants concessions not authorized by Buyer | Terminate or credit equal to concession value over remaining lease term |
| Lease termination | Any tenant exercising a termination option not disclosed in DD | Terminate if > 10% of revenue; credit if < 10% |

**Category C: Regulatory/Legal**

| Event | MAC Threshold | Buyer's Rights |
|---|---|---|
| Condemnation notice | Any notice of taking, even partial | Terminate or proceed with assignment of condemnation award + price credit |
| Zoning change | Any change that renders current use non-conforming | Terminate |
| Code violation | Citation requiring > $50K in remediation | Terminate or Seller cures before closing |
| Litigation | Lawsuit filed against the property or Seller relating to the property | Terminate if damages > $100K or if litigation clouds title |

**Category D: Market/Financing**

| Event | Buyer's Rights |
|---|---|
| Interest rate increase | No MAC right (market risk is Buyer's; this is why financing contingencies exist) |
| Comparable sale at lower cap rate | No MAC right (market repricing is not a property-specific MAC) |
| Lender pulls commitment | Financing contingency applies if retained; otherwise Buyer must close with cash |

### MAC Analysis Decision Tree

```
Event occurs between PSA execution and closing
    |
    v
Is the event covered by the PSA's MAC provision?
    |
    +-- Yes --> Does the event exceed the defined threshold?
    |               |
    |               +-- Yes --> Buyer may terminate with deposit refund
    |               |           OR proceed with credit/assignment
    |               |
    |               +-- No --> Not a MAC; Buyer must close
    |
    +-- No --> Is the event covered by Seller's representations?
                |
                +-- Yes --> Seller breach; Buyer may terminate or
                |           seek indemnification post-closing
                |
                +-- No --> Buyer bears the risk unless Buyer can
                            demonstrate fraud or willful concealment
```

### MAC Clause Drafting Principles

1. **Quantify thresholds**. "Material" without a dollar figure is litigable. "$250,000 or 2% of Purchase Price" is not.
2. **Enumerate categories**. A general MAC clause that says "material adverse change in the condition or value of the Property" is less protective than one that specifically enumerates casualty, condemnation, environmental, and tenant events.
3. **Specify remedies**. Termination with deposit refund should be the default. Proceed-with-credit should be the Buyer's option, not the Seller's.
4. **Include "threatened" events**. A condemnation that is threatened but not formally commenced still depresses value. Include "commenced or threatened" language.
5. **Time the bring-down**. Seller reaffirms reps at closing. If any rep is no longer true, Buyer has a MAC termination right. This is the "bring-down certificate" and is the primary enforcement mechanism.

---

## Part 3: Deposit Mechanics

### Hard vs. Soft Deposits

| Feature | Soft (Refundable) Deposit | Hard (Non-Refundable) Deposit |
|---|---|---|
| Timing | During DD period | After DD expiration |
| Refundability | Full refund if Buyer terminates during DD | Non-refundable except for Seller default or MAC |
| Typical amount | 1-3% of purchase price | 2-5% of purchase price |
| Signal to Seller | "I'm serious but still evaluating" | "I'm closing this deal" |
| Risk to Buyer | Minimal (limited to DD costs if terminated) | Deposit at risk if Buyer defaults |

### Deposit Timeline (Standard Structure)

```
PSA Execution (Day 0)
    |
    +--> Soft deposit due (Day 3-5): $[X] into escrow
    |
    +--> DD Period (Days 1-30)
    |       |
    |       +--> Buyer may terminate: full refund of soft deposit
    |
    +--> DD Expiration (Day 30): Deposit goes hard
    |       |
    |       +--> Additional hard deposit due: $[X] (optional)
    |
    +--> Financing Contingency Expiration (Day 45)
    |
    +--> Closing (Day 60): Deposit applied to purchase price
```

### Day-One Hard Deposit Negotiation

A day-one hard deposit means the Buyer's earnest money is non-refundable from the moment the PSA is executed. This is the most aggressive term a buyer can offer and is used primarily in competitive bid situations.

**When to offer day-one hard**:
- Marketed deal with 10+ offers and clear seller preference for certainty
- Asset you know well (you've toured it, you know the market, you've pre-underwritten)
- Basis is so compelling that you'd close even with moderate negative DD findings
- You have a relationship with the broker and intel that the seller values certainty above price

**When NOT to offer day-one hard**:
- First-time acquisition in an unfamiliar market
- Environmental risk indicators (gas station proximity, industrial history, soil concerns)
- Complex title (multiple parcels, easement disputes, boundary issues)
- Seller has not provided financials or rent roll pre-LOI

**Sizing day-one hard deposits**:
- 1% of purchase price: Minimum credible day-one hard. Below 1% is not meaningful.
- 2-3%: Standard competitive day-one hard for marketed multifamily.
- 5%+: Extremely aggressive. Used for trophy assets or distressed acquisitions where the discount justifies the risk.

**Protective provisions when offering day-one hard**:
1. Environmental carve-out: "Notwithstanding the foregoing, if Buyer's Phase I ESA identifies a Recognized Environmental Condition requiring remediation estimated to cost $[X] or more, Buyer may terminate with full Deposit refund."
2. Title carve-out: "Notwithstanding the foregoing, if the title commitment reveals a defect that is not insurable and not curable, Buyer may terminate with full Deposit refund."
3. Fraud carve-out: "Notwithstanding the foregoing, if Seller's representations are materially false, Buyer may terminate with full Deposit refund."

These carve-outs preserve the appearance of a hard deposit while retaining exit rights for the scenarios most likely to destroy value.

---

## Part 4: Title and Survey Exception Categories

### What Is a Title Exception?

A title exception is any matter that appears on the title commitment as an exception to the title insurer's coverage. The title company is saying: "We will insure your ownership except for these items." Exceptions fall into standard categories.

### Standard (Usually Acceptable) Exceptions

| Category | Examples | Risk Level | Action |
|---|---|---|---|
| Utility easements | Electric, gas, water, sewer easements within defined corridors | Low | Review survey to confirm easements don't cross building footprint; accept if standard |
| Recorded covenants | CC&Rs, deed restrictions, HOA rules | Low-Medium | Review for use restrictions; confirm current use is compliant |
| Property taxes | Current and future real property taxes | None | Standard; taxes are always excepted |
| Zoning ordinances | Municipal zoning regulations | None | Standard; zoning is always excepted |
| Rights of tenants in possession | Leasehold interests under existing leases | Low | Confirm via estoppel certificates; accept if leases are as represented |
| Survey matters | Minor encroachments (fence, planter, sign) | Low | Accept if encroachment is < 12 inches and does not affect building or parking |

### Potentially Problematic Exceptions (Require Review)

| Category | Examples | Risk Level | Action |
|---|---|---|---|
| Access easements | Third-party access roads crossing the property | Medium | Confirm easement does not restrict development or parking; verify location on survey |
| Drainage easements | Stormwater detention or drainage across the property | Medium | Confirm easement area is not within building footprint or planned improvement area |
| Mineral rights reservations | Prior owner retained subsurface mineral rights | Medium-High | Evaluate extraction risk; in some states (PA, TX, WV), mineral rights include surface access |
| Historic preservation | Property on historic register or in historic district | Medium | Restricts exterior modifications; may restrict demolition; evaluate renovation plans |
| Restrictive covenants | Use restrictions (e.g., no commercial use, no multi-family) | High | Confirm current use is permitted; violations can trigger forfeiture |
| Mechanic's liens | Contractor claims for unpaid work | High | Seller must cure before closing; non-negotiable |

### Unacceptable Exceptions (Must Be Cured or Buyer Terminates)

| Category | Examples | Risk Level | Action |
|---|---|---|---|
| Mortgage liens | Existing mortgages not being paid off at closing | Critical | Seller must pay off all mortgage liens at or before closing |
| Judgment liens | Court judgments against Seller recorded against the property | Critical | Seller must satisfy or bond around all judgment liens |
| Tax liens | Delinquent property tax or IRS federal tax liens | Critical | Seller must pay off all tax liens at closing |
| Lis pendens | Pending litigation notice recorded against property | Critical | Evaluate litigation; may require resolution before closing or indemnification |
| Mechanics' liens | Contractor claims for unpaid pre-closing work | Critical | Seller must satisfy or bond around before closing |
| Boundary disputes | Survey reveals overlap with adjacent property | Critical | Title company may exclude the disputed area; evaluate materiality |
| Encroachments by neighbors | Adjacent building or structure encroaching on the property | High-Critical | Evaluate materiality; may require easement agreement or legal action |

### Survey Review Checklist

| Item | What to Check | Red Flag |
|---|---|---|
| Boundary lines | Match legal description in deed | Discrepancy between survey and deed |
| Building footprint | Within property lines with required setbacks | Building crosses property line or violates setback |
| Easements | Plotted on survey; do not cross building | Easement crosses building footprint or parking area |
| Flood zone | FEMA flood zone designation | Zone AE or AH (100-year floodplain); evaluate insurance cost |
| Access | Legal access to public road confirmed | No legal access = landlocked property; critical defect |
| Encroachments | Adjacent improvements on our property; our improvements on adjacent | Encroachment > 12 inches into building area |
| Parking count | Actual spaces match zoning requirement | Deficit may trigger variance requirement |
| Utilities | Utility lines plotted; no conflicts with improvements | Water/sewer lines under planned construction area |

### Title Insurance Endorsements (Buyer Should Request)

| Endorsement | ALTA # | Purpose |
|---|---|---|
| Access | 17/17.1 | Insures legal access to public road |
| Zoning | 3/3.1 | Insures current use complies with zoning |
| Survey | -- | Deletes standard survey exception based on new survey |
| Contiguity | 19 | Confirms multiple parcels are contiguous (for assemblage) |
| Environmental protection lien | 8.1 | Insures against priority environmental liens |
| Tax parcel | 18/18.1 | Confirms property is separately taxed |
| Comprehensive | 9 | Omnibus endorsement covering common issues |
| Subdivision | -- | Confirms compliance with subdivision laws |

---

## Part 5: Closing Checklist

### T-30 Days to Closing

- [ ] Title commitment reviewed; all objections raised in writing
- [ ] Survey reviewed; all objections raised in writing
- [ ] Estoppel certificates received from 80%+ of tenants
- [ ] Environmental Phase I completed with no unresolved RECs
- [ ] Property condition assessment completed
- [ ] Appraisal completed (if financing)
- [ ] Lender closing commitment received (if financing)
- [ ] Insurance binder obtained for closing date
- [ ] Entity formation for acquiring SPE completed

### T-14 Days to Closing

- [ ] Title objections cured or waived
- [ ] Survey objections cured or waived
- [ ] PSA closing conditions checklist reviewed with counsel
- [ ] Seller's bring-down certificate drafted
- [ ] Transfer tax calculations confirmed with title company
- [ ] Prorations worksheet prepared (rents, taxes, utilities)
- [ ] Closing statement (HUD-1 or settlement statement) draft reviewed
- [ ] Utility account transfer initiated

### T-7 Days to Closing

- [ ] Final walkthrough of property completed
- [ ] Closing funds confirmed with lender and equity sources
- [ ] Wire instructions verified via phone (fraud prevention)
- [ ] Closing documents reviewed and pre-signed where possible
- [ ] Security deposit transfer confirmed with property manager
- [ ] Vendor contracts: list of contracts to assume vs. terminate delivered to Seller
- [ ] Property management transition plan confirmed

### Closing Day

- [ ] Buyer's wire sent (verify receipt with title company)
- [ ] Lender's wire sent (verify receipt with title company)
- [ ] All documents executed and delivered
- [ ] Title company records deed and mortgage
- [ ] Title policy issued or committed to issue
- [ ] Keys, access codes, and property files delivered
- [ ] Tenant notification letters sent (ownership change)
- [ ] Insurance policy effective as of closing date
