# Event ROI Model

Quantitative framework for measuring return on investment from tenant event programming in CRE properties.

## Core Premise

Tenant events are not a cost center. They are a retention tool with measurable financial impact. The primary ROI driver is avoided turnover cost. Secondary drivers include referral value, rent premium sustainability, and reduced vacancy loss.

## ROI Formula

```
ROI = (Avoided Turnover Cost + Referral Value + Rent Premium Retention) / Total Event Cost

Where:
  Avoided Turnover Cost = Incremental Retained Units * Avg Turnover Cost Per Unit
  Referral Value = New Leases Attributed to Events * Avg Lease Commission Saved
  Rent Premium Retention = Units Retaining Premium * Annual Premium Delta
  Total Event Cost = Direct Event Spend + Staff Time Cost + Opportunity Cost of Space
```

## Component Calculations

### Avoided Turnover Cost

The largest ROI component. Each avoided turnover eliminates make-ready, vacancy loss, and leasing costs.

**Average Turnover Cost by Property Type:**

| Property Type | Make-Ready | Vacancy Loss (avg days) | Leasing/Marketing | Total Turnover Cost |
|---|---|---|---|---|
| MF Class A | $1,500-2,500 | $2,000-4,000 (30-45 days) | $500-1,000 | $4,000-7,500 |
| MF Class B | $800-1,500 | $1,200-2,500 (25-40 days) | $400-800 | $2,400-4,800 |
| MF Class C | $500-1,000 | $800-1,500 (20-30 days) | $300-600 | $1,600-3,100 |
| Office Class A | N/A | $15-30/SF (60-120 days) | $5-10/SF TI + commission | $20-40/SF |
| Office Class B | N/A | $10-20/SF (90-180 days) | $3-8/SF TI + commission | $13-28/SF |

**Retention Rate Impact:**

Industry data shows consistent tenant event programming (4+ events/year) correlates with:
- Multifamily: 3-8 percentage point improvement in annual retention rate
- Office: 2-5 percentage point improvement in lease renewal rate

Conservative modeling should use the low end of these ranges.

**Incremental Retained Units Calculation:**

```
Incremental Retained Units = Total Units * Retention Rate Improvement

Example:
  200-unit MF property
  Baseline turnover: 45% (90 units/year turn over)
  With events: 40% turnover (80 units/year)
  Incremental retained: 10 units
```

### Referral Value

Event-attending tenants are more likely to refer friends/colleagues. Referrals reduce leasing cost and typically have higher retention themselves.

```
Referral Value = Referrals Attributed to Events * (Avg Leasing Cost - Referral Bonus)

Example:
  200-unit MF, 8 referral leases/year attributed to community feel
  Avg leasing cost avoided: $600/unit
  Referral bonus paid: $200/unit
  Referral Value = 8 * ($600 - $200) = $3,200
```

### Rent Premium Retention

Properties with active community programming can sustain higher rents relative to comps. Events contribute to a perception of value that supports premium pricing.

```
Rent Premium Retention = Units at Premium * Monthly Premium * 12

Example:
  Property achieves $25/month premium over comp set, partially attributable to amenity programming
  Attribute 30% of premium to events: $7.50/month/unit
  200 units * $7.50 * 12 = $18,000/year
```

This is the hardest component to isolate. Use conservatively or omit if attribution data is weak.

### Total Event Cost

```
Total Event Cost = Direct Spend + Staff Time + Space Opportunity Cost

Direct Spend: Sum of all event budgets for the year
Staff Time: Hours spent on event planning/execution * loaded hourly rate
  Typical: 15-25 hours per major event, 5-10 hours per minor event
  Property manager loaded rate: $35-55/hour
Space Opportunity Cost: Revenue forgone if event space could have been rented
  Usually $0 for common areas; may apply to bookable amenity spaces
```

## Worked Examples

### Example 1: 200-Unit Class B Multifamily

**Annual Event Program:**
| Event | Frequency | Cost Per | Annual Cost |
|---|---|---|---|
| Tenant appreciation BBQ | 2x/year | $2,000 | $4,000 |
| Holiday party | 1x/year | $3,500 | $3,500 |
| Food truck Friday | 10x/summer | $800 | $8,000 |
| Movie night | 4x/summer | $1,500 | $6,000 |
| Pet event | 2x/year | $1,000 | $2,000 |
| Welcome packages | ~80/year | $75 | $6,000 |
| Misc (decorations, small events) | Ongoing | -- | $2,500 |
| **Total Direct** | | | **$32,000** |
| Staff time (est. 200 hours) | | $45/hr | $9,000 |
| **Total All-In** | | | **$41,000** |

**Cost per unit**: $41,000 / 200 = $205/unit/year ($17/unit/month)

