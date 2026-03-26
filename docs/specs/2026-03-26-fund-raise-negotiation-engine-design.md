# Fund Capital Raise Negotiation Engine -- Design Spec

> **For agentic workers:** This spec defines a new skill + calculator + state system for the CRE Skills Plugin. Use superpowers:writing-plans to create the implementation plan from this spec.

**Goal:** A stateful skill that tracks LP-by-LP capital raise negotiations, models fee concession impact in real-time (including MFN cascade), and maintains a persistent ledger across sessions so the IR team always has an accurate picture of their blended economics as commitments lock in.

**Target repo:** ~/Documents/GitHub/cre-skills-plugin/ (branch: feature/fund-raise-engine)

---

## Architecture

Three components:

1. **Skill** (`skills/fund-raise-negotiation-engine/SKILL.md`) -- the agent-facing methodology. Interrogates the user, manages negotiation state, produces analysis. 400+ lines following v2.0.0 skill conventions (frontmatter, interrogation protocol, branching, workflows, red flags, chain notes, computational tools).

2. **Calculator** (`scripts/calculators/fund_fee_modeler.py`) -- pure Python, zero dependencies. Accepts the full LP ledger as JSON stdin, computes: blended fee rate, dollar revenue, MFN cascade, GP promote sensitivity, breakeven analysis. Outputs structured JSON.

3. **State file** (`~/.cre-skills/fund-raises/{fund-id}.json`) -- persistent JSON ledger per fund. Tracks every LP's status, terms, side letter provisions, and commitment history. Supports CSV import/export via the calculator.

---

## Scope

### In Scope
- Fund setup (standard terms, target, hard cap, closes, MFN provisions)
- LP intake and tracking (prospect through funded, with branching: passed, stalled, reduced, re-opened)
- Side letter term capture (fee tiers, breaks, discounts, fee holidays, co-invest allocations, fee waivers, org expense caps, MFN clauses, custom provisions)
- Real-time scenario modeling ("what if I give LP X this concession?")
- MFN cascade analysis (which LPs ratchet, dollar impact, blended fee shift)
- GP promote sensitivity (how fee concessions affect net returns and promote breakeven)
- Multi-close support (first/second/final close, early closer discounts)
- Blended fee calculation across all committed LPs
- Revenue impact quantification (standard vs actual vs projected)
- Breakeven analysis (at what fund size does a concession become immaterial)
- CSV import/export for external spreadsheet workflows
- Persistent state across sessions (agent reads/writes JSON ledger)

### Out of Scope
- Actual legal document generation (side letter drafting -- use fund-formation-toolkit)
- SEC compliance (use sec-reg-d-compliance)
- LP pitch deck creation (use lp-pitch-deck-builder)
- Distribution calculations post-funding (use distribution-notice-generator)
- CRM/external system integration (v2.1+ consideration)

---

## State File Schema

