# LP Data Request Templates
# Reference data for lp-data-request-generator skill
# Provides complete line-item templates for each request type

---

## Template 1: Initial Due Diligence (New GP Relationship)

### Section 1: Organization and Team (ORG)

| ID | Item | Format | Priority | Red Flag Trigger |
|---|---|---|---|---|
| ORG-01 | Firm overview: history, founding date, ownership structure | Narrative + org chart (PDF) | Critical | Founded <5 years ago with no principals having 10+ year CRE track record |
| ORG-02 | Organizational chart including all investment, asset management, and IR staff | PDF | Critical | Unclear reporting lines or missing key functions |
| ORG-03 | Key person bios: education, career history, tenure at firm, personal track record | PDF per person | Critical | Principal tenure <3 years or significant career gaps |
| ORG-04 | GP commitment to fund: amount, form (cash vs fee waiver), source | Letter + evidence | Critical | GP commitment <1% of fund or 100% fee waiver |
| ORG-05 | Employee turnover: departures and hires by year for prior 3 years | Spreadsheet | Critical | Turnover >20% in any year or departure of senior investment staff |
| ORG-06 | AUM growth trajectory: AUM by year for prior 5 years | Spreadsheet | Important | AUM growth >50% in 24 months (asset-gathering signal) |
| ORG-07 | Compensation philosophy: how are principals and investment staff compensated | Narrative | Important | No carried interest participation for investment professionals |
| ORG-08 | Succession plan: what happens if a founder departs | Narrative | Important | No written succession plan |
| ORG-09 | Regulatory registrations: SEC, state registrations, any exemptions | Copies of registrations | Critical | Reliance on exempt reporting adviser status for large AUM |
| ORG-10 | Compliance program: CCO identity, compliance testing cadence, training | Summary + sample compliance manual | Important | No dedicated CCO or CCO is dual-hatted with investment role |
| ORG-11 | Litigation and regulatory history: all actions, settled or pending, prior 10 years | Narrative with case details | Critical | Any pending litigation by investors or regulatory enforcement |
| ORG-12 | Insurance: E&O, D&O, cyber, fidelity bond -- coverage amounts and carriers | Certificate summaries | Important | E&O coverage <$5M for funds >$500M |
| ORG-13 | Business continuity plan: disaster recovery, key systems, backup procedures | Summary | Supplemental | No documented BCP |
| ORG-14 | Affiliated entities and potential conflicts: list all GP-affiliated entities | Spreadsheet | Critical | Undisclosed affiliated service providers |
| ORG-15 | Political contributions policy and PAC activity (pay-to-play compliance) | Policy document | Important | No formal policy for firms managing public pension capital |

### Section 2: Track Record (PERF)

| ID | Item | Format | Priority | Red Flag Trigger |
|---|---|---|---|---|
| PERF-01 | Fund-level returns by vintage: gross IRR, net IRR, DPI, TVPI, RVPI (quarterly since inception) | Spreadsheet (ILPA template) | Critical | Missing any metric or only gross returns provided |
| PERF-02 | Deal-level returns for all realized investments: property name, type, market, entry price, exit price, hold period, MOIC, IRR | Spreadsheet | Critical | Refusal to provide deal-level data |
| PERF-03 | Deal-level data for unrealized investments: property name, type, market, entry basis, current NAV, hold period, strategy status | Spreadsheet | Critical | Missing current NAV or strategy status |
| PERF-04 | Return attribution: decomposition into income, appreciation, leverage for each fund | Spreadsheet | Important | Unable or unwilling to decompose returns |
| PERF-05 | Subscription credit facility usage: duration, utilization, IRR impact quantification | Spreadsheet + narrative | Critical | Sub-line used >12 months and IRR impact not disclosed |
| PERF-06 | Loss schedule: all investments returning <1.0x MOIC with explanation | Spreadsheet + narrative | Critical | Loss ratio >25% of invested capital |
| PERF-07 | Benchmark comparison: fund returns vs Cambridge Associates vintage cohort | Spreadsheet | Critical | Fund below vintage median on net basis |
| PERF-08 | Co-investment track record: returns on co-invest deals vs main fund deals | Spreadsheet | Important | Co-invest returns significantly differ from main fund |
| PERF-09 | Leverage history: average LTV by fund, maximum LTV, current LTV | Spreadsheet | Important | Maximum LTV exceeding stated policy by >10% |
| PERF-10 | Valuation methodology: GAAP compliance, appraiser identity, appraisal cadence | Policy document | Critical | Non-independent appraiser or appraisals less frequent than annual |

