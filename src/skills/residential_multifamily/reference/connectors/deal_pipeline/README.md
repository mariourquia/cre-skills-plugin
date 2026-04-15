# Deal Pipeline Connector (stub, vendor-neutral)

Investment deal pipeline feed. Tracks the pre-close lifecycle of acquisition, development, recapitalization, and refinance deals from sourcing through close, and seeds handoff records to downstream property management, accounting, and construction systems.

## Status

`status: stub` — schema, mapping template, sample, and reconciliation checks only. Vendor-specific adapters live under `../adapters/` (e.g., `dealpath_deal_pipeline/`).

## Scope

Vendor-agnostic. Pre-close truth for:

- Deal identity and classification (acquisition, development, refinance, recapitalization, other).
- Pipeline stage history (sourcing, under_loi, under_psa, under_dd, ic_review, approved, closed, dropped, dead).
- Investment-committee review milestones (pre_ic, ic_scheduled, ic_approved, ic_deferred, ic_declined).
- Key deal dates (LOI executed, PSA executed, DD start, DD end, financing contingency, expected close, actual close, delivery target).
- Deal-team assignments (sponsor, lead analyst, IC sponsor, capital markets, asset management lead).
- High-level financial placeholders (acquisition price placeholder, development budget placeholder, target leverage ratio, financing placeholder). Detailed underwriting numbers do NOT live here; they live in the underwriting model and, post-close, in the GL and PMS feeds.
- Asset placeholders (prospective property / site identity before a canonical Property master record exists).

Post-close, the deal-pipeline domain becomes secondary. AppFolio takes over as the PMS source of truth, Intacct as the GL source of truth, and Procore as the construction source of truth. The deal record remains as a historical pointer; the handoff event is tracked via reconciliation checks.

## Entities

| Entity | One-liner |
|---|---|
| `deal` | One row per investment deal (acquisition, development, refinance, recap). |
| `deal_stage` | One row per stage entry for a deal (pipeline stage history). |
| `deal_milestone` | One row per discrete milestone event (IC, key date, handoff trigger). |
| `investment_committee_review` | One row per IC review cycle for a deal. |
| `deal_key_date` | One row per named key date per deal (LOI, PSA, DD, close, delivery). |
| `deal_team_assignment` | One row per team-member assignment per deal. |
| `deal_financing_placeholder` | One row per financing commitment placeholder tracked pre-close. |
| `deal_asset_placeholder` | One row per prospective asset / site referenced by a deal, pre-canonical-master. |

## Canonical objects covered

Maps (with seed / placeholder status) to the following canonical ontology objects. Canonical records remain in their authoritative domain; the deal-pipeline domain only supplies pre-close seeds and handoff pointers.

- `Property` (placeholder) — pre-close; canonical Property master is created on close via `property_master_crosswalk`.
- `DevelopmentProject` (seed) — for deal_type = development; seeds the DevelopmentProject canonical record at approval.
- `CapexProject` (seed) — for deal_type = recapitalization or major-reno acquisitions that include a capex program.
- `Deal` (canonical, new) — the canonical deal record itself.
- `ApprovalRequest` (placeholder) — IC approvals map to the canonical `ApprovalRequest` with `subject_object_type = deal_approval`.
- `Asset` (seed, placeholder) — prospective asset identity; resolves via the pending `asset_crosswalk` (see `master_data/asset_crosswalk.yaml`, proposed).

## Integration

- `deal_pipeline.deal` seeds `canonical.property_master_crosswalk` at close for acquisitions.
- `deal_pipeline.deal` of type `development` seeds `canonical.dev_project_crosswalk`.
- `deal_pipeline.investment_committee_review` reconciles to `canonical.ApprovalRequest` for IC audit trails.
- `deal_pipeline.deal_key_date` drives the executive pipeline summary and pre-close workflows.
- `deal_pipeline.deal_asset_placeholder` resolves via the proposed `master_data/asset_crosswalk.yaml` once the canonical asset master is established.

Downstream consumers (proposed workflows, see `../adapters/dealpath_deal_pipeline/workflow_activation_additions.yaml`):

- `pipeline_review` — weekly deal pipeline reporting.
- `pre_close_deal_tracking` — weekly deal key-date status.
- `development_pipeline_tracking` — development deal portfolio status.
- `acquisition_handoff` — acquisition close-to-operations handoff.
- `investment_committee_prep` — pre-IC package assembly.
- `executive_pipeline_summary` — executive-audience pipeline rollup.

## Constraints

- Never carries PII for individual counterparties beyond broker name and seller legal-entity label; buyer-side deal-team assignments use internal role slugs or name placeholders.
- No underwriting numbers (IRR, cap rate, DSCR, equity multiple) live here; those are in the underwriting model and, post-close, in the GL and PMS feeds.
- No credential or closing document content lives in the connector; document references are pointer strings only.

See `INGESTION.md` for the landing convention.
