# Agency Multifamily Quote Methodology (Freddie Mac Optigo / Fannie Mae DUS)

Reference for the `agency-loan-quote-analyzer` skill. This file documents how
to read, normalize, and reconcile agency multifamily quotes. It describes
mechanics and industry conventions in general terms. **Every numeric threshold,
spread, fee, and reserve figure below is illustrative** -- a representative
mid-cycle value used to make the methodology concrete. Real constraints are set
by the lender's actual quote, the agency's then-current guide, the property
type, and the rate environment. Always size and reconcile against the figures
on the borrower's specific term sheet, not these placeholders.

---

## 1. The two agencies and their programs

Freddie Mac (branded **Optigo**) and Fannie Mae (branded **DUS**, Delegated
Underwriting and Servicing) are the two GSE multifamily executions. Both lend
through approved seller/servicers (lenders), are non-recourse with standard
bad-boy carve-outs at stabilization, and size against simultaneous DSCR / LTV /
debt-yield constraints. The practical differences a quote analyzer must hold:

| Dimension | Freddie (Optigo) | Fannie (DUS) |
|---|---|---|
| Underwriting model | Lender quotes, agency re-underwrites (prior approval on many deals) | Delegated: lender underwrites and shares loss risk, faster cert |
| Rate-lock style | Index lock and early rate lock available on many programs | Early rate lock (ERL) and standard delivery |
| Lease-up program | Lease-Up / Value-Add / Near-Stabilization loans | Near-Stabilization / Forward executions |
| Small balance | Small Balance Loan (SBL) program | Fannie Small Loans |
| Green | Green Up / Green Advantage | Green Rewards / Green Financing |

The analyzer should never assert a program rule from memory. It should read the
program named on the quote and reconcile the stated constraints.

---

## 2. Sizing: the binding-constraint method

Agency proceeds are the **minimum** of several simultaneous tests. Size each,
identify the binder, and reconcile to the lender's quoted number.

```
NCF              = NOI - replacement_reserve            (size off NCF, never NOI)

Max_DSCR_amort   = NCF / (min_DSCR_amort * debt_constant_amort)
Max_DSCR_IO      = NCF / (min_DSCR_IO    * debt_constant_IO)     (if IO offered)
Max_LTV          = value_basis * max_LTV
Max_LTPP         = purchase_price * max_LTPP                     (acquisitions)
Max_DebtYield    = NCF / min_debt_yield                          (if stated)

Max_Proceeds     = min(applicable tests above)
Binding          = argmin(applicable tests above)
```

Where the debt constant is the annualized constant for the amortization (or the
interest-only constant for the IO test):

```
debt_constant_amort = (annual P&I payment per $1 of loan at the coupon/amort)
debt_constant_IO    = coupon                                     (IO: DS = rate * balance)
```

**Illustrative constraint defaults (representative, conventional stabilized):**

| Constraint | Illustrative threshold | Notes |
|---|---|---|
| Min DSCR (amortizing) | 1.25x | Tighter (1.30x+) for weaker markets/older vintage |
| Min DSCR (IO test) | 1.05x - 1.10x | Applied to the IO debt service |
| Max LTV | 75-80% (conventional), 75% (cash-out) | On as-stabilized or as-is value |
| Max LTPP (acquisition) | 80% of purchase price | Often the binding constraint on a purchase |
| Min debt yield | ~7.0-8.0% | Not always stated; when stated can bind in low-cap markets |

**Reconciliation rule.** If the lender's `quoted_proceeds` exceeds
`Max_Proceeds` computed off the borrower's underwritten NCF by more than ~3%,
the lender is using a higher NCF, a higher value, or an unstated assumption.
The analyzer reports the dollar gap and the most likely driver. The gap usually
narrows or vanishes at rate lock once the appraisal and agency re-underwrite
land.

**LTPP vs LTV.** On an acquisition, max-LTPP (loan-to-purchase-price) frequently
binds tighter than max-LTV because the appraised value can exceed the contract
price. Always check both denominators.

---

## 3. Lease-up and forward structures: initial funding + earnout

Lease-up / near-stabilization / forward quotes fund in two conceptual pieces:

1. **Initial funding** -- sized off *in-place* (current) NCF at today's
   occupancy. This is the committed money at close.
2. **Holdback / earnout** -- the difference up to the full quoted amount, sized
   off *stabilized* NCF, released only when the property hits the gate metrics
   by the deadline. This is **conditional**, not committed.

The analyzer must size the constraint twice (in-place for initial, stabilized
for the full amount) and present the holdback as contingent.

**Illustrative earnout-gate structure (representative, lease-up):**

```
Initial funding:     ~ sized to in-place NCF, e.g. 1.05x-1.10x DSCR floor at close
Earnout release gate:
  Achieved DSCR    >= 1.25x   (trailing-3-month annualized NCF)
  Physical occ.    >= 90%
  Economic occ.    >= 88%
  Sustained for    >= 3 consecutive months
  Achieved by      <= 12-24 months from close (the achievement deadline)
Miss the deadline -> holdback forfeited / re-margin / springing recourse (read the quote)
Conversion        -> may step the rate down and re-underwrite to permanent
```

