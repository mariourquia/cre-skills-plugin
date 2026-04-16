# Dealpath Deal Pipeline Adapter

Status: stub
Wave: 4
Domain: deal_pipeline (new in wave 4)

## Role

Dealpath is the primary source of truth for pre-close deal state. It owns:

- deal pipeline (sourcing through close)
- IC milestones (pre_ic, ic_scheduled, ic_approved/declined/deferred)
- deal team assignments
- deal key dates (LOI, PSA, DD start/end, financing contingency, expected close, actual close)
- deal-level financial summary (acquisition price placeholder; no underwriting model)

It seeds downstream:
- AppFolio property setup (post-close acquisition or post-delivery development)
- Procore project creation (post-IC for development deals)
- Intacct entity / project / location dimension setup
- Canonical `approval_request` for IC decisions

## Source-of-truth claims

| Object | Role | Claim until | Then transitions to |
|---|---|---|---|
| deal | primary | always (deal is the canonical pre-close artifact) | n/a |
| asset | primary | post-close | AppFolio + Intacct co-define operating asset |
| development_project | primary (seed) | gc_award | Procore primary |
| capex_project | primary (seed) | project execution start | Procore + Intacct |
| property | placeholder | property setup complete | AppFolio primary |
| approval_request (IC) | primary | always | n/a |

## What's covered

- `deal` records with stage progression
- `deal_milestone` events (IC approvals, key dates)
- `deal_team_assignment` records
- `deal_key_date` records (LOI, PSA, financing contingency, close)
- `asset` records (Dealpath asset master)
- Lifecycle handoff seed records

## What's deferred

- Detailed underwriting model (lives in deal-team workbooks, not Dealpath)
- Post-close operating data (AppFolio + Intacct take over)
- Construction execution (Procore takes over)
- Investor communications (separate stack outside this wave)

## Adapter files

| File | Purpose |
|---|---|
| `manifest.yaml` | Adapter declaration |
| `source_contract.yaml` | Raw Dealpath payload shapes per entity (PENDING) |
| `normalized_contract.yaml` | Mapping to canonical objects (PENDING) |
| `field_mapping.yaml` | Field-by-field mapping (PENDING) |
| `sample_raw/` | Synthetic raw payloads (PENDING) |
| `sample_normalized/` | Synthetic canonical payloads (PENDING) |
| `dq_rules.yaml` | Dealpath-specific DQ rules |
| `reconciliation_rules.md` | Dealpath ↔ AppFolio + Intacct + Procore recon (PENDING) |
| `edge_cases.md` | Documented edge cases (PENDING) |
| `source_registry_entry.yaml` | Source registry fragment |
| `crosswalk_additions.yaml` | Crosswalk row additions (PENDING) |
| `workflow_activation_additions.yaml` | Workflow activation fragment |
| `tests/test_adapter.py` | Adapter-local pytest tests |
| `runbooks/dealpath_onboarding.md` | Onboarding runbook (PENDING) |
| `runbooks/dealpath_common_issues.md` | Common-issue runbook (PENDING) |

PENDING = scheduled for next wave-4 implementation pass.

## Open questions

See `_core/stack_wave4/open_questions_and_risks.md`:

- `asset_crosswalk.yaml` must be created in `master_data/`
- Proposed workflows (`pipeline_review`, `pre_close_deal_tracking`, etc.) must be added to `workflows/`
- Whether GraySail integrates as part of `deal_pipeline` or stays separate

## Lifecycle handoffs

See `_core/stack_wave4/lifecycle_handoffs.md` Handoffs 1, 2, 3.
