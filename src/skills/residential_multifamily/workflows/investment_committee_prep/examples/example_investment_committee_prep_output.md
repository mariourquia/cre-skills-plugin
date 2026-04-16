# Example — Investment Committee Prep (abridged)

**Prompt.** "Prep the IC packet for the 2026-04-22 cycle. Four deals on docket; flag any condition past deadline and confirm LP coverage by fund."

**As-of.** 2026-04-15 (prep window day -7); adapter `as_of_date=2026-04-15` (status=sample).

**Inputs.** Dealpath normalized `deal`, `deal_milestone`, `investment_committee_review`, `deal_key_date`; canonical `asset` master; IC calendar + docket policy overlay; IC memo templates; sensitivity-test outputs from `skills/sensitivity_stress_test`; `rent_comp_evidence__charlotte_mf.csv` + `rent_comp_evidence__atlanta_mf.csv` + `rent_comp_evidence__phoenix_mf.csv`; LP capital snapshot; debt term sheet state from `workflows/pipeline_review`; IC-member roster.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: docket mix (middle_market 3, luxury 1)
- form_factor: mixed (garden 2, urban_mid_rise 1, high_rise 1)
- lifecycle_stage: pre-close bias (stabilized 3, development 1)
- management_mode: n/a at deal grain
- role: investments_lead
- market: mixed (Charlotte, Atlanta, Phoenix)
- output_type: memo + dashboard + checklist
- decision_severity: action_requires_approval (IC decision is the gated action)
- org_id: {org}
- ic_meeting_date: 2026-04-22
- fund_id: Fund III

## Expected packs loaded

- `workflows/investment_committee_prep/`
- `workflows/pipeline_review/` (cross-link — debt variance, retrade screen)
- `workflows/pre_close_deal_tracking/` (cross-link — closing-week deals with open IC conditions)
- `workflows/owner_approval_routing/` (for condition-extension or waiver requests)
- `skills/sensitivity_stress_test/` (sensitivity batteries per deal)

## Expected references

- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml`
- `reference/connectors/deal_pipeline/schema.yaml`
- `reference/connectors/master_data/asset_crosswalk.yaml`
- `reference/connectors/master_data/market_crosswalk.yaml`
- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/rent_comp_evidence__charlotte_mf.csv`
- `reference/normalized/rent_comp_evidence__atlanta_mf.csv`
- `reference/normalized/rent_comp_evidence__phoenix_mf.csv`
- `reference/normalized/sale_comp_evidence__charlotte_mf.csv`
- `reference/normalized/sale_comp_evidence__atlanta_mf.csv`

## DQ gate outcome

- `dp_freshness_deals`: pass (feed landed 2026-04-15 17:32Z, within latency).
- `dp_completeness_ic_record`: pass — all `ic_approved` carry `ic_decision_date`.
- `dp_conformance_stage_enum`: pass.
- `dp_completeness_required_fields`: pass.
- `dp_handoff_lag`: warn — 1 closed-deal with 4-day lag (not on this docket; surfaced in banner).
- `dp_renamed_after_approval`: info — none this cycle.

## Docket summary

| # | deal_id | deal_name | deal_type | Market | Strategy | Memo validated | Prior conditions | Sensitivity | Comp freshness |
|---|---|---|---|---|---|---|---|---|---|
| 1 | DP_DEAL_022 | Oakwood Park | acquisition | Charlotte | core_plus | yes | 1 open (LP consent) | pass | within band |
| 2 | DP_DEAL_024 | Grand Marquee | acquisition | Atlanta | value_add | yes | none | pass | within band |
| 3 | DP_DEAL_031 | Arcadia Tower | acquisition | Phoenix | core | yes | 1 open (insurance confirm) | pass | within band (2d to stale) |
| 4 | DP_DEAL_029 | Lakeside Ridge | development | Atlanta | development | yes | none | pass | n/a (dev) |

- `ic_docket_load_count` (proposed) = **4** (within overlay capacity band of 5).
- Quorum check: pass (5 of 7 IC members confirmed available).
- Distribution list: per overlay; packet tagged `draft_for_review`.

## Condition-tracking rollup (carried forward from prior cycles)

| deal_id | Condition | Responsible | `resolution_deadline` | Status | Aging (days) |
|---|---|---|---|---|---|
| DP_DEAL_022 | LP consent on side-letter | asset_management_director | 2026-04-20 | open | 12 |
| DP_DEAL_019 | Roof-scope bid confirmation (also in `pre_close_deal_tracking`) | asset_management_director | 2026-04-20 | open | 19 |
| DP_DEAL_031 | Insurance program confirmation (prior cycle) | reporting_finance_ops_lead | 2026-04-25 | open | 8 |

