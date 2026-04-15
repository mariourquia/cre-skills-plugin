# Ontology

Canonical object definitions. Every role pack, workflow pack, overlay, and reference file references these objects. Adding or mutating a canonical object is a core change; it must be logged and reviewed.

Each object below declares: description, keys, key fields, parents, time basis, grain, typical sources, validation, null handling, and an example record. Fields marked `required` must be present in every instance. Fields marked `optional` may be null; null handling is specified.

---

## Property

**Description.** An owned residential multifamily asset at a single operating site, distinct from the legal entity that owns it.

**Keys.** `property_id` (string, owner-scoped; globally unique within an org overlay).

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `property_id` | string | required | canonical ID. |
| `property_name` | string | required | operating name. |
| `legal_entity_id` | string | required | pointer to the owning entity; resolved outside this subsystem. |
| `segment` | enum | required | see taxonomy Axis 2. |
| `form_factor` | enum | required | see taxonomy Axis 3. |
| `lifecycle_stage` | enum | required | see taxonomy Axis 4. |
| `management_mode` | enum | required | see taxonomy Axis 5. |
| `market` | string | required | foreign key to `reference/normalized/markets/`. |
| `submarket` | string | optional | null = market only; used for rent comp scoping. |
| `year_built` | int | optional | null allowed for pre-delivery assets. |
| `year_renovated` | int | optional | |
| `unit_count_total` | int | required | |
| `unit_count_rentable` | int | required | excludes employee / model / down. |
| `nrsf_total` | int | required | net rentable sf. |
| `parcel_acres` | float | optional | |
| `class` | enum | optional | `a, b, c, d` — present for scoping, not required. |
| `acquired_date` | date | optional | null for ground-up pre-delivery. |
| `cost_basis_date` | date | optional | used in lifecycle `recap_support`. |

**Parents.** None. A Property is a root object.

**Children.** `Building[]`, `StaffingPlan`, `BudgetLine[]`, `CapexProject[]`, overlays.

**Time basis.** As-of record. Attribute changes (segment, lifecycle, management mode) are logged via change log.

**Grain.** One row per property.

**Typical sources.** Owner-maintained asset register, PMA for third-party managed assets, T-12 / rent roll for operating state.

**Validation.** `unit_count_rentable <= unit_count_total`. `nrsf_total > 0`. `lifecycle_stage` + `acquired_date` consistency (if stage is `lease_up` or later, `acquired_date` must be set).

**Null handling.** `year_built` may be null during development; skills that need it must surface the missing reference, not guess.

**Example.**

```yaml
property_id: PROP_001
property_name: Ashford Park
legal_entity_id: ENT_ASH_PARK_LLC
segment: middle_market
form_factor: garden
lifecycle_stage: stabilized
management_mode: third_party_managed
market: Charlotte
submarket: South End
year_built: 2002
year_renovated: 2019
unit_count_total: 248
unit_count_rentable: 244
nrsf_total: 218560
class: B
acquired_date: 2021-06-15
```

---

## Building

**Description.** A physical structure within a Property. Garden properties often have many; mid-rise properties often have one.

**Keys.** `(property_id, building_id)`.

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `building_id` | string | required | property-scoped. |
| `building_label` | string | required | often a letter or number. |
| `stories` | int | required | |
| `has_elevator` | bool | required | |
| `has_structured_parking` | bool | required | |
| `unit_count` | int | required | |
| `nrsf` | int | required | |
| `year_built` | int | optional | |
| `address_line` | string | optional | |

**Parents.** `Property`. **Children.** `Unit[]`.

**Typical sources.** Owner asset register, PMA, as-built drawings.

**Example.**

```yaml
building_id: BLD_A
property_id: PROP_001
building_label: "A"
stories: 3
has_elevator: false
has_structured_parking: false
unit_count: 48
nrsf: 41280
```

---

## Unit

**Description.** A single rentable residential unit.

