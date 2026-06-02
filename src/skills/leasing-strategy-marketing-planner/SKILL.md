---
name: leasing-strategy-marketing-planner
slug: leasing-strategy-marketing-planner
version: 0.1.0
status: deployed
category: reit-cre
description: "Create leasing marketing materials, plan broker events, benchmark TI costs and commissions, and develop property marketing plans. Use when a user needs to build a leasing flyer, plan a broker open house, determine TI allowances, set commission structures, or create an annual leasing marketing strategy for office, retail, or industrial properties."
user-invocable: true
triggers:
  - "marketing plan"
  - "leasing strategy"
  - "broker event"
  - "TI allowance"
  - "commission structure"
  - "leasing flyer"
  - "CoStar listing"
  - "leasing budget"
  - "tenant improvement cost"
  - "broker commission"
targets:
  - claude_code
---

# Leasing Strategy & Marketing Planner

Develop leasing strategies, create marketing materials, plan broker events, benchmark TI costs and commissions, and drive leasing velocity across office, retail, and industrial portfolios.

## When to Activate

- User needs marketing materials (flyers, brochures, listing copy) for available spaces
- User is planning a broker event, open house, or market update
- User needs TI cost benchmarking or allowance determination
- User wants an annual or property-specific marketing plan with budget allocation
- User needs commission structure analysis or listing agreement negotiation guidance

**Do NOT activate for:**
- Lease document drafting or amendment — use `lease-document-factory`
- Lease-up funnel diagnostics or absorption tracking — use `lease-up-war-room`
- Rent optimization or concession modeling — use `rent-optimization-planner`

## Input Schema

| Field | Required | Default if Missing |
|-------|----------|--------------------|
| workflow_step (marketing_material / broker_event / ti_benchmarking / marketing_plan / commission_benchmarking) | Yes | Infer from request |
| property_name | Yes | Ask user |
| property_type (office / retail / industrial / mixed-use) | Yes | Ask user |
| total_sf | Yes | Ask user |
| available_sf | Yes | Estimate from vacancy_rate if provided |
| vacancy_rate | No | Calculate from available_sf / total_sf |
| asking_rent ($/SF) | No | Use market_rent if available |
| location (city, submarket) | Yes | Ask user |
| class (A / B / C) | No | Infer from asking_rent and year_built |

Additional inputs by workflow step — see [input-schema-detail.yaml](references/input-schema-detail.yaml) for the full schema including `available_spaces`, `market_context`, `budget`, and `brand_guidelines` fields.

If fewer than 3 required fields are present, ask clarifying questions.

## Process

### Step 0: Load Brand Guidelines (Auto)

