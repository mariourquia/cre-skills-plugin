# Example — Pipeline Review (abridged)

**Prompt.** "Produce the weekly pipeline review for Monday. Flag anything stalled past our 14-day LOI threshold and summarize IC load for the next session."

**As-of.** Friday 2026-04-10 close; adapter `as_of_date=2026-04-10` (status=sample).

**Inputs.** Dealpath normalized deal pipeline + DQ outcomes + asset crosswalk + role KPI targets + overlay thresholds.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: portfolio roll-up (middle_market, luxury)
- lifecycle_stage: pre-close bias (development, stabilized)
- management_mode: n/a at deal grain
- role: investments_lead
- market: all
- output_type: dashboard + memo
- decision_severity: recommendation
- org_id: {org}

## Expected packs loaded

- `workflows/pipeline_review/`
- `workflows/investment_committee_prep/` (cross-linked; IC in 6 days)
- `workflows/pre_close_deal_tracking/` (cross-linked for 2 closing-week deals)

## Expected references

- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml`
- `reference/connectors/deal_pipeline/schema.yaml`
- `reference/connectors/master_data/asset_crosswalk.yaml`
- `reference/connectors/master_data/market_crosswalk.yaml`
- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## DQ gate outcome

- `dp_freshness_deals`: pass (feed landed 2026-04-10 18:14Z, within latency).
- `dp_completeness_required_fields`: pass.
- `dp_completeness_ic_record`: pass — all `ic_approved` deals carry `ic_decision_date`.
- `dp_handoff_lag`: warn — 1 closed deal (DP_DEAL_003) shows 4-day lag without property setup; within overlay tolerance band but surfaced.
- `dp_one_deal_multiple_projects`: info — DP_DEAL_004 (portfolio, 2 assets) flagged for manual map confirmation.

## Expected output shape

### Stage scorecard (counts, exposure in $MM weighted by stage probability)

| Stage | Count | Exposure ($MM) | Velocity (median days) | Velocity band |
|---|---|---|---|---|
| sourcing | 12 | 45.2 | 8 | within |
| under_loi | 5 | 87.5 | 11 | within |
| under_psa | 3 | 62.4 | 14 | within |
| under_dd | 4 | 78.1 | 41 | above (flag) |
| ic_review | 2 | 51.0 | 6 | within |
| ic_approved | 3 | 74.8 | 9 | within |
| under_financing | 2 | 48.5 | 18 | within |
| pre_close | 1 | 28.2 | 7 | within |
| closed (this wk) | 1 | 23.0 | — | — |

### Stalled-deal list

| deal_id | Stage | Days in stage | Owner | Next step |
|---|---|---|---|---|
| DP_DEAL_014 | under_loi | 21 | A. Patel | Seller reply on LOI counter |
| DP_DEAL_027 | under_dd | 34 | R. Chen | Roof scope resolution + DD extension |

### IC load

- **Next session:** 2 deals on docket, 1 expected to add. Overlay capacity band = 3. Within capacity.
- **Cross-link:** `workflows/investment_committee_prep/` active.

### Debt term sheet variance

- DP_DEAL_009: indicated coupon +55 bps over UW assumption. Outside overlay band. Flag.

### Retrade-risk flags

- DP_DEAL_027: DD finding on roof scope; seller extension requested; market shift since LOI beyond overlay threshold. Evidence pointer to Dealpath DD log.

### Capital-need concentration

- Equity need (stage-weighted): $38.4MM across 18 active deals. No single deal exceeds overlay concentration band.
- Debt need: $142.6MM. Concentration within band.

### Narrative memo (abridged)

> Pipeline advanced this week: one acquisition closed (DP_DEAL_003), one moved into pre_close (DP_DEAL_019), and two passed IC (DP_DEAL_022, DP_DEAL_024). Under-DD velocity sits above band at 41 days median, pulled by DP_DEAL_027's roof scope and a seller extension on DP_DEAL_014. Next IC carries 2 deals on docket with a third expected; within the overlay capacity band. One debt term sheet (DP_DEAL_009) indicated 55 bps wide of UW — not yet a portfolio pattern but worth watching if a second shows next week. DQ is clean on IC records; handoff lag on DP_DEAL_003 is within tolerance but surfaced. Handoff path to AppFolio / Intacct not yet activated.

### Confidence banner

```
References: dealpath_deal_pipeline@2026-04-10 (sample),
asset_crosswalk@2026-04-15 (sample), market_crosswalk@2026-04-15 (sample),
role_kpi_targets@2026-03-31 (starter),
approval_threshold_defaults@2026-03-31 (starter).
DQ: 1 warn (dp_handoff_lag), 1 info (dp_one_deal_multiple_projects). No blockers.
Metrics: all metric slugs proposed (not yet in _core/metrics.md).
```
