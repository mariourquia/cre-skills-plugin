# Vendor Management Framework

## Overview

This framework covers the full vendor lifecycle for property management operations: onboarding, contract tracking, performance evaluation, insurance compliance, competitive bidding, cost benchmarking, and vendor replacement. It applies to all service categories including janitorial, landscaping, security, HVAC maintenance, elevator service, fire/life safety, pest control, snow removal, and specialty trades.

## Contract Tracking Fields

Maintain a vendor registry with the following fields for every active vendor:

| Field | Description |
|---|---|
| Vendor Name | Legal entity name |
| DBA / Trade Name | Operating name if different |
| Service Category | Primary service (janitorial, HVAC, elevator, etc.) |
| Contract Type | Fixed price, time & materials, GMP, cost-plus |
| Contract Start Date | Effective date |
| Contract End Date | Expiration date |
| Auto-Renewal | Yes/No; if yes, notice period to cancel |
| Notice Period (days) | Days before expiration to give non-renewal notice |
| Annual Contract Value | Base contract amount |
| Payment Terms | Net 30, Net 15, etc. |
| Scope of Work Summary | One-paragraph scope description |
| Performance Bond | Required Y/N; amount if yes |
| Retainage | Percentage withheld; release conditions |
| Primary Contact | Name, phone, email |
| Emergency Contact | 24/7 contact for after-hours emergencies |
| Insurance Requirements | GL limit, WC, auto, umbrella per contract |
| COI Expiration Date | Current certificate of insurance expiration |
| Additional Insured | Property entity listed as additional insured Y/N |
| Waiver of Subrogation | Included Y/N |
| W-9 on File | Y/N |
| License / Certification | Required licenses and current status |
| Last Performance Review | Date of most recent scorecard |
| Current Score | Weighted composite score (1.0-5.0) |
| Notes | Special terms, known issues, renewal strategy |

**Alert Triggers:**
- Contract expiring within 90 days: initiate renewal or rebid decision
- COI expiring within 30 days: send renewal request to vendor
- Score below 3.0: initiate Performance Improvement Plan
- Score below 2.5: initiate replacement process

## Performance Scorecard Methodology

Score each vendor quarterly using five weighted categories. Scores are on a 1.0-5.0 scale.

### Scoring Categories

| Category | Weight | 5.0 (Excellent) | 3.0 (Acceptable) | 1.0 (Unacceptable) |
|---|---|---|---|---|
| **Quality of Work** | 30% | Zero deficiencies, zero callbacks, positive tenant feedback | Occasional deficiency, <5% callback rate, no complaints | Repeated deficiencies, >10% callbacks, tenant complaints |
| **Responsiveness** | 25% | Responds within 1 hour, emergency available 24/7, proactive communication | Responds within contract SLA, generally available, reactive communication | Missed SLA >10% of time, unreachable during emergencies |
| **Cost Control** | 20% | At or below contract pricing, zero unauthorized extras, competitive vs. market | Within 5% of contract pricing, <3 change orders/year | Frequent overcharges, >5 unauthorized extras, above market |
| **Safety & Compliance** | 15% | Zero OSHA incidents, all insurance current, all licenses active, full background checks | Minor documentation gaps, quickly remediated | OSHA recordable, lapsed insurance, expired licenses |
| **Partnership** | 10% | Proactive improvement suggestions, flexible on scheduling, strong relationship | Cooperative, meets obligations, professional | Adversarial, inflexible, poor communication |

### Composite Score Calculation

```
Composite = (Quality x 0.30) + (Responsiveness x 0.25) + (Cost x 0.20) + (Safety x 0.15) + (Partnership x 0.10)
```

### Score Thresholds and Actions

| Composite Score | Rating | Action |
|---|---|---|
| 4.5 - 5.0 | Exceptional | Preferred vendor status; consider contract extension |
| 3.5 - 4.4 | Good | Standard renewal; no action required |
| 3.0 - 3.4 | Acceptable | Monitor closely; note improvement areas |
| 2.5 - 2.9 | Below Standard | Performance Improvement Plan (30-60 days) |
| Below 2.5 | Unacceptable | Initiate replacement; begin bid process |

## Insurance Compliance Checklist

Before any vendor begins work on property, verify the following:

