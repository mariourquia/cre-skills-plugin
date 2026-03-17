# Preventive Maintenance Program Reference

Complete PM schedule templates by system type, equipment useful life tables, and deferred maintenance cost analysis. All examples use a baseline 200-unit Class B multifamily property, built 2008, in ASHRAE Climate Zone 4A (NYC metro).

---

## 1. HVAC System PM Schedules

### Rooftop Units (RTU) / Packaged Units

Baseline: 8 Carrier 48XL RTUs, 15-ton each, installed 2018 (8 years old, EUL 20 years)

| Frequency | Task | Est. Labor (hrs) | Materials | Notes |
|---|---|---|---|---|
| Monthly | Filter inspection | 0.5/unit | $0 (inspect only) | Replace if > 50% loaded |
| Monthly | Belt inspection/tension | 0.25/unit | $0 | Replace if cracked, glazed, or > 1/2" deflection |
| Monthly | Condensate drain check | 0.25/unit | $0 | Flush with bleach solution |
| Monthly | Visual inspection (leaks, corrosion, vibration) | 0.25/unit | $0 | Note and report anomalies |
| Quarterly | Filter replacement | 0.5/unit | $35/filter x 2/unit = $70 | Use MERV-13 minimum |
| Quarterly | Coil inspection | 0.5/unit | $0 | Clean if dirty; full clean semi-annual |
| Quarterly | Refrigerant pressure check | 0.5/unit | $0 (unless adding) | Log pressures; flag if low |
| Quarterly | Economizer linkage and damper operation | 0.5/unit | $0 | Verify free movement, proper sequencing |
| Quarterly | Electrical connections torque check | 0.5/unit | $0 | Loose connections cause fires |
| Semi-annual | Comprehensive coil cleaning (evaporator) | 1.0/unit | $45 coil cleaner | Chemical clean, rinse, verify drain |
| Semi-annual | Condenser coil cleaning | 1.0/unit | $45 coil cleaner | Power wash if severely fouled |
| Semi-annual | Blower wheel cleaning | 0.75/unit | $0 | Buildup reduces airflow 10-30% |
| Annual | Full refrigerant leak check | 1.0/unit | $0 (unless adding) | EPA 608 compliance |
| Annual | Motor amp draw measurement | 0.5/unit | $0 | Compare to nameplate; > 110% indicates problem |
| Annual | Vibration analysis | 0.75/unit | $0 (equipment needed) | Baseline + trend; flag if increasing |
| Annual | Control sequence verification | 1.0/unit | $0 | Verify heating, cooling, economizer, dehumidification |
| Annual | Condensate pan treatment | 0.25/unit | $15 pan tablets | Prevent algae/biofilm |
| Annual | Crankcase heater verification | 0.25/unit | $0 | Must operate during off cycles |

**Annual PM cost per RTU (labor + materials)**:
```
Labor hours: monthly (1.25 x 12) + quarterly (2.5 x 4) + semi (2.75 x 2) + annual (3.75)
           = 15 + 10 + 5.5 + 3.75 = 34.25 hours/unit
Materials: quarterly ($70 x 4) + semi ($90 x 2) + annual ($15) = $280 + $180 + $15 = $475/unit
Burdened labor rate: $85/hour
Annual PM cost per unit: (34.25 x $85) + $475 = $2,911 + $475 = $3,386
Annual PM cost (8 units): $27,090

Replacement cost per unit: $60,000 (15-ton packaged RTU, installed)
PM cost as % of replacement: 5.6% -- WITHIN NORMAL RANGE (target < 10%)
```

### Boiler Systems

Baseline: 2 Weil-McLain 88 Series cast iron boilers, 3,000 MBH each, installed 2008 (18 years old, EUL 25-30 years)

| Frequency | Task | Est. Labor (hrs) | Materials | Notes |
|---|---|---|---|---|
| Monthly (heating season) | Flame inspection and adjustment | 0.5/unit | $0 | Blue flame, no lifting/impingement |
| Monthly (heating season) | Pressure/temperature check | 0.25/unit | $0 | Verify within operating range |
| Monthly (heating season) | Low water cutoff test | 0.25/unit | $0 | Blow down and test activation |
| Quarterly | Water chemistry test | 0.5/system | $25 test kit | pH 7.0-9.0, hardness < 3.5 gpg |
| Pre-season (fall) | Full start-up inspection | 3.0/unit | $150 gaskets/consumables | Clean, inspect, test all safety devices |
| Pre-season | Burner inspection and tuning | 2.0/unit | $0 | Combustion analysis: CO < 100 ppm, O2 3-5% |
| Pre-season | Safety valve test | 0.5/unit | $0 | Lift and reseat; replace if leaks |
| Annual | Fireside cleaning | 2.0/unit | $75 brushes/chemicals | Remove soot/scale from heat exchanger |
| Annual | Waterside cleaning and inspection | 2.0/unit | $100 chemicals | Inspect for scale, corrosion, cracks |
| Annual | Flue and chimney inspection | 1.0/system | $0 | Check for obstructions, deterioration |
| Annual | Expansion tank pressure check | 0.5/system | $0 | Pre-charge pressure per design |
| Annual | Circulating pump inspection | 1.0/system | $25 seal kit | Check seals, bearings, alignment |
| Annual | Code inspection (jurisdiction required) | 1.0/system | $250 permit fee | Required in most jurisdictions |

