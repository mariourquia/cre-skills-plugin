# CRE Skill Routing Index

> 99 CRE skills across 16 subcategories. Use this index to find the right skill -- do NOT load all SKILL.md files.
> When a CRE task comes in, match the user's request to a category below, then invoke the specific skill via `/skill-slug`.
> Only read the full SKILL.md + references when you need the detailed process.

## Quick Routing Table

| User says... | Invoke this skill |
|---|---|
| "screen this deal", "should I look at this", new OM/listing | `/deal-quick-screen` |
| "reverse price this OM", "what should I pay" | `/om-reverse-pricing` |
| "underwrite this deal", "run the numbers", "model this property" | `/acquisition-underwriting-engine` |
| "analyze this rent roll", "clean up this rent roll" | `/rent-roll-analyzer` |
| "stress test", "sensitivity analysis", "where does it break" | `/sensitivity-stress-test` |
| "draft an LOI", "build an offer", "structure the bid" | `/loi-offer-builder` |
| "review this PSA", "redline strategy" | `/psa-redline-strategy` |
| "waterfall", "promote", "preferred return", "GP/LP split" | `/jv-waterfall-architect` |
| "1031", "like-kind exchange", "tax deferral" | `/1031-exchange-executor` |
| "seller financing", "carryback", "assumption vs new loan" | `/creative-seller-financing` |
| "due diligence", "DD period", "inspection period" | `/dd-command-center` |
| "distressed", "special servicing", "note purchase", "REO" | `/distressed-acquisition-playbook` |
| "size the loan", "DSCR/LTV/debt yield", "agency loan" | `/loan-sizing-engine` |
| "mezz", "preferred equity", "subordinate capital" | `/mezz-pref-structurer` |
| "refinance", "refi", "loan maturity" | `/refi-decision-analyzer` |
| "capital stack", "optimal leverage", "WACC" | `/capital-stack-optimizer` |
| "debt portfolio", "loan watchlist", "maturity wall" | `/debt-portfolio-monitor` |
| "workout", "loan modification", "forbearance", "DPO" | `/workout-playbook` |
| "submarket analysis", "market reality check" | `/submarket-truth-serum` |
| "comps", "comparable sales", "rent comps" | `/comp-snapshot` |
| "supply pipeline", "absorption forecast" | `/supply-demand-forecast` |
| "market cycle", "where are we in the cycle", "Mueller" | `/market-cycle-positioner` |
| "annual budget", "operating budget", "IREM benchmark" | `/annual-budget-engine` |
| "NOI sprint", "90-day plan", "stabilize NOI" | `/noi-sprint-plan` |
| "property performance", "dashboard", "hold/sell/refi" | `/property-performance-dashboard` |
| "capex", "capital projects", "replacement reserves" | `/capex-prioritizer` |
| "lease compliance", "CAM audit", "percentage rent audit" | `/lease-compliance-auditor` |
| "delinquent tenant", "eviction", "tenant workout" | `/tenant-delinquency-workout` |
| "tenant retention", "lease renewal", "WALT impact" | `/tenant-retention-engine` |
| "lease-up", "absorption", "concession strategy" | `/lease-up-war-room` |
| "lease negotiation", "anchor replacement", "sublease consent" | `/lease-negotiation-analyzer` |
| "rent optimization", "loss-to-lease", "rent increase plan" | `/rent-optimization-planner` |
| "IC memo", "investment committee", "deal presentation" | `/ic-memo-generator` |
| "investor update", "quarterly report", "LP letter" | `/quarterly-investor-update` |
| "pitch deck", "LP presentation", "track record" | `/lp-pitch-deck-builder` |
| "capital raise", "data room", "capital call" | `/capital-raise-machine` |
| "fund formation", "PPM", "Reg D", "GP commitment" | `/fund-formation-toolkit` |
| "land residual", "HBU", "highest and best use" | `/land-residual-hbu-analyzer` |
| "development proforma", "construction budget", "draw schedule" | `/dev-proforma-engine` |
| "zoning", "entitlement", "rezoning", "variance" | `/entitlement-feasibility` |
| "GC budget", "CSI benchmarks", "construction costs" | `/construction-budget-gc-analyzer` |
| "sell vs hold", "disposition strategy", "exit analysis" | `/disposition-strategy-engine` |
| "prepare for sale", "broker selection", "disposition prep" | `/disposition-prep-kit` |
| "deal sourcing", "off-market", "outreach", "broker network" | `/sourcing-outreach-system` |
| "cost segregation", "accelerated depreciation", "bonus depreciation" | `/cost-segregation-analyzer` |
| "opportunity zone", "OZ", "QOZB" | `/opportunity-zone-underwriter` |
| "partnership allocation", "704(b)", "UBIT", "K-1" | `/partnership-allocation-engine` |
| "carbon audit", "LL97", "GRESB", "emissions" | `/carbon-audit-compliance` |
| "climate risk", "flood risk", "TCFD", "stranded asset" | `/climate-risk-assessment` |
| "portfolio allocation", "concentration risk", "rebalancing" | `/portfolio-allocator` |
| "performance attribution", "alpha", "NCREIF benchmark" | `/performance-attribution` |
| "CAM reconciliation", "tenant billing", "common area maintenance" | `/cam-reconciliation-calculator` |
| "estoppel", "estoppel certificate" | `/estoppel-certificate-generator` |
| "normalize T-12", "trailing twelve", "one-time items" | `/t12-normalizer` |
| "lease abstract", "extract lease terms" | `/lease-abstract-extractor` |
| "certificate of insurance", "COI", "insurance compliance" | `/coi-compliance-checker` |
| "work order", "maintenance request", "triage" | `/work-order-triage` |
| "debt covenant", "DSCR compliance", "covenant breach" | `/debt-covenant-monitor` |
| "CPI escalation", "rent escalation", "CPI adjustment" | `/cpi-escalation-calculator` |
| "vendor invoice", "invoice validation" | `/vendor-invoice-validator` |
| "property tax appeal", "assessment challenge" | `/property-tax-appeal-analyzer` |
| "variance narrative", "budget vs actual explanation" | `/variance-narrative-generator` |
| "closing checklist", "title review", "closing timeline" | `/closing-checklist-tracker` |
| "standardize rent roll", "format rent roll" | `/rent-roll-formatter` |
| "lender compliance certificate", "lender reporting" | `/lender-compliance-certificate` |
| "stacking plan", "floor plan", "space layout" | `/stacking-plan-builder` |
| "RFI", "submittal", "construction draw", "punch list" | `/construction-project-command-center` |
| "fund compliance", "capital account", "Form D", "LPAC" | `/fund-operations-compliance-dashboard` |
| "PM schedule", "HVAC maintenance", "elevator inspection" | `/building-systems-maintenance-manager` |
| "leasing pipeline", "tour prep", "prospect follow-up" | `/leasing-operations-engine` |
| "investor meeting", "audit coordination", "GIPS composite" | `/investor-lifecycle-manager` |
| "environmental remediation", "tenant bankruptcy", "condemnation" | `/crisis-special-situations-playbook` |
| "building code violation", "OSHA", "ADA compliance" | `/compliance-regulatory-response-kit` |
| "parking management", "janitorial", "tenant survey" | `/property-operations-admin-toolkit` |
| "GC selection", "bid leveling", "GMP negotiation" | `/construction-procurement-contracts-engine` |
| "insurance renewal", "coverage adequacy", "builder's risk" | `/insurance-risk-manager` |
| "lease amendment", "expansion option", "build-to-suit" | `/lease-document-factory` |
| "marketing plan", "TI benchmarks", "commission benchmarks" | `/leasing-strategy-marketing-planner` |
| "post-close onboarding", "PM transition", "asset handoff" | `/post-close-onboarding-transition` |
| "tenant event", "appreciation event", "holiday party" | `/tenant-event-planner` |
| "review title commitment", "title exceptions", "title insurance schedule B", "title defects" | `/title-commitment-reviewer` |
| "analyze tenant credit", "tenant financials", "tenant creditworthiness", "guarantor strength" | `/tenant-credit-analyzer` |
| "build term sheet", "lender term sheet", "loan term sheet", "quote term sheet" | `/term-sheet-builder` |
| "review loan documents", "loan agreement review", "promissory note review", "security agreement review" | `/loan-document-reviewer` |
| "prepare transfer documents", "deed preparation", "assignment of leases", "transfer instruments" | `/transfer-document-preparer` |
| "calculate funds flow", "closing statement", "HUD-1", "settlement statement", "wire amounts" | `/funds-flow-calculator` |
| "structure lease options", "purchase option", "ROFR", "ROFO", "expansion option structure" | `/lease-option-structurer` |
| "trade out analysis", "lease trade-out", "effective rent trade-out", "roll-to-market delta" | `/lease-trade-out-analyzer` |
| "evaluate GP performance", "assess GP track record", "GP evaluation", "manager due diligence" | `/gp-performance-evaluator` |
| "compare fund terms", "fee comparison", "carried interest benchmark", "fund economics comparison" | `/fund-terms-comparator` |
| "generate LP data request", "LP questionnaire", "DDQ", "LP information request" | `/lp-data-request-generator` |
| "Reg D", "506(b)", "506(c)", "accredited investor verification", "blue sky filing" | `/sec-reg-d-compliance` |
| "Monte Carlo", "return simulation", "probability distribution", "stochastic model" | `/monte-carlo-return-simulator` |
| "property management", "PM operations", "daily operations checklist", "site team" | `/property-management-operations` |
| "distribution notice", "capital distribution", "distribution waterfall letter" | `/distribution-notice-generator` |
| "1031 pipeline", "replacement property pipeline", "exchange timeline", "1031 ID deadline" | `/1031-pipeline-manager` |
| "deal attribution", "deal-level P&L", "track record attribution", "realized/unrealized" | `/deal-attribution-tracker` |
| "emerging manager", "first-time fund", "emerging GP evaluation", "seed allocation" | `/emerging-manager-evaluator` |
| "track fund raise", "LP negotiation tracker" | `/fund-raise-negotiation-engine` |
| "model fee concession", "blended management fee" | `/fund-raise-negotiation-engine` |
| "MFN cascade analysis" | `/fund-raise-negotiation-engine` |

