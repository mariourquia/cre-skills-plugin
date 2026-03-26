# Option Interaction Matrix Reference

## Overview

Lease options do not exist in isolation. When a tenant holds multiple options,
or when multiple tenants hold options on overlapping space, the combinations
create interactions that range from reinforcing to contradictory to legally
incompatible. This reference maps common combinations, classifies them, and
provides collision-detection rules for use in the Existing Options Impact
Analysis workflow.

---

## 1. Single-Tenant Option Combination Matrix

How options interact when held by the same tenant on the same lease.

```
Combination                           Compatible?   Classification   Notes
------------------------------------  -----------   ---------------  ------------------------------------------
Renewal + Expansion ROFO              Yes           Reinforcing      Standard package; no conflict
Renewal + Contraction                 Conditional   Interdependent   Contraction must complete before renewal
                                                                     notice window opens; sequence carefully
Renewal + Termination                 Partial       Limiting         Termination overrides renewal if exercised.
                                                                     Restrict termination window to mid-term
                                                                     only; never allow termination in the 12-18
                                                                     months before renewal notice deadline.
Renewal + Purchase Option             Yes           Reinforcing      Purchase is often exercisable only during
                                                                     renewal terms; aligned
Expansion (committed) + ROFO same sf  Redundant     Inefficient      Committed expansion supersedes ROFO on
                                                                     same space; ROFO adds no value -- remove it
Expansion (committed) + ROFR same sf  Redundant     Inefficient      Same as above; ROFR is irrelevant once
                                                                     expansion is committed
ROFO + ROFR same space                Redundant     Landlord risk    ROFR subsumes ROFO. Granting both gives
                                                                     tenant two bites. Pick one (ROFO preferred).
Contraction + Co-tenancy right        Linked        Cascade risk     If contraction reduces anchor's occupancy
                                                                     below co-tenancy threshold, other tenants'
                                                                     co-tenancy rights may trigger simultaneously.
                                                                     Model before granting contraction to anchors.
Termination + Purchase option         Compatible    Alternative      Tenant can choose between exit strategies.
                                                                     Ensure windows don't overlap (can't terminate
                                                                     and exercise purchase simultaneously).
Expansion + Termination               Contradictory Value transfer   Tenant expands (gets more space) then
                                                                     terminates (gives it all back). Net result:
                                                                     landlord has new TI exposure on expanded
                                                                     space with no guarantee of recovery.
                                                                     If both are granted: ensure termination fee
                                                                     covers TI on expanded space too.
Contraction + Termination             Excessive     Option stack     Tenant can shrink then exit. Creates
                                                                     month-to-month economics. Avoid granting
                                                                     both on same lease without significant
                                                                     fee and notice period structures.
Multiple renewal options (3+)         Conditional   WALT extension   3+ options = 15+ years of optional occupancy.
                                                                     Positive for WALT if at FMV; negative if
                                                                     below-market rates lock in value transfer.
                                                                     Limit to 2 renewals for most tenants.
```

---

## 2. Multi-Tenant Option Collision Detection

How options from different tenants interact when they cover the same space or event.

### Collision Type 1: Space Competition

Two tenants hold rights on the same physical space.

```
Scenario A: Two tenants have ROFO on Suite 500
  Problem: Landlord delivers ROFO notice to both simultaneously.
           Which tenant has priority? Legal conflict.
  Resolution:
    - Establish priority order in each lease: "This ROFO is subordinate to
      the ROFO held by [Tenant X] as of [date]."
    - Priority typically by: first-executed lease, or by negotiated rank.
    - Document priority in both leases at signing.
    - Do not grant overlapping ROFOs without explicit priority language.

Scenario B: Two tenants have ROFR on Suite 500
  Problem: If landlord receives third-party offer, which tenant matches first?
  Resolution:
    - Grant ROFR to only one tenant per space.
    - If second tenant demands ROFR, offer ROFO (weaker right) as substitute.
    - Alternative: grant ROFR to Tenant A with explicit subordination of Tenant B's
      right to a ROFO that triggers only if Tenant A declines.

Scenario C: Tenant A has committed expansion option on Space X;
            Tenant B has ROFO on Space X.
  Problem: When Tenant A exercises expansion, Tenant B's ROFO triggers.
           But the space is not available to Tenant B -- it's being taken.
  Resolution:
    - Tenant B's ROFO must explicitly state: "This ROFO is subordinate to the
      expansion option held by [Tenant A] pursuant to their lease dated [date]."
    - If not documented: legal dispute, potential damages claim from Tenant B.
    - Lesson: always check committed expansion options before granting any ROFO/ROFR.
```

