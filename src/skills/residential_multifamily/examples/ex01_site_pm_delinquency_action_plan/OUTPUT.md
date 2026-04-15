# Example 01 — OUTPUT

## Delinquency Action Plan — Ashford Park

**Property.** Ashford Park (ashford_park_charlotte_01) — Charlotte / South End
**Week ending.** 2026-04-12
**Prepared by.** Property Manager (routed through `roles/property_manager` + `workflows/delinquency_collections`)
**Segment / form / stage / mode.** middle_market / garden / stabilized / third_party_managed

## Confidence banner

- Delinquency playbook reference as-of: 2026-03-15 (status: starter)
- Collections benchmark (southeast_mf) as-of: 2026-03-31 (status: sample)
- Approval threshold defaults as-of: 2026-03-15 (status: starter)
- Org overlay approval matrix as-of: 2026-04-01 (status: approved)
- Market rents (Charlotte) as-of: 2026-03-31 (status: sample)

Interpretation: starter / sample references are the operating fact only inside this demonstration. Operator overlay overrides are expected before this plan is executed in a live environment.

## Headline

- `delinquency_rate_30plus`: 6.8% (prior week 6.4%, trend up). Target band (middle-market) per `role_kpi_targets.csv` — subject property is above band.
- 21 residents in the 30+ bucket, ~$62,400 open balance above 30 days.
- Payment plans: 4 active, 1 in breach.

## Aging-bucket movement (this week vs. prior)

| Bucket | Units prior | Units this week | $ open | Movement |
|---|---|---|---|---|
| 1-7 | 6 | 5 | ~$9,200 | Improved |
| 8-30 | 10 | 12 | ~$22,700 | Worsened (2 crossed from 1-7) |
| 31-60 | 14 | 16 | ~$41,900 | Worsened (2 crossed from 8-30) |
| 61-90 | 4 | 4 | ~$13,100 | Flat |
| 90+ | 1 | 1 | ~$7,400 | Flat |

Primary drivers: 2 residents moving 8-30 -> 31-60 drove the headline; neither on a plan. One on a plan is in breach.

## Stage-by-stage playbook (middle-market, per overlay reference)

| Stage | Residents in stage | Action this week | Owner | Approval gate |
|---|---|---|---|---|
| Day 1-5: reminder + ledger validate | 5 | Portal reminder; verify ledger accuracy; confirm auto-pay status | PM / APM | none |
| Day 6-15: plan offer + PM review | 12 | Offer standard plan; PM review call where applicable; assemble pay-or-quit package for those past Day 15 | PM | pay-or-quit package is `draft_for_review` pending row 1 approval |
| Day 16+: eviction-track review | 16 | Counsel pre-read; package for regional + AM; no autonomous filing | PM -> Regional -> AM -> legal | row 2 eviction_filing |

## Draft resident communications (NOT sent)

- `portal_delinquency_draft_for_review.md` — one instance per resident in Day 1-15; LEGAL REVIEW REQUIRED BEFORE SEND banner preserved.
- Pay-or-quit package (pre-read only) — assembled for 12 residents past Day 15; does NOT leave the system until row 1 approval is recorded.

## Non-standard payment plan requests (row 13)

- 2 residents requested a non-standard plan (extended term; partial reinstatement of fees). Both routed via `owner_approval_routing_checklist.md`. Approver chain resolved from org overlay: PM -> Regional -> AM (owner rep).

## Escalations opened this week

- To Regional: aging-bucket worsening + 2 non-standard plan requests.
- To AM (owner rep): pay-or-quit package assembled for 12 residents (awaiting row 1 approval).
- To TPM: payment-plan-in-breach resident for re-engagement call within 48h.
- To legal counsel (not yet — will engage post row-1 approval for those past Day 15).

## Action items

| # | Action | Owner | Due | Approval gate | Confidence |
|---|---|---|---|---|---|
| 1 | Send portal reminder to Day 1-5 residents | PM | 2026-04-14 | none | high |
| 2 | Hold PM review calls with Day 6-15 residents | PM | 2026-04-16 | none | high |
| 3 | Complete payment-plan-in-breach re-engagement call | TPM -> PM | 2026-04-15 | none | high |
| 4 | Finalize pay-or-quit pre-read package for Day 16+ residents | PM | 2026-04-16 | row 1 pending | high |
| 5 | Submit non-standard plan request for 2 residents | PM -> Regional -> AM | 2026-04-18 | row 13 pending | medium |
| 6 | Assemble counsel pre-read for Day 61+ (5 residents) | PM -> Regional | 2026-04-17 | row 2 pending | medium |

## Gates surfaced / approval requests

- Row 1 `legal_notice`: 1 approval request opened covering 12 residents (consolidated).
- Row 2 `eviction_filing`: 1 approval request opened covering 5 residents (consolidated).
- Row 13 `non_standard_payment_plan`: 2 approval requests opened (one per resident).
- Row 3 `fair_housing_flag`: no flags raised in this batch.

## Next-week watch

- Four residents projected to cross 30+ next week without intervention. Prioritize in PM review calls this week.
- Collections benchmark comparison (sample reference) indicates portfolio-level delinquency > benchmark by ~1.3 pts; suggest surfacing to AM for watchlist review if not already.

---

*Output status: starter. No resident-facing communication was sent. All gated actions are queued as approval requests; execution awaits human approval per approval matrix.*
