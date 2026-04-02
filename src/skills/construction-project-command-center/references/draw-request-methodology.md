# Construction Draw Request Verification Methodology

Step-by-step verification process for construction loan draw requests. Covers schedule of values review, percentage complete verification, lien waiver collection, retainage tracking, stored materials, and lender inspector coordination. Worked example uses a $45M, 200-unit ground-up multifamily project with monthly draws.

---

## 1. Schedule of Values (SOV) Review

### Structure

The SOV is the line-item budget that governs all draw requests. Established at the start of construction, it must:

1. **Match the contract**: every contract line item has a corresponding SOV line
2. **Sum correctly**: total of all line items = contract amount (GMP or lump sum)
3. **Reasonable allocation**: no front-loading (disproportionate value assigned to early work)
4. **Sufficient granularity**: major trades broken into subcomponents (e.g., "Concrete" broken into foundations, slabs, columns, walls)

### Front-Loading Detection

Front-loading occurs when a contractor assigns inflated values to early SOV items to draw more cash upfront. Detection methods:

```
Method 1: Percentage of total vs physical scope
  If "Mobilization" = 3% of contract but typical is 0.5-1.5%, likely front-loaded.
  If "Foundations" = 12% of contract but foundations represent 6-8% of hard costs
  by RSMeans for this building type, investigate.

Method 2: Early draw velocity
  If cumulative draws at 20% schedule completion exceed 25% of contract value,
  evaluate whether physical progress supports the draws.

Method 3: Unit cost comparison
  Calculate implied unit costs from SOV allocation:
    SOV line "Cast-in-place concrete": $3,200,000
    Estimated concrete volume: 4,800 CY
    Implied unit cost: $667/CY
    RSMeans range for structural concrete (form, rebar, place, finish): $450-750/CY
    Result: within range, but high end. Acceptable.
```

### SOV Approval Checklist

- [ ] All contract line items represented
- [ ] Total matches contract amount exactly
- [ ] No single line item > 15% of total unless justified by scope (e.g., structural steel for a high-rise)
- [ ] General conditions line reasonable (typically 8-12% of hard costs)
- [ ] Contingency shown as a separate line (not distributed across trades)
- [ ] Soft costs (if included) match approved soft cost budget
- [ ] Retainage calculation methodology documented
- [ ] Line item numbering matches AIA G703 format

---

## 2. Percentage Complete Verification

### Methods

| Method | When to Use | Accuracy |
|---|---|---|
| Physical observation | All trades, every draw | High (if inspector is qualified) |
| Quantity-based | Concrete, steel, framing, drywall | Very high |
| Milestone-based | Mechanical, electrical, plumbing | Medium-high |
| Expenditure-based | Soft costs, GC general conditions | Medium |

### Physical Observation Protocol

For each SOV line item claimed at > 0% in the current draw:

1. **Site walk**: verify work in place matches claimed percentage
2. **Photo documentation**: dated photos showing completed work by area
3. **Quantity verification**: for measurable items (e.g., linear feet of piping, square feet of drywall), field-measure a representative sample (minimum 10% of installed quantity)
4. **Quality check**: is the work installed per specifications? Defective work does not count toward completion

### Common Overstatement Patterns

```
Pattern: "Rough-in at 90%" when connections and testing are incomplete.
Reality: Rough-in without testing is 70-75% complete. Testing, corrections,
         and final connections are the remaining 25-30%.

Pattern: "MEP complete" before commissioning.
Reality: MEP installation without startup, testing, and balancing is 85%
         at best. Commissioning is 10-15% of total MEP scope.

Pattern: "Drywall 100%" when taping and finishing remain.
Reality: Drywall hung but unfinished is approximately 55-60% of total
         drywall scope (hang, tape, finish, sand, prime).

Pattern: General conditions claimed at straight-line percentage.
Reality: GC general conditions should track overall project completion,
         not calendar time. If project is 40% complete at month 8 of 18,
         general conditions should be 40%, not 44% (8/18).
```

### Percentage Complete Verification Table (Worked Example, Draw #8)

