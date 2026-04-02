# 1031 Exchange Timeline Calculator Reference

Day-by-day timeline reference for managing forward, reverse, and improvement 1031 exchanges. Includes milestone checklists, deadline extension rules for presidentially declared disasters, and state-specific considerations.

---

## Day-by-Day Timeline: Forward Exchange

### Pre-Exchange (Days -90 to -1)

```yaml
phase: pre_exchange
description: "Preparation before close of relinquished property"

day_neg90_to_neg60:
  label: "Strategic Planning"
  tasks:
    - "Confirm property qualifies (held for investment or business use, not dealer property)"
    - "Calculate estimated gain: sale_price - adjusted_basis = gain"
    - "Calculate depreciation recapture: Section 1250 amount taxed at 25%"
    - "Calculate federal + state tax if no exchange"
    - "Determine exchange type (forward, reverse, improvement)"
    - "Begin replacement property search (do NOT wait until after Day 0)"
  owner: "CPA, Tax Attorney, Exchanger"
  deliverable: "Tax analysis memo with exchange vs no-exchange comparison"

day_neg60_to_neg30:
  label: "QI Selection and Engagement"
  tasks:
    - "Interview 2-3 QI firms"
    - "Verify QI qualifications:"
    - "  - Segregated accounts (not commingled)"
    - "  - Fidelity bond >= $5M for exchanges over $1M"
    - "  - E&O insurance >= $2M"
    - "  - FDIC-insured accounts"
    - "  - FEA (Federation of Exchange Accommodators) membership"
    - "  - 10+ years in business, 500+ exchange track record"
    - "Execute exchange agreement with selected QI"
    - "Confirm QI's timeline calculation matches yours"
  owner: "Tax Attorney, Exchanger"
  deliverable: "Executed exchange agreement"

day_neg30_to_neg1:
  label: "Pre-Close Preparation"
  tasks:
    - "Confirm relinquished property PSA assigns exchanger's interest to QI at closing"
    - "Provide QI's wire instructions to closing agent / title company"
    - "Confirm direct deed: title passes from exchanger to buyer (not through QI)"
    - "Notify buyer of exchange and assignment (most PSAs require notice)"
    - "Continue replacement property search (5-10 candidates in pipeline)"
    - "Pre-qualify for financing on 2-3 leading replacement candidates"
  owner: "Exchanger, Broker, Closing Attorney"
  deliverable: "Assignment documents, wire instructions, replacement candidate shortlist"
```

### Exchange Period: Identification Phase (Days 0-45)

