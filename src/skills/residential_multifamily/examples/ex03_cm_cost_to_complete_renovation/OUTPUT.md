# Example 03 — OUTPUT

## Cost-to-Complete Memo — Greenbriar Value-Add

**Project.** Greenbriar Value-Add (greenbriar_value_add_01)
**Property.** Greenbriar — Phoenix / North Tempe
**Prepared by.** Construction Manager (`roles/construction_manager`) via `workflows/cost_to_complete_review` + `workflows/change_order_review`
**Draw upcoming.** 2026-04-18

## Confidence banner

- Material costs (west residential) as-of: 2026-03-31 (status: sample)
- Labor rates (Phoenix residential) as-of: 2026-03-31 (status: sample)
- Unit-turn cost library (middle-market) as-of: 2026-02-01 (status: starter)
- Capex line items (middle_market_value_add) as-of: 2026-02-01 (status: starter)
- Approval thresholds as-of: 2026-03-15 (status: starter)

Interpretation: starter / sample references are stand-ins; any decision that crosses a threshold will be re-checked against the org overlay's approved approval matrix before execution.

## Project snapshot

- Contract value at NTP: $3,180,000
- Approved COs YTD: $64,200
- Pending CO backlog (pre this review): $92,500
- Percent complete (cost-loaded / physical): 38% / 40%
- Contingency remaining: $221,600 (69.7% of original $318,000)
- `schedule_variance_days` vs. baseline: currently 0; flooring issue could slip critical path by ~7 days if unresolved by 2026-04-22

## Cost-to-complete (CTC)

| Category | ETC (pre flooring issue) | ETC delta (flooring) | ETC (post issue) |
|---|---|---|---|
| Contract remaining work | $1,971,600 | +$108,000 | $2,079,600 |
| Approved CO carry-over | — | — | — |
| Pending CO backlog | $92,500 | — | $92,500 |
| **Total CTC** | **$2,064,100** | **+$108,000** | **$2,172,100** |

## Flooring trade variance

- Original estimate (per `capex_line_items__middle_market_value_add.csv`, status: starter): $468,000 (LVP + stair treads for balance of in-place unit turns).
- GC buyout: $576,000.
- `trade_buyout_variance` (this trade): +$108,000 (+23.1%).
- Reference-implied unit-level floor cost (starter): consistent with ~$900 per turn for LVP + stair at value-add finish level; GC buyout implies ~$1,109 per turn — above reference by ~$209 per turn across the remaining ~90 turn-units.
- Root cause (GC narrative): regional LVP pricing moved post-bid; installer labor constrained.

## Contingency read

- Contingency remaining: $221,600.
- Flooring variance as % of original contract: 3.4%.
- `contingency_burn_rate` vs. % complete: pre-issue 30.3% / 40% = 0.76 (healthy, <1.0); post-issue 64.2% / 40% = 1.61 (elevated).

## Options

### Option A — Absorb in contingency (no CO)

- Cost: +$108,000 against contingency.
- Schedule: no slip.
- Risk: draws 35% of remaining contingency in one event. Leaves $113,600 for balance of project; well below the 10% contingency buffer the org overlay prefers.
- Approval gate: contingency-use is within CM authority until contingency remaining drops below the org overlay's "minimum-reserve" level — and this option crosses that level. Routes per approval matrix row 11 (major CO equivalent) in this org.

### Option B — Formal change order (major tier)

- Cost: +$108,000 booked to contract (contingency preserved).
- Schedule: no slip (processing already underway).
- Risk: increases `change_orders_pct_of_contract` to 5.4%; within allowable band per org overlay.
- Approval gate: row 11 `change_order_major`. Approver chain (resolved from org overlay): CM -> development_manager -> asset_manager -> COO.

### Option C — Rebid flooring scope for remaining turns

- Cost: uncertain; plausible $40-80k reduction vs. GC buyout if a competitive installer is available inside a 3-week window.
- Schedule: +7 to +14 days slip on critical path.
- Risk: schedule slip pushes stabilization; rebid process itself requires vendor qualification, insurance and license verification per guardrails.
- Approval gate: row 9 `award_or_rebid_contract` + row 11 `change_order_major` for the resulting new pricing (whether higher or lower than GC buyout — both require re-papering). Approver chain: CM -> development_manager -> asset_manager -> COO.

### Option D — Descope (pull stair treads from value-add package)

- Cost: reduces scope by ~$55,000; residual variance ~$53,000 covered via Option A or B.
- Schedule: no slip.
- Risk: reduces lease-up rent uplift; finish package divergence vs. comps; requires `finish_standards` override per segment overlay.
- Approval gate: row 11 + segment overlay finish-standard override (requires approver chain CM -> development_manager -> asset_manager; may also require portfolio_manager buy-in given lease-up pricing implication).

## Recommendation

Option B (formal CO) is the cleanest. It preserves contingency, documents the GC's pricing movement, and does not introduce schedule risk. Option C (rebid) is worth exploring only if the schedule can absorb 7-14 days of slip — current funnel forecast says it cannot. Option D's downstream lease-up risk outweighs the finish-package savings at this segment.

## Draw next week (2026-04-18)

- Does this draw include the flooring variance? No — the pending CO is not approved in time. Draw package reflects contract value + approved COs only.
- Retainage posture unchanged.
- `draw_cycle_time` target: <=14 days request-to-funding; prior draw was 12 days.

## Proposed actions

| # | Action | Owner | Due | Approval gate |
|---|---|---|---|---|
| 1 | Finalize CO review sheet for Option B | CM | 2026-04-15 | row 11 pending |
| 2 | Confirm flooring trade price lock w/ GC | CM -> GC | 2026-04-16 | none |
| 3 | Explore rebid feasibility (quick read on vendor availability + schedule impact) | CM | 2026-04-17 | none (info-gather only) |
| 4 | Decision meeting with dev_manager + AM | CM | 2026-04-18 | none |
| 5 | If Option B approved: update CO log + contract exhibit | CM | 2026-04-21 | row 11 approved |
| 6 | If Option C selected: run `vendor_bid_leveling_template.md` | CM -> estimator | 2026-04-22 | row 9 pending |

## Confidence

Medium-high on CTC mechanics and contingency read. Medium on rebid feasibility (depends on vendor availability — no live quote yet). Price-reference inputs carry `sample` / `starter` tags; decision tightening requires operator-approved references post tailoring.

---

*Output status: starter. No CO has been approved or executed. Every gated action remains open as an approval request.*
