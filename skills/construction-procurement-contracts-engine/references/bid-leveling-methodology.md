# Bid Leveling Methodology

## Purpose

Standardize the process of evaluating and comparing general contractor bids for institutional CRE development projects. Ensure apples-to-apples comparison by normalizing scope, pricing, and qualitative factors.

## Bid Evaluation Matrix

### Quantitative Scoring (50 points)

| Category | Weight | Scoring Criteria |
|----------|--------|-----------------|
| Base Bid Price | 20 | Lowest normalized bid = 20, others prorated inversely |
| Scope Completeness | 15 | Full scope = 15, deductions for each exclusion |
| Schedule | 10 | Shortest credible schedule = 10, +1 month = -2 points |
| Alternates Pricing | 5 | Competitive alternate pricing vs market |

### Qualitative Scoring (50 points)

| Category | Weight | Scoring Criteria |
|----------|--------|-----------------|
| Relevant Experience | 15 | 3+ comparable projects in last 5 years = 15 |
| Project Team | 10 | Dedicated superintendent + PM, named individuals, availability confirmed |
| Financial Strength | 10 | Bonding capacity > 2x project, current ratio > 1.5, D&B rating |
| Safety Record | 5 | EMR < 1.0 = 5, 1.0-1.2 = 3, >1.2 = 0 |
| References | 5 | 3 owner references checked, all positive = 5 |
| Local Presence | 5 | Office within 50 miles, local sub relationships, permit experience |

## Scope Leveling Process

### Step 1: Create Master Scope Matrix

Build a line-item matrix from the owner's scope of work document. Typical CSI divisions:

```
Division 01 - General Requirements (general conditions, insurance, bonds, permits)
Division 02 - Existing Conditions (demolition, abatement, geotechnical)
Division 03 - Concrete (foundations, slabs, structural)
Division 04 - Masonry
Division 05 - Metals (structural steel, misc metals, railings)
Division 06 - Wood/Plastics/Composites
Division 07 - Thermal & Moisture Protection (roofing, waterproofing, insulation)
Division 08 - Openings (doors, windows, hardware, glazing)
Division 09 - Finishes (drywall, paint, flooring, tile, countertops)
Division 10 - Specialties (signage, toilet accessories, mailboxes)
Division 11 - Equipment (appliances, trash compactors)
Division 12 - Furnishings (window treatments, amenity furniture if owner-supplied)
Division 13 - Special Construction (pools, green roofs)
Division 14 - Conveying (elevators, escalators)
Division 21 - Fire Suppression
Division 22 - Plumbing
Division 23 - HVAC
Division 26 - Electrical
Division 27 - Communications (low voltage, data, cable)
Division 28 - Electronic Safety (fire alarm, security, access control)
Division 31 - Earthwork (excavation, grading, site utilities)
Division 32 - Exterior Improvements (paving, landscaping, site lighting)
Division 33 - Utilities (water, sewer, storm, gas connections)
```

### Step 2: Map Each Bidder's Scope

For each CSI division and line item:

| Item | Owner Scope | Bidder A | Bidder B | Bidder C |
|------|-------------|----------|----------|----------|
| Demolition | Included | Included | Excluded -- $85K | Included |
| Abatement | Allowance $50K | Allowance $75K | Not addressed | Allowance $50K |
| Structural Steel | Per drawings | Included | Included | Included, excludes misc metals |

### Step 3: Normalize Pricing

