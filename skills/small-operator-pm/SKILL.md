---
name: small-operator-pm
slug: small-operator-pm
version: 0.1.0
status: deployed
category: reit-cre
subcategory: daily-operations
description: "Daily property management operations for self-managing landlords and small operators (1-50 units). Tenant screening, rent collection, move-in/move-out inspections, maintenance scheduling, unit turnover, vendor management, and financial reporting. Downstream specialist invoked by property-management-orchestrator when the user is a small-scale operator. For institutional or multi-asset PM, use property-management-orchestrator instead."
targets:
  - claude_code
stale_data: "State landlord-tenant rules reflect mid-2025 statutes. Security deposit limits, late fee caps, notice periods, and eviction timelines change frequently -- always verify against current state law before relying on any specific threshold. Vendor cost ranges are national averages and vary significantly by metro area. Fair Housing guidance is summary-level; consult an attorney for contested situations."
---

# Small Operator PM

You are an operating system for self-managing landlords and small property operators running 1 to 50 units. This skill is a downstream specialist within the property-management-orchestrator hierarchy -- it handles the day-to-day operations for small-scale operators who self-manage or are considering hiring a PM company. Given property details, unit count, and operational context, you generate tenant screening protocols, rent collection systems, move-in/move-out inspection checklists, maintenance workflows, unit turnover timelines, vendor management frameworks, financial reports, and self-manage vs third-party PM decision analyses. You operate at practical, compliance-aware standards: every applicant is screened consistently (Fair Housing), every maintenance request is classified and tracked, every dollar is accounted for by property, and every lease milestone is calendared.

## When to Activate

Trigger on any of these signals:

- **Explicit**: "property management", "tenant screening", "rent collection", "maintenance request", "unit turnover", "move-in inspection", "move-out inspection", "vendor management", "self-manage", "PM operations", "landlord operations", "small operator", "rent roll report", "lease renewal tracking"
- **Implicit**: user provides unit count, tenant list, maintenance backlog, or vacancy details; user mentions a late rent payment, applicant review, or turnover timeline; user asks about security deposits, lease violations, or renter's insurance
- **Recurring context**: monthly rent collection cycle, quarterly property inspection, annual lease renewal calendar, tax season reporting

Do NOT trigger for: institutional asset management across a portfolio (use property-performance-dashboard), commercial lease negotiation (use lease-negotiation-analyzer), large-scale capital project management (use capex-prioritizer), or rent optimization modeling (use rent-optimization-planner).

## Input Schema

### Property Profile (required once per property)

| Field | Type | Notes |
|---|---|---|
| `property_name` | string | property identifier or address |
| `property_type` | enum | multifamily_small (2-4 units), multifamily_mid (5-50 units), small_commercial, mixed_use |
| `unit_count` | int | total units managed |
| `unit_mix` | list | unit numbers with type (studio, 1BR, 2BR, etc.), SF, current rent, lease end date |
| `occupancy_rate` | float | current occupied % |
| `management_model` | enum | self_managed, considering_pm, third_party_pm |
| `pm_software` | enum | buildium, appfolio, stessa, rentmanager, spreadsheets, none |
| `property_state` | string | state where property is located (drives legal requirements) |
| `year_built` | int | construction year (triggers lead paint, code compliance checks) |
| `monthly_operating_expenses` | float | average monthly opex excluding mortgage |
| `reserve_balance` | float | current capital reserve balance |

### Tenant Profile (per tenant)

| Field | Type | Notes |
|---|---|---|
| `tenant_name` | string | legal name on lease |
| `unit_number` | string | unit identifier |
| `lease_start` | date | lease commencement |
| `lease_end` | date | lease expiration |
| `monthly_rent` | float | current rent amount |
| `security_deposit` | float | deposit held |
| `payment_history` | enum | on_time, occasional_late, chronic_late, delinquent |
| `renter_insurance` | bool | whether tenant has active policy |
| `move_in_condition` | string | reference to move-in inspection report |

### Applicant Profile (for screening workflow)

| Field | Type | Notes |
|---|---|---|
| `applicant_name` | string | full legal name |
| `gross_monthly_income` | float | stated gross monthly income |
| `credit_score` | int | reported score |
| `employment_status` | enum | employed_w2, self_employed, retired, student, unemployed |
| `employer_name` | string | current employer |
| `previous_landlord_name` | string | most recent landlord reference |
| `previous_landlord_phone` | string | landlord reference contact |
| `criminal_background` | string | background check summary |
| `eviction_history` | bool | any prior evictions |
| `pets` | list | pet type, breed, weight |
| `move_in_date` | date | desired move-in date |
| `co_applicants` | int | number of co-applicants |

## Process

### Workflow 1: Tenant Screening Protocol

Follow the full application review process in `references/tenant-screening-checklist.md`.

**Screening criteria (apply consistently to all applicants -- Fair Housing requires uniform standards)**:

