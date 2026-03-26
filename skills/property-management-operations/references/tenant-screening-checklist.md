# Tenant Screening Checklist Reference

Complete application review process, Fair Housing compliance protocol, income verification methods, landlord reference scripts, and adverse action notice templates. All examples use a baseline 12-unit multifamily property in a mid-tier market with average rents of $1,500-$2,000/month.

---

## 1. Application Review Process

### Step-by-Step Screening Workflow

```
APPLICATION RECEIVED
  |
  v
Step 1: Completeness Check (5 minutes)
  [ ] All fields filled in (name, SSN, DOB, current address, employment, income)
  [ ] All adult occupants have submitted separate applications
  [ ] Government-issued photo ID provided (copy front and back)
  [ ] Application fee received ($25-$75, per state law)
  [ ] Signed authorization for credit and background check
  [ ] 2 most recent pay stubs OR tax return (if self-employed)
  [ ] If incomplete: return to applicant with list of missing items
      DO NOT begin screening until application is complete
  |
  v
Step 2: Income Verification (30-60 minutes)
  Method 1 -- W-2 Employee:
    [ ] Review 2 most recent pay stubs
    [ ] Calculate gross monthly income:
        Bi-weekly pay stubs: (gross per period * 26) / 12
        Semi-monthly pay stubs: gross per period * 2
        Weekly pay stubs: (gross per period * 52) / 12
    [ ] Verify income meets 3x rent threshold:
        Required income: $[rent] * 3 = $[minimum]
        Applicant income: $[calculated]
        PASS: income >= minimum
        FAIL: income < minimum (offer guarantor option)
    [ ] Call employer to verify:
        - Position and start date
        - Full-time vs part-time
        - Likelihood of continued employment
        IMPORTANT: call the employer's main number (verify online),
        NOT the number the applicant provided

  Method 2 -- Self-Employed:
    [ ] Request 2 most recent federal tax returns (1040 + Schedule C or K-1)
    [ ] Calculate average annual net income from both years
    [ ] Divide by 12 for monthly income
    [ ] If income is highly variable, use the lower of the two years
    [ ] Request 3 months of bank statements showing regular deposits
    [ ] Look for: consistent deposit patterns, average monthly balance > 3x rent
    [ ] If income is from a business: request business license and 1 year of
        business bank statements

  Method 3 -- Non-Employment Income:
    [ ] Social Security: request benefits letter (ssa.gov letter)
    [ ] Pension/Retirement: request most recent statement
    [ ] Investment income: request brokerage statements (3 months)
    [ ] Alimony/Child support: request court order and 3 months bank statements
    [ ] Housing voucher (Section 8): request voucher letter from housing authority
        NOTE: many states and cities prohibit discrimination based on source of
        income, including Section 8 vouchers. Check local law.
  |
  v
Step 3: Credit Check (15-30 minutes)
  Services: TransUnion SmartMove, MyRental, RentPrep, or through PM software
  Cost: $25-$40 per applicant (charged to applicant via application fee)

  Review checklist:
    [ ] Credit score recorded: ___
    [ ] Credit score tier:
        700+:   Strong -- standard deposit
        650-699: Acceptable -- standard deposit, note any concerning items
        600-649: Conditional -- review details below
        Below 600: High risk -- guarantor required
        No score: Thin file -- verify income strongly, consider guarantor

    [ ] Review for disqualifying items:
        - Eviction judgment: DISQUALIFY (unless > 7 years old and explained)
        - Landlord collection: DISQUALIFY (indicates rent non-payment)
        - Utility shutoff for non-payment: YELLOW FLAG (pattern of non-payment)
        - Bankruptcy: review age and type
            Chapter 7 > 3 years old: consider (debts discharged)
            Chapter 7 < 3 years old: higher risk
            Chapter 13 (active plan): verify plan payments are current

    [ ] Review for context (do NOT auto-disqualify):
        - Medical debt: common, often involuntary, low predictive value
        - Student loans: look at payment status, not balance
        - Old collections (> 3 years): less relevant than recent history
        - Authorized user accounts: applicant is not the primary debtor

    [ ] Debt-to-income ratio check:
        Monthly debt payments (from credit report): $___
        Monthly gross income: $___
        DTI ratio: ___% (ideal: < 40% including proposed rent)
  |
  v
Step 4: Background Check (concurrent with credit)
  [ ] Criminal history check (county + national)
      NOTE ON CRIMINAL HISTORY:
        - Check local law FIRST. Many jurisdictions restrict or prohibit
          use of criminal history in tenant screening:
            NYC: Fair Chance for Housing Act (2024)
            Seattle: Fair Chance Housing Ordinance
            Portland: Fair Access in Renting Ordinance
            San Francisco, Oakland, Berkeley: various restrictions
            New Jersey: Fair Chance in Housing Act
            Cook County IL: Just Housing Amendment
        - Where permitted, use individualized assessment:
            Nature of offense
            Time since offense
            Evidence of rehabilitation
            Relevance to tenancy
        - DO NOT use arrest records (arrests are not convictions)
        - DO NOT apply blanket policies ("no felonies ever")
        - HUD guidance (2016): blanket criminal history policies have
          disparate impact and may violate Fair Housing Act

  [ ] Eviction history check (court records)
      - Search county court records in current and prior jurisdictions
      - Look for: filings (even if dismissed), judgments, writs of possession
      - Note: a filing that was dismissed may indicate a dispute, not default

  [ ] Sex offender registry check
      - National Sex Offender Public Website (nsopw.gov)
      - State-specific registry
  |
  v
Step 5: Landlord Reference Check (20-30 minutes)
  Contact BOTH current AND prior landlord.
  WHY BOTH: current landlord may give a positive reference just to
  get a problem tenant to move out.

  Prior Landlord Script:
  "Hi, my name is [your name] and I'm a property owner verifying a
  rental application. [Applicant name] listed your property at [address]
  as a prior residence from [dates]. May I ask a few questions?"

  Questions:
    1. "Can you confirm [name] rented from [date] to [date]?"
       Answer: ___

    2. "What was the monthly rent?"
       Answer: $___

    3. "Did [name] pay rent on time consistently?"
       Answer: ___
       Follow-up if "mostly" or "usually": "How often was rent late?
       By how many days?"

    4. "Was the unit left in good condition when they moved out?"
       Answer: ___
       Follow-up if no: "What were the issues?"

    5. "Were there any complaints from neighbors or lease violations?"
       Answer: ___

    6. "Did [name] give proper notice before moving out?"
       Answer: ___

    7. "Would you rent to [name] again?"
       Answer: ___
       This is the most important question. A "no" or hesitation
       is a significant red flag.

  Current Landlord Script:
    Same questions, but add:
    8. "Why is [name] moving?"
       Answer: ___
       (Verify against what the applicant told you)

  [ ] Document all answers with date, time, and landlord contact name
  [ ] If landlord is unresponsive after 2 attempts: note in file,
      do not hold application indefinitely (3 business day limit)
  |
  v
Step 6: Decision (same day if possible)
  Compile screening scorecard:

  | Criterion | Result | Pass/Fail |
  |---|---|---|
  | Income >= 3x rent | $X,XXX vs $X,XXX | PASS / FAIL |
  | Credit score >= threshold | XXX | PASS / CONDITIONAL / FAIL |
  | No eviction history | Yes / No | PASS / FAIL |
  | No landlord collections | Yes / No | PASS / FAIL |
  | Positive landlord references | Yes / Mixed / No | PASS / CONDITIONAL / FAIL |
  | Employment verified | Yes / No | PASS / FAIL |
  | Background check clear | Yes / Issues | PASS / CONDITIONAL / FAIL |
  | DTI ratio < 40% | XX% | PASS / CONDITIONAL / FAIL |

  Decision matrix:
    All PASS: APPROVE -- proceed to lease
    Any CONDITIONAL: APPROVE WITH CONDITIONS
      Conditions may include: guarantor, additional deposit (per state law),
      shorter lease term, requirement to set up autopay
    Any FAIL on income or eviction: DENY
    Borderline: use judgment, document reasoning

  CRITICAL: apply the same criteria to every applicant. The decision
  must be based on the criteria above, not on how the applicant looks,
  sounds, or "seems."
```