```yaml
phase: identification
description: "45-day identification period -- HARD DEADLINE"

day_0:
  label: "Relinquished Property Closes"
  tasks:
    - "Close on sale of relinquished property"
    - "Confirm net proceeds wire sent to QI (NOT to exchanger)"
    - "Confirm QI received funds and provides written acknowledgment"
    - "Confirm exchange agreement is activated"
    - "Record Day 45 and Day 180 dates (calculate exactly)"
    - "If tax return extension not filed: file immediately"
  critical: true
  note: "Day 0 is immovable. All subsequent dates are calculated from this."

day_1_to_5:
  label: "Post-Close Verification"
  tasks:
    - "Confirm QI account is segregated and FDIC-insured"
    - "Obtain written confirmation of fund receipt and account details"
    - "Confirm QI's calculation of Day 45 and Day 180 dates"
    - "Verify no funds were inadvertently sent to exchanger (constructive receipt check)"
    - "Commence formal replacement property search if not already underway"

day_6_to_14:
  label: "Broad Search"
  tasks:
    - "Request offering materials on 6-10 candidates"
    - "Conduct preliminary financial review (cap rate, NOI, occupancy)"
    - "Eliminate candidates with obvious disqualifiers (timeline, boot, quality)"
    - "Schedule property tours for top candidates"
    - "Begin debt replacement analysis: can you match or exceed relinquished debt?"

day_15_to_25:
  label: "Narrowing and Touring"
  tasks:
    - "Tour 3-5 leading candidates"
    - "Request detailed financials: rent roll, T12, operating statements"
    - "Preliminary title search on top 2-3 candidates"
    - "Preliminary environmental screening (Phase I availability)"
    - "Score each candidate per Workflow 3 framework"
    - "Begin PSA negotiations on leading candidate (conditional on identification)"

day_26_to_35:
  label: "Scoring and Selection"
  tasks:
    - "Finalize candidate scores"
    - "Confirm boot exposure for each candidate (Workflow 4)"
    - "Engage legal counsel for identification letter preparation"
    - "If no strong candidates by Day 30: begin DST research (Workflow 6)"
    - "Pre-arrange financing: LOI from lender on primary candidate"

day_36_to_40:
  label: "Identification Letter Preparation"
  tasks:
    - "Draft identification letter with all required elements"
    - "Legal description or unambiguous street address for each property"
    - "Confirm delivery method with QI (courier + email recommended)"
    - "Review letter with counsel"
    - "Sign identification letter"
    - "TARGET: send letter by Day 40 (5-day buffer)"
  critical: true

day_41_to_43:
  label: "Letter Delivery"
  tasks:
    - "Send identification letter via primary method (courier or hand delivery)"
    - "Send backup copy via email with read receipt"
    - "Obtain QI acknowledgment of receipt"
    - "If Day 43 and letter not yet acknowledged: call QI immediately"
    - "Document delivery confirmation (tracking number, receipt, email confirmation)"
  critical: true

day_44:
  label: "Emergency Buffer"
  tasks:
    - "If letter not yet delivered: hand-deliver to QI office"
    - "If QI office closed (weekend/holiday): this is too late -- letter should have been sent earlier"
    - "If using certified mail: confirm USPS tracking shows delivered"
  critical: true
  note: "This is the emergency buffer day. If you are relying on Day 44, the process failed at Day 40."

day_45:
  label: "IDENTIFICATION DEADLINE"
  tasks:
    - "Confirm QI has received identification letter"
    - "Obtain written confirmation from QI of properties identified"
    - "The identification CANNOT be amended after this date"
    - "Any property not on the letter cannot be acquired as a replacement"
  critical: true
  hard_deadline: true
  note: "No extensions. No exceptions. No relief. Letter must be RECEIVED by QI before midnight local time of exchanger."
```

### Exchange Period: Acquisition Phase (Days 46-180)

```yaml
phase: acquisition
description: "135-day acquisition period -- HARD DEADLINE at Day 180"

day_46_to_60:
  label: "PSA Execution"
  tasks:
    - "Execute PSA on primary replacement property"
    - "Open escrow with title company"
    - "Begin formal due diligence period (per PSA terms)"
    - "Order Phase I environmental"
    - "Order survey"
    - "Order preliminary title report"
    - "Submit loan application to lender"

day_61_to_90:
  label: "Due Diligence"
  tasks:
    - "Complete Phase I environmental (if clean, proceed; if RECs found, evaluate)"
    - "Review title report and address title objections"
    - "Complete property inspection / property condition assessment"
    - "Review tenant estoppels (if commercial)"
    - "Review lease abstracts and rent roll verification"
    - "Lender appraisal ordered and completed"
    - "Lender underwriting in process"

day_91_to_120:
  label: "Financing and DD Resolution"
  tasks:
    - "Lender issues commitment letter"
    - "Resolve any DD findings (environmental remediation, title cure, tenant issues)"
    - "Clear title objections or negotiate indemnification"
    - "Finalize loan terms and conditions"
    - "If primary candidate failing: pivot to backup identified property"
    - "If pivoting: reset DD timeline -- confirm can still close by Day 180"

day_121_to_150:
  label: "Pre-Closing Preparation"
  tasks:
    - "Loan documents drafted and circulated"
    - "Entity formation for replacement property (if needed)"
    - "Insurance binder obtained"
    - "Closing agent / title company prepares settlement statement"
    - "QI provides wire instructions for exchange proceeds"
    - "Coordinate QI wire timing with closing agent"

day_151_to_170:
  label: "Closing Execution"
  tasks:
    - "Finalize loan documents (sign)"
    - "Confirm lender funding date and advance notice requirement"
    - "Schedule closing date (target Day 160-170)"
    - "Confirm QI can wire exchange proceeds on closing day"
    - "Final title search and bring-down"
    - "Close on replacement property"

day_171_to_179:
  label: "Emergency Buffer"
  tasks:
    - "If not yet closed: this is critical -- escalate all outstanding items"
    - "If lender delay: demand expedited processing or consider all-cash close"
    - "If title issue: negotiate around it or consider title indemnification"
    - "DST fallback: if direct acquisition cannot close, execute DST by Day 179"

day_180:
  label: "ACQUISITION DEADLINE"
  tasks:
    - "All replacement property must be acquired by this date"
    - "Title must transfer to exchanger (recorded deed)"
    - "If not closed: exchange fails entirely"
    - "All deferred gain becomes immediately taxable"
  critical: true
  hard_deadline: true
  note: "No extensions. No exceptions. Unless presidentially declared disaster applies (see below)."
```