## Workflow Chains

When a task spans multiple skills, use these chains (detailed docs in `plans/reit-cre/_workflows/`):

1. **Acquisition Pipeline**: sourcing -> quick-screen -> [KEEP] -> om-reverse -> rent-roll-analyzer -> underwriting-engine -> sensitivity -> ic-memo -> loi -> psa-redline -> dd-command-center -> close
2. **Capital Stack**: underwriting-engine -> loan-sizing -> mezz-pref -> jv-waterfall -> capital-stack-optimizer -> refi-decision (at maturity)
3. **Hold Period**: annual-budget -> performance-dashboard -> capex/lease-compliance/delinquency-workout/retention-engine -> noi-sprint (if needed)
4. **Disposition**: performance-dashboard -> disposition-strategy -> [SELL] disposition-prep -> 1031-exchange | [HOLD] refi-decision | [REFI] loan-sizing
5. **Development**: land-residual + entitlement -> dev-proforma -> construction-budget -> loan-sizing -> capital-stack -> ic-memo -> lease-up-war-room -> refi-decision
6. **Fund Management**: fund-formation -> pitch-deck -> capital-raise -> portfolio-allocator -> [deploy via acquisition pipeline] -> quarterly-update + performance-attribution

## Skill Locations

All skills: `~/.claude/skills-lab/skills/<slug>/SKILL.md`
Reference files: `~/.claude/skills-lab/skills/<slug>/references/`
Commands: `~/.claude/commands/<slug>.md`
Workflow docs: `~/.claude/skills-lab/plans/reit-cre/_workflows/`
Registry: `~/.claude/skills-lab/plans/reit-cre/_registry.yaml`
