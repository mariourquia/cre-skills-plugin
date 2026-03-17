# Physical Climate Risk Assessment Framework for CRE

## Methodology Overview

Physical climate risk assessment quantifies the probability and financial impact of climate-related hazards on real property. This framework covers five primary hazards, each with standardized data sources, scoring methodology, and dollar-denominated impact estimation.

### Risk Scoring Scale (All Hazards)
| Score | Level | Description |
|-------|-------|-------------|
| 1 | Minimal | Negligible probability within investment horizon |
| 2 | Low | <5% annual probability, limited financial impact |
| 3 | Moderate | 5-15% annual probability or material financial impact |
| 4 | High | 15-30% annual probability, significant financial impact |
| 5 | Severe | >30% annual probability or existential financial threat |

---

## Hazard 1: Flood Risk

### Data Sources
| Source | Coverage | Resolution | Access |
|--------|----------|-----------|--------|
| FEMA NFIP Flood Maps | US nationwide | Parcel-level | map.fema.gov (free) |
| First Street Foundation (FSF) | US nationwide | Property-level | riskfactor.com / API (paid) |
| NOAA Sea Level Rise Viewer | Coastal US | 1m increments | coast.noaa.gov (free) |
| USACE National Levee Database | Levee-protected areas | Structure-level | nld.usace.army.mil (free) |
| Private vendors (Moody's RMS, CoreLogic) | Global | Building-level | Licensed data |

### Assessment Methodology

**Step 1: Baseline Flood Zone Classification**
| FEMA Zone | Annual Probability | Federal Insurance Requirement |
|-----------|-------------------|------------------------------|
| Zone A/AE | 1% (100-yr) | Mandatory for federally backed mortgages |
| Zone V/VE | 1% + wave action | Mandatory, highest premiums |
| Zone X (shaded) | 0.2% (500-yr) | Not required but recommended |
| Zone X (unshaded) | <0.2% | Not required |
| Zone D | Undetermined | Not required |

**Step 2: Forward-Looking Flood Risk (First Street Foundation)**
FSF provides Factor scores (1-10) and flood depth projections at 15- and 30-year horizons accounting for:
- Climate-adjusted precipitation intensity
- Sea level rise projections
- Upstream development and impervious surface changes
- Coastal erosion and subsidence

**Step 3: Dollar-Denominated Impact Estimation**
```
Expected Annual Loss (EAL) = SUM over return_periods(
  probability_increment * damage_at_depth(flood_depth)
)
```

**Depth-damage functions (% of building replacement cost):**
| Flood Depth | Slab-on-Grade | Basement Present | Parking Structure |
|-------------|---------------|------------------|-------------------|
| 0-1 ft | 8-12% | 15-25% | 5-10% |
| 1-3 ft | 15-25% | 30-45% | 12-20% |
| 3-6 ft | 25-40% | 45-65% | 20-35% |
| 6-10 ft | 40-60% | 60-80% | 35-55% |
| >10 ft | 55-75% | 75-95% | 50-70% |

**Step 4: Insurance Premium Trajectory**
- FEMA Risk Rating 2.0: individual property pricing based on actual risk
- Average premium increases: 5-18% annually for high-risk properties
- Private flood insurance: increasingly available, often 20-40% below NFIP
- Model insurance costs over hold period using compound annual increase

**Worked Example: Coastal Office Building, Miami-Dade County**
- Replacement cost: $50M
- FEMA Zone AE (100-yr flood zone)
- FSF Factor: 8/10 (severe, increasing)
- Current flood depth (100-yr event): 3.5 ft
- Projected flood depth (30-yr, 100-yr event): 5.5 ft
- Current EAL: $185,000
- Projected EAL (30-yr): $340,000
- Current NFIP premium: $45,000/yr
- Projected premium (10-yr at 12% CAGR): $139,800/yr
- Total 10-year flood cost (premiums + expected loss): ~$2.9M

---

## Hazard 2: Wind/Hurricane Risk

### Data Sources
| Source | Coverage | Resolution | Access |
|--------|----------|-----------|--------|
| NOAA Historical Hurricane Tracks | Atlantic/Pacific | Track-level | coast.noaa.gov (free) |
| ASCE 7 Wind Speed Maps | US nationwide | County-level | asce7hazardtool.online (free) |
| AIR/RMS Catastrophe Models | Global | Building-level | Licensed |
| IBHS Fortified Standards | US Southeast/Gulf | Building-level | disastersafety.org |
| NOAA Storm Prediction Center | US nationwide | County-level | spc.noaa.gov (free) |

### Assessment Methodology

**Step 1: Design Wind Speed (ASCE 7-22)**
| Risk Category | Return Period | Typical Range (mph) |
|---------------|--------------|---------------------|
| Category I (low) | 300-yr | 95-180 |
| Category II (standard) | 700-yr | 105-195 |
| Category III (essential) | 1,700-yr | 115-200 |
| Category IV (critical) | 3,000-yr | 120-210 |

**Step 2: Vulnerability Assessment**
| Building Characteristic | Lower Vulnerability | Higher Vulnerability |
|------------------------|--------------------|--------------------|
| Construction | Reinforced concrete, steel | Wood frame, unreinforced masonry |
| Roof attachment | Hurricane clips/straps | Toe-nailed rafters |
| Roof covering | Impact-rated, adhered | Gravel ballast, mechanically attached |
| Openings | Impact-rated glazing | Unprotected windows |
| Age | Post-2002 (modern codes) | Pre-1992 (pre-Andrew codes) |

**Step 3: Dollar-Denominated Impact**
```
Wind EAL = SUM over return_periods(
  probability_increment * vulnerability_factor * replacement_cost
)
```

**Damage ratios by wind speed and construction type:**
| Wind Speed (mph) | Concrete/Steel | Masonry | Wood Frame |
|-------------------|---------------|---------|-----------|
| 90-110 | 1-5% | 3-10% | 5-15% |
| 110-130 (Cat 1-2) | 5-15% | 10-25% | 15-40% |
| 130-155 (Cat 3) | 15-30% | 25-50% | 40-70% |
| 155-180 (Cat 4) | 25-50% | 45-75% | 65-90% |
| >180 (Cat 5) | 40-70% | 65-95% | 80-100% |

**Step 4: Insurance Premium Modeling**
- Wind/hurricane deductible: typically 2-5% of insured value (named storm)
- Coastal property premiums: $2-8 per $100 of coverage (vs $0.30-0.80 inland)
- Premium trend: 8-15% annual increases in Gulf/Atlantic coastal markets
- Mitigation credits: IBHS Fortified designation can reduce premiums 15-35%

---

## Hazard 3: Wildfire Risk

### Data Sources
| Source | Coverage | Resolution | Access |
|--------|----------|-----------|--------|
| USFS Wildfire Risk to Potential Structures (WRPS) | US nationwide | Parcel-level | wildfirerisk.org (free) |
| CAL FIRE Severity Zone Maps | California | Parcel-level | osfm.fire.ca.gov (free) |
| First Street Foundation Fire Factor | US nationwide | Property-level | riskfactor.com (paid) |
| LANDFIRE (fuel models) | US nationwide | 30m grid | landfire.gov (free) |
| CoreLogic Wildfire Risk Score | US nationwide | Address-level | Licensed |

### Assessment Methodology

**Step 1: WUI (Wildland-Urban Interface) Classification**
| Zone | Definition | Risk Level |
|------|-----------|-----------|
| Interface | Structures directly adjacent to wildland vegetation | Highest |
| Intermix | Structures interspersed within wildland vegetation | High |
| Influence | Within 1.5 miles of large wildland area | Moderate |
| Non-WUI | Fully urbanized, no wildland proximity | Lower (not zero) |

**Step 2: CAL FIRE (or equivalent) Severity Zones**
| Zone | Description | Building Code Impact |
|------|-------------|---------------------|
| Very High (VHFHSZ) | Extreme fire weather + dense fuels + steep terrain | Chapter 7A compliance required |
| High (FHSZ) | Moderate fire weather + fuel load | Enhanced requirements |
| Moderate | Some fire weather potential | Standard code |

**Step 3: Property-Level Assessment**
- Defensible space: 0-5 ft (ember-resistant), 5-30 ft (lean/clean/green), 30-100 ft (reduced fuel)
- Construction materials: fire-rated roofing, ignition-resistant siding, tempered glazing
- Access: two-way egress road, emergency vehicle access
- Water supply: fire hydrant distance, on-site water storage

**Step 4: Financial Impact**
```
Wildfire EAL = annual_probability * (
  direct_damage + business_interruption + smoke_damage + evacuation_cost
)
```

**Damage estimates:**
| Impact Category | Typical Range |
|-----------------|---------------|
| Direct structure loss | 50-100% of replacement (total loss common) |
| Smoke/soot damage (near miss) | 5-20% of replacement |
| Business interruption (evacuation) | 2-8 weeks revenue loss |
| Post-fire debris flow/mudslide | Additional 10-30% site damage |
| Increased insurance (3-5 years post-fire) | 50-200% premium increase |

---

## Hazard 4: Extreme Heat

### Data Sources
| Source | Coverage | Resolution | Access |
|--------|----------|-----------|--------|
| NOAA Climate Normals | US nationwide | Station-level | ncei.noaa.gov (free) |
| First Street Foundation Heat Factor | US nationwide | Property-level | riskfactor.com (paid) |
| NASA NEX-GDDP-CMIP6 | Global | 25km grid | nasa.gov (free) |
| Urban Heat Island mapping | Major metros | Block-level | Various municipal sources |
| OSHA Heat Index Guidelines | US nationwide | N/A | osha.gov (free) |

### Assessment Methodology

**Step 1: Baseline Heat Exposure**
| Metric | Definition | Source |
|--------|-----------|--------|
| Cooling Degree Days (CDD) | Annual sum of (daily avg temp - 65F) | NOAA |
| Extreme heat days | Days above 95F (or local threshold) | NOAA/FSF |
| Heat index days >105F | Combined temperature + humidity | NOAA |
| Urban Heat Island (UHI) premium | Temp differential vs surrounding rural | Municipal data |

**Step 2: Projected Heat Exposure (CMIP6 Scenarios)**
| Scenario | Description | 2050 CDD Increase | 2080 CDD Increase |
|----------|-------------|-------------------|-------------------|
| SSP2-4.5 (middle road) | Moderate mitigation | +15-25% | +25-40% |
| SSP5-8.5 (fossil-fueled) | No mitigation | +25-40% | +50-80% |

**Step 3: Financial Impact Channels**
```
Heat cost impact = cooling_energy_increase
  + equipment_degradation
  + productivity_loss
  + worker_safety_compliance
  + insurance_increase
```

| Impact Channel | Quantification Method |
|---------------|----------------------|
| Cooling energy increase | +3-5% per 1F average temp increase * cooling cost |
| HVAC equipment degradation | Reduced useful life by 10-20% at sustained high temps |
| Chiller capacity shortfall | Risk of insufficient cooling on extreme days (>design temp) |
| Roof/pavement degradation | Accelerated thermal cycling damage |
| Outdoor worker safety | OSHA heat illness prevention compliance costs |
| Tenant productivity | 2-4% productivity loss per degree above 77F indoor |

**Mitigation measures:**
- Cool roofs (high albedo): reduce surface temp 50-80F, 10-15% cooling savings
- Urban tree canopy: 5-10F ambient temp reduction
- Chiller oversizing or N+1 redundancy
- Thermal energy storage (ice storage for peak shifting)

---

## Hazard 5: Sea Level Rise

### Data Sources
| Source | Coverage | Resolution | Access |
|--------|----------|-----------|--------|
| NOAA Sea Level Rise Viewer | US coastal | 1 ft increments | coast.noaa.gov (free) |
| NOAA Technical Report 2022 | US coastal | Tide gauge stations | tidesandcurrents.noaa.gov (free) |
| IPCC AR6 Sea Level Projections | Global | Regional | ipcc.ch (free) |
| USACE Sea Level Change Calculator | US coastal | Station-level | corpsmapu.usace.army.mil (free) |
| Sweet et al. 2022 (interagency) | US coastal | Regional | oceanservice.noaa.gov (free) |

### Assessment Methodology

**Step 1: Current Elevation and Tidal Datum**
- Property elevation (NAVD88 datum): LiDAR data, survey, or USGS 3DEP
- Local mean higher high water (MHHW): NOAA tide gauge
- Freeboard: elevation above MHHW
- Subsidence rate: local land subsidence (critical in Houston, Norfolk, Miami)

**Step 2: Sea Level Rise Projections (NOAA 2022 Scenarios)**
| Scenario | 2050 Rise (ft) | 2100 Rise (ft) | Notes |
|----------|----------------|----------------|-------|
| Low | 0.5 | 1.0 | Strong mitigation, low ice sheet sensitivity |
| Intermediate-Low | 0.7 | 1.6 | Current trajectory lower bound |
| Intermediate | 1.0 | 3.3 | Most likely range for planning |
| Intermediate-High | 1.3 | 4.9 | Higher emissions / ice sheet response |
| High | 1.6 | 6.6 | High emissions + ice cliff instability |

Regional variation matters: Mid-Atlantic and Gulf Coast see faster rise than West Coast.

**Step 3: Tipping Point Analysis**
```
Years to chronic flooding = (property_elevation_above_MHHW - tidal_range) / annual_SLR_rate
```

**Chronic flooding thresholds:**
| Condition | Definition | Impact |
|-----------|-----------|--------|
| Nuisance flooding | >6 events/year at property | Tenant inconvenience, access issues |
| Disruptive flooding | >26 events/year | Operational disruption, insurance trigger |
| Chronic inundation | >100 events/year | Effectively unusable without adaptation |

**Step 4: Financial Impact**
```
SLR_value_impact = adaptation_capex + increased_insurance + reduced_NOI + terminal_value_impairment
```

| Impact Category | Quantification |
|-----------------|---------------|
| Adaptation infrastructure (seawall, elevated utilities) | $50-200/SF of protected area |
| Flood insurance premium increase | 8-18% CAGR for exposed properties |
| Revenue impairment (tenant loss, rent discount) | 5-20% rent discount for flood-prone |
| Mortgage availability | Lenders restricting 30-yr terms in high-SLR zones |
| Terminal value impairment | 10-50% reduction at exit for at-risk coastal |
| Stranded asset risk | Total loss if chronic inundation within economic life |

---

## Portfolio Risk Aggregation

### Composite Physical Risk Score
```
Portfolio_Risk = SUM over assets(
  asset_value_weight * composite_hazard_score_i
)

Composite_Hazard_Score = MAX(hazard_scores)
  + 0.3 * SECOND_HIGHEST(hazard_scores)
```

Use MAX rather than average because the dominant hazard drives the risk profile. The second-highest hazard adds correlated exposure.

### Risk Concentration Metrics
- Geographic concentration: % of portfolio value in single MSA/county
- Hazard correlation: coastal portfolio has correlated flood + wind + SLR
- Insurance coverage ratio: insured value / total exposure per hazard
- Adaptation investment as % of portfolio value

### Reporting Frequency
| Metric | Frequency | Audience |
|--------|-----------|---------|
| Portfolio risk score | Quarterly | Investment committee |
| Property-level hazard assessment | Annually or at acquisition | Asset management |
| Insurance coverage adequacy | Annually (pre-renewal) | Risk management |
| Climate scenario analysis | Annually | Board, LP reporting, TCFD |
| Forward-looking projections update | Every 2-3 years (new IPCC/NOAA data) | Strategic planning |
