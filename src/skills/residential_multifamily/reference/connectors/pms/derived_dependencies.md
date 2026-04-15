# PMS Derived Dependencies

Which canonical metrics, workflows, and templates depend on normalized PMS data. Metric slugs and workflow slugs below reference names in `_core/metrics.md` and `workflows/`.

## Required normalized inputs

The following PMS entities must be landed and QA-passed before downstream recomputation is triggered:

- `pms.property`: base for every per-property metric.
- `pms.unit`: unit status, rentable counts, unit-type mix.
- `pms.lease`: active lease set, lease expiry, rent roll.
- `pms.lease_event`: lease lifecycle history (signed, move-in, notice, move-out, broken).
- `pms.charge`: resident ledger charges.
- `pms.payment`: resident ledger payments.
- `pms.delinquency_case`: case-level aging and legal stage.

## Optional enrichment inputs

- `pms.lead`, `pms.tour`, `pms.application`, `pms.renewal_offer`: enrich leasing-funnel metrics; absence causes leasing metrics to degrade to funnel-less summaries.
- `pms.work_order`: feeds maintenance and SLA dashboards.
- `pms.turn`: feeds unit turn and capex-per-turn metrics.

## Confidence minimum

Downstream consumption requires that the reconciliation report for the window has:

- No open blocker failures on the required inputs.
- No more than one repeated warning per property per window.
- Provenance fields present on every row.

If a required input carries an open blocker, downstream metrics and workflows refuse to run (fail closed).

## Blocking data issues

The following issues block every PMS-dependent metric for the affected scope:

- Unit-count reconciliation failure against the property master.
- Lease-status rollup failure (statuses do not sum to rentable count).
- Missing required-field population on any required input.
- Provenance missing on any row.
- Identity-resolution gap (a property_id or unit_id referenced but not resolvable via crosswalk).

## Fallback mode when partial

When only a subset of PMS entities is available (e.g., property + unit but no lease), the subsystem degrades as follows:

- Property- and unit-level structural metrics (unit count, unit mix, NRSF, classification mix) still compute.
- Occupancy metrics refuse; notices, renewals, and move-ins cannot be derived from structure alone.
- Charges, payments, and delinquency metrics refuse.
- Leasing-funnel metrics refuse; CRM-only interactions without PMS lead grounding do not feed the funnel.

No metric silently ingests a partial landing. Every consumer checks the `reconciliation_report.json` before loading.

## Canonical metrics that depend on PMS

### Property Operations family

- `physical_occupancy`: requires `pms.unit` (status), `pms.property` (unit_count_rentable).
- `leased_occupancy`: requires `pms.unit`, `pms.lease` (status in in_effect, notice, preleased).
- `economic_occupancy`: requires `pms.charge` (rental-income charges) and `pms.payment` (applied cash).
- `notice_exposure`: requires `pms.lease` (notice status), `pms.lease_event` (notice_to_vacate).
- `preleased_occupancy`: requires `pms.lease` (future start_date), `pms.unit` (status).
- `lead_response_time`: requires `pms.lead` and `crm.lead_interaction`.
- `tour_conversion`: requires `pms.lead`, `pms.tour`.
- `application_conversion`: requires `pms.application`, `pms.tour`.
- `approval_rate`: requires `pms.application`.
- `move_in_conversion`: requires `pms.application`, `pms.lease`, `pms.lease_event`.
- `renewal_offer_rate`: requires `pms.renewal_offer`, `pms.lease`.
- `renewal_acceptance_rate`: requires `pms.renewal_offer`.
- `turnover_rate`: requires `pms.lease_event` (move_in, move_out).
- `average_days_vacant`: requires `pms.unit`, `pms.lease_event`.
- `make_ready_days`: requires `pms.turn` (move_out_date, actual_ready_date).
- `open_work_orders`, `work_order_aging`, `repeat_work_order_rate`: require `pms.work_order`.
- `delinquency_rate_30plus`: requires `pms.delinquency_case`.
- `collections_rate`: requires `pms.charge`, `pms.payment`.
- `bad_debt_rate`: requires `pms.delinquency_case` (write-off stage), `pms.charge`.
- `concession_rate`: requires `pms.charge` (charge_type in concession, concession_reversal).
- `rent_growth_new_lease`, `rent_growth_renewal`, `blended_lease_trade_out`: require `pms.lease`, `pms.lease_event`.
- `market_to_lease_gap`, `loss_to_lease`: require `pms.lease`, `pms.unit`, plus market_data.

### Asset Management family

- `noi`, `noi_margin`: require the full PMS charge and payment stack plus GL alignment.
- `dscr`, `debt_yield`: derived from `noi` and debt schedule.
- `stabilization_pace_vs_plan`: requires `pms.lease_event` (move_in), `pms.unit`.

### Development and Construction family

- `lease_up_pace_post_delivery`: requires `pms.lease_event` on newly delivered units.

## Example output types

- Monthly property operating review report (uses most PMS entities).
- Variance narrative generator (uses `pms.charge`, `pms.payment`, `pms.lease`).
- Delinquency workout playbook (uses `pms.delinquency_case`, `pms.charge`, `pms.payment`).
- Lease-up war room dashboard (uses `pms.lead` + CRM + market_data).
- Work-order triage queue (uses `pms.work_order`).

## Dependent workflows

Workflows under `workflows/` that depend on PMS being QA-passed:

- `monthly_property_operating_review`
- `delinquency_collections`
- `lead_to_lease_funnel_review`
- `renewal_retention`
- `unit_turn_make_ready`
- `work_order_triage`
- `move_in_administration`
- `move_out_administration`
- `vendor_dispatch_sla_review` (for PMS-issued work orders)
