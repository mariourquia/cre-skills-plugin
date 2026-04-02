# Vendor Invoice Dispute Resolution Templates

## Overview

Templates and checklists for disputing vendor invoices, comparing contract rates,
and verifying scope of work in commercial real estate property management.

---

## 1. Dispute Letter Template

### Standard Invoice Dispute Letter

```
[Property Management Company Letterhead]

Date: [YYYY-MM-DD]

[Vendor Name]
[Vendor Address]
[City, State ZIP]

RE: Invoice Dispute - Invoice #[NUMBER]
    Property: [Property Name and Address]
    Invoice Date: [YYYY-MM-DD]
    Invoice Amount: $[AMOUNT]
    Disputed Amount: $[AMOUNT]

Dear [Vendor Contact Name],

We have completed our review of the above-referenced invoice and have
identified the following discrepancies that require resolution before
payment can be processed.

DISCREPANCY SUMMARY:

| Item | Description              | Invoiced   | Contract   | Variance   |
|------|--------------------------|------------|------------|------------|
|  1   | [Line item description]  | $[amount]  | $[amount]  | $[amount]  |
|  2   | [Line item description]  | $[amount]  | $[amount]  | $[amount]  |
|  3   | [Line item description]  | $[amount]  | $[amount]  | $[amount]  |
|      | TOTAL DISPUTED           |            |            | $[amount]  |

DETAILED FINDINGS:

1. [Line item]: The invoiced rate of $[X]/[unit] exceeds the contracted
   rate of $[Y]/[unit] per Section [X] of our service agreement dated
   [date]. Please revise to reflect the contract rate.

2. [Line item]: This charge of $[X] for [service] was not authorized
   under the existing scope of work. Our records do not contain a
   change order or written authorization for this additional work.
   Per Section [X] of our agreement, all out-of-scope work requires
   prior written approval from the property manager.

3. [Line item]: The quantity billed ([X] units) does not match our
   field verification ([Y] units). Please provide supporting
   documentation (time sheets, material receipts, delivery tickets)
   for the invoiced quantity.

REQUESTED ACTION:

Please issue a corrected invoice reflecting the adjustments above within
[15] business days. Alternatively, provide supporting documentation that
substantiates the original charges. Upon receipt of the corrected invoice
or acceptable documentation, we will process payment within our standard
[30]-day payment cycle.

The undisputed portion of this invoice ($[amount]) will be processed
for payment on our next payment cycle ([date]).

Please direct all correspondence regarding this dispute to:

[Property Manager Name]
[Email]
[Phone]

We value our working relationship and look forward to a prompt resolution.

Sincerely,

_________________________
[Property Manager Name]
[Title]
[Property Management Company]

cc: [Owner/Asset Manager]
    [Accounting Department]

Enclosures:
- Copy of disputed invoice
- Relevant contract excerpts
- Field verification documentation
```

### Escalation Letter (Second Notice)

```
[Property Management Company Letterhead]

Date: [YYYY-MM-DD]

[Vendor Name]
[Vendor Address]

RE: SECOND NOTICE - Unresolved Invoice Dispute
    Invoice #[NUMBER] - Originally Disputed [DATE]
    Property: [Property Name]

Dear [Vendor Contact Name],

This letter serves as our second notice regarding the invoice dispute
communicated on [original dispute date]. As of this date, we have not
received a corrected invoice or adequate supporting documentation.

DISPUTE TIMELINE:
  Original invoice date:     [YYYY-MM-DD]
  Initial dispute notice:    [YYYY-MM-DD]
  Response deadline:         [YYYY-MM-DD]
  Days since initial notice: [X] days
  Response received:         NONE / INADEQUATE

OUTSTANDING DISPUTED AMOUNT: $[AMOUNT]

Per Section [X] of our service agreement, disputes not resolved within
[30] days may result in:

  1. Withholding of the disputed amount from future payments
  2. Engagement of a third-party auditor at vendor's expense
     (if audit reveals overcharge exceeding 5%)
  3. Formal review of the vendor relationship, including potential
     termination per Section [X] (termination for cause)

We request your immediate attention to this matter. Please provide
one of the following within [10] business days:

  (a) A corrected invoice reflecting the adjustments in our original
      dispute notice, OR
  (b) Documented evidence supporting the original charges, including
      time sheets, material invoices, change orders, and delivery
      receipts.

If we do not receive a response by [DATE], we will proceed with
withholding the disputed amount and initiating a formal vendor review.

Sincerely,

_________________________
[Senior Property Manager / Director Name]
[Title]

cc: [Vendor's supervisor/owner]
    [Asset Manager]
    [Legal counsel (if applicable)]
```

---

## 2. Contract Rate Comparison Format

### Rate Comparison Worksheet

