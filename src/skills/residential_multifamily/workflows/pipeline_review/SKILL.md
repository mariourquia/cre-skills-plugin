---
name: Pipeline Review
slug: pipeline_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Pipeline state, stage probabilities, IC-prep load, and debt term sheet market
  conditions drift day to day. Deal-team ownership and attribution may change
  intra-week. Blocking dq issues from Dealpath (dp_completeness_ic_record,
  dp_handoff_lag) surface different deals each cycle. Target bands for
  velocity, stalled-deal thresholds, and retrade materiality are overlay-driven.
applies_to:
  segment: [middle_market, luxury, affordable]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [development, construction, lease_up, stabilized, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [investments_lead, asset_management_director, deal_team_lead, executive]
  output_types: [operating_review, kpi_review, dashboard, memo]
  decision_severity_max: recommendation
references:
  reads:
    - reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml
    - reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml
    - reference/connectors/deal_pipeline/schema.yaml
    - reference/connectors/master_data/asset_crosswalk.yaml
    - reference/connectors/master_data/market_crosswalk.yaml
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - pipeline_velocity_days           # proposed: true
  - stage_conversion_rate            # proposed: true
  - stalled_deal_count               # proposed: true
  - ic_prep_load_count               # proposed: true
  - debt_term_sheet_variance         # proposed: true
  - retrade_risk_count               # proposed: true
  - closing_certainty_score          # proposed: true
  - pipeline_weighted_capital_need   # proposed: true
escalation_paths:
  - kind: stalled_deal_threshold_breach
    to: deal_team_lead -> investments_lead -> asset_management_director
  - kind: debt_market_shift_material
    to: investments_lead -> executive
  - kind: dq_blocker_from_dealpath
    to: data_platform_team -> investments_lead
  - kind: pipeline_velocity_outside_band
    to: investments_lead -> executive
approvals_required: []
description: |
  Weekly review of every deal in the pipeline by stage (sourcing, loi_signed,
  psa_signed, ic_approved, debt_term_sheet, close, funded). Produces a
  stage-by-stage scorecard, flags stalled deals beyond the overlay-defined
  aging threshold, surfaces IC-prep load and debt-term-sheet variance, and
  quantifies retrade risk. Dealpath is the primary source; the workflow
  surfaces any `dp_completeness_ic_record` or `dp_handoff_lag` blocker from
  adapter dq rules before any roll-up claim is made.
---

# Pipeline Review

## Workflow purpose

Deliver a weekly pipeline scorecard that the investments lead, asset-management director, and executive can read in one sitting to answer: which deals advanced, which stalled, where is the capital-need concentration, what is the IC load next session, and which blocking data-quality issues from Dealpath need resolution before the roll-up can be trusted. The workflow composes stage-by-stage counts, dollar-weighted exposure, and stalled-deal aging into a single dashboard; it recommends no deal-level action — every action remains with the deal team.

## Trigger conditions

- **Explicit:** "weekly pipeline review", "pipeline scorecard", "pipeline dashboard for Monday", "where are we on IC load this cycle".
- **Implicit:** Dealpath adapter emits a pipeline-stage transition for 3+ deals in a week; week-close calendar event; IC calendar approaches within one cycle.
- **Recurring:** weekly, end-of-week close; also on-demand ahead of executive check-ins.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Dealpath normalized `deal` records | table | required | via `dealpath_deal_pipeline` adapter; canonical shape per `normalized_contract.yaml` |
| Dealpath normalized `deal_milestone` records | table | required | primary source; covers stage transitions |
| Dealpath normalized `deal_key_date` records | table | required | LOI expiry, PSA expiry, expected close, close target |
| Canonical `asset` records | table | required | resolved via `master_data/asset_crosswalk.yaml` |
| Dealpath dq outcomes | table | required | `dq_rules.yaml` evaluation; blockers surface before roll-up |
| Stalled-deal aging policy | overlay | required | overlay-defined per stage; overlay_id + `as_of_date` |
| Debt term sheet policy bands | overlay | optional | market-level coupon and advance-rate bands; falls back to `use_prior_period` |
| IC calendar | reference | optional | next IC meeting date; falls back to overlay default cadence |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Stage-by-stage scorecard | `kpi_review` | count + dollar-weighted exposure per stage |
| Stalled-deal list | `checklist` | deal_id, stage, days in stage, owner, next step, policy band |
| IC-prep load summary | `dashboard` | deals on-docket, deals expected, capacity band |
| Debt term sheet variance table | `kpi_review` | deal_id, indicated terms vs. UW, variance, flag |
| Retrade-risk flag list | `checklist` | deal_id, reason, evidence, proposed follow-up |
| Pipeline narrative memo | `memo` | stage changes this week, capital-need concentration, DQ blockers, open items |
| Confidence banner | banner | adapter `as_of_date`, dq outcomes, overlay `status` tags |

## Required context

`asset_class=residential_multifamily`, scope = portfolio (or a declared subset of assets / funds). Segment, form_factor, and lifecycle are not required at the deal grain but may be used to filter — the workflow defaults to all-segments roll-up if unspecified. `market` filter optional for market-scoped cuts. `org_id` required whenever approval-threshold bands or staffing bands are read.

## Process

1. **Freshness + DQ gate.** Load Dealpath adapter output; evaluate `dq_rules.yaml`. If `dp_completeness_ic_record` or `dp_freshness_deals` returns a blocker, surface it at the top of the pack; refuse to claim any stage roll-up that the blocker affects. Warn on `dp_handoff_lag`.
2. **Resolve canonical keys.** Join Dealpath `deal.asset_id` to canonical `asset_id` via `master_data/asset_crosswalk.yaml`. Resolve `market` via `market_crosswalk.yaml`. Flag any unresolved rows; exclude from roll-up and list in DQ appendix.
3. **Stage scorecard.** Bucket active deals by canonical pipeline stage (`sourcing`, `loi_signed`/`under_loi`, `psa_signed`/`under_psa`, `under_dd`, `ic_review`, `ic_approved`, `debt_term_sheet` / `under_financing`, `pre_close`, `close` / `closed`, `funded`). Compute count and dollar-weighted exposure (`deal.total_cost` or equivalent from Dealpath contract).
4. **Velocity.** For each stage transition seen this week, compute `pipeline_velocity_days` per deal and roll up the stage median. Compare against overlay band; color within / below / above.
5. **Stalled-deal scan.** For each active deal, compute days-in-current-stage. Compare against overlay-defined stalled threshold per stage. Flag; include owner, last touch, next step note from Dealpath.
6. **IC-prep load.** Count deals currently at `ic_review` or `ic_approved` pending final conditions; compare to overlay IC capacity band. Cross-link to `workflows/investment_committee_prep/` if next IC is within one cycle.
7. **Debt term sheet variance.** For deals at `debt_term_sheet` / `under_financing`, compare indicated terms (coupon, advance rate, DSCR test, covenant set) vs. last underwritten assumption. Compute `debt_term_sheet_variance`; flag deals outside overlay band.
8. **Retrade-risk screen.** Flag deals where any of the following hold: DD findings outside overlay tolerance, seller extension requested, market shift since LOI beyond overlay threshold, multi-party hesitation on recent key-date. List with evidence pointer. Cross-link to `workflows/pre_close_deal_tracking/` for closing-week deals.
9. **Capital-need concentration.** Roll equity and debt capital requirements up by stage-weighted probability; call out any single deal exceeding overlay concentration band.
10. **Compose narrative memo.** One paragraph per stage change category: advancing, stalled, debt-variance, retrade-risk, DQ-blocked. Cite every claim to a metric slug.
11. **Confidence banner.** List adapter `as_of_date`, DQ outcome status (pass / warn / blocker), overlay `status` tags (`starter`, `sample`, `approved`), and any references that fell back to prior period.

## Metrics used

See frontmatter `metrics_used`. All metric slugs for this workflow are proposed (`proposed: true`) — no deal-pipeline metric has landed in `_core/metrics.md` yet. The workflow surfaces computed values with the `proposed` flag on every output.

## Reference files used

- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml`
- `reference/connectors/deal_pipeline/schema.yaml`
- `reference/connectors/master_data/asset_crosswalk.yaml`
- `reference/connectors/master_data/market_crosswalk.yaml`
- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Stalled-deal aging breaches overlay threshold: deal_team_lead -> investments_lead -> asset_management_director.
- Debt market shift material (coupon spread or advance rate outside overlay band across multiple deals): investments_lead -> executive.
- DQ blocker from Dealpath adapter: data_platform_team -> investments_lead; roll-up paused for affected stages.
- Pipeline velocity outside band two consecutive cycles: investments_lead -> executive.

## Required approvals

None. The pack is informational / recommendation severity. Any deal-level action surfaced here is owned by the originating workflow (deal team, capital sourcing, IC prep), which carries its own approval gate.

## Failure modes

1. Rolling up deals without checking `dp_completeness_ic_record` first. Fix: DQ gate is step 1; blocker halts the affected roll-up.
2. Reporting stalled-deal counts without overlay-defined thresholds. Fix: overlay `as_of_date` and band cited; no thresholds hardcoded in prose.
3. Merging deal counts across canonical stages after informal stage renaming in Dealpath. Fix: `map_dealpath_stage` is the single mapping; unmapped stages flagged as DQ conformance blockers.
4. Double-counting deals in retrade-risk and stalled-deal lists. Fix: deals appearing on both lists are explicit; union reported with dedup.
5. Reporting capital-need concentration without stage-weighted probability. Fix: probability applied; un-probabilitized figures not published.
6. Missing adapter freshness check. Fix: `dp_freshness_deals` evaluated; stale feed surfaces banner and escalates.

## Edge cases

- **Stalled deal:** days-in-stage exceeds overlay threshold — listed with owner, last activity, next-step note, and escalation path. If stalled > 2x threshold, escalates to investments_lead.
- **Retrade in progress:** deal shows PSA executed + DD findings + price renegotiation signal — flagged on retrade list with evidence pointer; counted separately from stalled.
- **Declined-then-resurrected deal:** deal previously `dropped` or IC-declined that returns to active — surfaced with prior-decision pointer; treated as new stage entry for velocity purposes.
- **Deal renamed after IC:** name change post-`ic_approved` tracked via `dp_renamed_after_approval`; roll-up uses stable `deal_id`, surfaces prior name alias.
- **Multi-asset deal / portfolio acquisition:** one Dealpath `deal_id` mapping to multiple canonical assets via `property_master_crosswalk` (manual_override) — listed with all target assets; capital-need counted once at deal level, exposure breakdown per asset.
- **Cross-fund allocation:** deal tagged with multiple target funds — per-fund allocation carried through; concentration check applied per fund.
- **Debt market shift:** indicated coupon moves > overlay threshold week-over-week — flagged across affected deals; escalates to investments_lead.
- **Partial closing (equity closes before debt or vice versa):** shown as two stage positions; deal not claimed closed until both transitions recorded.
- **Condition unresolved at close:** ic_approved with open conditions whose deadline lapses — flagged, cross-linked to approval request, escalates per approval_matrix.
- **Late legal entity setup:** canonical `legal_entity_id` not populated post-close beyond overlay lag — surfaced as handoff warning (`dp_handoff_lag`); cross-linked to `workflows/acquisition_handoff/` once it exists.

## Example invocations

1. "Produce the weekly pipeline review for Monday. Flag anything stalled past our 14-day LOI threshold."
2. "Pipeline scorecard, portfolio-wide, as of Friday close. Highlight IC load for the next session and any debt variance."
3. "What's retrade risk on this quarter's pipeline? Evidence list, not opinions."
4. "Pipeline cut, Southeast markets only. Capital-need concentration by fund."
5. "Run the pipeline review with focus on deals sourced in the last 30 days versus the rest."

## Example outputs

See `examples/example_pipeline_review_output.md` for the full artifact shape.

### Output — Stage scorecard (abridged)

**Stages.** `sourcing` (12 deals), `under_loi` (5), `under_psa` (3), `under_dd` (4), `ic_review` (2), `ic_approved` (3), `under_financing` (2), `pre_close` (1), `closed` (1 this week).

**Velocity.** `pipeline_velocity_days` (stage median) within band for sourcing, under_loi; above band for under_dd (flagged).

**Stalled.** 2 deals past overlay threshold — DP_DEAL_014 (under_loi, 21 days) and DP_DEAL_027 (under_dd, 34 days). Owners + next-step notes listed.

**IC load.** 2 on docket next cycle; overlay capacity band = 3; within capacity.

**Debt variance.** 1 deal outside band — DP_DEAL_009 coupon indicated at +55bps over UW assumption.

**Retrade risk.** 1 flag — DP_DEAL_027 (DD finding on roof scope; seller extension requested).

**DQ banner.** `dp_freshness_deals`: pass. `dp_completeness_ic_record`: pass. `dp_handoff_lag`: warn (1 closed deal, 4 days lag). Adapter `as_of_date`: sample / starter.

**Confidence banner.** References: `dealpath_deal_pipeline@2026-04-14 (sample)`, `asset_crosswalk@2026-04-15 (sample)`, `role_kpi_targets@2026-03-31 (starter)`.
