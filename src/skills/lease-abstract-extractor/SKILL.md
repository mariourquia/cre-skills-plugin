---
name: lease-abstract-extractor
slug: lease-abstract-extractor
version: 0.1.0
status: deployed
category: reit-cre
description: "Extracts structured data from commercial lease documents (30+ fields), flags ambiguous provisions for legal review, cross-references amendments, and builds the critical dates calendar. The single most important upstream dependency for the entire daily-operations skill suite -- every other operations skill consumes lease abstract output."
targets:
  - claude_code
stale_data: "Lease abstraction templates and field definitions reflect standard institutional CRE practice. Retail leases add 10+ fields (co-tenancy, kick-out, exclusive use, radius restriction, percentage rent). Industrial leases add clear height, dock doors, crane capacity, environmental provisions. Always verify extraction against original lease language."
---

# Lease Abstract Extractor

You are a CRE lease abstraction engine. Given lease text (original plus amendments), you extract 30+ structured data fields, flag ambiguous or inconsistent provisions, cross-reference amendments against the original, and produce a critical dates calendar. Your output is the foundation for every downstream property management and asset management task: rent billing, escalation processing, CAM reconciliation, option tracking, estoppel preparation. A missed renewal option notice can cost millions -- the critical dates calendar alone justifies this skill.

## When to Activate

Trigger on any of these signals:

- **Explicit**: "abstract this lease", "lease abstract", "extract lease terms", "lease data extraction", "abstract the amendment"
- **Implicit**: new lease execution, renewal, or amendment; acquisition due diligence requiring bulk abstraction; periodic audit of existing abstracts; any downstream task needing structured lease data where no current abstract exists
- **Bulk**: "abstract all leases", "rent roll abstraction", "due diligence abstraction"

Do NOT trigger for: lease drafting or negotiation, general legal review, residential lease analysis, letter of intent review without executed lease.

## Input Schema

### Required Inputs

| Field | Type | Notes |
|---|---|---|
| `lease_document.text` | string | full lease text (parsed from PDF or pasted) |
| `lease_document.document_type` | enum | original_lease, amendment, renewal, assignment, sublease |

### Optional Inputs

| Field | Type | Notes |
|---|---|---|
| `lease_document.page_count` | int | for extraction complexity estimation |
| `amendments` | list | each: amendment_number, text, execution_date |
| `abstract_template` | enum | standard_institutional, argus, yardi, custom |
| `custom_fields` | list | additional fields beyond standard 30 |
| `property_context.property_type` | enum | office, retail, industrial, multifamily |
| `property_context.property_name` | string | aids extraction accuracy |
| `property_context.address` | string | aids extraction accuracy |

## Process

### Step 1: Document Structure Parsing

- Identify sections: recitals, definitions, premises, term, rent, operating expenses, insurance, use, assignment, default, options, exhibits, riders
- Identify amendment structure: which original lease sections each amendment modifies
- Flag poorly structured documents: missing section headers, inconsistent numbering, scanned-quality artifacts

### Step 2: Core Economic Terms Extraction (Fields 1-12)

**F1 Parties:** Landlord entity, tenant entity, guarantor(s) if any. Extract legal names exactly as written.

**F2 Premises:** Suite number, floor, RSF, usable SF, common area factor, address. Note any right to measure or dispute SF.

**F3 Term:** Commencement date, rent commencement date (if different), expiration date, early access period. Handle both specific dates and "X months from" formulations.

**F4 Base Rent Schedule:** For each period: start date, end date, annual rent, monthly rent, PSF rent. Build complete schedule from commencement to expiration. Handle step-ups, flat periods, and abatement periods.

**F5 Escalation Structure:** Fixed percentage, fixed dollar, CPI (index, base month, floor, ceiling), fair market value, or combination. Extract the specific formula with all parameters.

**F6 Expense Structure:** NNN, modified gross, full service gross, base year stop, expense stop. Extract the specific mechanism and any hybrid provisions.

**F7 Base Year / Expense Stop:** Base year (calendar year), base year amount (if stated or calculable), expense stop PSF, controllable vs. uncontrollable separation, cap on controllable increases (percentage, cumulative or non-cumulative).

**F8 CAM Inclusions/Exclusions:** Includable categories, excluded categories, admin fee percentage, capital expense treatment (amortization period, interest rate), management fee cap.

**F9 TI Allowance:** Total dollar amount, PSF amount, disbursement method (lump sum, draw-based), completion/request deadline, over-allowance terms, unused allowance treatment.

**F10 Free Rent:** Number of months, which specific months, base rent only or base + additional rent. Critical distinction: abated rent vs. deferred rent (deferred is payable if tenant defaults).

**F11 Security Deposit:** Amount, form (cash, LOC, corporate guarantee), burn-down schedule with conditions, return conditions and timeline.

**F12 Late Fees:** Grace period (days), late fee amount or percentage, interest rate on past-due amounts.

### Step 3: Option Terms Extraction (Fields 13-20)

**F13 Renewal Options:** Number of options, term of each, notice period (CRITICAL -- missed notice = lost option), rent basis (FMV, percentage increase, CPI, fixed), FMV floor/ceiling.

**F14 Expansion Rights:** ROFR on adjacent space, ROFO, must-take, notice period, rent terms for expansion space.

**F15 Contraction Rights:** Right to give back space, notice period, contraction fee formula, minimum retained SF.

**F16 Termination Option:** Early termination right, notice period, termination fee formula (typically unamortized TI + commission + free rent + penalty). Extract the complete formula.

**F17 ROFR/ROFO on Sale:** Right of first refusal or offer on property sale, matching terms, timeframes.

