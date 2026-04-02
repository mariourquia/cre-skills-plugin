# Leasing Pipeline Management Framework Reference

Pipeline stage definitions, conversion rate benchmarks, velocity metrics, CRM field requirements, and reporting templates. Worked example uses a 200,000 SF Class A office building in Midtown Manhattan with 30,000 SF available across 4 suites.

---

## 1. Pipeline Stage Definitions and CRM Fields

### Required CRM Fields by Stage

**All stages (mandatory on every record)**:

| Field | Type | Purpose |
|---|---|---|
| Prospect ID | auto-generated | unique identifier |
| Company name | string | legal or trade name |
| Primary contact | string | name of decision-maker or representative |
| Contact email | string | primary email |
| Contact phone | string | primary phone |
| Inquiry source | enum | attribution for marketing ROI |
| Inquiry date | date | first contact date |
| Space need (SF) | int | stated requirement |
| Target move date | date | desired occupancy |
| Budget | float | stated budget per SF or monthly |
| Broker name | string | tenant-rep broker if represented |
| Broker company | string | brokerage firm |
| Current stage | enum | pipeline stage |
| Stage entry date | date | when prospect entered current stage |
| Last activity date | date | most recent interaction |
| Next action | string | scheduled follow-up |
| Next action date | date | deadline for next action |
| Assigned agent | string | responsible leasing agent |
| Notes | text | running log of interactions |

**Stage-specific fields**:

```
Tour Scheduled (add):
  Tour date/time: datetime
  Suites to show: list
  Attendees: list (prospect contacts + broker)
  Special requirements: text (ADA, parking, security)

Toured (add):
  Tour date completed: date
  Tour feedback: text (prospect's reaction, concerns, questions)
  Decision timeline: string (when will they decide?)
  Decision-maker identified: boolean
  Competing properties: list (which others are they touring?)
  Qualification score: int (1-5, see scoring matrix below)

Proposal (add):
  Proposal date sent: date
  Suite proposed: string
  Proposed rent: float
  Proposed term: int (months)
  Proposed TI: float
  Proposed concessions: string
  Proposal expiry date: date
  Counterproposal received: boolean
  Counter terms: text

LOI (add):
  LOI date executed: date
  LOI terms summary: text
  LOI expiry date: date
  Legal counsel (tenant): string
  Lease draft target date: date
  Deposit amount: float

Lease Out (add):
  Lease sent date: date
  Lease attorney (LL): string
  Lease attorney (tenant): string
  Outstanding comments: text
  Target execution date: date

Executed (add):
  Execution date: date
  Lease start date (commencement): date
  Rent commencement date: date
  Term months: int
  Annual rent: float
  TI allowance total: float
  Free rent months: int
  Security deposit received: boolean
  Commission due: float
  Commission paid: float
```

### Prospect Qualification Scoring

```
Score each factor 1-5, total determines qualification level:

Factor 1: Space Match (does our availability match their need?)
  5: Perfect match (size, condition, location within building)
  4: Good match (minor compromise needed)
  3: Acceptable match (prospect would need to adjust expectations)
  2: Marginal match (significant compromise)
  1: Poor match (our space doesn't really work)

Factor 2: Financial Qualification (can they afford it?)
  5: Budget exceeds asking rent by 10%+
  4: Budget matches asking rent
  3: Budget is 5-10% below asking (concession could bridge)
  2: Budget is 10-20% below asking (significant gap)
  1: Budget is 20%+ below asking (not viable without major concession)

Factor 3: Timeline (does their timeline match our availability?)
  5: Need space within 30 days (urgent, ready to decide)
  4: Need space in 1-3 months (active search)
  3: Need space in 3-6 months (planning ahead)
  2: Need space in 6-12 months (early stage)
  1: No defined timeline (browsing)

Factor 4: Decision Authority (are we talking to the decision-maker?)
  5: Decision-maker is directly involved in the search
  4: Decision-maker will tour and is engaged
  3: Decision-maker delegates but will approve
  2: Decision-maker is unknown or uninvolved
  1: Contact cannot make or influence the decision

Factor 5: Competitive Position (how do we compare to alternatives?)
  5: We are the top choice, prospect has said so
  4: We are a strong contender (top 2)
  3: We are one of several options
  2: We are a backup option
  1: Prospect prefers another property

Total score:
  20-25: HOT -- prioritize, move to proposal quickly
  15-19: WARM -- nurture, address gaps in scoring
  10-14: COOL -- maintain contact, lower priority
  5-9:   COLD -- unlikely to convert, minimal effort
```

---

## 2. Conversion Rate Benchmarks