**Keys.** `(property_id, unit_id)`.

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `unit_id` | string | required | property-scoped, usually unit number. |
| `building_id` | string | required | FK to Building. |
| `unit_type_id` | string | required | FK to UnitType. |
| `floor` | int | optional | |
| `nrsf` | int | required | square feet. |
| `bedrooms` | int | required | 0 for studio. |
| `bathrooms` | float | required | half-baths = 0.5. |
| `status` | enum | required | `occupied, vacant_rented, vacant_unrented, notice_occupied, notice_unrented, model, employee, down, admin`. |
| `classification` | enum | optional | `classic, renovated, fully_renovated` — for renovation programs. |
| `has_washer_dryer` | bool | optional | |
| `has_patio_balcony` | bool | optional | |
| `view_premium_eligible` | bool | optional | |

**Parents.** `Building`, `Property`. **Children.** `Lease[]`, `WorkOrder[]`, `TurnProject[]`.

**Time basis.** Attributes are as-of record; status is event-sourced through `LeaseEvent` and `MoveInEvent` / `MoveOutEvent`.

**Grain.** One row per unit per property.

**Validation.** `nrsf > 0`, `bedrooms >= 0`, `bathrooms >= 0.5`, status must be one of enum.

**Null handling.** `classification` null = classic unrenovated default for rollups.

**Example.**

```yaml
unit_id: "101"
property_id: PROP_001
building_id: BLD_A
unit_type_id: UT_B1
floor: 1
nrsf: 910
bedrooms: 1
bathrooms: 1.0
status: occupied
classification: renovated
has_washer_dryer: true
has_patio_balcony: true
view_premium_eligible: false
```

---

## UnitType

**Description.** A floor plan / unit configuration class.

**Keys.** `(property_id, unit_type_id)`.

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `unit_type_id` | string | required | |
| `label` | string | required | e.g., `A1`, `B2`, `C1`. |
| `bedrooms` | int | required | |
| `bathrooms` | float | required | |
| `nrsf_typical` | int | required | representative NRSF. |
| `unit_count` | int | required | count of units of this type. |
| `floor_plan_name` | string | optional | marketing name. |

**Parents.** `Property`. **Children.** `Unit[]`.

**Example.**

```yaml
unit_type_id: UT_B1
property_id: PROP_001
label: "B1"
bedrooms: 1
bathrooms: 1.0
nrsf_typical: 910
unit_count: 96
floor_plan_name: "The Park"
```

---

## FloorPlan

**Description.** Alias for `UnitType` when presented for marketing. Not a separate canonical object; kept in alias registry. Skills should use `UnitType` canonically.

---

## Lease

**Description.** An executed rental agreement between the owner (or property manager) and one or more residents for a specific unit over a specified term.

**Keys.** `lease_id` (org-scoped).

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `lease_id` | string | required | |
| `property_id` | string | required | |
| `unit_id` | string | required | |
| `resident_account_id` | string | required | primary resident / household. |
| `status` | enum | required | `draft, approved, executed, in_effect, renewing, expired, terminated, broken`. |
| `start_date` | date | required | |
| `end_date` | date | required | |
| `term_months` | int | required | |
| `base_rent_monthly` | decimal | required | |
| `concessions_total` | decimal | required | see ConcessionRecord. |
| `fees_monthly` | decimal | optional | pet, trash, tech package, garage, storage. |
| `rent_schedule` | list | optional | for step-up leases. |
| `is_renewal` | bool | required | |
| `prior_lease_id` | string | optional | if renewal. |
| `is_corporate` | bool | optional | |

**Parents.** `Unit`, `Property`. **Children.** `LeaseEvent[]`, `Charge[]`, `Payment[]`, `ConcessionRecord[]`, `DelinquencyCase?`.

**Validation.** `end_date > start_date`, `term_months` consistent with dates, `is_renewal => prior_lease_id is not null`.

---

## LeaseEvent

**Description.** An event in a lease's lifecycle: signed, moved in, renewed, renewal offered, notice to vacate given, skip, legal notice served, eviction filed, moved out, terminated.

**Keys.** `lease_event_id`.

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `lease_event_id` | string | required | |
| `lease_id` | string | required | |
| `event_type` | enum | required | `lease_signed, move_in, renewal_offered, renewal_accepted, renewal_declined, notice_to_vacate, late_payment, legal_notice_served, eviction_filed, eviction_judgment, move_out, lease_broken, lease_terminated, skip`. |
| `event_date` | date | required | |
| `event_data` | object | optional | event-specific payload (e.g., renewal offer rent, notice reason). |

