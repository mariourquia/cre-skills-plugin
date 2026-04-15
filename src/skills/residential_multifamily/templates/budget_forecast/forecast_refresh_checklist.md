---
template_slug: forecast_refresh_checklist
title: Forecast Refresh Checklist
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, asset_manager, reporting_finance_ops_lead]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
produced_by: workflows/reforecast
---

# Forecast Refresh Checklist

**Property.** {{property_name}} ({{property_id}})
**Refresh period.** {{refresh_period}}
**Refresh lead.** {{refresh_lead}}
**Refresh trigger.** {{refresh_trigger}}  (cadence | variance | event)

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})
- Market references as-of: {{market_references_as_of}} (status: {{market_references_status}})

## Phase 1 — Actuals true-up

- [ ] T-MTD actuals closed through: {{mtd_close_date}}
- [ ] GL reconciliation complete
- [ ] Accruals captured (utility, property tax, insurance, bonus)
- [ ] Any unusual items flagged (one-time gain/loss)

## Phase 2 — Remaining-period assumptions

- [ ] Rent roll snapshot for forward view: {{rent_roll_snapshot_date}}
- [ ] Renewal offer pipeline captured (units and assumed acceptance)
- [ ] Concession posture reaffirmed vs. overlay
- [ ] Turn pipeline timing reaffirmed (make_ready_days, vacant days)
- [ ] Market rent trajectory updated from reference (as-of: {{market_rents_as_of}})

## Phase 3 — Opex reforecast

- [ ] Payroll adjusted for open positions, bonus accrual, seasonal hires
- [ ] R&M adjusted for storm / seasonal / known projects
- [ ] Turn cost aligned with turn pipeline volume
- [ ] Utilities adjusted for seasonality and recent rate changes
- [ ] Insurance and tax adjusted for known notices
- [ ] Contract escalations captured

## Phase 4 — Capex reforecast

- [ ] Active project spend vs. plan updated
- [ ] Scope changes reflected (change orders logged)
- [ ] Deferred or accelerated projects noted

## Phase 5 — Outputs

- [ ] NOI reforecast vs. budget vs. prior forecast
- [ ] DSCR reforecast
- [ ] `budget_attainment` implied vs. band
- [ ] Variance narrative per `variance_commentary_template`
- [ ] Watchlist status review

## Phase 6 — Review and approval

- [ ] Property-level review: {{property_review_status}}
- [ ] Asset-level review: {{asset_review_status}}
- [ ] Lender / covenant impact review (if DSCR sensitive): {{lender_review_status}}
- [ ] Reforecast published: {{publish_status}}

---

*Template status: starter. Any reforecast shared externally tagged `final` requires approval per approval matrix.*