```
Draw #8 -- Period ending 2026-08-31
Project: 200-unit multifamily, $45M total ($32.5M hard costs)

| SOV Line | SOV Amount | Prior % | This Period % | Cumul % | This Draw | Cumul Billed | Retainage |
|---|---|---|---|---|---|---|---|
| 01 - General Conditions | $3,250,000 | 38% | 5% | 43% | $162,500 | $1,397,500 | $139,750 |
| 02 - Sitework | $2,100,000 | 85% | 5% | 90% | $105,000 | $1,890,000 | $94,500 |
| 03 - Concrete | $4,800,000 | 72% | 8% | 80% | $384,000 | $3,840,000 | $384,000 |
| 04 - Masonry | $1,650,000 | 40% | 12% | 52% | $198,000 | $858,000 | $85,800 |
| 05 - Structural Steel | $3,200,000 | 95% | 3% | 98% | $96,000 | $3,136,000 | $156,800 |
| 06 - Rough Carpentry | $2,400,000 | 50% | 10% | 60% | $240,000 | $1,440,000 | $144,000 |
| 07 - Roofing | $980,000 | 0% | 15% | 15% | $147,000 | $147,000 | $14,700 |
| 08 - Doors/Windows | $1,800,000 | 20% | 15% | 35% | $270,000 | $630,000 | $63,000 |
| 09 - Drywall/Plaster | $2,600,000 | 10% | 8% | 18% | $208,000 | $468,000 | $46,800 |
| 10 - Flooring | $1,200,000 | 0% | 0% | 0% | $0 | $0 | $0 |
| 11 - Painting | $850,000 | 0% | 0% | 0% | $0 | $0 | $0 |
| 12 - HVAC | $3,100,000 | 25% | 10% | 35% | $310,000 | $1,085,000 | $108,500 |
| 13 - Plumbing | $2,400,000 | 30% | 8% | 38% | $192,000 | $912,000 | $91,200 |
| 14 - Electrical | $2,800,000 | 22% | 8% | 30% | $224,000 | $840,000 | $84,000 |
| 15 - Fire Protection | $1,100,000 | 15% | 10% | 25% | $110,000 | $275,000 | $27,500 |
| 16 - Elevator | $1,600,000 | 5% | 5% | 10% | $80,000 | $160,000 | $16,000 |
| 17 - Specialties | $670,000 | 0% | 0% | 0% | $0 | $0 | $0 |
| TOTALS | $32,500,000 | | | | $2,726,500 | $17,078,500 | $1,456,550 |

Summary:
  Gross billing this period:    $2,726,500
  Less retainage (10%):          -$272,650
  Net draw this period:         $2,453,850
  Cumulative gross billed:      $17,078,500
  Cumulative retainage held:    $1,456,550 (retainage reduced to 5% after 50%
                                             completion -- applies next draw)
  Net amount funded to date:    $15,621,950
  Remaining to bill:            $15,421,500
```

---

## 3. Lien Waiver Collection

### Waiver Types

| Type | When Required | What It Covers |
|---|---|---|
| Conditional Progress | With current draw request | Current draw amount, conditional on receipt of payment |
| Unconditional Progress | With next draw request | Prior draw amount, confirms payment was received |
| Conditional Final | With final draw request | Final payment amount, conditional on receipt |
| Unconditional Final | After final payment clears | Entire contract amount, irrevocable release |

### Collection Matrix

```
Draw #8 Requirements:

From GC:
  [x] Conditional progress waiver for Draw #8 ($2,453,850)
  [x] Unconditional progress waiver for Draw #7 ($2,180,000)

From each subcontractor with contract > $10,000:
  [x] Conditional progress waiver for current billing
  [x] Unconditional progress waiver for prior period billing

Lien Waiver Tracker (excerpt):

| Subcontractor | Contract | Draw 7 Unconditional | Draw 8 Conditional | Status |
|---|---|---|---|---|
| ABC Concrete | $4,800,000 | RECEIVED 08/15 | RECEIVED 08/28 | CLEAR |
| XYZ Mechanical | $3,100,000 | RECEIVED 08/18 | RECEIVED 08/30 | CLEAR |
| DEF Electrical | $2,800,000 | RECEIVED 08/16 | MISSING | HOLD |
| GHI Plumbing | $2,400,000 | RECEIVED 08/14 | RECEIVED 08/29 | CLEAR |
| JKL Steel | $3,200,000 | RECEIVED 08/12 | RECEIVED 08/27 | CLEAR |

Action: DEF Electrical conditional waiver missing. HOLD $224,000 from draw
        until received. Notify GC -- 48-hour deadline before draw submission.
```

### Mechanic's Lien Exposure

```
Jurisdiction: New York (varies significantly by state)

Filing deadline: 8 months from last work performed (private improvement)
Notice requirement: depends on sub tier (direct subs typically exempt,
                    lower-tier subs may need preliminary notice)
Priority: relates back to first visible work on site
Amount: limited to amount owed on the contract (not the full contract value)

Risk mitigation:
  1. Collect waivers every draw cycle without exception
  2. Verify GC is paying subs within 7 days of draw receipt (payment affidavit)
  3. For subs > $100,000, verify sub-subcontractor and supplier payments
  4. Joint-check agreements for problematic subs or subs in financial distress
  5. Title search at substantial completion before final draw
```

---

## 4. Retainage Tracking

### Standard Retainage Schedule

```
Retainage Structure (typical construction loan):

Phase 1: 0% to 50% complete
  Retainage rate: 10% of each progress payment
  Purpose: ensure contractor has sufficient incentive to complete work

Phase 2: 50% to substantial completion
  Retainage rate: 5% of each progress payment (reduced rate)
  Condition: no outstanding defaults, schedule on track, lender approval

Phase 3: Substantial completion to final completion
  Retainage rate: 0% on new billings
  Release: 50% of retained amount at substantial completion
  Hold: remaining 50% until punch list completion + final waivers

Phase 4: Final completion
  Release: remaining retainage upon:
    - All punch list items verified complete
    - Final unconditional lien waivers from all parties
    - As-built documents received
    - O&M manuals received
    - All warranties received
    - Final certificate of occupancy issued
```

### Retainage Tracking Table

