# Audience Map — Tailoring (Residential Multifamily)

Canonical 8-audience split for the residential multifamily tailoring interview. Supersedes the prior 7-audience layout (`coo.yaml`, `cfo.yaml`, `regional_ops.yaml`, `asset_mgmt.yaml`, `development.yaml`, `construction.yaml`, `reporting.yaml`).

The split separates top-of-house strategy (executive) from functional depth (finance, ops, compliance, site), so each audience can be interviewed in isolation and re-interviewed on its own cadence. Cross-audience conflicts are surfaced by the preview layer (`DIFF_APPROVAL_PREVIEW.md`) and resolved before apply.

## The 8 audiences

| # | Audience slug | Scope | Primary bank | Secondary (read-only) banks | Approvers routed | Required for new-org onboarding |
|---|---|---|---|---|---|---|
| 1 | `executive` | CEO / COO / CFO top-of-house: operating model, portfolio segmentation, capital posture, approval-matrix tier structure, growth vs disposition, board/LP reporting cadence | `executive.yaml` | `finance_reporting`, `compliance_risk` | `ceo_executive_leader`, `coo_operations_leader`, `cfo_finance_leader` | Yes (p1) |
| 2 | `regional_ops` | RM, DOO, portfolio-level operating cadence, span of control, regional staffing | `regional_ops.yaml` | `site_ops`, `asset_mgmt` | `director_of_operations`, `regional_manager` | Yes (p1) |
| 3 | `asset_mgmt` | AM / PM asset-level performance, business plan posture, variance threshold policy, hold-period posture | `asset_mgmt.yaml` | `finance_reporting`, `regional_ops` | `asset_manager`, `portfolio_manager` | Yes (p1) |
| 4 | `finance_reporting` | CFO-detail finance plus reporting: chart of accounts, budget/forecast cadence, variance policy, lender / investor / audit cadence | `finance_reporting.yaml` | `executive`, `asset_mgmt` | `cfo_finance_leader`, `reporting_finance_ops_lead` | Yes (p1) |
| 5 | `development` | Dev pipeline, underwriting assumptions, preconstruction sign-off posture, developer fee structure | `development.yaml` | `construction`, `executive` | `development_manager` | Optional (only if operator has dev pipeline) |
| 6 | `construction` | GC selection, contract structure, change order policy, draw approval policy | `construction.yaml` | `development`, `asset_mgmt` | `construction_manager` | Optional (only if operator has active construction) |
| 7 | `compliance_risk` | Fair housing, screening, VAWA, regulatory-program participation (LIHTC / HUD / USDA / state / mixed-income), REAC / NSPIRE posture, insurance, safety | `compliance_risk.yaml` | `executive`, `site_ops` | `coo_operations_leader`, `legal_counsel`, `compliance_officer` | Yes (p1) |
| 8 | `site_ops` | PM / APM / leasing / maintenance norms, staffing schedule defaults, SLA commitments, unit turn scope, vendor dispatch authority | `site_ops.yaml` | `regional_ops` | `property_manager` (read-only — surfaced to `regional_ops` and `asset_mgmt` for policy endorsement) | Optional (default posture inherits from `regional_ops` until explicit site-level overrides) |

Secondary (read-only) banks: answers already captured in a prior audience's session are surfaced to the current interviewer for context only; they cannot be overwritten from a secondary audience. Overwrites require re-entering the primary audience.

## Legacy bank mapping

Prior sessions that cite a legacy bank slug resolve transparently to the new banks:

| Legacy bank | New primary | New secondary | Notes |
|---|---|---|---|
| `coo.yaml` | `executive.yaml` (top-of-house) | `regional_ops.yaml` (ops span of control) | Top-of-house strategy questions moved to `executive`; span-of-control, regional operating cadence, and portfolio-oversight questions moved to `regional_ops`. |
| `cfo.yaml` | `executive.yaml` (CEO/COO/CFO top-of-house posture) | `finance_reporting.yaml` (CFO detail) | Portfolio-wide capital posture and approval-tier structure moved to `executive`; chart of accounts, variance thresholds, reporting cadence, investor/lender cadence moved to `finance_reporting`. |
| `reporting.yaml` | `finance_reporting.yaml` | — | Report inventory, platform, automation, data sources folded into `finance_reporting`. |

The legacy `.yaml` files are retained under `tailoring/question_banks/` with deprecation banners (see top-of-file comments in `coo.yaml`, `cfo.yaml`, `reporting.yaml`). Removal is scheduled for the next refinement cycle after the TUI is updated to consume the 8-bank map.

## When each audience is required (new-org triggers)

| Audience | Trigger condition |
|---|---|
| `executive` | Always required. No other audience's answers are accepted as authoritative until the executive session exists. |
| `regional_ops` | Always required when the operator runs operations (any `operating_model` other than 100% third-party with no oversight role). |
| `asset_mgmt` | Always required if the operator owns or co-owns assets (i.e., not a pure fee-manager). |
| `finance_reporting` | Always required. |
| `development` | Required if the operator has one or more properties in `lifecycle: development` or `lifecycle: construction`, or declares an active dev pipeline during the `executive` interview. |
| `construction` | Required if the operator has properties in `lifecycle: construction` or an active renovation program. |
| `compliance_risk` | Always required. The `executive` interview asks whether the operator runs LIHTC, HUD, USDA, state program, or mixed-income properties; `compliance_risk` then branches per program. Conventional-only operators still must complete the fair-housing / screening / VAWA / insurance / emergency-response portion. |
| `site_ops` | Optional. Defaults inherit from `regional_ops`. Required only when the operator's site-level norms (staffing, SLAs, turn scope) deviate from the regional default and the operator wants property-level posture recorded. |

## Cross-references

- `DIFF_APPROVAL_PREVIEW.md` — how proposed overlay diffs are previewed, signed off, and conflict-reconciled across audiences.
- `MISSING_DOC_MATRIX.md` — expected documents per audience and how missing documents are tracked.
- `_core/approval_matrix.md` — the canonical approval floor each audience's answers must respect.
- `tailoring/SKILL.md` — the interview flow sequencing across audiences.
- `tailoring/doc_catalog.yaml` — the document catalog referenced by `missing_doc_triggers` across all 8 banks.

## Versioning

`audience_map_version: "0.1.0"` — bump on audience add/remove or any bank slug rename. TUI consumers pin to a compatible major version.