The achievement deadline and the consequence of missing it are the single most
important caveats on a lease-up quote. A forfeitable earnout with a tight
deadline and a springing-recourse penalty is a fundamentally different risk than
a generous deadline with partial release.

---

## 4. Optional features and how to price them

### Rate buy-down
The borrower pays additional points upfront to lower the coupon. Recommend only
if the breakeven hold is comfortably inside the plan:

```
annual_DS_savings  = (rate_high - rate_low) * loan_balance        (approx, IO)
breakeven_years    = upfront_points_cost / annual_DS_savings
Recommend buy-down only if breakeven_years << planned_hold_years
```

### IO vs amortization
IO raises cash-on-cash and current DSCR headroom but leaves more principal at
maturity (bigger balloon, less equity build). Report the maturity-balance delta:

```
balloon_IO    = original_balance                                  (full-term IO)
balloon_amort = original_balance - principal_amortized_over_term
maturity_delta = balloon_IO - balloon_amort                       (extra refi/sale risk)
```

### Index lock / early rate lock (ERL)
On forward/lease-up, the borrower can lock the index early to remove rate risk
during construction/lease-up, at a good-faith deposit and potential breakage
cost. Lay out the cost of locking vs the exposure of staying open through the
lock window. Note the lock fee and window (illustrative: good-faith deposit
~1-2% of loan, refundable at delivery; lock windows commonly 30-180+ days,
longer on forwards).

### Rate cap (floating only)
Floating agency loans typically require a purchased interest-rate cap. Model the
capped worst-case:

```
capped_DS    = cap_strike * loan_balance                          (worst-case, at/above strike)
capped_DSCR  = NCF / capped_DS
```
Never recommend a floater without modeling cap cost and the capped DSCR.

---

## 5. Reserves, escrows, and net proceeds

Gross quoted proceeds are not cash-at-close. Net them down:

```
net_proceeds = gross_proceeds
             - upfront_repair_completion_holdback
             - upfront_tax_insurance_escrow_funding
             - origination_fee
             - (third-party report + legal costs, if netted)
```

**Illustrative reserve/escrow conventions (representative):**

| Item | Illustrative figure | Treatment |
|---|---|---|
| Replacement reserve | $250-$300 / unit / yr | Deducted to NCF (drives sizing) |
| Tax & insurance escrow | Monthly impound + upfront | Ongoing, non-refundable |
| Immediate-repair / completion holdback | PCA-driven, e.g. 100-125% of est. cost | Upfront, refundable on completion |
| Deferred-maintenance reserve | PCA-driven | Reconcile to `pca-reserve-analyzer` output |
| Origination fee | ~0.5-1.0% of loan | At close |

The replacement reserve is the line that converts NOI to NCF. If a quote sized
DSCR off NOI, restate to NCF; the real DSCR is lower than quoted.

---

## 6. Recourse, net worth, and liquidity tests

Agency loans are non-recourse with standard bad-boy carve-outs **at
stabilization**. Lease-up/forward quotes commonly carry a completion/payment
guaranty or springing recourse that burns off only when the stabilization gate
is met. The sponsor must also clear financial-strength tests.

**Illustrative sponsor tests (representative):**

```
Required net worth        >= loan amount                          (common agency convention)
Required post-close liquidity >= 9-12 months of debt service
Guaranty                  : bad-boy carve-outs (always) + completion/recourse (lease-up, springing)
```

Flag a net-worth or liquidity shortfall: it can require an additional guarantor
or kill the quote. Treat springing full recourse on a missed stabilization gate
as a Deal-Breaker-severity caveat unless the sponsor can carry it.

---

## 7. Prepayment structures and hold-plan alignment

Score each quote's prepay against the borrower's planned exit:

| Structure | Behavior | Best fit |
|---|---|---|
| Yield maintenance (YM) | Make lender whole on lost interest; very costly to break early when rates fall | Long, certain hold |
| Defeasance | Substitute Treasury/agency securities; cost driven by rate environment | Long hold, securitized pool |
| Declining penalty / step-down (e.g. 5-4-3-2-1) | Fixed % of balance, declining by year | Shorter or uncertain hold |
| Open window | Prepayable without penalty after open date | Exit near/after open date |

If the planned exit falls inside a heavy YM or defeasance window, flag the
misalignment. Directional prepay-cost figures are **illustrative only** unless an
actual rate environment and remaining term are supplied; do not assert a dollar
prepay cost without the inputs to compute it.

---

## 8. Master caveat: indicative until lock

A quote's rate and proceeds are **indicative** until rate/index lock and are
subject to the appraisal, PCA, Phase I environmental, and (where applicable)
seismic/zoning reports, plus the agency re-underwrite. The analyzer must never
present quoted proceeds as committed money before lock. Every output ends with a
caveat list, and "index not locked / proceeds subject to third-party reports" is
always on it.