### Collision Type 2: Co-Tenancy Cascade

One tenant's option exercise triggers another tenant's co-tenancy right.

```
Scenario: Anchor tenant has contraction right. Inline tenants have co-tenancy rights.

  Threshold: Inline co-tenancy clauses trigger if anchor occupancy < 25,000 SF.
  Anchor's current space: 30,000 SF.
  Contraction: anchor contracts to 20,000 SF (below threshold).
  Result: 8 inline tenants activate reduced rent or termination right simultaneously.
  NOI impact: potentially -40% of inline NOI in addition to anchor contraction loss.

  Detection: Before granting anchor contraction, map all co-tenancy clauses and
  thresholds in the rent roll. Test whether post-contraction occupancy breaches any.

  Resolution options:
    1. Require anchor to execute co-tenancy waiver from all affected inlines
       before contraction right is added to lease.
    2. Restrict contraction minimum: anchor cannot go below 25,001 SF (the threshold).
    3. Do not grant contraction right.
```

### Collision Type 3: Termination Creates Isolation

One tenant's termination or contraction isolates another tenant's space.

```
Scenario: Tenant A occupies floors 3-5 of a building. Tenant B occupies suite 3A.
  Suite 3A is accessible only through Tenant A's reception.
  Tenant A has termination option for floors 3-5.
  If exercised: Tenant B's suite is inaccessible.

  Detection: Map all space physically. Flag any suite whose only egress route
  passes through another tenant's exclusive space.

  Resolution:
    - Restrict Tenant A's termination to floors 4-5 only (floor 3 must remain).
    - Or require Tenant A to cooperate in creating independent access for Tenant B
      at Tenant A's expense.
    - Or include relocation right: landlord can relocate Tenant B to comparable
      space within building at landlord's cost if Tenant A terminates.
```

### Collision Type 4: ROFR Chills Anchor Replacement

ROFR granted to a small tenant interferes with anchor re-tenanting.

```
Scenario: Anchor space (40,000 SF) becomes vacant. Landlord negotiates with
  replacement anchor. A small inline tenant holds ROFR on "any space in the center."
  The inline tenant's ROFR technically covers the anchor space.
  Inline tenant exercises ROFR, disrupting anchor replacement.

  Note: This is an extreme edge case, but it has occurred.

  Prevention:
    - Never grant ROFR on "any space in the center" -- always define specific suites.
    - Exclude anchor spaces explicitly from any inline tenant's ROFO/ROFR.
    - Standard exclusion language: "Notwithstanding the foregoing, this ROFR
      shall not apply to any space of 20,000 SF or more, or any space designated
      as anchor space in the site plan attached hereto."
```

---

## 3. Option Stack Test

Use this test to determine whether a lease's cumulative options create effectively
month-to-month economics.

```
For any lease, calculate the "minimum committed term" at any given point:

  At any moment in time, the tenant is obligated to pay rent for:
    remaining_base_term
    minus: any termination option exercisable within that period
           (weighted by notice period, not exercise date)
    minus: any contraction reducing NOI exposure

  If minimum_committed_term < 3 years at any point after lease year 2:
    the option stack has destroyed the lease's collateral value.

Example (10-year lease with multiple options):
  Year 0:    10 years committed
  Year 2:    Contraction right exercisable (12-month notice) -- tenant can shrink
  Year 3:    Contraction effective -- tenant commits to remaining 7 years, smaller SF
  Year 5:    Termination right exercisable (18-month notice) -- commit 1.5 yrs only
  Year 6.5:  Termination effective -- tenant exits

At year 5, the tenant's minimum commitment = 18 months.
This is effectively month-to-month economics from lender's perspective.
Result: lenders may treat the lease as expiring in year 5 for DSCR purposes.

Remedy: Never grant both contraction and termination on the same lease without
ensuring at least 4 years of committed term remains after all options are
considered and modeled at their earliest exercise dates.
```

---

## 4. Option Coherence Best Practices

Rules for building an internally consistent option package.

