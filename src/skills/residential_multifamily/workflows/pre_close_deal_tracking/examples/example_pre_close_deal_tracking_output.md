# Example — Pre-Close Deal Tracking (abridged)

**Prompt.** "Build the closing checklist snapshot for DP_DEAL_019. Daily close tracking — what's open this week? Flag key dates in the alert band."

**As-of.** Wednesday 2026-04-15 end-of-day; adapter `as_of_date=2026-04-15` (status=sample).

**Inputs.** Dealpath normalized `deal`, `deal_key_date`, and `deal_milestone` records; closing-checklist template overlay; lender deliverable schedule; escrow agent SLA; approval_threshold_defaults; close_calendar__portfolio.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized (target post-close)
- management_mode: third_party_managed (target)
- role: deal_team_lead
- market: Charlotte
- output_type: kpi_review + checklist + memo
- decision_severity: recommendation
- org_id: {org}
- deal_id: DP_DEAL_019

## Expected packs loaded

- `workflows/pre_close_deal_tracking/`
- `workflows/pipeline_review/` (cross-linked — retrade screen consumer)
- `workflows/investment_committee_prep/` (cross-linked — 1 IC condition open)
- `workflows/acquisition_handoff/` (queued for post-close handoff, trigger date = expected_close)

## Expected references

- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml`
- `reference/connectors/deal_pipeline/schema.yaml`
- `reference/connectors/master_data/asset_crosswalk.yaml`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/close_calendar__portfolio.csv`

## DQ gate outcome

- `dp_freshness_deals`: pass (feed landed 2026-04-15 17:32Z).
- `dp_completeness_required_fields`: pass.
- `dp_completeness_ic_record`: pass — `ic_decision_date` present.
- `dp_handoff_lag`: n/a (not yet closed).
- `dp_conformance_stage_enum`: pass.

## Deal header

| Field | Value |
|---|---|
| deal_id | DP_DEAL_019 |
| deal_name | Ashford Run (248-unit garden acquisition) |
| pipeline_stage | pre_close |
| expected_close | 2026-04-22 |
| target legal entity | ENT_ASHFORD_RUN_LLC |
| target property | prop_ashford_run (placeholder) |

## Key-date countdown

| Key date | date_kind | target_date | actual_date | days remaining | band |
|---|---|---|---|---|---|
| LOI executed | `loi_executed` | 2026-02-10 | 2026-02-10 | — | achieved |
| PSA executed | `psa_executed` | 2026-03-05 | 2026-03-05 | — | achieved |
| DD period end | `dd_end` | 2026-04-18 | — | 3 | alert (within overlay band) |
| Financing contingency | `financing_contingency` | 2026-04-19 | — | 4 | alert (within overlay band) |
| Expected close | `expected_close` | 2026-04-22 | — | 7 | within |
| Tax lookback | (tax) | 2026-04-15 | 2026-04-15 | 0 | compliant |

## Open contingencies

| # | Contingency | Responsible | Evidence state | Deadline | Status |
|---|---|---|---|---|---|
| 1 | Title commitment review | L. Garcia (legal) | evidence pending | 2026-04-17 | open — flag |
| 2 | Survey acceptance | deal_team_lead + legal | evidence received | 2026-04-17 | pending legal sign-off |
| 3 | Phase I ESA | third-party consultant | evidence on file | 2026-04-10 | cleared |
| 4 | IC-approval condition: roof scope bid confirmation | asset_mgmt_director | open | 2026-04-20 | open — routed via `workflows/investment_committee_prep/` |

## Lender deliverables

| # | Item | Responsible | State | Days to lender deadline |
|---|---|---|---|---|
| 1 | Entity formation certificate | finance_systems_team | complete | — |
| 2 | Certificate of good standing | finance_systems_team | pending | 3 |
| 3 | Insurance binder (property + liability) | asset_mgmt_director | pending | 3 |
| 4 | Opinion of counsel | legal | complete | — |
| 5 | Zoning compliance letter | legal | complete | — |
| 6 | Survey + title pro forma | legal | complete | — |
| 7 | Rent roll certification | regional_ops_director | complete | — |
| 8 | Operating budget | reporting_finance_ops_lead | complete | — |

- `lender_deliverable_status_score` = **0.75** (proposed). Within overlay band but trending tight.

## Escrow status

- Earnest money: **posted** 2026-02-11 ($1.25MM).
- Final deposit required: 2026-04-21.
- Escrow agent: (stub) — SLA per overlay.
- `escrow_funding_status` = **partial** (proposed).

## Closing certainty

- `closing_certainty_score` = **0.82** (proposed).
- Drivers: open title commitment review (weight: high), 2 pending lender deliverables (weight: medium), open IC roof-scope condition (weight: medium), no retrade or price-change signal (weight: positive).
- `key_date_breach_count` = **0** (proposed).
- `days_to_close` = **7** (proposed).
- `pre_close_cycle_time` = **41** days (PSA execution → today; proposed).

## Escalation drafts

- **Draft composed (`draft_for_review`)** to `deal_team_lead`: title commitment review flag, deadline 2026-04-17. Cc: `investments_lead`.
- **No retrade / price-change** signal detected; retrade-risk line not populated on this run.

## Gates potentially triggered (elsewhere)

- `workflows/investment_committee_prep/`: IC condition tracking — roof-scope condition open past `resolution_deadline` if not cleared by 2026-04-20.
- `workflows/owner_approval_routing/`: row tied to any lender deliverable blocked > 48h from deadline.
- `workflows/acquisition_handoff/`: triggers on `deal_close_date_actual`.

## Per-deal narrative memo (abridged)

> Ashford Run is on track to close 2026-04-22 conditional on title commitment review by Friday and receipt of the insurance binder and entity good-standing certificate for the lender package. DD and financing-contingency dates are both in the overlay alert band (3 and 4 business days remaining). One IC-approved condition remains open — the roof-scope bid confirmation — tracked separately via `workflows/investment_committee_prep/`. Escrow shows earnest money posted; final deposit due 2026-04-21. No retrade or price-change signals from Dealpath. Closing certainty score (proposed) of 0.82 reflects the tight-but-manageable lender deliverable window.

## Confidence banner

```
References:
- dealpath_deal_pipeline@2026-04-15 (sample)
- deal_pipeline/schema.yaml@0.1.0
- asset_crosswalk@2026-04-15 (sample)
- close_calendar__portfolio@2026-03-31 (starter)
- approval_threshold_defaults@2026-03-31 (starter)
DQ: all blockers pass; no warnings.
Metrics: all metric slugs proposed (not yet in _core/metrics.md).
Canonical extensions required: Deal, DealKeyDate, DealMilestone
(tracked under deal_pipeline wave-4 extension).
```
