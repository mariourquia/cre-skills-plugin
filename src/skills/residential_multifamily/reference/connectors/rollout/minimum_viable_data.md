# Minimum Viable Data

status_tag: reference

For each canonical workflow, the minimum viable data package required to activate it meaningfully. Also note what each workflow can run on in manual-files-only mode.

All 27 canonical workflow slugs come from `../../workflows/`. Audiences from `tailoring/AUDIENCE_MAP.md`.

## Legend

- **Required**: the workflow cannot produce a useful output without this input.
- **Helpful**: the workflow produces a meaningful output with or without this input; richer with it.
- **Fallback**: an alternative source when the ideal input is unavailable.
- **Manual-only mode**: the workflow can run using manual_uploads alone; confidence is downgraded.

## Workflow table

### bid_leveling_procurement_review

- Required: construction `bid_package`, construction `estimate_line_item`, ap `vendor`, ap `vendor_agreement`.
- Helpful: market_data vendor rate benchmarks.
- Fallback: manual_uploads with bid response template if construction source is not yet active.
- Manual-only mode: possible with a bid-response template in manual_uploads plus an external vendor list; low confidence.

### budget_build

- Required: gl `actual` (trailing), pms `unit`, pms `lease`, pms `charge`.
- Helpful: market_data rent and concession benchmarks, payroll benchmarks, utility benchmarks.
- Fallback: manual_uploads budget_shared_drive_dropbox source if gl is not yet active.
- Manual-only mode: possible for a single-property seed using a manual trailing P&L plus a rent roll snapshot.

### capex_estimate_generation

- Required: construction `capex_project`, construction `estimate_line_item`.
- Helpful: market_data materials, labor, vendor rate benchmarks; schedule duration benchmarks.
- Fallback: manual_uploads capex template.
- Manual-only mode: possible with a manually entered capex project and a reference benchmark set.

### capital_project_intake_and_prioritization

- Required: construction `capex_project`, gl `capex_actual`, pms `unit`.
- Helpful: market_data capex cost library, schedule duration benchmarks.
- Fallback: manual_uploads capital_project_intake template if construction is not yet active.
- Manual-only mode: possible; confidence downgraded.

### change_order_review

- Required: construction `change_order`, construction `capex_project`, construction `bid_package` or estimate baseline.
- Helpful: market_data cost benchmarks.
- Fallback: manual_uploads change_order template.
- Manual-only mode: possible with a manual CO packet; low confidence.

### construction_meeting_prep_and_action_tracking

- Required: construction `capex_project`, construction `schedule_milestone`, construction `change_order`.
- Helpful: construction `draw_request` status, ap commitments.
- Manual-only mode: possible with a meeting-notes template in manual_uploads plus status from the project owner.

### cost_to_complete_review

- Required: construction `capex_project`, construction `estimate_line_item`, construction `change_order`, construction `draw_request`.
- Helpful: ap commitments, gl capex actuals, market_data cost benchmarks.
- Manual-only mode: possible with a manual cost-to-complete worksheet; low confidence.

### delinquency_collections

- Required: pms `lease`, pms `charge`, pms `payment`, pms `delinquency_case`.
- Helpful: pms `work_order` for related issues, ap for payment plan agreements.
- Fallback: none, if pms charges and payments are not current, this workflow cannot run without compromising fair-housing controls.
- Manual-only mode: not recommended; risk of fair-housing sensitivity.

### draw_package_review

- Required: construction `draw_request`, construction `capex_project`, construction `change_order`, construction `estimate_line_item`, ap `vendor_agreement` including lien-waiver attestation.
- Helpful: gl `capex_actual`, construction `schedule_milestone`.
- Fallback: manual_uploads draw packet if construction source is not yet active; lien-waiver attestations still required.
- Manual-only mode: possible for a small project; approval gate still enforced (matrix row 12).

### executive_operating_summary_generation

- Required: pms `property`, pms `unit`, pms `lease`, pms `charge`, pms `payment`, gl `actual`, gl `budget`.
- Helpful: market_data benchmarks, construction capex status, crm lead funnel.
- Fallback: manual_uploads rolling aggregate.
- Manual-only mode: possible for a portfolio-level snapshot; many sub-metrics blanked.

### lead_to_lease_funnel_review

- Required: crm `lead`, crm `tour`, crm `application`, pms `lease`.
- Helpful: market_data rent and concession benchmarks.
- Fallback: pms lead and application if crm is not yet active (some operators run leasing directly in pms).
- Manual-only mode: partial; funnel conversion figures at low confidence.

### market_rent_refresh

- Required: market_data `market_comp`, pms `unit`, pms `unit_type`, pms `lease`.
- Helpful: crm concession observations.
- Fallback: manual_uploads market-rent template.
- Manual-only mode: possible for a one-off refresh; ongoing refresh requires a system source.

### monthly_asset_management_review

- Required: gl `actual`, gl `budget`, pms `property`, pms `unit`, pms `lease`, pms `charge`, pms `payment`.
- Helpful: construction capex status, market_data benchmarks, ap vendor status, crm lead funnel.
- Fallback: manual_uploads rolling aggregate plus a rent-roll snapshot.
- Manual-only mode: possible for a single asset; portfolio-level reviews blanked without a gl source.

### monthly_property_operating_review