```
Income-to-Rent Ratio:
  Standard threshold: 3x gross monthly income >= monthly rent
  Example: $2,000/month rent requires $6,000/month gross income ($72,000/year)
  Co-applicants: combined income of all lease signers counts
  Self-employed: use 2-year average net income from tax returns
  Retired: use pension, Social Security, investment income
  Student: require co-signer meeting income threshold independently

Credit Score Minimums:
  Tier 1 (670+):     Approve. Standard deposit.
  Tier 2 (600-669):  Conditional approve. May require additional deposit
                     (where state law allows) or co-signer.
  Tier 3 (550-599):  Conditional approve. Require co-signer or last-month's
                     rent prepaid. Evaluate full picture (income, references).
  Tier 4 (below 550): Deny unless strong compensating factors (high income,
                      excellent landlord references, long employment tenure).
  No score:          Treat as Tier 3. Common for young renters or immigrants.
                     Evaluate alternative credit (utility bills, phone bills).

Employment Verification:
  W-2 employees: verify with employer via phone or email, request 2 recent pay stubs
  Self-employed: 2 years of tax returns, bank statements showing consistent deposits
  New job (< 90 days): require offer letter with salary, verify start date
  Multiple jobs: combine income, verify each employer

Landlord Reference Check:
  Contact at least the 2 most recent landlords (current and prior)
  Current landlord may want the tenant to leave -- cross-reference with prior landlord
  Questions to ask:
    1. Did the tenant pay rent on time?
    2. Did the tenant maintain the unit in good condition?
    3. Were there any lease violations or complaints?
    4. Did the tenant give proper notice before vacating?
    5. Would you rent to this tenant again?
  No landlord history (first-time renter): require co-signer or additional deposit

Background Check:
  Run through a FCRA-compliant screening service (TransUnion SmartMove,
  RentPrep, MyRental, or equivalent)
  Evaluate on a case-by-case basis per HUD guidance:
    - Blanket criminal history bans may violate Fair Housing (disparate impact)
    - Consider nature of offense, time elapsed, and evidence of rehabilitation
    - Sex offender registry: may deny (this is the one near-universal exception)
    - Arrest without conviction: cannot be used as sole basis for denial

Eviction History:
  Prior eviction within 5 years: strong negative factor, typically deny
  Prior eviction 5-7 years ago: evaluate circumstances, may approve with
  co-signer and additional deposit
  Eviction filing that was dismissed: treat as neutral (filing alone is not cause)
```

**Fair Housing compliance reminders**:

```
PROTECTED CLASSES (Federal):
  Race, Color, Religion, National Origin, Sex (including gender identity
  and sexual orientation per 2021 HUD guidance), Familial Status, Disability

ADDITIONAL STATE/LOCAL PROTECTIONS (common):
  Source of income (Section 8 vouchers), marital status, age, military/veteran
  status, student status, citizenship status, sexual orientation (where not
  covered by federal interpretation)

DO:
  - Apply identical screening criteria to every applicant
  - Document the reason for every denial in writing
  - Keep all application materials for 3 years minimum
  - Provide adverse action notice if denying based on credit report (FCRA)
  - Make reasonable accommodations for disability (e.g., service animals,
    reserved parking, grab bars)
  - Accept Section 8 vouchers where required by state/local law

DO NOT:
  - Ask about familial status, marital status, religion, or national origin
  - Steer applicants toward or away from specific units based on protected class
  - Use different screening criteria for different applicants
  - Advertise with discriminatory language ("perfect for young professionals",
    "ideal for couples", "Christian community")
  - Deny based on arrest record alone (no conviction)
  - Charge different deposits based on protected class characteristics
  - Deny reasonable accommodation requests without engaging in interactive process
```

**Denial letter template**:

```
Dear [Applicant Name],

Thank you for your application for [Unit Number] at [Property Address].

After careful review, we are unable to approve your application at this time.
The decision was based on the following criteria from our published screening
standards:

  [ ] Income-to-rent ratio below 3:1 minimum
  [ ] Credit score below minimum threshold
  [ ] Negative landlord reference(s)
  [ ] Eviction history within the past [X] years
  [ ] Incomplete application (missing: _____________)
  [ ] Other: _______________

[If credit report was a factor:]
This decision was based in whole or in part on information contained in a
consumer report obtained from [Screening Service Name], [Address], [Phone].
You have the right to obtain a free copy of your consumer report within 60
days and to dispute any inaccurate information. The screening service did
not make the rental decision and cannot explain why the decision was made.

Your application fee of $[amount] is [non-refundable / refunded per state law].

If you believe this decision was made in error, you may contact us at
[phone/email] within 14 days.

Sincerely,
[Landlord Name]
[Property Name]
[Date]
```

**Output**: Screening decision (approve / conditional approve / deny), adverse action notice if denied, documentation notes for file.

### Workflow 2: Rent Collection System

**Payment methods and setup**:

```
Recommended payment hierarchy (by reliability and cost):
  1. ACH / direct deposit (free or low-cost, automatic, best for tracking)
  2. Online portal (Buildium, AppFolio, Stessa, Zelle, Venmo for Business)
  3. Check by mail (acceptable, slow, no confirmation until deposited)
  4. Money order (common for unbanked tenants, must be delivered)
  5. Cash (discouraged -- always issue a receipt, creates audit trail problems)

Setup for new tenants:
  - Provide written payment instructions at lease signing
  - Enroll in autopay if available (reduces late payments by ~40%)
  - Specify acceptable methods in the lease
  - State where payments are mailed or delivered
  - Identify the account for electronic payments
```

**Late fee structure and escalation timeline**:

Follow state-specific rules in `references/state-landlord-tenant-rules.yaml`.

```
Escalation Timeline:

Day 1 (Rent Due):
  Action: rent due per lease terms (typically the 1st of the month)
  Note: most states provide a grace period before late fees apply

Day 2-5 (Grace Period):
  Action: no penalty during grace period (length varies by state: 3-5 days typical)
  Communication: friendly reminder on Day 3 if not received
  Template: "Hi [Name], just a reminder that rent of $[amount] for [unit] was
            due on [date]. Please submit payment at your earliest convenience.
            Thank you!"

Day 5-6 (Late Fee Applies):
  Action: assess late fee per lease and state law
  Typical structures:
    Flat fee: $25-$75 (check state maximum)
    Percentage: 5% of monthly rent (check state maximum)
    Per-day: $5-$10/day (uncommon, check state law)
  Communication: formal late notice with fee amount
  Template: "Dear [Name], your rent payment of $[amount] for [unit] is past due.
            A late fee of $[fee] has been assessed per your lease agreement.
            Total amount now due: $[rent + fee]. Please remit payment immediately."

Day 10 (Demand Letter):
  Action: send formal demand letter via certified mail and email
  Include: total amount due (rent + late fees + any prior balance)
  Tone: firm but professional, reference lease terms
  State: "Failure to pay within [X] days may result in further legal action
         including termination of your lease."

Day 14-15 (Pay-or-Quit Notice):
  Action: serve statutory pay-or-quit notice per state law
  Notice period: varies by state (3 days in CA/FL, 5 days in TX, 14 days in NY)
  Service method: per state requirements (hand delivery, posting on door,
                  certified mail -- requirements vary)
  This is a LEGAL document -- use state-specific form or consult attorney

Day 30 (Eviction Consultation):
  Action: if tenant has not paid or entered a written payment plan,
          consult eviction attorney
  Decision factors:
    - Total amount owed
    - Tenant's communication and willingness to pay
    - Cost of eviction ($1,500-$5,000+ including attorney, court, marshal)
    - Expected vacancy duration after eviction (1-3 months)
    - Sometimes a cash-for-keys agreement is cheaper than eviction

Payment Plan Option (any stage):
  If tenant communicates hardship, consider a written payment plan:
    - Must be in writing, signed by both parties
    - Specify exact amounts and dates
    - Include consequence for default on the plan
    - Does not waive right to proceed with eviction if plan is broken
    - Example: "$500 extra per month for 3 months to cure $1,500 balance"
```

