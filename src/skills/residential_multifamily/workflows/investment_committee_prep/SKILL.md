---
name: Investment Committee Prep
slug: investment_committee_prep
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  IC cadence, docket capacity bands, memo-template sections, condition-tracking
  deadlines, sensitivity-test materiality bands, and comp-evidence freshness
  policy are all overlay-driven. The IC-member roster and LP capital-availability
  posture drift cycle-to-cycle; IC-condition deadlines are per-deal and drift
  with any approved extension. Rent-comp and sale-comp reference inventories
  refresh on reference-library cadence; stale comps surface through confidence
  banner.
applies_to:
  segment: [middle_market, luxury, affordable]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [development, construction, lease_up, stabilized, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [investments_lead, asset_management_director, executive, ic_members]
  output_types: [memo, kpi_review, dashboard, checklist]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml
    - reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml
    - reference/connectors/deal_pipeline/schema.yaml
    - reference/connectors/master_data/asset_crosswalk.yaml
    - reference/connectors/master_data/market_crosswalk.yaml
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/approval_threshold_defaults.csv
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/rent_comp_evidence__{market}_mf.csv
    - reference/normalized/sale_comp_evidence__{market}_mf.csv
  writes: []
metrics_used:
  - ic_approval_rate                 # proposed: true
  - ic_deferral_rate                 # proposed: true
  - ic_decline_rate                  # proposed: true
  - ic_condition_completion_rate     # proposed: true
  - ic_condition_aging_days          # proposed: true
  - ic_docket_load_count             # proposed: true
  - sensitivity_test_pass_rate       # proposed: true
  - comp_evidence_freshness_days     # proposed: true
  - lp_capital_coverage_ratio        # proposed: true
  - ic_cycle_time_days               # proposed: true
escalation_paths:
  - kind: ic_condition_past_deadline
    to: deal_team_lead -> investments_lead -> asset_management_director -> approval_request(row per matrix)
  - kind: sensitivity_test_material_failure
    to: investments_lead -> executive
  - kind: comp_evidence_stale_beyond_policy
    to: investments_lead -> data_platform_team
  - kind: lp_capital_shortfall
    to: investments_lead -> cfo_finance_leader -> executive
  - kind: dq_blocker_from_dealpath
    to: data_platform_team -> investments_lead; affected deals paused from docket
approvals_required:
  - ic_committee_approval
description: |
  Pre-IC packet assembly for each IC cycle. Assembles the docket, pulls each
  deal's memo and cross-references, tracks IC conditions from prior decisions
  through to completion, consumes the sensitivity / stress-test output,
  surfaces comp evidence with freshness flags, and runs an LP capital
  availability check. The pack is the IC committee's input; the committee
  owns the decision. The workflow refuses to publish a deal's packet if
  blocking Dealpath DQ rules are open (`dp_completeness_ic_record`) or if
  required sensitivity tests are missing. Outputs include the IC packet,
  the condition-tracking rollup (from prior cycles), and the post-IC
  condition-log draft ready for minute-keeping.
---

# Investment Committee Prep

## Workflow purpose

Deliver a clean, auditable IC packet that lets the committee make the decision. Compose the docket, cross-reference each deal memo, track conditions from prior decisions to closure, verify the sensitivity / stress-test battery ran and published, surface comp evidence with freshness flags, and confirm LP capital availability against the capital call required for approvals on this docket. The workflow does not make the IC decision; it assembles the input and records the minute-ready artifact.

## Trigger conditions

- **Explicit:** "prep the IC packet", "IC agenda for next cycle", "draft the IC memo cross-references", "condition-tracking rollup", "sensitivity posture for tomorrow's IC".
- **Implicit:** an IC meeting is within overlay-defined prep window (typically 5-10 business days); any deal enters `ic_review` in Dealpath; `workflows/pipeline_review` flags an IC-load approaching capacity band; an IC condition deadline approaches within overlay band; a sensitivity test is requested by the investments_lead.
- **Recurring:** bi-weekly per the overlay IC cadence, or event-driven per IC meeting. Condition-tracking sweep runs daily.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Dealpath normalized `deal` records | table | required | scope: deals at `ic_review`, `ic_approved`, or `under_dd` for pre-IC advisory |
| Dealpath normalized `deal_milestone` records | table | required | covers prior IC decisions and condition history |
| Dealpath normalized `investment_committee_review` records | table | required | per-cycle IC review state |
| Canonical `asset` records | table | required | resolved via `master_data/asset_crosswalk.yaml` |
| Dealpath dq outcomes | table | required | `dq_rules.yaml` evaluation; `dp_completeness_ic_record` blocks any IC-approved roll-up |
| IC calendar + docket policy overlay | overlay | required | cadence, capacity band, prep window |
| IC memo templates (per deal_type / segment) | overlay | required | section set, required exhibits, governance sections |
| Sensitivity / stress-test outputs | records | required | from `skills/sensitivity_stress_test` — if absent, the deal is blocked from the docket |
| Rent-comp evidence | reference | required | `rent_comp_evidence__{market}_mf.csv`; freshness checked against overlay policy |
| Sale-comp evidence | reference | optional | `sale_comp_evidence__{market}_mf.csv`; optional for recap / refi |
| LP capital availability snapshot | record | required | for docket capital-call coverage; feeds `lp_capital_coverage_ratio` |
| Debt term sheet state | record | optional | from `workflows/pipeline_review` debt variance scan |
| Prior-cycle IC conditions (open) | table | required | carries forward open conditions from prior decisions |
| IC-member roster | overlay | required | voting-member list per overlay; used for quorum and distribution |

## Outputs

| Output | Type | Shape |
|---|---|---|
| IC packet (per deal on docket) | `memo` | full memo with cross-references, exhibits pointer, sensitivity results, comp evidence |
| Docket summary | `dashboard` | deals on docket, capacity band, required reads, quorum check |
| Condition-tracking rollup | `checklist` | open conditions from prior IC cycles with responsible party, evidence required, deadline, status |
| Sensitivity test posture | `kpi_review` | per-deal pass/fail on overlay-defined sensitivity battery |
| Comp evidence scorecard | `kpi_review` | per-deal rent-comp set freshness + adequacy score |
| LP capital coverage | `kpi_review` | docket capital call vs. LP-available capital; `lp_capital_coverage_ratio` |
| Approval packet (for ApprovalRequest row per matrix) | bundle | routed via `workflows/owner_approval_routing` |
| Minute-ready condition-log draft | `checklist` | post-decision template for the IC secretary |
| Confidence banner | banner | adapter `as_of_date`, DQ outcomes, overlay `status` tags, comp freshness |

## Required context

`asset_class=residential_multifamily`. Scope: one IC cycle, either by declared `ic_meeting_date` or by `next_ic` per overlay. Per-deal grain requires `deal_id` (or all deals at `ic_review` within prep window). `org_id` required for IC-member roster and approval-threshold bands. `market` is deal-level; the pack handles multi-market dockets. `fund_id` required if LP-capital check is scoped by fund (most cycles).

## Process

1. **Freshness + DQ gate.** Evaluate Dealpath `dq_rules.yaml`. `dp_freshness_deals` blocker halts the run for affected deals. `dp_completeness_ic_record` blocker refuses to publish any IC-approved roll-up until every `ic_approved` deal carries an `ic_decision_date`. `dp_conformance_stage_enum` blocker halts stage-based filters.
2. **Scope.** Resolve the IC cycle: named `ic_meeting_date`, or `next_ic` per overlay. Pull all deals at `ic_review`; optionally include `under_dd` deals flagged for pre-IC advisory per overlay policy.
3. **Docket composition.** Compose the docket with each deal's canonical identity (via `asset_crosswalk`), deal_type, market, target capital, strategy tag. Compare `ic_docket_load_count` to overlay capacity band.
4. **Memo cross-reference.** For each deal, pull the memo artifact from Dealpath (or memo location per overlay). Validate against the IC memo template overlay (per `deal_type`, `segment`): every required section present, every required exhibit pointer resolvable. Missing sections surface as `packet_incomplete` — deal held back from publication until resolved.
5. **Prior-cycle IC condition tracking.** For every deal carrying `ic_approved_with_conditions` status in `investment_committee_review`, pull open conditions and their `resolution_deadline`. Compute `ic_condition_aging_days` and `ic_condition_completion_rate`. Any condition past deadline escalates per approval matrix; the workflow opens an `ApprovalRequest` for extension or waiver if requested.
6. **Sensitivity / stress-test confirmation.** For each deal on docket, verify the sensitivity output from `skills/sensitivity_stress_test` exists and covers the overlay-defined battery (cap-rate shift, rent-growth haircut, expense-inflation bump, vacancy stress, interest-rate shift, exit-cap sensitivity). Compute `sensitivity_test_pass_rate` and publish per-deal pass/fail. Missing tests hold the deal back.
7. **Comp evidence scan.** For each deal, read `rent_comp_evidence__{market}_mf.csv` (and `sale_comp_evidence` for acquisitions / recaps) and compute freshness vs. overlay policy. `comp_evidence_freshness_days` flag fires if any comp is older than overlay band. Stale comp evidence surfaces but does not block unless overlay marks it blocking for the deal type.
8. **Debt term sheet cross-link.** Consume debt variance state from `workflows/pipeline_review` for any deal at `under_financing`. Surface indicated-vs-UW coupon and advance-rate variance in the packet.
9. **LP capital availability.** Read LP capital snapshot for each fund in scope. Compute `lp_capital_coverage_ratio` = LP-available capital / docket-weighted required capital. Flag if coverage < overlay threshold; escalate to cfo_finance_leader.
10. **Quorum + distribution check.** Verify IC-member roster and quorum threshold met; prepare distribution list per overlay (encrypted at rest, share policy per overlay).
11. **Compose IC packet.** Per deal: memo + sensitivity + comp evidence + debt variance (if any) + conditions-brought-forward + capital-call coverage. Top-of-packet summary: docket + condition rollup + LP coverage + DQ outcomes.
12. **Draft post-IC condition log.** Minute-ready template for the IC secretary: decision field (approved / approved_with_conditions / deferred / declined / withdrawn), condition text, responsible party, `resolution_deadline`, approval_request pointer.
13. **Route through approval.** The IC packet itself is not an approval artifact; the IC decision is. However, the workflow does route the packet through `workflows/owner_approval_routing` for committee-visibility logging and audit, citing `decision_severity=action_requires_approval` (the IC decision is the gated action).
14. **Confidence banner.** Adapter `as_of_date`, DQ outcomes, overlay `status`, comp freshness, any fallback behavior invoked.

## Metrics used

See frontmatter `metrics_used`. All metric slugs for this workflow are proposed (`proposed: true`) — no IC-preparation metric has landed in `_core/metrics.md` yet. Every output carries the `proposed` flag on each metric.

## Reference files used

- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml`
- `reference/connectors/deal_pipeline/schema.yaml`
- `reference/connectors/master_data/asset_crosswalk.yaml`
- `reference/connectors/master_data/market_crosswalk.yaml`
- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/rent_comp_evidence__{market}_mf.csv`
- `reference/normalized/sale_comp_evidence__{market}_mf.csv`

## Escalation points

- IC condition past deadline: deal_team_lead -> investments_lead -> asset_management_director -> `approval_request` per matrix row.
- Sensitivity test material failure (any deal fails overlay-defined critical test): investments_lead -> executive.
- Comp evidence stale beyond policy (rent-comp set fresher than required for the deal type): investments_lead -> data_platform_team.
- LP capital shortfall on the docket: investments_lead -> cfo_finance_leader -> executive.
- DQ blocker from Dealpath (`dp_completeness_ic_record`, `dp_conformance_stage_enum`): data_platform_team -> investments_lead; affected deals paused from the docket.

## Required approvals

- `ic_committee_approval` is the committee's decision on each deal. The workflow is the input; the approval is the output of the IC meeting itself. Condition extensions and waivers open their own `ApprovalRequest` via `workflows/owner_approval_routing`.
- The packet itself carries `decision_severity=action_requires_approval` for audit purposes (the IC decision is the gated action); no action is taken by the workflow itself.

## Failure modes

1. Publishing a deal packet without its sensitivity / stress-test output. Fix: sensitivity confirmation is step 6; missing test holds the deal back.
2. Forgetting prior-cycle conditions when the deal returns to IC. Fix: condition tracking runs on every sweep; resurrected deals carry prior conditions forward explicitly.
3. Citing stale comp evidence without surfacing freshness. Fix: `comp_evidence_freshness_days` flag and banner required.
4. Over-committing capital on the docket beyond LP availability. Fix: `lp_capital_coverage_ratio` < overlay threshold escalates before publish.
5. Confusing `ic_approved` with `ic_approved_with_conditions` — not tracking conditions as still-open. Fix: separate status tracking in `investment_committee_review`; approved_with_conditions never treated as closed until conditions resolved.
6. Missing quorum flag. Fix: IC-member roster check is step 10; quorum failure surfaces before packet finalized.
7. Auto-routing IC packet outside approved distribution list. Fix: distribution list per overlay; workflow default is `draft_for_review`.
8. Publishing a memo where a required exhibit pointer doesn't resolve. Fix: template validation is step 4; unresolved exhibits block the deal's entry.
9. Treating DQ `dp_completeness_ic_record` blocker as a warning. Fix: blocker halts the affected IC-approved deal's appearance in any roll-up.

## Edge cases

- **Stalled deal resurfacing at IC after previous deferral:** prior-decision pointer (`deal_milestone.milestone_type=ic_deferred`) carried forward; conditions or questions from prior cycle surface at top of the packet.
- **Retrade in progress:** deal on docket has an open retrade flag from `workflows/pipeline_review` — packet includes the retrade summary and evidence pointer; IC may defer pending resolution.
- **Declined-then-resurrected deal:** prior IC decline (`milestone_type=ic_declined`) fetched and prominently cited; deal's re-presentation requires a "what changed" section per overlay policy.
- **Deal renamed after IC:** name change logged via `dp_renamed_after_approval`; packet uses canonical `deal_id` and surfaces prior-name alias.
- **Multi-asset deal / portfolio acquisition:** one `deal_id` to multiple canonical assets — memo cross-references each asset; sensitivity ran per asset; comp evidence per asset; capital-call coverage at deal level.
- **Cross-fund allocation:** deal split across funds — LP capital check per fund; capital call allocated per fund per overlay; approval decision tracked per fund where overlay requires.
- **Debt market shift mid-docket:** indicated coupon moved since memo draft — packet surfaces the latest indication vs. memo assumption; IC may defer for re-underwriting.
- **Partial closing path (equity closes before debt):** pre-IC if applicable — packet surfaces the capital-sequence plan and contingency.
- **Condition unresolved at resolution_deadline:** condition past deadline triggers approval request for extension or waiver; deal re-surfaces at next IC for condition review.
- **Late legal entity setup on prior-approved deal that has not yet closed:** surfaced under prior-condition tracking; escalated to asset_management_director.
- **Committee member on vacation / unavailable:** alternate per overlay; quorum re-checked; packet distribution list updated.
- **Conditional approval pending LP consent:** packet records `approved_with_conditions`; LP consent tracked as a prior-cycle condition on subsequent runs.
- **IC cancelled / rescheduled last-minute:** condition-tracking sweep still runs; packet regenerated on new date; prior-draft artifacts retained for audit.
- **Sensitivity battery changes mid-cycle:** deals on docket ran against prior battery — workflow flags, investments_lead decides whether to re-run before meeting.

## Example invocations

1. "Prep the IC packet for next Wednesday's meeting. Five deals expected; flag any condition past deadline."
2. "What IC conditions are open across the current book of approved-with-conditions deals? Group by deal_team_lead."
3. "Build the pre-read for tomorrow's IC. Sensitivity posture on every deal; LP capital coverage by fund."
4. "Draft the post-IC minute-ready condition log template for DP_DEAL_024. Approved with three conditions."
5. "Show the IC docket outlook for the next two cycles — what's coming through, capacity check, capital-need."

## Example outputs

See `examples/example_investment_committee_prep_output.md` for the full artifact shape.

### Output — IC packet summary (abridged)

**Cycle.** IC meeting 2026-04-22; prep window day -7.

**Docket.** 4 deals on docket + 1 pre-IC advisory. `ic_docket_load_count` = 4 (within overlay capacity band of 5).

**Memos.** 4 of 4 memos validated against the template (middle_market acquisition + luxury development variants).

**Conditions carried forward.** 3 open conditions across the current book.
- DP_DEAL_022: LP consent on side-letter — responsible asset_management_director, deadline 2026-04-20.
- DP_DEAL_019: Roof-scope bid confirmation — responsible asset_management_director, deadline 2026-04-20 (also tracked by `pre_close_deal_tracking`).
- DP_DEAL_031: Insurance program confirmation (prior-cycle condition) — responsible reporting_finance_ops_lead, deadline 2026-04-25.

**Sensitivity posture.** 4 of 4 deals pass the overlay battery. `sensitivity_test_pass_rate` = 1.00.

**Comp evidence.** Fresh within band on 4 of 4 deals; one comp set (Charlotte luxury) is within 2 days of overlay stale threshold.

**LP capital coverage.** `lp_capital_coverage_ratio` = 1.28 (within band). No shortfall.

**Debt term sheet.** 1 deal (DP_DEAL_009) carries the variance flag from `workflows/pipeline_review` — packet includes latest-indication line.

**DQ outcomes.** All blockers pass. 1 warn (`dp_handoff_lag` on recently closed deal, not on docket). No deal paused.

**Minute-ready condition-log template.** Drafted for IC secretary.

**Confidence banner.** `dealpath_deal_pipeline@2026-04-15 (sample)`; `asset_crosswalk@2026-04-15 (sample)`; `market_crosswalk@2026-04-15 (sample)`; `rent_comp_evidence@2026-03-31 (starter)`; `role_kpi_targets@2026-03-31 (starter)`.
