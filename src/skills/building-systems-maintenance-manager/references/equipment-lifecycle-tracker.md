# Equipment Lifecycle Tracker Reference

Major system tracking methodology, condition scoring criteria, remaining life estimation, replacement reserve calculation, and capital planning integration. Worked example uses a 200-unit Class B multifamily property, built 2008, in ASHRAE Climate Zone 4A (NYC metro).

---

## 1. Condition Scoring Methodology

### 5-Point Scale Definition

| Score | Rating | Definition | Action Required |
|---|---|---|---|
| 5 | Excellent | Like-new condition. Recently installed or renovated. No deficiencies. Full remaining useful life expected. | Standard PM only. |
| 4 | Good | Normal wear for age. Minor cosmetic issues. Fully functional. Expected to reach full useful life with proper maintenance. | Standard PM. Budget for replacement at EUL. |
| 3 | Fair | Noticeable wear. Occasional repairs beyond routine PM. Functional but some components approaching end of life. May not reach full EUL without increased maintenance spend. | Increased monitoring. Begin replacement planning. Budget for replacement 2-5 years ahead of EUL. |
| 2 | Poor | Significant deterioration. Frequent breakdowns. Repairs becoming costly relative to replacement. Reliability concerns. Will not reach full EUL. | Active replacement planning. Obtain pricing. Budget for replacement within 1-2 years. |
| 1 | Critical | Failed or at imminent risk of failure. Safety concerns possible. Cannot reliably serve its function. Emergency replacement risk. | Immediate replacement. Emergency funding if not budgeted. |

### Scoring Guidelines by System

**HVAC (RTU/Split System)**:
```
Score 5: Age 0-5 years, no refrigerant additions, all components original, meets efficiency specs.
Score 4: Age 5-12 years, < 1 refrigerant addition, minor component replacements (capacitors, contactors), meets efficiency specs.
Score 3: Age 12-17 years, 1-2 refrigerant additions, compressor running but amp draw elevated, coils have minor corrosion, efficiency declining.
Score 2: Age 17-22 years, frequent refrigerant additions (suspected leak), compressor amp draw > 110% nameplate, multiple component failures per year, efficiency < 80% of rated.
Score 1: Age 20+ years, compressor failed or imminent, major refrigerant leak, parts unavailable, no longer economical to repair.
```

**Boiler**:
```
Score 5: Age 0-10 years, no section failures, water chemistry maintained, passes annual inspection without findings.
Score 4: Age 10-20 years, no section failures, minor findings on annual inspection (gasket replacement, minor refractory repair), water chemistry maintained.
Score 3: Age 20-27 years, 1 section replacement, burner requires frequent adjustment, annual inspection findings require more than minor repairs, efficiency declining.
Score 2: Age 25-32 years, multiple section replacements, significant corrosion visible, annual inspection findings include safety-related items, parts becoming scarce.
Score 1: Age 30+ years, section failure imminent, safety device issues, fails annual inspection, or manufacturer no longer supports.
```

**Elevator**:
```
Score 5: Age 0-10 years (since last modernization), < 2 callbacks/month, 0 entrapments, > 99.5% uptime.
Score 4: Age 10-18 years, 2-4 callbacks/month, < 1 entrapment/year, > 99% uptime.
Score 3: Age 18-23 years, 4-6 callbacks/month, 1-2 entrapments/year, 97-99% uptime, some code violations at inspection.
Score 2: Age 23-28 years, > 6 callbacks/month, > 2 entrapments/year, < 97% uptime, multiple code violations, controller obsolete.
Score 1: Age 28+ years, frequent failures, safety device concerns, parts unavailable, code violations uncorrectable without modernization.
```

**Roofing**:
```
Score 5: Age 0-7 years, no leaks, no ponding, membrane and flashings intact, warranty active.
Score 4: Age 7-14 years, no active leaks, minor ponding (< 48-hour drain), flashings intact, occasional patching.
Score 3: Age 14-18 years, 1-2 leaks in past year (repaired), moderate ponding, some flashing deterioration, patches visible, warranty expired.
Score 2: Age 18-22 years, recurring leaks, significant ponding, membrane showing alligator cracking or blistering, multiple patches, insulation saturated in areas.
Score 1: Age 22+ years, active leaks causing interior damage, widespread membrane failure, insulation saturated, structural concerns possible.
```

---

## 2. Remaining Life Estimation

### Adjusted Remaining Life Formula

```
Base remaining life = EUL - current_age
Adjusted remaining life = Base remaining life * condition_adjustment_factor

Condition adjustment factors:
  Score 5: 1.10 (equipment outperforming age expectations)
  Score 4: 1.00 (on track for full useful life)
  Score 3: 0.85 (may fail before EUL)
  Score 2: 0.50 (accelerated deterioration)
  Score 1: 0.00 (immediate replacement needed)

Example:
  RTU installed 2018, EUL 20 years, current year 2026, condition score 3
  Base remaining life: 20 - 8 = 12 years
  Adjusted remaining life: 12 * 0.85 = 10.2 years
  Estimated replacement year: 2026 + 10 = 2036

  Same RTU with condition score 2:
  Adjusted remaining life: 12 * 0.50 = 6 years
  Estimated replacement year: 2026 + 6 = 2032
```

