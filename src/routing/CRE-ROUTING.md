# CRE Skill Routing Index

> 127 CRE skills across 16 subcategories. Use this index to find the right skill -- do NOT load all SKILL.md files.
> When a CRE task comes in, match the user's request to a category below, then invoke the specific skill via `/skill-slug`.
> Only read the full SKILL.md + references when you need the detailed process.

## Quick Routing Table

> This table routes to **specialist** skills only. The 7 `category: workspace` skills (`navigator`, `deal-intake`, `lease-strategy-papering`, `asset-ops-cockpit`, `capital-projects-development`, `fund-lp-reporting`, `plugin-admin`) are intentionally excluded: they are top-level entry points / orchestration routers that dispatch *to* the specialists below (and among themselves via `navigator`), so they carry no trigger-phrase row. Their absence here is by design, not a coverage gap. The `residential_multifamily` domain subsystem is likewise excluded and is documented in its own section below.

| User says... | Invoke this skill |
|---|---|
| "1031", "like-kind exchange", "tax deferral" | `/1031-exchange-executor` |
| "1031 pipeline", "replacement property pipeline", "exchange timeline", "1031 ID deadline" | `/1031-pipeline-manager` |
| "underwrite this deal", "run the numbers", "model this property" | `/acquisition-underwriting-engine` |
| "analyze this agency quote", "compare Freddie vs Fannie", "DUS quote", "Optigo quote" | `/agency-loan-quote-analyzer` |
| "run the IC workflow", "take this deal from data room to IC", "orchestrate the acquisition" | `/amos-icomm-demo-orchestrator` |
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
| "quick underwrite", "deal analysis", "go/no-go scorecard" | `/deal-underwriting-assistant` |
| "debt covenant", "DSCR compliance", "covenant breach" | `/debt-covenant-monitor` |
| "debt portfolio", "loan watchlist", "maturity wall" | `/debt-portfolio-monitor` |
| "development proforma", "construction budget", "draw schedule" | `/dev-proforma-engine` |
| "prepare for sale", "broker selection", "disposition prep" | `/disposition-prep-kit` |
| "sell vs hold", "disposition strategy", "exit analysis" | `/disposition-strategy-engine` |
| "distressed", "special servicing", "note purchase", "REO" | `/distressed-acquisition-playbook` |
| "distribution notice", "capital distribution", "distribution waterfall letter" | `/distribution-notice-generator` |
| "extract the data room", "build the fact table", "index this deal package" | `/document-to-data-room-extractor` |
| "turn these documents into a database", "ingest this data room to our schema" | `/document-to-database` |
| "build the warehouse dataset", "assemble these extractions", "validate the data room for the model", "make this deck-ready", "stage extracted data for the warehouse" | `/document-to-warehouse-pipeline` |
| "emerging manager", "first-time fund", "emerging GP evaluation", "seed allocation" | `/emerging-manager-evaluator` |
| "zoning", "entitlement", "rezoning", "variance" | `/entitlement-feasibility` |
| "estoppel", "estoppel certificate" | `/estoppel-certificate-generator` |
| "fund formation", "PPM", "Reg D", "GP commitment" | `/fund-formation-toolkit` |
| "fund compliance", "capital account", "Form D", "LPAC" | `/fund-operations-compliance-dashboard` |
| "track fund raise", "LP negotiation tracker", "model fee concession", "blended management fee", "MFN cascade analysis" | `/fund-raise-negotiation-engine` |
| "compare fund terms", "fee comparison", "carried interest benchmark", "fund economics comparison" | `/fund-terms-comparator` |
| "calculate funds flow", "closing statement", "HUD-1", "settlement statement", "wire amounts" | `/funds-flow-calculator` |
| "evaluate GP performance", "assess GP track record", "GP evaluation", "manager due diligence" | `/gp-performance-evaluator` |
| "build the IC deck", "compose the committee deck", "valuation committee deck", "quarterly asset review deck", "annual business plan deck" | `/ic-deck-composer` |
| "IC memo", "investment committee", "deal presentation" | `/ic-memo-generator` |
| "red team this deal", "pressure-test the recommendation", "play devil's advocate" | `/ic-red-team-challenger` |
| "build the IC Q&A pack", "prep for committee questions", "what will IC ask" | `/icomm-context-builder` |
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
| "write a market memo", "market update" | `/market-memo-generator` |
| "mezz", "preferred equity", "subordinate capital" | `/mezz-pref-structurer` |
| "Monte Carlo", "return simulation", "probability distribution", "stochastic model" | `/monte-carlo-return-simulator` |
| "NOI sprint", "90-day plan", "stabilize NOI" | `/noi-sprint-plan` |
| "reverse price this OM", "what should I pay" | `/om-reverse-pricing` |
| "load this operating statement", "normalize the P&L to our accounts" | `/operating-statement-to-database` |
| "opportunity zone", "OZ", "QOZB" | `/opportunity-zone-underwriter` |
| "partnership allocation", "704(b)", "UBIT", "K-1" | `/partnership-allocation-engine` |
| "PCA", "property condition assessment", "reserve adequacy" | `/pca-reserve-analyzer` |
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
| "REIT profile", "build a REIT comp", "REIT ticker" | `/reit-profile-builder` |
| "rent optimization", "loss-to-lease", "rent increase plan" | `/rent-optimization-planner` |
| "analyze this rent roll", "clean up this rent roll" | `/rent-roll-analyzer` |
| "standardize rent roll", "format rent roll" | `/rent-roll-formatter` |
| "tie out the rent roll to the T-12", "reconcile contractual rent to actuals", "revenue leakage check" | `/rent-roll-t12-tieout` |
| "load this rent roll into the database", "normalize the rent roll to our schema", "rent roll to warehouse" | `/rent-roll-to-database` |
| "Reg D", "506(b)", "506(c)", "accredited investor verification", "blue sky filing" | `/sec-reg-d-compliance` |
| "stress test", "sensitivity analysis", "where does it break" | `/sensitivity-stress-test` |
| "small operator PM", "self-manage", "landlord operations", "1-50 units" | `/small-operator-pm` |
| "deal sourcing", "off-market", "outreach", "broker network" | `/sourcing-outreach-system` |
| "stacking plan", "floor plan", "space layout" | `/stacking-plan-builder` |
| "submarket analysis", "market reality check" | `/submarket-truth-serum` |
| "supply pipeline", "absorption forecast" | `/supply-demand-forecast` |
| "normalize T-12", "trailing twelve", "one-time items" | `/t12-normalizer` |
| "load this T-12", "normalize the trailing twelve into the database", "T-12 to warehouse" | `/t12-to-database` |
| "analyze tenant credit", "tenant financials", "tenant creditworthiness", "guarantor strength" | `/tenant-credit-analyzer` |
| "delinquent tenant", "eviction", "tenant workout" | `/tenant-delinquency-workout` |
| "tenant event", "appreciation event", "holiday party" | `/tenant-event-planner` |
| "tenant retention", "lease renewal", "WALT impact" | `/tenant-retention-engine` |
| "build term sheet", "lender term sheet", "loan term sheet", "quote term sheet" | `/term-sheet-builder` |
| "review title commitment", "title exceptions", "title insurance schedule B", "title defects" | `/title-commitment-reviewer` |
| "prepare transfer documents", "deed preparation", "assignment of leases", "transfer instruments" | `/transfer-document-preparer` |
| "variance narrative", "budget vs actual explanation" | `/variance-narrative-generator` |
| "vendor invoice", "invoice validation" | `/vendor-invoice-validator` |
| "map this to exhibits", "turn the dataset into slides", "build the exhibit specs", "table or chart for this deck", "spec the slide inputs" | `/warehouse-to-exhibit-mapper` |
| "work order", "maintenance request", "triage" | `/work-order-triage` |
| "workout", "loan modification", "forbearance", "DPO" | `/workout-playbook` |

