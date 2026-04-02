# Submarket Analysis Framework: What Brokers Won't Tell You

## Purpose

Strip away marketing spin. Every submarket OM tells you "strong fundamentals" and "growing demand." This framework forces you to verify claims with independent data, identify risks brokers downplay, and build a conviction score before underwriting.

## The Five Pillars

### 1. Supply Pipeline by Quarter

Brokers quote annual deliveries. You need quarterly granularity because timing matters -- a Q1 delivery competing for the same tenant pool during your lease-up is different from a Q4 delivery after you've stabilized.

**What to gather:**

| Field | Source | Why It Matters |
|---|---|---|
| Permits filed (not yet started) | County building dept | 18-24 month forward signal |
| Under construction (SF/units) | CoStar, county records | 12-18 month delivery window |
| Planned/proposed | Planning commission agendas | Speculative but reveals developer sentiment |
| Pre-leased % of pipeline | Broker surveys, CoStar | Separates committed demand from spec risk |
| Conversion/adaptive reuse | Planning dept, news | Often missed -- office-to-resi, hotel-to-apt |

**Red flags brokers won't highlight:**
- Pipeline quoted as annual number hides a Q2 cluster that creates temporary glut
- "Pre-leased" may count LOIs, not executed leases
- Entitled but not yet started projects get excluded from "active pipeline" -- they can break ground any quarter
- Moratoria or impact fee increases signal political backlash against growth (short-term supply constraint, long-term demand question)

**Quarterly pipeline template:**

```
Submarket: [name]
Date compiled: [date]
Existing stock: [units/SF]

| Project | Type | Units/SF | Start | Est Delivery | Pre-leased % | Developer | Notes |
|---------|------|----------|-------|-------------|-------------|-----------|-------|
|         |      |          |       | Q1 20XX     |             |           |       |
|         |      |          |       | Q2 20XX     |             |           |       |
```

Pipeline as % of existing stock:
- < 3%: Tight. Pricing power for existing owners.
- 3-6%: Manageable if absorption is healthy.
- 6-10%: Elevated. Need above-average absorption to avoid rent pressure.
- > 10%: Danger zone. Underwrite flat-to-negative rent growth.

### 2. Absorption-to-Delivery Ratio

The single most important submarket health metric. Brokers cherry-pick the timeframe that looks best. You need trailing 4-quarter and trailing 8-quarter to see the trend.

**Formula:**
```
A/D Ratio = Net Absorption (SF or units) / New Deliveries (SF or units)
```

**Interpretation:**

| A/D Ratio | Signal | Implication |
|---|---|---|
| > 1.5x | Demand significantly outpacing supply | Rent growth accelerating, consider development |
| 1.0 - 1.5x | Healthy equilibrium | Stable rent growth, good for acquisitions |
| 0.7 - 1.0x | Supply catching up | Rent growth moderating, concessions appearing |
| 0.5 - 0.7x | Oversupply forming | Flat to negative rent growth, avoid new acquisitions |
| < 0.5x | Significant oversupply | Rent declines, rising vacancy, distressed opportunities ahead |

**Trend matters more than level.** An A/D of 0.9x that was 1.3x two quarters ago is worse than a steady 0.8x that has been stable for a year. The former signals deterioration; the latter is priced in.

**What brokers do:** Quote peak-quarter absorption annualized. "The submarket absorbed 500,000 SF last year!" -- but 400k was one Amazon BTS in Q2 and organic absorption was 100k against 300k deliveries.

**What you do:** Exclude BTS from both absorption and delivery. Organic absorption is what matters for your rent growth assumptions.

### 3. Effective vs Face Rent

The gap between asking rent and effective rent is the market's true pricing signal. Brokers quote face rent. You need effective.

**Effective Rent Calculation:**
```
Effective Rent = (Face Rent x Lease Term - Concessions) / Lease Term

Example:
Face rent: $30.00/SF NNN
Lease term: 60 months
Free rent: 3 months
TI: $25/SF on 5,000 SF = $125,000
TI amortized monthly: $125,000 / 60 = $2,083/mo = $5.00/SF/yr

Effective Rent = $30.00 - ($30.00 x 3/60) - $5.00
             = $30.00 - $1.50 - $5.00
             = $23.50/SF effective
```

**Concession types to capture:**
- Free rent months (most visible)
- Tenant improvement allowances (often largest dollar impact)
- Moving allowances
- Early termination options (optionality cost to landlord)
- Above-market buyout of existing lease (hidden concession)
- Parking or storage included (normally extra)
- Base year resets on opex escalation

