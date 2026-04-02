# Highest and Best Use (HBU) Analysis Framework

## Overview

Structured framework for HBU analysis following the four-test methodology:
legally permissible, physically possible, financially feasible, and maximally
productive. Includes entitlement probability adjustment and the Linneman
land-to-total-development-cost test.

---

## 1. HBU Four-Test Matrix

### Test Sequence

The four tests are applied sequentially. Each test eliminates uses that fail
before proceeding to the next. Only uses surviving all four tests can be HBU.

```
ALL POTENTIAL USES
       |
       v
Test 1: Legally Permissible
       |  Eliminates: uses not allowed by zoning, deed restrictions,
       |  environmental regulations, or applicable law
       v
LEGALLY PERMITTED USES
       |
       v
Test 2: Physically Possible
       |  Eliminates: uses the site cannot support due to size, shape,
       |  topography, soils, access, utilities, or environmental constraints
       v
PHYSICALLY FEASIBLE USES
       |
       v
Test 3: Financially Feasible
       |  Eliminates: uses where completed property value does not exceed
       |  total development cost (land + hard + soft costs)
       v
FINANCIALLY FEASIBLE USES
       |
       v
Test 4: Maximally Productive
       |  Selects: the use that produces the highest residual land value
       |  (or highest return on investment)
       v
HIGHEST AND BEST USE
```

---

## 2. Test 1: Legally Permissible

### Zoning Analysis Checklist

```yaml
zoning_analysis:
  current_zoning:
    zone_designation: "[e.g., R-5, C-2, M-1]"
    permitted_uses_by_right: ["list of uses"]
    conditional_uses: ["list of conditional/special permit uses"]
    prohibited_uses: ["list"]
    density_regulations:
      max_far: "[X.XX]"
      max_lot_coverage: "[XX%]"
      max_building_height: "[X feet / X stories]"
      max_units_per_acre: "[X units]"
      min_lot_size: "[X SF]"
    setbacks:
      front: "[X feet]"
      side: "[X feet]"
      rear: "[X feet]"
    parking_requirements:
      residential: "[X spaces per unit]"
      office: "[X spaces per 1,000 SF]"
      retail: "[X spaces per 1,000 SF]"
    open_space: "[X% of site]"

  overlay_districts:
    historic: true/false
    flood_zone: "[zone designation]"
    environmental_sensitive: true/false
    airport_noise: true/false
    transit_oriented: true/false
    impact: "[description of additional restrictions or incentives]"

  deed_restrictions:
    private_covenants: "[list]"
    easements: "[list]"
    development_agreements: "[list]"
    expiration: "[dates if applicable]"

  entitlement_path:
    by_right: "Uses permitted without discretionary approval"
    variance: "Minor deviations from zoning (hardship required)"
    special_permit: "Conditional use requiring public hearing"
    rezoning: "Change of zone designation (legislative act)"
    planned_development: "Negotiated development plan"
```

### Rezoning Probability Assessment

```yaml
rezoning_probability:
  factors:
    comprehensive_plan_consistency:
      description: "Does proposed use align with municipality's comprehensive plan?"
      weight: 0.25
      scoring:
        consistent: 0.80  # High probability factor
        neutral: 0.50
        inconsistent: 0.15

    adjacent_land_use:
      description: "Is proposed use compatible with surrounding uses?"
      weight: 0.20
      scoring:
        compatible: 0.85
        mixed: 0.50
        incompatible: 0.20

    infrastructure_capacity:
      description: "Can existing infrastructure support proposed use?"
      weight: 0.15
      scoring:
        adequate: 0.90
        needs_upgrade: 0.60
        insufficient: 0.25

    political_environment:
      description: "Community and political support for proposed use"
      weight: 0.20
      scoring:
        supportive: 0.85
        neutral: 0.50
        opposition: 0.15

    precedent:
      description: "Have similar rezonings been approved in the area?"
      weight: 0.10
      scoring:
        strong_precedent: 0.85
        some_precedent: 0.55
        no_precedent: 0.30

    economic_benefit:
      description: "Does proposed use generate tax revenue and jobs?"
      weight: 0.10
      scoring:
        significant: 0.80
        moderate: 0.55
        minimal: 0.35

  calculation:
    formula: "sum(factor_score * weight) for all factors"
    result_interpretation:
      above_0.70: "Probable approval (proceed with application)"
      0.45_to_0.70: "Uncertain (proceed with caution, build community support)"
      below_0.45: "Unlikely (consider alternative uses or sites)"

  timeline_by_jurisdiction:
    small_municipality: "3-6 months"
    mid_size_city: "6-12 months"
    large_city: "12-24 months"
    with_eir_required: "Add 6-18 months"
    with_litigation_risk: "Add 12-36 months"
```

