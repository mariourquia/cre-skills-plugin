---
name: Pre-Close Deal Tracking
slug: pre_close_deal_tracking
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Closing-checklist templates, lender-deliverable standards, escrow-agent SLAs,
  and tax-lookback-day rules are overlay-driven and jurisdiction-sensitive.
  Key-date definitions and extension policies vary per deal (PSA-specific).
  Overlay status tags (`starter`, `sample`, `approved`) must be surfaced with
  every closing-week call.
applies_to:
  segment: [middle_market, luxury, affordable]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [development, construction, lease_up, stabilized, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [investments_lead, deal_team_lead, asset_management_director, executive]
  output_types: [checklist, kpi_review, memo, email_draft]
  decision_severity_max: recommendation
references:
  reads:
    - reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml
    - reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml
    - reference/connectors/deal_pipeline/schema.yaml
    - reference/connectors/master_data/asset_crosswalk.yaml
    - reference/normalized/approval_threshold_defaults.csv
    - reference/normalized/close_calendar__portfolio.csv
  writes: []
metrics_used:
  - key_date_breach_count            # proposed: true
  - key_date_days_remaining          # proposed: true
  - closing_certainty_score          # proposed: true
  - open_contingency_count           # proposed: true
  - lender_deliverable_status_score  # proposed: true
  - escrow_funding_status            # proposed: true
  - pre_close_cycle_time             # proposed: true
  - days_to_close                    # proposed: true
escalation_paths:
  - kind: key_date_breach_imminent
    to: deal_team_lead -> investments_lead
  - kind: open_contingency_past_deadline
    to: deal_team_lead -> investments_lead -> asset_management_director
  - kind: lender_deliverable_blocker
    to: deal_team_lead -> investments_lead -> finance_systems_team
  - kind: retrade_or_price_change_request
    to: deal_team_lead -> investments_lead -> executive
approvals_required: []
description: |
  Per-deal closing discipline. Tracks PSA / financing key-date countdown
  (LOI expiry, PSA expiry, DD period end, financing contingency, close
  target, tax lookback), open contingencies and their evidence of removal,
  escrow funding status, and lender deliverable status. Produces a weekly
  running scorecard per deal (daily for closing-week deals), triggers
  escalations as key dates approach, and composes a closing-week dashboard
  covering every deal within the close_window_days overlay band.
---

# Pre-Close Deal Tracking

## Workflow purpose

Keep every deal from PSA signature through funding on schedule: track the closing checklist row-by-row, show the key-date countdown, catch contingency removal evidence gaps before they become escrow delays, and escalate when lender deliverables are at risk. The workflow does not execute closing actions — the deal team does. Its job is to surface the countdown and the gaps consistently so the human decisions are timely.

## Trigger conditions

- **Explicit:** "closing checklist for DP_DEAL_019", "daily close tracking for next week's closes", "what's open on this deal", "key-date countdown".
- **Implicit:** deal enters `under_psa`, `under_dd`, `under_financing`, or `pre_close` in Dealpath; a `deal_key_date` approaches within the overlay alert band (e.g., DD-period-end within 5 days).
- **Recurring:** weekly for all deals past `under_psa`; daily for deals within the overlay-defined closing window (typically 5-10 business days before `expected_close_date`).

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Dealpath normalized `deal` records | table | required | canonical shape from `normalized_contract.yaml` |
| Dealpath normalized `deal_key_date` records | table | required | LOI expiry, PSA expiry, DD period end, financing contingency, close target, tax lookback |
| Dealpath normalized `deal_milestone` records | table | required | closing-checklist milestones and contingency-removal evidence linkage |
| Closing-checklist template overlay | overlay | required | per-segment / per-deal-type rows; overlay carries `as_of_date` |
| Lender deliverable schedule | overlay | optional | per-lender requirements; falls back to overlay default |
| Escrow agent contact / SLA | overlay | optional | per-jurisdiction default; overlay-tunable |
| Legal entity setup status | reference | optional | signals readiness for funding; falls back to `not_started` warning |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Per-deal closing dashboard | `kpi_review` | key dates, days remaining, status per row |
| Closing checklist with status | `checklist` | row, owner, due date, evidence, state (open / complete / waived / blocked) |
| Open-contingency list | `checklist` | contingency, evidence required, responsible party, deadline |
| Lender-deliverable scorecard | `kpi_review` | item, responsible, state, days to lender deadline |
| Escalation notices | `email_draft` | `draft_for_review`; to deal_team_lead / investments_lead when key date approaches |
| Closing-week dashboard | `kpi_review` | all deals within close_window_days; at-risk flags |
| Narrative memo (per deal) | `memo` | summary of what's open, what's cleared, next 72 hours |

## Required context

`asset_class=residential_multifamily`. Deal grain: either a single `deal_id` or a list of `deal_id`s within a portfolio or fund scope. `org_id` required for approval-threshold bands. Segment and form_factor used only for overlay selection (closing-checklist template varies by deal_type and segment). `jurisdiction` relevant for tax-lookback day count and legal-entity setup bands.

## Process

1. **Freshness + DQ gate.** Evaluate Dealpath `dq_rules.yaml`. `dp_freshness_deals` blocker halts the run for affected deals. Log `dp_handoff_lag` warnings for recently closed deals.
2. **Scope.** Resolve the deal list: either a named `deal_id`, all deals past `under_psa`, or all deals within the overlay-defined closing window.
3. **Key-date countdown.** For each deal, pull every `deal_key_date` row. Compute `key_date_days_remaining` per row. Flag any date within the overlay alert band (yellow) or past date without recorded achievement (red).
4. **Closing-checklist composition.** Load overlay-defined checklist template per deal type and segment. For each row, read Dealpath `deal_milestone` state; resolve to one of `open / complete / waived / blocked`. Attach evidence pointer when present; surface missing-evidence rows explicitly.
5. **Contingency tracking.** Enumerate open contingencies with their evidence requirement and responsible party. For each, flag if past its removal deadline or if evidence is missing.
6. **Escrow status.** Surface escrow account status (opened / funded / pending), earnest-money posted state, and any hold-back or reserve requirements. Defer to reference if the adapter does not carry it; surface the gap.
7. **Lender deliverable tracking.** For each item on the lender schedule, resolve state from milestones and `deal_document` references. Compute `lender_deliverable_status_score` (overlay-defined).
8. **Tax lookback + legal entity readiness.** Compute days remaining on tax lookback; flag legal entity setup status (warn if `not_started` past overlay band).
9. **Closing certainty.** Composite `closing_certainty_score` from open-contingency count, key-date countdown, lender deliverable score, and escrow status. Overlay-tunable weighting. Publish with `proposed: true`.
10. **Escalation.** If any key date breach is imminent, any open contingency is past deadline, or any lender deliverable is blocked, compose escalation draft (`email_draft`, `draft_for_review`) to deal_team_lead and investments_lead.
11. **Price change / retrade screen.** If Dealpath records show a requested price adjustment, extension, or seller concession request, open a retrade line item and cross-link to `workflows/pipeline_review/` retrade list.
12. **Compose per-deal memo.** Three sections: (a) state of play, (b) what's open in the next 72 hours, (c) escalations sent / pending. Every claim cites a metric slug or evidence reference.
13. **Closing-week dashboard.** Roll all deals in `close_window_days` into one view; at-risk flags per deal; capital-funding sequence noted.
14. **Confidence banner.** Adapter `as_of_date`, overlay `status`, dq outcomes, any fallback behavior invoked.

## Metrics used

See frontmatter `metrics_used`. All metric slugs for this workflow are proposed (`proposed: true`) — no pre-close metric has landed in `_core/metrics.md` yet. Every output carries the `proposed` flag on each metric.

## Reference files used

- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml`
- `reference/connectors/deal_pipeline/schema.yaml`
- `reference/connectors/master_data/asset_crosswalk.yaml`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/close_calendar__portfolio.csv`

## Escalation points

- Key-date breach imminent (within overlay alert band): deal_team_lead -> investments_lead.
- Open contingency past deadline: deal_team_lead -> investments_lead -> asset_management_director.
- Lender deliverable blocked: deal_team_lead -> investments_lead -> finance_systems_team.
- Retrade / price-change request surfaced: deal_team_lead -> investments_lead -> executive.
- DQ blocker from Dealpath: data_platform_team -> investments_lead; affected deals paused.

## Required approvals

None for the tracking pack itself. Any closing-week action (PSA extension, deposit release, price adjustment, contingency waiver) opens its own `ApprovalRequest` via the originating workflow — this pack surfaces the gap but does not execute.

## Failure modes

1. Marking a checklist row complete without evidence pointer. Fix: evidence required or row stays `open`.
2. Using a closing-checklist template that does not match the deal type. Fix: overlay selection checks `deal_type` and `segment`; mismatch refused.
3. Reporting `days_to_close` without surfacing imminent key-date breach. Fix: imminent breaches flagged before overall countdown is published.
4. Silently defaulting escrow status when reference is absent. Fix: absent state surfaces as `unknown` with warning, not a clean status.
5. Composing an escalation draft without `draft_for_review` tag. Fix: every email output carries `draft_for_review` until overlay permits auto-send.
6. Claiming funding on partial closing (equity closed but debt pending). Fix: funding claimed only when both tranches record; split state reported explicitly.
7. Surfacing contingency as `waived` without policy reference. Fix: waiver requires overlay policy reference and approval_request link.

## Edge cases

- **Stalled deal (post-PSA, no DD progress):** deal shows extended days in `under_dd` — flagged with owner and last activity; escalation draft composed.
- **Retrade request:** seller or buyer requests price adjustment after PSA — surfaced on retrade list with evidence pointer; cross-link to pipeline_review retrade screen.
- **Declined-then-resurrected deal:** deal previously dropped that returns to active — key-date countdown restarts from new LOI; prior-decision pointer retained.
- **Deal renamed after IC:** name change logged via `dp_renamed_after_approval`; closing checklist reads canonical `deal_id` regardless of display name.
- **Multi-asset deal (portfolio acquisition):** one deal, multiple target properties — closing checklist enumerates per-asset contingencies (title, survey, PCR, Phase I) while keeping single financing key dates.
- **Cross-fund allocation:** deal split across funds — capital sequence noted per fund; per-fund funding state tracked.
- **Debt market shift mid-close:** lender indicates term adjustment inside closing window — surface immediately; cross-link to pipeline_review debt variance and escalate.
- **Partial closing:** equity closes before debt (or vice versa) — two positions recorded; closing_certainty_score reflects the partial state; no "closed" claim until both record.
- **Condition unresolved at close (ic_approved pending conditions):** open condition within `resolution_deadline` — if deadline lapses before close, escalate per approval_matrix; block `closed` transition until resolved.
- **Late legal entity setup:** legal_entity_id not populated post-close beyond overlay lag — flagged as `dp_handoff_lag` warning; cross-link to acquisition_handoff when that workflow exists.
- **Escrow holdback:** reserved funds post-close (repairs, compliance, litigation) — tracked as a separate line item with release trigger.

## Example invocations

1. "Build the closing checklist snapshot for DP_DEAL_019. What's open this week?"
2. "Daily close tracking for all deals closing next week. Flag at-risk deals."
3. "Key-date countdown for DP_DEAL_022. Where are we on lender deliverables?"
4. "What contingencies are still open on DP_DEAL_004 and who owns each?"
5. "Draft an escalation to the investments lead — DD period ends tomorrow on DP_DEAL_027 and the roof scope is unresolved."

## Example outputs

See `examples/example_pre_close_deal_tracking_output.md` for the full artifact shape.

### Output — Closing dashboard (abridged, DP_DEAL_019)

**Deal.** DP_DEAL_019 — 248-unit garden acquisition, Charlotte, expected close 2026-04-22.

**Key-date countdown.**
- LOI expiry: achieved 2026-02-10.
- PSA expiry: achieved 2026-03-05.
- DD period end: 2026-04-18 (3 business days remaining). Within alert band. Flag.
- Financing contingency: 2026-04-19 (4 business days remaining). Within alert band.
- Close target: 2026-04-22.
- Tax lookback: 2026-04-15 (today — compliant).

**Open contingencies.** 3.
- Title commitment review: evidence pending; responsible L. Garcia; deadline 2026-04-17.
- Survey acceptance: evidence received; pending legal sign-off.
- Phase I ESA: cleared; evidence on file.

**Lender deliverables.** 8 items; 6 complete, 2 pending (insurance binder, entity certificate of good standing). `lender_deliverable_status_score` = 0.75 (proposed). Within overlay band but trending tight.

**Escrow.** Earnest money posted; final deposit required by 2026-04-21.

**Closing certainty.** `closing_certainty_score` = 0.82 (proposed). On track conditional on title commitment review by 2026-04-17.

**Escalation.** Draft composed (`draft_for_review`) to deal_team_lead: title commitment review flag.

**Confidence banner.** `dealpath_deal_pipeline@2026-04-15 (sample)`, `close_calendar__portfolio@2026-03-31 (starter)`, `approval_threshold_defaults@2026-03-31 (starter)`.