**How to discover true concessions:**
1. Ask leasing brokers directly -- they know the market but also have incentive to inflate
2. Review recent lease comps in CoStar (if available with concession data)
3. FOIA rent rolls for government-financed properties (LIHTC, HUD)
4. Talk to property managers at competing properties (they gossip)
5. Track listings that sit for 60+ days -- the gap between list and done deal is widening

### 4. Shadow Vacancy

Reported vacancy only counts physically vacant space on the market. Shadow vacancy captures the additional risk.

**Shadow vacancy components:**

| Component | Definition | How to Estimate |
|---|---|---|
| Sublease space | Leased but offered back to market | CoStar sublease availability |
| Zombie tenants | Occupied but likely to vacate at expiration | Lease expiration schedule + tenant health |
| Underutilized space | Tenant using <60% of leased SF (remote/hybrid) | Badge data, parking counts, utility usage |
| Dark space | Retail/office occupied per lease but physically closed | Drive the submarket |
| Month-to-month tenants | Technically occupied but zero stickiness | Rent roll analysis |

**Total vacancy = Reported vacancy + Shadow vacancy**

**Example:**
```
Submarket reported vacancy: 7.2%
+ Sublease availability: 2.1%
+ Near-term expirations (12 mo) at risk: 1.8%
+ Estimated underutilization: 1.5%
= Effective vacancy: 12.6%

Broker tells you: "7.2% vacancy, below the long-term average of 8%"
Reality: 12.6% effective vacancy, well above historical average
```

**How to detect shadow vacancy:**
- Track sublease listings separately (CoStar flags these)
- Monitor utility consumption data (some municipalities publish)
- Count cars in parking lots at 2pm on Tuesday (crude but effective for office)
- Review tenant credit / financial health for top 10 tenants by SF
- Ask property managers: "Which tenants are you worried about?"

### 5. Regulatory Risk

The factor most likely to be completely absent from broker materials. Regulation can cap your upside, increase your basis, or make your exit impossible.

**Regulatory risk checklist:**

| Risk | Impact | Detection |
|---|---|---|
| Rent control / stabilization | Caps rent growth below market | State/local statute review |
| Just-cause eviction | Limits ability to reposition | Municipal code review |
| Inclusionary zoning | Requires affordable set-asides | Planning dept, recent approvals |
| Impact / linkage fees | Increases development cost | Fee schedules (changes signal political mood) |
| Building moratorium | Constrains supply (good for existing) | Planning commission minutes |
| Short-term rental restrictions | Affects exit to condo/STR | Municipal code, HOA docs |
| Environmental overlay | Restricts development, adds cost | GIS mapping, FEMA, state DEP |
| Historic preservation | Limits renovation scope | National Register, local designation |
| Property tax reassessment | Post-acquisition tax increase | Assessor methodology, comparable assessments |
| Transfer tax | Transaction friction on exit | State/county rate schedule |

**Emerging regulatory risks (2025-2026):**
- Building performance standards (energy retrofit mandates) -- NYC LL97, DC BEPS
- EV charging requirements for new construction and major renovation
- Embodied carbon disclosure for commercial buildings (CA, WA, CO)
- Beneficial ownership reporting affecting entity structuring
- State-level rent control expansion (CA, OR, MN, CO, CT pending)

## Conviction Scoring

After completing all five pillars, score the submarket:

| Pillar | Weight | Score (1-5) | Weighted |
|---|---|---|---|
| Supply Pipeline | 25% | | |
| A/D Ratio | 25% | | |
| Effective Rent Trend | 20% | | |
| Shadow Vacancy | 15% | | |
| Regulatory Risk | 15% | | |
| **Total** | **100%** | | |

**Interpretation:**
- 4.0 - 5.0: Strong conviction. Underwrite with confidence.
- 3.0 - 3.9: Moderate. Proceed but stress-test aggressively.
- 2.0 - 2.9: Weak. Requires exceptional deal-level economics to overcome.
- < 2.0: Avoid. Submarket headwinds will overwhelm deal-level alpha.

## Common Broker Misdirections

| What They Say | What They Mean | What You Do |
|---|---|---|
| "Strong absorption" | One large deal inflated the number | Decompose into organic vs BTS |
| "Below historical vacancy" | Denominator grew (new stock added) | Look at absolute vacant SF, not rate |
| "Limited new supply" | Entitled projects not yet started | Check entitlements, not just construction |
| "Rents are trending up" | Face rents up, concessions up more | Calculate effective rent trend |
| "Diversified tenant base" | Top 3 tenants are 60% of submarket | Confirm at property and submarket level |
| "Pro-business environment" | Low regulation today, but politics shifting | Read planning commission minutes for 6 months |
| "Irreplaceable location" | Old building that happens to be well-located | Replacement cost irrelevant if functionally obsolete |
