# Example 02 — OUTPUT

## Monthly Asset Management Memo — Liberty Apartments (March 2026)

**Property.** Liberty Apartments (liberty_apartments_nashville_01) — Nashville / The Gulch
**Period.** March 2026
**Prepared by.** Asset Manager (`roles/asset_manager`) via `workflows/monthly_asset_management_review`

## Confidence banner

- Market rents (Nashville) as-of: 2026-03-31 (status: sample)
- Concession benchmarks (Nashville) as-of: 2026-03-31 (status: sample)
- Collections benchmark (southeast_mf) as-of: 2026-03-31 (status: sample)
- TPM scorecard weights as-of: 2026-01-01 (status: starter)
- KPI targets source as-of: 2026-01-15 (status: starter)

Interpretation: starter / sample references stand in for operator-specific overrides pending org overlay completion.

## Headline

Liberty Apartments finished March behind budget on NOI (-6.8% MTD). The miss is primarily revenue-driven — occupancy and delinquency both ran below band. TPM variance commentary was incomplete; the scorecard reflects that. No watchlist change is recommended yet; one more month below band triggers formal add. No gated actions in this review.

## Plan-vs-actual snapshot

| Metric | Plan | Actual | Delta | Assessment |
|---|---|---|---|---|
| `physical_occupancy` (EOM) | plan band | 92.1% | below band | Driven by move-outs > move-ins in March; funnel backfill slipped |
| `economic_occupancy` MTD | plan band | 88.4% | below band | Combined vacancy + delinquency drag |
| `delinquency_rate_30plus` | plan band | 5.9% | above band | Two new residents aged into 30+ bucket without plan |
| `blended_lease_trade_out` MTD | plan band | +1.2% | below band | New-lease trade-out weaker vs. Nashville comps |
| `controllable_opex_per_unit` T12 | plan band | above plan by $31 per unit | above band | R&M run-rate higher; payroll largely on plan |
| `noi` MTD | plan | -6.8% | miss | Revenue-driven miss |

## TPM scorecard (weights from reference)

| Dimension | Score (1-5) | Weight | Weighted | Commentary |
|---|---|---|---|---|
| `report_timeliness` | 3 | 0.10 | 0.30 | Submitted on 2026-04-09 — 1 business day late |
| `kpi_completeness` | 3 | 0.15 | 0.45 | 85% complete; missing leasing-funnel and turn-pipeline tabs |
| `variance_explanation_completeness` | 2 | 0.15 | 0.30 | Revenue variance cited "market" without substantiating concessions vs. occupancy split |
| `budget_adherence` | 2 | 0.20 | 0.40 | Budget attainment below band for second consecutive month |
| `staffing_vacancy_rate_tpm` | 3 | 0.10 | 0.30 | One vacant leasing role open 28 days; within band but trending |
| `tpm_collections_performance` | 2 | 0.10 | 0.20 | 30+ bucket above band; playbook execution slow at Day 6-15 stage |
| `tpm_turn_performance` | 4 | 0.10 | 0.40 | `make_ready_days` within band; no material turn issues |
| `service_level_adherence` | 4 | 0.05 | 0.20 | Work-order SLAs within band |
| `approval_response_time_tpm` | 3 | 0.03 | 0.09 | Median 6 business days; target band tighter |
| `audit_issue_count_and_severity` | 4 | 0.02 | 0.08 | No S1/S2 issues open |

**Composite TPM score: 2.72 (prior month 3.10). Trend: down.**

## Observed gaps (from TPM audit issue log)

- S2: variance commentary incomplete. Corrective action: TPM to resubmit April-forward commentary per `variance_commentary_template.md` materiality framework; owner to require completeness before release.
- S3: KPI completeness below 100%. Corrective action: TPM to include leasing-funnel and turn-pipeline tabs as a standing requirement.
- S3: approval-response-time drift. Corrective action: TPM to adopt same-business-day acknowledgment plus target band per org overlay.

## Watchlist assessment

- Current status: not on watchlist.
- Drivers: second consecutive month of budget attainment below band + delinquency above band.
- Recommendation: monitor April. If April attainment remains below band OR delinquency does not recover, add to watchlist with quarterly recovery plan.

## Asset-plan reaffirmation

- Hold.
- No triggers for sell / refi yet; refi window still 8 months out.
- If April / May occupancy does not recover, reopen pricing strategy and staffing plan with TPM.

## Actions for next TPM meeting

1. Walk TPM through variance-commentary expectations; share `variance_commentary_template.md`.
2. Request revised March commentary by 2026-04-22.
3. Review delinquency playbook execution at Day 6-15 stage; identify why 2 residents aged without a plan offer.
4. Review leasing-funnel detail; confirm whether tour-conversion or mid-funnel attrition is driving occupancy miss.
5. Align on an April-forward scorecard target to exit watchlist risk.

## Decisions requested from IC

| # | Decision | Required by | Approval path |
|---|---|---|---|
| 1 | Ratify "watch but not watchlist" posture | 2026-04-21 IC | AM -> portfolio_manager |
| 2 | Approve TPM April corrective action plan (after TPM submission) | End of April | AM -> portfolio_manager -> COO for record |

---

*Output status: starter. This memo is internal IC-read; not tagged `final` to LPs or lender. A `final` external version would route per approval matrix.*
