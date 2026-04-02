# CRE Skill Routing Index

> 112 CRE skills across 16 subcategories. Use this index to find the right skill -- do NOT load all SKILL.md files.
> When a CRE task comes in, match the user's request to a category below, then invoke the specific skill via `/skill-slug`.
> Only read the full SKILL.md + references when you need the detailed process.

## Quick Routing Table

| User says... | Invoke this skill |
|---|---|
| "1031", "like-kind exchange", "tax deferral" | `/1031-exchange-executor` |
| "1031 pipeline", "replacement property pipeline", "exchange timeline", "1031 ID deadline" | `/1031-pipeline-manager` |
| "underwrite this deal", "run the numbers", "model this property" | `/acquisition-underwriting-engine` |
| "annual budget", "operating budget", "IREM benchmark" | `/annual-budget-engine` |
| "PM schedule", "HVAC maintenance", "elevator inspection" | `/building-systems-maintenance-manager` |
| "CAM reconciliation", "tenant billing", "common area maintenance" | `/cam-reconciliation-calculator` |
| "capex", "capital projects", "replacement reserves" | `/capex-prioritizer` |
| "capital raise", "data room", "capital call" | `/capital-raise-machine` |
| "capital stack", "optimal leverage", "WACC" | `/capital-stack-optimizer` |
| "carbon audit", "LL97", "GRESB", "emissions" | `/carbon-audit-compliance` |
| "climate risk", "flood risk", "TCFD", "stranded asset" | `/climate-risk-assessment` |
| "closing checklist", "title review", "closing timeline" | `/closing-checklist-tracker` |
| "certificate of insurance", "COI", "insurance compliance" | `/coi-compliance-checker` |
| "comps", "comparable sales", "rent comps" | `/comp-snapshot` |
| "building code violation", "OSHA", "ADA compliance" | `/compliance-regulatory-response-kit` |
| "GC budget", "CSI benchmarks", "construction costs" | `/construction-budget-gc-analyzer` |
| "estimate construction costs", "how much to build", "TDC estimate", "price this floor plan" | `/construction-cost-estimator` |
| "GC selection", "bid leveling", "GMP negotiation" | `/construction-procurement-contracts-engine` |
| "RFI", "submittal", "construction draw", "punch list" | `/construction-project-command-center` |
| "cost segregation", "accelerated depreciation", "bonus depreciation" | `/cost-segregation-analyzer` |
| "CPI escalation", "rent escalation", "CPI adjustment" | `/cpi-escalation-calculator` |
| "seller financing", "carryback", "assumption vs new loan" | `/creative-seller-financing` |
| "environmental remediation", "tenant bankruptcy", "condemnation" | `/crisis-special-situations-playbook` |
| "due diligence", "DD period", "inspection period" | `/dd-command-center` |
| "deal attribution", "deal-level P&L", "track record attribution", "realized/unrealized" | `/deal-attribution-tracker` |
| "screen this deal", "should I look at this", "new OM/listing" | `/deal-quick-screen` |
| "debt covenant", "DSCR compliance", "covenant breach" | `/debt-covenant-monitor` |
| "debt portfolio", "loan watchlist", "maturity wall" | `/debt-portfolio-monitor` |
| "development proforma", "construction budget", "draw schedule" | `/dev-proforma-engine` |
| "prepare for sale", "broker selection", "disposition prep" | `/disposition-prep-kit` |
| "sell vs hold", "disposition strategy", "exit analysis" | `/disposition-strategy-engine` |
| "distressed", "special servicing", "note purchase", "REO" | `/distressed-acquisition-playbook` |
| "distribution notice", "capital distribution", "distribution waterfall letter" | `/distribution-notice-generator` |
| "emerging manager", "first-time fund", "emerging GP evaluation", "seed allocation" | `/emerging-manager-evaluator` |
| "zoning", "entitlement", "rezoning", "variance" | `/entitlement-feasibility` |
| "estoppel", "estoppel certificate" | `/estoppel-certificate-generator` |
| "fund formation", "PPM", "Reg D", "GP commitment" | `/fund-formation-toolkit` |
| "fund compliance", "capital account", "Form D", "LPAC" | `/fund-operations-compliance-dashboard` |
| "track fund raise", "LP negotiation tracker", "model fee concession", "blended management fee", "MFN cascade analysis" | `/fund-raise-negotiation-engine` |
| "compare fund terms", "fee comparison", "carried interest benchmark", "fund economics comparison" | `/fund-terms-comparator` |
| "calculate funds flow", "closing statement", "HUD-1", "settlement statement", "wire amounts" | `/funds-flow-calculator` |
| "evaluate GP performance", "assess GP track record", "GP evaluation", "manager due diligence" | `/gp-performance-evaluator` |
| "IC memo", "investment committee", "deal presentation" | `/ic-memo-generator` |
| "insurance renewal", "coverage adequacy", "builder's risk" | `/insurance-risk-manager` |
| "investor meeting", "audit coordination", "GIPS composite" | `/investor-lifecycle-manager` |
| "waterfall", "promote", "preferred return", "GP/LP split" | `/jv-waterfall-architect` |
| "land residual", "HBU", "highest and best use" | `/land-residual-hbu-analyzer` |
| "lease abstract", "extract lease terms" | `/lease-abstract-extractor` |
| "lease compliance", "CAM audit", "percentage rent audit" | `/lease-compliance-auditor` |
| "lease amendment", "expansion option", "build-to-suit" | `/lease-document-factory` |
| "lease negotiation", "anchor replacement", "sublease consent" | `/lease-negotiation-analyzer` |
| "structure lease options", "purchase option", "ROFR", "ROFO", "expansion option structure" | `/lease-option-structurer` |
| "trade out analysis", "lease trade-out", "effective rent trade-out", "roll-to-market delta" | `/lease-trade-out-analyzer` |
| "lease-up", "absorption", "concession strategy" | `/lease-up-war-room` |
| "leasing pipeline", "tour prep", "prospect follow-up" | `/leasing-operations-engine` |
| "marketing plan", "TI benchmarks", "commission benchmarks" | `/leasing-strategy-marketing-planner` |
| "lender compliance certificate", "lender reporting" | `/lender-compliance-certificate` |
| "review loan documents", "loan agreement review", "promissory note review", "security agreement review" | `/loan-document-reviewer` |
| "size the loan", "DSCR/LTV/debt yield", "agency loan" | `/loan-sizing-engine` |
| "draft an LOI", "build an offer", "structure the bid" | `/loi-offer-builder` |
| "generate LP data request", "LP questionnaire", "DDQ", "LP information request" | `/lp-data-request-generator` |
| "pitch deck", "LP presentation", "track record" | `/lp-pitch-deck-builder` |
| "market cycle", "where are we in the cycle", "Mueller" | `/market-cycle-positioner` |
| "mezz", "preferred equity", "subordinate capital" | `/mezz-pref-structurer` |
| "Monte Carlo", "return simulation", "probability distribution", "stochastic model" | `/monte-carlo-return-simulator` |
| "NOI sprint", "90-day plan", "stabilize NOI" | `/noi-sprint-plan` |
| "reverse price this OM", "what should I pay" | `/om-reverse-pricing` |
| "opportunity zone", "OZ", "QOZB" | `/opportunity-zone-underwriter` |
| "partnership allocation", "704(b)", "UBIT", "K-1" | `/partnership-allocation-engine` |
| "performance attribution", "alpha", "NCREIF benchmark" | `/performance-attribution` |
| "portfolio allocation", "concentration risk", "rebalancing" | `/portfolio-allocator` |
| "post-close onboarding", "PM transition", "asset handoff" | `/post-close-onboarding-transition` |
| "property management command center", "PM dashboard", "full PM operations" | `/property-management-orchestrator` |
| "parking management", "janitorial", "tenant survey" | `/property-operations-admin-toolkit` |
| "property performance", "dashboard", "hold/sell/refi" | `/property-performance-dashboard` |
| "property tax appeal", "assessment challenge" | `/property-tax-appeal-analyzer` |
| "review this PSA", "redline strategy" | `/psa-redline-strategy` |
| "investor update", "quarterly report", "LP letter" | `/quarterly-investor-update` |
| "refinance", "refi", "loan maturity" | `/refi-decision-analyzer` |
| "rent optimization", "loss-to-lease", "rent increase plan" | `/rent-optimization-planner` |
| "analyze this rent roll", "clean up this rent roll" | `/rent-roll-analyzer` |
| "standardize rent roll", "format rent roll" | `/rent-roll-formatter` |
| "Reg D", "506(b)", "506(c)", "accredited investor verification", "blue sky filing" | `/sec-reg-d-compliance` |
| "stress test", "sensitivity analysis", "where does it break" | `/sensitivity-stress-test` |
| "small operator PM", "self-manage", "landlord operations", "1-50 units" | `/small-operator-pm` |
| "deal sourcing", "off-market", "outreach", "broker network" | `/sourcing-outreach-system` |
| "stacking plan", "floor plan", "space layout" | `/stacking-plan-builder` |
| "submarket analysis", "market reality check" | `/submarket-truth-serum` |
| "supply pipeline", "absorption forecast" | `/supply-demand-forecast` |
| "normalize T-12", "trailing twelve", "one-time items" | `/t12-normalizer` |
| "analyze tenant credit", "tenant financials", "tenant creditworthiness", "guarantor strength" | `/tenant-credit-analyzer` |
| "delinquent tenant", "eviction", "tenant workout" | `/tenant-delinquency-workout` |
| "tenant event", "appreciation event", "holiday party" | `/tenant-event-planner` |
| "tenant retention", "lease renewal", "WALT impact" | `/tenant-retention-engine` |
| "build term sheet", "lender term sheet", "loan term sheet", "quote term sheet" | `/term-sheet-builder` |
| "review title commitment", "title exceptions", "title insurance schedule B", "title defects" | `/title-commitment-reviewer` |
| "prepare transfer documents", "deed preparation", "assignment of leases", "transfer instruments" | `/transfer-document-preparer` |
| "variance narrative", "budget vs actual explanation" | `/variance-narrative-generator` |
| "vendor invoice", "invoice validation" | `/vendor-invoice-validator` |
| "work order", "maintenance request", "triage" | `/work-order-triage` |
| "workout", "loan modification", "forbearance", "DPO" | `/workout-playbook` |

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
