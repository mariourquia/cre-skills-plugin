# Fund Compliance Framework Reference

Regulatory compliance requirements for closed-end real estate private equity funds operating under Regulation D exemptions. Covers Form D filings, AML/KYC, side letter tracking, LPAC governance, and regulatory calendars. All examples use a baseline $250M fund (Fund IV) with 35 LPs, 506(b) exemption, and SEC-registered adviser.

---

## 1. Regulation D Compliance

### 506(b) vs 506(c) Requirements

| Requirement | 506(b) | 506(c) |
|---|---|---|
| Maximum non-accredited investors | 35 (sophisticated) | 0 (none permitted) |
| General solicitation | Prohibited | Permitted |
| Accredited investor verification | Self-certification acceptable | Reasonable steps required (third-party verification) |
| Disclosure requirements | Material info to non-accredited | No specific requirement (but anti-fraud applies) |
| Bad actor disqualification | Applies | Applies |
| Form D filing | Required | Required |
| Preemption of state registration | Yes (with notice filing) | Yes (with notice filing) |

### Accredited Investor Verification Methods

**For 506(b) -- self-certification**:
```
Acceptable verification:
  - LP representation in subscription agreement
  - Investor questionnaire completed and signed
  - No independent verification required
  - Must have reasonable belief that LP is accredited
```

**For 506(c) -- reasonable steps required**:
```
Individual (income test -- $200K/$300K joint, 2 of last 3 years):
  - Tax returns (2 most recent years) + written representation for current year
  - W-2s, 1099s, K-1s (2 most recent years) + written representation
  - Written confirmation from CPA, attorney, broker-dealer, or registered investment adviser

Individual (net worth test -- $1M excluding primary residence):
  - Third-party verification from CPA, attorney, or broker-dealer
  - Bank/brokerage statements (within 90 days) + credit report
  - Appraisal of assets + statements of liabilities

Entity (assets > $5M):
  - Audited or unaudited financial statements (most recent fiscal year)
  - Tax return showing assets
  - Third-party confirmation

Qualified purchaser ($5M+ in investments, individual; $25M+ entity):
  - Same methods as accredited, plus confirmation of investment portfolio value
  - For fund-of-funds or institutional investors: most recent audited financial statements
```

### Bad Actor Disqualification Check

```
Must screen the following "covered persons" for disqualifying events:
  1. The issuer (fund entity)
  2. Directors, officers, general partners of the issuer
  3. Managing members of the GP entity
  4. 20%+ equity holders of the issuer
  5. Promoters connected to the offering
  6. Persons compensated for solicitation (placement agents)
  7. Directors, officers, general partners of any compensated solicitor

Disqualifying events (look-back varies by event type):
  - Felony or misdemeanor conviction related to securities (10-year lookback)
  - Court injunction related to securities (5-year lookback, or if still in effect)
  - SEC disciplinary order (varies)
  - SEC cease-and-desist order (5-year lookback)
  - Suspension/expulsion from SRO membership
  - SEC stop order on registration statement (5-year lookback)
  - USPS false representation order (5-year lookback)

Screening frequency:
  - At fund formation (all covered persons)
  - At each closing (new covered persons, if any)
  - When GP personnel changes
  - Annually as best practice

Documentation:
  - Bad actor questionnaire completed by each covered person
  - Background check results on file
  - Written certification from fund counsel that no disqualifying events exist
```

### Form D Filing Requirements

```
Initial Filing:
  Due: 15 calendar days after first sale of securities
  Filed with: SEC EDGAR system
  Content: fund name, GP, offering amount, investors, exemption claimed

  Required information:
    - Issuer identity and address
    - Related persons (GP, managing members, executive officers)
    - Industry group (pooled investment fund)
    - Type of security (limited partnership interest, LLC interest)
    - Exemption claimed (Rule 506(b) or 506(c))
    - Offering amount (or "indefinite" if not fixed)
    - Amount sold to date
    - Number of investors
    - Sales commissions and finder's fees
    - Use of proceeds (describe investment strategy)

Annual Amendment:
  Due: within 30 days of each anniversary of initial filing
  Content: update all fields, particularly:
    - Total amount sold (updated for subsequent closings)
    - Number of investors (updated)
    - Any changes to related persons

Material Change Amendment:
  Due: within 30 days of material change
  Material changes include:
    - New GP or managing member
    - Change in exemption relied upon
    - Change in offering amount > 10%
    - Change in issuer name or address

Termination Filing:
  Due: after final close and all subscriptions are complete
  Signals that the offering is complete

Failure to file:
  - SEC can revoke Reg D exemption (loss of safe harbor, not necessarily loss of exemption)
  - State securities regulators may take enforcement action
  - Practical impact: institutional LPs will not invest in a fund with delinquent filings
```