Check `~/.cre-skills/brand-guidelines.json`. If missing, prompt: "Would you like to set up brand guidelines with `/cre-skills:brand-config`? Or I can proceed with professional defaults." Apply loaded or default guidelines (navy #1B365D, white #FFFFFF, gold #C9A84C, Helvetica Neue/Arial) to all deliverables.

### Step 1: Marketing Material Creation

1. **Define target audience** for each available space: size range, industry vertical, credit quality, growth stage, location drivers.
2. **Develop content** — benefit-led headline (not feature-led), 3-5 differentiators vs. competitive set, space specs, amenity package, financial summary (asking rent, NNN, TI, move-in date).
3. **Format by channel**: CoStar/LoopNet (SEO-optimized, photos, floor plans), print flyer (one-page front/back, QR code), brochure (4-8 pages with market context), digital (email blast template, LinkedIn, website), signage.
4. **Quality gate**: Professional photography, consistent brand identity, accurate SF/rent, legal review of claims.

### Step 2: Broker Event Planning

1. **Select format** — broker open house (new availability), market update breakfast ($15-25/person), exclusive preview (5-10 targeted brokers), or tenant appreciation event.
2. **Plan logistics** — venue, F&B budget, invitations 4 weeks out with 2-week and 1-week follow-up, collateral and tech.
3. **Execute follow-up** — thank-you email within 24 hours, personal calls to top 10 attendees within 1 week, track tours generated within 30/60/90 days, calculate ROI.

### Step 3: TI Cost Benchmarking

1. **Classify space condition** — cold shell, warm shell, move-in ready (spec suite), or second-generation. See [ti-cost-benchmarks.yaml](references/ti-cost-benchmarks.yaml) for market-appropriate cost ranges.
2. **Determine allowance** based on: competing building offers, lease economics (amortize at target return), tenant credit, lease term, space condition.
3. **Run amortization analysis**:
   ```
   Monthly TI Amortization = TI Amount / PV Annuity Factor (rate, months)
   Effective Rent = Face Rent - (Monthly Amortization x 12 / Lease SF)
   ```
   Verify effective rent meets or exceeds underwriting target.

### Step 4: Marketing Plan Development

1. **Situation analysis** — vacancy, expiring leases, pipeline, competitive landscape, market trajectory.
2. **Define target tenant profiles** per available space block (industry, size, credit, growth stage, location sensitivity). See [marketing-plan-template.md](references/marketing-plan-template.md) for the full template.
3. **Allocate budget by channel** — digital listings (15-25%), broker co-op (20-30%), direct mail/email (5-10%), digital ads (10-15%), signage (10-15%), PR (5-10%), events (10-20%).
4. **Set quarterly calendar** — Q1 launch, Q2 peak touring, Q3 LOI push, Q4 year-end close.
5. **Define KPIs** — inquiries, tours, proposals, LOIs, leases signed (SF and count), days on market, conversion rates (inquiry→tour→proposal→lease).

### Step 5: Commission Structure Benchmarking

1. **Compile market rates** by property type and deal type. See [commission-benchmarks.yaml](references/commission-benchmarks.yaml).
2. **Evaluate structures** — standard percentage, flat fee, speed/SF accelerators, listing override.
3. **Negotiate listing agreement terms** — commission rate and split, protected tenant list, term/termination, tail period (6-12 months), marketing obligations.
4. **Project commission budget**:
   ```
   Projected Commission = Absorption Target (SF) x Avg Rent x Avg Term x Commission Rate
   ```
   Include renewal commissions (typically 50% of new deal rate).

## Output Format

```markdown
## [Workflow Step] -- [Property Name]

### Executive Summary
[2-3 sentences: objective, recommended strategy, expected outcome]

### Market Context
| Metric | Property | Submarket | Delta |
|--------|----------|-----------|-------|
| Vacancy | XX% | XX% | +/-XX% |
| Asking Rent | $XX/SF | $XX/SF | +/-$X |
| Net Absorption (T12) | XX,XXX SF | XX,XXX SF | |

### [Workflow-Specific Analysis]
[Detailed analysis per process steps]

### Budget Allocation
| Channel | Budget | % of Total | Expected ROI |
|---------|--------|-----------|-------------|
| [Channel 1] | $XX,XXX | XX% | |
| [Channel 2] | $XX,XXX | XX% | |

### KPI Targets
| Metric | Q1 | Q2 | Q3 | Q4 | Annual |
|--------|-----|-----|-----|-----|--------|
| Inquiries | XX | XX | XX | XX | XXX |
| Tours | XX | XX | XX | XX | XXX |
| Proposals | X | X | X | X | XX |
| Leases Signed | X | X | X | X | XX |

### Recommendations
1. [Recommendation with rationale]
2. [Recommendation with rationale]
3. [Recommendation with rationale]

### Action Items
- [ ] [Action] -- [Owner] -- [Deadline]
```

## Red Flags & Failure Modes

1. **Pricing above market without justification**: If asking rent exceeds market by more than 5-10%, be prepared for extended vacancy. Either justify with superior product or adjust pricing.
2. **Over-investing in TI for short-term leases**: TI allowance should amortize fully within the lease term at a reasonable rate (7-9%). A $50/SF TI on a 3-year lease means the landlord loses money on the buildout.
3. **Spec suites without market data**: Building spec suites is expensive. Only invest in spec when: (a) demand is confirmed by broker feedback, (b) the space layout matches the most common size requirement, and (c) the finish level targets the dominant tenant profile.
4. **Commission overrides that erode economics**: Offering above-market commissions or overrides can attract broker attention but may signal desperation. Use overrides strategically and temporarily, not as permanent market positioning.
5. **Neglecting the broker channel**: In most markets, 60-80% of office deals come through tenant representation brokers. Under-investing in broker relationships is the fastest way to extended vacancy.
6. **Marketing without a story**: Every property needs a narrative beyond specs. Why does this building exist? What tenant thrives here? What experience does it deliver? Generic marketing produces generic results.
7. **Ignoring the competitive set**: If the building across the street has better amenities at lower rent, no amount of marketing overcomes the product gap. Address the product before increasing the marketing budget.
8. **TI not matched to tenant credit**: High TI allowances for non-credit tenants create recovery risk if the tenant defaults early. Require proportional security (larger deposit, guaranty, letter of credit).
9. **Stale listings**: Outdated photos, incorrect SF, or expired pricing on CoStar/LoopNet signals neglect. Audit listings quarterly.
10. **No conversion tracking**: Without tracking inquiry-to-lease conversion, marketing spend cannot be optimized. Implement CRM tracking from day one.

## Chain Notes

- **Upstream**: Receives market data from `comp-snapshot` and `supply-demand-forecast`, lease expiration data from `rent-roll-analyzer`, property condition from `property-performance-dashboard`.
- **Downstream**: Feeds `lease-document-factory` (TI and commission parameters for lease negotiation), `lease-up-war-room` (marketing execution for lease-up properties), `annual-budget-engine` (leasing cost projections for budget).
- **Parallel**: Coordinates with `tenant-retention-engine` (existing tenant renewals vs. new leasing), `lease-negotiation-analyzer` (complex deal structures), `noi-sprint-plan` (leasing as NOI lever).
- **Data sources**: CoStar, CompStak, broker surveys, CBRE/JLL/Cushman market reports, internal CRM data.
- **Frequency**: Marketing plan annually with quarterly updates. TI benchmarking per deal. Commission benchmarking annually or per listing agreement renewal. Broker events quarterly. Marketing materials refreshed as availabilities change.
