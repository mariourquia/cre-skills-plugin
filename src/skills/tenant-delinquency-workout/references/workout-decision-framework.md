# Tenant Delinquency Workout Decision Framework

## Overview

Three-scenario NPV comparison for delinquent tenants. Every workout decision reduces
to: (A) negotiate a workout, (B) evict and re-lease, or (C) cash-for-keys buyout.
The correct path depends on credit quality, local eviction timelines, re-leasing
probability, and covenant exposure.

---

## 1. Scenario Definitions

### Scenario A: Workout (Reduced Rent / Deferral)

Tenant remains in place under modified terms. Typical structures:

| Modification         | Description                                          |
|----------------------|------------------------------------------------------|
| Temporary abatement  | 0-50% rent reduction for 3-12 months                |
| Deferral + payback   | Deferred rent added to remaining term, amortized     |
| Blend-and-extend     | Lower face rent, extended term, NPV-neutral target   |
| Percentage rent swap | Base rent reduced, percentage rent added on upside    |

**Cash flow model inputs:**

```
modified_rent[t]        = negotiated rent schedule by month
probability_cure        = P(tenant stabilizes and pays modified terms)
probability_default     = 1 - probability_cure
months_to_re_default    = expected months before re-default if cure fails
legal_cost_workout      = attorney fees for lease modification ($2K-$8K)
```

**NPV formula:**

```
NPV_A = sum(t=1..T) [
    probability_cure * modified_rent[t] / (1+r)^t
  + probability_default * (
      sum(t=1..re_default_month) modified_rent[t] / (1+r)^t
      + NPV_B_from(re_default_month)
    )
] - legal_cost_workout
```

### Scenario B: Eviction + Re-Lease

Terminate lease, pursue eviction, re-tenant the space.

**Key variables by jurisdiction:**

| Variable                    | NJ      | NY      | CA      | TX      | FL      |
|-----------------------------|---------|---------|---------|---------|---------|
| Notice to cure (days)       | 30      | 14      | 3       | 3       | 3       |
| Court filing to hearing     | 30-90   | 60-120  | 30-60   | 21-30   | 15-30   |
| Judgment to lockout          | 7-14    | 14-30   | 5-15    | 1-7     | 1-7     |
| Total expected (months)      | 3-6     | 4-8     | 2-5     | 1-3     | 1-3     |
| Commercial vs residential   | Same    | Same    | Faster  | Same    | Same    |

**Cash flow model inputs:**

```
vacancy_months          = eviction_timeline + turnover + lease_up
eviction_legal_cost     = $5K-$25K (jurisdiction dependent)
turnover_cost           = TI + LC + make-ready
market_rent             = current market for comparable space
downtime_carrying_cost  = taxes + insurance + utilities + debt service during vacancy
probability_collection  = P(collecting judgment from departing tenant)
judgment_amount         = back rent + fees owed
```

**NPV formula:**

```
NPV_B = -eviction_legal_cost
        - sum(t=1..vacancy_months) downtime_carrying_cost[t] / (1+r)^t
        + probability_collection * judgment_amount / (1+r)^collection_month
        + sum(t=vacancy_months+1..T) market_rent[t] / (1+r)^t
        - turnover_cost / (1+r)^vacancy_months
```

### Scenario C: Cash-for-Keys

Negotiated departure. Landlord pays tenant to surrender lease and vacate.

**Typical buyout ranges:**

| Tenant Type      | Buyout Range         | Notes                          |
|------------------|----------------------|--------------------------------|
| Retail < $5K/mo  | $5K - $25K          | 1-3 months gross rent          |
| Retail $5-15K/mo | $15K - $75K         | 2-5 months gross rent          |
| Office           | $10K - $100K        | Proportional to remaining TI   |
| Industrial       | $5K - $50K          | Equipment relocation factor    |

**NPV formula:**

```
NPV_C = -buyout_payment / (1+r)^negotiation_months
        - turnover_cost / (1+r)^(negotiation_months + turnover_months)
        + sum(t=departure_month+turnover..T) market_rent[t] / (1+r)^t
```

---

## 2. Credit Quality Decision Tree

```
START: Tenant is delinquent
  |
  +-- Is tenant a national/investment-grade credit?
  |     |
  |     +-- YES: Likely temporary distress. Pursue Scenario A.
  |     |         - Verify: parent guarantee still valid?
  |     |         - Verify: other locations paying?
  |     |         - Structure: deferral with payback, short window
  |     |
  |     +-- NO: Continue to local tenant evaluation
  |
  +-- Is tenant local / single-location operator?
        |
        +-- Assess financial viability:
        |     |
        |     +-- Viable (temporary cash flow issue):
        |     |     - Scenario A with tighter terms
        |     |     - Require personal guarantee enhancement
        |     |     - Monthly financial reporting covenant
        |     |
        |     +-- Marginal (structural decline in business):
        |     |     - Compare NPV of A vs C
        |     |     - Cash-for-keys often optimal here
        |     |     - Avoid extended vacancy of Scenario B
        |     |
        |     +-- Non-viable (business failing):
        |           - Scenario B or C, whichever is faster
        |           - In slow-eviction states: prefer C
        |           - In fast-eviction states: prefer B
        |
        +-- Assess space re-leasing probability:
              |
              +-- High demand submarket (vacancy < 5%):
              |     - Favor B or C (get to market rent faster)
              |
              +-- Soft submarket (vacancy > 10%):
                    - Favor A (occupied space > vacant space)
                    - Even reduced rent beats carrying cost + vacancy
```

---

## 3. Covenant Impact Analysis

Delinquent tenants affect loan covenants. Evaluate before choosing a path.

### DSCR Impact