```
Rule 1: Sequence options logically
  Options that modify space (contraction, expansion) should expire before
  options that affect the term (renewal, termination). A tenant should not
  be able to contract, then renew the contracted space, then re-expand.
  If allowing this, document the interaction explicitly.

Rule 2: Define all trigger events precisely
  "When the space becomes available" is ambiguous. Define:
    - What constitutes "available" (vacated, lease expired, landlord not
      in active negotiations, landlord has delivered notice to current tenant)
    - Who determines availability (landlord's written notice)
    - The window for exercise (calendar days, not business days)
    - What happens if tenant fails to exercise (right lapses for that instance)

Rule 3: Terminate options on default
  All options should automatically terminate upon:
    - Tenant default not cured within the applicable cure period
    - Tenant's assignment or sublease without landlord consent
    - Tenant's bankruptcy filing (options are property of the estate -- address separately)
  Include: "Any option granted herein shall be void and of no force and effect
  if Tenant is in default, beyond applicable cure periods, at the time of exercise."

Rule 4: No option within an option
  Avoid constructs where exercising one option grants a new option:
    Example to avoid: "If Tenant exercises the Expansion Option for Suite 400,
    Tenant shall have a Right of First Refusal on Suite 401."
    This creates a chain of contingent rights that is difficult to track.
    Instead: grant all options upfront with clear geographic scope.

Rule 5: Limit option transferability
  Options should be personal to the named tenant. They do not transfer
  in an assignment or sublease unless landlord expressly consents.
  Include: "The options set forth herein are personal to [Tenant Name] and
  may not be exercised by, or transferred to, any assignee or subtenant
  without Landlord's prior written consent."

Rule 6: Estoppel obligations
  At each lease amendment, re-certify the status of all options in the
  tenant's estoppel certificate: which have been exercised, which remain,
  which have lapsed. This prevents disputes at sale or refinancing.
```

---

## 5. Option Register Template

Maintain this register for every property. Update at each lease execution,
amendment, or option exercise.

```
Property: [Name]
As of: [Date]
Maintained by: [Asset Manager Name]

| # | Tenant    | Option Type    | Space Covered  | Trigger              | Notice   | Response | Priority | Status     | Last Verified |
|---|-----------|----------------|----------------|----------------------|----------|----------|----------|------------|---------------|
| 1 | Acme Corp | Renewal        | Suite 200      | Lease exp 12/31/28   | 12 mo    | N/A      | N/A      | Active     | 2025-06-01    |
| 2 | Acme Corp | Expansion ROFO | Suite 210      | Vacancy + LL notice  | N/A      | 10 days  | 1st      | Active     | 2025-06-01    |
| 3 | Beta LLC  | Renewal        | Suite 300      | Lease exp 06/30/27   | 9 mo     | N/A      | N/A      | Active     | 2025-06-01    |
| 4 | Beta LLC  | ROFO           | Suite 310      | Vacancy + LL notice  | N/A      | 10 days  | 2nd*     | Active     | 2025-06-01    |
| 5 | Gamma Inc | Termination    | Suite 150      | Mid-term (yr 5 only) | 15 mo    | N/A      | N/A      | Lapsed**   | 2025-06-01    |

Notes:
  * Beta LLC's ROFO on Suite 310 is subordinate to Acme Corp's ROFO on Suite 210.
    Suite 310 is adjacent to Suite 210. If Acme exercises ROFO on Suite 210,
    Beta's right does not apply to Suite 210. If Acme declines, Beta has no right
    to Suite 210 (Beta's ROFO is Suite 310 only).
  ** Gamma Inc's termination option lapsed on 2025-03-31 (year 5 window closed).
     No further termination right exists under current lease.

Collision Map:
  Suite 210/310 adjacency: Acme ROFO (1st priority) confirmed before Beta ROFO (2nd priority).
  No other collisions detected as of this date.
```

---

## 6. Option Language Cheat Sheet

Short-form drafting templates for common options. Always pass to legal counsel
for final documentation. These are negotiating starting points.

### Renewal Option (FMV with Floor)

