---
template_slug: budget_package_outline
title: Budget Package Outline
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [reporting_finance_ops_lead, asset_manager, regional_manager]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
  - reference/normalized/labor_rates__{market}_residential.csv
  - reference/normalized/utility_benchmarks__{market}.csv
  - reference/normalized/insurance_tax_assumptions__{market}.csv
produced_by: workflows/budget_build
---

# Budget Package Outline

**Property.** {{property_name}} ({{property_id}})
**Budget year.** {{budget_year}}

## Section 1 — Executive summary

- One-page narrative: {{executive_summary_narrative}}
- Headline NOI vs. prior year and underwriting: {{noi_headline}}

## Section 2 — Assumptions

- Rent growth assumption: {{rent_growth_assumption}} (source: {{rent_growth_source}})
- Renewal vs. new-lease mix: {{renewal_new_mix}}
- Concession assumption: {{concession_assumption}} (source: {{concession_source}})
- Vacancy / loss assumption: {{vacancy_loss_assumption}}
- Labor escalator: {{labor_escalator}} (source: {{labor_source}})
- Utility escalator: {{utility_escalator}} (source: {{utility_source}})
- Insurance escalator: {{insurance_escalator}} (source: {{insurance_source}})
- Real-estate tax escalator: {{tax_escalator}} (source: {{tax_source}})
- Capex plan total: {{capex_plan_total}}

## Section 3 — Revenue build (monthly)

- Base rent by unit type (link to detail): {{base_rent_detail}}
- Loss-to-lease and vacancy (link): {{ltl_vacancy_detail}}
- Concessions (link): {{concessions_detail}}
- Other income lines (link): {{other_income_detail}}

## Section 4 — Opex build (monthly)

- Payroll: {{payroll_detail}}
- R&M: {{rm_detail}}
- Utilities (net RUBS): {{utilities_detail}}
- Contracts: {{contracts_detail}}
- Marketing: {{marketing_detail}}
- Admin and office: {{admin_detail}}
- Insurance: {{insurance_detail}}
- Real-estate tax: {{tax_detail}}

## Section 5 — Capex plan

{{capex_plan_table}}

## Section 6 — Financial statements

- Monthly P&L (link): {{monthly_pl_link}}
- Annual P&L (link): {{annual_pl_link}}
- Variance to prior year (link): {{variance_prior_year_link}}
- Variance to underwriting (link): {{variance_uw_link}}

## Section 7 — Debt schedule

- Debt service by month: {{debt_service_detail}}
- DSCR projection: {{dscr_projection}}
- Debt yield projection: {{debt_yield_projection}}
- Covenant risk narrative: {{covenant_risk_narrative}}

## Section 8 — Sensitivities

- Occupancy +/-: {{sens_occupancy}}
- Trade-out +/-: {{sens_trade_out}}
- Opex line +/-: {{sens_opex}}

## Section 9 — Reforecast governance

- Monthly reforecast cadence: {{reforecast_cadence}}
- Variance triggers: {{variance_triggers}}
- Approval path for reforecast deviations: {{reforecast_approval_path}}

## Confidence banner

- Market references as-of: {{market_references_as_of}} (status: {{market_references_status}})
- Labor reference as-of: {{labor_reference_as_of}} (status: {{labor_reference_status}})
- Utility reference as-of: {{utility_reference_as_of}} (status: {{utility_reference_status}})
- Insurance / tax reference as-of: {{insurance_tax_reference_as_of}} (status: {{insurance_tax_reference_status}})

---

*Template status: starter.*
