# Example 01 — ROUTING

## Matched rule

- `r001_property_manager_stabilized_middle_market` (primary)
- `r009_direct_workflow` (secondary) — because the request text implies `workflow=delinquency_collections`.

## Axis resolution

| Axis | Resolved to | Source of resolution |
|---|---|---|
| `asset_class` | `residential_multifamily` | default |
| `segment` | `middle_market` | property master |
| `form_factor` | `garden` | property master |
| `lifecycle_stage` | `stabilized` | property master |
| `management_mode` | `third_party_managed` | property master |
| `role` | `property_manager` | session context |
| `workflow` | `delinquency_collections` | inferred from request text "delinquency action plan" |
| `market` | `Charlotte` | property master |
| `submarket` | `South End` | property master |
| `output_type` | `checklist` + `memo` | request text ("action plan … draft comms") |
| `decision_severity` | `recommendation` | no autonomous action implied |
| `org_id` | `examples_org` | session context |

## Packs loaded

- Role pack: `roles/property_manager/` (primary).
- Workflow pack: `workflows/delinquency_collections/` (direct match).
- Segment overlay: `overlays/segments/middle_market/`.
- Form-factor overlay: `overlays/form_factor/garden/`.
- Lifecycle overlay: `overlays/lifecycle/stabilized/`.
- Management-mode overlay: `overlays/management_mode/third_party_managed/`.
- Org overlay: `overlays/org/examples_org/` (loaded first per overlay merge rules).

## Overlay merge order applied

1. canonical `_core/` defaults
2. segment (`middle_market`)
3. form_factor (`garden`)
4. lifecycle (`stabilized`)
5. management_mode (`third_party_managed`)
6. market (none market-specific overlay present; no-op)
7. org (`examples_org`) — wins final

## References loaded

| Path | Category | as-of | Status | Fallback if missing |
|---|---|---|---|---|
| `reference/normalized/delinquency_playbook_middle_market.csv` | approval_threshold_policy | 2026-03-15 | starter | refuse |
| `reference/normalized/collections_benchmarks__southeast_mf.csv` | occupancy_benchmark | 2026-03-31 | sample | use_portfolio_average |
| `reference/normalized/approval_threshold_defaults.csv` | approval_threshold_policy | 2026-03-15 | starter | refuse |
| `reference/normalized/market_rents__charlotte_mf.csv` | market_rent_benchmark | 2026-03-31 | sample | ask_user |
| `overlays/org/examples_org/approval_matrix.yaml` | approval_threshold_policy | 2026-04-01 | approved | refuse |

## Metrics engaged

- `delinquency_rate_30plus`
- `collections_rate`
- `bad_debt_rate` (T12 contextual)
- `concession_rate` (for non-standard plan context)
- `notice_exposure` (to cross-check rollover risk)

## Gates surfaced (approval-matrix rows)

- Row 1 `legal_notice`: any pay-or-quit or rent-default notice requires approval.
- Row 2 `eviction_filing`: any eviction-track action requires approval + legal counsel.
- Row 3 `fair_housing_flag`: any flag raised during review routes to approval.
- Row 13 `concession_over_policy / non_standard_payment_plan`: routes to regional + owner rep.

## Escalation routes pre-identified

- PM -> regional manager -> asset manager (owner-side) for any Row 1 / 2 action.
- PM -> TPM oversight lead (owner-side) for any TPM-execution-dependent step.

## Templates selected for output assembly

- `templates/site_ops/weekly_delinquency_review.md` (main structure).
- `templates/resident_comms/portal_delinquency_draft_for_review.md` (resident draft, legal review required).
- `templates/tpm_oversight/owner_approval_routing_checklist.md` (approval routing for any gated step).

## Output shape

- Short KPI snapshot + aging-bucket movement.
- Stage-by-stage playbook (middle-market) with owner, due date, approval gate.
- Communication drafts pinned to templates with legal_review banner preserved.
- Confidence banner citing reference freshness + status.
