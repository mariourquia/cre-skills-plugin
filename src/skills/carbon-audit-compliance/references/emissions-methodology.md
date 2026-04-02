# Emissions Calculation Methodology for Commercial Real Estate

## Scope Framework (GHG Protocol Applied to Buildings)

### Scope 1: Direct Emissions
On-site combustion from building-owned/controlled sources.

**Sources**
- Natural gas boilers and furnaces (space heating, domestic hot water)
- Diesel/gas-fired emergency generators
- On-site CHP (combined heat and power) plants
- Refrigerant leaks from owned HVAC systems (HFCs)

**Calculation**
```
Scope 1 = SUM(fuel_volume_i * emission_factor_i)
```

| Fuel | Unit | Emission Factor (kgCO2e) |
|------|------|--------------------------|
| Natural gas | therm | 5.31 |
| #2 Fuel oil | gallon | 10.16 |
| Diesel (generator) | gallon | 10.18 |
| Propane | gallon | 5.74 |

**Refrigerant Leakage**
```
Refrigerant emissions = charge_size_kg * annual_leak_rate * GWP
```
- R-410A GWP: 2,088
- R-134a GWP: 1,430
- Typical annual leak rate: 2-10% of charge
- Report when total exceeds de minimis threshold (typically 50 kgCO2e)

### Scope 2: Indirect Emissions (Purchased Energy)
Electricity and district steam/chilled water consumed by the building.

**Location-Based Method**
Uses regional grid average emission factor.
```
Scope 2 (location) = kWh_consumed * eGRID_factor
```

Key eGRID subregion factors (lbCO2e/MWh, 2023):
| Subregion | Factor | Coverage |
|-----------|--------|----------|
| NPCC (NYCW) | 394.7 | NYC metro |
| RFCE | 536.2 | PJM East (DC, Philly) |
| SRMV | 714.3 | Southeast |
| CAMX | 447.1 | California |
| RMPA | 892.6 | Rocky Mountain |
| ERCT | 797.4 | Texas (ERCOT) |

**Market-Based Method**
Uses contractual instruments (RECs, PPAs, utility green tariffs).
```
Scope 2 (market) = (kWh_total - kWh_renewable_contracted) * residual_mix_factor
```
- Renewable energy certificates (RECs): must be from same market/vintage year
- Virtual PPA: financial settlement, paired with RECs
- Utility green tariff: direct enrollment program

**District Energy**
```
District steam: lbs_steam * 0.06686 kgCO2e/lb (NYC ConEd typical)
District chilled water: ton-hours * 0.85 kgCO2e/ton-hr (varies by provider)
```

### Scope 3: Value Chain Emissions
Relevant categories for CRE owners/operators:

| Category | Description | Data Source |
|----------|-------------|-------------|
| Cat 1: Purchased goods | Construction materials, maintenance supplies | Spend-based (EEIO factors) |
| Cat 3: Fuel/energy | Upstream extraction and T&D losses | 8-12% adder on Scope 1+2 |
| Cat 5: Waste | Tenant and operational waste | Waste hauler reports, EPA WARM model |
| Cat 6: Business travel | Corporate travel for asset management | Expense reports |
| Cat 7: Employee commute | Property management staff commute | Survey + distance-based |
| Cat 13: Downstream leased | Tenant-controlled energy in NNN leases | Utility data requests, green lease clauses |

**Category 13 is the largest for NNN landlords.** If tenants pay utilities directly, those emissions are Scope 3 Cat 13 for the owner. This is the "split incentive" problem.

## ENERGY STAR Benchmarking

### Portfolio Manager Methodology
1. Enter 12 consecutive months of utility data (all fuel types)
2. Enter property use details (GFA, operating hours, occupancy, data center presence)
3. System calculates Source EUI and compares to CBECS peer group

**Source vs Site EUI**
```
Source EUI = Site EUI * source-site ratio
```
| Fuel | Source-Site Ratio |
|------|-------------------|
| Electricity | 2.80 |
| Natural gas | 1.05 |
| District steam | 1.20 |
| District chilled water | 1.04 |

Source EUI captures full primary energy including generation and transmission losses.

### ENERGY STAR Score (1-100)
- Regression model: expected source EUI based on property characteristics
- Score = percentile rank of actual vs expected
- Score >= 75: eligible for ENERGY STAR certification
- Median commercial building: score 50, source EUI ~90 kBtu/SF (office)

**Typical Source EUI Ranges (kBtu/SF/yr)**
| Property Type | Bottom Quartile | Median | Top Quartile |
|---------------|-----------------|--------|--------------|
| Office | 55-70 | 90 | 130-160 |
| Multifamily | 60-75 | 95 | 120-150 |
| Retail | 40-55 | 70 | 100-130 |
| Hotel | 90-110 | 140 | 180-220 |
| Hospital | 200-250 | 320 | 400+ |

## Utility Cost per SF Analysis

### Benchmarking Framework
```
Utility Cost Intensity = Total annual utility cost / Gross Leasable Area
```

**National Benchmarks (2024-2025)**
| Property Type | Low | Median | High |
|---------------|-----|--------|------|
| Office (Class A) | $2.00/SF | $3.25/SF | $5.00/SF |
| Office (Class B) | $1.75/SF | $2.75/SF | $4.25/SF |
| Multifamily | $0.80/SF | $1.40/SF | $2.20/SF |
| Industrial | $0.50/SF | $0.90/SF | $1.50/SF |
| Retail (strip) | $1.50/SF | $2.50/SF | $4.00/SF |

