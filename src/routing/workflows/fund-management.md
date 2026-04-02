# Workflow Chain: Fund Management

## Purpose

Covers the complete fund lifecycle from formation and capital raising through deployment, ongoing portfolio management, investor reporting, and wind-down. This is the top-level orchestrator: the deal-pipeline-acquisition chain runs inside this chain's deployment phase. Fund management adds the LP relationship layer, portfolio-level allocation decisions, compliance/ESG overlays, and performance attribution that sit above individual asset operations.

## Chain Diagram

```
fund-formation-toolkit --> lp-pitch-deck-builder --> capital-raise-machine
  |
  v
portfolio-allocator (deployment strategy)
  |
  v [DEPLOY via Deal Pipeline]
  |
  v
quarterly-investor-update + performance-attribution
  +--> debt-portfolio-monitor
  +--> carbon-audit-compliance / climate-risk-assessment (ESG overlay)
```

## Entry Trigger Conditions

- Decision to launch new fund vehicle (opportunistic, value-add, core-plus, development)
- Existing fund approaching final close or deployment period
- Separate account mandate awarded by institutional LP
- Co-invest vehicle formation for specific deal
- Fund wind-down or extension decision point

## Step-by-Step Breakdown

| Step | Skill | Inputs | Outputs | Decision Gate | Daily-Ops Skills Used |
|------|-------|--------|---------|---------------|----------------------|
| 1 | fund-formation-toolkit | Fund strategy (sector, geography, return target), GP track record, target fund size, legal structure preferences | Fund term sheet, fee structure (mgmt fee, promote, catch-up), GP commit sizing, key person provisions, investment period/fund life parameters, legal entity structure | GP/counsel approval of terms. If LP feedback during marketing requires changes, loop back | entity-structure-advisor, fee-calculator |
| 2 | lp-pitch-deck-builder | Fund term sheet, GP track record data, market thesis, pipeline deals, competitive landscape | LP pitch deck, data room contents, DDQ (due diligence questionnaire) responses, track record tearsheet | Deck quality gate: does it pass internal review? Iterate until GP-approved | track-record-builder, ddq-response-library |
| 3 | capital-raise-machine | Approved pitch deck, LP target list, existing LP relationships, placement agent strategy | Capital raise pipeline tracker, LP meeting schedule, subscription document workflow, close schedule, commitment tracker | CLOSE GATE: first close (minimum viable fund size). Subsequent closes until hard cap or final close date | lp-crm-tracker, subscription-doc-processor, aml-kyc-checklist |
| 4 | portfolio-allocator | Fund size (committed capital), investment strategy, sector/geography allocation targets, pipeline deal quality | Deployment plan (allocation by sector, geography, deal size), pacing model, diversification constraints, reserve strategy | Allocation within fund mandate? Investment period remaining sufficient? Over-concentrated in any sector/geography? | pacing-model-engine, concentration-limit-checker |
| 5 | [DEAL PIPELINE] | Individual deal opportunities meeting fund criteria | Closed acquisitions/developments per deal-pipeline-acquisition and development-pipeline chains | Each deal passes through its own IC process. Fund-level gate: does this deal fit portfolio allocation? | All skills from deal-pipeline-acquisition chain |
| 6a | quarterly-investor-update | Portfolio performance data, asset-level NOI/occupancy, capital account balances, distribution history, market commentary | Quarterly LP letter, financial statements, portfolio summary, capital account statements, distribution notices | None -- regulatory/contractual obligation. Must meet reporting deadlines | lp-letter-drafter, capital-account-calculator, distribution-waterfall-runner |
| 6b | performance-attribution | Asset-level returns, fund-level returns, benchmark data, leverage impact | Attribution analysis (income vs. appreciation, asset selection vs. market beta, leverage effect), time-weighted vs. money-weighted returns, PME analysis | Performance review: is the fund tracking to target? Underperformance triggers portfolio review | twrr-mwrr-calculator, benchmark-comparison-engine, pme-calculator |
| 6c | debt-portfolio-monitor | All fund-level debt positions, rate environment, covenant compliance data, maturity schedule | Portfolio debt summary, covenant compliance dashboard, maturity ladder, interest rate exposure, floating rate risk quantification | Covenant breach risk? Maturity within 12 months? Rate cap expiration? Each triggers specific action | covenant-tracker, maturity-calendar, rate-cap-monitor |
| 6d-i | carbon-audit-compliance | Property-level energy consumption, utility data, GRESB survey requirements, regulatory requirements | Carbon footprint by asset, portfolio emissions total, GRESB submission data, regulatory compliance status, reduction pathway | GRESB submission deadline met? Regulatory compliance achieved? Identify assets needing energy retrofits | utility-data-aggregator, gresb-data-mapper |
| 6d-ii | climate-risk-assessment | Property locations, climate hazard data, insurance costs, physical risk scenarios | Climate risk scores by asset, portfolio-level risk exposure, insurance adequacy, stranded asset risk, adaptation investment needs | Material physical risk identified? If yes, triggers capex-prioritizer for resilience investments or disposition-strategy-engine for exit | flood-risk-scorer, heat-stress-analyzer, insurance-adequacy-tester |

## Data Handoff Specifications

### Step 1 -> 2 (Formation to Pitch Deck)
- **Payload**: `{fund_name, fund_strategy, target_size, fee_structure{mgmt_fee_pct, promote_structure, catch_up_pct, gp_commit_pct}, investment_period_years, fund_life_years, target_returns{net_irr, net_equity_multiple}, gp_track_record{}, legal_structure}`
- **Notes**: Pitch deck must accurately reflect all formation terms. Any term sheet changes require deck update

