# Excel Market Surveys Edge Cases

Enumerated edge cases the Excel adapter must handle. Each entry declares
the trigger, the detector, the routed action, and the downstream impact.
Thresholds reference `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
rather than being hardcoded here.

---

## 1. as_of date in future

- Trigger: workbook row lands with as_of > now (analyst mis-typed 2027 when
  they meant 2026, or ran a forward projection into a benchmark sheet)
- Detector: dq rule ex_freshness_future_as_of
- Action: blocker; route to runbooks/excel_common_issues.md::future_as_of;
  analyst resubmits with corrected as_of
- Downstream impact: intake rejects the drop entirely; previous version
  remains canonical

## 2. as_of past staleness threshold

- Trigger: file family staleness_threshold_days exceeded (e.g.,
  rent_comp_weekly with as_of 12 days old vs 10-day threshold)
- Detector: dq rule ex_freshness_per_family citing intake_manifest.yaml
- Action: blocker; route to runbooks/excel_common_issues.md::stale_export;
  analyst must either refresh the data or formally extend the window with
  a change request
- Downstream impact: consuming workflows (market_rent_refresh,
  capex_estimate_generation, budget_build) refuse the stale source and
  either run with prior version confidence-reduced or halt

## 3. Header drift across quarters

- Trigger: quarterly refresh changes column names (scope_template becomes
  scope_tier, as_of becomes effective_date, market becomes msa) even
  though payload structure is unchanged
- Detector: dq rule ex_conformance_column_headers_match_schema
- Action: blocker; route to runbooks/excel_common_issues.md::header_drift;
  propose header alias rows in template_schemas or restore prior headers
- Downstream impact: every row rejected until headers match template
  schema; sample_invalid/header_drift.csv illustrates

## 4. Vendor name fuzzy-match across files

- Trigger: vendor_rate_card in 2025-Q4 lists "Vista Mechanical Services
  Inc" while the 2026-Q1 drop lists "Vista Mechanical LLC" but both
  reference the same vendor_id
- Detector: dq rule ex_reference_vendor_in_crosswalk combined with
  vendor_master_crosswalk surfaced alias matching
- Action: resolves if vendor_id column matches crosswalk; if vendor_id
  absent or mismatched, route to runbooks/excel_common_issues.md::vendor_name_typo
- Downstream impact: vendor rate not applied to the wrong entity; vendor
  spend reconciliation against Intacct invoices remains correct

## 5. Market name not in market_crosswalk

- Trigger: workbook introduces a new market (e.g., "Greenville-Spartanburg")
  that has no crosswalk row
- Detector: dq rule ex_reference_market_in_crosswalk
- Action: blocker; crosswalk_additions.yaml::market_crosswalk must grow
  to cover the new market; master_data/unresolved_exceptions_queue.md
  receives the exception
- Downstream impact: every row referencing the unmapped market blocks
  intake until crosswalk extended

## 6. Mid-quarter refresh overwriting prior

- Trigger: capex_cost_library_q1_2026.xlsx is dropped again two weeks
  later with revised numbers triggered by a lumber supply shock
- Detector: dq rule ex_consistency_mid_quarter_refresh
- Action: warning if change_log row references delta; blocker if not
- Downstream impact: on confirmed refresh, prior version retained as
  audit, new version supersedes per late_arriving_data_supersedes; if
  without change_log, intake blocked until analyst provides the delta
  rationale

## 7. Manual override without rationale

- Trigger: analyst hand-edits a benchmark row (e.g., bumps asking_rent
  by +$50) but leaves source column blank or marks "override" without a
  paired rationale note
- Detector: dq rule ex_provenance_source_populated combined with
  override_flag detection
- Action: blocker; runbooks/excel_common_issues.md::override_vs_correction_handling
- Downstream impact: row rejected; analyst must resubmit with paired
  note that cites either a direct observation or an override rationale

## 8. Conflicting refs across rate cards

- Trigger: Vista Mechanical quotes hvac_pm_biannual at $95 in one rate
  card tab and $125 in another tab of the same workbook, or across two
  rate cards dropped the same week
- Detector: dq rule ex_uniqueness_vendor_rate_key on
  (vendor_id, service, market, as_of); duplicate key with differing
  rate_typical
- Action: blocker; route to procurement_lead; both rows retained in
  audit; canonical rate is the later-as-of-date row after resolution
- Downstream impact: vendor budget build pauses for the affected vendor
  until resolved

## 9. Capex line item duplicated across CSI divisions

- Trigger: roof_replace_shingle appears under both CSI 07 31 13 (Asphalt
  Shingles) and CSI 02 71 19 (which is wrong; that's parking)
- Detector: dq rule ex_uniqueness_capex_key combined with
  cost_code_crosswalk validation
- Action: blocker; the misclassified row rejected; analyst must
  reclassify or tag the correct csi_division
- Downstream impact: capex_estimate_generation would otherwise
  double-count the line item

## 10. Currency / unit basis ambiguity

- Trigger: vendor_rate_card row with unit_basis dollars_per_unit but the
  numeric cell shows a figure that is clearly dollars_per_hour (e.g.,
  $35 for an HVAC service call)
- Detector: dq rule ex_consistency_outlier_check citing tolerance band
  per service_category
- Action: warning; flagged for analyst review; does not block if the
  analyst confirms with a source note, blocks if unresolved past
  ingestion window
- Downstream impact: budget build confidence drops for the affected
  vendor until resolved

## 11. Escalation applied vs not

- Trigger: capex_cost_library.typical appears to already include the
  escalation_assumption baked into the number (e.g., analyst applied
  the 3.5% escalator to typical before submission), leading to double
  escalation downstream
- Detector: recon check ex_recon_capex_cost_library_vs_intacct_posted
  detects systematic overstatement vs realized spend
- Action: warning first period, blocker after two periods outside
  tolerance_band.yaml::capex_cost_drift
- Downstream impact: downstream estimators must know whether escalation
  is pre-applied; escalation_base_date on cover_metadata clarifies

## 12. Rate band collapsed (low = typical = high)

- Trigger: vendor_rate_card row where rate_low = rate_typical = rate_high
  (analyst had a single quote and defaulted all three to the same number)
- Detector: dq rule ex_consistency_band_not_collapsed
- Action: warning; requires paired source_note or confidence = low
- Downstream impact: downstream sensitivity analysis cannot vary within
  band; reviewer must decide if the single-quote pattern represents a
  contracted bundle or a data completeness issue

## 13. Partial submarket coverage

- Trigger: rent_comp_weekly for Charlotte covers South End and Uptown but
  not NoDa; downstream workflow needs NoDa
- Detector: coverage gap detection at workflow activation time (not a
  dq rule; a workflow-side precondition)
- Action: workflow enters partial_mode_behavior; the missing submarket
  surfaces as a prominent gap in the resulting market_rent_benchmark
  rollup and the NoDa-specific deal underwriting flags missing comp set
- Downstream impact: no silent imputation; consuming skill must either
  extend comp search or surface the gap to the reader

## 14. Unit-type label drift

- Trigger: one property carries the unit_type_label "A1" while a
  comparable property lists "1BR-1BA" for the same floor plan
- Detector: dq rule comp_unit_type_harmonized (in rent_comp_template)
  combined with unit_type_harmonization crosswalk lookup
- Action: blocker on first encounter of an unresolved label; crosswalk
  expansion resolves
- Downstream impact: rent benchmarks rolled up by unit_type would
  otherwise compare apples to oranges

## 15. Merged-cell anchor loss on extract

- Trigger: analyst used merged cells to visually group the market in
  column A for rows 2-50 (only cell A2 carries "Charlotte"); extractor
  populates market for row 2 only
- Detector: completeness rule ex_completeness_required_fields_per_schema
  catches nulls in market column for rows 3-50
- Action: blocker; upstream unmerge + forward-fill required before drop
- Downstream impact: preprocessing runbook
  runbooks/excel_common_issues.md::merged_cells

## 16. Commentary author anonymous

- Trigger: market_commentary row with author = "Research Team" or
  "Anonymous" or blank
- Detector: dq rule ex_provenance_commentary_author_named
- Action: blocker; runbooks/excel_common_issues.md::commentary_author_missing
- Downstream impact: directional_call and confidence_band cannot be
  audited without a named author; quarterly_portfolio_review and
  executive_operating_summary_generation would propagate unauditable
  claims
