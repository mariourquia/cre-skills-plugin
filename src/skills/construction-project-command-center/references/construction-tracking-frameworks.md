# Construction Tracking Frameworks Reference

Complete methodologies for RFI management, submittal tracking, change order evaluation, earned value analysis, and critical path monitoring. All examples use a baseline $45M ground-up multifamily project (200 units, 18-month construction timeline).

---

## 1. RFI Log Management

### Log Structure

| Field | Type | Purpose |
|---|---|---|
| RFI # | sequential int | unique identifier, never reused |
| Date Submitted | date | GC submission date |
| Submitted By | string | GC, sub name, or architect |
| Spec Section | string | CSI division and section (e.g., 03 30 00 - Cast-in-Place Concrete) |
| Drawing Reference | string | sheet number and detail (e.g., S-201, Detail 3) |
| Question | text | clear, specific question requiring a design decision |
| Priority | enum | Critical, High, Standard, Informational |
| Response Due | date | per contract (typically 7-10 business days) |
| Responded By | string | architect, engineer, or owner |
| Response Date | date | actual response date |
| Days Open | computed | response_date - date_submitted (or current_date if open) |
| CO Potential | boolean | does the response imply a scope or cost change? |
| Status | enum | Open, Responded, Closed, Void |

### Priority Classification

```
Critical:  Blocks active work. Crew is idle or will be within 24 hours.
           Response required: same day or next business day.
           Escalation: immediate call to architect + owner.

High:      Blocks work within 5 business days. Lookahead shows this trade
           cannot proceed without resolution.
           Response required: 3 business days.
           Escalation: email to architect with owner cc at day 2.

Standard:  Does not currently block work. Clarification needed for upcoming
           activities (2-4 weeks out).
           Response required: 7-10 business days per contract.
           Escalation: weekly OAC meeting agenda item at day 7.

Informational: Documentation of field condition or existing condition.
               No response required -- acknowledgment only.
               No escalation.
```

### Aging Report Template

```
RFI Aging Report -- Project: [name] -- Date: [date]

Summary:
  Total RFIs issued:      [n]
  Open:                   [n]  ([n] Critical, [n] High, [n] Standard)
  Closed this period:     [n]
  Average days to close:  [n] days
  Overdue (past response deadline): [n]

Open RFIs by Age:
  0-7 days:    [n] ([list])
  8-14 days:   [n] ([list])
  15-30 days:  [n] ([list])  <-- flag all as overdue if Standard
  30+ days:    [n] ([list])  <-- escalation required regardless of priority

Open RFIs by Responsible Party:
  Architect:   [n]
  Structural:  [n]
  MEP:         [n]
  Owner:       [n]
  GC:          [n]

CO Potential Flag:
  RFIs with CO potential: [n] (estimated exposure: $[amount])
```

### Worked Example

Project: 200-unit multifamily, month 6 of 18

```
RFI #047 -- Critical
  Submitted: 2026-01-15 by GC (XYZ Construction)
  Spec: 03 30 00 (Cast-in-Place Concrete)
  Drawing: S-301, Detail 7
  Question: Structural drawing shows #5 rebar at 12" o.c. in transfer beam at
            grid line C-4, but structural notes call for #6 at 8" o.c. for
            transfer beams > 24" depth. Beam is 30" deep. Which governs?
  Priority: Critical -- forming crew on-site, concrete pour scheduled 01/18.
  Response Due: 01/15 (same day)
  Response: Structural engineer confirms #6 at 8" o.c. governs. Drawing to be
            updated in next ASI. No cost impact (rebar difference is minor).
  Days Open: 0
  CO Potential: No -- rebar quantity difference is within tolerance.
  Status: Closed

RFI #048 -- High
  Submitted: 2026-01-16 by MEP Sub (ABC Mechanical)
  Spec: 23 05 00 (Common Work for HVAC)
  Drawing: M-401
  Question: Ductwork routing at Level 3 corridor conflicts with structural
            beam at grid D-6. Duct cannot maintain minimum ceiling height
            (8'-0" AFF) without rerouting. Request design team resolution.
  Priority: High -- HVAC rough-in starts Level 3 in 4 days.
  Response Due: 01/21
  Response (01/20): Architect directs soffit at corridor D-6 to accommodate
                    duct. Ceiling height reduced to 7'-8" at soffit (within
                    code minimum). No additional cost.
  Days Open: 4
  CO Potential: No -- field coordination, no cost change.
  Status: Closed
```