```
Retainage Summary -- Draw #8

Total billed to date:           $17,078,500
Retainage at 10% (Draws 1-7):   $1,183,900
Retainage at 10% (Draw 8):        $272,650
Total retainage held:            $1,456,550

Retainage by trade:
| Trade | Billed | Retainage | % of Trade Billed |
|---|---|---|---|
| Concrete | $3,840,000 | $384,000 | 10.0% |
| Structural Steel | $3,136,000 | $156,800 | 5.0% (reduced at 95% complete) |
| HVAC | $1,085,000 | $108,500 | 10.0% |
| ... | | | |

Note: Structural steel retainage reduced to 5% at Draw #6 when trade reached
50% complete, per lender approval dated 2026-06-15. All other trades remain at
10% until they individually reach 50% complete.
```

---

## 5. Stored Materials Verification

### Eligibility Requirements

Stored materials may be included in a draw request if:

1. **On-site storage**: materials are on the project site, properly protected from weather and damage
2. **Off-site storage** (requires lender approval): materials at a bonded warehouse or fabrication facility with:
   - Bill of sale transferring title to the owner
   - Insurance certificate covering stored materials (builder's risk or inland marine)
   - Warehouse agreement or fabrication contract
   - Periodic inventory verification (photos + count)

### Verification Checklist

```
Stored Materials Claim -- Draw #8

| Item | Location | Quantity | Unit Cost | Total Value | Documentation |
|---|---|---|---|---|---|
| Windows (Marvin) | On-site lay-down | 340 units | $1,200 | $408,000 | Invoice + delivery receipt |
| Elevator cab panels | Fabricator (Ohio) | 4 sets | $28,000 | $112,000 | Bill of sale + insurance |
| HVAC units (Carrier) | On-site | 12 units | $8,500 | $102,000 | Invoice + photos |

Verification:
  [x] Windows: counted on-site 08/28, matches claim (340 units), stored on
      pallets under tarps in designated lay-down area. Photos attached.
  [x] Elevator panels: fabricator warehouse inspection report dated 08/25.
      Bill of sale transferring title to owner on file. Insurance certificate
      names owner and lender as additional insured. APPROVED for off-site billing.
  [x] HVAC units: counted on-site 08/29, 12 units on concrete pad with
      protective covers. Serial numbers match purchase order.

Total stored materials this draw: $622,000
Less retainage (10%): -$62,200
Net stored materials draw: $559,800
```

---

## 6. Lender Inspector Coordination

### Inspection Triggers

```
Mandatory inspection (per typical construction loan agreement):

1. Every monthly draw > $250,000
2. Foundation completion milestone
3. Structural topping-out milestone
4. Substantial completion milestone
5. Any draw that brings cumulative funding > 50% of total commitment
6. At lender's discretion upon notice of delay, dispute, or cost overrun

Inspector scope:
  - Verify physical completion matches draw percentages
  - Confirm stored materials on-site
  - Assess overall construction quality
  - Report any observed safety concerns
  - Note any deviation from approved plans
  - Provide independent % complete estimate by trade
```

### Variance Resolution

```
When lender inspector % differs from GC % by more than 5 percentage points:

1. Identify the specific line items in disagreement
2. Request inspector's written basis for lower percentage
3. Arrange joint site walk: GC super + PM + inspector
4. Reach consensus on adjusted percentage
5. Process draw at agreed-upon percentage
6. Document resolution for audit trail

If variance cannot be resolved:
  - Draw processes at the lower of GC or inspector percentage
  - Disputed amount held pending next inspection
  - GC may request supplemental draw if resolved before next cycle
```

---

## 7. Draw Certification Package Checklist

### Complete Draw Package Contents

```
Draw #8 -- Certification Checklist

Required Documents:
  [x] AIA G702 - Application and Certificate for Payment
  [x] AIA G703 - Continuation Sheet (schedule of values detail)
  [x] GC sworn statement / contractor's affidavit
  [x] GC conditional lien waiver (current draw)
  [x] GC unconditional lien waiver (prior draw)
  [x] Sub conditional lien waivers (current -- all subs > $10,000)
  [x] Sub unconditional lien waivers (prior -- all subs > $10,000)
  [x] Stored materials documentation (invoices, photos, insurance)
  [x] Progress photos (dated, organized by area)
  [x] Lender inspection report (if applicable)

Supporting Documents:
  [x] Updated construction schedule (2-week lookahead minimum)
  [x] Change order log (current through this draw period)
  [x] RFI log status (open items summary)
  [x] Safety incident log (this period)
  [x] Insurance certificate confirmations (all current)

Certification:
  Owner representative certifies that:
  1. Work represented in this draw has been verified by site observation
  2. Quantities and percentages are consistent with physical progress
  3. All required lien waivers have been collected
  4. Retainage has been calculated correctly
  5. No known defaults or uncured notices exist

  Signature: _________________________  Date: ______________

Draw Summary:
  Gross amount due:           $2,726,500
  Less retainage held:          -$272,650
  Less outstanding waivers:     -$224,000 (DEF Electrical)
  Net amount certified:       $2,229,850
  Wire transfer instructions: [per loan agreement]
```
