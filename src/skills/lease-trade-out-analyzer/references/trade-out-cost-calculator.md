# Trade-Out Cost Calculator

---

## Purpose

This reference provides the complete formula methodology for computing renewal NPV, trade-out NPV, and the breakeven conditions that govern the renewal-vs.-trade-out decision. All formulas in SKILL.md are derived from this reference. Use this document when building a spreadsheet model or when verifying a manual calculation.

---

## Part 1: Renewal NPV Formula

### 1.1 Core Formula

```
NPV_renewal = SUM[ (Renewal_Rent_t - OpEx_t) / (1 + r)^t ]  for t = 1 to T
              - TI_renewal  (upfront, time 0)
              - LC_renewal  (upfront, time 0)
              - Free_Rent_cost  (months 1 to N, discounted at monthly rate)
```

Where:
- `t` = year index (1 to T)
- `T` = analysis period in years (typically match to new lease term; use 10 years for cross-scenario consistency)
- `r` = annual discount rate (default 7%; adjust upward for credit risk on new tenant)
- `Renewal_Rent_t` = annual rental income in year t (apply escalations from Year 1 base)
- `OpEx_t` = landlord operating expense in year t (0 for NNN; full OpEx load for gross leases)
- `TI_renewal` = renewal tenant improvement allowance (upfront cash outflow, $/SF x SF)
- `LC_renewal` = leasing commission for renewal (if broker involved; typically 0-3% of aggregate rent)
- `Free_Rent_cost` = rent forgiven during free rent period

### 1.2 Effective Renewal Rent

Effective rent normalizes the face rent for all landlord concessions amortized over the lease term. This is the true economic rent realized per SF per year.

```
Effective_Rent_renewal = Face_Rent_renewal
                         - (TI_renewal / T)
                         - (LC_renewal / (T x SF))
                         - (Free_Rent_months x Monthly_Rent / (T x 12))
```

Units: $/SF/yr. Compare directly to effective trade-out rent.

### 1.3 Renewal Escalation Schedule

Build the full rent schedule before discounting:

```
Year 1:  Renewal_Rent_base
Year 2:  Renewal_Rent_base x (1 + g)
Year 3:  Renewal_Rent_base x (1 + g)^2
...
Year t:  Renewal_Rent_base x (1 + g)^(t-1)
```

Where `g` = annual rent escalation rate (fixed %; or CPI -- use 2.5-3% as a CPI proxy if not specified).

For stepped increases (common in retail): define `Renewal_Rent_t` explicitly for each year.

### 1.4 No-Downtime Assumption

Renewal scenarios assume 0 months of vacancy between lease expiration and renewal commencement. This is the primary structural advantage of renewal over trade-out and must be preserved as a hard assumption (do not inadvertently add transition costs to the renewal scenario).

---

## Part 2: Trade-Out NPV Formula

### 2.1 Core Formula

```
NPV_tradeout = - Carrying_Cost  (months 1 to V, discounted at monthly rate)
               - Make_Ready  (upfront, time 0)
               - TI_new  (upfront, time 0)
               - LC_new  (upfront, time 0)
               + SUM[ (New_Rent_t - OpEx_t) / (1 + r + risk_premium)^t ]  for t = V/12 to T
```

Where:
- `V` = vacancy duration in months
- `V/12` = vacancy duration in years (fractional years; discount the new tenant cash flows starting at month V+1)
- `Carrying_Cost` = monthly out-of-pocket cost during vacancy x V months
- `Make_Ready` = cost to prepare the vacant space for marketing ($/SF x SF)
- `TI_new` = new tenant TI allowance ($/SF x SF)
- `LC_new` = leasing commission on new lease (% x aggregate rent over new lease term)
- `New_Rent_t` = annual rent from new tenant in year t (post-vacancy; apply new lease escalations)
- `risk_premium` = additional discount rate applied to new tenant cash flows to reflect unknown credit (default: 0bps for rated tenant, 50-100bps for unrated/unknown, 150-200bps for speculative)

### 2.2 Monthly Carrying Cost Components

```
Carrying_Cost_monthly = (Debt_Service_monthly
                        + Property_Tax_monthly
                        + Insurance_monthly
                        + Utilities_minimal_monthly)
                        + OpEx_load (gross leases only; 0 for NNN)

Notes:
  Debt Service: allocate pro-rata SF share of total debt service if space is part of larger asset
  Utilities: minimal climate control and lighting only during vacancy
  For NNN: landlord obligation is limited to base building costs; tenant pays own OpEx
  For Gross/FSG: landlord bears full operating expense load even with no tenant in place
```