```
current_DSCR = NOI / annual_debt_service

# Scenario A impact:
modified_NOI_A = NOI - (contract_rent - modified_rent) * 12
DSCR_A = modified_NOI_A / annual_debt_service

# Scenario B impact (during vacancy):
vacancy_NOI_loss = contract_rent * 12 + reimbursements_lost
DSCR_B_vacancy = (NOI - vacancy_NOI_loss) / annual_debt_service

# Scenario B impact (after re-lease):
DSCR_B_stabilized = (NOI - contract_rent*12 + market_rent*12) / annual_debt_service
```

### Occupancy Covenant

Many loans require minimum physical or economic occupancy (typically 80-85%).

```
current_occupancy = leased_sf / total_sf
post_eviction_occupancy = (leased_sf - tenant_sf) / total_sf

# If post_eviction_occupancy < covenant_minimum:
#   -> Triggers reporting requirement or default
#   -> Workout (Scenario A) may be required to avoid breach
```

### Tenant Concentration Covenant

If delinquent tenant is >15-25% of revenue, lender may have approval rights
over any lease modification. Check loan docs for:

- Major tenant definition (usually >10% of GLA or >15% of revenue)
- Lender consent requirements for modifications
- Co-tenancy clause triggers affecting other tenants

### Decision Matrix: Covenant vs Optimal

| Scenario Optimal | Covenant Constraint          | Adjusted Action                    |
|------------------|------------------------------|------------------------------------|
| B (evict)        | Occupancy drops below min    | Pursue A; negotiate lender waiver  |
| A (workout)      | DSCR drops below 1.15x      | Shorten modification; add payback  |
| C (cash-keys)    | Major tenant consent needed  | Get lender approval first          |
| B (evict)        | No constraints               | Proceed with eviction              |

---

## 4. State-Specific Timeline Framework

### Eviction Timeline Components

```
total_eviction_timeline =
    notice_period
  + cure_period (if applicable)
  + court_filing_to_hearing
  + continuances_expected
  + judgment_to_writ
  + writ_to_lockout
  + tenant_appeal_risk_buffer
```

### Jurisdiction Categories

**Fast-Track States (1-3 months typical):**
Texas, Florida, Georgia, Arizona, Colorado, Tennessee

- No right-to-cure for commercial
- Summary proceedings available
- Constable/sheriff execution within days of writ

**Moderate States (3-5 months typical):**
Illinois, Pennsylvania, Ohio, Virginia, Maryland, Massachusetts

- Cure periods common (10-30 days)
- Court backlogs add 30-60 days
- Appeal stays possible but uncommon

**Slow States (4-8+ months typical):**
New York, New Jersey, California, Connecticut, District of Columbia

- Extended cure periods
- Court backlogs 60-120 days
- Tenant attorneys commonly request continuances
- Appeal stays more common
- NJ: discovery rights in commercial evictions
- NY: commercial slightly faster than residential but still slow

### Timeline Adjustment Factors

| Factor                        | Adjustment      |
|-------------------------------|-----------------|
| Tenant retains counsel        | +30-60 days     |
| Tenant files counterclaim     | +60-120 days    |
| Lease has cure provisions     | +30 days        |
| COVID-era moratorium residue  | +0-30 days      |
| Bankruptcy filing (Ch 11)     | +90-365 days    |
| Bankruptcy filing (Ch 7)      | +60-180 days    |

---

## 5. Workout Negotiation Parameters

### Landlord Leverage Indicators

- Strong submarket (low vacancy, rising rents)
- Short remaining lease term (less to lose)
- Tenant has no personal guarantee exposure
- Lease has strong remedies (acceleration, lockout)
- Space is generic / easy to re-tenant

### Tenant Leverage Indicators

- Long remaining term with below-market rent
- Space is specialized / hard to re-tenant
- Tenant is anchor (co-tenancy triggers)
- Slow eviction jurisdiction
- Tenant has strong counsel
- Bankruptcy filing threat is credible

### Modification Term Sheet Template

```yaml
modification_terms:
  effective_date: "YYYY-MM-DD"
  term:
    months_of_modification: 6
    reversion_date: "YYYY-MM-DD"
  rent_schedule:
    months_1_3: 50% of contract rent
    months_4_6: 75% of contract rent
    month_7_onward: 100% of contract rent
  deferred_rent:
    total_deferred: calculated
    payback_method: "amortized over remaining term"
    payback_start: month 7
  additional_security:
    additional_deposit: 2 months rent
    personal_guarantee: required if not existing
    financial_reporting: monthly P&L, quarterly balance sheet
  default_triggers:
    late_payment_cure: 5 days (reduced from 10)
    financial_reporting_miss: event of default
    re_default: all original rent + deferred immediately due
  landlord_protections:
    lease_extension: none (no additional term for concession)
    option_cancellation: tenant renewal options voided
    assignment_restriction: no assignment during modification
```

---

## 6. Decision Output Template

```yaml
workout_decision:
  tenant: "[name]"
  space: "[suite/unit]"
  property: "[address]"
  delinquency:
    months_past_due: X
    amount_owed: $XX,XXX
    last_payment_date: "YYYY-MM-DD"

  scenario_npv:
    A_workout: $XXX,XXX
    B_evict_re_lease: $XXX,XXX
    C_cash_for_keys: $XXX,XXX

  recommended_scenario: "A|B|C"
  reasoning: |
    [2-3 sentence explanation]

  covenant_impact:
    dscr_effect: "X.XXx -> X.XXx"
    occupancy_effect: "XX% -> XX%"
    lender_consent_required: true|false

  timeline:
    scenario_A: "X months to stabilized cash flow"
    scenario_B: "X months vacancy + X months lease-up"
    scenario_C: "X months to vacant + X months lease-up"

  next_steps:
    - "[action 1]"
    - "[action 2]"
    - "[action 3]"
```