- `ic_condition_completion_rate` (proposed) = **0.70** (trailing 2 cycles).
- `ic_condition_aging_days` (proposed): median 12 days; max 19 days; none past deadline this run.
- No extension / waiver ApprovalRequest opened this cycle.

## Sensitivity test posture

| deal_id | Cap-rate shift | Rent-growth haircut | Expense-inflation | Vacancy stress | Rate shift | Exit-cap sensitivity | Overall |
|---|---|---|---|---|---|---|---|
| DP_DEAL_022 | pass | pass | pass | pass | pass | pass | pass |
| DP_DEAL_024 | pass | pass | pass | pass | pass | pass | pass |
| DP_DEAL_031 | pass | pass | pass | pass | pass | pass | pass |
| DP_DEAL_029 | pass | pass | pass | n/a (dev) | pass | pass | pass |

- `sensitivity_test_pass_rate` (proposed) = **1.00**.
- No material failure flagged.

## Comp evidence scorecard

| deal_id | Rent comps used | Sale comps used | Freshest comp (days) | Oldest comp (days) | Flag |
|---|---|---|---|---|---|
| DP_DEAL_022 | 6 | 4 | 11 | 58 | within |
| DP_DEAL_024 | 5 | 3 | 17 | 62 | within |
| DP_DEAL_031 | 5 | 4 | 22 | 88 | 2 days to stale |
| DP_DEAL_029 | 8 (sub/projection) | n/a | 14 | 73 | within |

- `comp_evidence_freshness_days` (proposed): median 16 days; DP_DEAL_031 approaches overlay stale threshold.

## Debt term sheet cross-link

| deal_id | Indicated coupon | UW assumption | Variance (bps) | Flag (from pipeline_review) |
|---|---|---|---|---|
| DP_DEAL_009 (not on docket — info) | 6.55% | 6.00% | +55 | outside band |
| DP_DEAL_022 | 6.15% | 6.00% | +15 | within band |
| DP_DEAL_024 | 6.25% | 6.10% | +15 | within band |
| DP_DEAL_031 | 6.00% | 5.95% | +5 | within band |
| DP_DEAL_029 | 7.20% (constr) | 7.00% | +20 | within band |

## LP capital coverage

| Fund | LP-available capital | Docket-weighted required capital | `lp_capital_coverage_ratio` (proposed) | Flag |
|---|---|---|---|---|
| Fund III | $180.0MM | $140.5MM | 1.28 | within band |

- No capital shortfall on this docket.
- Overlay threshold: 1.10x minimum.

## Gates potentially triggered

- Condition extensions / waivers: none this cycle.
- Retrade flag from `pipeline_review`: none on this docket.
- Debt variance > overlay threshold: DP_DEAL_009 (not on this docket; surfaced in cross-link).
- `workflows/owner_approval_routing` called only for post-IC condition-extension or waiver requests after the meeting.

## Minute-ready condition-log draft (per deal template)

```
deal_id: <id>
deal_name: <name>
ic_decision: <approved | approved_with_conditions | deferred | declined | withdrawn>
decision_date: 2026-04-22
conditions:
  - condition_text: ""
    responsible_party: ""
    resolution_deadline: ""
    approval_request_ref: ""   # populated if extension / waiver needed
minute_reference: ""            # IC secretary fills post-meeting
```

## Post-IC narrative memo (abridged placeholder)

> Four-deal docket with a balanced mix (3 middle-market acquisitions, 1 luxury high-rise development). Memos validated against the template; sensitivity battery passes on every deal. Three prior-cycle conditions remain open with aging within band. LP capital coverage on Fund III sits at 1.28x against a 1.10x overlay threshold — sufficient headroom. The Arcadia Tower (DP_DEAL_031) rent-comp set is two days from the overlay stale threshold; the investments_lead may request a comp refresh before the meeting. Debt variance is contained: DP_DEAL_009's +55 bps indication is surfaced for IC awareness but is not a docket deal.

## Confidence banner

```
References:
- dealpath_deal_pipeline@2026-04-15 (sample)
- deal_pipeline/schema.yaml@0.1.0
- asset_crosswalk@2026-04-15 (sample)
- market_crosswalk@2026-04-15 (sample)
- role_kpi_targets@2026-03-31 (starter)
- approval_threshold_defaults@2026-03-31 (starter)
- rent_comp_evidence__{market}_mf@2026-03-31 to 2026-04-04 (starter; DP_DEAL_031 approaches staleness)
- sale_comp_evidence__{market}_mf@2026-03-31 (starter)
DQ: all blockers pass; 1 warn (dp_handoff_lag — not on docket); no info items above threshold.
Metrics: all metric slugs proposed (not yet in _core/metrics.md).
Canonical extensions required: Deal, DealMilestone, InvestmentCommitteeReview
(tracked under deal_pipeline wave-4 extension).
Distribution: draft_for_review; IC-member roster per overlay.
```
