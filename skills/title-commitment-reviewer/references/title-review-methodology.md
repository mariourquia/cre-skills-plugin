# Title Review Methodology

Reference for SKILL.md Workflows 1-7. This document covers the anatomy of an ALTA title commitment, the step-by-step review checklist, common cure procedures with cost and timeline estimates, and the endorsement order process.

---

## ALTA Title Commitment Anatomy

An ALTA title commitment (also called a "title binder" in some states) is a written commitment by the title insurance underwriter to issue a policy upon satisfaction of stated conditions. It is not a policy -- it becomes a policy at closing when the premium is paid and all conditions are met.

### Structure

```
Commitment Cover Page
  - Commitment number (title order number)
  - Effective date (date of last search)
  - Proposed insured(s)
  - Type of policy (owner's, lender's, or simultaneous issue)
  - Underwriter name

Schedule A -- The Basics
  - Section 1: Effective date
  - Section 2: Proposed insured
  - Section 3: Estate or interest (fee simple, leasehold)
  - Section 4: Title is vested in (current owner of record)
  - Section 5: Legal description of land
  - Section 6: Policy amount

Schedule B-I -- Requirements
  - Conditions that must be satisfied before the policy will be issued
  - Numbered list; each item has an implicit or explicit deadline
  - Failure to satisfy any B-I item means no policy is issued

Schedule B-II -- Exceptions
  - Matters excluded from coverage under the policy
  - The title company will not defend or indemnify against these
  - Numbered list; each item corresponds to a recorded instrument or a
    standard exception category

Exhibit A (if attached)
  - Legal description (sometimes attached rather than in Schedule A)

Endorsement Schedules (if applicable)
  - Listed endorsements to be issued with the policy at closing
```

### What Title Insurance Covers vs. Does Not Cover

**Covered (post-closing discoveries of pre-closing defects):**
- Forgeries in the chain of title
- Undisclosed heirs of a prior owner
- Errors in recording prior instruments
- Liens that were in the public record but missed by the search
- Judgment liens that attached and were not identified
- Claims by prior owners or lienholders

**Not Covered (standard policy exclusions -- not negotiable):**
- Matters created by the insured after the policy date (future defects)
- Matters the insured knew about and did not disclose
- Eminent domain / governmental taking (some endorsements provide limited coverage)
- Environmental contamination (CERCLA superliens are in the gray zone; ALTA 8.1 helps)
- Zoning violations (unless ALTA 3.1 endorsement is issued)
- Physical condition of the land and improvements (that is what inspections are for)
- Rights of parties in possession (unless deleted with estoppels)

---

## Step-by-Step Review Checklist

Use this checklist to conduct a complete title commitment review. Each item maps to a SKILL.md workflow.

### Phase 1: Organize the File (Before Review)

```
[ ] Assemble documents:
    [ ] Title commitment (all schedules)
    [ ] ALTA/NSPS survey (current certification)
    [ ] Prior title policy (if available)
    [ ] Lien search results
    [ ] Recorded easements referenced in B-II
    [ ] Deed and prior deeds (if available from title plant)
    [ ] Entity documents (operating agreement, good standing certificate)

[ ] Confirm property details:
    [ ] State, county, municipality
    [ ] Attorney state or title company state
    [ ] APN / tax parcel number
    [ ] Acreage / square footage

[ ] Identify deal parameters:
    [ ] Transaction type (acquisition, refi, 1031)
    [ ] Policy type (owner, lender, simultaneous)
    [ ] Anticipated closing date
    [ ] Lender (if applicable) and lender's endorsement requirements
```

### Phase 2: Schedule A Review (Workflow 1)

```
[ ] Effective date:
    [ ] Note days between commitment date and anticipated closing
    [ ] If > 30 days: flag gap endorsement requirement (ALTA 16)
    [ ] If > 90 days: discuss re-ordering commitment with title officer

[ ] Proposed insured:
    [ ] Owner's policy: compare to acquiring entity name; must match exactly
    [ ] Lender's policy: compare to lender name in loan commitment; ISAOA/ATIMA present
    [ ] Confirm entity type matches (LLC vs. LP vs. Corp)
    [ ] Confirm acquiring entity is authorized to take title in subject state

[ ] Vesting (Schedule A, Section 4):
    [ ] Current owner matches seller under contract
    [ ] Entity is active and in good standing in state of formation
    [ ] Entity is registered to do business in property state (if different from formation state)
    [ ] Tax records and county assessor records match vested owner

[ ] Legal description:
    [ ] Compare Schedule A legal description to survey legal description (word-for-word)
    [ ] Note any discrepancy, no matter how minor
    [ ] Compare to deed in chain (confirm same description)
    [ ] Multi-parcel: confirm all parcels are listed; no parcel is missing or duplicated

[ ] Policy amount:
    [ ] Owner's: matches purchase price
    [ ] Lender's: matches loan amount
    [ ] Any gap between policy amount and purchase price / loan amount is uninsured exposure

[ ] Estate or interest:
    [ ] Fee simple: standard
    [ ] Leasehold: obtain ground lease; leasehold policy form is different
    [ ] Any life estate, remainder, or qualified interest: flag; consult local counsel
```