---

## ResidentAccount

**Description.** The household (one or more legal residents) party to leases on this property. A resident account persists across leases (e.g., transfer or renewal).

**Keys.** `resident_account_id`.

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `resident_account_id` | string | required | |
| `primary_resident_name` | string | required | |
| `additional_residents` | list | optional | |
| `email` | string | optional | |
| `phone` | string | optional | |
| `ledger_balance` | decimal | required | current balance across all charges and payments. |
| `risk_flags` | list | optional | e.g., `repeat_late`, `skip_risk`. Never includes protected-class attributes. |

**Guardrail.** `risk_flags` must not contain any protected-class attribute (race, color, religion, national origin, sex, familial status, disability, or any state/local protected class). Tests enforce.

---

## Charge / Payment

**Description.** A ledger entry. `Charge` = amount owed; `Payment` = amount received. Together they resolve to a resident ledger balance.

**Keys.** `(charge_id | payment_id)`.

**Key fields (Charge).** `charge_id, lease_id, resident_account_id, charge_type (rent, base_rent, pet_fee, concession_reversal, late_fee, nsf_fee, damage, utility, other), charge_date, amount, posted_by, notes`.

**Key fields (Payment).** `payment_id, resident_account_id, payment_date, amount, tender_type (ach, card, cash, money_order, check, portal), applied_to_charge_ids, posted_by`.

---

## DelinquencyCase

**Description.** A tracked instance of outstanding balance beyond a configured aging bucket.

**Keys.** `case_id`.

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `case_id` | string | required | |
| `lease_id` | string | required | |
| `stage` | enum | required | `current, 1_7, 8_30, 31_60, 61_90, 91_plus, legal_notice, eviction_filed, judgment, write_off`. |
| `current_balance` | decimal | required | |
| `stage_entered_date` | date | required | |
| `last_contact_date` | date | optional | |
| `last_contact_channel` | enum | optional | `email, phone, portal_msg, door_hang, certified_mail`. |
| `payment_plan_id` | string | optional | |
| `legal_flag` | bool | required | true = legal exposure; forces approval gate. |

---

## Lead / Tour / Application / ApprovalOutcome

### Lead

**Keys.** `lead_id`. **Parents.** `Property`.

**Fields.** `lead_id, property_id, source_channel, inquiry_date, prospect_name, contact_email, contact_phone, preferences (bedrooms, move_date, budget, pets), pipeline_stage (inquiry, contacted, tour_scheduled, toured, applied, approved, leased, lost), assigned_to, notes`.

**Guardrail.** `preferences` and `notes` must not capture protected-class attributes. Tests enforce by pattern.

### Tour

**Keys.** `tour_id`. **Parents.** `Lead`.

**Fields.** `tour_id, lead_id, scheduled_date, conducted_date?, tour_type (in_person, self_guided, virtual), conducted_by, units_shown, outcome (applied, follow_up, lost, no_show), notes`.

### Application

**Keys.** `application_id`.

**Fields.** `application_id, lead_id, applied_date, unit_id_preferred?, household_composition (count only), income_basis, employment_basis, rental_history_basis, background_screen_status, approval_status`.

**Guardrail.** Screening criteria must reference a documented screening policy overlay. No ad-hoc criteria.

### ApprovalOutcome

**Keys.** `approval_outcome_id`.

**Fields.** `approval_outcome_id, application_id, outcome (approved, approved_with_conditions, declined), conditions (e.g., higher deposit, guarantor required), decided_date, decided_by, policy_ref (pointer to screening policy)`.

**Guardrail.** `outcome` must cite `policy_ref`. No discretionary denials without policy reference. Tests enforce.

---

## MoveInEvent / MoveOutEvent / NoticeEvent

Specialized `LeaseEvent` types, but frequently reasoned about as first-class. Fields inherit `LeaseEvent` fields plus:

- `MoveInEvent`: `move_in_inspection_id, keys_issued_count, welcome_package_delivered`.
- `MoveOutEvent`: `move_out_inspection_id, forwarding_address, deposit_disposition_status, security_deposit_returned_amount`.
- `NoticeEvent`: `notice_type (ntv, non_renewal_owner, non_renewal_resident, lease_break), notice_date, vacate_date, reason_code?`.

---

## WorkOrder

**Keys.** `work_order_id`. **Parents.** `Unit` (usually) or `Property` (common area).

**Fields.** `work_order_id, property_id, unit_id?, reported_date, reported_by (resident | staff | pm_tool), priority (p1_safety, p2_habitability, p3_standard, p4_cosmetic), category (plumbing, hvac, electrical, appliance, doors_locks, pest, general, other), status (open, assigned, in_progress, awaiting_parts, awaiting_vendor, scheduled, completed, closed, deferred), assigned_to, completed_date?, resolution_notes, parts_cost, labor_hours, vendor_id?, cost_total?`.

**Validation.** `priority = p1_safety => acknowledgment SLA in approval_matrix`.

---

## PreventiveMaintenanceTask

**Keys.** `pm_task_id`.

**Fields.** `pm_task_id, property_id, building_id?, unit_id?, system (hvac_filter, fire_panel, boiler, pool, elevator, pest_treatment, gutter_clean, landscape_seasonal, etc.), cadence (monthly, quarterly, annual, custom), last_completed_date, next_due_date, vendor_id?, cost_estimate, cost_actual_ytd`.

---

## TurnProject

**Description.** The make-ready project for a specific unit between residents.

**Keys.** `turn_id`.

**Fields.** `turn_id, property_id, unit_id, move_out_date, classic_to_renovated?, scope_template_ref, scope_line_items[], vendor_assignments[], start_date, target_ready_date, actual_ready_date?, budget_total, actual_total?, status (planned, in_progress, awaiting_parts, punchlist, ready, leased), pre_lease_holds?`.

**Metrics derived:** `make_ready_days`, `turn_cost`, `turn_variance_vs_budget`.

---

## Vendor / VendorAgreement

### Vendor

**Fields.** `vendor_id, vendor_name, services[], markets_served[], w9_on_file, insurance_expiry_date, license_numbers[], rate_card_ref?, performance_score?, preferred_flag`.

### VendorAgreement

**Fields.** `agreement_id, vendor_id, property_id?, scope, term_start, term_end, pricing_model (time_materials, unit_rate, lump_sum, retainer), rate_card_ref, insurance_requirements_ref, termination_clause_summary, approval_thresholds`.

**Guardrail.** A vendor may not be dispatched to safety-critical work if `insurance_expiry_date < today`. Tests enforce.

---

## StaffingPlan

**Description.** The approved site staffing structure for a property.

**Fields.** `staffing_plan_id, property_id, effective_start, effective_end?, roles (list of {role_slug, fte_count, salary_band_ref}), reports_to (org_chart_ref), notes`.

Reference pointer: `reference/normalized/staffing_ratios.csv` plus `reference/normalized/payroll_assumptions.csv`.

---

## BudgetLine / ForecastLine / VarianceExplanation

### BudgetLine

**Fields.** `budget_line_id, property_id, period (fiscal year or month), chart_of_account (chart_ref), line_label, amount, scenario (budget), build_notes, build_basis (unit_count_ratio, psf, fixed, percent_of_revenue, per_occupied_unit_per_month, etc.), assumption_refs[]`.

### ForecastLine

**Same shape plus** `scenario: forecast, as_of_date, prior_forecast_ref?, variance_from_prior`.

### VarianceExplanation

**Fields.** `variance_explanation_id, budget_line_id, period, actual_amount, variance_amount, variance_percent, driver_category (volume, rate, timing, one_time, mix, other), narrative, proposed_corrective_action?, author, reviewed_by?`.

**Guardrail.** Variance explanations marked `approved_for_owner_report` require approval per approval matrix.

---

## CapexProject / EstimateLineItem / BidPackage / BidComparison / ChangeOrder / DrawRequest / ScheduleMilestone

### CapexProject

