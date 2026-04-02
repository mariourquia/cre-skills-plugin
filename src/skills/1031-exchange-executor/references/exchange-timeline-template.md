# 1031 Exchange Timeline Template

## Overview

Day-by-day timeline template for managing a forward 1031 exchange from
pre-sale preparation through replacement property acquisition. Includes
parallel tracks for QI coordination, property identification, due diligence,
and financing.

---

## Pre-Exchange Preparation (Days -90 to -1)

### Day -90 to -60: Strategic Planning

```yaml
tasks:
  tax_analysis:
    - "Calculate estimated gain and tax liability without exchange"
    - "Determine depreciation recapture (Section 1250)"
    - "Model boot scenarios (partial exchange vs full deferral)"
    - "Confirm property qualifies (held for investment/business, not dealer)"
    - "Review state tax implications (some states don't conform to 1031)"
    owner: "CPA / Tax Advisor"
    deliverable: "Tax analysis memo with exchange vs no-exchange comparison"

  exchange_structure:
    - "Select exchange type (forward, reverse, improvement)"
    - "Determine if DST fallback is needed"
    - "If debt replacement is an issue, plan financing for replacement early"
    - "Review any related party considerations"
    owner: "Tax Attorney"
    deliverable: "Exchange structure recommendation"

  replacement_property_search:
    - "Define replacement property criteria (type, size, location, return)"
    - "Engage broker for replacement property search"
    - "Begin touring potential replacement properties"
    - "Pre-qualify for financing on replacement property"
    owner: "Exchanger + Broker"
    deliverable: "Replacement property shortlist (5-10 candidates)"
```

### Day -60 to -30: QI and Team Assembly

```yaml
tasks:
  qi_selection:
    - "Interview 2-3 QI firms"
    - "Verify: segregated accounts, fidelity bond, FEA membership"
    - "Confirm QI is not disqualified person"
    - "Negotiate fee and interest allocation on held funds"
    - "Execute QI engagement letter"
    owner: "Exchanger"
    deliverable: "Signed QI engagement agreement"

  legal_preparation:
    - "Draft exchange agreement with QI"
    - "Review relinquished property PSA for exchange cooperation clause"
    - "Prepare assignment of PSA to QI (for closing)"
    - "Notify buyer that exchange will occur (buyer cooperation clause)"
    owner: "Exchange Attorney"
    deliverable: "Exchange agreement, PSA assignment"

  financing:
    - "Pre-approval for replacement property financing"
    - "Confirm loan assumption feasibility (if applicable)"
    - "Calculate required equity and debt for full deferral"
    owner: "Mortgage Broker / Lender"
    deliverable: "Pre-approval letter, financing term sheet"
```

### Day -30 to -1: Final Pre-Sale

```yaml
tasks:
  closing_coordination:
    - "Confirm closing date for relinquished property"
    - "Ensure QI is named in closing instructions"
    - "Wire instructions: proceeds go DIRECTLY to QI (not exchanger)"
    - "Confirm no funds will flow through exchanger's account"
    - "Title company briefed on exchange structure"
    owner: "Exchange Attorney + Title Company"

  identification_prep:
    - "Narrow replacement candidates to top 5"
    - "Begin due diligence on top 2-3 candidates"
    - "Prepare identification letter (addresses, legal descriptions)"
    - "Have backup DST options identified and ready"
    owner: "Exchanger + Broker"

  critical_reminders:
    - "DO NOT take possession of any sale proceeds"
    - "DO NOT instruct QI to pay personal obligations"
    - "DO NOT sign closing docs that give exchanger access to funds"
    - "Confirm exchange agreement has proper safe harbor language"
```

---

## Day 0: Relinquished Property Closes

```yaml
day_0:
  date: "YYYY-MM-DD"
  tasks:
    - time: "Morning"
      action: "Final walkthrough of relinquished property"
    - time: "At closing"
      action: "Execute assignment of PSA from exchanger to QI"
    - time: "At closing"
      action: "QI signs closing documents as principal"
    - time: "At closing"
      action: "Net proceeds wired DIRECTLY to QI segregated account"
    - time: "Post-closing"
      action: "Confirm wire receipt with QI (same day)"
    - time: "Post-closing"
      action: "Record sale with county (title company handles)"
    - time: "Post-closing"
      action: "Calendar Day 45 and Day 180 deadlines"

  verification:
    - "Proceeds deposited in QI account: $________"
    - "Mortgage payoff confirmed: $________"
    - "Selling costs paid: $________"
    - "Net exchange value: $________"
    - "QI confirmation received: YES / NO"

  deadlines_set:
    day_45: "YYYY-MM-DD (identification deadline)"
    day_180: "YYYY-MM-DD (exchange deadline)"
    tax_return_due: "YYYY-MM-DD (if earlier than Day 180, file extension)"
```