**Cost Decomposition**
- Electricity: 55-70% of total utility cost (office/retail)
- Natural gas: 15-25%
- Water/sewer: 8-15%
- Waste removal: 3-8%

### Carbon Intensity Metric
```
Carbon Intensity = Total GHG (kgCO2e) / Gross Floor Area (SF)
```

**Benchmarks (kgCO2e/SF/yr)**
| Property Type | Top Performer | Average | Poor Performer |
|---------------|---------------|---------|----------------|
| Office | 2.5 | 6.0 | 12.0 |
| Multifamily | 2.0 | 5.0 | 9.0 |
| Retail | 2.0 | 4.5 | 8.5 |
| Hotel | 5.0 | 10.0 | 18.0 |

## Local Law 97 (NYC) Penalty Framework

### Timeline
- 2024-2029: Period 1 limits (less stringent)
- 2030-2034: Period 2 limits (significantly tighter)
- 2035+: Limits adjusted every 5 years toward 2050 net-zero

### Emissions Limits (tCO2e/SF/yr)
| Occupancy Group | 2024-2029 | 2030-2034 |
|-----------------|-----------|-----------|
| Office (B) | 0.00846 | 0.00453 |
| Residential (R-2) | 0.00675 | 0.00407 |
| Retail/Mercantile (M) | 0.01109 | 0.00569 |
| Hotel (R-1) | 0.00987 | 0.00526 |
| Healthcare (I-2) | 0.02381 | 0.01330 |
| Assembly (A) | 0.01074 | 0.00569 |
| Educational (E) | 0.00758 | 0.00407 |
| Industrial (F) | 0.00574 | 0.00453 |

### Penalty Calculation
```
Penalty = (Actual_Emissions - Limit) * $268/tCO2e
```

**Worked Example: 500,000 SF Class A Office (NYC)**
- Annual emissions: 5,500 tCO2e
- 2024 limit: 0.00846 * 500,000 = 4,230 tCO2e
- Excess: 5,500 - 4,230 = 1,270 tCO2e
- Annual penalty: 1,270 * $268 = **$340,360/yr**
- 2030 limit: 0.00453 * 500,000 = 2,265 tCO2e
- Excess: 5,500 - 2,265 = 3,235 tCO2e
- Annual penalty: 3,235 * $268 = **$866,980/yr**

### Compliance Pathways
1. Direct emissions reduction (energy efficiency, electrification)
2. Purchase of Renewable Energy Credits (limited, NYC-generated only for certain provisions)
3. Power Purchase Agreements (eligible under certain conditions)
4. Greenhouse Gas Offsets (not currently accepted for LL97)
5. Deduction for purchase of carbon credits via NYC MOCEJ program (if established)
6. Prescriptive compliance path (implement all measures on approved list)

## Green Certification ROI

### LEED (Leadership in Energy and Environmental Design)
| Level | Rent Premium | Value Premium | Certification Cost (100K SF) |
|-------|-------------|---------------|------------------------------|
| Certified | 2-4% | 5-8% | $150K-250K |
| Silver | 4-6% | 8-12% | $200K-350K |
| Gold | 6-10% | 12-18% | $300K-500K |
| Platinum | 8-15% | 15-25% | $500K-800K+ |

### WELL Building Standard
| Level | Rent Premium | Tenant Retention Impact | Certification Cost (100K SF) |
|-------|-------------|------------------------|------------------------------|
| Silver | 3-5% | +5-8% retention | $200K-350K |
| Gold | 5-8% | +8-12% retention | $350K-550K |
| Platinum | 7-12% | +10-15% retention | $500K-800K |

### ENERGY STAR Certification
- Rent premium: 2-5%
- Value premium: 5-10%
- Annual certification cost: $5K-15K (benchmarking + verification)
- ROI: typically 10-20x annual cost via rent premium and operating savings

### Certification Selection Matrix
| Goal | Best Fit |
|------|----------|
| Maximum rent premium, institutional tenants | LEED Gold/Platinum |
| Tenant wellness, tech/creative tenants | WELL Gold + Fitwel |
| Operating cost reduction, quick payback | ENERGY STAR |
| ESG reporting requirement, fund-level | GRESB participation + LEED |
| Existing building, limited capex | ENERGY STAR + LEED O+M |

## Data Collection Checklist

- [ ] 24+ months utility bills (all meters, all fuel types)
- [ ] Property characteristics (GFA, occupancy, operating hours, # units)
- [ ] HVAC equipment inventory (age, type, capacity, refrigerant)
- [ ] Building automation system (BAS) trend logs
- [ ] Submetering data (if available)
- [ ] Tenant utility data (NNN properties -- green lease clause)
- [ ] Waste hauling invoices and diversion reports
- [ ] Refrigerant purchase/recharge records
- [ ] Generator run-hour logs and fuel receipts
- [ ] Solar/on-site generation production data
- [ ] REC/PPA documentation
- [ ] Prior ENERGY STAR scores and benchmarking reports
- [ ] Any existing green certifications and renewal dates