### Step 2 -> 3 (Pitch Deck to Capital Raise)
- **Payload**: `{approved_pitch_deck, data_room_url, ddq_responses{}, lp_target_list[{name, type, allocation_range, relationship_status, contact}], placement_agent_engagement | null}`

### Step 3 -> 4 (Capital Raise to Portfolio Allocator)
- **Payload**: `{total_commitments, close_schedule[{close_number, date, amount}], investment_period_end_date, fund_mandate_constraints{sector_limits, geography_limits, single_asset_limit, leverage_limit}}`
- **Trigger**: First close achieved (minimum capital to begin deployment)

### Step 4 -> 5 (Allocator to Deal Pipeline)
- **Payload**: `{deployment_budget_remaining, allocation_targets{sector: {target_pct, deployed_pct}, geography: {target_pct, deployed_pct}}, max_single_deal_size, leverage_parameters, return_hurdles}`
- **Notes**: Each deal entering the pipeline is screened against fund-level allocation constraints before proceeding through deal-level underwriting

### Step 5 -> 6a (Deals to Quarterly Update)
- **Payload**: `{portfolio_assets[{property_id, acquisition_date, cost_basis, current_value, current_noi, occupancy, debt_balance}], capital_account_balances[{lp_id, committed, called, distributed, nav}], fund_level_metrics{gross_irr, net_irr, gross_multiple, net_multiple, dpi, rvpi, tvpi}}`
- **Cadence**: Quarterly, with annual audited financials

### Step 5 -> 6b (Deals to Performance Attribution)
- **Payload**: `{asset_level_returns[{property_id, income_return, appreciation_return, leverage_contribution}], fund_level_return, benchmark_returns{}, time_series_cashflows[]}`

### Step 5 -> 6c (Deals to Debt Monitor)
- **Payload**: `{debt_positions[{loan_id, property_id, balance, rate, type, maturity_date, covenants{dscr_min, ltv_max}, rate_cap_expiry | null}], rate_environment{}}`

### Step 5 -> 6d (Deals to ESG)
- **Payload**: `{property_data[{property_id, address, sf, property_type, utility_accounts[], climate_zone, flood_zone, year_built}]}`

## Decision Gates Summary

| Gate | Location | Outcomes |
|------|----------|----------|
| Term Sheet Approval | After step 1 | Approved (proceed to pitch), revise (loop), abandon fund launch |
| Pitch Quality | After step 2 | Approved (go to market), revise (iterate) |
| First Close | During step 3 | Minimum achieved (begin deployment), not achieved (extend marketing or abort) |
| Hard Cap / Final Close | End of step 3 | Fund fully raised, or final close deadline reached |
| Allocation Fit | Before each deal in step 5 | Fits mandate (proceed with deal pipeline), exceeds limits (pass or request LP consent) |
| Performance Review | After step 6b | On-track (continue), underperforming (trigger portfolio review, consider dispositions) |
| Covenant Watch | After step 6c | Compliant (no action), watch list (monitor closely), breach risk (cure or restructure) |
| Fund Extension | End of fund life | Extend (LP vote), wind down (begin dispositions), fully realized |

## Fund Lifecycle Phases

| Phase | Duration | Primary Skills Active |
|-------|----------|----------------------|
| Formation | 3-6 months | fund-formation-toolkit |
| Marketing / Capital Raise | 6-18 months | lp-pitch-deck-builder, capital-raise-machine |
| Investment Period | 2-4 years | portfolio-allocator, deal-pipeline-acquisition (all sub-skills) |
| Hold / Management | 3-7 years | hold-period-management chain, quarterly-investor-update, performance-attribution, debt-portfolio-monitor |
| Harvest / Wind-Down | 1-3 years | disposition-pipeline chain, final distributions, fund accounting |

## Exit Conditions

- **Fund Fully Realized**: All assets sold or refinanced, proceeds distributed, fund wound down. Final audited financials and performance report issued
- **Fund Extension**: LP vote approves 1-2 year extension to complete dispositions. Continue hold-period-management and disposition chains
- **GP Removal**: Key person event or cause removal. Transition management or wind down
- **Successor Fund**: New fund launched. Remaining assets in prior fund continue through hold and disposition chains

## Estimated Time Savings

| Phase | Manual | Automated Chain | Savings |
|-------|--------|-----------------|---------|
| Fund formation + legal structuring | 40-80 hrs | 10-20 hrs | 75% |
| Pitch deck + DDQ prep | 30-60 hrs | 8-15 hrs | 75% |
| Capital raise tracking + docs | 15-25 hrs/month during raise | 4-8 hrs/month | 70% |
| Portfolio allocation + pacing | 8-16 hrs/quarter | 2-4 hrs/quarter | 75% |
| Quarterly LP reporting | 20-40 hrs/quarter | 5-10 hrs/quarter | 75% |
| Performance attribution | 8-16 hrs/quarter | 1-3 hrs/quarter | 80-85% |
| Debt portfolio monitoring | 4-8 hrs/month | 1-2 hrs/month | 75% |
| ESG / climate reporting | 20-40 hrs/year | 5-10 hrs/year | 75% |
| **Annual fund overhead** | **~600-1100 hrs** | **~150-300 hrs** | **~74%** |