---

## 2. Change Order Evaluation Framework

### Cost Reasonableness Analysis

For each change order line item, verify:

1. **Labor rates**: compare to prevailing wage schedule (if applicable) or contract-established rates
2. **Material costs**: compare to RS Means, recent procurement quotes, or contract unit prices
3. **Equipment rates**: compare to Blue Book or contract-established rates
4. **Productivity**: are the labor hours reasonable for the scope? Reference RS Means crew productivity data
5. **Markup**: verify markup is within contractual limits

**Typical markup structure (GMP contract)**:

```
Subcontractor self-performed work:
  Labor burden:           30-40% of base labor (FICA, insurance, benefits)
  Overhead:               10-15% of direct costs
  Profit:                 5-10% of direct costs
  Sub total markup:       15-25% of direct costs (typical negotiated: 15%)

GC markup on sub work:
  Overhead:               5-8% of sub cost
  Profit:                 3-5% of sub cost
  GC total markup:        8-13% of sub cost (typical negotiated: 10%)

GC self-performed work:
  Markup:                 15-20% of direct costs (OH&P combined)
```

### Cumulative Budget Impact Tracker

```
Change Order Budget Impact -- Project: [name] -- Date: [date]

Original Contract (GMP):              $32,500,000
Approved Change Orders:
  CO #001 - Owner-directed finish upgrade:     +$145,000
  CO #002 - Unsuitable soil remediation:       +$287,000
  CO #003 - Electrical panel upsizing:          +$42,000
  CO #004 - Fire alarm redesign (code change):  +$93,000
  ...
  Total Approved COs:                          +$892,000

Pending Change Orders:
  PCO #012 - Waterproofing scope addition:     +$165,000 (est.)
  PCO #013 - Elevator pit modification:         +$78,000 (est.)
  Total Pending COs:                           +$243,000

Current Contract Value:                        $33,392,000
  (original + approved)
Projected Contract Value:                      $33,635,000
  (current + pending estimate)

Contingency Status:
  Original contingency:                        $1,625,000 (5.0% of original)
  Contingency used (CO charges):                -$567,000
  Remaining contingency:                       $1,058,000
  Project % complete:                          38%
  Contingency burn rate:                       34.9% consumed at 38% complete
  Status:                                      GREEN (burn < completion %)
```

### Contingency Drawdown Analysis

```
Expected contingency drawdown curve (industry benchmark):

  25% complete:  15-25% contingency consumed
  50% complete:  40-55% contingency consumed
  75% complete:  65-80% contingency consumed
  100% complete: 85-95% contingency consumed (5-15% should remain)

Warning thresholds:
  Contingency consumed > project % complete + 15%:  YELLOW
  Contingency consumed > project % complete + 25%:  RED
  Contingency consumed > 90% before 75% complete:   RED -- immediate review

Your project at 38% complete with 34.9% consumed: GREEN
  (34.9% < 38% + 15% = 53% threshold)
```

### Change Order Classification

| Classification | Definition | Cost Responsibility | Schedule Impact |
|---|---|---|---|
| Owner-directed | Owner requests a change to scope/finishes/program | Owner bears cost | Compensable time if on critical path |
| Field condition | Unforeseen site condition (soil, existing structure) | Depends on contract risk allocation | Typically excusable, may be compensable |
| Design error/omission | Architect/engineer mistake or gap in documents | A/E E&O insurance claim potential | Excusable and compensable |
| Code requirement | Building code change or AHJ interpretation | Depends on contract language | Typically excusable |
| Allowance reconciliation | Actual cost vs contract allowance amount | True-up per contract | No schedule impact |
| VE credit | Value engineering savings accepted by owner | Credit to owner | May improve schedule |

