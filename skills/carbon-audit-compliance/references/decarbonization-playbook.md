# Decarbonization Playbook: Building Systems Retrofit Guide

## Overview

Emissions reduction priority should follow marginal abatement cost (MAC) curve logic: lowest cost per tCO2e abated first, highest-impact measures prioritized when capital is constrained. The sequence below is generally ordered by cost-effectiveness for typical commercial buildings.

---

## 1. Operational Optimization (No/Low Capex)

### Building Management System (BMS) Optimization
**Emissions reduction potential**: 10-20% of total building energy
**Payback**: 0-1 year (mostly labor/commissioning cost)

Measures:
- Retro-commissioning (RCx): systematic review of all control sequences
- Optimize supply air temperature reset schedules
- Correct simultaneous heating and cooling
- Fix economizer operation (stuck dampers, broken sensors)
- Implement demand-controlled ventilation (CO2-based)
- Reduce after-hours HVAC operation (schedule audits)
- Optimize chiller/boiler staging and sequencing
- Calibrate or replace failed sensors (temperature, pressure, humidity)
- Reset condenser water temperature based on wet-bulb
- Implement variable speed drives on constant-volume fans and pumps

**Typical findings from RCx:**
| Issue | Prevalence | Energy Waste |
|-------|-----------|-------------|
| Simultaneous heating/cooling | 60% of buildings | 10-15% of HVAC energy |
| After-hours operation | 50% of buildings | 5-10% of total energy |
| Broken economizer | 40% of buildings | 5-8% of cooling energy |
| Stuck dampers | 35% of buildings | 3-7% of HVAC energy |
| Disabled setbacks | 30% of buildings | 5-10% of heating energy |

### Occupant Behavior Programs
**Emissions reduction potential**: 5-10%
**Payback**: Immediate

- Tenant energy dashboards (sub-metered data visualization)
- Green lease clauses: utility data sharing, efficient operations commitment
- Temperature setpoint education (each 1F setback = ~3% HVAC savings)
- Plug load management (smart power strips, equipment shutdown schedules)
- Lighting behavior campaigns (daylit spaces, task lighting)

---

## 2. Lighting Systems (LED Retrofit)

### Full LED Retrofit
**Emissions reduction potential**: 15-25% of electricity consumption
**Simple payback**: 2-4 years
**IRR**: 25-50%
**Useful life**: 50,000-100,000 hours (15-25 years)

**Cost benchmarks:**
| Space Type | Cost/SF | Annual Savings/SF | Payback |
|-----------|---------|-------------------|---------|
| Office (troffer replacement) | $3.00-5.00 | $1.00-2.00 | 2.5-4 yr |
| Parking garage | $1.50-3.00 | $0.75-1.50 | 2-3 yr |
| Common area/lobby | $4.00-8.00 | $1.50-2.50 | 2.5-4 yr |
| Warehouse/industrial | $1.00-2.50 | $0.50-1.25 | 2-3 yr |
| Exterior/site | $2.00-4.00 | $0.75-1.50 | 2.5-4 yr |

### Lighting Controls
**Additional savings beyond LED**: 20-40% of lighting energy
**Simple payback**: 1-3 years (when bundled with LED)

| Control Type | Savings | Best Application |
|-------------|---------|-----------------|
| Occupancy sensors | 20-30% | Private offices, restrooms, storage |
| Daylight harvesting | 25-40% | Perimeter zones with glazing |
| Scheduling/time clock | 15-25% | Common areas, parking |
| Personal dimming | 10-20% | Open office workstations |
| Networked controls (PoE) | 30-50% | New construction, major renovation |

### Utility Incentives
- Most utilities offer $0.50-2.00/fixture rebate for LED retrofits
- Custom incentives for controls: $0.10-0.25/kWh saved
- Always apply before project start; pre-approval often required
- Can reduce payback by 30-50%

---

## 3. HVAC Electrification

### Heat Pump Conversion
**Emissions reduction potential**: 30-50% of heating emissions (depends on grid carbon intensity)
**Simple payback**: 5-10 years
**IRR**: 10-20%
**Useful life**: 15-25 years

**Technology options:**
| System | Best Fit | COP Range | Cost Premium vs Gas |
|--------|---------|-----------|-------------------|
| Air-source heat pump (ASHP) | Small-medium buildings, mild climates | 2.5-4.0 | 20-40% |
| Variable refrigerant flow (VRF) | Hotels, multifamily, mixed-use | 3.0-5.0 | 30-50% |
| Ground-source heat pump (GSHP) | Large campus, long hold period | 4.0-6.0 | 60-100% |
| Air-to-water heat pump | Hydronic distribution systems | 2.5-3.5 | 25-45% |

