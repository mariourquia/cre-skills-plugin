---
template_slug: annual_budget_build_checklist
title: Annual Budget Build Checklist
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
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
  - reference/normalized/labor_rates__{market}_residential.csv
  - reference/normalized/utility_benchmarks__{market}.csv
  - reference/normalized/insurance_tax_assumptions__{market}.csv
produced_by: roles/reporting_finance_ops_lead, workflows/budget_build
---

# Annual Budget Build Checklist

**Property.** {{property_name}} ({{property_id}})
**Budget year.** {{budget_year}}
**Prep lead.** {{prep_lead}}
**Budget package due.** {{budget_package_due_date}}

## Phase 1 — Inputs and references

- [ ] Pull rent roll snapshot for budget anchor date: {{rent_roll_anchor_date}}
- [ ] Pull T-12 operating data through: {{t12_through_date}}
- [ ] Pull market rents reference (as-of verified): {{market_rents_as_of}}
- [ ] Pull concession benchmark reference (as-of verified): {{concession_benchmarks_as_of}}
- [ ] Pull labor-rate reference (as-of verified): {{labor_rates_as_of}}
- [ ] Pull utility benchmark reference (as-of verified): {{utility_benchmarks_as_of}}
- [ ] Pull insurance / tax assumption reference (as-of verified): {{insurance_tax_as_of}}
- [ ] Confirm org overlay escalator assumptions (wages, utility, R&M, insurance, tax): {{org_escalator_source}}
- [ ] Confirm loan covenants and debt service schedule: {{loan_covenants_source}}

## Phase 2 — Revenue build

- [ ] Market rent by unit type entered and reconciled to reference
- [ ] Rollover schedule built (lease by lease) and reconciled to rent roll
- [ ] Renewal vs. new-lease assumptions set inside overlay bands
- [ ] Concessions modeled (where applicable) inside concession policy
- [ ] Vacancy / loss assumption set with trigger for re-review
- [ ] Other income (RUBS, pet, parking, late, admin) built from T-12 with adjustments

## Phase 3 — Operating expense build

- [ ] Payroll built from staffing plan + labor rate reference
- [ ] R&M built by category with seasonality
- [ ] Turn budget aligned with make-ready days target band and turn cost library
- [ ] Utilities built net of RUBS, reconciled to benchmark
- [ ] Insurance / tax updated from latest notices or assumptions reference
- [ ] Contracts (landscaping, pest, trash, elevator, life-safety, etc.) confirmed
- [ ] Marketing budget aligned with funnel plan
- [ ] Administrative / office / bank fees reconciled

## Phase 4 — Capex / below-NOI

- [ ] Capex plan linked to capex intake memos and approved projects
- [ ] Replacement reserve contribution set
- [ ] Deferred maintenance surface added to capex plan
- [ ] Life-safety capex not deferred without explicit approval

## Phase 5 — Validation

- [ ] NOI vs. underwriting reconciliation completed
- [ ] DSCR and debt yield projected for each quarter
- [ ] `budget_attainment` expectation stated; sensitivity on key drivers
- [ ] Variance tripwires set for monthly review (per `variance_commentary_template`)
- [ ] Confidence banner (staleness of each reference) completed

## Phase 6 — Review and approval

- [ ] Property-level review (PM, regional)
- [ ] Asset-level review (AM)
- [ ] Reforecast governance attachment (frequency, triggers)
- [ ] Owner review package assembled
- [ ] Lender review package assembled (if covenant-sensitive)
- [ ] Final approval path: {{approval_path}}

## Phase 7 — Publication

- [ ] Final budget loaded into system of record
- [ ] Reference versions locked; change log entry recorded
- [ ] Monthly reforecast cadence scheduled

---

*Template status: starter. No line-item figures live here; every numeric assumption resolves to the reference layer.*