## Residential Multifamily subsystem (not a trigger-phrase skill)

`residential_multifamily` is intentionally absent from the table above and is **not** a flat `/<slug>` skill. It is a self-contained **subsystem router** (`classification: workspace`, `runtime_role: workspace_router`, `category: cross-cutting`) that ships its own `_core/` taxonomy, `roles/`, `workflows/`, `overlays/`, `templates/`, and a `tailoring/` interview. Its catalog `intent_triggers` are empty by design, so the dispatcher never phrase-routes to it. How it is actually invoked:

- **Signal-based activation, not a phrase match.** It engages when the request concerns a U.S. residential multifamily property/portfolio/development -- a property tagged multifamily, an asker in a multifamily role (property/regional/asset/portfolio manager, development/construction manager, COO/CFO/CEO over MF), or one of its workflows (`delinquency_collections`, `renewal_retention`, `monthly_asset_management_review`, `draw_package_review`, `executive_operating_summary_generation`, ...).
- **It classifies and dispatches; it does not answer directly.** The router resolves 10 taxonomy axes (asset_class, segment, form_factor, lifecycle_stage, management_mode, role/workflow, market, org), asks **one** focused question when a required axis is unresolved, layers overlays, loads the matching role/workflow packs plus their references, and executes inside `_core/guardrails.md` + `_core/approval_matrix.md`.
- **Decision-grade output needs org tailoring first.** Every reference figure ships tagged `sample | starter | illustrative | placeholder`. An operator runs the interactive `tailoring/` interview (terminal TUI) to produce an `overlays/org/<org_id>/` overlay before output is operational; final-marked and period-grade workflows **fail closed** on missing required inputs or an insufficient close status (see `_core/final_marked_workflows.yaml`).

Entry point: read `src/skills/residential_multifamily/SKILL.md`, then `src/skills/residential_multifamily/_core/README.md`. Let the router load packs, overlays, and references progressively -- do not eagerly read them.

## Workflow Chains

When a task spans multiple skills, use these chains (detailed docs in `src/routing/workflows/`):

1. **Acquisition Pipeline**: sourcing -> quick-screen -> [KEEP] -> om-reverse -> rent-roll-analyzer -> underwriting-engine -> sensitivity -> ic-memo -> loi -> psa-redline -> dd-command-center -> close
2. **Capital Stack**: underwriting-engine -> loan-sizing -> mezz-pref -> jv-waterfall -> capital-stack-optimizer -> refi-decision (at maturity)
3. **Hold Period**: annual-budget -> performance-dashboard -> capex/lease-compliance/delinquency-workout/retention-engine -> noi-sprint (if needed)
4. **Disposition**: performance-dashboard -> disposition-strategy -> [SELL] disposition-prep -> 1031-exchange | [HOLD] refi-decision | [REFI] loan-sizing
5. **Development**: land-residual + entitlement -> dev-proforma -> construction-budget -> loan-sizing -> capital-stack -> ic-memo -> lease-up-war-room -> refi-decision
6. **Fund Management**: fund-formation -> pitch-deck -> capital-raise -> portfolio-allocator -> [deploy via acquisition pipeline] -> quarterly-update + performance-attribution

## Skill Locations

All skills: `src/skills/<slug>/SKILL.md`
Reference files: `src/skills/<slug>/references/`
Commands: `src/commands/` (shared orchestration commands only -- each skill is invoked directly via `/<slug>`, not a per-skill command file)
Workflow docs: `src/routing/workflows/`
Registry: `registry.yaml` (repo root)