### By Property Type

```
Office (Class A):
  Inquiry -> Tour:        30-40%
  Tour -> Proposal:       35-50%
  Proposal -> LOI:        25-40%
  LOI -> Executed:        75-85%
  Total (Inquiry -> Exec): 5-10%

Office (Class B):
  Inquiry -> Tour:        25-35%
  Tour -> Proposal:       30-45%
  Proposal -> LOI:        20-35%
  LOI -> Executed:        70-80%
  Total (Inquiry -> Exec): 3-7%

Retail (Inline):
  Inquiry -> Tour:        20-30%
  Tour -> Proposal:       25-35%
  Proposal -> LOI:        15-25%
  LOI -> Executed:        65-80%
  Total (Inquiry -> Exec): 2-5%

Industrial:
  Inquiry -> Tour:        35-45%
  Tour -> Proposal:       40-55%
  Proposal -> LOI:        30-45%
  LOI -> Executed:        80-90%
  Total (Inquiry -> Exec): 8-15%

Multifamily:
  Inquiry -> Tour:        40-55%
  Tour -> Application:    25-40%
  Application -> Approved: 70-85%
  Approved -> Lease:       85-95%
  Total (Inquiry -> Lease): 6-15%
```

### By Inquiry Source

```
Source quality ranking (highest to lowest conversion):

1. Broker referral:       Total conversion 8-15%
   Why: pre-qualified by broker, serious intent, understands market

2. Direct referral:       Total conversion 6-12%
   Why: warm introduction, trust transferred from referrer

3. Walk-in / signage:     Total conversion 5-10%
   Why: prospect is physically in the area, likely has specific interest

4. CoStar/LoopNet (paid): Total conversion 3-8%
   Why: active searchers, but also casting a wide net

5. Website (organic):     Total conversion 2-6%
   Why: mixed intent, some are early-stage research

6. Paid search (Google):  Total conversion 1-4%
   Why: broad audience, many not serious

7. Social media:          Total conversion 0.5-2%
   Why: brand awareness more than lead generation

8. Direct mail:           Total conversion 0.5-1.5%
   Why: low response rate, but respondents tend to be qualified
```

---

## 3. Velocity Metrics and Benchmarks

### Days in Stage

```
Average days by stage (commercial office):

| Stage | Target | Average | Slow (investigate) |
|---|---|---|---|
| Inquiry to Tour Scheduled | 3 days | 5 days | > 7 days |
| Tour Scheduled to Toured | 5 days | 7 days | > 14 days |
| Toured to Proposal | 7 days | 12 days | > 21 days |
| Proposal to LOI | 14 days | 25 days | > 45 days |
| LOI to Lease Out | 14 days | 21 days | > 30 days |
| Lease Out to Executed | 14 days | 28 days | > 45 days |
| Total Cycle | 57 days | 98 days | > 120 days |
```

### Absorption Rate Calculation

```
Absorption rate = SF leased per month (net of move-outs)

Formula:
  Gross absorption = new leases signed (SF) in the period
  Net absorption = gross absorption - lease expirations/terminations - move-outs

Example (rolling 12 months):
  New leases signed: 45,000 SF
  Lease expirations: 22,000 SF
  Early terminations: 3,000 SF
  Gross absorption: 45,000 SF
  Net absorption: 45,000 - 22,000 - 3,000 = 20,000 SF
  Monthly net absorption: 20,000 / 12 = 1,667 SF/month

Months to lease remaining vacancy:
  Available SF: 30,000
  Monthly net absorption: 1,667 SF
  Months to full occupancy: 30,000 / 1,667 = 18 months

If target is < 12 months, absorption pace is too slow.
Action: increase marketing spend, adjust pricing, or expand broker outreach.
```

---

## 4. Weekly Pipeline Report Template

### Worked Example