**Annual PM cost (2-boiler system)**:
```
Labor: monthly (1.5 x 7mo) + quarterly (0.5 x 4) + pre-season (10) + annual (7.5)
     = 10.5 + 2 + 10 + 7.5 = 30 hours
Materials: quarterly ($25 x 4) + pre-season ($300) + annual ($450) = $850
Annual PM cost: (30 x $85) + $850 = $3,400
Replacement cost (2 boilers + piping): $180,000
PM cost %: 1.9% -- EXCELLENT (boilers benefit greatly from PM)
```

### Cooling Tower

Baseline: 1 Marley NC Series cooling tower, 200-ton, installed 2018

| Frequency | Task | Est. Labor (hrs) | Materials | Notes |
|---|---|---|---|---|
| Monthly (cooling season) | Water treatment chemical check | 0.5 | $150 chemicals | Maintain per treatment program |
| Monthly (cooling season) | Basin inspection and cleaning | 0.5 | $0 | Remove debris, check drain |
| Monthly (cooling season) | Fan and motor inspection | 0.5 | $0 | Vibration, noise, alignment |
| Quarterly | Legionella testing | 0.5 | $250 lab test | Per ASHRAE 188 / local law (NYC LL77) |
| Quarterly | Blowdown valve operation | 0.25 | $0 | Verify automatic blowdown working |
| Semi-annual | Fill media inspection | 1.0 | $0 | Check for scale, biofilm, damage |
| Semi-annual | Drift eliminator inspection | 0.5 | $0 | Missing or damaged = aerosol risk |
| Annual | Full inspection and winterization | 4.0 | $200 consumables | Drain, clean, inspect structure, treat |
| Annual | VFD/motor testing | 1.0 | $0 | Megger test, amp draw, VFD parameters |

**Legionella compliance note**: NYC Local Law 77 requires quarterly Legionella culture testing, annual certification, and an owner-registered Water Management Program per ASHRAE Standard 188. Non-compliance carries fines of $2,000+ per violation. Similar requirements exist in many other jurisdictions.

---

## 2. Elevator PM Schedules

### Traction Elevator (Machine-Room)

Baseline: 2 Otis Gen2 gearless traction elevators, 3500 lb capacity, installed 2008

| Frequency | Task | Est. Labor (hrs) | Materials | Notes |
|---|---|---|---|---|
| Monthly | Cab interior inspection | 0.5/unit | $0 | Finishes, lighting, indicators, phone |
| Monthly | Door operator adjustment | 0.5/unit | $0 | Open/close speed, nudging, force |
| Monthly | Door track cleaning and lubrication | 0.5/unit | $15 lubricant | Prevents door faults (most common callback) |
| Monthly | Pit inspection | 0.5/unit | $0 | Oil, water, debris, buffer condition |
| Monthly | Machine room check | 0.5/unit | $0 | Oil level, temp, cleanliness, ventilation |
| Monthly | Emergency phone test | 0.25/unit | $0 | Verify connection to monitoring center |
| Monthly | Ride quality observation | 0.25/unit | $0 | Smooth acceleration, leveling, noise |
| Quarterly | Safety device testing | 1.0/unit | $0 | Governor, buffers, safety switches |
| Quarterly | Door protective devices | 0.5/unit | $0 | Safety edge, photo eye, detector edge |
| Quarterly | Leveling accuracy measurement | 0.5/unit | $0 | Per ADA: within 1/2 inch of landing |
| Quarterly | Firefighter Phase I/II test | 0.5/unit | $0 | Fire recall and in-car operation |
| Quarterly | Hoistway door lock and interlock | 0.5/unit | $0 | Each landing door verified |
| Annual | Full load test (125% rated) | 2.0/unit | $0 | Per ASME A17.1 |
| Annual | Belt/rope inspection | 1.5/unit | $0 | Measure diameter, count broken wires |
| Annual | Controller inspection | 2.0/unit | $0 | Clean, tighten connections, check components |
| Annual | Guide shoe/roller inspection | 1.0/unit | $100 rollers if needed | Replace if worn beyond tolerance |
| Annual | State/local inspection | 1.0/unit | $300 permit fee | Code-required annual inspection |
| 5-Year | Category 5 comprehensive test | 8.0/unit | $0 | Full test per ASME A17.2 |
| 5-Year | Governor testing under load | 2.0/unit | $0 | Verify trip speed per nameplate |