### Worked Example: Change Order Evaluation

```
CO #005 -- Proposed by GC

Description: Additional waterproofing at below-grade parking level P2.
             Existing contract includes bentonite sheet membrane at P1.
             Geotechnical report (Section 4.3) identifies seasonal high
             water table at 2' below P2 slab. GC proposes crystalline
             waterproofing additive + additional drain tile at P2.

Proposed cost breakdown:
  Crystalline additive (Xypex):     $18/SF x 12,400 SF  = $223,200
  Additional drain tile:            $24/LF x 680 LF     = $16,320
  Labor (waterproofing sub):        480 hours x $65/hr   = $31,200
  Equipment:                        lump sum             = $4,800
  Sub OH&P (15%):                                        = $41,328
  GC markup (10%):                                       = $31,685
  Total proposed:                                        = $348,533

Evaluation:

1. Cost reasonableness:
   - Xypex crystalline: RS Means shows $14-22/SF installed. $18/SF is mid-range. PASS.
   - Drain tile: RS Means shows $18-30/LF for interior drain tile. $24/LF reasonable. PASS.
   - Labor: 480 hours for 12,400 SF = 25.8 SF/hour. RS Means shows 20-30 SF/hour
     for crystalline application. PASS.
   - Markup: 15% sub + 10% GC = combined 26.5% of direct costs. Per contract
     limits (15% sub, 10% GC). PASS.

2. Classification: Field condition -- geotech report disclosed water table,
   but original design did not address P2 waterproofing. Potential design
   omission. Flag for A/E E&O consideration.

3. Schedule impact: GC claims 8 additional days for P2 waterproofing before
   slab pour. P2 slab is on critical path. 8 days is reasonable for 12,400 SF
   application + cure time. JUSTIFIED.

4. Budget impact:
   - This CO at $348,533 brings total approved+pending to $1,240,533
   - Contingency remaining after approval: $709,467
   - Project 38% complete with 56.4% contingency consumed: YELLOW

Recommendation: APPROVE with notation that cost should be tracked under
potential A/E E&O claim. Request A/E provide written explanation for why
P2 waterproofing was omitted from original design given geotech data.
```

---

## 3. Earned Value Analysis

### Core Metrics and Interpretation

| Metric | Formula | Good | Warning | Critical |
|---|---|---|---|---|
| CPI | EV / AC | > 1.00 | 0.90-1.00 | < 0.90 |
| SPI | EV / PV | > 1.00 | 0.90-1.00 | < 0.90 |
| TCPI | (BAC - EV) / (BAC - AC) | < 1.10 | 1.10-1.20 | > 1.20 |
| VAC | BAC - EAC | > 0 | -5% to 0 | < -5% |

Where:
- BAC = Budget at Completion (original total budget)
- EAC = Estimate at Completion = BAC / CPI (simplest method)
- TCPI = To-Complete Performance Index (required future CPI to finish on budget)

### Worked Example: Month 8 of 18

```
Earned Value Report -- Month 8

Budget at Completion (BAC):          $32,500,000
Planned Value (PV) through Month 8:  $16,250,000  (cumulative planned spend)
Earned Value (EV) through Month 8:   $14,950,000  (budgeted cost of work done)
Actual Cost (AC) through Month 8:    $15,780,000  (actual spend to date)

CPI = 14,950,000 / 15,780,000 = 0.947
  Interpretation: for every $1.00 spent, $0.95 of budgeted work is accomplished.
  Status: WARNING -- 5.3% cost overrun on completed work.

SPI = 14,950,000 / 16,250,000 = 0.920
  Interpretation: 92% of planned work is complete.
  Status: WARNING -- 8% behind schedule.

EAC = 32,500,000 / 0.947 = $34,319,000
  Projected overrun: $1,819,000 (5.6% over budget)

ETC = 34,319,000 - 15,780,000 = $18,539,000
  Remaining cost to complete at current performance.

VAC = 32,500,000 - 34,319,000 = -$1,819,000
  Projected to finish $1.82M over budget.

TCPI = (32,500,000 - 14,950,000) / (32,500,000 - 15,780,000)
     = 17,550,000 / 16,720,000 = 1.050
  Must achieve CPI of 1.05 on remaining work to finish on budget.
  This is achievable but requires immediate corrective action.

Trend (last 3 months):
  Month 6 CPI: 0.98  SPI: 0.95
  Month 7 CPI: 0.96  SPI: 0.93
  Month 8 CPI: 0.947 SPI: 0.92
  Trend: DECLINING -- both metrics worsening. Corrective action required.
```