### Phase 3: Schedule B-I Review (Workflow 2)

```
[ ] List all B-I requirements in an assignment matrix
[ ] For each requirement:
    [ ] Identify responsible party (seller, buyer, title company, third party)
    [ ] Estimate resolution timeline
    [ ] Flag any requirement that depends on a third party outside the transaction
    [ ] Note if requirement has a fixed deadline (e.g., "within 30 days of commitment date")

[ ] Specific items to check:
    [ ] All prior liens identified and payoff letters received or ordered
    [ ] FIRPTA certificate required? (Seller is foreign person or entity)
    [ ] Entity authorization documents required and obtained
    [ ] Survey required? (Some B-I items require a current survey)
    [ ] Gap period indemnity required? (Commitment date to closing date)
```

### Phase 4: Schedule B-II Review (Workflow 3)

```
[ ] Number every exception in B-II
[ ] For each exception:
    [ ] Identify the type (standard, non-standard)
    [ ] Locate the underlying recorded document if referenced
    [ ] Assign a Tier (1, 2, or 3) using the acceptability matrix in title-exception-categories.md
    [ ] Determine treatment: accept, negotiate endorsement, cure required
    [ ] If endorsement: identify the applicable ALTA endorsement number

[ ] Exceptions requiring particular attention:
    [ ] Any mechanic's or materialman's lien filed in the last 120 days
    [ ] Any lis pendens or active litigation
    [ ] Rights of parties in possession (tenants): confirm estoppels in process
    [ ] Any restriction that might conflict with intended use
    [ ] Any easement that might encroach on improvements (cross-reference to survey)
    [ ] Any exception for "unrecorded interests": investigate; may indicate seller's disclosure
```

### Phase 5: Survey Cross-Reference (Workflow 4)

```
[ ] Confirm survey certification date and surveyor licensure
[ ] Confirm survey complies with 2021 ALTA/NSPS minimum standard detail requirements
[ ] Run the legal description comparison (Schedule A vs. survey)
[ ] Map every easement shown on survey to a B-II exception number
[ ] Map every B-II easement exception to a survey depiction
[ ] Document any easement shown on survey with no B-II exception (unscheduled matter)
[ ] Identify all encroachments:
    [ ] Subject property improvements encroaching onto adjacent parcels
    [ ] Adjacent improvements encroaching onto subject property
    [ ] Any improvement within a setback or buffer zone
[ ] Note FEMA flood zone designation from survey
[ ] Confirm direct access to public road (or record access easement)
```

### Phase 6: Chain Validation (Workflow 5)

```
[ ] Confirm search period meets state's marketable title act requirements
[ ] Trace conveyances: each grantor in current deed = grantee in prior deed
[ ] Flag any name mismatch between instruments
[ ] Note any gap in time > 12 months between recorded instruments
[ ] Identify any instrument referenced in the chain that is not in the search results
[ ] Confirm no probate issues (owner died without recorded transfer in chain)
[ ] Confirm no entity dissolution issues in the chain
[ ] Confirm current vested owner (seller) matches final instrument in chain
```

### Phase 7: Lien Search (Workflow 6)

```
[ ] Confirm search period: minimum 10 years for judgment liens, current for mechanics
[ ] Confirm search jurisdiction: county where property sits + all counties where owner
    is known to have real property interests (for judgment liens)
[ ] Ad valorem taxes: current year and 5 prior years -- all paid or escrowed
[ ] Special assessments: current -- confirmed paid or assumed
[ ] Judgment liens: none open against current owner or any prior owner within search period
[ ] Mechanic's liens: none filed within statutory lien period (90-120 days, state-specific)
[ ] UCC fixture filings: none active against seller entity covering property fixtures
[ ] Federal tax liens: none open against current owner
[ ] Confirm each open lien has a corresponding B-I requirement
```

### Phase 8: Cure Path Assembly (Workflow 7)

```
[ ] Compile all open items from Phases 2-7 into a single cure matrix
[ ] Assign priority level (P0-P4) per the SKILL.md framework
[ ] Assign responsible party and deadline for each P1 item
[ ] Confirm all P0 items are disclosed to principal immediately
[ ] Draft cure letter to seller's counsel and title officer
[ ] Order all P3 endorsements from title underwriter
[ ] Document all P4 items in the deal file with client acceptance noted
```

---