---

## 2. Fair Housing Do's and Don'ts

### Protected Classes

```
FEDERAL (apply everywhere in the US):
  1. Race
  2. Color
  3. Religion
  4. National origin
  5. Sex (including gender identity and sexual orientation per HUD guidance)
  6. Familial status (families with children under 18, pregnant women)
  7. Disability (physical or mental)

STATE AND LOCAL (varies -- check your jurisdiction):
  - Source of income (Section 8 vouchers) -- required in CA, NY, NJ, OR, WA,
    CT, MA, VT, and many cities
  - Age
  - Marital status
  - Sexual orientation (separate from federal sex protection in some states)
  - Gender identity/expression
  - Veteran/military status
  - Student status
  - Immigration/citizenship status
  - Political affiliation
  - Victim of domestic violence
  - Genetic information
```

### Advertising Compliance

```
NEVER use these phrases in listings:
  - "Perfect for young professionals" (age, familial status)
  - "Great for singles" or "ideal for couples" (familial status, marital status)
  - "Walking distance to [church/temple/mosque]" (religion)
  - "English-speaking preferred" (national origin)
  - "No children" or "adults only" (familial status -- unless senior housing
    exemption applies: 62+ or 55+ with HUD certification)
  - "No wheelchairs" or "must be able to climb stairs" (disability)
  - "No Section 8" (source of income -- in many jurisdictions)
  - "Female roommate wanted" (sex -- exception: shared living space)

ALWAYS use these practices:
  - Describe the PROPERTY, not the ideal TENANT
  - "Spacious 2BR apartment with in-unit laundry" -- describes property
  - Use the Equal Housing Opportunity logo on all advertising
  - List objective facts: bedrooms, bathrooms, rent, location, amenities
  - Include accessibility features if present (wheelchair accessible,
    elevator, ground floor)
```

### Reasonable Accommodations and Modifications