```json
{
  "fundId": "string (kebab-case, unique per fund)",
  "fundName": "string",
  "targetRaise": "number (dollars)",
  "hardCap": "number (dollars)",
  "currency": "string (default USD)",
  "gpEntity": "string (GP legal name)",
  "vintage": "number (year)",
  "strategy": "string (core|core-plus|value-add|opportunistic)",
  "standardTerms": {
    "managementFee": "number (decimal, e.g., 0.015 = 1.50%)",
    "managementFeeBasis": "string (committed_capital|invested_capital|nav)",
    "feeStepDown": {
      "trigger": "string (investment_period_end|year_N|percent_deployed)",
      "rate": "number (decimal)",
      "basis": "string"
    },
    "carry": "number (decimal, e.g., 0.20 = 20%)",
    "preferredReturn": "number (decimal)",
    "waterfallType": "string (american|european)",
    "catchUp": "number (decimal, 0 = none, 1.0 = 100% GP catch-up)",
    "gpCommitment": "number (decimal, as % of fund)",
    "gpCommitmentType": "string (cash|fee_waiver|mixed)",
    "orgExpenseCap": "number (dollars)",
    "feeOffsetPercentage": "number (decimal, 1.0 = 100% offset)",
    "fundTerm": "number (years)",
    "investmentPeriod": "number (years)",
    "extensions": "number (1-year extensions allowed)"
  },
  "closes": [
    {
      "closeId": "string (first|second|final|interim-N)",
      "targetDate": "string (ISO date)",
      "actualDate": "string (ISO date, null if not yet closed)",
      "earlyCloserDiscount": "number (decimal, bps reduction from standard fee)",
      "status": "string (planned|open|closed)"
    }
  ],
  "mfnProvisions": {
    "enabled": "boolean",
    "scope": "string (most_favored|commitment_tier_matched|custom)",
    "excludeGPAffiliates": "boolean",
    "excludeFoundingLPs": "boolean",
    "excludeAnchorLPs": "boolean",
    "minimumCommitmentForMFN": "number (dollars, 0 = all LPs eligible)",
    "cascadeAutomatically": "boolean (if true, granting a concession auto-ratchets MFN holders)",
    "retroactiveAdjustment": "boolean (if true, existing MFN holders adjust to new floor)"
  },
  "investors": [
    {
      "lpId": "string (unique identifier)",
      "name": "string",
      "type": "string (pension|endowment|foundation|insurance|family_office|fund_of_funds|sovereign_wealth|hnw_individual|gp_affiliate|emerging_manager_program|other)",
      "tier": "string (anchor|strategic|standard|emerging|seed)",
      "status": "string (prospect|in_negotiation|verbal_commit|signed|funded|passed|stalled|reduced|re_opened)",
      "targetClose": "string (closeId reference)",
      "commitment": "number (dollars, current or target)",
      "originalCommitment": "number (dollars, if reduced from original)",
      "negotiatedTerms": {
        "managementFee": "number (decimal, null = standard terms apply)",
        "managementFeeTiers": [
          {
            "upTo": "number (dollars)",
            "rate": "number (decimal)"
          }
        ],
        "feeHoliday": {
          "months": "number",
          "reason": "string (early_closer|anchor_incentive|relationship|custom)"
        },
        "feeWaiver": {
          "type": "string (full|partial)",
          "duration": "string (investment_period|fund_life|custom)",
          "rate": "number (decimal, for partial waiver)"
        },
        "coInvestAllocation": "number (decimal, pro-rata share of co-invest)",
        "coInvestFee": "number (decimal, fee on co-invest, 0 = fee-free)",
        "orgExpenseCap": "number (dollars, null = standard cap applies)",
        "feeOffsetPercentage": "number (decimal, null = standard offset applies)",
        "carry": "number (decimal, null = standard carry applies)",
        "preferredReturn": "number (decimal, null = standard pref applies)",
        "mfnClause": "boolean",
        "blendedRateAcrossFunds": {
          "enabled": "boolean",
          "otherFunds": ["string (fundId references)"],
          "totalFamilyCommitment": "number (dollars)",
          "blendedRate": "number (decimal)"
        },
        "customProvisions": ["string (free text: advisory_committee_seat, quarterly_call_access, etc.)"]
      },
      "statusHistory": [
        {
          "status": "string",
          "date": "string (ISO date)",
          "amount": "number (dollars, if commitment changed)",
          "notes": "string"
        }
      ],
      "contactInfo": {
        "primaryContact": "string",
        "title": "string",
        "email": "string",
        "phone": "string"
      },
      "notes": "string (free text for relationship context)"
    }
  ],
  "lastUpdated": "string (ISO timestamp)",
  "version": "1.0.0"
}
```

---

## LP Status Flow

```
                              +-> Passed
                              |
Prospect -> In Negotiation ---+-> Stalled
                              |
                              +-> Verbal Commit --+-> Signed --+-> Funded
                                    |              |            |
                                    +-> Reduced    +-> Re-Opened
                                                   +-> Reduced
```