**Fields.** `capex_project_id, property_id, project_name, project_type (component_replacement, value_add, amenity_upgrade, deferred_mx, life_safety, compliance, other), scope_summary, target_start, target_completion, total_budget, contingency_pct, funding_source (reserves, owner_capital_call, loan_draw, insurance_proceeds), approvals[], status (proposed, approved, in_progress, complete, cancelled, deferred)`.

### EstimateLineItem

**Fields.** `line_item_id, project_id, csi_division?, line_label, unit (ea, sf, lf, cy, ton, hr, lot), quantity, unit_cost_ref (pointer to reference/normalized/material_labor_rates.csv row + as_of_date), extended_cost, contingency_applied, escalation_applied, source_basis (historical, bid, reference_library, rom)`.

### BidPackage

**Fields.** `bid_package_id, project_id, scope_description, bidders_invited[], bid_due_date, qualification_requirements, received_bids[]`.

### BidComparison

**Fields.** `bid_comparison_id, bid_package_id, leveled_line_items[], normalization_notes, recommended_award, recommendation_rationale, approvals_required`.

### ChangeOrder

**Fields.** `change_order_id, project_id, co_number, scope_delta, cost_delta, time_delta_days, justification, category (owner_directed, design_error, site_condition, scope_clarification, unforeseen), status (proposed, approved, rejected, pending_approval), approver, approved_date?`.

### DrawRequest

**Fields.** `draw_request_id, project_id, period, amount_requested, cost_to_date, cost_to_complete_estimate, percent_complete_physical, percent_complete_cost, supporting_docs[], reviewer, reviewer_findings, approval_status`.

### ScheduleMilestone

**Fields.** `milestone_id, project_id, milestone_name, baseline_date, current_forecast_date, actual_date?, critical_path_flag, predecessors[], status`.

---

## Commitment / PurchaseCommitment