Typical carrying cost ranges (NNN):
- Office: $1.50-$3.50/SF/month (primarily taxes + insurance + debt service allocation)
- Retail: $1.25-$3.00/SF/month
- Industrial: $0.75-$2.00/SF/month

### 2.3 Effective Trade-Out Rent

```
Effective_Rent_tradeout = Face_Rent_new
                          - (TI_new / T)
                          - (LC_new / (T x SF))
                          - (Make_Ready / (T x SF))
                          - (Carrying_Cost_total / (T x SF))
```

Where `Carrying_Cost_total` = Carrying_Cost_monthly x V.

This is the true economic rent per SF per year from the trade-out path. A trade-out with $35/SF face rent, $25/SF TI, $95K LC, $50K make-ready, and $100K carrying cost over 10 years and 10,000 SF produces an effective rent of approximately $30.55/SF -- substantially below the $35 face rent.

### 2.4 New Tenant Cash Flow Schedule

```
Months 1-V:    Cash flow = 0 - Carrying_Cost_monthly
Month V+1:     New lease commences; cash flow = New_Rent_monthly (or 0 if free rent period)
Month V+2 ...: New_Rent_monthly x (1 + g/12) per month (monthly escalation; or apply annually)
```

For annual NPV modeling, convert:
```
Year 1: (12-V) months of new rent (if V < 12) + V months of 0
         = New_Rent_annual x (12-V)/12
Year 2: New_Rent_annual x (1 + g)
...
Year T: New_Rent_annual x (1 + g)^(T-1)
```

---

## Part 3: Breakeven Formulas

### 3.1 Breakeven Vacancy Duration

Solve for `V*` (months) such that NPV_renewal = NPV_tradeout:

```
NPV_renewal = NPV_tradeout(V*)

Simplified (holding rent and TI constant):
  NPV_renewal - NPV_tradeout_at_V=0 = V* x PV_factor x Carrying_Cost_monthly
                                    + V* x (deferred rent PV impact)

Approximate formula:
  V* = (NPV_renewal - NPV_tradeout_base) / (Monthly_Carrying_Cost + Monthly_New_Rent_PV_impact)
```

In practice, solve iteratively in a spreadsheet: plug in V = 1, 2, 3... months until NPV_tradeout crosses NPV_renewal. The crossing point is the breakeven vacancy.

**Interpretation**: if expected market vacancy is below V*, the trade-out can win. If expected market vacancy is above V*, renewal wins.

### 3.2 Breakeven New Rent

Solve for `R*` ($/SF/yr) such that NPV_renewal = NPV_tradeout:

```
PV of (R* - Renewal_Rent) x SF x annual discount factor over T years
  = TI_new - TI_renewal + LC_new - LC_renewal + Carrying_Cost_total + Make_Ready
  (approximately, ignoring escalation differences)

R* = Renewal_Rent + [(TI_new - TI_renewal + LC_new - LC_renewal + Carrying_Cost_total + Make_Ready)
      / (SF x PV_annuity_factor(r, T))]
```

Where PV_annuity_factor = SUM[1/(1+r)^t] for t = 1 to T (standard annuity factor).

**Interpretation**: new rent must exceed `R*` for trade-out to win. If `R*` exceeds current market rent, trade-out requires above-market execution -- flag as high risk.

### 3.3 Breakeven TI

Solve for `TI*` ($/SF) such that NPV_renewal = NPV_tradeout:

```
TI* = TI_renewal + (NPV_tradeout_at_TI=0 - NPV_renewal) / SF

Simplified:
  TI* = (NPV_tradeout_base - NPV_renewal) / SF + TI_renewal
  (where NPV_tradeout_base assumes TI_new = 0)
```

**Interpretation**: if market TI exceeds TI*, the trade-out cost structure makes renewal more attractive. Negotiate new tenant TI below TI* or structure as a phased TI disbursement tied to rent commencement.

---

## Part 4: Sensitivity Table Template

Use this table structure for the sensitivity output in Workflow 4. Populate the NPV delta (Trade-Out NPV minus Renewal NPV). Positive = trade-out wins. Negative = renewal wins.