Multi-close assignment:
- Each LP is assigned to a target close (first, second, final, interim-N)
- Early closer discount is applied based on close assignment
- LPs can move between closes (e.g., slip from first to second)
- Close status: planned -> open -> closed

---

## Calculator Design (fund_fee_modeler.py)

### Input
Full state file JSON via stdin or --json argument.

### Commands (via --command flag)

**`dashboard`** -- Full fund raise dashboard (default)
```
FUND RAISE DASHBOARD: {fundName}
Target: ${targetRaise} | Hard Cap: ${hardCap} | Progress: ${totalCommitted} ({pct}%)

STATUS BREAKDOWN:
  Funded:          $XXM (N LPs)
  Signed:          $XXM (N LPs)
  Verbal Commit:   $XXM (N LPs)
  In Negotiation:  $XXM (N LPs)
  Prospect:        $XXM (N LPs)

BLENDED FEE ANALYSIS:
  Standard fee rate:                X.XX%
  Blended fee (funded+signed):      X.XX% (-XX bps)
  Blended fee (incl verbal):        X.XX% (-XX bps)
  Blended fee (all pipeline):       X.XX% (-XX bps projected)

  Annual fee revenue at standard:   $X,XXX,XXX
  Annual fee revenue at blended:    $X,XXX,XXX
  Concession cost:                  -$X,XXX,XXX/yr

MFN CASCADE STATUS:
  N LPs with MFN clauses
  Current MFN floor: X.XX% (set by {LP name})
  LPs at risk of ratchet: N (list)
  Potential cascade cost: -$XXX,XXX/yr

CLOSE SCHEDULE:
  {per-close breakdown with amounts and LP lists}

GP PROMOTE SENSITIVITY:
  At current blended fee: promote breakeven at XX.X% gross IRR
  At standard fee: promote breakeven at XX.X% gross IRR
  Promote delta over fund life: +/-$X.XM to GP
```

**`scenario`** -- What-if analysis (requires --lp-id and --proposed-fee or --proposed-terms JSON)
```
SCENARIO ANALYSIS: What if {LP name} gets {proposed terms}?

DIRECT IMPACT:
  Fee rate change: X.XX% -> X.XX% on ${commitment}
  Annual revenue impact: -$XXX,XXX

MFN CASCADE:
  Triggers N MFN ratchets:
    {LP name}: X.XX% -> X.XX% (MFN floor match) = -$XXX,XXX/yr
    {LP name}: X.XX% -> X.XX% (MFN floor match) = -$XXX,XXX/yr
  Total cascade cost: -$XXX,XXX/yr

TOTAL ANNUAL IMPACT: -$X,XXX,XXX/yr
BLENDED FEE SHIFT: X.XX% -> X.XX%

GP PROMOTE SENSITIVITY:
  Promote breakeven shifts: XX.X% -> XX.X% gross IRR
  Promote delta over fund life: +/-$X.XM

BREAKEVEN:
  This concession becomes immaterial (<1 bps blended impact) at fund size: $XXXM
  Current fund size: $XXXM ({pct}% of breakeven)

RECOMMENDATION:
  {Counter-offer suggestion if cascade cost is high}
  {Flag if concession creates new MFN floor}
```

**`mfn-audit`** -- Full MFN cascade analysis
```
MFN AUDIT: {fundName}

CURRENT MFN FLOOR: X.XX% (set by {LP name}, ${commitment})

MFN-ELIGIBLE LPs:
  {table: LP name, current rate, MFN-eligible (Y/N), would ratchet (Y/N), cost if ratcheted}

HISTORICAL MFN EVENTS:
  {timeline of when MFN floor changed and which LPs were affected}

EXPOSURE:
  If next LP negotiates X.XX%: N ratchets, $XXX,XXX/yr additional cost
  If next LP negotiates X.XX%: N ratchets, $XXX,XXX/yr additional cost
  If next LP negotiates X.XX%: N ratchets, $XXX,XXX/yr additional cost
```

