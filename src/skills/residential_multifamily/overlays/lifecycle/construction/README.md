# Construction Lifecycle Overlay

Active construction posture. Applies from notice-to-proceed through substantial
completion (and typically continues through punchlist until TCO). Loads alongside
the development overlay when residual design items remain.

## What this overlay shifts

- Reporting emphasis: cost to complete, contingency status, schedule variance,
  change-order register, trade-buyout variance, draw-cycle health, RFI / submittal
  throughput, punchlist progress.
- Approval posture: construction-manager plus asset-manager as default; executive
  review escalates with dollar size.
- Staffing: construction-side (CM, project manager, superintendent, QA/QC if
  applicable). Site operating team not yet present.

<a id="weekly_review"></a>

## Weekly construction review

- Schedule review: critical path, look-ahead three weeks, delays and mitigations.
- Cost review: cost to complete, contingency, change-order log, trade-buyout
  variance to budget.
- Quality review: RFIs open, submittals in progress, non-conformance log.
- Safety review: incidents, near-misses, corrective actions.
- Owner report-out cadence: weekly summary plus monthly deep-dive with financials.

<a id="draw_discipline"></a>

## Draw-cycle discipline

- Submission-to-funding target in
  `reference/derived/role_kpi_targets.csv#row_lifecycle_construction_draw_cycle_time`.
- Lender conditions checked before submission (lien waivers, sworn statements,
  inspector sign-off, insurance current).
- Contractor pay application reconciles to schedule of values; variance over
  threshold triggers asset-management review before submission.
- Any draw submission marked `final` to lender is a gated action per approval
  matrix row 12.

## Transition to lease-up

At substantial completion and TCO, the lease-up lifecycle overlay loads. The
construction overlay remains active for punchlist and closeout until formal
project closeout. The two overlays co-exist during this window.
