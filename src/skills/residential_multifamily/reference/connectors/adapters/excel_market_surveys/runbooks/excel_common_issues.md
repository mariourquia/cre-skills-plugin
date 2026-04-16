# Runbook: Excel Market Surveys Common Issues

Cross-reference for `dq_rules.yaml` and `edge_cases.md`. Every issue
below maps to a dq rule or an edge case and declares a routing and
resolution path.

---

## header_drift

- Trigger rule: `ex_conformance_column_headers_match_schema`
- Observed symptom: one or more columns renamed across quarters (e.g.,
  `as_of` became `effective_date`, `market` became `msa`)
- Resolution:
  1. Identify the offending drop via the dq log
  2. Compare observed headers to `template_schemas/<family>.yaml` column
     names
  3. If the rename is intentional (a template revision), record the
     change in the `template_release_registry` and extend the dual-run
     window accordingly
  4. If the rename is accidental (analyst edited the sheet), restore the
     canonical header and re-drop
- Escalation: data_platform_team + the family's required_reviewer
- Illustrative sample: `sample_invalid/header_drift.csv`

## vendor_name_typo

- Trigger rule: `ex_reference_vendor_in_crosswalk`
- Observed symptom: `vendor_id` absent or `vendor_name` drifts
  ("Vista Mechanical LLC" vs "Vista Mechanical Services Inc")
- Resolution:
  1. Confirm the vendor identity via the vendor master
  2. If a legitimate alias, extend `vendor_master_crosswalk` via
     `crosswalk_additions.yaml::vendor_master_crosswalk`
  3. If a typo, return the workbook to the analyst
  4. Re-drop after correction
- Escalation: procurement_lead
- Edge case: see `edge_cases.md` item 4

## market_naming_conventions

- Trigger rule: `ex_reference_market_in_crosswalk`
- Observed symptom: market label does not resolve (e.g., "Charlotte MSA"
  vs "Charlotte"; "ATL Metro" vs "Atlanta"; new market "Greenville-Spartanburg")
- Resolution:
  1. If alias, add to `crosswalk_additions.yaml::market_crosswalk` with
     `excel_label` and `canonical_market_id`
  2. If new market, create canonical `MKT_<slug>` and extend crosswalk
  3. Escalate via `master_data/unresolved_exceptions_queue.md` if
     ownership is ambiguous (two regions claim the market)
- Escalation: research_analyst + asset_mgmt_director

## partial_submarket_coverage

- Trigger: edge case 13 (not a dq rule; a workflow precondition)
- Observed symptom: rent_comp_weekly covers some submarkets but not
  others within a market
- Resolution:
  1. Workflow enters `partial_mode_behavior` per
     `workflow_activation_additions.yaml`
  2. Downstream consumer receives the gap with a surfaced message
  3. Analyst extends comp set in the next weekly drop
  4. No silent imputation, no fill-in from peer submarket
- Escalation: research_analyst

## rate_band_collapsed

- Trigger rule: `ex_consistency_band_not_collapsed`
- Observed symptom: rate_low = rate_typical = rate_high (single-quote
  case) or low = typical = high on turn_cost or capex line
- Resolution:
  1. Analyst attaches a source_note explaining the single-quote
     basis (e.g., "sole-source vendor, contracted bundle")
  2. Row lands but confidence is set to low
  3. If the single-quote pattern persists across multiple files,
     escalate to procurement_lead for sourcing diversification
- Escalation: procurement_lead (for vendor_rate_card); capital_projects_team
  (for turn_cost_library and capex_cost_library)

## escalation_reapplication

- Trigger: edge case 11 (recon check
  `ex_recon_capex_cost_library_vs_intacct_posted` drifts outside band)
- Observed symptom: capex_cost_library.typical systematically overstates
  realized spend because analyst pre-applied the escalator
- Resolution:
  1. Confirm `escalation_base_date` on cover_metadata
  2. If pre-applied, downstream estimator must treat the value as already
     escalated; set `typical_is_escalated = true` in intake metadata
  3. If not pre-applied, escalator is applied downstream; consistent with
     the canonical convention
  4. Document the convention in the template_release_registry; every
     family must follow the same convention
- Escalation: development_director + data_platform_team

## missing_as_of

- Trigger rule: `ex_completeness_as_of_present`
- Observed symptom: `as_of` column blank on rows (common in sample_invalid
  `missing_as_of.csv`)
- Resolution:
  1. Inspect the filename for an implicit date and compare to rows
  2. If the workbook filename declares `2026-01-15` but rows lack the
     value, fill from filename via the intake pre-processor
  3. If no date in filename either, block and return to analyst
- Escalation: data_platform_team
- Illustrative sample: `sample_invalid/missing_as_of.csv`

## future_as_of

- Trigger rule: `ex_freshness_future_as_of`
- Observed symptom: as_of date > today (analyst typo; forward projection
  misfiled as benchmark)