```
Disability-related requests:

Reasonable accommodation: a change in rules, policies, or services
  Examples:
    - Allowing an assistance animal in a no-pets building
    - Providing a reserved parking spot closer to the unit
    - Allowing a live-in aide
    - Providing written (not just verbal) notices for a deaf tenant
  Landlord obligation: grant unless it would be an undue financial
  or administrative burden, or fundamentally alter the nature of
  the housing operation
  Cost: landlord bears the cost (no extra charge to tenant)

Reasonable modification: a physical change to the unit or common area
  Examples:
    - Installing grab bars in bathroom
    - Widening doorways for wheelchair access
    - Installing a ramp at building entrance
    - Lowering countertops or light switches
  Landlord obligation: must allow the modification
  Cost: tenant pays for the modification (in most cases)
  Restoration: landlord may require tenant to restore the unit to
  original condition at move-out (where reasonable)

Process:
  1. Tenant makes a request (does not need to be in writing or use
     specific language -- "I need X because of my disability" is sufficient)
  2. Landlord may request documentation of the disability-related need
     (NOT the specific diagnosis -- just verification from a healthcare
     provider that there is a disability-related need for the accommodation)
  3. Engage in an interactive process to find a solution
  4. Respond within 10 business days
  5. Document the request, the process, and the outcome
```

---

## 3. Adverse Action Notice Template

```
NOTICE OF ADVERSE ACTION

Date: [date]

To: [applicant name]
    [applicant address]

RE: Rental Application for [property address], Unit [number]

Dear [applicant name],

After careful review of your rental application, we are unable to
approve your tenancy at this time.

The decision was based on the following criteria:

  [ ] Income does not meet minimum requirement (3x monthly rent)
  [ ] Credit score below minimum threshold
  [ ] Negative rental history (eviction record or landlord reference)
  [ ] Insufficient employment history or verification
  [ ] Criminal history (per individualized assessment)
  [ ] Incomplete application (missing required documentation)
  [ ] Other: ________________________________

[If credit report was a factor:]
This decision was based in whole or in part on information obtained
from a consumer reporting agency:

  Agency: [TransUnion / Experian / Equifax / screening service name]
  Address: [agency address]
  Phone: [agency phone]

Under the Fair Credit Reporting Act, you have the right to:
  - Obtain a free copy of your consumer report from the agency within
    60 days of this notice
  - Dispute the accuracy or completeness of any information in the report
  - The consumer reporting agency did not make this decision and cannot
    explain why it was made

[If applicant was denied and wishes to discuss:]
If you have questions about this decision, you may contact:

  [Landlord/PM name]
  [Phone]
  [Email]

Your application fee of $[amount] is [non-refundable / will be refunded
within X days] per [state law / our policy].

Sincerely,
[Landlord/PM name]
[Property name]
```

---

## 4. Guarantor Requirements

```
When to require a guarantor:
  - Applicant income below 3x rent threshold
  - Applicant credit score below 600
  - Applicant has no credit history (first-time renter)
  - Applicant is a student with limited income
  - Applicant is newly employed (< 6 months at current job)

Guarantor screening criteria:
  - Income: 5x monthly rent (guarantor takes on risk, higher bar)
  - Credit score: 700+ (guarantor must be creditworthy)
  - Must complete full application and screening process
  - Must sign a guaranty agreement (separate from the lease)
  - Guarantor is jointly and severally liable for all lease obligations

Guaranty agreement key terms:
  - Guarantor unconditionally guarantees all rent and charges
  - Guaranty survives lease renewal (or specify if limited to initial term)
  - Guarantor waives right to require landlord to pursue tenant first
  - Guarantor agrees to pay landlord's attorney fees if collection is needed
  - Guarantor can be released only with landlord's written consent

Alternative to personal guarantor:
  - Institutional guarantor services: Insurent, TheGuarantor, Rhino
  - Cost: typically one month's rent (paid by tenant)
  - Coverage: guarantees rent up to a specified amount
  - Useful for tenants who cannot find a personal guarantor
  - Landlord should verify the institutional guarantor's coverage terms
```

---

## 5. Application Processing Timeline

```
Best practice timeline:

Day 1: Application received
  - Completeness check (same day)
  - Order credit and background check (same day)
  - Contact employers and landlord references (same day)

Day 2: Follow up on outstanding verifications
  - Second attempt on unresponsive landlord references
  - Review credit and background results (usually available in hours)

Day 3: Decision
  - Compile screening scorecard
  - Make approval/denial/conditional decision
  - Notify applicant in writing

Maximum hold period: 3 business days from complete application
  - If you cannot verify references in 3 days, make a conditional
    decision and continue verification
  - Holding applications longer than 3 days risks losing good tenants
    to competing landlords
  - If you have multiple applicants, process in order received
    (first-come, first-served prevents discrimination claims)

Multiple applicants:
  - Screen in order of application receipt
  - Approve the first qualified applicant
  - Do NOT compare applicants against each other
    (this opens the door to discrimination claims)
  - Do NOT hold an apartment for a "better" applicant while
    screening others
```