### State Blue Sky Requirements

```
Federal preemption: Section 18(b)(4)(F) of the Securities Act preempts state
registration requirements for 506 offerings. However, states may:
  1. Require notice filing (Form D + state-specific form)
  2. Charge a filing fee
  3. Require consent to service of process

State filing requirements (examples):
  New York:       No notice filing required
  California:     Form D filing within 15 days of first CA sale, $300 fee
  Texas:          Form D filing within 15 days, $300 fee
  Florida:        No notice filing required
  Illinois:       Form D filing within 15 days, fee based on offering amount
  Connecticut:    Form D filing within 15 days, $150 fee
  Massachusetts:  Form D filing within 15 days, fee based on offering amount
  New Jersey:     Form D filing within 10 days (shorter deadline), $100 fee

Best practice: file in all states where LPs are located within 15 days
of closing. Maintain a state filing tracker with deadlines and confirmations.

Worked example for Fund IV ($250M, 35 LPs across 12 states):
  Total state filing fees (estimated): $3,200-$5,500
  Filing deadline: 15 days after each closing
  States requiring filing: CA, TX, IL, CT, MA, NJ, PA, GA, CO, MD, VA, NC
  States not requiring filing: NY, FL
```

---

## 2. AML/KYC Verification Framework

### Customer Identification Program (CIP) Requirements

```
Individual LPs:
  Required information:
    1. Full legal name
    2. Date of birth
    3. Address (residential, not P.O. Box)
    4. Government-issued ID number (SSN or passport)

  Verification methods:
    - Government-issued photo ID (passport, driver's license)
    - Social Security verification
    - Utility bill or bank statement (address verification)
    - For non-US persons: passport + W-8BEN

Entity LPs:
  Required information:
    1. Full legal name and form of organization
    2. Address (principal place of business)
    3. EIN or equivalent tax ID
    4. Formation documents (certificate of incorporation, partnership agreement)

  Beneficial ownership (FinCEN CDD Rule):
    - Identify all individuals with 25%+ equity ownership
    - Identify one individual with significant management control
    - Collect CIP information for each beneficial owner
    - For multi-tier structures: look through to natural person level

  Entity-specific documents:
    - Corporation: articles of incorporation, board resolution authorizing investment
    - Partnership: partnership agreement, GP authorization
    - Trust: trust agreement, trustee authorization
    - IRA/pension: plan document, authorized signatory verification
    - Fund-of-funds: offering memorandum, authorized signatory
```

### Sanctions Screening

```
Required screens (run against all LPs and beneficial owners):

  1. OFAC Specially Designated Nationals (SDN) List
     Source: https://sanctionssearch.ofac.treas.gov/
     Frequency: at subscription, quarterly, and before each distribution

  2. OFAC Consolidated Sanctions List
     Includes: sectoral sanctions, non-SDN lists
     Frequency: same as SDN

  3. EU Consolidated Sanctions List
     Required if: fund has EU-based LPs or EU-nexus investments
     Frequency: at subscription and semi-annually

  4. UN Security Council Consolidated List
     Required if: fund has international investors
     Frequency: at subscription and annually

  5. PEP (Politically Exposed Persons) Database
     Commercial providers: World-Check, Dow Jones, LexisNexis
     Frequency: at subscription and annually
     Note: PEP status does not automatically disqualify, but requires
           enhanced due diligence and senior management approval

Hit resolution:
  - Potential match: do not proceed with subscription until resolved
  - True match: reject subscription, file SAR (Suspicious Activity Report)
  - False positive: document resolution, maintain in file

Worked example:
  LP: "Hassan Al-Rashid Investment Group LLC"
  OFAC screening result: potential match on SDN list
  Resolution: full name comparison shows SDN entry is "Hassan Al-Rashid" (individual)
              located in Syria. LP is a Delaware LLC with UAE beneficial owner
              named "Hassan Al-Rashid bin Mohammed" -- different person.
              Verified via passport, address, and date of birth mismatch.
              Result: FALSE POSITIVE. Document and proceed with enhanced monitoring.
```