- [ ] Certificate of Insurance (COI) received and on file
- [ ] General Liability: minimum $1M per occurrence / $2M aggregate (or per contract requirement)
- [ ] Workers' Compensation: statutory limits for state of operations
- [ ] Commercial Auto Liability: minimum $1M combined single limit (if vehicles on property)
- [ ] Umbrella / Excess Liability: per contract requirement (typically $5M for large contracts)
- [ ] Professional Liability / E&O: per contract requirement (for consultants, engineers)
- [ ] Property owner entity named as Additional Insured on GL and Umbrella policies
- [ ] Waiver of Subrogation in favor of property owner on GL and WC policies
- [ ] 30-day notice of cancellation endorsement
- [ ] Policy dates cover the full contract period
- [ ] Certificate holder name and address correct
- [ ] No exclusions that would void coverage for contracted scope of work

**Non-Compliant Vendor Protocol:**
1. Send deficiency notice specifying missing or inadequate coverage
2. Allow 10 business days to cure
3. If not cured: suspend work authorization pending compliance
4. If COI compliance cannot be achieved: escalate to coi-compliance-checker for detailed analysis

## Bid Process Steps

For contracts exceeding $25,000 annually or any service being competitively bid:

1. **Scope Development** (Week 1)
   - Draft detailed scope of work with measurable performance standards
   - Include property-specific requirements (hours, staffing, equipment, materials)
   - Define reporting and inspection requirements
   - Specify insurance and licensing requirements
   - Include sample scorecard so bidders understand evaluation criteria

2. **Bidder Identification** (Week 1-2)
   - Include current incumbent vendor (if rebidding)
   - Identify 2-4 additional qualified firms from: BOMA directory, IREM referrals, peer property manager recommendations, trade associations
   - Pre-qualify bidders: confirm licensing, insurance capacity, relevant experience, references

3. **Bid Distribution and Q&A** (Week 2-3)
   - Distribute RFP to all qualified bidders simultaneously
   - Schedule mandatory property walk-through for all bidders
   - Establish Q&A period with responses distributed to all bidders
   - Set firm bid deadline (typically 2-3 weeks after distribution)

4. **Bid Evaluation** (Week 4)
   - Create comparison matrix with standardized format
   - Evaluate on: base price, unit rates, included/excluded items, staffing plan, equipment, insurance, references, transition plan
   - Check references (minimum 3 per bidder)
   - Normalize pricing to compare apples-to-apples

5. **Selection and Award** (Week 5)
   - Recommend award with written justification (lowest cost is not always the recommendation)
   - Obtain owner/asset manager approval
   - Negotiate final terms
   - Execute contract with all required exhibits (scope, insurance, scorecard)

6. **Transition** (Week 5-8)
   - 30-day transition period for outgoing/incoming vendor overlap
   - Knowledge transfer: key contacts, property-specific procedures, equipment locations, tenant preferences
   - Update all vendor tracking records, emergency contacts, and access credentials

## Cost Benchmarking Approach

Compare vendor pricing against market benchmarks using the following sources and methodology:

1. **Primary Benchmarks**: BOMA Experience Exchange Report and IREM Income/Expense Analysis for the property's asset type, class, size range, and region.
2. **Secondary Benchmarks**: Recent bids received for comparable scopes at peer properties in the same market.
3. **Benchmark Comparison**: Calculate vendor cost per SF (or per unit for multifamily) by service category and compare to the benchmark median and quartile range.
4. **Acceptable Range**: Within 15% of benchmark median is considered competitive. Flag any category exceeding benchmark by >15% for rebid or renegotiation.
5. **Below-Benchmark Caution**: Costs significantly below benchmark (<75% of median) may indicate scope gaps, understaffing, or quality concerns. Verify scope alignment before celebrating savings.

## Vendor Replacement Triggers

Initiate vendor replacement when any of the following occur:

- Composite scorecard drops below 2.5 after a Performance Improvement Plan period
- OSHA recordable incident caused by vendor negligence
- Lapsed insurance not cured within 10 business days
- Material breach of contract (scope abandonment, unauthorized subcontracting, theft)
- Repeated billing disputes (>3 in 12 months) indicating systemic pricing integrity issues
- Loss of required license or certification
- Vendor voluntarily exits the market or declares bankruptcy
- Cost exceeds benchmark by >25% and vendor refuses to negotiate