**Decision framework for heat pump conversion:**
```
IF grid_carbon_intensity < 0.4 kgCO2e/kWh
  AND building_has_hydronic_or_ducted_distribution
  AND remaining_boiler_life < 10 years
  AND climate_zone NOT in [7, 8] (extreme cold)
THEN heat_pump_conversion_likely_favorable
```

**Cold climate considerations:**
- Modern cold-climate ASHPs rated to -13F (-25C)
- Below design temp: dual-fuel backup or supplemental electric resistance
- Ground-source avoids cold-climate performance degradation
- Oversizing penalty: avoid -- use proper Manual J/load calculations

### Central Plant Optimization
**Chiller plant:**
- Variable primary pumping: 15-25% pump energy reduction
- Magnetic bearing centrifugal chillers: 30-40% more efficient than legacy
- Chilled water temperature reset: 2-5% chiller energy savings per degree
- Free cooling (waterside economizer): eliminates chiller in cool months

**Boiler plant:**
- Condensing boilers: 90-95% efficiency vs 80% for legacy
- Modulating burners: better part-load performance
- Hot water temperature reset: lower supply temp = higher boiler efficiency

---

## 4. Building Envelope

### Insulation Improvements
**Emissions reduction potential**: 10-20% of heating/cooling energy
**Simple payback**: 7-15 years
**IRR**: 5-12%

| Measure | Cost/SF of Improved Area | Annual Savings/SF | Payback |
|---------|--------------------------|-------------------|---------|
| Roof insulation (to R-30) | $3.00-6.00 | $0.30-0.60 | 8-12 yr |
| Wall insulation (exterior) | $8.00-15.00 | $0.50-1.00 | 10-15 yr |
| Below-grade insulation | $2.00-5.00 | $0.20-0.40 | 8-15 yr |
| Air sealing | $0.50-2.00 | $0.20-0.50 | 2-5 yr |

- Best ROI when coordinated with roof replacement or facade repair
- Air sealing almost always the highest-ROI envelope measure
- Infrared thermography identifies worst thermal bridges and air leaks

### Window Upgrades
**Simple payback**: 15-25 years (standalone), 8-12 years (bundled with facade)

| Technology | U-Value | SHGC | Cost/SF of Glass | Best Fit |
|-----------|---------|------|-------------------|---------|
| Low-e double pane | 0.25-0.30 | 0.25-0.40 | $30-50 | Standard replacement |
| Low-e triple pane | 0.15-0.20 | 0.20-0.35 | $50-80 | Cold climates, premium office |
| Electrochromic (smart glass) | 0.25 | 0.09-0.41 (variable) | $80-120 | High solar exposure, no blinds |
| Interior film retrofit | Minimal U improvement | 0.30-0.50 | $5-10 | Budget option, short hold |

- Window upgrades rarely pencil standalone; bundle with facade renovation
- Interior film: 2-4 year payback, good short-hold-period solution
- Electrochromic glass: premium buildings, 10+ year payback, eliminates blinds

---

## 5. Renewable Energy

### On-Site Solar PV
**Emissions reduction potential**: 5-20% of electricity (roof-constrained in urban)
**Simple payback**: 5-8 years (with ITC/IRA credits)
**IRR**: 12-20% (with incentives)
**Useful life**: 25-30 years

**Installed cost benchmarks (2025):**
| System Size | Cost/Watt (installed) | Annual Yield/kW | Notes |
|-------------|----------------------|-----------------|-------|
| < 100 kW (rooftop) | $2.50-3.50 | 1,200-1,800 kWh | Small commercial |
| 100-500 kW (rooftop) | $2.00-2.80 | 1,200-1,800 kWh | Mid-size commercial |
| 500 kW-5 MW (ground/carport) | $1.50-2.20 | 1,300-1,900 kWh | Campus/industrial |

**Federal incentives (IRA/Inflation Reduction Act):**
- Investment Tax Credit (ITC): 30% of installed cost (base)
- Bonus: +10% for domestic content, +10% for energy community, +10-20% for low-income
- Total potential ITC: 30-70%
- Depreciation: 5-year MACRS (adds ~15-20% effective value)

**Urban constraints:**
- Typical commercial roof: 10-15 watts/SF of available roof
- 100,000 SF building with 30% usable roof: ~300-450 kW system
- May cover 10-25% of total electricity consumption

### Power Purchase Agreements (PPA)
**Structure**: Third party owns system, building buys electricity at fixed rate
**Typical PPA rate**: $0.04-0.08/kWh (below retail in most markets)
**Term**: 15-25 years
**Capex required**: $0 (third party funds)

