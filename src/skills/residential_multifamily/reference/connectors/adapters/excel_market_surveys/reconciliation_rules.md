# Excel Market Surveys Reconciliation Rules

Excel adapter is the declared primary source for every benchmark-side
canonical object under `market_data` (see `_core/stack_wave4/source_of_truth_matrix.md`).
The operating systems (AppFolio, Intacct, Procore) carry the realized
transactions and observations. Reconciliation here is asymmetric: Excel
benchmarks supply the contract, operational systems supply drift signals
that either calibrate or challenge the benchmark.

Tolerance bands cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`;
no numeric thresholds are hardcoded in this document.

## Excel ↔ AppFolio

### Rent comp vs realized lease trade-out

- Excel rent_comp asking_rent / effective_rent is the benchmark signal
- AppFolio lease_event (renewal_accepted, move_in) plus Charge (base_rent_monthly_cents)
  yields actual trade-out by comp submarket + unit_type
- Drift: abs(excel.effective_rent - appfolio.trade_out_weighted_avg) /
  excel.effective_rent. Band defined in reconciliation_tolerance_band.yaml
  for rent_trade_out_drift. Outside band lowers confidence to medium;
  large drift routes to research_analyst for reclassification.

### Concession benchmark vs concession_rate metric drift

- Excel concession_benchmark.concession_months_offered is the benchmark
- AppFolio-derived concession_rate metric (from Charge rows classified as
  concession or credit against base_rent_monthly_cents) yields realized
  concession exposure by submarket
- Drift: percent points divergence. Band per reconciliation_tolerance_band.yaml
  concession_benchmark_drift. Drift > band triggers a market commentary
  refresh and a routed investigation to leasing_director.

### Turn cost reference vs turn_cost actuals

- Excel turn_cost_library.value (dollars_per_unit by turn_scope) is the benchmark
- AppFolio TurnProject actual_cost (realized turn spend rolled up by scope)
  yields the actual
- Drift: abs(excel.typical - appfolio.realized_median) / excel.typical.
  Band per reconciliation_tolerance_band.yaml turn_cost_drift. Drift > band
  triggers regional_ops_director review and may trigger library mid-quarter
  refresh.

## Excel ↔ Intacct

### Capex cost reference vs posted spend

- Excel capex_cost_library.value is the benchmark
- Intacct actual_line posts to capex_project deliver realized cost per
  line_item_slug (via capex_project_crosswalk and cost_code_crosswalk)
- Drift: abs(excel.typical - intacct.actual_weighted_avg) / excel.typical
  by (csi_division, line_item_slug, market). Band per reconciliation_tolerance_band.yaml
  capex_cost_drift. Drift > band triggers development_director review and
  a scheduled library refresh.

### Vendor rate vs invoice rate

- Excel vendor_rate_card.rate_typical is the contracted rate
- Intacct invoice rows posted to vendor_id yield observed unit-rate
- Drift: abs(excel.rate_typical - intacct.invoice_unit_rate) /
  excel.rate_typical. Band per reconciliation_tolerance_band.yaml
  vendor_invoice_drift. Drift > band triggers procurement_lead review;
  systematic drift > 2 consecutive periods triggers mid-cycle
  renegotiation workflow.

## Excel ↔ Procore

### Capex cost reference calibration via commitments and actuals

- Excel capex_cost_library.value is the benchmark
- Procore commitment (awarded GC / subcontract) and actual spend yield
  project-specific realizations
- Drift: per-line-item divergence between excel.typical and procore.commitment
  at award time; band per reconciliation_tolerance_band.yaml
  capex_commitment_drift. Drift > band triggers a bid leveling review
  and flags the library entry for refresh.

### Schedule assumption vs procore baselines

- Excel schedule_assumption.baseline_duration_days is the benchmark
- Procore schedule_milestone baseline + actual yields realized duration
- Drift: abs(excel.baseline_duration_days - procore.actual_median_duration).
  Band per reconciliation_tolerance_band.yaml schedule_duration_drift.
  Drift > band triggers development_director review and a scheduled
  assumption sheet refresh.

## Excel ↔ Manual

### Analyst override workflow

- Manual analyst override rows in a rent comp or market survey workbook
  carry an override_flag column + paired rationale_note
- Override without rationale: ex_provenance_commentary_author_named or
  ex_provenance_source_populated blocks intake
- Override with rationale: row lands but confidence is reduced to medium
  and annotated in source_record_audit
- Reconciliation: monthly roll-up of overrides by analyst yields an
  override_volume metric; > reconciliation_tolerance_band.yaml
  analyst_override_volume_band triggers research_analyst calibration
  review

## Cross-cutting behavior

- Drift within band: confidence reduced to medium per
  `disagreement_threshold_band` rule in source_of_truth_matrix.md
- Drift outside band: blocks the affected downstream workflow
  (market_rent_refresh, capex_estimate_generation, budget_build,
  etc.) until reconciliation closed
- Late-arriving data from Excel supersedes earlier Excel load with
  identical (family, market, as_of); audit row preserved per
  `late_arriving_data_supersedes` rule