**`export-csv`** -- Export LP ledger to CSV for spreadsheet use
**`import-csv`** -- Import LP data from CSV (merge with existing state)

### Computation Methods

**Blended fee calculation:**
For each LP with status in (signed, funded, verbal_commit):
- Determine effective fee rate (negotiated or standard, minus early closer discount, minus fee holiday amortization)
- Weight by commitment amount
- Blended = sum(commitment_i * effective_rate_i) / sum(commitment_i)

**MFN cascade:**
- Find the lowest fee rate granted to any non-excluded LP (the MFN floor)
- For each LP with mfnClause=true: if their effective rate > MFN floor, they ratchet to the floor
- Calculate the dollar impact of each ratchet
- If retroactiveAdjustment=true, this applies to already-signed LPs

**Fee holiday amortization:**
- Fee holiday grants N months of zero management fee
- Amortize the holiday value over the fund term for blended rate calculation
- Effective annual rate = (fund_term_months - holiday_months) / fund_term_months * negotiated_rate

**GP promote sensitivity:**
- Lower blended fees = lower fund expenses = higher net returns to LPs
- Model the promote waterfall at different net return levels
- Calculate the gross IRR needed to reach preferred return hurdle at each fee level
- Promote breakeven = gross IRR where net IRR = preferred return

**Blended rate across fund family:**
- Some LPs commit across multiple funds from the same GP
- Blended rate calculated on total family commitment, not per-fund
- Requires cross-referencing otherFunds in the LP's negotiatedTerms

---

## Skill Design (fund-raise-negotiation-engine/SKILL.md)

### Frontmatter
```yaml
---
name: fund-raise-negotiation-engine
slug: fund-raise-negotiation-engine
version: 0.1.0
status: deployed
category: reit-cre
subcategory: investor-relations
description: "Tracks LP-by-LP capital raise negotiations with persistent state, models fee concession impact in real-time including MFN cascade analysis, and maintains a live ledger of blended fund economics as commitments lock in. Scales from 10-LP seed funds to 300+ LP institutional raises."
targets: [claude_code]
stale_data: "Fee benchmarks and market norms reflect mid-2025 institutional fundraising market. Verify current benchmarks with placement agents."
---
```

### Branching Logic
- **Fund size:** Seed (<$100M, 10-30 LPs, simpler terms) vs Mid-market ($100M-$500M, 30-100 LPs, standard institutional) vs Large ($500M+, 100-300+ LPs, complex tiering with anchor economics)
- **Strategy:** Core (lower fees, higher commitment thresholds) vs Value-add/Opportunistic (higher fees, more fee negotiation)
- **GP maturity:** First fund (less leverage, LPs dictate terms) vs Established (GP has leverage, can hold on fees)
- **Close structure:** Single close vs Multi-close (affects early closer discounts and MFN timing)

### Interrogation Protocol (10 questions)
1. "What fund are we tracking? (New fund or existing raise?)" -- checks for existing state file
2. "Fund name, target raise, and hard cap?"
3. "What's the standard management fee and basis? (e.g., 1.50% on committed capital)"
4. "Fee step-down after investment period? (rate and basis)"
5. "Carry structure? (rate, preferred return, waterfall type, catch-up)"
6. "GP commitment amount and type? (cash, fee waiver, or mixed)"
7. "How many closes planned? (Dates and early closer discounts)"
8. "MFN provisions? (Scope, exclusions, cascade behavior, retroactive)"
9. "Are there any LPs already in the pipeline? (I can import from CSV)"
10. "What's the org expense cap and fee offset percentage?"

### Workflows (7)

**Workflow 1: Fund Setup**
- Create state file at ~/.cre-skills/fund-raises/{fund-id}.json
- Capture all standard terms, close schedule, MFN provisions
- Validate: target <= hard cap, fee rates reasonable (0.50%-2.50%), GP commitment >= 1%
- Output: confirmation summary with standard terms table