---

## Days 1-15: Active Identification Period

```yaml
days_1_to_15:
  priority: "HIGH -- active property search and due diligence"
  tasks:
    week_1:
      - "Tour top 3 replacement candidates in person"
      - "Request seller financials (T12, rent roll, tax returns)"
      - "Order preliminary title on top candidate"
      - "Engage property inspector"
      - "Submit LOI on top candidate"
    week_2:
      - "Negotiate LOI/PSA on replacement property"
      - "Begin Phase I environmental (if not already available)"
      - "Verify zoning and permitted uses"
      - "Run lease audit on replacement rent roll"
      - "Confirm financing terms with lender"
```

---

## Days 16-30: Due Diligence and Backup Planning

```yaml
days_16_to_30:
  priority: "HIGH -- close on primary, prepare backups"
  tasks:
    primary_property:
      - "Execute PSA on primary replacement property"
      - "Open escrow, deposit earnest money"
      - "Order appraisal, survey, environmental"
      - "Review leases, service contracts, warranties"
      - "Inspect property (physical, mechanical, structural)"
      - "Review title commitment, resolve exceptions"
    backup_planning:
      - "Maintain active search for backup properties"
      - "Pre-qualify 1-2 DST investments as emergency fallback"
      - "Request DST PPMs and subscription docs"
      - "Keep broker engaged on backup candidates"
    financing:
      - "Submit full loan application for replacement property"
      - "Lender orders appraisal and third-party reports"
      - "Review loan commitment terms"
```

---

## Days 31-44: Identification Finalization

```yaml
days_31_to_44:
  priority: "CRITICAL -- identification deadline approaching"
  tasks:
    day_31_to_40:
      - "Assess primary property due diligence progress"
      - "If any red flags: accelerate backup identification"
      - "Finalize list of up to 3 identified properties"
      - "If using 200% rule: calculate aggregate FMV"
      - "Prepare written identification letter"
    day_41_to_43:
      - "Final decision on identified properties"
      - "Draft identification letter with:"
      - "  (a) Exchanger name and exchange reference number"
      - "  (b) Each property: address, legal description, estimated FMV"
      - "  (c) Statement: 'The above properties are identified as replacement'"
      - "  (d) Date and signature of exchanger"
      - "Have attorney review identification letter"
    day_44:
      - "DELIVER identification letter to QI"
      - "Send via email AND certified mail (belt and suspenders)"
      - "Request written acknowledgment from QI"
      - "Retain copy with proof of delivery"
      - "DO NOT WAIT UNTIL DAY 45"
```

---

## Day 45: Identification Deadline

```yaml
day_45:
  date: "YYYY-MM-DD"
  status: "HARD DEADLINE -- NO EXTENSIONS"

  by_end_of_day:
    - "Identification letter delivered to QI: YES / NO"
    - "QI acknowledgment received: YES / NO"
    - "Number of properties identified: ___"
    - "Rule used: 3-property / 200% / 95%"

  identified_properties:
    property_1:
      address: "_______"
      estimated_fmv: "$_______"
      psa_status: "Executed / In negotiation / Identified only"
    property_2:
      address: "_______"
      estimated_fmv: "$_______"
      psa_status: "_______"
    property_3:
      address: "_______"  # Often DST fallback
      estimated_fmv: "$_______"
      psa_status: "_______"

  if_identification_missed:
    consequence: "Exchange fails. Full gain recognized in year of sale."
    action: "Consult tax advisor immediately for mitigation strategies"
    options:
      - "Installment sale (if any proceeds remain with QI)"
      - "Opportunity Zone investment (different section, partial deferral)"
      - "Charitable remainder trust (if charitable intent exists)"
```

---

## Days 46-150: Replacement Acquisition

```yaml
days_46_to_150:
  priority: "Execute on identified property; keep backups alive"
  tasks:
    due_diligence_completion:
      - "Complete Phase I environmental review"
      - "Receive and review appraisal"
      - "Survey review and exception resolution"
      - "Finalize title commitment"
      - "Complete property inspection and negotiate repairs"
      - "Review and approve estoppel certificates from tenants"
      - "Approve all service contracts for assumption"
      - "Review property tax history and appeals"

    financing:
      - "Receive loan commitment"
      - "Clear all loan conditions"
      - "Order rate lock (timing depends on market)"
      - "Prepare for closing: insurance binder, entity docs"

    exchange_coordination:
      - "Confirm with QI: funds available for closing"
      - "Coordinate closing instructions with QI"
      - "QI will assign PSA and close as principal (same as relinquished)"
      - "Wire instructions: QI sends funds directly to replacement closing"

    contingency_planning:
      week_8: "If primary at risk, accelerate backup"
      week_12: "If primary dead, pivot to backup or DST"
      week_16: "DST subscription must be completed by Day 170 at latest"
      week_20: "If no property closing, exchange will fail"
```

