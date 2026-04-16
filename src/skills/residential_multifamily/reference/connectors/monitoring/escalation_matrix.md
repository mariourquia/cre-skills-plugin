# Escalation Matrix, Integration Layer

status_tag: reference

Who gets called when, mapped to canonical audience slugs and the approval-floor categories in `_core/approval_matrix.md`. All roles are organizational, not named individuals.

## Canonical audience slugs

These slugs are shared with `tailoring/AUDIENCE_MAP.md`:

- `executive`
- `regional_ops`
- `asset_mgmt`
- `finance_reporting`
- `development`
- `construction`
- `compliance_risk`
- `site_ops`

## Functional roles layered over audiences

These roles name the specific responders invoked during integration-layer incidents. They are not audiences; they are assigned on a per-source basis in `source_registry/source_registry.yaml` or for a specific workflow.

- `on_call_ops`, the current on-call engineer for the integration layer.
- `data_owner`, named on the source registry entry; accountable for data quality.
- `business_owner`, named on the source registry entry; accountable for business use.
- `technical_owner`, named on the source registry entry; accountable for adapter and credentials.
- `legal_counsel`, the operator's legal function.
- `compliance_officer`, compliance analyst role; operates within `compliance_risk` audience.
- `data_platform_team`, `finance_systems_team`, `hr_systems_team`, `capital_projects_team`, named technical teams; often map to `technical_owner` for their domains.
- `approvers_for_gate`, resolved per row in `_core/approval_matrix.md`.

## Escalation matrix, by exception category

| Category | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| `dq_blocker` | on_call_ops, data_owner, technical_owner | business_owner, primary consumer audience | finance_reporting, asset_mgmt | executive |
| `dq_warning` | data_owner | business_owner | finance_reporting |  |
| `reconciliation_mismatch` | on_call_ops, data_owner | finance_reporting, business_owner | asset_mgmt | executive |
| `identity_unresolved` | on_call_ops, data_owner | asset_mgmt, regional_ops, finance_reporting | compliance_risk |  |
| `schema_drift` | on_call_ops, technical_owner, data_owner | business_owner | finance_reporting, asset_mgmt | executive |
| `stale_source` | on_call_ops, data_owner | business_owner, primary consumer audience | finance_reporting, asset_mgmt | compliance_risk |
| `mapping_override_pending` | data_owner, business_owner | finance_reporting, asset_mgmt |  |  |
| `approval_override_pending` | approvers_for_gate | finance_reporting, asset_mgmt | executive |  |
| `manual_correction_required` | data_owner, business_owner | technical_owner, finance_reporting |  |  |
| `policy_violation` | on_call_ops, approvers_for_gate | finance_reporting, asset_mgmt | executive | legal_counsel |
| `fair_housing_sensitive` | compliance_risk, legal_counsel | executive |  |  |
| `legal_sensitive` | legal_counsel, compliance_risk | executive |  |  |

## Primary consumer audience per domain

The `primary_consumer_audience` alias resolves per source_domain:

| Domain | Primary consumer audience |
|---|---|
| `pms` | `regional_ops`, `site_ops`, `asset_mgmt` |
| `gl` | `finance_reporting` |
| `crm` | `regional_ops`, `site_ops` |
| `ap` | `finance_reporting`, `regional_ops` |
| `market_data` | `asset_mgmt`, `finance_reporting` |
| `construction` | `construction`, `development`, `asset_mgmt` |
| `hr_payroll` | `regional_ops`, `finance_reporting` |
| `manual_uploads` | resolves per `object_coverage`, use the domain whose data the file contains |

## Escalation by approval-floor category

The approval matrix (`_core/approval_matrix.md`) gates specific action classes. When an integration-layer incident crosses a gate, the escalation follows the matrix, not this document. Mapping for quick reference:

| Approval floor row | Gate | Approvers (canonical) |
|---|---|---|
| 1 | Legal notice (pay-or-quit, cure-or-quit, non-renewal) | `property_manager`, `regional_manager`, overlay-defined owner rep |
| 2 | Eviction filing | `property_manager`, `regional_manager`, `legal_counsel` |
| 3 | Tenant dispute with legal exposure | `regional_manager`, `legal_counsel` |
| 4 | Safety-critical maintenance decision | `maintenance_supervisor`, `property_manager`, `regional_manager` |
| 5 | Licensed engineering judgment | licensed engineer or compliance officer |
| 6 | Financial disbursement mid-tier | `property_manager`, `regional_manager` |
| 7 | Financial disbursement high-tier | `property_manager`, `regional_manager`, `asset_manager` |
| 8 | Contract award above procurement threshold | `regional_manager`, `asset_manager` |
| 9 | Bid award regardless of dollar | `construction_manager`, `asset_manager`; development or executive for major |
| 10 | Change order minor threshold | `construction_manager`, `asset_manager` |
| 11 | Change order major threshold | `construction_manager`, `asset_manager`, `executive` |
| 12 | Draw request submission | `construction_manager`, `asset_manager` |
| 13 | Lease deviation, concession above policy | `property_manager`, `regional_manager` |
| 14 | Lender-facing final submission | `asset_manager`, `finance_reporting` lead |
| 15 | Investor-facing final submission | `asset_manager` or `portfolio_manager`, `executive` |
| 16 | Board-, lender-, investor-facing final report | `executive`, `finance_reporting` lead |
| 17 | Any `human_approval_required` per overlay | per overlay |
| 18 | Hiring, termination, discipline at a site | `regional_manager`, HR |
| 19 | PMA amendment, vendor agreement signature, contract binding owner | `asset_manager` or `portfolio_manager`, `legal_counsel` |
| 20 | Assumption change to ontology, metric contract, alias registry, routing core | system maintainer, designated reviewer |

## Auto-escalation to executive

Per `_core/approval_matrix.md`, any action tagged `fair_housing_risk`, `policy_discrimination_risk`, child-safety, or visible to LPs, lenders, regulators, or press escalates to `executive` regardless of dollar magnitude.

## Quiet-hours policy

- `critical` severity alerts page `on_call_ops` 24/7 regardless of hour.
- `warning` severity alerts observe the operator's business-hours policy as declared in `overlays/org/<org_id>/`.
- `info` severity alerts never page; they land in channels for routine review.
- Fair-housing-sensitive and legal-sensitive categories are always treated as critical regardless of the nominal severity of their trigger alert.

## Review cadence for this matrix

- Quarterly review by the integration-layer operations lead with sign-off from `finance_reporting`, `asset_mgmt`, and `compliance_risk`.
- Annual review with `executive` attendance.
- Any change logs per `_core/change_log_conventions.md`.