---

## 3. Test 2: Physically Possible

### Site Capability Assessment

```yaml
physical_analysis:
  site_characteristics:
    total_acreage: "[X.XX acres]"
    usable_acreage: "[X.XX acres]"  # Net of easements, setbacks, wetlands
    net_to_gross_ratio: "[XX%]"
    shape: "[Regular/Irregular]"
    frontage: "[X feet on [road name]]"
    depth: "[X feet]"
    topography:
      grade: "[Flat/Gentle/Moderate/Steep]"
      elevation_change: "[X feet across site]"
      grading_cost_estimate: "$[per cubic yard]"
    soils:
      bearing_capacity: "[psf]"
      drainage: "[Good/Moderate/Poor]"
      contamination: "[None/Suspected/Confirmed]"
      remediation_estimate: "$[if applicable]"

  utilities:
    water: "[Available/Requires extension of [X] feet / Not available]"
    sewer: "[Available/Requires extension / Septic only]"
    electric: "[Capacity: [X] kVA]"
    gas: "[Available / Not available]"
    telecom: "[Fiber / Cable / Limited]"
    utility_extension_cost: "$[if applicable]"

  access:
    road_frontage: "[X] feet on [road name]"
    road_classification: "[Arterial/Collector/Local]"
    traffic_count: "[AADT]"
    turn_lanes: "[Required/Existing/N/A]"
    secondary_access: "[Available/Not available]"
    public_transit: "[Distance to nearest stop/station]"

  environmental:
    wetlands: "[Delineated: X acres / None]"
    flood_zone: "[Zone A/AE/X/None]"
    endangered_species: "[Present/Not present/Study needed]"
    phase_i_esa: "[Clean/RECs identified]"
    tree_preservation: "[Required / Not required]"

  development_envelope:
    formula: "Total site - setbacks - easements - wetlands - infrastructure"
    buildable_area: "[X SF]"
    max_building_footprint: "[X SF]"  # Based on lot coverage
    max_gfa: "[X SF]"  # Based on FAR
    max_units: "[X units]"  # Based on density
    max_parking: "[X spaces]"  # Surface or structured
```

---

## 4. Test 3: Financially Feasible

### Residual Land Value Method

The core HBU feasibility test: does the completed project value exceed
total development cost INCLUDING land cost?

```
Residual Land Value = Completed Property Value - Development Cost (ex-land)

Where:
  Completed Property Value = Stabilized NOI / Cap Rate
                          OR Comparable sales $/SF * GFA
                          OR Unit count * Value per unit

  Development Cost (ex-land) = Hard Costs + Soft Costs + Financing + Developer Profit

If Residual Land Value > 0: use is financially feasible
If Residual Land Value > Asking Price: use justifies the land price

The HBU is the use with the HIGHEST residual land value.
```

### Development Cost Estimation

