# Survivorship Rules

Field-level rules for which source wins on which field when sources disagree. Rules are deterministic: the same inputs always produce the same output. A losing source's value is recorded for lineage but is not surfaced to downstream skills as the effective value.

Every crosswalk row names one `survivorship_rule` by slug. The rules below are the slugs referenced in the starter crosswalks. Additional rules may be added without schema changes; the rule name on a crosswalk row is free-form.

## Global principles

1. **Field-level, not record-level.** A property's `property_name` may survive from one source while its `legal_entity_id` survives from another.
2. **Deterministic ordering.** Each rule declares an explicit ranking of sources per field. The first source in the ranking that carries a non-null value wins.
3. **Null is not a valid survival.** A source that provides a null value is skipped; the next source in the ranking is consulted.
4. **Manual override outranks automated survivorship.** If an active entry in `manual_overrides.yaml` applies, the override value wins regardless of the rule. When an override expires, the default ranking applies again.
5. **Protected-class guardrail.** No survivorship rule may reference a protected-class attribute in any way, not as a selector, not as a tiebreaker, not as a conditional.

## property_default

Applies to records in `property_master_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `property_name` | pms (primary), gl (fallback), manual_upload (last resort) |
| `legal_entity_id` | gl (primary), manual override, pms (fallback only if gl lacks the record) |
| `market` | pms (primary), manual_upload |
| `submarket` | pms (primary), market_data, manual_upload |
| `year_built` | pms (primary), construction (fallback for in-development assets) |
| `year_renovated` | construction (primary for major renovations), pms (fallback) |
| `unit_count_total` | pms (primary), gl (fallback), manual_upload |
| `unit_count_rentable` | pms (primary); no fallback (if pms does not supply, record is held) |
| `nrsf_total` | pms (primary), construction (fallback for in-development) |
| `parcel_acres` | manual_upload (primary; rarely in PMS or GL) |
| `class` | pms (primary), manual_upload |
| `acquired_date` | gl (primary; derived from closing entries), pms (fallback) |

## unit_default

Applies to records in `unit_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `unit_type_id` | pms (primary), construction (fallback during value-add reconfiguration) |
| `nrsf` | pms (primary), construction (fallback for reconfigured units) |
| `bedrooms` | pms (primary), construction (fallback) |
| `bathrooms` | pms (primary), construction (fallback) |
| `status` | pms (primary); status is operational (no other source wins) |
| `classification` | pms (primary), construction (when renovation records lag the PMS update) |
| `has_washer_dryer`, `has_patio_balcony`, `view_premium_eligible` | pms (primary), manual_upload |

## lease_default

Applies to records in `lease_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `lease_id` aliases | pms (primary); other sources reference pms lease id |
| `start_date`, `end_date`, `term_months` | pms (primary); no fallback |
| `base_rent_monthly` | pms (primary); ap cross-checks but does not win |
| `concessions_total` | pms (primary); ap used for reconciliation |
| `fees_monthly` | pms (primary); ap (fallback for residual postings) |
| `is_renewal`, `prior_lease_id` | pms (primary); manual override permitted when pms lacks the linkage |
| `status` | pms (primary); no other source wins |

## resident_account_default

Applies to records in `resident_account_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `primary_resident_name` | pms (primary); crm fallback for lead-stage records before lease |
| `email`, `phone` | pms (primary); crm (fallback when pms lacks) |
| `ledger_balance` | pms (primary); no other source wins |
| `risk_flags` | pms (primary); crm restricted to non-protected-class observations only |

**Guardrail.** None of the fields above may be survived based on a protected-class attribute. If two candidate identities tie on composite match and none of the allowed tiebreakers can be applied, the row is routed to the unresolved queue; it is not resolved silently.

## vendor_master_default

Applies to records in `vendor_master_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `vendor_name` (legal) | ap (primary); construction (fallback); coi (cross-check) |
| `tax_id_last_four` | ap (primary) |
| `services` | construction (primary for trade classification); ap (fallback) |
| `markets_served` | construction (primary); ap (fallback) |
| `w9_on_file`, `insurance_expiry_date` | coi (primary); ap (fallback) |
| `license_numbers` | coi (primary); ap (fallback) |
| `rate_card_ref` | construction (primary); ap (fallback) |
| `performance_score` | construction (primary); ap (fallback) |
| `preferred_flag` | ap (primary); construction (fallback) |

## account_default

Applies to records in `account_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| canonical account slug mapping | manual (primary); no automated source wins |
| account description | gl (primary) |

Chart of accounts mapping is operator-curated. Automated suggestion is permitted but never wins without reviewer sign-off.

## capex_project_default

Applies to records in `capex_project_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `project_name` | construction (primary); gl (fallback only if construction lacks a record for the project) |
| `project_type` | construction (primary); gl account slug cross-reference (via `account_crosswalk`) |
| `scope_summary` | construction (primary) |
| `target_start`, `target_completion` | construction (primary) |
| `total_budget` | construction (primary); gl (cross-check; does not win) |
| `contingency_pct` | construction (primary) |
| `funding_source` | gl (primary); construction (fallback for operator-notes level detail) |
| `status` | construction (primary); gl (marks closed / cancelled via posting behavior) |

## change_order_default

Applies to records in `change_order_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `co_number` | construction (primary) |
| `scope_delta`, `cost_delta`, `time_delta_days` | construction (primary); gl (cross-check for posted cost_delta) |
| `justification`, `category` | construction (primary) |
| `status` | construction (primary); gl (marks posted status only) |
| `approver`, `approved_date` | construction (primary); approval workflow may override via manual override |

## draw_request_default

Applies to records in `draw_request_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `period`, `amount_requested` | construction (primary) |
| `cost_to_date`, `cost_to_complete_estimate` | construction (primary) |
| `percent_complete_physical`, `percent_complete_cost` | construction (primary) |
| `supporting_docs` | construction (primary) |
| `funded_date` | gl (primary); construction (not authoritative for funding timestamp) |
| `approval_status` | construction (primary); gl (marks final funded or declined) |

## employee_default

Applies to records in `employee_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `employment_id` | hr_payroll (primary) |
| `name_last`, `name_first` | hr_payroll (primary) |
| `work_email` | hr_payroll (primary); construction (fallback for tracker-only users) |
| `employment_type` (employee vs contractor) | hr_payroll (primary); manual override permitted when comingled |
| property assignment | carried on `staffing_plan` normalized record; not survived from sources directly |

**Guardrail.** No field on an employee record is survived based on a protected-class attribute.

## dev_project_default

Applies to records in `dev_project_crosswalk.yaml`.

| Field | Ranked sources |
|---|---|
| `project_name`, `scope_summary`, `baseline_schedule` | construction (primary) |
| `baseline_cost_plan`, `current_cost_plan` | construction (primary); gl (cross-check via posted actuals) |
| `entitlements_status`, `permits_status` | manual_upload (primary); construction (fallback) |
| `land_basis` | gl (primary) |
| `total_budget` | construction (primary); gl (cross-check) |

## Review cadence

- `property_default`, `unit_default`, `lease_default`, `resident_account_default`: annual review minimum; plus any review triggered by reconciliation failure or a change in the source registry.
- `vendor_master_default`: annual review.
- `account_default`: reviewed whenever the chart of accounts is modified.
- `capex_project_default`, `change_order_default`, `draw_request_default`, `dev_project_default`: reviewed per-project at project kickoff and at project close.
- `employee_default`: reviewed quarterly; interim reviews triggered by any PII classification change.