```
=================================================================
     WEEKLY LEASING PIPELINE REPORT
     250 Park Avenue
     Week Ending: March 14, 2026
     Prepared by: [Agent Name]
=================================================================

AVAILABLE INVENTORY:
  Total building SF:    200,000
  Available SF:         30,000 (15.0% vacancy)
  Under negotiation:    12,500 (Suites 1801 + 2205)
  Effective available:  17,500 (8.8% effective vacancy)

  Available Suites:
  | Suite | Floor | SF | Condition | Asking Rent | Days on Market |
  |---|---|---|---|---|---|
  | 1205 | 12 | 8,500 | Turn-key | $72.00/RSF | 45 |
  | 1801 | 18 | 5,200 | 2nd gen | $74.00/RSF | 62 (LOI) |
  | 2003 | 20 | 9,300 | Warm shell | $76.00/RSF | 28 |
  | 2205 | 22 | 7,000 | Turn-key | $78.00/RSF | 90 (Proposal) |

-----------------------------------------------------------------

NEW ACTIVITY THIS WEEK:
  New inquiries:          4
  Tours completed:        2
  Proposals sent:         1
  LOIs executed:          0
  Leases executed:        0

PIPELINE BY STAGE:
| Stage | Count | SF | Wtd Prob | Expected SF |
|---|---|---|---|---|
| Inquiry | 6 | 42,000 | 10% | 4,200 |
| Tour Scheduled | 3 | 21,500 | 15% | 3,225 |
| Toured | 4 | 28,000 | 25% | 7,000 |
| Proposal | 2 | 16,500 | 40% | 6,600 |
| LOI | 1 | 5,200 | 75% | 3,900 |
| Lease Out | 0 | 0 | 90% | 0 |
| TOTAL | 16 | 113,200 | | 24,925 |

Weighted pipeline (24,925 SF) covers 83% of available (30,000 SF).
Target: 2-3x coverage. Need additional qualified prospects.

-----------------------------------------------------------------

KEY DEALS:

1. TechVenture Inc. -- Suite 1801 (5,200 SF) -- LOI
   Contact: Sarah Chen (CEO)  |  Broker: JLL (Mike Torres)
   LOI executed 03/07. Terms: $72/RSF, 7-year, 6mo free, $75 TI.
   Lease draft being prepared. Target execution: 03/28.
   Risk: LOW. Decision-maker engaged, no competing offers.

2. GlobalHealth Partners -- Suite 2205 (7,000 SF) -- Proposal
   Contact: Dr. James Park  |  Direct (no broker)
   Proposal sent 03/10. $76/RSF, 10-year, 4mo free, $80 TI.
   Follow-up call 03/17. Prospect comparing to 300 Madison ($78).
   Risk: MEDIUM. Prospect has not toured 300 Madison yet.
   Action: invite for second tour with building engineer to discuss
           HVAC modifications for medical use.

3. Apex Consulting -- Suite 2003 (9,300 SF) -- Toured
   Contact: Lisa Wang (COO)  |  Broker: CBRE (Amy Zhao)
   Toured 03/12. Positive feedback on space and views. Concerned
   about warm shell condition and build-out timeline.
   Next step: prepare proposal with 2 TI scenarios (LL build-out
   vs. tenant build-out with higher TI allowance). Due 03/18.
   Risk: MEDIUM. 3 other buildings being toured this week.

-----------------------------------------------------------------

STALE PROSPECTS (no activity > 14 days):
| Prospect | Stage | Last Activity | Days Stale | Action |
|---|---|---|---|---|
| Meridian Group | Toured | 02/25 | 17 | Final follow-up call today |
| BlueWave Capital | Proposal | 02/28 | 14 | Broker follow-up scheduled |

-----------------------------------------------------------------

CONVERSION METRICS (rolling 90 days):
  Inquiry -> Tour:        33% (target: 35%) -- SLIGHTLY BELOW
  Tour -> Proposal:       42% (target: 40%) -- ON TARGET
  Proposal -> LOI:        28% (target: 30%) -- SLIGHTLY BELOW
  LOI -> Executed:        80% (target: 80%) -- ON TARGET
  Overall: 3.1% (target: 5%) -- BELOW TARGET

  Analysis: inquiry-to-tour conversion is the bottleneck. 4 of last
  12 inquiries were disqualified (budget mismatch). Consider adjusting
  CoStar listing to show rent range rather than "contact for pricing"
  to pre-qualify online leads.

-----------------------------------------------------------------

MARKETING SPEND (MTD March):
| Channel | Spend | Inquiries | Cost/Inquiry | Tours | Cost/Tour |
|---|---|---|---|---|---|
| CoStar | $2,400 | 6 | $400 | 2 | $1,200 |
| LoopNet | $800 | 2 | $400 | 0 | N/A |
| Website SEO | $500 | 3 | $167 | 1 | $500 |
| Broker events | $1,200 | 4 | $300 | 2 | $600 |
| Signage | $0 | 1 | $0 | 1 | $0 |
| TOTAL | $4,900 | 16 | $306 | 6 | $817 |

  Best channel (cost/tour): Signage ($0) and Broker events ($600)
  Worst channel: LoopNet ($800, 0 tours from 2 inquiries)
  Action: evaluate LoopNet ROI at quarter-end. Consider reallocating
  to additional broker co-op events.

=================================================================
```