```yaml
cost_estimation:
  hard_costs:  # Per SF of GFA, varies by use and market
    multifamily:
      garden_style: 150  # $/SF
      mid_rise_wood: 200
      mid_rise_concrete: 275
      high_rise: 400
    office:
      suburban_low_rise: 175
      mid_rise: 250
      high_rise_class_a: 450
    retail:
      strip_center: 125
      lifestyle_center: 200
      enclosed_mall: 300
    industrial:
      warehouse: 75
      distribution: 90
      flex: 125
    hotel:
      limited_service: 150
      full_service: 300
      luxury: 500

  soft_costs_as_pct_of_hard:
    architecture_engineering: "6-10%"
    permits_fees: "2-5%"
    legal: "1-2%"
    insurance: "1-2%"
    accounting: "0.5-1%"
    marketing_leasing: "2-4%"
    contingency: "5-10%"
    total_soft: "20-35% of hard costs"

  financing_costs:
    construction_loan_interest: "Rate * Average balance * Construction period"
    origination_fee: "1-2% of loan amount"
    interest_reserve: "Included in loan sizing"

  developer_profit:
    typical_margin: "15-25% of total cost (or 8-12% of value)"
    risk_adjustment: "Higher margin for riskier projects"
```

---

## 5. Test 4: Maximally Productive

### Residual Land Value Comparison

```
Use         | Completed Value | Dev Cost (ex-land) | Residual Land | $/SF Land
------------|-----------------|--------------------|--------------|-----------
MF Garden   | $18,500,000     | $14,200,000        | $4,300,000   | $19.72
MF Mid-Rise | $28,000,000     | $23,500,000        | $4,500,000   | $20.64
Office      | $22,000,000     | $19,800,000        | $2,200,000   | $10.09
Retail      | $12,500,000     | $10,200,000        | $2,300,000   | $10.55
Industrial  | $8,000,000      | $6,500,000         | $1,500,000   | $6.88

HBU = MF Mid-Rise ($4,500,000 residual = $20.64/SF)
```

### Return on Cost Analysis (Alternative Test)

```
Return on Cost = Stabilized NOI / Total Development Cost (including land)

Use         | Stabilized NOI | Total Cost + Land | Return on Cost
------------|----------------|-------------------|---------------
MF Garden   | $1,200,000     | $18,100,000       | 6.63%
MF Mid-Rise | $1,750,000     | $27,400,000       | 6.39%
Office      | $1,400,000     | $23,700,000       | 5.91%
Retail      | $850,000       | $14,100,000       | 6.03%
Industrial  | $560,000       | $10,400,000       | 5.38%

HBU by ROC = MF Garden (6.63%)
Note: ROC may rank differently than residual land value
Use residual land value as primary metric per appraisal standards
```

---

## 6. Linneman Land-to-TDC Test

### Framework

Dr. Peter Linneman's heuristic: land cost should generally represent
15-25% of total development cost (TDC) for a project to be financially
feasible. If land exceeds 30% of TDC, the project is likely over-paying.

```
Land-to-TDC Ratio = Land Cost / Total Development Cost

Where:
  Total Development Cost = Land + Hard Costs + Soft Costs + Financing + Profit

Benchmarks:
  < 15%:  Land may be undervalued or site has challenges (access, zoning)
  15-25%: Healthy range for most development types
  25-30%: Expensive land market; project is feasible but tight
  > 30%:  Danger zone. Project economics depend on aggressive assumptions.
          Either land is overpriced or the use is wrong.
```

### By Property Type

```yaml
land_to_tdc_benchmarks:
  multifamily:
    garden_suburban: "10-20%"
    mid_rise_urban: "15-25%"
    high_rise_urban: "20-35%"
  office:
    suburban: "10-20%"
    cbd: "20-35%"
  retail:
    strip_center: "15-25%"
    power_center: "10-20%"
    urban_ground_floor: "20-40%"
  industrial:
    warehouse: "15-25%"
    distribution: "10-20%"
    infill: "20-35%"
  hotel:
    limited_service: "10-20%"
    full_service_urban: "20-35%"

  special_situations:
    entitled_land: "Premium justified (add 5-10% to range)"
    raw_unentitled: "Discount required (subtract 5-10%)"
    brownfield: "Remediation cost reduces effective land cost"
    land_lease: "Capitalize ground rent; may appear as 0% but has ongoing cost"
```