**Workflow 2: LP Intake**
- Add new LP to tracker at prospect stage
- Capture: name, type, tier, target commitment, contact info, notes
- Auto-suggest tier based on commitment size (anchor >15% of target, strategic 5-15%, standard 1-5%, emerging <1%)
- Output: LP added confirmation, current pipeline summary

**Workflow 3: Negotiation Update**
- Advance LP status (prospect -> in_negotiation -> verbal_commit -> signed -> funded)
- Capture negotiated terms at each stage (fee rate, fee tiers, holiday, co-invest, MFN, custom provisions)
- Handle branching: passed (capture reason), stalled (capture blocker), reduced (capture new amount and reason), re-opened (capture what changed)
- Auto-log status history with timestamp
- Output: updated LP card, pipeline impact summary

**Workflow 4: Scenario Modeling (the core value)**
- User asks: "What if I give [LP] [these terms]?"
- Run calculator in scenario mode WITHOUT modifying state
- Show: direct fee impact, MFN cascade (which LPs ratchet, dollar cost), blended fee shift, revenue delta, promote sensitivity, breakeven fund size
- Suggest counter-offers if cascade cost exceeds threshold
- Flag if proposed terms create a new MFN floor
- Output: full scenario analysis (see calculator output above)

**Workflow 5: Commitment Lock-In**
- Move LP from verbal to signed (or funded)
- Apply negotiated terms permanently to the ledger
- Trigger MFN recalculation across all MFN-holding LPs
- If cascade occurs: report which LPs ratcheted and the aggregate cost
- Update blended fee, revenue projections, close schedule
- Output: lock-in confirmation, updated dashboard, MFN cascade report (if triggered)

**Workflow 6: Close Management**
- Assign LPs to closes, calculate early closer discounts
- Track close progress: projected vs actual amounts
- Handle close date changes (slip from first to second)
- Calculate close-by-close fee revenue (different LPs at different rates)
- Output: close schedule with LP assignments, projected amounts, fee revenue by close

**Workflow 7: Reporting and Export**
- Full dashboard (see calculator output)
- MFN audit report
- CSV export (LP ledger with all fields)
- CSV import (merge new LPs or update existing)
- Summary memo for fund principal/IC (one-page: raise progress, blended economics, key negotiations, MFN exposure)
- Fee waterfall by LP (table: LP, commitment, standard fee, negotiated fee, discount, annual fee revenue, % of total fees)

### Red Flags (9)

1. **Blended fee below GP breakeven**: if blended management fee drops below the level needed to cover fund operating expenses + GP overhead, the fund economics don't work. Flag when blended fee * total commitments < annual operating budget.

2. **MFN cascade consuming >20% of fee concession value**: if granting one LP a discount triggers cascading ratchets that cost 2x+ the direct concession, the GP is giving away too much. Recommend restructuring MFN provisions or excluding the LP from MFN scope.

3. **Anchor LP getting >50bps below standard**: concessions beyond 50bps create a deep MFN floor that constrains all future negotiations. Flag and suggest tiered rates or non-fee concessions (co-invest, advisory seat) instead.

4. **More than 30% of LPs with MFN clauses**: creates a fragile fee structure where any single concession cascades widely. Recommend capping MFN eligibility to commitments above a threshold.

5. **Fee holiday exceeding 12 months**: extended fee holidays materially reduce fund economics and set precedent. Flag if total fee holidays across all LPs exceed 6% of fund-year revenue.

6. **GP commitment via fee waiver >50% of total GP commit**: institutional LPs increasingly scrutinize GP commitment quality. Fee waiver commitments should be flagged and quantified as a % of total GP commit.

7. **Hard cap at risk**: if signed + verbal exceeds hard cap, some LPs will need to be reduced. Flag when pipeline exceeds 90% of hard cap.