```yaml
vendor_contract_comparison:
  vendor_name: "[Name]"
  contract_number: "[Number]"
  contract_date: "[YYYY-MM-DD]"
  contract_expiration: "[YYYY-MM-DD]"
  property: "[Property Name]"

  rate_comparison:
    - category: "Regular Maintenance"
      items:
        - description: "Technician hourly rate"
          contract_rate: 85.00
          invoiced_rate: 95.00
          variance: 10.00
          variance_pct: 11.8
          status: "DISPUTED"
          contract_reference: "Exhibit B, Section 2.1"

        - description: "Helper/apprentice hourly rate"
          contract_rate: 55.00
          invoiced_rate: 55.00
          variance: 0.00
          variance_pct: 0.0
          status: "VERIFIED"
          contract_reference: "Exhibit B, Section 2.1"

        - description: "Overtime rate (after 5pm/weekends)"
          contract_rate: 127.50  # 1.5x regular
          invoiced_rate: 142.50  # 1.5x of wrong base
          variance: 15.00
          variance_pct: 11.8
          status: "DISPUTED"
          contract_reference: "Exhibit B, Section 2.2"

    - category: "Materials"
      items:
        - description: "Materials markup"
          contract_rate: "Cost + 15%"
          invoiced_rate: "Cost + 25%"
          variance: "10% excess markup"
          status: "DISPUTED"
          contract_reference: "Exhibit B, Section 3.1"

        - description: "Materials over $500 pre-approval"
          contract_rate: "Required"
          invoiced_rate: "Not obtained"
          variance: "Process violation"
          status: "DISPUTED"
          contract_reference: "Section 4.3"

    - category: "Emergency Services"
      items:
        - description: "Emergency response fee"
          contract_rate: 250.00
          invoiced_rate: 350.00
          variance: 100.00
          variance_pct: 40.0
          status: "DISPUTED"
          contract_reference: "Exhibit B, Section 5.1"

        - description: "Emergency hourly rate"
          contract_rate: 150.00  # 2x regular
          invoiced_rate: 150.00
          variance: 0.00
          status: "VERIFIED"

  escalation_verification:
    contract_escalation: "CPI annually, max 3%"
    last_escalation_date: "[YYYY-MM-DD]"
    escalation_applied: 2.8  # percent
    cpi_actual: 2.8
    within_cap: true
    status: "VERIFIED"

  summary:
    total_invoiced: 12450.00
    total_at_contract_rates: 10875.00
    total_disputed: 1575.00
    disputed_pct: 12.7
```

### Multi-Vendor Rate Benchmarking

```
Service: HVAC Preventive Maintenance (quarterly, 50-ton system)

Vendor           | Contract Rate | Market Low | Market Mid | Market High | Status
-----------------|---------------|------------|------------|-------------|--------
Current: ABC HVAC| $1,850/visit  | $1,200     | $1,600     | $2,100      | In range
Bid 1: XYZ Mech  | $1,400/visit  |            |            |             | Below mid
Bid 2: DEF Svcs  | $1,650/visit  |            |            |             | At mid
Bid 3: GHI Corp  | $2,200/visit  |            |            |             | Above high

Market source: RS Means, local PM network survey (n=12)
Recommendation: Current vendor in range but 15% above median.
                Renegotiate to $1,650 at next renewal or award to Bid 2.

Service: Janitorial (nightly, 50,000 SF office)

Vendor           | Contract Rate | Market Low | Market Mid | Market High | Status
-----------------|---------------|------------|------------|-------------|--------
Current: Clean Co| $0.22/SF/mo   | $0.15      | $0.20      | $0.28       | In range
Bid 1: Sparkle   | $0.18/SF/mo   |            |            |             | Below mid
Bid 2: ProClean  | $0.21/SF/mo   |            |            |             | At mid

Market source: BOMA benchmarks, 3 competitive bids
Recommendation: Current rate acceptable. No action needed.
```

---

## 3. Scope Verification Checklist

### Pre-Invoice Verification (Field Check)