### Corrective Action Triggers

```
CPI declining for 2 consecutive months:
  1. Require GC cost-to-complete analysis by trade
  2. Identify top 3 cost overrun drivers
  3. Evaluate value engineering opportunities
  4. Consider scope reduction if available
  5. Brief lender on projected overrun if EAC exceeds contingency

SPI declining for 2 consecutive months:
  1. Require GC recovery schedule within 5 business days
  2. Identify critical path activities causing delay
  3. Evaluate acceleration options (overtime, additional crews, resequencing)
  4. Calculate acceleration cost vs liquidated damages exposure
  5. Formal delay notice if GC-caused per contract

Both CPI and SPI below 0.90:
  1. Formal project distress notification to ownership
  2. Lender notification per loan agreement requirements
  3. Weekly (not monthly) EVA reporting
  4. Consider independent schedule/cost consultant
  5. Evaluate GC performance bond claim if GC-fault driven
```

---

## 4. Critical Path Methodology

### Float Analysis

```
Total Float = Late Finish - Early Finish (for each activity)

Critical path activities: Total Float = 0
Near-critical activities: Total Float = 1-10 days
Non-critical activities:  Total Float > 10 days

Float consumption tracking:
  If an activity's remaining float decreases by > 50% in one reporting
  period without corresponding progress, it is trending toward critical.
  Flag for immediate attention.
```

### Schedule Variance Report Template

```
Critical Path Activities -- Month [n]

| Activity | Baseline Duration | Baseline Finish | Forecast Finish | Variance | Status |
|---|---|---|---|---|---|
| Foundations | 45 days | 03/15 | 03/18 | +3 days | YELLOW |
| Structural steel L1-3 | 60 days | 05/20 | 05/20 | 0 days | GREEN |
| MEP rough-in L1 | 30 days | 06/25 | 07/05 | +10 days | RED |
| Exterior envelope | 75 days | 08/15 | 08/15 | 0 days | GREEN |
| ...

Near-Critical Activities (float < 10 days):
| Activity | Remaining Float | Risk |
|---|---|---|
| Elevator installation | 5 days | Long-lead equipment delivery |
| Fire alarm rough-in | 8 days | Dependent on MEP rough-in |
```

### Delay Analysis

For each claimed delay:

```
1. Is the delay on the critical path?
   - If no: delay consumes float but does not extend project. No time extension.
   - If yes: proceed to classification.

2. Delay classification:
   - Excusable-compensable: owner-caused delay. GC gets time + money.
     Examples: owner-directed changes, site access delays, owner-furnished
     equipment late.
   - Excusable-non-compensable: neither party's fault. GC gets time only.
     Examples: weather (beyond contract allowance), force majeure, pandemic,
     unforeseen site conditions.
   - Non-excusable: GC-caused. No time extension, LD exposure begins.
     Examples: inadequate crew, poor coordination, sub default.
   - Concurrent: both owner and GC delays overlap. Typically excusable but
     not compensable (jurisdiction-dependent).

3. Documentation requirements:
   - Daily logs showing impact
   - Contemporaneous schedule showing critical path shift
   - Written notice per contract requirements (typically within 7-14 days
     of delay event)
   - Quantification of time and cost impact
```