### Maintenance Cost Ratio Analysis

```
Annual maintenance cost ratio = annual_maintenance_cost / replacement_cost

Decision thresholds:
  < 5%:   Normal range. Continue PM program.
  5-10%:  Elevated but acceptable. Monitor trend.
  10-15%: Begin replacement planning. Next year's budget should include replacement.
  > 15%:  Replacement is more economical. Every maintenance dollar is wasted.

Example:
  RTU #3 (condition score 2):
    Replacement cost: $60,000
    Annual maintenance spend:
      2023: $4,200 (7.0%)
      2024: $6,800 (11.3%)
      2025: $9,100 (15.2%) <-- REPLACEMENT THRESHOLD CROSSED
    Trend: increasing at 35-40% per year
    Recommendation: replace in 2026 budget cycle
```

### End-of-Life Warning System

```
Warning levels:
  GREEN:  Adjusted remaining life > 5 years, maintenance ratio < 10%
  YELLOW: Adjusted remaining life 2-5 years, or maintenance ratio 10-15%
  RED:    Adjusted remaining life < 2 years, or maintenance ratio > 15%, or condition score 1

For each piece of equipment, the lifecycle tracker assigns a color based on the most severe applicable criterion. Any RED equipment must appear in the next capital budget.
```

---

## 3. Worked Example: 200-Unit Multifamily Equipment Lifecycle Dashboard

### Property Profile
```
Property: Riverside Terrace Apartments
Units: 200
Built: 2008 (18 years old)
Last major renovation: 2018 (common areas, roofing, 3 RTUs)
Total building SF: 220,000
Floors: 5
Climate zone: 4A (NYC metro)
```

### Equipment Inventory and Lifecycle Status

```
| ID | Equipment | Year Installed | Age | EUL | Condition | Adj. Remaining | Replace Cost | Annual Maint | Maint Ratio | Warning |
|---|---|---|---|---|---|---|---|---|---|---|
| HVAC-01 | RTU #1 (15-ton) | 2008 | 18 | 20 | 2 | 1.0 yr | $60,000 | $9,100 | 15.2% | RED |
| HVAC-02 | RTU #2 (15-ton) | 2008 | 18 | 20 | 2 | 1.0 yr | $60,000 | $8,400 | 14.0% | RED |
| HVAC-03 | RTU #3 (15-ton) | 2018 | 8 | 20 | 4 | 12.0 yr | $60,000 | $3,200 | 5.3% | GREEN |
| HVAC-04 | RTU #4 (15-ton) | 2018 | 8 | 20 | 4 | 12.0 yr | $60,000 | $3,100 | 5.2% | GREEN |
| HVAC-05 | RTU #5 (15-ton) | 2008 | 18 | 20 | 3 | 1.7 yr | $60,000 | $7,200 | 12.0% | RED |
| HVAC-06 | RTU #6 (15-ton) | 2018 | 8 | 20 | 4 | 12.0 yr | $60,000 | $2,900 | 4.8% | GREEN |
| HVAC-07 | RTU #7 (15-ton) | 2008 | 18 | 20 | 3 | 1.7 yr | $60,000 | $6,800 | 11.3% | RED |
| HVAC-08 | RTU #8 (15-ton) | 2008 | 18 | 20 | 3 | 1.7 yr | $60,000 | $6,500 | 10.8% | YELLOW |
| BLR-01 | Boiler #1 | 2008 | 18 | 30 | 4 | 12.0 yr | $90,000 | $1,800 | 2.0% | GREEN |
| BLR-02 | Boiler #2 | 2008 | 18 | 30 | 3 | 10.2 yr | $90,000 | $2,600 | 2.9% | GREEN |
| ELV-01 | Elevator Cab 1 | 2008 | 18 | 25 | 3 | 6.0 yr | $175,000 | $12,800 | 7.3% | YELLOW |
| ELV-02 | Elevator Cab 2 | 2008 | 18 | 25 | 3 | 6.0 yr | $175,000 | $12,800 | 7.3% | YELLOW |
| ROOF-A | Roof Section A | 2018 | 8 | 22 | 4 | 14.0 yr | $160,000 | $2,200 | 1.4% | GREEN |
| ROOF-B | Roof Section B | 2018 | 8 | 22 | 4 | 14.0 yr | $160,000 | $2,000 | 1.3% | GREEN |
| GEN-01 | Emergency Generator | 2008 | 18 | 28 | 4 | 10.0 yr | $120,000 | $3,500 | 2.9% | GREEN |
| PUMP-01 | Booster Pump Set | 2008 | 18 | 20 | 3 | 1.7 yr | $25,000 | $2,400 | 9.6% | RED |
| SWG-01 | Main Switchgear | 2008 | 18 | 35 | 4 | 17.0 yr | $150,000 | $1,200 | 0.8% | GREEN |
| CT-01 | Cooling Tower | 2008 | 18 | 22 | 3 | 3.4 yr | $180,000 | $8,200 | 4.6% | YELLOW |

Dashboard Summary:
  RED items (immediate/1-year):     5  (RTUs 1,2,5,7 + booster pump)
  YELLOW items (2-5 year planning): 4  (RTU 8, Elevators 1+2, Cooling Tower)
  GREEN items (on track):           9
  Total equipment tracked:          18
```