- Virtual PPA (VPPA): financial contract + REC delivery, no on-site system
- Physical PPA: on-site installation, behind-the-meter
- Community solar subscription: off-site, bill credit model, 5-15% savings

### Battery Energy Storage
**Useful for**: Demand charge reduction, solar self-consumption, resilience
**Cost**: $400-700/kWh installed (2025)
**Payback**: 5-10 years (demand charge savings markets)
**Best markets**: High demand charges (>$15/kW), time-of-use rate spreads > $0.10/kWh

---

## 6. Water and Waste

### Water Conservation
**Emissions reduction**: Indirect (water-energy nexus: 0.5-2.0 kWh/1,000 gal)
**Payback**: 1-3 years

| Measure | Water Savings | Cost | Payback |
|---------|--------------|------|---------|
| Low-flow fixtures (1.28 gpf toilets, 0.5 gpm faucets) | 20-30% | $50-200/fixture | 1-2 yr |
| Cooling tower water treatment optimization | 10-20% of makeup water | $5K-15K | 1-3 yr |
| Irrigation: smart controllers + drip | 30-50% landscape water | $10K-30K | 2-4 yr |
| Greywater reuse (toilet flushing) | 25-40% potable water | $50K-200K | 8-15 yr |

### Waste Diversion
**Emissions reduction**: Scope 3 (waste category)
| Program | Diversion Rate | Cost Impact |
|---------|---------------|-------------|
| Single-stream recycling | 15-25% | Net cost reduction (avoided disposal) |
| Composting (food waste) | 5-15% | Cost neutral to slight increase |
| E-waste/bulky item program | 2-5% | Cost neutral |
| Construction waste management | 50-90% (during renovation) | 10-20% savings vs landfill |

---

## Prioritization Matrix

### By Payback Period
| Priority | Measure | Payback | Emissions Impact |
|----------|---------|---------|-----------------|
| 1 | BMS optimization / RCx | 0-1 yr | 10-20% |
| 2 | LED lighting + controls | 2-4 yr | 15-25% electricity |
| 3 | Air sealing | 2-5 yr | 5-10% heating |
| 4 | Solar PV (with ITC) | 5-8 yr | 5-20% electricity |
| 5 | Heat pump conversion | 5-10 yr | 30-50% heating |
| 6 | Roof insulation | 8-12 yr | 5-10% heating/cooling |
| 7 | Window replacement | 15-25 yr | 5-15% heating/cooling |

### By Hold Period
| Hold Period | Recommended Measures |
|-------------|---------------------|
| < 3 years | BMS optimization, LED retrofit, air sealing, interior window film |
| 3-7 years | All above + solar PV, chiller/boiler replacement (if at end of life) |
| 7-15 years | All above + heat pump conversion, envelope improvements |
| 15+ years | Full deep retrofit: envelope + electrification + on-site renewables |

### By Building Type
| Building Type | Priority 1 | Priority 2 | Priority 3 |
|---------------|-----------|-----------|-----------|
| Office (Class A) | BMS optimization | LED + controls | Chiller plant upgrade |
| Office (Class B) | RCx + LED | Boiler replacement | Envelope sealing |
| Multifamily | DHW heat pump | LED common areas | Envelope + windows |
| Hotel | HVAC controls | LED + occupancy | Kitchen electrification |
| Industrial | Lighting | Process heat recovery | Roof insulation + solar |
| Retail | LED + daylighting | HVAC right-sizing | Roof insulation |

---

## Financial Modeling Template

### Retrofit Pro Forma Inputs
```
capex_total          = SUM(measure_costs)
annual_energy_savings = pre_retrofit_cost - post_retrofit_cost
annual_penalty_avoided = excess_emissions * penalty_rate
annual_maintenance_delta = new_maintenance - old_maintenance
incentives           = utility_rebates + tax_credits + grants
net_capex            = capex_total - incentives

annual_benefit       = energy_savings + penalty_avoided - maintenance_delta
simple_payback       = net_capex / annual_benefit
npv                  = SUM(annual_benefit_t / (1 + discount_rate)^t) - net_capex
irr                  = rate where npv = 0
```

### Discount Rate Guidance
- Institutional owner (core): 6-8% (WACC-based)
- Value-add fund: 8-12%
- Opportunistic: 12-15%
- Penalty avoidance: use risk-free rate (penalty is certain cost)

### Green Premium on Exit
- LEED-certified buildings: 5-15% cap rate compression vs non-certified
- ENERGY STAR 75+: 3-8% rent premium
- LL97-compliant (NYC): emerging premium as penalties bite
- Factor green premium into exit valuation for full retrofit ROI