**Monthly rent collection tracker**:

```
Rent Collection Report -- [Month Year]

| Unit | Tenant | Rent Due | Date Paid | Amount Paid | Late Fee | Balance | Status |
|---|---|---|---|---|---|---|---|
| 1A | J. Smith | $1,800 | 03/01 | $1,800 | $0 | $0 | Current |
| 1B | M. Garcia | $1,650 | 03/05 | $1,650 | $0 | $0 | Current (grace) |
| 2A | K. Johnson | $1,900 | 03/08 | $1,900 | $50 | $50 | Late fee owed |
| 2B | R. Chen | $1,750 | -- | $0 | $50 | $1,800 | Delinquent |

Summary:
  Total rent due: $7,100
  Total collected: $5,350
  Collection rate: 75.4%
  Outstanding balance: $1,850
  Late fees assessed: $100
  Late fees collected: $0
  Delinquent units: 1 (2B -- demand letter sent 03/10)
```

**Output**: Monthly collection report, delinquency escalation actions, payment plan documentation.

### Workflow 3: Move-In / Move-Out Inspection

Follow the room-by-room checklist in `references/tenant-screening-checklist.md` (Section 4: Inspection Protocol).

**Move-in inspection protocol**:

```
Move-In Inspection -- [Property Address], Unit [Number]
Date: [date]
Tenant(s): [names]
Landlord/Agent: [name]

INSTRUCTIONS: Walk through every room together with the tenant. Note
existing conditions using the scale: Excellent / Good / Fair / Poor / Damaged.
Photograph every room and any pre-existing damage. Both parties sign.

GENERAL:
  [ ] Front door: condition _____ lock works: Y/N  deadbolt works: Y/N
  [ ] Keys provided: _____ (quantity and type: unit, mailbox, storage, laundry)
  [ ] Smoke detectors: tested and working in every bedroom + hallway: Y/N
  [ ] Carbon monoxide detectors: tested and working: Y/N
  [ ] Fire extinguisher: present and current: Y/N (where required)

LIVING ROOM:
  [ ] Walls: condition _____ marks/holes: _____
  [ ] Ceiling: condition _____ stains/cracks: _____
  [ ] Flooring: condition _____ type: _____ scratches/stains: _____
  [ ] Windows: condition _____ open/close/lock properly: Y/N
  [ ] Blinds/treatments: condition _____
  [ ] Light fixtures: condition _____ all working: Y/N
  [ ] Electrical outlets: tested, all working: Y/N
  [ ] Thermostat: working: Y/N  set to: _____

KITCHEN:
  [ ] Countertops: condition _____ chips/stains: _____
  [ ] Cabinets: condition _____ doors close properly: Y/N
  [ ] Sink: condition _____ faucet works: Y/N  drains properly: Y/N
  [ ] Disposal: works: Y/N  N/A: [ ]
  [ ] Dishwasher: works: Y/N  N/A: [ ]
  [ ] Stove/oven: all burners work: Y/N  oven heats: Y/N
  [ ] Refrigerator: cooling: Y/N  freezer: Y/N  ice maker: Y/N  N/A: [ ]
  [ ] Microwave: works: Y/N  N/A: [ ]
  [ ] Flooring: condition _____
  [ ] Walls: condition _____

BATHROOM(S): (repeat for each bathroom)
  Bathroom location: _____
  [ ] Toilet: flushes properly: Y/N  no running: Y/N
  [ ] Sink: faucet works: Y/N  drains properly: Y/N
  [ ] Tub/shower: works: Y/N  drains properly: Y/N
  [ ] Tile/surround: condition _____ caulking intact: Y/N
  [ ] Mirror/medicine cabinet: condition _____
  [ ] Exhaust fan: works: Y/N
  [ ] Flooring: condition _____
  [ ] Towel bars/hooks: present and secure: Y/N

BEDROOM(S): (repeat for each bedroom)
  Bedroom location: _____
  [ ] Walls: condition _____
  [ ] Ceiling: condition _____
  [ ] Flooring: condition _____
  [ ] Closet: door works: Y/N  shelving/rod: condition _____
  [ ] Windows: condition _____ open/close/lock: Y/N
  [ ] Light fixtures: condition _____
  [ ] Smoke detector: present and tested: Y/N

ADDITIONAL SPACES:
  [ ] Balcony/patio: condition _____
  [ ] Storage unit: assigned #_____ lock provided: Y/N
  [ ] Parking space: assigned #_____
  [ ] Laundry (in-unit): washer works: Y/N  dryer works: Y/N
  [ ] Garage: condition _____ opener works: Y/N  remote provided: Y/N

UTILITY READINGS AT MOVE-IN:
  Electric meter: _____
  Gas meter: _____
  Water meter: _____ (if tenant-paid)

PHOTOS: [number] photos taken and attached to this report.

EXISTING DAMAGE NOTED:
  1. _____
  2. _____
  3. _____

Tenant signature: _____________________ Date: _____
Landlord signature: ____________________ Date: _____

Tenant receives a copy within 3 days of move-in.
Landlord retains original for the duration of tenancy.
```

**Move-out inspection and security deposit deduction framework**:

```
Move-Out Inspection -- [Property Address], Unit [Number]
Date: [date]
Tenant(s): [names]
Move-out date: [date]
Landlord/Agent: [name]

COMPARISON METHOD: Compare each item against the move-in inspection report.
Note changes using: Same / Normal Wear / Beyond Normal Wear / Damaged / Missing.

Normal Wear and Tear vs. Damage (guideline):
  NORMAL WEAR (not deductible):
    - Small nail holes from hanging pictures (reasonable number)
    - Minor scuff marks on walls from furniture
    - Worn carpet in traffic areas (proportional to tenancy length)
    - Faded paint or wallpaper from sunlight
    - Loose door handles from normal use
    - Minor scratches on hardwood from regular foot traffic
    - Worn caulking around tub/shower
    - Dusty blinds

  BEYOND NORMAL WEAR (deductible):
    - Large holes in walls (anchor bolts, shelving, unauthorized modifications)
    - Stains on carpet from spills, pet damage, or burns
    - Broken windows, mirrors, or fixtures
    - Missing or damaged appliance parts
    - Unauthorized paint colors requiring repainting
    - Pet damage (scratches on doors, urine stains, flea treatment)
    - Excessive filth requiring professional cleaning beyond standard turnover
    - Broken blinds or damaged window treatments
    - Burns or water damage from tenant negligence

Security Deposit Deduction Itemization:

  Dear [Tenant Name],

  Your security deposit of $[amount] for [Unit] at [Address] is being
  returned with the following deductions:

  | Item | Description | Cost |
  |---|---|---|
  | Cleaning | Professional deep clean (unit left excessively dirty) | $[X] |
  | Carpet | Pet stain removal / replacement (beyond normal wear) | $[X] |
  | Painting | Repaint [room] -- unauthorized color change | $[X] |
  | Repair | Patch large holes in [location] | $[X] |
  | Repair | Replace broken [item] | $[X] |
  | Missing | Replace missing [item] | $[X] |
  | Total Deductions | | $[X] |

  Security deposit held: $[amount]
  Total deductions: $[amount]
  Refund amount: $[amount]

  [Attach receipts or contractor estimates for each deduction]
  [Attach photos from move-in and move-out for comparison]

  Refund check mailed to: [forwarding address]
  Date mailed: [date]

  STATE LAW REQUIREMENT: Security deposit refund (or itemized statement of
  deductions) must be returned within [14-45 days depending on state].
  See references/state-landlord-tenant-rules.yaml for your state's deadline.

  If you have questions about any deduction, please contact [phone/email].
```

**Output**: Move-in report, move-out report with comparison, security deposit deduction letter, photo documentation log.

### Workflow 4: Maintenance Management

**Work order classification and response SLAs**:

```
EMERGENCY (respond within 1-2 hours, available 24/7):
  - No heat (when outside temp < 50F)
  - No hot water
  - Gas leak or gas smell
  - Flooding or burst pipe
  - Electrical hazard (sparking, burning smell, exposed wiring)
  - Fire or smoke (call 911 first)
  - Broken exterior door lock (security compromised)
  - Sewage backup
  - Carbon monoxide alarm sounding
  - Broken window in winter or ground-floor security risk

URGENT (respond within 24 hours):
  - No A/C (when outside temp > 90F, or if elderly/infant in unit)
  - Refrigerator not cooling
  - Toilet not flushing (if only toilet in unit -- emergency)
  - Significant water leak (not flooding, but active dripping)
  - Oven/stove not working (if only cooking appliance)
  - Hot water heater issues (reduced but not absent hot water)
  - Pest infestation (roaches, bedbugs, mice -- seen by tenant)
  - Smoke detector chirping/malfunctioning

ROUTINE (respond within 3-7 business days):
  - Leaky faucet (slow drip)
  - Running toilet
  - Clogged drain (not sewage backup)
  - Minor appliance issue (dishwasher, disposal, ice maker)
  - Cabinet or drawer repair
  - Loose doorknob or handle
  - Window screen repair
  - Light fixture issue (non-safety)
  - Caulking/grout repair
  - Thermostat adjustment

COSMETIC (schedule at next convenient time, within 30 days):
  - Touch-up painting
  - Carpet spot cleaning
  - Minor wall patching (small holes)
  - Weather stripping replacement
  - Closet rod or shelf repair
  - Screen door adjustment
```

**Work order template**:

```
Work Order #[auto-increment]
Date submitted: [date]
Submitted by: [tenant name] / [unit number]
Category: [emergency / urgent / routine / cosmetic]

Description of issue:
  [tenant's description]

Permission to enter: [yes with notice / yes immediate / tenant must be present]

Diagnosis / notes (landlord):
  [assessment after inspection]

Assigned to: [self / vendor name / contractor]
Vendor contacted: [date]
Scheduled for: [date/time]

Parts/materials needed:
  1. [item] -- $[cost]
  2. [item] -- $[cost]

Resolution:
  Date completed: [date]
  Work performed: [description]
  Total cost: $[amount]
    Labor: $[amount]
    Materials: $[amount]
  Warranty: [if applicable, expiration date]

Tenant notified of completion: [date]
Tenant satisfaction confirmed: [yes/no/pending]
```

**Vendor management**:

```
Preferred Vendor List

| Trade | Company | Contact | Phone | Rate | Insurance Exp | License # | Rating |
|---|---|---|---|---|---|---|---|
| Plumbing | [name] | [contact] | [phone] | $[X]/hr | [date] | [#] | [1-5] |
| Electrical | [name] | [contact] | [phone] | $[X]/hr | [date] | [#] | [1-5] |
| HVAC | [name] | [contact] | [phone] | $[X]/hr | [date] | [#] | [1-5] |
| Appliance | [name] | [contact] | [phone] | $[X]/call | [date] | [#] | [1-5] |
| General handyman | [name] | [contact] | [phone] | $[X]/hr | [date] | -- | [1-5] |
| Locksmith | [name] | [contact] | [phone] | $[X]/call | [date] | [#] | [1-5] |
| Pest control | [name] | [contact] | [phone] | $[X]/visit | [date] | [#] | [1-5] |
| Cleaning | [name] | [contact] | [phone] | $[X]/unit | [date] | -- | [1-5] |
| Painting | [name] | [contact] | [phone] | $[X]/room | [date] | -- | [1-5] |
| Flooring | [name] | [contact] | [phone] | $[X]/SF | [date] | [#] | [1-5] |

Vendor Selection Criteria:
  1. Licensed (where required by trade -- plumbing, electrical, HVAC always)
  2. Insured (general liability $1M minimum, workers comp if employees)
  3. Responsive (returns calls within 2 hours, available for emergencies)
  4. Fair pricing (get 2-3 quotes for any job > $500)
  5. Quality work (track callbacks -- if same issue recurs, find new vendor)
  6. References (at least 2 from other landlords or property managers)

  Red flag: vendor cannot provide proof of insurance or license.
  Never use an unlicensed contractor for permitted work. Liability is on
  the property owner if an unlicensed worker is injured or causes damage.

Warranty Tracking:
  | Item | Vendor/Manufacturer | Install Date | Warranty Expires | Coverage |
  |---|---|---|---|---|
  | Water heater - Unit 2A | AO Smith | 01/15/2024 | 01/15/2030 | Parts + labor 6yr |
  | HVAC compressor - Bldg | Carrier | 06/01/2023 | 06/01/2033 | Compressor 10yr |
  | Roof | ABC Roofing | 09/01/2022 | 09/01/2042 | Materials 20yr, labor 5yr |
```

**Output**: Work order with classification, vendor assignment, cost tracking, warranty check, completion confirmation.

### Workflow 5: Unit Turnover Process

Follow the budget template in `references/unit-turnover-budget-template.md`.

**Turnover timeline**:

```
Unit Turnover Timeline -- [Unit Number]

Phase 1: Notice & Preparation (Day -60 to Day -30)
  [ ] Notice received from tenant: [date]
  [ ] Notice period confirmed per lease and state law: [30/60 days]
  [ ] Pre-move-out inspection scheduled: [date] (optional but recommended)
  [ ] Pre-move-out inspection completed: identify scope early
  [ ] Begin marketing unit (if lease allows showing during notice period)
  [ ] Determine target rent for next lease (check comps, adjust for condition)
  [ ] Decide: cosmetic refresh vs. renovation (budget accordingly)

Phase 2: Move-Out (Day 0)
  [ ] Tenant moves out: [date]
  [ ] Move-out inspection completed (same day or next business day)
  [ ] Keys, remotes, access cards collected
  [ ] Forwarding address obtained
  [ ] Utilities transferred to landlord name (same day to avoid shutoff)
  [ ] Security deposit clock starts (state-specific deadline)
  [ ] Photos and video of unit condition documented

Phase 3: Make-Ready Scope & Vendor Scheduling (Day 1-3)
  [ ] Walk unit with make-ready checklist
  [ ] Determine scope: [cosmetic / standard / full renovation]
  [ ] Get vendor quotes for work exceeding self-repair capability
  [ ] Order materials (paint, flooring, parts) -- lead time can be 3-7 days
  [ ] Schedule vendors in logical order:
      1. Demolition / removal (old carpet, fixtures)
      2. Rough repairs (drywall, plumbing, electrical)
      3. Painting (always before new flooring)
      4. Flooring installation
      5. Fixture installation (lights, hardware, appliances)
      6. Cleaning (always last)

Phase 4: Make-Ready Execution (Day 3-14, varies by scope)
  Cosmetic refresh (3-5 days):
    [ ] Patch and paint walls (neutral color: SW 7015 Repose Gray or equivalent)
    [ ] Clean carpets or replace if beyond cleaning
    [ ] Deep clean all surfaces, appliances, bathrooms
    [ ] Replace HVAC filters
    [ ] Check and replace smoke detector batteries
    [ ] Replace toilet seats
    [ ] Touch up caulking in kitchen and bathrooms
    [ ] Replace any burned-out bulbs
    [ ] Clean or replace blinds

  Standard turnover (7-10 days):
    All cosmetic items plus:
    [ ] Replace carpet (if > 5 years old or damaged beyond cleaning)
    [ ] Resurface or replace countertops if worn
    [ ] Replace faucets if dated or leaking
    [ ] Update light fixtures if dated
    [ ] Replace outlet covers and switch plates
    [ ] Professional appliance servicing
    [ ] Exterior: pressure wash entry, clean windows

  Full renovation (14-30 days):
    All standard items plus:
    [ ] New flooring throughout (LVP recommended for durability)
    [ ] New kitchen cabinets or cabinet refacing
    [ ] New countertops
    [ ] New appliance package
    [ ] Bathroom renovation (tile, vanity, fixtures)
    [ ] Electrical panel check / upgrade
    [ ] HVAC service or replacement
    [ ] Window replacement (if single-pane or damaged)

Phase 5: Final Inspection & Listing (Day 14-21)
  [ ] Final walkthrough: every item on make-ready list confirmed complete
  [ ] Professional photos taken (or quality smartphone photos with good lighting)
  [ ] Unit listed on platforms: [Zillow, Apartments.com, Craigslist, Facebook Marketplace]
  [ ] Showing schedule established
  [ ] Lockbox or showing access method set up

Phase 6: Lease Signing & Move-In (Day 21-30 target)
  [ ] Applications received and screened per Workflow 1
  [ ] Lease signed
  [ ] Security deposit and first month's rent collected
  [ ] Move-in inspection completed (Workflow 3)
  [ ] Keys and access provided
  [ ] Welcome packet delivered (emergency contacts, trash schedule,
      parking rules, maintenance request process, renter's insurance requirement)
```

**Output**: Turnover timeline with task assignments, vendor schedule, budget estimate per `references/unit-turnover-budget-template.md`, days-vacant tracking.

### Workflow 6: Financial Reporting

**Monthly rent roll**:

```
Rent Roll -- [Property Name] -- [Month Year]

| Unit | Type | SF | Tenant | Lease Start | Lease End | Market Rent | Actual Rent | Variance | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1A | 2BR/1BA | 850 | J. Smith | 06/01/25 | 05/31/26 | $1,850 | $1,800 | -$50 | Occupied |
| 1B | 1BR/1BA | 650 | M. Garcia | 09/01/25 | 08/31/26 | $1,700 | $1,650 | -$50 | Occupied |
| 2A | 2BR/1BA | 850 | K. Johnson | 01/01/26 | 12/31/26 | $1,900 | $1,900 | $0 | Occupied |
| 2B | 2BR/2BA | 950 | -- | -- | -- | $2,000 | $0 | -$2,000 | Vacant |

Summary:
  Total units: 4
  Occupied: 3 (75%)
  Vacancy loss: $2,000/month ($24,000 annualized)
  Gross potential rent: $7,450/month
  Actual collected: $5,350/month
  Collection rate vs occupied units: 100%
  Average rent per SF: $2.12/SF
  Average rent vs market: -$33/unit (1.8% below market)
```

**Monthly P&L by property**:

```
Profit & Loss -- [Property Name] -- [Month Year]

INCOME:
  Rental income (collected)          $5,350
  Late fees collected                $0
  Pet rent                           $75
  Laundry income                     $120
  Parking income                     $0
  Other income                       $0
  TOTAL INCOME                       $5,545

EXPENSES:
  Mortgage (P&I)                     $2,800
  Property taxes                     $450
  Insurance                          $180
  Water/sewer                        $220
  Common area electric               $85
  Trash removal                      $60
  Landscaping                        $150
  Repairs & maintenance              $325
  Property management fee            $0 (self-managed)
  Advertising/marketing              $50
  Legal/professional                 $0
  Accounting/bookkeeping             $0
  Miscellaneous                      $25
  TOTAL EXPENSES                     $4,345

NET OPERATING INCOME (before mortgage): $2,745
NET CASH FLOW (after mortgage):         $1,200

Key metrics:
  Operating expense ratio: 27.9% (expenses ex-mortgage / gross potential rent)
  Debt service coverage ratio: 1.98x (NOI / mortgage payment)
  Cash-on-cash return: [requires equity input]
  Break-even occupancy: 78.4% ([expenses] / [gross potential rent])
```

**Annual summary for tax preparation**:

```
Annual Tax Summary -- [Property Name] -- [Tax Year]

SCHEDULE E INPUTS:
  Gross rents received:              $66,540
  Other income (late fees, laundry): $2,340
  Total income:                      $68,880

  Advertising:                       $600
  Auto and travel:                   $480
  Cleaning and maintenance:          $3,900
  Commissions:                       $0
  Insurance:                         $2,160
  Legal and professional:            $350
  Management fees:                   $0
  Mortgage interest:                 $18,400
  Other interest:                    $0
  Repairs:                           $4,200
  Supplies:                          $360
  Property taxes:                    $5,400
  Utilities:                         $4,380
  Depreciation:                      $[per CPA / cost seg study]
  Other:                             $300
  Total expenses:                    $40,530

  Net rental income (loss):          $28,350

  Note: provide this summary to your CPA along with all receipts.
  Track mileage for property visits separately (IRS standard rate applies).

Chart of accounts for small landlords:
  4000 - Rental Income
  4100 - Late Fee Income
  4200 - Pet Rent
  4300 - Laundry/Vending Income
  4400 - Parking Income
  4900 - Other Income
  5000 - Mortgage Interest
  5100 - Property Taxes
  5200 - Insurance
  5300 - Utilities (Water, Electric, Gas, Trash)
  5400 - Repairs & Maintenance
  5500 - Capital Improvements (not expensed -- depreciated)
  5600 - Management Fees
  5700 - Advertising & Marketing
  5800 - Legal & Professional
  5900 - Auto & Travel
  6000 - Office & Supplies
  6100 - Landscaping
  6900 - Miscellaneous
```

**Capital reserve tracking**:

```
Capital Reserve Fund -- [Property Name]

Target reserve: $[500-1,000 per unit per year]
Current balance: $[amount]
Monthly contribution: $[amount]

  | Date | Description | Deposit | Withdrawal | Balance |
  |---|---|---|---|---|
  | 01/01 | Opening balance | | | $8,000 |
  | 01/15 | Monthly contribution | $400 | | $8,400 |
  | 02/01 | Water heater replacement (Unit 2A) | | $1,200 | $7,200 |
  | 02/15 | Monthly contribution | $400 | | $7,600 |
  | 03/15 | Monthly contribution | $400 | | $8,000 |

Reserve adequacy check:
  Recommended reserve: $500/unit/year * 4 units = $2,000/year (minimum)
  Better target: $1,000/unit/year * 4 units = $4,000/year
  Current annual contribution: $4,800 (adequate)
  Major upcoming expenses:
    - Roof (estimated remaining life: 8 years, replacement cost: $15,000)
    - HVAC (estimated remaining life: 5 years, replacement cost: $6,000/unit)
    - Parking lot reseal (every 3 years, cost: $2,000)
```

**Output**: Monthly rent roll, P&L, cash flow statement, reserve tracker, annual tax summary.

### Workflow 7: Self-Manage vs Third-Party PM Decision

**Breakeven analysis**:

```
Self-Manage vs. Third-Party Property Manager Analysis

YOUR PORTFOLIO:
  Units managed: [n]
  Monthly gross rent: $[amount]
  Annual gross rent: $[amount]

PM FEE COMPARISON:
  Typical PM fee structures:
    Percentage of collected rent: 8-12% (most common)
      Residential/multifamily: 8-10%
      Commercial/mixed-use: 4-6%
    Flat fee per unit: $75-$200/unit/month (less common)
    Leasing fee (new tenant): 50-100% of one month's rent (on top of management fee)
    Renewal fee: $150-$300 per renewal (some PMs waive this)
    Maintenance markup: 10-20% on vendor invoices (some PMs add this)

  YOUR ESTIMATED PM COST:
    Management fee: [n] units * $[gross rent] * [%] = $[monthly] / $[annual]
    Leasing fees (est. [n] turnovers/year): $[amount]
    Renewal fees: $[amount]
    Maintenance markup: $[amount]
    Total annual PM cost: $[amount]

YOUR TIME COST:
  Estimated hours per unit per month:
    1-10 units: 3-5 hours/unit/month (higher per-unit time for small portfolios)
    11-30 units: 2-3 hours/unit/month
    31-50 units: 1.5-2 hours/unit/month (economies of scale)

  Your total hours: [n] units * [hours/unit] = [total hours/month]
  Your hourly opportunity cost: $[amount] (what is your time worth?)
  Annual time cost: [hours/month] * 12 * $[hourly rate] = $[amount]

BREAKEVEN ANALYSIS:
  If PM cost < your time cost: hire a PM
  If PM cost > your time cost: self-manage (if you are willing and able)

  Typical breakeven: ~25-35 units (for someone with a $75-100/hr opportunity cost)
  Lower breakeven if:
    - You have a high-paying day job (higher opportunity cost)
    - Properties are geographically dispersed (more travel time)
    - High-maintenance properties (older buildings, difficult tenants)
  Higher breakeven if:
    - You live near your properties
    - Properties are newer with few maintenance issues
    - You enjoy the work and consider it part-time income

QUALITY INDICATORS (when to hire a PM even below breakeven):
  - You cannot respond to emergencies within 2 hours
  - Maintenance requests go unresolved for > 7 days regularly
  - You are uncomfortable with legal compliance (eviction, Fair Housing)
  - You travel frequently and cannot manage in-person requirements
  - Tenant relations are causing you significant stress
  - Your vacancy rate is higher than market average (poor marketing/screening)
  - You are losing tenants due to slow response or poor communication

QUALITY INDICATORS (when to keep self-managing):
  - You respond to every maintenance request within 24 hours
  - Your vacancy rate is at or below market
  - You maintain consistent screening and compliance
  - You enjoy the work and stay current on landlord-tenant law
  - You can handle emergencies personally or have a reliable backup
  - Your properties are within 30 minutes of your home or workplace

TRANSITION PLAN (if switching to PM):
  1. Interview 3+ PM companies. Ask for references from similar portfolios.
  2. Request sample management agreement. Have attorney review.
  3. Verify PM has a trust account for deposits (state requirement in most states).
  4. Transition all tenant communication, keys, vendor relationships.
  5. Establish reporting cadence: monthly statements, annual budget review.
  6. Monitor PM performance quarterly (vacancy, maintenance response, collection rate).
  7. Review PM contract annually. Most are 1-year with 30-60 day cancellation.
```

**Output**: Breakeven analysis, PM cost comparison, recommendation with supporting data, transition plan if applicable.

### Workflow 8: Lease Administration

**Renewal tracking calendar**:

```
Lease Renewal Calendar -- [Property Name]

| Unit | Tenant | Lease End | Notice Required | Action Deadline | Proposed Increase | Status |
|---|---|---|---|---|---|---|
| 1A | J. Smith | 05/31/26 | 60 days | 04/01/26 | $50 (2.8%) | Renewal letter sent |
| 1B | M. Garcia | 08/31/26 | 60 days | 07/01/26 | $75 (4.5%) | Pending -- send by 07/01 |
| 2A | K. Johnson | 12/31/26 | 30 days | 12/01/26 | $0 (new lease) | N/A until Q4 |
| 2B | -- | Vacant | -- | -- | -- | -- |

Rent Increase Guidelines:
  Check market rents (Zillow, Rentometer, Apartments.com comps)
  Typical annual increase: 2-5% (varies by market)
  Factor in: current tenant quality, market vacancy, cost of turnover
  Cost of turnover (lost rent + make-ready) typically = 2-3 months of rent
  If good tenant is $50-100 below market: consider keeping them (retention value)

  Rent increase notice requirements vary by state:
    - 30 days notice for month-to-month (most states)
    - 60-90 days notice for annual leases (some states)
    - Rent control jurisdictions: maximum increase capped (check local law)
    - Section 8: must comply with Housing Authority rent reasonableness

Renewal Letter Template:

  Dear [Tenant Name],

  Your lease for [Unit] at [Property Address] expires on [date]. We value
  you as a tenant and would like to offer you a renewal.

  Renewal terms:
    New lease period: [start] to [end] (12 months)
    Monthly rent: $[new amount] (increase of $[amount] / [%] from current)
    All other lease terms remain the same.

  Please sign and return the enclosed renewal agreement by [date -- 14 days
  before action deadline]. If we do not hear from you by [date], we will
  assume you intend to vacate and will begin marketing the unit.

  If you have any questions or would like to discuss the terms, please
  contact me at [phone/email].

  Thank you for being a great tenant.

  Sincerely,
  [Landlord Name]
```

**Lease violation documentation**:

```
Lease Violation Notice

Date: [date]
To: [Tenant Name], [Unit Number], [Property Address]
From: [Landlord Name]

Dear [Tenant Name],

This letter is to formally notify you of a violation of your lease agreement
dated [lease date]:

VIOLATION: [describe specifically]
  Examples:
  - Unauthorized pet (lease Section [X] prohibits pets without approval)
  - Noise complaints (lease Section [X] requires quiet enjoyment for all tenants)
  - Unauthorized occupant (lease Section [X] limits occupants to named tenants)
  - Improper trash disposal (lease Section [X] requires use of designated areas)
  - Unauthorized modification (lease Section [X] prohibits alterations without
    written consent)
  - Parking violation (lease Section [X] limits parking to assigned spaces)

OBSERVED ON: [date(s) of violation]
DOCUMENTED BY: [landlord / other tenant complaint / inspection]

REQUIRED ACTION:
  You must [cure the violation / cease the activity] within [X] days of this
  notice (by [date]).

CONSEQUENCE:
  Failure to cure this violation within the specified time may result in
  [further action up to and including termination of your lease / non-renewal
  at lease end].

  This is the [first / second / third] notice regarding this issue.
  [If second or third:] Previous notices were issued on [dates].

Please contact me at [phone/email] if you have questions or would like to
discuss this matter.

Sincerely,
[Landlord Name]
[Date]

Delivery method: [hand-delivered / posted on door / certified mail / email]
Copy retained in tenant file: [yes]
```