---

## 3. Side Letter Tracking and MFN Compliance

### Common Side Letter Provisions

| Provision | Description | MFN Eligible? | Tracking Frequency |
|---|---|---|---|
| Fee discount | Reduced management fee rate | Yes | Quarterly (fee calc) |
| Co-investment rights | Right to participate in co-investments | Yes | Per deal |
| Most Favored Nation | Right to receive any better terms given to other LPs | N/A (is the MFN) | Each closing |
| Reporting enhancements | Additional or more frequent reports | Typically no | Per report cycle |
| ESG exclusions | Ability to opt out of certain investments | Typically no | Per deal |
| Transfer restrictions | Modified transfer provisions | Varies | Per transfer event |
| Tax reporting | Enhanced tax reporting (e.g., PFIC, UBTI) | Typically no | Annually |
| Key person notification | Enhanced notification of key person events | Varies | Per event |
| Advisory committee seat | Designated LPAC seat | No | At formation |
| Excuse rights | Right to not participate in certain investments | Varies | Per deal |

### MFN Compliance Process

```
Step 1: Compile master side letter matrix
  - List every LP with a side letter
  - Catalog every provision by category
  - Mark which provisions are MFN-eligible vs. LP-specific

Step 2: After each closing, identify new MFN-eligible terms
  - Compare new LP side letter provisions to existing matrix
  - Any new provision that is more favorable than existing terms is a
    potential MFN trigger

Step 3: Notify MFN-eligible LPs
  - Per LPA requirements (typically within 30-60 days of closing)
  - Provide summary of available MFN terms (redacted for LP identity)
  - LPs elect which provisions they wish to receive
  - Track election deadline and follow up

Step 4: Update allocation model
  - If LP elects a fee discount via MFN, update fee calculation
  - If LP elects co-invest rights, add to co-invest notification list
  - Document all MFN elections in fund records

Worked example:
  Fund IV first close: 12 LPs, 3 with side letters
    LP A ($50M): 25bp fee discount, co-invest rights
    LP B ($40M): co-invest rights, LPAC seat
    LP C ($30M): 15bp fee discount, excuse rights for gaming assets

  MFN-eligible LPs at first close: LP A, LP B, LP C (all have MFN clause)
  Best fee term: 25bp discount (LP A)
  MFN notification: LP B and LP C can elect 25bp discount
  LP B elects: 25bp fee discount (exercises MFN)
  LP C declines: prefers 15bp discount (already has it, net benefit of
                 additional 10bp not worth exercising MFN on other terms)

  Fund IV second close: 8 additional LPs, 2 with side letters
    LP D ($35M): 30bp fee discount, enhanced reporting
    LP E ($25M): co-invest rights

  New MFN trigger: LP D's 30bp discount is better than LP A's 25bp
  MFN notification to all prior MFN-eligible LPs (A, B, C):
    - LP A can upgrade from 25bp to 30bp
    - LP B can upgrade from 25bp (elected via MFN) to 30bp
    - LP C can upgrade from 15bp to 30bp

  Fee impact analysis:
    Before MFN: total fee discount = $50M*25bp + $40M*25bp + $30M*15bp + $35M*30bp = $307,500/yr
    After MFN (worst case, all elect): = $50M*30bp + $40M*30bp + $30M*30bp + $35M*30bp = $465,000/yr
    Incremental fee revenue loss: $157,500/yr
```

---

## 4. LPAC Governance Procedures

### LPAC Composition and Authority