## Common Cure Procedures

### Payoff and Release of Existing Mortgage / Deed of Trust

**Process:**
1. Request payoff letter from existing lender. Letters typically expire in 30 days.
2. Calculate payoff to closing date (include per-diem interest).
3. Confirm release / reconveyance will be recorded promptly after payoff (most lenders: 5-30 days after receiving funds, depending on state).
4. At closing: wire payoff amount to existing lender from closing proceeds.
5. Title company records deed of trust release (or trustee's deed of reconveyance in deed-of-trust states) concurrently or shortly after closing.

**Cost estimate:** Payoff amount (principal + accrued interest + prepayment premium if applicable) + lender recording fee ($50-$200).

**Timeline:** 3-10 business days from wire for release to be recorded.

**Failure mode:** Prepayment penalty not calculated correctly; lender fails to record release timely. Require written release commitment from lender's servicing department before closing.

---

### Mechanic's Lien -- Payment and Release

**Process:**
1. Obtain copy of filed lien. Confirm: claimant name, amount claimed, property description, date of last furnishing, date filed.
2. Verify the lien is within the statutory period (if lien period has expired, it may be unenforceable -- but do not rely on this without local counsel confirmation).
3. Negotiate payoff with claimant. Lien amount may differ from actual amount owed.
4. At closing: pay claimant from proceeds; require claimant to execute and record a lien release.
5. Confirm release is recorded before or simultaneously with deed.

**Cost estimate:** Lien amount + any attorney fees + recording fee ($50-$200).

**Timeline:** 1-10 business days after settlement with claimant.

**Alternative -- Bond Off:**
1. Obtain a surety bond from a licensed surety company equal to 1.0x-1.5x the claimed lien amount (state law specifies the multiple).
2. File the bond with the county clerk; this substitutes the bond for the lien on the property.
3. The lien claimant now has a claim against the bond rather than the property.
4. Property is released from the lien; closing can proceed.
5. Dispute between lienor and obligor is resolved separately.

**Bond cost estimate:** 1-3% of the bond amount per year + attorney fees for filing.

**Bond timeline:** 1-5 business days if surety company is available.

---

### Judgment Lien -- Release

**Process:**
1. Confirm judgment debtor is the same party as the seller / prior owner in the chain. Judgment against John Smith does not attach to property owned by John Smith LLC.
2. Confirm the judgment is within the attachment period (typically 10 years; renewable in most states).
3. Calculate satisfaction amount: judgment principal + interest at statutory rate from judgment date.
4. Pay the judgment creditor (or their attorney); require a Satisfaction of Judgment to be filed with the court.
5. Court clerk issues the satisfaction; it is recorded in the judgment lien index.

**Cost estimate:** Judgment amount + accrued interest (8-9% per annum in many states) + attorney fees.

**Timeline:** 5-15 business days after payment for Satisfaction to be filed and recorded.

**Failure mode:** Judgment creditor is unreachable or disputes amount. Escrow sufficient funds at closing; require satisfaction to record within 30 days or title company can draw down escrow.

---

### Federal Tax Lien -- Certificate of Discharge

**Process:**
1. Confirm the federal tax lien is against the seller entity (not a prior owner -- if prior owner, lien may be expired if not renewed within 10 years).
2. File Form 14135 (Application for Certificate of Discharge of Property from Federal Tax Lien) with the IRS.
3. IRS reviews whether the sale proceeds allocable to the tax lien are sufficient to satisfy the lien (IRS has 30 days from application to act).
4. IRS issues Certificate of Discharge; property is released from the lien.
5. If the sale proceeds are insufficient: IRS may discharge the property but retain a claim against remaining proceeds (seller's net).

**Cost estimate:** No IRS fee. Legal fees for application preparation: $3,000-$10,000 depending on complexity.

**Timeline:** Standard: 30-45 days. Expedited (economic hardship showing): 15 days.

**Note:** IRS notice to the taxpayer and any subordinate lienholders is required. This becomes part of the closing disclosure to lender.

---

### Quiet Title Action

**When required:** Chain break that cannot be cured by affidavit, instrument recorded by a dissolved entity, adverse possession claim, or missing heir situation that cannot be resolved by heirship affidavit.

**Process:**
1. File petition for quiet title in the county where property is located.
2. Serve all parties with a potential interest (including unknown heirs, adjacent owners if applicable).
3. Publish notice in newspaper of general circulation for the statutory period (typically 4-6 weeks).
4. If uncontested: court enters default judgment quieting title in petitioner.
5. If contested: litigation proceeds; timeline and cost become unpredictable.
6. Record the court's final judgment; judgment is the new root of title.

**Cost estimate:** Uncontested: $8,000-$25,000 in legal fees + court costs + publication. Contested: $50,000+.

**Timeline:** Uncontested: 90-180 days. Contested: 12-36 months.

**Alternative to quiet title:** Some title companies will insure over a curable chain defect without quiet title if the underwriter's risk committee approves and a sufficiently large indemnity reserve is held in escrow. Discuss with title officer before assuming quiet title is the only path.

---

### Entity Retroactive Reinstatement

**When required:** Entity in the title chain (seller or prior owner) was administratively dissolved at the time of a transfer. Some state laws treat a deed from a dissolved entity as void.

**Process:**
1. Determine the state of organization of the dissolved entity.
2. File for retroactive reinstatement with the Secretary of State (or equivalent). Most states allow reinstatement if the entity pays outstanding fees and filings.
3. Once reinstated, the entity is treated as if it never dissolved (retroactive treatment varies by state).
4. Obtain a new Certificate of Good Standing post-reinstatement.
5. If the state does not allow retroactive reinstatement: quiet title may be required.

**States with favorable retroactive reinstatement:**
- Delaware: same-day reinstatement; retroactive to date of dissolution.
- Texas: retroactive reinstatement available; files with TX Secretary of State.
- Florida: retroactive reinstatement; franchise tax arrears must be paid.
- California: FTB must be paid; reinstatement effective retroactively.

**Cost estimate:** State filing fees ($50-$500) + any unpaid franchise taxes + legal fees ($500-$2,000).

**Timeline:** 1-30 days depending on state; Delaware is same-day.

---

### Tenant Estoppel and SNDA

**When required:** B-II exception for "rights of parties in possession" (tenants) is not acceptable to lender or buyer without confirmation that tenants acknowledge the lease as-is and agree to attorn to new owner.

**Estoppel process:**
1. Prepare estoppel form (usually lender-provided template for acquisitions with financing).
2. Send to each tenant with instructions; include the lease abstract and ask tenant to confirm accuracy.
3. Tenant signs and returns estoppel; if tenant notes exceptions, evaluate materiality.
4. Deliver to title company and lender.

**SNDA process:**
1. Lender provides SNDA form (Subordination, Non-Disturbance, Attornment Agreement).
2. Each major tenant must sign (typically tenants occupying > 5,000 SF or > 5% of GLA).
3. SNDA subordinates tenant's lease to lender's mortgage, commits tenant to attorn to new owner if lender forecloses, and lender commits not to disturb tenant's possession if tenant is not in default.
4. Execute at or before closing.

**Cost estimate:** Legal fees for estoppel and SNDA review: $500-$2,000 per tenant. Title company may require originals.

**Timeline:** Tenant estoppel: 5-21 business days per tenant (allow 30 days for contentious tenants). SNDA: 10-30 days per tenant (lender negotiation can extend).

---

## Endorsement Order Process

### Timing

- Order endorsements at commitment. Do not wait until closing.
- Title officer needs time to confirm eligibility (e.g., ALTA 3.1 requires zoning compliance letter from municipality, which takes 10-30 days).
- ALTA 9 requires a current ALTA/NSPS survey; if survey is not yet complete, endorsement cannot be issued.

### Order Checklist

```
At commitment:
  [ ] Identify all endorsements needed based on B-II review
  [ ] Send endorsement list to title officer with commitment number
  [ ] Confirm underwriter's endorsement availability for each item (not all underwriters
      issue all endorsements in all states)
  [ ] Confirm premium for each endorsement; include in closing cost estimate

During due diligence:
  [ ] Deliver ALTA/NSPS survey to title officer (enables ALTA 9, 22, 25)
  [ ] Obtain zoning compliance letter if ALTA 3.1 is ordered
  [ ] Confirm utility connections for ALTA 17.2
  [ ] Confirm all parcels contiguous for ALTA 19

At closing:
  [ ] Confirm all ordered endorsements are reflected in the final commitment update
  [ ] Confirm premium amounts match estimates
  [ ] Confirm simultaneous issue discount is applied if both policies are being issued
  [ ] File original policy and all endorsements in deal file immediately after closing
```

### Premium Calculation

Title insurance premiums are regulated by state and vary significantly. General approach:

```
Base premium: set by state rate schedule, typically as a rate per $1,000 of policy amount
  Example: $3.50 per $1,000 for first $1M, $2.50 per $1,000 for next $4M (illustrative)

Simultaneous issue discount: if owner's and lender's policies issued together, the smaller
  policy receives a 40-60% discount on the base premium (discount varies by state and underwriter)

Endorsement premiums: percentage of base premium or flat fee (see title-exception-categories.md)

Refinance credit: if subject property was insured within the prior 3-5 years (varies by state),
  a credit of 10-40% may apply on a refinance policy

Reissue credit: if a prior owner's policy was issued, a reissue rate may apply (10-15% discount)
```