```yaml
scope_verification:
  invoice_reference: "[Invoice #]"
  vendor: "[Name]"
  service_date: "[YYYY-MM-DD]"
  property: "[Property Name]"
  verified_by: "[PM Name]"
  verification_date: "[YYYY-MM-DD]"

  work_authorization:
    - check: "Work order or purchase order exists"
      status: "YES / NO"
      reference: "[WO/PO #]"
    - check: "Work within existing contract scope"
      status: "YES / NO"
      note: "If NO, was change order approved?"
    - check: "Spending authority limit not exceeded"
      status: "YES / NO"
      limit: "$[amount]"
      invoice_amount: "$[amount]"
    - check: "Required approvals obtained before work"
      status: "YES / NO"
      approver: "[Name]"
      approval_date: "[YYYY-MM-DD]"

  quantity_verification:
    - check: "Labor hours match field observation"
      invoiced: "[X] hours"
      observed: "[Y] hours"
      status: "MATCH / DISPUTE"
    - check: "Number of workers matches sign-in log"
      invoiced: "[X] workers"
      log_shows: "[Y] workers"
      status: "MATCH / DISPUTE"
    - check: "Materials delivered match delivery receipts"
      invoiced_items: "[list]"
      received_items: "[list]"
      status: "MATCH / DISPUTE"
    - check: "Equipment rental hours/days match field records"
      invoiced: "[X] days"
      field_record: "[Y] days"
      status: "MATCH / DISPUTE"

  quality_verification:
    - check: "Work completed as specified"
      status: "YES / NO / PARTIAL"
      deficiencies: "[describe if any]"
    - check: "Punch list items completed"
      status: "YES / NO / N/A"
      open_items: "[count]"
    - check: "Area left clean and restored"
      status: "YES / NO"
    - check: "Permits obtained and closed (if required)"
      status: "YES / NO / N/A"
      permit_number: "[number]"
    - check: "Warranty documentation received"
      status: "YES / NO / N/A"
      warranty_term: "[months/years]"

  rate_verification:
    - check: "Hourly rates match contract"
      status: "YES / NO"
      variance: "$[amount]"
    - check: "Material prices verified (receipts provided)"
      status: "YES / NO"
    - check: "Markup within contract limits"
      status: "YES / NO"
      contract_markup: "[X]%"
      invoiced_markup: "[Y]%"
    - check: "Travel/mobilization charges per contract"
      status: "YES / NO / N/A"
    - check: "No duplicate charges from prior invoices"
      status: "VERIFIED / DUPLICATE FOUND"

  overall_status:
    approved_amount: "$[amount]"
    disputed_amount: "$[amount]"
    action: "APPROVE / APPROVE PARTIAL / DISPUTE / HOLD"
    notes: "[explanation]"
```

### Recurring Service Verification Matrix

For monthly or quarterly recurring service contracts:

```
Service Contract: [Vendor Name] - [Service Type]
Contract #: [Number]
Monthly Fee: $[Amount]
Verification Period: [Month/Quarter]

Deliverable               | Required | Completed | Verified | Notes
--------------------------|----------|-----------|----------|------
Monthly PM report         | Yes      | Y/N       | Y/N      |
Equipment inspection logs | Yes      | Y/N       | Y/N      |
Filter replacements       | Quarterly| Y/N       | Y/N      | [lot #]
Belt inspections          | Monthly  | Y/N       | Y/N      |
Refrigerant levels        | Quarterly| Y/N       | Y/N      | [readings]
Drain pan cleaning        | Monthly  | Y/N       | Y/N      |
Coil cleaning             | Semi-ann | Y/N       | Y/N      |
Controls calibration      | Quarterly| Y/N       | Y/N      | [readings]
Emergency response calls  | As needed| [count]   | [count]  | [response time]
After-hours calls         | As needed| [count]   | [count]  | [invoiced separately?]

Deliverables completed: [X] of [Y] = [Z]%
If < 90%: withhold 10% of monthly fee pending completion
If < 75%: issue cure notice per contract Section [X]
If < 50%: grounds for termination per contract Section [X]

Verified by: ________________  Date: ________
```

---

## 4. Dispute Resolution Process

### Escalation Ladder

```
Level 1: Property Manager <-> Vendor Account Rep
  Timeline: 15 business days
  Method: Written dispute letter + phone discussion
  Resolution: Corrected invoice or supporting documentation

Level 2: Senior PM / Director <-> Vendor Branch Manager
  Timeline: 15 additional business days (30 total)
  Method: Formal meeting, written summary
  Resolution: Negotiated settlement, credit memo, or payment plan

Level 3: Asset Manager / Owner <-> Vendor Principal
  Timeline: 15 additional business days (45 total)
  Method: Executive-level discussion
  Resolution: Final settlement or contract termination

Level 4: Legal / Mediation
  Timeline: 30-90 additional days
  Method: Demand letter from attorney, mediation
  Resolution: Mediated settlement, arbitration, or litigation
  Threshold: Generally disputes > $25,000
```

### Dispute Tracking Log

```yaml
dispute_log:
  - dispute_id: "D-2026-001"
    vendor: "[Name]"
    invoice: "#12345"
    amount_disputed: 3450.00
    date_identified: "2026-01-15"
    dispute_letter_sent: "2026-01-18"
    response_due: "2026-02-08"
    response_received: "2026-02-05"
    resolution: "Corrected invoice issued"
    credit_received: 2800.00
    resolved_date: "2026-02-12"
    days_to_resolve: 28
    escalation_level: 1

  - dispute_id: "D-2026-002"
    vendor: "[Name]"
    invoice: "#12389"
    amount_disputed: 8200.00
    date_identified: "2026-02-01"
    dispute_letter_sent: "2026-02-03"
    response_due: "2026-02-24"
    response_received: null
    second_notice_sent: "2026-02-28"
    resolution: "Pending"
    escalation_level: 2
    next_action: "Meeting with vendor branch manager scheduled 2026-03-10"
```