- Resolution:
  1. Block; return to analyst
  2. If the drop is a forward projection, it belongs in the forecast
     workbook family, not the benchmark family; route to forecast
     intake instead
- Escalation: research_analyst

## stale_export

- Trigger rule: `ex_freshness_per_family`
- Observed symptom: as_of older than `staleness_threshold_days` per
  family (sample_invalid `stale_export_q3_2024.csv` illustrates)
- Resolution:
  1. Block; require analyst to drop a fresh file
  2. If the workflow is mid-cycle and needs the benchmark, run with
     prior version confidence-reduced and annotate in the output
  3. If the analyst is intentionally back-loading historical data,
     route to the historical archive (not the live intake)
- Escalation: research_analyst + asset_mgmt_director
- Illustrative sample: `sample_invalid/stale_export_q3_2024.csv`

## duplicate_rows

- Trigger rules: `ex_uniqueness_vendor_rate_key`,
  `ex_uniqueness_capex_key`, `ex_uniqueness_rent_comp_key`
- Observed symptom: duplicate key within a single drop; common when
  analyst pastes an analyst-observed row alongside a provider row
- Resolution:
  1. Block
  2. Analyst decides which row is canonical; the other lands in an
     audit sheet with a paired note
  3. Re-drop
- Escalation: research_analyst (for rent_comp); procurement_lead (for
  vendor_rate); capital_projects_team (for capex)

## rate_band_inversion

- Trigger rule: `ex_consistency_band_monotonic`
- Observed symptom: low > typical or typical > high
- Resolution:
  1. Block; typically a typo
  2. Analyst corrects and re-drops
- Escalation: none (fixed inline)

## reviewer_signoff_missing

- Trigger rule: `ex_completeness_reviewer_for_highimpact`
- Observed symptom: capex_cost_library, labor_rate_quarterly,
  turn_cost_library, vendor_rate_card, analyst_benchmark_pack, or
  market_survey_workbook dropped without reviewer or signed_off_date
- Resolution:
  1. Block
  2. Required reviewer must sign off
  3. Re-drop
- Escalation: the file family's required_reviewer; escalate to
  asset_mgmt_director if review is systemically delayed

## commentary_author_missing

- Trigger rule: `ex_provenance_commentary_author_named`
- Observed symptom: market_commentary row with author = "Research Team"
  or empty
- Resolution:
  1. Block
  2. Analyst names the author and re-drops
- Escalation: investments_director

## segment_contamination

- Trigger rule: `ex_consistency_segment_sheet_declaration`
- Observed symptom: luxury comp appears in a middle_market sheet (or
  affordable in middle_market)
- Resolution:
  1. Block
  2. Move the row to the correct segment sheet
  3. If the row belongs in the sheet but is a legitimate outlier (e.g.,
     a premium finish building classified as middle_market), document
     in a paired source note; confidence is reduced
- Escalation: research_analyst

## override_vs_correction_handling

- Trigger: edge case 7; detected via rule `ex_provenance_source_populated`
  combined with override_flag detection
- Observed symptom: analyst hand-edit without paired rationale
- Resolution:
  1. If the edit is a correction (row was wrong; analyst fixed it),
     the paired source note must cite the correct source
  2. If the edit is an override (analyst disagrees with the source),
     the paired rationale_note must explain; confidence drops to
     medium; the row lands in the override_audit
  3. Without paired note, block
- Escalation: research_analyst; systematic override volume per analyst
  per family is reviewed monthly per
  `ex_recon_analyst_override_volume`

## merged_cells

- Trigger rule: `ex_completeness_required_fields_per_schema` catches
  nulls on rows where a merged anchor was not propagated
- Observed symptom: market column populated only on first row of a
  visually-grouped block; subsequent rows null
- Resolution:
  1. Block
  2. Analyst unmerges cells and forward-fills the anchor value
  3. Re-drop
- Escalation: data_platform_team (pre-processing guidance in the
  onboarding runbook)

## midquarter_refresh_no_changelog

- Trigger rule: `ex_consistency_mid_quarter_refresh`
- Observed symptom: capex_cost_library or analyst_benchmark_pack dropped
  again mid-quarter without a change_log row
- Resolution:
  1. Warning; acceptable with analyst commentary
  2. If no commentary, block
  3. Analyst adds change_log entry and re-drops
- Escalation: the file family's required_reviewer

## currency_unit_drift

- Trigger rule: `ex_consistency_outlier_check`
- Observed symptom: unit_basis declared dollars_per_unit but numeric
  value is plausible only as dollars_per_hour
- Resolution:
  1. Warning on first drop; flagged for analyst review
  2. If unresolved, block second drop
  3. Analyst either corrects unit_basis or confirms unusual value with
     a paired source note
- Escalation: procurement_lead + capital_projects_team
