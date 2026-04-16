# Procore Construction Adapter

Adapter id: `procore_construction`
Vendor family: `procore_family`
Connector domain: `construction`
Status: `stub`
Rollout wave: `wave_4`

## Role in the integration layer

Procore is the primary source of construction-side data for the residential
multifamily subsystem:

- Project master (`Projects` API).
- Budget (direct costs with line items; Original Budget and Revised Budget
  snapshots).
- Commitments (`Purchase Orders` and `Work Order Contracts` / subcontracts).
- Change Events and Commitment Change Orders.
- Payment Applications (operator term: pay apps; canonical: `draw_request`).
- Schedule (native Gantt milestones or MS Project / P6 imports).
- Punchlist items and closeout documents.
- Project Financials snapshot state.

Procore is **not** the system of record for posted GL actuals; Intacct owns
that. Procore is not the system of record for property operations post-
delivery; AppFolio owns that. Procore's construction-side totals reconcile
against Intacct postings through the canonical reconciliation framework.

## Project vs property semantics

Procore models a **project** — a unit of construction work with its own
budget, schedule, directory, and commitments. A canonical `Property` (per
`_core/ontology.md`) is the operating asset.

- Ground-up development: Procore project predates the canonical Property;
  the Property record opens in AppFolio at delivery.
- Major renovation: Procore project runs concurrent with an active
  Property; resident-occupied buildings require tight PMS/Procore
  coordination.
- Phased delivery (e.g., two-building development): one Procore project
  may split across multiple canonical Properties via
  `related_canonical_ids` on the property_master_crosswalk.
- Project split: one Procore project ultimately delivering two properties
  (e.g., separate legal entities). Tracked via `property_master_crosswalk`
  and `dev_project_crosswalk`.

Procore project name and AppFolio property name **do not** reliably agree.
Name matching is unsafe; canonical joins go through crosswalks.

## Commitment model

Procore uses two commitment types:

- **Purchase Orders (POs)**: typically material or equipment purchases.
  Often simpler line-item structure.
- **Work Order Contracts (subcontracts)**: labor or full-scope trade
  commitments. Drive the majority of change-order and pay-application
  activity.

Both normalize to the canonical construction `commitment` entity (see open
question below). `line_item_type` distinguishes Labor / Material / Equipment
/ Subcontract / Other Cost / Professional Service.

**Open question for Wave 4 integration agent.** The canonical ontology at
`_core/ontology.md` does not list `Commitment` as a first-class canonical
object. Construction commitments are currently modeled as an extension of
`VendorAgreement` scoped to a `CapexProject`. Procore's first-class
commitment model surfaces this gap. Recommended: add `Commitment` to the
ontology with fields
`commitment_id, capex_project_id, vendor_id, commitment_type (purchase_order, subcontract), contract_total_cents, revised_contract_total_cents, status, retention_percent, billed_to_date_cents, paid_to_date_cents`.
Flagged in `edge_cases.md` and on this adapter's open-questions list.

## Change order lifecycle

Procore distinguishes:

- **Change Events**: upstream cost impacts logged before a formal CO; may
  roll up to a Pending Revised Budget but do not change commitment totals.
- **Commitment Change Orders (CCOs)**: formal change to a commitment.
  States: `draft`, `pending`, `approved`, `void`.
- **Potential Change Orders (PCOs) / Change Order Requests (CORs)**: some
  operators use these mid-pipeline between Change Event and CCO.

The adapter normalizes Procore CO state to canonical:

| Procore state | Canonical `status` |
|---|---|
| draft | proposed |
| pending | pending_approval |
| approved | approved |
| void | rejected (with `void_reason` note) |

Pending COs are excluded from the canonical commitment ceiling per the
canonical construction reconciliation rule; draws referencing pending COs
are flagged.

## Draw / pay application workflow

Procore pay applications (also called requisitions) normalize to canonical
`draw_request`. Each pay app carries:

- `period_start` / `period_end` and `billing_date`.
- `current_payment_due` (canonical `amount_requested_cents`).
- `retainage_held_this_period`, `retainage_released_this_period`,
  `retainage_balance`.
- `work_completed_to_date` and `stored_materials_to_date`
  (used to derive canonical `percent_complete_cost`).
- Line-item detail at the commitment schedule-of-values level.

Approval flows through Procore then posts to Intacct AP. Draw timing
(Procore approval vs Intacct posting) is expected to differ; the
reconciliation framework handles the timing band.

## Schedule structure

Procore schedule sources:

- Native Gantt (Procore's schedule module).
- MS Project `.mpp` import.
- Primavera P6 XML import.

Each milestone carries `baseline_start`, `baseline_finish`, `forecast_start`,
`forecast_finish`, `actual_finish`. Baseline preservation requires the
Procore schedule baseline feature to be enabled at project setup. Operators
who skip baseline capture have no slippage reference; flag as a data
readiness gap.

## Handoff to AppFolio at delivery

At `project_phase = Post Construction` (canonical `delivered` / `lease_up`):

1. Procore marks the project `closed_out`.
2. A canonical `Property` record opens in AppFolio with the
   `capex_project_crosswalk` row linking back to the Procore project id.
3. Final capex totals lock in Intacct; Procore becomes a historical source
   for warranty claims.
4. Punchlist closeout rate must pass before AppFolio units begin leasing;
   `punchlist_closeout_rate` blocker applies.

Handoff trigger: `project_phase` changes from `current_construction` to
`post_construction`. Emits an event that activates:

- `property_master_crosswalk` intake for new Property ids.
- `post_close_onboarding_transition` skill workflow.
- AppFolio adapter ingestion start.

## File layout

```
procore_construction/
  manifest.yaml
  README.md
  source_contract.yaml       # Raw Procore payload shape per entity
  normalized_contract.yaml   # Canonical mapping
  field_mapping.yaml         # Full per-entity field map
  dq_rules.yaml              # Procore-specific DQ rules
  reconciliation_rules.md    # Narrative reconciliation spec
  reconciliation_checks.yaml # Machine-readable checks
  edge_cases.md              # Known edge cases
  source_registry_entry.yaml # source_registry fragment
  crosswalk_additions.yaml   # Rows to add to master_data crosswalks
  workflow_activation_additions.yaml # Procore's role per workflow
  sample_raw/                # Synthetic JSONL per entity
  sample_normalized/         # Synthetic canonical output
  runbooks/                  # Onboarding + common issues
  tests/                     # pytest adapter conformance tests
```

## Sample data

All sample records under `sample_raw/` and `sample_normalized/` carry
`status: sample` and use synthetic ids only. No real customer data, no
credentials, no numeric thresholds embedded in prose.