### Section 3: Fund Terms (TERMS)

| ID | Item | Format | Priority | Red Flag Trigger |
|---|---|---|---|---|
| TERMS-01 | Draft or final PPM | PDF | Critical | No PPM available pre-commitment |
| TERMS-02 | Draft or final LPA | PDF | Critical | No LPA available pre-commitment |
| TERMS-03 | Management fee schedule: rate, basis, step-down, offset provisions | Summary spreadsheet | Critical | Fee above 75th percentile for strategy |
| TERMS-04 | Carry mechanics: rate, hurdle, catch-up, waterfall type, clawback | Summary spreadsheet | Critical | 100% GP catch-up with American waterfall |
| TERMS-05 | GP commitment details: amount, form, timing, co-invest alongside | Detail letter | Critical | GP commitment <1% or 100% fee waiver |
| TERMS-06 | Fee offset schedule with calculation methodology and examples | Spreadsheet | Important | Fee offset <80% |
| TERMS-07 | Side letter policy: what provisions are negotiable, MFN availability | Narrative | Important | No MFN offered to similarly-sized LPs |
| TERMS-08 | Fund expenses: organizational cap, operating expenses, broken-deal cost policy | LPA excerpt | Important | No organizational expense cap |
| TERMS-09 | Key person clause: named persons, trigger, consequence, cure period | LPA excerpt | Critical | Key person clause missing or with >90 day cure |
| TERMS-10 | LP consent rights: what actions require LP vote, what threshold | LPA excerpt | Important | No LP consent on extensions or related-party transactions |
| TERMS-11 | LPAC provisions: composition, rights, meeting frequency, conflict review | LPA excerpt | Important | No LPAC or LPAC with no meaningful rights |

### Section 4: References (REF)

| ID | Item | Format | Priority | Red Flag Trigger |
|---|---|---|---|---|
| REF-01 | 5 current LP references (include at least 1 from underperforming fund) | Contact list | Critical | Unwilling to provide references from underperforming fund |
| REF-02 | 2 non-investor references (lender, broker, property manager, counsel) | Contact list | Important | No non-investor references available |
| REF-03 | Former employee reference availability (at least 1 senior departure) | Contact list | Supplemental | Refuses to facilitate former employee contact |

---

## Template 2: Quarterly Monitoring

### Standard Quarterly Items

| ID | Item | Format | Priority | Delivery Standard |
|---|---|---|---|---|
| QTR-01 | Capital account statement (contributions, distributions, NAV, unreturned capital) | ILPA template spreadsheet | Critical | 60 days post quarter-end |
| QTR-02 | Fund-level returns: gross IRR, net IRR, DPI, TVPI, RVPI | ILPA template spreadsheet | Critical | 60 days |
| QTR-03 | NAV bridge: beginning NAV, contributions, distributions, income, appreciation, fees, ending NAV | Spreadsheet | Critical | 60 days |
| QTR-04 | Deal-level update: status, occupancy, NOI, current NAV, key events per asset | Spreadsheet + narrative | Critical | 60 days |
| QTR-05 | Deployment summary: capital invested, capital committed, pipeline, pacing vs plan | Spreadsheet | Important | 60 days |
| QTR-06 | Fee reconciliation: management fee charged, carry accrued, other fees | Spreadsheet | Important | 60 days |
| QTR-07 | GP letter: market commentary, portfolio update, key events, outlook | Narrative (PDF) | Important | 60 days |
| QTR-08 | Compliance certification: no material breaches of LPA investment guidelines | Letter | Important | 60 days |
| QTR-09 | Key person status: confirmation all key persons remain and devote required time | Letter | Critical | 60 days |
| QTR-10 | Sub-line usage update: balance outstanding, utilization rate, maturity | Spreadsheet | Important | 60 days |