8. **Close timeline slippage**: if target close dates are approaching with insufficient committed capital, flag the gap and recommend acceleration tactics.

9. **Retroactive MFN adjustment on already-funded LPs**: if a late-closing LP negotiates a lower fee and MFN provisions are retroactive, the GP may owe refunds to early closers. Quantify the exposure.

### Reference Files (3)

**references/fee-negotiation-playbook.md**
- Standard concession tiers by LP size (anchor, strategic, standard)
- Non-fee concessions that preserve economics (co-invest, advisory committee, reporting, LPAC seat)
- Negotiation sequencing (anchor first, then fill, then MFN cleanup)
- When to hold vs when to concede (market-dependent)
- Common GP mistakes in fee negotiations

**references/mfn-cascade-mechanics.md**
- How MFN provisions work (scope, exclusions, triggers)
- Worked example with 10 LPs showing cascade math
- Strategies for limiting MFN exposure (tier-matching, commitment floors, anchor exclusions)
- Side letter provisions that interact with MFN (co-invest, fee offset, org expense)

**references/blended-fee-benchmarks.yaml**
- Market blended fee rates by strategy and fund size (Preqin/Cambridge data ranges)
- Typical concession ranges by LP commitment size
- Early closer discount norms
- GP commitment benchmarks
- Org expense cap ranges
- Fee step-down timing and rate benchmarks

### Chain Notes
- **Upstream:** capital-raise-machine (raise operations), fund-formation-toolkit (fund structure and terms), fund-terms-comparator (market benchmarks for negotiation positioning)
- **Downstream:** distribution-notice-generator (distributions use actual negotiated terms per LP), quarterly-investor-update (reporting reflects actual fee structure), deal-attribution-tracker (fund-level economics fed by actual fee structure)
- **Lateral:** jv-waterfall-architect (promote calculations informed by net fee structure), sec-reg-d-compliance (offering compliance), lp-pitch-deck-builder (pitch reflects standard terms, not negotiated)
- **Brand:** brand-config auto-loads for IC summary memos and LP-facing reports

### Computational Tools
```bash
# Full dashboard
python3 scripts/calculators/fund_fee_modeler.py --command dashboard --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

# Scenario: what if CalPERS gets 1.10%?
python3 scripts/calculators/fund_fee_modeler.py --command scenario --lp-id calpers-001 --proposed-fee 0.011 --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

# MFN audit
python3 scripts/calculators/fund_fee_modeler.py --command mfn-audit --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)"

# Export to CSV
python3 scripts/calculators/fund_fee_modeler.py --command export-csv --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)" > fund-v-ledger.csv

# Import from CSV
python3 scripts/calculators/fund_fee_modeler.py --command import-csv --csv fund-v-ledger.csv --json "$(cat ~/.cre-skills/fund-raises/meridian-fund-v.json)" > updated-state.json
```

---

## Testing Strategy

1. **Calculator unit tests**: blended fee calculation with known inputs, MFN cascade with worked example, promote sensitivity math, CSV round-trip (export then import)
2. **State file validation**: malformed JSON handling, missing fields with defaults, status transition validation
3. **Edge cases**: single LP fund, LP at exact MFN floor (no ratchet), fee holiday spanning close dates, blended rate across fund family with missing cross-references
4. **Integration**: scenario modeling then lock-in (verify scenario numbers match post-lock-in dashboard)

---

## Implementation Notes

- State file directory `~/.cre-skills/fund-raises/` created on first fund setup (mirrors telemetry pattern)
- Calculator must handle funds with 0 committed LPs (empty dashboard, not crash)
- CSV export includes all fields; CSV import is merge-mode (updates existing LPs by lpId, adds new ones)
- MFN cascade is recalculated on every lock-in AND on every scenario run
- Scenario mode NEVER modifies state file (read-only analysis)
- All dollar amounts stored as integers (cents) internally, displayed as formatted dollars
- Dates stored as ISO 8601 strings