- Required: gl `actual`, gl `budget`, pms `property`, pms `unit`, pms `lease`, pms `charge`, pms `payment`, pms `work_order`.
- Helpful: hr_payroll for staffing, ap for vendor spend, market_data for benchmark comparison.
- Fallback: manual_uploads property operating statement.
- Manual-only mode: possible per property; confidence downgraded.

### move_in_administration

- Required: pms `lease`, pms `application`, pms `unit`.
- Helpful: pms `charge` for security deposit, crm `lead` for attribution.
- Fallback: none, move-in requires current lease and unit state.
- Manual-only mode: not recommended; move-in is an operational process, not a reporting workflow.

### move_out_administration

- Required: pms `lease`, pms `charge`, pms `payment`, pms `work_order` for turn scope, pms `unit`.
- Helpful: ap vendor for turn work.
- Fallback: none.
- Manual-only mode: not recommended.

### owner_approval_routing

- Required: any workflow output that triggers an approval; `ApprovalRequest` infrastructure per `_core/schemas/approval_request.yaml`.
- Helpful: `_core/approval_matrix.md` and `overlays/org/<org_id>/approval_matrix.yaml`.
- Fallback: none, routing is the workflow.
- Manual-only mode: not applicable; the workflow is the gate itself.

### quarterly_portfolio_review

- Required: gl `actual`, gl `budget`, pms across all in-scope properties, construction capex status.
- Helpful: market_data benchmarks, ap vendor status, hr_payroll.
- Fallback: manual_uploads portfolio aggregate.
- Manual-only mode: possible but slow; confidence downgraded.

### reforecast

- Required: gl `actual` (trailing), gl `budget`, pms `unit`, pms `lease`, pms `charge`, pms `payment`.
- Helpful: market_data rent and concession benchmarks.
- Fallback: manual_uploads reforecast template.
- Manual-only mode: possible for a single property; confidence downgraded.

### renewal_retention

- Required: pms `lease`, pms `renewal_offer`, pms `charge`, pms `payment`.
- Helpful: market_data rent benchmarks.
- Fallback: manual_uploads renewal template.
- Manual-only mode: partial; rolled up portfolio view blanked.

### rent_comp_intake

- Required: market_data `market_comp`.
- Helpful: crm notes on observed concessions; pms `lease` signed rents.
- Fallback: manual_uploads rent_comp template.
- Manual-only mode: possible for ad hoc intake; scheduled refresh requires system source.

### schedule_risk_review

- Required: construction `schedule_milestone`, construction `capex_project`.
- Helpful: construction `change_order` status, weather feeds (out of scope here).
- Fallback: manual_uploads schedule template.
- Manual-only mode: possible for a single project; portfolio-level rollup blanked.

### third_party_manager_scorecard_review

- Required: manual_uploads operator_owner_portal_sftp (or equivalent) and hr_payroll staffing data; gl `actual` and pms `lease`, `charge`, `payment` at the managed properties.
- Helpful: market_data benchmarks.
- Fallback: manual_uploads property operating statement plus a vendor performance list.
- Manual-only mode: possible; the workflow is explicitly designed to tolerate manual-mode intake from TPMs.

### unit_turn_make_ready

- Required: pms `unit`, pms `lease` (move-out), pms `work_order`.
- Helpful: ap vendor for turn work, market_data labor and materials benchmarks.
- Fallback: manual_uploads turn-status template.
- Manual-only mode: partial.

### vendor_dispatch_sla_review

- Required: pms `work_order`, ap `vendor`, ap `vendor_agreement`.
- Helpful: insurance_coi_intake for COI validation.
- Fallback: manual_uploads vendor-dispatch log.
- Manual-only mode: possible; dispatch-SLA math requires work-order timestamps.

### work_order_triage

- Required: pms `work_order`, pms `unit`, pms `lease`.
- Helpful: pms `resident` preferences, prior work-order history.
- Fallback: manual_uploads work-order intake.
- Manual-only mode: possible for small volume; scale requires pms source.

## Manual-only mode policy

A workflow in manual-only mode must:

- Tag outputs with `confidence_band: low`.
- Include a visible freshness advisory in any output consumed downstream.
- Avoid crossing any approval gate without the full required evidence (manual-only does not bypass `_core/approval_matrix.md`).
- Track time-in-manual-mode; a workflow that has stayed in manual-only mode beyond an overlay-defined window triggers `../runbooks/cutover_manual_to_system.md` candidacy review.

## Cross-wave coverage

| Workflow | Wave activated (typical) |
|---|---|
| `budget_build`, `reforecast`, `monthly_property_operating_review`, `executive_operating_summary_generation`, `monthly_asset_management_review`, `quarterly_portfolio_review`, `market_rent_refresh`, `rent_comp_intake` | Wave 1 |
| `lead_to_lease_funnel_review`, `bid_leveling_procurement_review`, `vendor_dispatch_sla_review`, `third_party_manager_scorecard_review` (partial) | Wave 2 |
| `capex_estimate_generation`, `capital_project_intake_and_prioritization`, `change_order_review`, `draw_package_review`, `construction_meeting_prep_and_action_tracking`, `cost_to_complete_review`, `schedule_risk_review`, `third_party_manager_scorecard_review` (full) | Wave 3 |
| `move_in_administration`, `move_out_administration`, `renewal_retention`, `delinquency_collections`, `unit_turn_make_ready`, `work_order_triage`, `owner_approval_routing` (as ready per wave) | Wave 1 through Wave 4 as pms coverage deepens |
