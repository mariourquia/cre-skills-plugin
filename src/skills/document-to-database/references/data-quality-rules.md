# Data-Quality Rules

The validation and grading layer. Validation rules live in `src/calculators/validate_payload.py`; the grade is computed in `src/calculators/grade_ingestion.py` over the rubric mirror in `src/calculators/ingest/rubric.py`; tolerances live in `src/calculators/ingest/tolerances.py`. The grader is the executable realization of `src/skills/rent-roll-analyzer/references/data-quality-rubric.yaml` — it shares the rubric's dimensions, weights, and weakest-link semantics, and parity is enforced by `tests/test_ingestion_canonical_sources.py`. It is not a parallel grader.

## Impossible vs implausible — the central distinction

The validator separates two kinds of bad data and treats them differently, so a genuinely high trophy-asset rent is never rejected:

- **Impossible data** violates an identity or a hard range. It is a critical failure and fails closed: negative rentable SF, occupancy outside `[0, 100]`, a lease expiry before its start, a T-12 period count above twelve, an occupied unit with no positive base rent, or an NOI that includes below-the-line items.
- **Implausible data** is a statistical outlier that could still be real. It is a warning that lowers confidence but never a hard rejection: a base-rent PSF outside `[0, 500]` on a commercial lease is flagged for review, not failed.

## Cross-field reconciliation rules

- **Rent arithmetic.** `annual == monthly*12` within **$1** for flat, full-period leases. It is SKIPPED-with-note for any lease carrying free rent / abatement or an in-period step, because the point-in-time identity legitimately does not hold mid-abatement. A real contradiction (not a step/abatement) is `rent_arithmetic_contradiction` — critical.
- **Base rent on occupied units.** An occupied unit must carry positive base rent; otherwise `negative_or_zero_rent_occupied` — critical.
- **PSF reconciliation branches on property type.** Commercial (office / retail / industrial / mixed-use) checks base-rent PSF against `[0, 500]` and warns on an outlier; multifamily PSF is skipped because the basis is per-unit, not per-SF.
- **Occupancy range.** Physical occupancy must be in `[0, 100]`; outside is `occupancy_out_of_range` — critical.
- **Non-negative SF.** Any unit with negative rentable SF is `negative_sf` — critical.
- **T-12 period integrity.** Exactly twelve monthly periods passes; fewer is a partial-year / lease-up warning (annualization is carried as a gap, never synthesized); more than twelve is `t12_period_count_invalid` — critical (it usually means an aggregate "Total"/"YTD" column was not excluded).
- **NOI classification.** Reported NOI must equal revenue minus operating expense with below-the-line items excluded; otherwise `noi_includes_below_the_line` — critical.
- **Account mapping coverage.** Lines mapped to the `unmapped` bucket are flagged and routed to review, not rejected.

## The grade: weakest-link letter, primary; 0-100 score, secondary

The grade mirrors the rubric exactly. Each dimension is graded A / B / C. The overall letter is the **weakest link** — the lowest grade across all scored dimensions — so a single C caps the grade and cannot be averaged away. A secondary 0-100 score is the weighted readout (A=3 / B=2 / C=1, weighted by each dimension's weight and normalized), re-weighted to only the dimensions actually graded so an N/A dimension is excluded rather than scored zero.

Dimension blocks by document type:

- **Rent roll**: field completeness, date consistency, square-footage reconciliation, rent arithmetic, escalation documentation, vacancy identification, lease-type clarity, tenant credit information, lease-option documentation, historical consistency.
- **Operating statement** (same weakest-link contract): period integrity, account-mapping coverage, sign-convention consistency, NOI-classification consistency, duplicate/subtotal detection, provenance coverage.
- **Reconciliation** (folds in when a tie-out is present): base-rent tie-out, recoveries tie-out, other-income tie-out, occupancy tie-out, EGI/NOI-revenue bridge, residual unexplained.

## The gates

| Gate | Requires |
|---|---|
| **Merge** | score >= **85** AND no C grade AND no critical failure |
| **Production** | score >= **92** AND all-A AND no critical failure |

A PII-redaction breach is a **critical, non-overridable** block at any score — it cannot be waived even as a documented fixture limitation. Every other critical can, in principle, be documented as a fixture limitation by a reviewer, but a PII breach cannot. See `self-iteration-loop.md` and `security-governance.md`.

## The enumerated critical failures

Any of these forces a hard block regardless of the numeric score:

- `pii_redaction_breach` — **non-overridable**
- `rent_arithmetic_contradiction`
- `negative_or_zero_rent_occupied`
- `t12_period_count_invalid`
- `vacant_unit_active_lease`
- `lease_expiry_before_start`
- `forced_tie_out`
- `confidence_below_floor`
- `noi_includes_below_the_line`

## Tolerances (accepted ranges)

Tolerances are data, so a caller may override a reconciliation dimension via the input payload.

- Rent arithmetic: within **$1** (the rubric's `4_rent_arithmetic` rule).
- Commercial base-rent PSF plausibility window: `[0, 500]`.
- Occupancy: `[0, 100]`.
- Reconciliation, by dimension (fraction of the larger side): base rent **1%** (contractual vs gross-potential ties tight), recoveries **15%** (CAM is billed as a monthly estimate and trued-up annually, so it legitimately floats), other income **10%**, occupancy **1%** (count basis), EGI bridge **3%**.
- Confidence floor: a `low`-confidence record routes to human review; `medium` and `high` pass the floor (a `low` mapping is `confidence_below_floor` when it gates a decision).

The reconciliation tolerances are intentionally not a single global number: holding recoveries to the same tightness as base rent would flag every normal CAM true-up as an error. See `field-dictionary.md` for the per-field ranges and `human-review-workflow.md` for what a flagged check does next.