**Annual PM cost (2 elevators, full-service contract)**:
```
Full-service maintenance contract (typical for 2 traction elevators):
  Monthly contract: $1,800-$2,800/month for 2 units
  Covers: all PM tasks above, callbacks, parts (except major modernization)
  Annual contract cost: $21,600-$33,600
  Typical for Class B multifamily: $25,000/year

State inspection fees: $600/year
Total annual elevator cost: $25,600

Replacement cost (2 elevators, full modernization): $350,000
PM cost %: 7.3% -- NORMAL for elevators (high-maintenance equipment)
```

**Callback metrics (quality indicator for elevator maintenance vendor)**:
```
Good performance:    < 3 callbacks/unit/month
Acceptable:          3-5 callbacks/unit/month
Poor (review vendor): > 5 callbacks/unit/month
Entrapments:         0 is the target. > 2/year/unit = unacceptable
```

---

## 3. Equipment Useful Life Tables

### ASHRAE-Based Expected Useful Life (EUL)

| Equipment | EUL (years) | Replacement Cost Range (/unit) | Notes |
|---|---|---|---|
| **HVAC** | | | |
| Package RTU (< 20 ton) | 15-20 | $40,000-$80,000 | Climate and maintenance dependent |
| Split system (residential) | 15-18 | $8,000-$15,000 | Per unit for multifamily |
| Chiller (centrifugal) | 20-25 | $150,000-$500,000 | Size dependent |
| Chiller (scroll/screw) | 20-23 | $80,000-$300,000 | Size dependent |
| Boiler (cast iron) | 25-35 | $60,000-$150,000 | Water treatment extends life |
| Boiler (steel) | 20-25 | $50,000-$120,000 | More susceptible to corrosion |
| Cooling tower | 20-25 | $100,000-$300,000 | Structure vs fill (fill: 10-15 years) |
| AHU / Fan coil | 20-25 | $15,000-$60,000 | Motors may need replacement at 10-15 |
| VFD / Motor controller | 15-20 | $3,000-$15,000 | Electronics degrade |
| BAS/DDC controller | 15-20 | $5,000-$25,000 | Software obsolescence often drives replacement |
| Ductwork | 30+ | Varies | Rarely replaced unless major renovation |
| **Elevator** | | | |
| Traction elevator (full) | 25-30 | $150,000-$250,000 | Per cab, full modernization |
| Hydraulic elevator | 20-25 | $100,000-$175,000 | Cylinder replacement is major cost |
| Elevator cab interior | 15-20 | $20,000-$40,000 | Cosmetic refresh |
| Elevator controller | 20-25 | $60,000-$100,000 | Most common modernization scope |
| **Fire/Life Safety** | | | |
| Fire alarm panel | 15-20 | $25,000-$100,000 | Building size dependent |
| Sprinkler heads | 50+ | $3-$8/head | NFPA 25 requires testing at 50 years |
| Fire pump | 25-30 | $30,000-$80,000 | Annual flow testing critical |
| Emergency generator | 25-30 | $50,000-$200,000 | Size dependent; fuel system: 15-20 years |
| Fire sprinkler piping | 40-50+ | $8-$15/SF | Corrosion in wet systems is primary concern |
| **Roofing** | | | |
| TPO/PVC membrane | 20-25 | $8-$14/SF | UV degradation, seam integrity |
| EPDM membrane | 20-25 | $7-$12/SF | Aging makes rubber brittle |
| Modified bitumen | 15-20 | $10-$16/SF | Multiple ply layers extend life |
| Built-up roofing (BUR) | 20-30 | $12-$18/SF | Traditional; heavy |
| Shingle (architectural) | 25-30 | $4-$8/SF | Residential/low-slope only |
| **Plumbing** | | | |
| Copper domestic piping | 50-70 | $12-$20/LF | Water chemistry dependent |
| Cast iron drain piping | 50-75 | $15-$25/LF | Orangeburg: replace immediately |
| Water heater (commercial) | 12-15 | $15,000-$40,000 | Scale buildup reduces life |
| Domestic booster pump | 15-20 | $5,000-$15,000 | |
| **Electrical** | | | |
| Switchgear | 30-40 | $50,000-$200,000 | Infrared scan annually |
| Electrical panels | 25-35 | $5,000-$15,000 | Breakers may need replacement sooner |
| Transformer (dry type) | 25-30 | $10,000-$50,000 | Load and temperature dependent |
| Emergency lighting | 7-10 | $200-$500/unit | Battery life is limiting factor |
| **Building Envelope** | | | |
| Windows (aluminum frame) | 25-35 | $25-$60/SF | Seal failure is first sign |
| Windows (vinyl frame) | 20-30 | $20-$45/SF | UV degradation of frame |
| Caulking/sealants | 7-12 | $3-$8/LF | Most overlooked PM item |
| Exterior paint | 7-10 | $2-$5/SF | Climate dependent |
| Parking lot (asphalt) | 15-20 | $3-$6/SF | Seal coat every 3-5 years extends life |