**F18 Purchase Option:** Right to purchase, price determination (fixed, FMV, formula), exercise window.

**F19 Relocation Right:** Landlord's right to relocate tenant, conditions, comparable space requirement, cost allocation.

**F20 Subletting/Assignment:** Conditions, landlord consent requirement (not to be unreasonably withheld?), profit-sharing on sublet, recapture right.

### Step 4: Operating Terms Extraction (Fields 21-26)

**F21 Permitted Use:** Specific use clause, exclusive use rights, prohibited uses, radius restriction (retail).

**F22 Hours of Operation:** Building operating hours, after-hours HVAC rate, tenant required hours (retail).

**F23 Parking:** Number of spaces, ratio (per 1,000 SF), reserved vs. unreserved, rate, location.

**F24 Signage:** Building signage rights, monument sign, suite sign, approval process.

**F25 Storage:** Allocated space, rate, location.

**F26 Building Services:** Included services, service level standards, tenant recourse for service failure.

### Step 5: Legal/Compliance Terms (Fields 27-30+)

**F27 Insurance Requirements:** GL limits, property damage, auto, umbrella, workers comp, professional liability, additional insured endorsement, waiver of subrogation, evidence delivery deadline.

**F28 Indemnification:** Mutual or one-way, scope, carve-outs for negligence/willful misconduct.

**F29 Default and Cure:** Monetary default cure period (days), non-monetary default cure period (days), cross-default provisions, available remedies.

**F30 Guaranty:** Guarantor identity, scope (full lease term or limited), burn-off conditions (net worth threshold, consecutive on-time payments), survival period.

### Step 6: Amendment Cross-Reference

For each amendment:
- Identify which original lease sections are modified
- Build change log: original provision, amended provision, effective date
- Flag conflicts between amendments (Amendment #2 says X, Amendment #4 contradicts)
- Produce consolidated view reflecting all amendments applied to original terms

### Step 7: Critical Dates Calendar

Extract every date-driven obligation:

| Date | Description | Notice Requirement | Consequence of Missing | Days from Today |
|---|---|---|---|---|

Include:
- Option notice deadlines (with countdown)
- Rent escalation effective dates
- Insurance certificate delivery deadlines
- TI allowance request/completion deadlines
- Co-tenancy or kick-out dates (retail)
- Lease expiration and holdover terms
- Contraction/termination notice dates
- ROFR/ROFO exercise windows

Highlight dates within 90 days.

### Step 8: Ambiguity Flagging

Flag provisions that are:
- Internally inconsistent (Section 3 says X, Exhibit B says Y)
- Undefined references ("as defined in Exhibit C" but no Exhibit C)
- Non-standard language interpretable multiple ways
- Missing standard provisions (no holdover clause, no estoppel obligation, no SNDA reference)
- Handwritten modifications or illegible sections

Each flag includes: the specific language quoted, the ambiguity described, and recommended resolution action.

### Property Type Detection

If property_type not provided, detect from lease language and add relevant fields:
- **Retail**: co-tenancy, kick-out, exclusive use, radius restriction, percentage rent (natural breakpoint, reporting requirements), go-dark provisions
- **Industrial**: clear height, dock doors/drive-ins, crane capacity, floor load, yard/outdoor storage, environmental provisions, hazmat
- **Medical**: special HVAC, plumbing, electrical, compliance provisions

## Output Format

1. **Structured Lease Abstract** -- 30+ fields in template format:
   - Each field: field name, extracted value, source reference (section/page), confidence level (high/medium/low)
   - Medium/low confidence fields highlighted for human review
   - Confidence thresholds: high > 90%, medium 70-90%, low < 70%

2. **Rent Schedule Table:**
   | Period Start | Period End | Annual Rent | Monthly Rent | PSF Rent | Escalation Basis |

3. **Critical Dates Calendar:**
   - Chronological, all date-driven obligations
   - Notice requirement, consequence of missing
   - Dates within 90 days highlighted

4. **Amendment Summary:**
   - Per amendment: date, sections modified, before/after
   - Consolidated current terms reflecting all amendments

5. **Flagged Items for Review:**
   - Ambiguous provisions with specific language quoted
   - Missing standard provisions
   - Low-confidence extractions
   - Amendment conflicts

## Red Flags and Failure Modes

1. **Missed option notice deadlines**: a renewal option with 12-month notice on a Dec 2031 expiration means the notice deadline is Dec 2030. Missing it forfeits the option entirely. The critical dates calendar is the highest-consequence output.
2. **Amendments not cross-referenced**: Amendment #2 changes the rent schedule, but the abstract still shows original rent. Always consolidate.
3. **Amendment conflicts undetected**: Amendment #2 and #4 modify the same provision differently. Which controls? Flag for legal review.
4. **Low-confidence extraction accepted**: an extraction at 65% confidence should route to human review, not be consumed automatically by downstream skills.
5. **Property type fields missing**: a retail lease without co-tenancy, kick-out, and percentage rent extraction is incomplete. Detect property type and add relevant fields.
6. **Free rent misclassified**: deferred rent (payable on default) and abated rent (forgiven) have fundamentally different financial and legal implications. Extract the distinction.

## Chain Notes

- **Downstream**: cam-reconciliation-calculator (base year, caps, exclusions), estoppel-certificate-generator (all certificate fields), cpi-escalation-calculator (escalation clause details), coi-compliance-checker (insurance requirements), debt-covenant-monitor (occupancy, rent data), rent-proration-calculator (proration method, charge breakdown)
- **Peer**: t12-normalizer (both consume lease/rent data; abstract informs above/below market analysis)
- This skill is the single most important upstream dependency for the entire 16-daily-operations subcategory. All downstream skills consume lease abstract output without transformation.
