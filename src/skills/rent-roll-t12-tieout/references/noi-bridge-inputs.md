# NOI-Bridge Revenue Inputs

How rent-roll revenue maps into T-12 revenue categories to support an NOI bridge, where the tie-out's responsibility ends, and how physical occupancy differs from economic occupancy on this bridge. This is documentation that GUIDES the `rent-roll-t12-tieout` skill and its calculator `reconcile_rent_roll_t12.py`; it does not introduce any new computation.

## What an NOI bridge needs from a tie-out

NOI is revenue minus operating expense. An IC challenge of an underwritten NOI almost always starts on the revenue side: *does the rent roll actually prove the income the operating statement recognized?* The tie-out answers exactly that question and no more. It reconciles the **revenue inputs** to NOI — base rent, recoveries, other income, and the EGI total — so the revenue line of the bridge is defensible. The **OpEx → NOI leg** (expense normalization, reclassification of capital items out of opex, the NOI line itself) is owned by `t12-to-database` / `t12-normalizer`, not by the tie-out. Keeping that boundary sharp is what lets each side be audited independently.

## The revenue mapping

The rent roll is a charge-level source: each lease decomposes into typed charge lines (base rent, CAM / tax / insurance recoveries, parking, storage, percentage rent, other recurring). The T-12 is an account-level source mapped to the canonical chart of accounts. The bridge aligns the two as follows:

| Rent-roll charge categories | Canonical T-12 account | Tie-out dimension |
|---|---|---|
| `base_rent` | `revenue_base_rent` | `base_rent` |
| `cam_recovery`, `tax_recovery`, `insurance_recovery` | `revenue_other_rental` | `other_rental` (recoveries leg) |
| `parking`, `storage`, `percentage_rent`, `other_recurring`, `one_time_amortized` | `revenue_other_rental` / `revenue_other_non_rental` | `other_rental` (other-income leg) |
| (sum of the above) | total recognized revenue | `egi_bridge` |

Two consequences follow from the canonical chart:

1. **Recoveries and other income reconcile jointly.** The chart combines recoveries and other income into the `revenue_other_rental` family, so the engine reconciles `other_rental` as one dimension and reports the rent-roll-side split (recoveries vs other income) on the row. This is stated honestly: the join key the T-12 carries does not separate the two, so the engine does not pretend to a per-account precision it cannot source. The breakdown is for the analyst's eye, not a second tie.

2. **The EGI bridge is the anchor.** EGI — the rent-roll annualized contractual gross vs the T-12 recognized total revenue — is reconciled first. Whether the total ties is what tells the engine, for every untied per-category gap, whether the difference is a reclassification (mapping), a period attribution (timing), or a genuine income gap (missing). See `references/tie-out-methodology.md` for the decision tree.

## Basis alignment on the bridge

The rent-roll side is **annualized contractual in-place** income; the T-12 side is **recognized accrual**, annualized from the months present (scaled by `12 / periods_present`). The bridge therefore expects the contractual gross to sit **above** recognized revenue by roughly the free rent plus vacancy plus any timing on recoveries — that spread is the economic story of the asset, not noise. Collected cash is out of scope (no AR feed), so the bridge never reaches down to cash receipts; it stops at recognized revenue.

## Physical vs economic occupancy

The bridge touches occupancy in two distinct ways, and conflating them is a common error:

- **Physical occupancy** is a count: occupied units (or leased SF) over rentable units (or SF), excluding non-revenue statuses (down, model, admin, employee, owner-occupied). It is reconciled directly as the `occupancy` dimension on a count basis with a tight tolerance — **when the T-12 carries an occupancy metric**. When it does not, occupancy is marked one-sided and not reconciled (the engine does not fabricate the missing side).

- **Economic occupancy** is a revenue ratio: recognized rental revenue over gross potential rent. It is not a separate reconciled dimension — it is **read off the EGI bridge**. The spread between the rent roll's contractual gross potential and the T-12's recognized revenue *is* the economic-vacancy-plus-concession story. A property can be 96% physically occupied yet show materially lower economic occupancy if free rent and concessions are heavy; the EGI bridge surfaces that gap, and the tie-out classifies it (typically timing or missing) rather than hiding it inside a single occupancy percentage.

So the five-tie-out requirement for "occupancy / vacancy (physical and economic)" is satisfied across two engine outputs: physical occupancy on the `occupancy` dimension, and economic occupancy as the revenue spread on `egi_bridge`. Both are reported; neither is forced.

## Where the tie-out hands off

| Bridge leg | Owner |
|---|---|
| Revenue inputs (base rent, recoveries, other income, EGI) | `rent-roll-t12-tieout` (this skill) |
| OpEx normalization and the OpEx → NOI leg | `t12-to-database` / `t12-normalizer` |
| Full proforma / underwritten NOI | `acquisition-underwriting-engine` |
| Orchestration + the human-review queue across all legs | `document-to-database` |

The tie-out's output — the reconciled revenue dimensions, the EGI verdict, and the residual / review queue — is the proven revenue foundation the downstream NOI build stands on. It does not compute NOI; it makes the revenue half of NOI defensible.