```
Typical LPAC structure:
  - 3-7 members selected from LP investor base
  - Mix of large LPs, institutional LPs, and independent members
  - Chair elected by LPAC members or designated in LPA
  - Term: life of fund or as specified in LPA

Matters requiring LPAC consent (typical LPA provisions):
  1. Conflicts of interest (GP or affiliate transactions)
  2. Valuation methodology changes
  3. Fund term extensions
  4. Key person replacement
  5. Investment period resumption after suspension
  6. Transactions with affiliates of the GP
  7. Co-investment allocation policy changes
  8. Material changes to fund expense policy
  9. GP removal for cause proceedings
  10. Changes to investment guidelines or restrictions

Matters for LPAC information (not consent):
  1. Portfolio company updates
  2. Market conditions and strategy updates
  3. Regulatory or legal developments
  4. Upcoming capital call/distribution schedule
  5. Key personnel departures (if not key person event)
```

### LPAC Meeting Procedures

```
Meeting scheduling:
  - Quarterly minimum per most LPAs
  - Special meetings upon request of GP or majority of LPAC members
  - Notice period: typically 10-15 business days
  - Materials distributed: 5-7 business days before meeting

Agenda template:
  1. Call to order and quorum confirmation
  2. Approval of prior meeting minutes
  3. GP update (portfolio, market, strategy)
  4. Consent items (if any)
  5. Information items
  6. Conflicts disclosure
  7. Valuation review (annual or as needed)
  8. New business
  9. Executive session (without GP)
  10. Adjournment

Quorum: typically majority of members (e.g., 3 of 5)
Voting: typically one vote per member, majority rules
Recusal: members must recuse from votes where they have a conflict

Minutes documentation:
  - Record attendance, quorum status
  - Summarize each agenda item discussion (not verbatim)
  - Record all votes with results (for/against/abstain/recused)
  - Note any action items with responsible party and deadline
  - Minutes reviewed and approved at next meeting
  - Maintain in fund records for life of fund + 5 years minimum
```

---

## 5. Regulatory Calendar Template

### Annual Compliance Calendar (Fund IV, Fiscal Year = Calendar Year)

```
January:
  [ ] Q4 capital account statements to LPs (due 45 days after quarter-end)
  [ ] Q4 management fee calculation and collection
  [ ] Annual OFAC/sanctions re-screening (all LPs)
  [ ] Annual PEP re-screening (all LPs)
  [ ] Beneficial ownership re-verification (entity LPs)
  [ ] Annual side letter compliance audit
  [ ] Insurance policy renewals review
  [ ] Annual LPAC meeting scheduling

February:
  [ ] Q4 capital account statements distributed (by Feb 15)
  [ ] K-1 preparation coordination with tax accountant
  [ ] Annual financial statement audit begins (PBC list to auditor)
  [ ] Form ADV annual amendment preparation (if registered adviser)

March:
  [ ] K-1 distribution to LPs (target: March 15; LPA deadline: varies)
  [ ] Form ADV annual amendment filing (due March 31, 90 days after FYE)
  [ ] Form PF annual filing (if applicable, due within 120 days of FYE)
  [ ] Annual audited financial statements (target: March 31)
  [ ] Q1 LPAC meeting

April:
  [ ] Q1 capital account statements preparation
  [ ] Q1 management fee calculation
  [ ] Annual Form D amendment (if anniversary falls in April)
  [ ] State Blue Sky renewal filings (as applicable)
  [ ] Distribute audited financial statements to LPs (due 120-180 days after FYE)

May-June:
  [ ] Q1 capital account statements distributed
  [ ] Q2 LPAC meeting
  [ ] Mid-year portfolio valuation review
  [ ] Insurance certificate renewals tracking (all subs and service providers)

July:
  [ ] Q2 capital account statements preparation
  [ ] Q2 management fee calculation
  [ ] Semi-annual compliance review (internal)
  [ ] OFAC re-screening (if semi-annual policy)

August-September:
  [ ] Q2 capital account statements distributed
  [ ] Q3 LPAC meeting
  [ ] Annual budget preparation for next fiscal year
  [ ] Fund expense ratio mid-year check

October:
  [ ] Q3 capital account statements preparation
  [ ] Q3 management fee calculation
  [ ] Annual Form D amendment (if anniversary falls in October)
  [ ] Year-end planning: distributions, capital calls, extensions

November-December:
  [ ] Q3 capital account statements distributed
  [ ] Q4 LPAC meeting
  [ ] Year-end valuation process initiated
  [ ] Tax planning coordination with fund accountant
  [ ] AML/KYC expiry review (identify renewals due in Q1)
  [ ] Compliance calendar update for next year
```