---

## Deadline Extension: Presidentially Declared Disasters

```
The ONLY circumstance under which 45-day and 180-day deadlines may be extended:

Condition: A presidentially declared disaster (under the Stafford Act) affects the
exchanger, the relinquished property, or the replacement property.

How it works:
  - IRS issues a notice (e.g., Notice 2024-XX) specifying:
    a. Which disaster qualifies
    b. Which deadlines are extended
    c. The new deadline dates
    d. Which taxpayers are eligible (by location, typically FEMA-declared counties)

  - Typical extension: 120 additional days from the original deadline
  - Extensions are disaster-specific and location-specific
  - Exchanger must be in the affected area OR the exchange property must be in the affected area

What to do:
  1. If a disaster occurs during the exchange period:
     - Check IRS.gov for disaster relief notices
     - Check FEMA.gov for declared disaster areas
     - Confirm with CPA and tax attorney whether the exchange qualifies
  2. Document everything: the disaster, the IRS notice, the extended deadlines
  3. Do NOT assume the extension applies -- verify with the specific IRS notice

Recent examples:
  - COVID-19 (2020): IRS Notice 2020-23 extended deadlines for exchanges with
    deadlines falling between April 1 and July 15, 2020
  - Hurricane-declared disasters: county-specific extensions
  - California wildfires: county-specific extensions

IMPORTANT: Disasters do NOT extend deadlines for all exchanges.
The exchange must have a deadline falling within the disaster relief period,
and the exchanger or property must be in the affected area.
```

---

## State-Specific Considerations

```yaml
state_rules:
  california:
    conforms_to_federal: true
    clawback: "If replacement property is out of state, CA may claw back deferred gain when replacement is eventually sold. File Form 593 and FTB 3840 annually."
    withholding: "CA may withhold 3.33% of sale price unless exemption claimed"
    note: "CA is the most aggressive state for 1031 enforcement"

  new_york:
    conforms_to_federal: true
    clawback: false
    note: "NY conforms fully. Transfer tax applies to relinquished sale regardless of exchange."

  texas:
    conforms_to_federal: true
    state_income_tax: false
    note: "No state income tax. 1031 is purely a federal tax planning tool in TX."

  florida:
    conforms_to_federal: true
    state_income_tax: false
    note: "No state income tax for individuals. Corporate income tax applies to C-corps."

  massachusetts:
    conforms_to_federal: "Partially"
    clawback: "MA may not recognize out-of-state replacement property for state tax deferral"
    note: "Consult MA-specific tax counsel"

  oregon:
    conforms_to_federal: "Partially"
    note: "OR has specific reporting requirements for 1031 exchanges involving OR property"

  montana:
    conforms_to_federal: "Partially"
    note: "MT has enacted limitations on 1031 treatment for certain property types"
```