### Replacement Reserve Analysis

```
Required Annual Reserve Contributions:

| Equipment | Replacement Cost | Remaining Life | Annual Contribution |
|---|---|---|---|
| RTU #1 | $60,000 | 1 yr | $60,000 (full funding needed) |
| RTU #2 | $60,000 | 1 yr | $60,000 (full funding needed) |
| RTU #3 | $60,000 | 12 yr | $5,000 |
| RTU #4 | $60,000 | 12 yr | $5,000 |
| RTU #5 | $60,000 | 2 yr | $30,000 |
| RTU #6 | $60,000 | 12 yr | $5,000 |
| RTU #7 | $60,000 | 2 yr | $30,000 |
| RTU #8 | $60,000 | 2 yr | $30,000 |
| Boiler #1 | $90,000 | 12 yr | $7,500 |
| Boiler #2 | $90,000 | 10 yr | $9,000 |
| Elevator 1 | $175,000 | 6 yr | $29,167 |
| Elevator 2 | $175,000 | 6 yr | $29,167 |
| Roof A | $160,000 | 14 yr | $11,429 |
| Roof B | $160,000 | 14 yr | $11,429 |
| Generator | $120,000 | 10 yr | $12,000 |
| Booster Pump | $25,000 | 2 yr | $12,500 |
| Switchgear | $150,000 | 17 yr | $8,824 |
| Cooling Tower | $180,000 | 3 yr | $60,000 |
| TOTAL | $1,905,000 | | $405,016/yr |

Per unit per year: $2,025 ($405,016 / 200 units)

Immediate Capital Need (Year 1):
  RTU #1 replacement: $60,000
  RTU #2 replacement: $60,000
  Total Year 1: $120,000

Year 2 Capital Need:
  RTU #5 replacement: $60,000
  RTU #7 replacement: $60,000
  RTU #8 replacement: $60,000
  Booster pump replacement: $25,000
  Total Year 2: $205,000

Year 3 Capital Need:
  Cooling tower replacement: $180,000
  Total Year 3: $180,000

5-Year Capital Need: $505,000 (Years 1-3) + elevator + other = $855,000 est.

Current Reserve Balance: $385,000
5-Year Need: $855,000
Reserve Adequacy: 45% -- UNDERFUNDED

Catch-up Plan:
  Annual contribution needed: $855,000 / 5 = $171,000 minimum
  Less current balance prorated: $385,000 / 5 = $77,000
  Net annual increase needed: $94,000/year above current contributions
  Per unit increase: $470/unit/year
```

---

## 4. Capital Planning Integration

### Priority Matrix

Combine condition score, safety impact, and financial impact to prioritize capital projects:

```
Priority 1 (must do -- safety or code):
  - Any fire/life safety system at condition score 1 or 2
  - Elevator with safety violations
  - Structural concerns
  - Building envelope failures causing water infiltration
  Funding: non-negotiable, fund immediately even if reserve is insufficient

Priority 2 (should do -- operational risk):
  - HVAC at condition score 1 or 2 (tenant comfort and retention)
  - Equipment with maintenance ratio > 15%
  - Plumbing with leak history
  Funding: next available capital budget cycle

Priority 3 (plan for -- lifecycle):
  - Equipment with adjusted remaining life < 5 years
  - Condition score 3 with declining trend
  - Systems approaching useful life (within 80% of EUL)
  Funding: include in 3-year capital plan

Priority 4 (enhancement -- ROI-driven):
  - Energy efficiency upgrades (LED, VFD, BAS optimization)
  - Amenity upgrades for competitive positioning
  - Technology upgrades (smart thermostats, access control)
  Funding: evaluate ROI, fund if payback < 5 years
```

### Annual Capital Budget Template

```
FY 2027 Capital Budget -- Riverside Terrace Apartments

| Priority | Project | Estimated Cost | Funding Source | Timeline |
|---|---|---|---|---|
| P1 | RTU #1 replacement | $60,000 | Reserve | Q1 2027 |
| P1 | RTU #2 replacement | $60,000 | Reserve | Q1 2027 |
| P2 | RTU #5 replacement | $60,000 | Reserve | Q2 2027 |
| P2 | Booster pump replacement | $25,000 | Reserve | Q2 2027 |
| P3 | Cooling tower (begin planning) | $0 (2028) | Reserve | Planning only |
| P4 | Common area LED retrofit | $45,000 | OpEx (ROI: 2.3yr) | Q3 2027 |

Total FY 2027 Capital: $250,000
Reserve balance after: $385,000 - $205,000 + $168,200 (contributions) = $348,200
```