**Description.** A buy-side contractual obligation from owner (or owner's GC) to a vendor or subcontractor for defined scope at defined price. The first-class object that change orders, draw requests, and posted invoices reconcile against. Distinct from `VendorAgreement`: a VendorAgreement is the umbrella relationship; a Commitment is a specific contracted dollar obligation within or alongside it.

**Keys.** `commitment_id` (org-scoped).

**Key fields.**

| Field | Type | Req | Notes |
|---|---|---|---|
| `commitment_id` | string | required | canonical ID. |
| `project_id` | string | required | FK to `CapexProject`, `ConstructionProject`, or `DevelopmentProject`. |
| `vendor_id` | string | required | FK to `Vendor`. |
| `vendor_agreement_id` | string | optional | FK when commitment is a release against a master agreement. |
| `commitment_type` | enum | required | `subcontract, purchase_order, services_agreement, change_order_release, allowance, contingency_release, retainage_release`. |
| `title` | string | required | short label. |
| `scope_summary` | string | required | one-paragraph scope. |
| `csi_division` | string | optional | when applicable. |
| `cost_code_id` | string | optional | FK to project cost code. |
| `executed_date` | date | optional | null until executed. |
| `effective_start` | date | required | when scope/payment may begin. |
| `effective_end` | date | optional | substantial completion target. |
| `original_amount` | decimal | required | initial committed dollars. |
| `approved_change_orders_amount` | decimal | required | net of approved COs (default 0). |
| `revised_amount` | decimal | required | original + approved COs. |
| `paid_to_date` | decimal | required | sum of approved draw applications. |
| `retainage_held` | decimal | required | dollars held back per contract. |
| `balance_to_complete` | decimal | required | revised - paid - retainage held. |
| `status` | enum | required | `draft, out_for_signature, executed, in_progress, complete, terminated, cancelled`. |
| `funding_source` | enum | optional | `reserves, owner_capital_call, loan_draw, insurance_proceeds, mixed`. |
| `bonded` | bool | optional | performance/payment bond required. |
| `insurance_certificate_ref` | string | optional | pointer to COI. |
| `payment_terms` | string | optional | e.g., net 30, monthly progress, milestone-based. |
| `lien_waiver_required` | bool | required | true if jurisdiction or owner policy requires. |

**Parents.** `Vendor`, `CapexProject` (or `ConstructionProject` / `DevelopmentProject`). **Children.** `ChangeOrder[]`, `DrawRequest[]` (via project), invoice postings (via Intacct). 

**Time basis.** Event-sourced. Status transitions logged via change log; financial state (paid_to_date, retainage_held, balance_to_complete) is derivable from `DrawRequest` + posted invoices but cached on the commitment for fast reporting.

**Grain.** One row per executed (or in-flight) commitment per project per vendor.

**Typical sources.** Procore (primary, scope and approval state), Sage Intacct (posted spend reconciliation), manual contracts (legacy or non-Procore projects).

**Validation.** `revised_amount = original_amount + approved_change_orders_amount`. `paid_to_date <= revised_amount`. `balance_to_complete = revised_amount - paid_to_date - retainage_held`. `status = complete IMPLIES balance_to_complete = 0 AND retainage_held = 0`.

**Null handling.** `executed_date` null permitted while `status in {draft, out_for_signature}`. `vendor_agreement_id` null permitted when commitment is a one-off PO without a master agreement.

**Guardrail.** A commitment cannot transition to `executed` without a vendor with non-expired insurance (per `Vendor.insurance_expiry_date`) and, where required, a current bond. Tests enforce.

**Example.**

```yaml
commitment_id: COMMIT_12450
project_id: PROJ_ASHFORD_RENOV_2026
vendor_id: VEN_VISTA_MECH
commitment_type: subcontract
title: HVAC Rooftop Replacement
scope_summary: Replace 4 RTUs on Building A; includes crane, controls integration, 1-year service warranty.
csi_division: "23"
executed_date: 2026-03-12
effective_start: 2026-04-01
effective_end: 2026-06-30
original_amount: 412000.00
approved_change_orders_amount: 18500.00
revised_amount: 430500.00
paid_to_date: 215250.00
retainage_held: 21525.00
balance_to_complete: 193725.00
status: in_progress
funding_source: reserves
bonded: true
lien_waiver_required: true
```

---

## DevelopmentProject / ConstructionProject

Extensions of `CapexProject` for ground-up or major renovation. Add:

- `entitlements_status` (`none, in_process, approved`).
- `permits_status` per permit class.
- `gc_contract_id`, `architect_id`, `civil_id`, etc. (party pointers).
- `baseline_cost_plan`, `current_cost_plan`.
- `baseline_schedule`, `current_schedule`.
- `lease_up_plan_ref` (for DevelopmentProject).

---

## MarketComp / RentBenchmark / ConcessionBenchmark / UtilityBenchmark / MaterialCostReference / LaborRateReference

All live in `reference/normalized/`. See `reference/README.md` for schemas and update flows. Reference record fields are shared across all reference files; see `schemas/reference_record.yaml`.

---

## ApprovalRequest / EscalationEvent

### ApprovalRequest

**Fields.** `approval_request_id, created_at, created_by (agent or human), subject_object_type (capex_project, change_order, lease_deviation, eviction_filing, vendor_award, bid_award, concession_above_policy, draw_request, final_report_submission, other), subject_object_id, action_proposed, rationale, dollar_impact, risk_flags[], approvers_required[], approvers_notified[], decisions[] (list of {approver, decision, notes, decided_at}), status (pending, approved, approved_with_conditions, denied, expired), expires_at`.

**Guardrail.** The subsystem may not execute a gated action without a linked approval request in `approved` status.

### EscalationEvent

**Fields.** `escalation_event_id, source_pack, source_object_type, source_object_id, kind (safety, legal, fair_housing, financial_threshold, policy_exception, reporting_gap, other), severity (low, medium, high, critical), opened_at, closed_at?, routed_to, resolution_summary?`.

---

## KPIDefinition

Alias for a canonical metric. See `_core/metrics.md`. Every KPI displayed in a template must resolve to a metric slug.

---

## OrgOverlay / PolicyOverlay / MarketOverlay

**Description.** Structured overrides to canonical thresholds, defaults, and references.

See `overlays/README.md`. Overlays declare their scope (org, market, or specific property) and the canonical objects / thresholds they override. They never redefine canonical fields; they only add constraints.

---

## Null handling — global rule

Null does not mean "zero" or "portfolio average." If a required field is null, the skill must surface the missing value and either request it or escalate. See DESIGN_RULES.md Rule 10.