### Decision Framework

```
IF land_to_tdc < 15%:
  -> Site likely has deficiencies or entitlement risk
  -> May be opportunity if challenges are solvable
  -> Investigate: why is this cheap?

IF land_to_tdc = 15-25%:
  -> Proceed with standard underwriting
  -> Project economics should work at market rents and normal absorption

IF land_to_tdc = 25-30%:
  -> Stress test aggressively
  -> Requires above-average rents or below-average construction costs
  -> Consider: is there a higher-density use that improves the ratio?

IF land_to_tdc > 30%:
  -> Red flag: developer may be overpaying
  -> Only works if: luxury product, irreplaceable location, or
     extraordinary demand (e.g., last developable parcel in supply-constrained market)
  -> Ask: at what rent level does this project breakeven?
  -> If breakeven rent > 90th percentile of market: DO NOT PROCEED
```

---

## 7. Entitlement Probability Adjustment

### Risk-Adjusted Land Value

```
Risk-Adjusted Land Value = Residual Land Value * P(entitlement) - Entitlement Costs

Where:
  P(entitlement) = Probability of obtaining required approvals
  Entitlement Costs = Legal + Engineering + Application fees + Carrying costs

Example:
  Residual land value (if entitled for MF): $4,500,000
  P(rezoning approval): 0.65
  Entitlement costs: $350,000
  Entitlement timeline: 18 months
  Carrying cost during entitlement: $180,000 (land taxes, interest)

  Risk-adjusted value = ($4,500,000 * 0.65) - $350,000 - $180,000
                      = $2,925,000 - $530,000
                      = $2,395,000

  Maximum land purchase price: $2,395,000
  (vs $4,500,000 if already entitled -- 47% discount for entitlement risk)
```

### Entitlement Risk Discount Table

```
P(Entitlement) | Appropriate Discount | Scenario
---------------|---------------------|----------
  > 90%        | 5-10%               | By-right development, minor variances
  70-90%       | 10-25%              | Special permit, supportive community
  50-70%       | 25-45%              | Rezoning required, mixed community support
  30-50%       | 45-65%              | Significant opposition, uncertain politics
  < 30%        | 65-80%+             | Major rezoning, strong opposition, legal risk
```

---

## 8. HBU Report Template

```yaml
hbu_report:
  property:
    address: "[address]"
    parcel_id: "[APN]"
    total_area: "[X acres / X SF]"
    current_use: "[description]"
    current_zoning: "[zone]"

  test_1_legally_permissible:
    by_right_uses: ["list"]
    conditional_uses: ["list"]
    uses_requiring_rezoning: ["list"]
    deed_restrictions: "[description or none]"
    surviving_uses: ["uses passing Test 1"]

  test_2_physically_possible:
    key_constraints: ["list of physical limitations"]
    max_development_potential:
      use_1: "[X SF / X units]"
      use_2: "[X SF / X units]"
      use_3: "[X SF / X units]"
    surviving_uses: ["uses passing Tests 1 and 2"]

  test_3_financially_feasible:
    for_each_surviving_use:
      - use: "[type]"
        completed_value: "$X"
        development_cost: "$X"
        residual_land_value: "$X"
        feasible: true/false
    surviving_uses: ["uses passing Tests 1, 2, and 3"]

  test_4_maximally_productive:
    ranking:
      1: {use: "[type]", residual_land_value: "$X"}
      2: {use: "[type]", residual_land_value: "$X"}
      3: {use: "[type]", residual_land_value: "$X"}

  conclusion:
    highest_and_best_use: "[type]"
    residual_land_value: "$X"
    land_to_tdc_ratio: "XX%"
    entitlement_adjusted_value: "$X"
    recommended_action: "[develop as-of-right / pursue rezoning / sell to developer]"
```
