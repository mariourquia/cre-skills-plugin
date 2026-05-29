# Tie-Out Methodology

How the `rent-roll-t12-tieout` skill reconciles a normalized rent roll against a normalized T-12: the stated basis, the dimension-specific tolerances, the deterministic mapping/timing/missing decision tree, the never-force contract, the handling of one-sided dimensions, and why the CAM true-up cycle is expected timing rather than an error. This is documentation that GUIDES the calculator `reconcile_rent_roll_t12.py`; every rule here is realized in that pure, stdlib-only function.

## The basis problem (and why it is stated, not hidden)

The two documents measure different things. Reconciling them without saying so produces either false ties or false alarms, so the basis is fixed up front and labeled on every reconciled row:

| Source | Basis | Meaning |
|---|---|---|
| Rent roll | annualized contractual in-place income | What the leases obligate tenants to pay, annualized from the in-place charge schedule. |
| T-12 | recognized accrual | What the operating statement recognized, annualized from the months actually present (scaled by `12 / periods_present`). |
| Collected cash | out of scope | There is no AR feed; billed-vs-collected is not reconciled. |

Comparing **contractual** to **recognized accrual** is expected to produce variances:
- **Free rent / abatement** — contractual rent is in place, but the accrual period recognized less.
- **Vacancy** — a unit contributes contractual rent in the roll only while leased; the accrual reflects the months it was actually occupied.
- **CAM true-ups** — recoveries are billed as monthly estimates and trued up to actual once a year.

These are findings, not defects. The engine classifies each one; it never relabels a legitimate basis variance as an extraction or arithmetic error.

## The five required tie-outs

The brief calls for five tie-outs. The canonical chart of accounts combines recoveries and other income in one revenue account (`revenue_other_rental`), so the engine reconciles those two **jointly** and reports the rent-roll-side breakdown — stated honestly rather than fabricating a per-account precision the chart does not carry. The five map to the engine's dimensions as:

| # | Required tie-out | Engine dimension | Notes |
|---|---|---|---|
| 1 | Base rent | `base_rent` | Two-sided; tightest tolerance. |
| 2 | Recoveries / CAM | `other_rental` (recoveries leg) | Reconciled jointly with other income; breakdown reported. |
| 3 | Other income (parking / storage / percentage rent) | `other_rental` (other-income leg) | Same joint dimension; breakdown reported. |
| 4 | Occupancy / vacancy (physical and economic) | `occupancy` | Physical occupancy is reconciled on a count basis; economic occupancy is read off the EGI bridge (see `references/noi-bridge-inputs.md`). |
| 5 | NOI-bridge revenue inputs (EGI) | `egi_bridge` | The most important; computed first; drives classification. |

## Dimension-specific tolerances

A single global tolerance is wrong. Base rent should tie tight on a contractual-vs-gross-potential basis; recoveries legitimately float because CAM is estimated monthly and trued up annually. Tolerances are expressed as a fraction of the larger side and are **data**, overridable per dimension via `tolerance_overrides` in the input dict.

| Dimension | Default tolerance | Why |
|---|---|---|
| `base_rent` | ~1% | Contractual vs gross-potential should be tight. |
| `recoveries` (drives `other_rental`) | ~15% | CAM estimate-vs-true-up float. |
| `other_income` | ~10% | Parking / storage / percentage rent move more than base rent. |
| `occupancy` | ~1% | Count basis ties tight. |
| `egi_bridge` | ~3% | The revenue-into-NOI total; modest float, but the anchor for classification. |

Rent-roll **arithmetic** validation (the `annual == monthly * 12` identity) is a separate, upstream concern owned by the rent-roll data-quality rubric (the "within $1" rule), not a reconciliation tolerance. See `../../document-to-database/references/data-quality-rules.md`.

## The mapping / timing / missing decision tree

The EGI bridge is reconciled first, because whether the **total** ties is the signal that distinguishes the three difference types. For each untied line dimension:

```
Is the dimension within its tolerance?
├─ YES → TIED (residual_unexplained = 0)
└─ NO  → does the EGI total tie?
         ├─ EGI ties
         │  ├─ base and other variances OFFSET (opposite signs, sum ≈ 0 within EGI tol)
         │  │      → MAPPING  (a charge reclassified into the wrong account; confidence medium)
         │  └─ a single category drifts (no offset)
         │         → TIMING   (estimate-vs-true-up / period attribution; confidence medium)
         └─ EGI does NOT tie
            ├─ this is the other-income/recoveries leg AND its variance is negative
            │  (T-12 recovery income exceeds the contractual run-rate)
            │      → TIMING   (CAM estimate-vs-annual-true-up; confidence medium)
            └─ otherwise
                   → MISSING  (income present in one source, absent in the other —
                              a collections / vacancy finding; confidence low)
```

Read in words:
- **MAPPING** — the money is all there (EGI ties) but landed in the wrong accounts; two categories move in opposite directions and cancel. A reclassification, not a leak.
- **TIMING** — the period attribution differs. Either the total ties and one category is early/late, or the recovery leg shows the T-12 recognizing more than the contractual run-rate, which is the signature of CAM billed-as-estimate then trued-up.
- **MISSING** — the total itself does not reconcile and the gap is not the recovery-true-up signature. Income is present in one source and absent in the other: a collections or vacancy finding that an analyst must run down.

A `MAPPING` or `TIMING` classification carries medium confidence; a `MISSING` gap carries low confidence and is the highest-priority review item.

## The never-force contract

A forced tie is impossible **by construction**, not by policy:
- `tie_status` takes only `tied` or `untied`. There is no third "reconciled-after-adjustment" state.
- No code path adjusts, plugs, or back-solves a value to make a dimension tie. The rent-roll value and the T-12 value are read as-is; the variance is whatever it is.
- `residual_unexplained` equals `|variance|` for every untied dimension and `0` only when the dimension genuinely ties. The unexplained amount is **surfaced**, never absorbed.
- Every untied dimension is appended to the human-review queue with its difference type, variance, residual, and confidence. Nothing is silently closed.

If a reconciliation appears to tie to the penny on a property with free rent or CAM estimates, that is the red flag: this engine cannot produce that result.

## One-sided dimensions

Some dimensions cannot be reconciled because one source carries no comparable value. The clearest case is occupancy: when the T-12 reports no occupancy or vacancy metric, occupancy is marked `one_sided: true`, `tie_status: untied`, with a note that it is not reconcilable here. The variance and residual are left unquantified (you cannot compute a gap against a value that does not exist) — the engine does not invent the missing side to manufacture a comparison. One-sided dimensions still route to review so the gap is visible.

## The CAM true-up cycle as expected timing

CAM and other recoveries are billed to tenants as a **monthly estimate** during the year and reconciled to **actual** operating costs once annually (the framework `cam-reconciliation-calculator` implements). On a contractual-vs-accrual comparison this guarantees a recovery variance for most of the year:
- Mid-year, the T-12 has recognized estimated recoveries that may run above or below the contractual run-rate.
- At true-up, a catch-up adjustment lands in a single period.

So when the recovery leg drifts and the T-12 recognizes **more** recovery income than the contractual run-rate, the engine classifies it as **TIMING** (CAM estimate-vs-annual-true-up), not as a missing or mapping error. This is the expected, healthy state of a recovery reconciliation between true-up cycles — it is reported, classified, and routed, but it is not an alarm.

## What this methodology does not do

- It does not normalize, extract, or grade the inputs — those are upstream (`rent-roll-to-database`, `t12-to-database`).
- It does not reconcile the OpEx → NOI leg; the tie-out proves the **revenue** inputs to NOI (see `references/noi-bridge-inputs.md`). The expense leg is owned by `t12-to-database`.
- It does not reconcile collected cash — there is no AR feed, and that basis is explicitly out of scope.