For each exclusion or variance:
1. Price the excluded item using the other bidders' line items or independent estimates
2. Add the cost to the excluding bidder's total
3. Adjust allowances to a common baseline (use owner's allowance amount)
4. Document all adjustments in a reconciliation table

**Normalization Table Format:**

| Adjustment | Bidder A | Bidder B | Bidder C |
|------------|----------|----------|----------|
| Base Bid | $42,500,000 | $39,800,000 | $44,200,000 |
| + Demolition scope gap | -- | +$85,000 | -- |
| + Abatement allowance adj | -$25,000 | +$50,000 | -- |
| + Misc metals scope gap | -- | -- | +$180,000 |
| + GC fee adjustment | -- | -- | -- |
| **Leveled Total** | **$42,475,000** | **$39,935,000** | **$44,380,000** |
| **Leveled $/SF** | **$170/SF** | **$160/SF** | **$178/SF** |

### Step 4: Validate Pricing Reasonableness

Check each bidder's major line items against:
- RS Means data for the project location (apply city cost index)
- Recent comparable project costs from owner's portfolio
- Independent cost estimator's budget (if available)

Flag line items more than 15% above or below the mean as requiring investigation.

## GC Interview Framework

Conduct 60-90 minute interviews with top 2-3 bidders. Standard question set:

### Team & Availability (Questions 1-3)

1. **"Walk us through the specific team you've assigned. What is each person's current project and when do they transition to ours?"**
   - Looking for: Named individuals, realistic transition dates, no double-booking.
   - Red flag: "We'll assign the team closer to start" or unnamed superintendent.

2. **"Your superintendent -- how many projects has he/she completed of this type and scale? Can we visit a current jobsite?"**
   - Looking for: 3+ comparable projects, willingness to show current work.
   - Red flag: Superintendent has never done this building type.

3. **"What is your current backlog and bonding capacity? What percentage of capacity does this project represent?"**
   - Looking for: Project < 30% of bonding capacity, healthy backlog but not overextended.
   - Red flag: Project > 50% of capacity, or GC has no other work.

### Scope & Approach (Questions 4-6)

4. **"Walk us through your qualifications and exclusions. Why did you exclude [specific item]?"**
   - Looking for: Thoughtful exclusions based on risk assessment, not scope-cutting to lower price.
   - Red flag: Cannot explain exclusions, or exclusions are core scope items.

5. **"Describe your approach to [most complex building system, e.g., curtain wall, post-tension concrete, MEP coordination]."**
   - Looking for: Specific methodology, named subcontractors, relevant experience.
   - Red flag: Vague answers, no pre-selected subs for critical systems.

6. **"How did you develop your schedule? What are the critical path items and what float exists?"**
   - Looking for: CPM schedule logic, realistic durations, identified long-lead items.
   - Red flag: Schedule seems compressed without explanation, no long-lead procurement plan.

### Risk & Problem Solving (Questions 7-8)

7. **"Describe a project where you encountered significant unforeseen conditions. How did you handle cost and schedule impact?"**
   - Looking for: Collaborative problem-solving, transparent communication, creative solutions.
   - Red flag: Blaming owner/architect, litigious tone, claims-oriented mindset.

8. **"How do you manage subcontractor default? Have you had to replace a sub mid-project?"**
   - Looking for: Bench strength, bonding of critical subs, proactive monitoring.
   - Red flag: Never happened (unlikely if experienced) or no contingency plan.

### Commercial (Questions 9-10)

9. **"Your general conditions are $X. Break that down for us -- staffing plan, equipment, temporary facilities, duration assumptions."**
   - Looking for: Transparent breakdown, reasonable staffing levels, realistic duration.
   - Red flag: Lump sum general conditions with no breakdown, or GC refuses to detail.

10. **"If we proceed with a GMP, what is your approach to buyout savings and shared savings?"**
    - Looking for: Willingness to share buyout savings (50/50 to 75/25 owner standard), open-book process.
    - Red flag: Wants to keep all buyout savings, or resists open-book accounting.

## Selection Recommendation Format

```markdown
## GC Selection Recommendation

### Project: [Name] -- [Units/SF] [Type] -- [Location]
### Date: [Date]
### Prepared by: [Name, Title]

### Executive Summary
[2-3 sentences: recommended GC, leveled bid amount, key differentiators]

### Bid Summary
| Metric | [GC A] | [GC B] | [GC C] |
|--------|--------|--------|--------|
| Base Bid | $X | $X | $X |
| Leveled Total | $X | $X | $X |
| Leveled $/SF | $X | $X | $X |
| Leveled $/Unit | $X | $X | $X |
| Quantitative Score | XX/50 | XX/50 | XX/50 |
| Qualitative Score | XX/50 | XX/50 | XX/50 |
| **Total Score** | **XX/100** | **XX/100** | **XX/100** |

### Scope Leveling Adjustments
[Table of all normalization adjustments]

### Interview Assessment
[Key takeaways from each GC interview]

### Risk Assessment
[Identified risks by GC and mitigation strategies]

### Recommendation
**Recommended GC: [Name]**
- Leveled price: $XX,XXX,XXX ($XXX/SF)
- Key strengths: [3 bullets]
- Key risks: [2 bullets with mitigations]
- Proposed contract structure: [GMP/Lump Sum] with [key terms]

### Next Steps
1. [Negotiate final contract terms]
2. [Execute AIA contract]
3. [Obtain payment and performance bonds]
4. [Verify insurance certificates]
5. [Schedule preconstruction kickoff]
```

## Worked Example: 250-Unit Multifamily -- 3-GC Bid Comparison

### Project Parameters
- 250 units, 5-story wood-frame over concrete podium
- 225,000 SF residential + 8,000 SF amenity + 15,000 SF structured parking
- Location: suburban Southeast
- Budget: $45M hard costs ($180/SF blended)

### Bids Received

| | Apex Construction | Meridian Builders | Summit Development |
|---|---|---|---|
| Base Bid | $43,800,000 | $41,200,000 | $46,500,000 |
| GC Fee | 4.0% | 3.5% | 4.5% |
| General Conditions | $2,400,000 | $1,900,000 | $2,800,000 |
| Schedule | 22 months | 20 months | 24 months |
| EMR | 0.82 | 0.95 | 0.78 |

### Scope Leveling Results

Meridian excluded: site utilities ($320K), landscape allowance was $50K below spec ($50K), fire alarm was allowance not lump sum (risk: +$75K). Adjusted Meridian: $41,645,000.

Summit included additional scope: enhanced amenity finishes (+$400K above spec), premium elevator spec (+$180K above spec). Adjusted Summit: $45,920,000.

Apex was substantially complete in scope. Minor adjustment for abatement allowance: +$25K. Adjusted Apex: $43,825,000.

### Leveled Comparison

| Metric | Apex | Meridian | Summit |
|--------|------|----------|--------|
| Leveled Total | $43,825,000 | $41,645,000 | $45,920,000 |
| Leveled $/SF | $177/SF | $168/SF | $185/SF |
| Leveled $/Unit | $175,300 | $166,580 | $183,680 |
| Quantitative | 38/50 | 44/50 | 32/50 |
| Qualitative | 42/50 | 35/50 | 44/50 |
| **Total** | **80/100** | **79/100** | **76/100** |

### Recommendation

**Apex Construction** recommended despite not being lowest leveled bidder. Rationale:
1. Strongest project team -- superintendent completed 3 comparable projects in market
2. 22-month schedule is realistic vs Meridian's aggressive 20-month target (saves carrying cost risk)
3. Meridian's low general conditions raise concerns about staffing adequacy
4. Apex's open-book approach to GMP with 60/40 shared savings favorable

Negotiate GMP target of $43.5M with Apex, including 3% owner contingency ($1.3M) and 2.5% GC contingency ($1.1M).