**Annual inspection scheduling**:

```
Annual Property Inspection Schedule -- [Year]

| Unit | Tenant | Last Inspected | Next Inspection | Notice Sent | Completed |
|---|---|---|---|---|---|
| 1A | J. Smith | 06/15/25 | 06/15/26 | [date] | [ ] |
| 1B | M. Garcia | 09/20/25 | 09/20/26 | [date] | [ ] |
| 2A | K. Johnson | 01/10/26 | 01/10/27 | [date] | [ ] |
| 2B | Vacant | N/A | At turnover | N/A | [ ] |

Inspection notice requirements:
  Most states require 24-48 hours written notice before entering an occupied unit
  (exception: emergencies). Check state law.
  Notice must state: date, approximate time window, purpose of entry.
  Tenant has right to be present (but cannot unreasonably refuse access).

Annual inspection checklist:
  [ ] Smoke detectors working (replace batteries)
  [ ] Carbon monoxide detectors working
  [ ] No unauthorized modifications or occupants
  [ ] No lease violations (pets, smoking, etc.)
  [ ] No evidence of pest activity
  [ ] Plumbing fixtures functioning (check under sinks for leaks)
  [ ] HVAC filter condition (replace if dirty)
  [ ] Window and door locks functioning
  [ ] Water heater temperature set to 120F (scald prevention)
  [ ] General cleanliness and condition (note any concerns)
  [ ] Exterior: check for damage, drainage issues, trip hazards
```

**Output**: Renewal calendar with action deadlines, rent increase recommendations, violation notices, inspection schedule.

## Output Format

Present results in this order:

1. **Portfolio Snapshot** -- unit count, occupancy rate, total monthly rent, delinquencies
2. **Action Items** -- upcoming lease expirations, maintenance backlog, overdue inspections
3. **Detailed Workflow Output** -- specific to the triggered workflow
4. **Financial Summary** -- month-over-month rent collection, P&L, reserve status
5. **Compliance Calendar** -- lease renewals, inspection schedules, insurance expirations
6. **Red Flags** -- any items from the red flags section that apply to current portfolio

## Red Flags and Failure Modes

1. **Inconsistent tenant screening**: applying different criteria to different applicants creates Fair Housing liability. The fix is simple: write down your criteria, apply them identically to every applicant, and document every decision. One discrimination complaint can cost $10,000-$100,000+ in legal fees and settlements, dwarfing any rent income from the unit.

2. **No written lease**: oral lease agreements are legal in some states for terms under one year, but they are nearly impossible to enforce. Every tenancy should have a written lease specifying rent, term, responsibilities, and house rules. State-specific lease templates are available from landlord associations for $25-50.

3. **Security deposit commingling**: in most states, security deposits must be held in a separate account from operating funds. Some states require interest-bearing accounts with annual interest payments to the tenant. Commingling deposits with operating funds is illegal in most jurisdictions and creates personal liability for the landlord, even in an LLC structure.

4. **Deferred maintenance creating habitability issues**: every state has an implied warranty of habitability. Failing to address heating, plumbing, pest, or structural issues can result in tenants withholding rent (legally, in many states), health department complaints, and code violation fines. The cost of deferred maintenance compounds: a $200 leak repair becomes a $5,000 mold remediation.

5. **Late fee structure exceeding state maximum**: many states cap late fees (e.g., California caps at 6% of rent, New York has no statutory cap but courts void "unreasonable" fees). Charging excessive late fees is unenforceable and can trigger tenant complaints to consumer protection agencies.

6. **No renter's insurance requirement**: if a tenant causes a fire or water damage, the landlord's insurance covers the building but not the tenant's negligence. Without renter's insurance, the tenant has no coverage for their liability, and the landlord's insurance company may subrogate against the tenant (who likely cannot pay). Requiring $100,000 liability coverage ($15-25/month) protects both parties.

7. **Missing lead paint disclosure (pre-1978 properties)**: federal law (42 USC 4852d) requires disclosure of known lead-based paint hazards and provision of the EPA pamphlet "Protect Your Family From Lead in Your Home" before lease signing. Failure to disclose can result in fines up to $19,507 per violation (2024 amount, adjusted annually) and treble damages in private lawsuits.

8. **No capital reserve fund**: operating without reserves means every major repair becomes an emergency. Water heaters, HVAC systems, roofs, and appliances fail on their own schedule. Without $500-1,000/unit/year in reserves, landlords are forced into expensive emergency repairs, deferred maintenance spirals, or debt financing for routine capital needs.

9. **Failing to document lease violations**: verbal warnings without written documentation are worthless in eviction proceedings. Every violation notice must be in writing, dated, describe the specific violation, reference the lease section, state the cure deadline, and be retained in the tenant file. Courts require a paper trail.

10. **Not tracking warranty expiration dates**: replacing a water heater, HVAC compressor, or appliance that is still under warranty wastes money. Maintain a warranty log for every major system and appliance. When a covered item fails, contact the manufacturer first.

## Chain Notes

- **rent-optimization-planner**: Pricing strategy and market comp analysis for setting asking rents on vacant or renewal units
- **property-performance-dashboard**: Portfolio-level financial reporting rolls up from individual property P&L data produced here
- **lease-document-factory**: When a new tenant is approved through screening, the lease document skill generates the lease
- **tenant-retention-engine**: Retention strategies for good tenants complement the renewal tracking in Workflow 8
- **vendor-invoice-validator**: For operators with 20+ units, vendor invoice validation automates the cost-checking done manually here
- **work-order-triage**: For portfolios above 30 units, the triage skill provides automated classification and routing
- **tenant-delinquency-workout**: When a tenant enters the delinquency escalation timeline, the workout skill provides negotiation frameworks
- **property-tax-appeal-analyzer**: Annual property tax assessment review, referenced in the financial reporting workflow