```
Renewal Option. Provided Tenant is not in default, Tenant shall have [one (1) / two (2)]
option(s) to renew this Lease for one (1) additional period(s) of [five (5)] years each
(each, a "Renewal Term") on the following terms: (a) Tenant shall deliver written notice
of exercise no later than [twelve (12)] months prior to the expiration of the then-current
term; (b) the Base Rent for the Renewal Term shall be the Fair Market Rent for comparable
space in the [Submarket], as mutually agreed upon by the parties within thirty (30) days
of Tenant's notice, provided that in no event shall the Base Rent for any Renewal Term
be less than the Base Rent in effect immediately prior to such Renewal Term; and (c) all
other terms and conditions of this Lease shall remain unchanged. If the parties fail to
agree on Fair Market Rent within thirty (30) days, each party shall appoint an MAI-certified
appraiser within fifteen (15) days thereafter, and the two appraisers shall together
determine Fair Market Rent; if the appraisers disagree, they shall jointly appoint a
third appraiser whose determination shall be final and binding.
```

### Expansion Right of First Offer (ROFO)

```
Right of First Offer. Provided Tenant is not in default and this Lease is in full force
and effect, if Landlord desires to lease [Suite 210 / any space on the Xth floor / the
adjacent space described on Exhibit __] (the "ROFO Space"), Landlord shall first offer
such space to Tenant in writing at the rent and on the terms Landlord proposes to offer
to third parties. Tenant shall have ten (10) business days following Landlord's written
offer to accept such offer by written notice to Landlord. If Tenant fails to respond
within such ten (10) business day period, or declines to accept Landlord's offer, Landlord
may lease the ROFO Space to any third party at rent no less than ninety-five percent (95%)
of the rent offered to Tenant and on terms no more favorable to such third party than those
offered to Tenant. This Right of First Offer is personal to [Tenant Name], may not be
assigned or transferred, and shall expire upon any assignment or sublease of this Lease.
```

### Contraction Right

```
Contraction Right. Provided Tenant is not in default, Tenant shall have a one-time right
to surrender approximately [XX,000] rentable square feet of the Premises (the "Surrendered
Space"), subject to the following conditions: (a) Tenant shall deliver written notice of
exercise no earlier than [Month XX] and no later than [Month XX] of the Lease Term;
(b) the effective date of surrender shall be no earlier than [twelve (12) / fifteen (15)]
months following Tenant's written notice; (c) simultaneously with the delivery of Tenant's
notice, Tenant shall pay to Landlord a contraction fee equal to [the unamortized portion
of the Tenant Improvement Allowance and leasing commissions paid by Landlord attributable
to the Surrendered Space, plus [X] months of Base Rent at the then-current rate for the
Surrendered Space]; and (d) Tenant shall demise the Surrendered Space in accordance with
a plan approved by Landlord in writing, at Tenant's cost, prior to the surrender date.
The Surrendered Space shall be as shown on Exhibit __ attached hereto.
```

### Termination Option

```
Termination Option. Provided Tenant is not in default, Tenant shall have a one-time option
to terminate this Lease effective as of [specific date / any date after Month XX] (the
"Termination Date"), subject to the following conditions: (a) Tenant shall deliver written
notice of exercise no later than [eighteen (18)] months prior to the Termination Date;
(b) simultaneously with the delivery of Tenant's notice, Tenant shall pay to Landlord a
termination fee equal to (i) the unamortized balance of the Tenant Improvement Allowance
paid by Landlord as of the Termination Date, calculated using a straight-line amortization
over the initial Lease Term; (ii) the unamortized balance of leasing commissions paid by
Landlord, calculated on the same basis; and (iii) [nine (9)] months of Base Rent at the
rate in effect at the time of notice; and (c) Tenant shall vacate and surrender the
Premises in broom-clean condition on or before the Termination Date.
```

### Right of First Refusal (ROFR) on Adjacent Space

```
Right of First Refusal. Provided Tenant is not in default and this Lease is in full force
and effect, if Landlord receives and intends to accept a bona fide, arm's-length offer from
a third party to lease [the ROFR Space described on Exhibit __], Landlord shall deliver to
Tenant a copy of such offer and Tenant shall have five (5) business days to exercise this
Right of First Refusal by written notice to Landlord, agreeing to lease the ROFR Space on
the identical terms and conditions of such third-party offer. If Tenant fails to respond
within such five (5) business day period, or declines to exercise, Landlord may lease the
ROFR Space to the third party on terms no more favorable than those presented to Tenant.
This Right of First Refusal: (a) is personal to [Tenant Name] and may not be assigned or
transferred; (b) is subordinate to the rights of any existing tenant in the ROFR Space;
(c) shall not apply to any renewal, extension, or expansion of an existing tenant's lease
for the ROFR Space; and (d) shall expire upon any default by Tenant.
```