**ROI Calculation:**
```
Baseline turnover: 48% = 96 units/year
With events: 43% = 86 units/year (conservative 5pp improvement)
Incremental retained: 10 units
Avg turnover cost: $3,200/unit (Class B)

Avoided Turnover Cost: 10 * $3,200 = $32,000
Referral Value: 6 referrals * $400 net savings = $2,400
Rent Premium Retention: Conservative $0 (not attributed)

Total Benefit: $34,400
Total Cost: $41,000

ROI = $34,400 / $41,000 = 0.84x (first-year payback not yet achieved)
```

Note: This property is spending above the Class B benchmark ($40-60/unit). Trimming to $30,000 ($150/unit):
```
ROI = $34,400 / $30,000 = 1.15x
```

Lesson: Spend within benchmarks. Over-programming does not proportionally increase retention.

### Example 2: 200-Unit Class A Multifamily (Optimized)

**Annual Event Program: $12,000 total ($60/unit)**

```
Baseline turnover: 40% = 80 units/year
With events: 36% = 72 units/year (4pp improvement)
Incremental retained: 8 units
Avg turnover cost: $5,250/unit (Class A)

Avoided Turnover Cost: 8 * $5,250 = $42,000
Referral Value: 5 * $500 = $2,500
Rent Premium Retention: 200 * $5/month * 12 = $12,000

Total Benefit: $56,500
Total Cost: $12,000 + $6,000 (staff) = $18,000

ROI = $56,500 / $18,000 = 3.14x
```

Class A properties see stronger ROI because turnover costs are higher, and tenants have more alternatives, making community a genuine differentiator.

### Example 3: 150,000 SF Class A Office (50 Tenant Companies)

**Annual Event Program: $20,000 total ($400/tenant company, ~$18/occupant for 1,100 occupants)**

```
Baseline renewal rate: 70% (15 leases expiring, 10.5 renew)
With events: 74% (11.1 renew)
Incremental retained: ~1 tenant (rounding from 0.6)
Avg turnover cost: 5,000 SF avg suite * $30/SF = $150,000

Avoided Turnover Cost: 1 * $150,000 = $150,000
Referral Value: Minimal for office
Rent Premium: Conservative $0

Total Benefit: $150,000
Total Cost: $20,000 + $8,000 (staff) = $28,000

ROI = $150,000 / $28,000 = 5.36x
```

Office ROI is disproportionately high because a single avoided turnover justifies years of events. Even a fractional improvement in renewal probability delivers outsized returns.

## Spending Benchmarks

### Recommended Annual Budget by Property Class

| Segment | Budget/Unit or Tenant/Year | Events/Year | ROI Range |
|---|---|---|---|
| MF Class A | $60-80/unit | 8-12 | 2.5-4.0x |
| MF Class B | $40-60/unit | 6-8 | 1.0-2.0x |
| MF Class C | $25-40/unit | 4-6 | 0.8-1.5x |
| Office Class A | $15-25/tenant occupant | 6-8 | 3.0-6.0x |
| Office Class B | $8-15/tenant occupant | 4-6 | 2.0-4.0x |
| Mixed-Use | $50-70/unit equivalent | 6-10 | 1.5-3.0x |

### Diminishing Returns Curve

Event spending ROI follows a curve with a clear inflection point:

```
Spending Level         | Marginal Retention Benefit
$0-25/unit/year       | High (+2-4pp per $10 spent)
$25-60/unit/year      | Moderate (+1-2pp per $10 spent)
$60-100/unit/year     | Low (+0.5-1pp per $10 spent)
$100+/unit/year       | Minimal (<0.5pp per $10 spent)
```

The sweet spot for most properties is $40-80/unit/year. Spending above $100/unit/year rarely produces incremental retention benefit and should only be pursued for Class A luxury properties where the competitive set demands it.

## Measurement Implementation

### Required Data Collection

To run this model for a specific property, collect:
1. Current annual turnover rate (trailing 12 months)
2. Average turnover cost (actual or estimated from components)
3. Current event spending (trailing 12 months)
4. Event attendance data (per-event headcount)
5. Tenant survey data (satisfaction, NPS, event feedback)
6. Referral tracking data (leases attributed to referrals)

### Attribution Methodology

The hardest part of event ROI is attribution. Recommended approach:
1. Compare renewal rates of event attendees vs. non-attendees (control group)
2. Track renewal rates before and after event program launch (time series)
3. Include "community/events" as an option on move-out surveys
4. Include "community/events" as an option on leasing lead source surveys
5. A/B test: if managing multiple similar properties, run event program at some but not others

### Reporting Cadence

- **Monthly**: Attendance metrics, budget tracking, upcoming event pipeline
- **Quarterly**: Satisfaction survey results, retention rate trending, cost-per-attendee analysis
- **Annually**: Full ROI calculation, benchmark comparison, program optimization recommendations