---

## Template 3: Annual Review

All quarterly items PLUS:

| ID | Item | Format | Priority | Delivery Standard |
|---|---|---|---|---|
| ANN-01 | Audited financial statements (fund-level) | PDF | Critical | 120 days post year-end |
| ANN-02 | Audit opinion: unqualified, qualified, or adverse | PDF (included in audit) | Critical | 120 days |
| ANN-03 | Reconciliation: Q4 quarterly data vs audited year-end figures | Spreadsheet | Important | 120 days |
| ANN-04 | Annual governance report: LPAC meetings held, conflict disclosures, LP votes | Narrative | Important | 120 days |
| ANN-05 | Valuation summary: methodology, appraiser, cap rates used, comparables | PDF | Critical | 120 days |
| ANN-06 | Fee reconciliation: annual management fee, carry, offsets, expenses | Spreadsheet | Critical | 120 days |
| ANN-07 | Tax package: K-1 (or equivalent), tax elections, UBTI analysis | Tax docs | Critical | March 15 (US partnerships) |
| ANN-08 | Updated Form ADV Part 2A | PDF | Important | Within 90 days of annual amendment |
| ANN-09 | Insurance renewal confirmations | Certificate | Supplemental | Upon renewal |
| ANN-10 | ESG/GRESB update: scores, initiatives, climate risk | Report | Supplemental | 120 days |

---

## Template 4: Re-Up Evaluation

| ID | Item | Format | Priority | Red Flag Trigger |
|---|---|---|---|---|
| REUP-01 | Updated track record: current fund + all prior funds, net returns, deal-level | Spreadsheet (ILPA template) | Critical | Performance declined from prior evaluation |
| REUP-02 | Next fund PPM and draft LPA | PDF | Critical | Terms worsened from current fund |
| REUP-03 | Terms comparison: current fund vs next fund, item by item | Spreadsheet | Critical | Any material term worsened without performance justification |
| REUP-04 | Team update: departures, hires, role changes since last DD | Narrative + updated org chart | Critical | Key person departure not previously disclosed |
| REUP-05 | Strategy evolution: how has strategy changed from current to next fund | Narrative | Critical | Material strategy shift without LP consultation |
| REUP-06 | Fund size justification: why is next fund larger/smaller, opportunity set analysis | Narrative | Important | Fund size increase >50% without proportional opportunity set expansion |
| REUP-07 | Reference list update: 5 current fund LP references | Contact list | Important | All references are re-upping LPs (no critical perspective) |
| REUP-08 | Current fund exit pipeline and projected remaining distributions | Spreadsheet | Important | No clear exit pipeline for unrealized investments |
| REUP-09 | Co-invest allocation data: how were co-invest opportunities distributed | Spreadsheet | Supplemental | LP excluded from co-invest despite commitment size |
| REUP-10 | Competitive landscape: how does GP position itself vs peers | Narrative | Supplemental | GP unable to articulate differentiation |

---

## Response Tracking Template

Use this structure to track GP responses to data requests:

```
| Item ID | Description | Date Requested | Date Received | Status | Quality |
|---------|-------------|---------------|---------------|--------|---------|
| ORG-01 | Firm overview | YYYY-MM-DD | YYYY-MM-DD or PENDING | Complete/Partial/Declined | Adequate/Insufficient |
```

Status definitions:
- **Complete**: All requested data provided in requested format
- **Partial**: Some data provided but missing elements
- **Declined**: GP declined to provide
- **Pending**: Not yet received, within deadline
- **Overdue**: Past deadline, not received

Quality definitions:
- **Adequate**: Data is sufficient for analytical purpose
- **Insufficient**: Data provided but lacks detail or format needed for analysis
- **Suspicious**: Data appears inconsistent, contradictory, or selectively presented