```
SENSITIVITY: NPV Delta ($, Trade-Out minus Renewal)

                         VACANCY DURATION
                    2 mo    4 mo    6 mo    9 mo    12 mo   18 mo
TI:  $10/SF         [+]     [+]     [+/-]   [-]     [-]     [-]
     $15/SF         [+]     [+/-]   [-]     [-]     [-]     [-]
     $20/SF         [+/-]   [-]     [-]     [-]     [-]     [-]
     $25/SF         [-]     [-]     [-]     [-]     [-]     [-]
     $35/SF         [-]     [-]     [-]     [-]     [-]     [-]
     $50/SF         [-]     [-]     [-]     [-]     [-]     [-]

Key:
  [+]   = Trade-out NPV > Renewal NPV by >5%  (trade-out wins)
  [+/-] = NPV delta within 5% (marginal -- use risk-adjusted tiebreaker)
  [-]   = Trade-out NPV < Renewal NPV by >5%  (renewal wins)
```

Also run sensitivity on new rent (rows) vs. vacancy (columns) holding TI at market:

```
                         VACANCY DURATION
                    2 mo    4 mo    6 mo    9 mo    12 mo   18 mo
New Rent: $28/SF    [-]     [-]     [-]     [-]     [-]     [-]
          $30/SF    [-]     [-]     [-]     [-]     [-]     [-]
          $32/SF    [+/-]   [-]     [-]     [-]     [-]     [-]
          $35/SF    [+]     [+/-]   [-]     [-]     [-]     [-]
          $40/SF    [+]     [+]     [+]     [+/-]   [-]     [-]
          $45/SF    [+]     [+]     [+]     [+]     [+/-]   [-]
```

---

## Part 5: TI Payback Period

Compute TI payback as a sanity check separate from the NPV analysis:

```
TI_payback_months = TI_new / (Monthly_Rent_premium)

Where:
  Monthly_Rent_premium = (New_Rent_psf - Renewal_Rent_psf) x SF / 12

Rule of thumb thresholds:
  < 12 months:  Fast payback. TI is not a constraint.
  12-18 months: Acceptable. Standard market range.
  18-24 months: Caution. Requires long lease term to justify.
  > 24 months:  Flag. TI is excessive relative to rent premium.
                Negotiate TI reduction or longer lease term.
  > 36 months:  Hard flag. Trade-out is very unlikely to win on NPV.
```

Example: $35/SF new rent vs. $32/SF renewal, $25/SF TI, 10,000 SF
```
Monthly_Rent_premium = ($35 - $32) x 10,000 / 12 = $2,500/mo
TI_payback = $250,000 / $2,500 = 100 months (8.3 years)
Flag: TI payback of 100 months exceeds typical 5-7 year lease term.
Trade-out cannot recoup TI within the lease term from rent premium alone.
```

---

## Part 6: Discount Rate Selection

| Scenario | Recommended Discount Rate |
|---|---|
| Renewal with credit tenant (rated) | Fund WACC or hurdle rate; typically 6-8% |
| Renewal with non-credit tenant | Add 50-75bps above WACC; typically 6.5-8.5% |
| Trade-out with known credit replacement | Same as renewal credit rate |
| Trade-out with unknown/unrated replacement | Add 75-125bps; typically 7.5-9.5% |
| Trade-out with speculative tenant | Add 150-200bps; typically 8.5-10% |
| Single-tenant building trade-out | Add 100-150bps for concentration risk |

Apply the same base rate to both renewal and trade-out scenarios. Apply the risk premium only to new tenant cash flows in the trade-out scenario (not to the upfront cost outflows, which are certain).

---

## Part 7: Co-Tenancy Adjustment

When co-tenancy clauses exist, adjust the trade-out NPV as follows:

```
Adjusted_NPV_tradeout = NPV_tradeout
                        - PV of co-tenancy rent reductions
                        - PV of co-tenancy termination risks

PV_cotenancy_reductions = SUM[ (Affected_SF x Rent_Reduction_psf x Probability_trigger) / (1+r)^t ]
                          for t = 1 to T_remaining for each affected tenant

If termination risk is present (tenant can terminate if anchor vacates for > N months):
  PV_termination_risk = Termination_probability x NPV_of_losing_that_tenant
  (use tenant-retention-engine NPV model for the affected tenant)
```

Always present co-tenancy-adjusted and unadjusted trade-out NPV separately so decision-makers understand the full exposure range.