---

## 4. Deferred Maintenance Cost Multiplier Analysis

### Multiplier Table by System

| System | Year 1 | Year 2 | Year 3 | Year 5 | Emergency |
|---|---|---|---|---|---|
| HVAC (RTU) | 1.0x | 1.5x | 2.0x | 3.5x | 4.5x |
| Boiler | 1.0x | 1.3x | 2.0x | 3.0x | 5.0x |
| Elevator | 1.0x | 1.2x | 1.8x | 2.5x | 4.0x |
| Roofing | 1.0x | 1.5x | 2.5x | 4.0x | 6.0x |
| Fire alarm | 1.0x | 1.2x | 1.5x | 2.0x | 3.0x |
| Plumbing | 1.0x | 1.5x | 2.5x | 4.5x | 5.5x |
| Electrical | 1.0x | 1.3x | 1.8x | 2.5x | 4.0x |
| Building envelope | 1.0x | 1.5x | 2.5x | 4.0x | 5.0x |

**Why multipliers vary by system**:
- **Roofing**: a small leak deferred becomes water damage to insulation, decking, ceilings, walls, and tenant spaces. The roofing repair itself is 10% of the total cost at year 5.
- **Plumbing**: a deferred pipe replacement becomes a catastrophic leak with water damage to multiple floors, tenant displacement, mold remediation, and potential liability.
- **HVAC**: compressor failure from deferred maintenance damages the entire condensing unit. Refrigerant contamination can cascade through the system.
- **Elevator**: deferred maintenance increases callback frequency, tenant complaints, and eventually triggers a code violation that forces emergency modernization at premium pricing.

### Worked Example: Deferred Maintenance Register

```
Property: 200-unit multifamily, built 2008

Deferred Maintenance Register:

| Item | Planned Year | Planned Cost | Years Deferred | Multiplier | Current Est. Cost | Risk |
|---|---|---|---|---|---|---|
| RTU #3 replacement | 2024 | $60,000 | 2 | 1.5x | $90,000 | MEDIUM |
| RTU #5 compressor | 2025 | $12,000 | 1 | 1.0x | $12,000 | LOW |
| Parking lot resurface | 2023 | $275,000 | 3 | 2.0x | $550,000 | HIGH |
| Boiler #2 retubing | 2024 | $35,000 | 2 | 1.3x | $45,500 | MEDIUM |
| Roof section A patch | 2023 | $18,000 | 3 | 2.5x | $45,000 | HIGH |
| Caulking/sealants | 2022 | $42,000 | 4 | 3.5x | $147,000 | HIGH |
| Emergency lighting | 2025 | $8,500 | 1 | 1.2x | $10,200 | LOW |
| Elevator cab refresh | 2024 | $28,000 | 2 | 1.2x | $33,600 | LOW |

Summary:
  Total planned cost (at original schedule): $478,500
  Total current estimated cost (deferred):   $933,300
  Deferred maintenance multiplier (blended): 1.95x
  Cost of deferral: $454,800 in additional expense

  Priority 1 (immediate -- risk of failure/damage):
    Parking lot, Roof section A, Caulking/sealants
    Combined cost: $742,000

  Priority 2 (within 12 months):
    RTU #3, Boiler #2
    Combined cost: $135,500

  Priority 3 (within 24 months):
    RTU #5 compressor, Emergency lighting, Elevator cab
    Combined cost: $55,800
```

### Return on PM Investment

```
PM investment vs reactive maintenance cost comparison:

Scenario A (with PM program):
  Annual PM cost: $114,000
  Annual reactive repairs: $38,000
  Emergency replacements: $15,000 (1 event/year average)
  Total annual maintenance: $167,000
  Equipment reaches full useful life: YES

Scenario B (deferred PM / reactive only):
  Annual PM cost: $0
  Annual reactive repairs: $95,000 (2.5x increase)
  Emergency replacements: $72,000 (5x increase)
  Total annual maintenance: $167,000
  Equipment reaches full useful life: NO (50-75% of EUL)

Costs appear similar, but:
  Scenario A useful life: 20 years
  Scenario B useful life: 12-15 years (replacement 5-8 years sooner)
  Early replacement cost: $480,000 (8 RTUs)
  Annualized cost of early replacement: $480,000 / 5 years early = $96,000/year
  True cost of deferred PM: $167,000 + $96,000 = $263,000/year

PM program ROI: ($263,000 - $167,000) / $114,000 PM investment = 84% annual return
```
