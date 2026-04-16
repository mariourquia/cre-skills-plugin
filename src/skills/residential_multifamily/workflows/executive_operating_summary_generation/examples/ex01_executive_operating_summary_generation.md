# Example — Executive Operating Summary (abridged, board packet)

**Prompt:** "Build the Q1 2026 board packet for the residential portfolio."

**Inputs:** AM reviews (3 months per asset) + quarterly portfolio review + same-store set + watchlist scoring + fund debt schedule + capex program summary + board packet template.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- audience: board
- org_id: {org}
- period: Q1 2026
- role: ceo_executive_leader / cfo_finance_leader
- output_type: operating_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/executive_operating_summary_generation/`
- `workflows/quarterly_portfolio_review/` (feeder)
- `workflows/monthly_asset_management_review/` (feeder)
- `overlays/segments/middle_market/`
- `overlays/management_mode/owner_oversight/`

## Expected references

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/derived/same_store_set__{org}.yaml`
- `reference/normalized/board_packet_template__{org}.md`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Board submission: row 16.
- Investor submission (if dual-audience): row 15.
- Lender submission (parallel workflow): row 14.
- Fair-housing / compliance disclosure: counsel-led; row 3 if public-facing.

## Expected output shape

- 1-3 page narrative summary with cited metrics.
- 1-page KPI dashboard.
- Covenant posture view.
- Watchlist distribution + top movers with drivers.
- Capex program summary.
- Lease-up status view (if applicable).
- Forecast discipline summary.
- Forward view.
- Approval request bundle.

## Confidence banner pattern

```
References: watchlist_scoring@2026-03-31 (starter), same_store_set@2026-03-31 (starter),
board_packet_template@2026-03-31 (starter), role_kpi_targets@2026-03-31 (starter).
External-use notation on any sample-tagged reference.
```

## Verdict-first output sample (conforms to `_core/executive_output_contract.md`)

### Verdict

- **Recommendation:** Proceed with Q1 board submission as drafted; add one covenant-watch addendum for Loan L-202.
- **Rationale:**
  1. Same-store NOI growth 3.8% YoY `[derived]` — ahead of the 3.2% `[benchmark]` portfolio target and the 3.0% `[overlay]` board floor.
  2. Watchlist movers limited to two assets, both already in AM action plans; aggregate exposure $4.2M `[derived]`.
  3. Covenant cushion on Loan L-202 compressed to 1.18x DSCR `[operator]` vs. 1.15x `[overlay]` floor — flag but not breach.
- **Confidence:** medium (watchlist_scoring and same_store_set are starter-tagged; board_packet_template is org-overlaid).
- **Materiality:** $14.3M YTD NOI `[derived]`; $92M fund NAV movement quarter-over-quarter.
- **Next action:** CFO to sign L-202 covenant-watch addendum and attach before the 2026-05-01 board meeting.

### Source-class legend

| Tag              | Meaning in this output                                                 |
|------------------|------------------------------------------------------------------------|
| `[operator]`     | Entered by a human operator in PMS, GL, or lender portal               |
| `[derived]`      | Computed from other cells by this workflow or a feeder workflow        |
| `[benchmark]`    | From `reference/normalized/` or `reference/derived/` file              |
| `[overlay]`      | From an `overlays/<org_or_loan_or_market>/` file at runtime            |
| `[placeholder]`  | Illustrative; BLOCKS final submission                                  |

### Evidence tables (excerpt)

| Metric                     | Value            | Source         |
|----------------------------|------------------|----------------|
| Same-store NOI growth YoY  | 3.8%             | `[derived]`    |
| Portfolio target NOI growth| 3.2%             | `[benchmark]`  |
| Board floor NOI growth     | 3.0%             | `[overlay]`    |
| Aggregate watchlist exposure | $4.2M          | `[derived]`    |
| Loan L-202 DSCR            | 1.18x            | `[operator]`   |
| Loan L-202 DSCR floor      | 1.15x            | `[overlay]`    |

If any cell in the production version of this table is labeled
`[placeholder]`, the board-submission approval request (row 16) MUST
NOT be assembled — the workflow refuses per
`_core/executive_output_contract.md#rule-2`.