---

## Quick Reference: Day Count Table

```
Use this table to quickly calculate Day 45 and Day 180 from any Day 0:

Day 0 (Jan):  Jan 1  -> Day 45: Feb 15  -> Day 180: Jun 30
              Jan 15 -> Day 45: Mar 1   -> Day 180: Jul 14
              Jan 31 -> Day 45: Mar 17  -> Day 180: Jul 30

Day 0 (Feb):  Feb 1  -> Day 45: Mar 18  -> Day 180: Jul 31
              Feb 15 -> Day 45: Apr 1   -> Day 180: Aug 14
              Feb 28 -> Day 45: Apr 14  -> Day 180: Aug 27

Day 0 (Mar):  Mar 1  -> Day 45: Apr 15  -> Day 180: Aug 28
              Mar 15 -> Day 45: Apr 29  -> Day 180: Sep 11
              Mar 31 -> Day 45: May 15  -> Day 180: Sep 27

Day 0 (Apr):  Apr 1  -> Day 45: May 16  -> Day 180: Sep 28
              Apr 15 -> Day 45: May 30  -> Day 180: Oct 12
              Apr 30 -> Day 45: Jun 14  -> Day 180: Oct 27

Day 0 (May):  May 1  -> Day 45: Jun 15  -> Day 180: Oct 28
              May 15 -> Day 45: Jun 29  -> Day 180: Nov 11
              May 31 -> Day 45: Jul 15  -> Day 180: Nov 27

Day 0 (Jun):  Jun 1  -> Day 45: Jul 16  -> Day 180: Nov 28
              Jun 15 -> Day 45: Jul 30  -> Day 180: Dec 12
              Jun 30 -> Day 45: Aug 14  -> Day 180: Dec 27

Day 0 (Jul):  Jul 1  -> Day 45: Aug 15  -> Day 180: Dec 28
              Jul 15 -> Day 45: Aug 29  -> Day 180: Jan 11 (next year)
              Jul 31 -> Day 45: Sep 14  -> Day 180: Jan 27 (next year)

Day 0 (Aug):  Aug 1  -> Day 45: Sep 15  -> Day 180: Jan 28 (next year)
              Aug 15 -> Day 45: Sep 29  -> Day 180: Feb 11 (next year)
              Aug 31 -> Day 45: Oct 15  -> Day 180: Feb 27 (next year)

Day 0 (Sep):  Sep 1  -> Day 45: Oct 16  -> Day 180: Feb 28 (next year)
              Sep 15 -> Day 45: Oct 30  -> Day 180: Mar 14 (next year)
              Sep 30 -> Day 45: Nov 14  -> Day 180: Mar 29 (next year)

Day 0 (Oct):  Oct 1  -> Day 45: Nov 15  -> Day 180: Mar 30 (next year)
              Oct 15 -> Day 45: Nov 29  -> Day 180: Apr 13 (next year)
              Oct 31 -> Day 45: Dec 15  -> Day 180: Apr 29 (next year)

Day 0 (Nov):  Nov 1  -> Day 45: Dec 16  -> Day 180: Apr 30 (next year)
              Nov 15 -> Day 45: Dec 30  -> Day 180: May 14 (next year)
              Nov 30 -> Day 45: Jan 14 (next year) -> Day 180: May 29 (next year)

Day 0 (Dec):  Dec 1  -> Day 45: Jan 15 (next year) -> Day 180: May 30 (next year)
              Dec 15 -> Day 45: Jan 29 (next year) -> Day 180: Jun 13 (next year)
              Dec 31 -> Day 45: Feb 14 (next year) -> Day 180: Jun 29 (next year)

NOTE: These are approximate. Always compute exact dates using a calendar.
      Leap years add 1 day to any period crossing Feb 29.
      Tax return due date (Apr 15 or Oct 15 with extension) may further limit Day 180.
```