---

## Days 151-175: Pre-Closing

```yaml
days_151_to_175:
  priority: "CRITICAL -- closing must occur by Day 180"
  tasks:
    - "Confirm closing date (must be on or before Day 180)"
    - "Dry run: verify all closing conditions met"
    - "Confirm QI wire timing (QI may need 24-48 hours for large wires)"
    - "Title company prepares closing statement showing QI as buyer"
    - "Review final closing statement for exchange compliance"
    - "Confirm replacement debt sufficient for full deferral"
    - "Calculate any boot exposure and plan accordingly"

  boot_check:
    cash_boot: "Are all QI funds being deployed? If not, how much cash boot?"
    mortgage_boot: "Is replacement debt >= relinquished debt? If not, adding cash?"
    action: "If boot unavoidable, calculate tax and confirm acceptable"

  closing_logistics:
    - "Schedule closing with all parties"
    - "Coordinate buyer entity formation (if purchasing in new LLC)"
    - "Transfer insurance policies"
    - "Utility transfers"
    - "Tenant notification letters"
```

---

## Days 176-180: Final Closing Window

```yaml
days_176_to_180:
  priority: "MAXIMUM -- exchange expires Day 180"
  tasks:
    day_176_178:
      - "Final walkthrough of replacement property"
      - "Sign closing documents"
      - "QI executes assignment and closing docs"
      - "QI wires funds to closing agent"
    day_179:
      - "BACKUP CLOSING DAY if Day 178 closing delayed"
      - "If closing not possible: execute DST subscription"
    day_180:
      - "ABSOLUTE FINAL DAY"
      - "If closing has not occurred: exchange fails"
      - "DST subscription must be fully executed and funded"

  if_closing_delayed:
    options:
      - "Push closing to earliest possible date (must be Day 180 or earlier)"
      - "Switch to backup identified property if primary cannot close"
      - "Subscribe to DST if no direct property can close"
      - "Accept partial exchange (some boot) rather than total failure"
```

---

## Day 180: Exchange Deadline

```yaml
day_180:
  date: "YYYY-MM-DD"
  status: "HARD DEADLINE -- EXCHANGE MUST CLOSE"

  outcome_matrix:
    full_deferral:
      condition: "Replacement closed, all cash reinvested, debt replaced"
      action: "File Form 8824 with tax return"
      tax: "$0 current year"
    partial_exchange:
      condition: "Replacement closed, but boot received"
      action: "File Form 8824, report boot as gain"
      tax: "Capital gains on boot amount only"
    exchange_failure:
      condition: "No replacement acquired by Day 180"
      action: "QI returns funds to exchanger"
      tax: "Full gain recognized, capital gains + depreciation recapture"

  post_closing:
    - "Obtain final QI accounting statement"
    - "Calculate new basis in replacement property"
    - "Set up depreciation schedule on replacement property"
    - "File Form 8824 with next tax return"
    - "Retain all exchange documentation for 7+ years"
```

---

## Post-Exchange Checklist

```yaml
post_exchange:
  immediately:
    - "Confirm deed recorded in exchanger's (or entity's) name"
    - "Obtain title insurance policy for replacement property"
    - "Transfer all insurance policies"
    - "Notify tenants of ownership change"
    - "Set up property management"
    - "Transfer utility accounts"

  within_30_days:
    - "Receive final QI accounting"
    - "Reconcile all funds (relinquished proceeds vs replacement costs)"
    - "Calculate new adjusted basis"
    - "Begin depreciation on replacement property"
    - "File change of ownership with county assessor"

  at_tax_filing:
    - "File IRS Form 8824 (Like-Kind Exchanges)"
    - "Report: description of properties, dates, amounts"
    - "Attach to individual or entity tax return"
    - "State filings (if state has separate exchange reporting)"
    - "Retain: QI agreement, identification letter, closing statements,
       exchange accounting, deed copies -- minimum 7 years"

  ongoing:
    - "Hold replacement property for minimum 24 months (safe harbor)"
    - "Do not immediately list for sale (intent scrutiny)"
    - "If planning another exchange: begin replacement search 6-12 months before"
    - "Track cumulative deferred gain across serial exchanges"
    - "Estate planning: at death, heirs receive stepped-up basis"
```
