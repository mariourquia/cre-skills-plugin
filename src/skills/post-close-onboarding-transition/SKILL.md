---
name: post-close-onboarding-transition
slug: post-close-onboarding-transition
version: 0.1.0
status: deployed
category: reit-cre
description: "Execute post-acquisition asset onboarding (60-day plan), coordinate TI projects, and manage development-to-stabilization transitions. Use when a user has just closed an acquisition and needs to onboard the asset to property management, coordinate tenant improvements, or transition a development project to operations."
user-invocable: true
triggers:
  - "post-close"
  - "post-acquisition"
  - "asset onboarding"
  - "PM transition"
  - "development to operations"
  - "TCO"
  - "utility transfer"
  - "vendor transition"
  - "tenant welcome letter"
  - "lease file audit"
targets:
  - claude_code
---

# Post-Close Onboarding & Transition

Execute post-acquisition integration, property management transitions, TI project coordination, and development-to-operations handoffs. Bridges Acquisitions, PM, Development, and Accounting teams. See [onboarding-checklist.md](references/onboarding-checklist.md) and [transition-frameworks.md](references/transition-frameworks.md) for detailed checklists and frameworks.

## When to Activate

- User has just closed an acquisition and needs a 60-day onboarding plan
- User needs to coordinate a tenant improvement (TI) buildout project
- User is transitioning a development project from construction to operations
- User needs to set up PM company, transfer utilities, or audit lease files post-close

**Do NOT activate for:**
- Pre-close due diligence — use `dd-command-center`
- Closing checklist and document tracking — use `closing-checklist-tracker`
- Ongoing property performance monitoring — use `property-performance-dashboard`

## Input Schema

| Field | Required | Default if Missing |
|-------|----------|--------------------|
| workflow_step (acquisition_onboarding / ti_coordination / dev_to_ops_transition) | Yes | Infer from context |
| property_name | Yes | Ask user |
| property_type | Yes | Ask user |
| total_sf_or_units | Yes | Ask user |
| closing_date | Yes | Ask user |
| location | Yes | Ask user |

**Workflow-specific inputs** (ask only when relevant):
- **Acquisition onboarding**: seller/buyer entities, PM company, occupancy rate, tenant count, annual NOI
- **TI coordination**: tenant name, suite, TI allowance, construction budget/timeline, lease commencement date
- **Dev-to-ops**: TCO date, lease-up target months, stabilized occupancy target, punch list status

If fewer than 3 required fields are present, ask clarifying questions.

## Process

### Step 1: Post-Acquisition Onboarding (60-Day Plan)

Follow the detailed checklist in [onboarding-checklist.md](references/onboarding-checklist.md). Key phases:

**Day 1-7 — Critical Path:**
1. **Ownership transfer** — file deed, notify tenants (welcome letter with new payment instructions), transfer utilities, bind buyer insurance (coordinate with [insurance-risk-manager](../insurance-risk-manager/SKILL.md)), set up lockbox and bank accounts.
2. **PM activation** — execute PM agreement, transfer emergency contacts, issue access credentials, conduct Day 1 walkthrough with photo documentation.
3. **Financial setup** — configure accounting system, load rent roll, process closing prorations, verify security deposit transfer against lease files.

**Day 8-30 — Foundation:**
4. **Lease file audit** — compare abstracts to actual documents, flag missing amendments, create critical dates calendar, send estoppels (see [estoppel-certificate-generator](../estoppel-certificate-generator/SKILL.md)).
5. **Vendor review** — inventory all contracts, assess pricing vs. market and cancellation provisions, notify vendors of ownership change or issue termination.
6. **Deferred maintenance** — commission PCA if not done during DD, prioritize safety and code items, build 30/60/90-day punch list.
7. **IT/access systems** — transfer BAS access, reset access control, set up security and utility monitoring.

**Day 31-60 — Stabilization:**
8. **First month close** — complete operating statement, reconcile prorations, verify rent payments at new lockbox, present actuals vs. underwriting.
9. **Budget** — develop operating budget (see [annual-budget-engine](../annual-budget-engine/SKILL.md)), set up monthly reporting and variance thresholds.
10. **Capital plan** — finalize Year 1 capex, obtain bids, coordinate lender reserve draws.
11. **Tenant relationships** — introductory meetings with top 5 tenants, satisfaction survey.
12. **Market positioning** — review leasing status, update materials, brief brokers on value-add strategy.

### Step 2: TI Project Coordination

1. **Pre-construction** — review TI scope vs. work letter, confirm allowance and disbursement method, bid to 2-3 contractors, verify code compliance.
2. **During construction** — weekly site visits, change order approval per lease limits, verify COI and lien waivers with each draw, track budget (committed/invoiced/paid/remaining), monitor schedule against rent commencement.
3. **Completion** — punch list walkthrough, tenant sign-off on substantial completion, collect as-builts and warranties, process final payment (retain 10% until punch list complete), confirm rent commencement.

### Step 3: Development-to-Operations Transition

See [transition-frameworks.md](references/transition-frameworks.md) for the full framework.

1. **Pre-TCO** (60-90 days before TCO) — engage PM company, develop Year 1 operating budget from pro forma, hire on-site staff, procure vendor contracts, launch leasing campaign (coordinate with [leasing-strategy-marketing-planner](../leasing-strategy-marketing-planner/SKILL.md)).
2. **TCO/CO transition** — obtain TCO, activate permanent insurance (transition from builder's risk), begin move-ins, commission all building systems, establish emergency procedures.
3. **Warranty tracking** — maintain master warranty log, schedule 6-month and 11-month walkthroughs, file claims promptly.
4. **Lease-up to stabilization** — track velocity weekly, monitor concession burn-down (coordinate with [lease-up-war-room](../lease-up-war-room/SKILL.md)), declare stabilization at target occupancy (90-95%), begin permanent financing process.
5. **Budget calibration** — after 3-6 months, compare actuals to pro forma, adjust for actual consumption, file warranty claims for deficiency-related costs.

## Output Format

```markdown
## [Workflow Step] -- [Property Name]

### Summary
[2-3 sentences: transaction context, current status, key priorities]

### Timeline
| Phase | Start | End | Status | Key Milestones |
|-------|-------|-----|--------|----------------|
| Day 1-7 | [Date] | [Date] | [Status] | [Milestones] |
| Day 8-30 | [Date] | [Date] | [Status] | [Milestones] |
| Day 31-60 | [Date] | [Date] | [Status] | [Milestones] |

### Checklist Dashboard
| Category | Total Items | Complete | In Progress | Not Started | Blocked |
|----------|------------|----------|-------------|-------------|---------|
| Ownership Transfer | XX | XX | XX | XX | XX |
| Financial Setup | XX | XX | XX | XX | XX |
| Lease Administration | XX | XX | XX | XX | XX |
| Vendor Management | XX | XX | XX | XX | XX |
| Capital/Maintenance | XX | XX | XX | XX | XX |

### Detailed Checklist
[Full checklist by category with responsible party and deadline]

### Issues and Risks
| Issue | Severity | Owner | Status | Resolution Deadline |
|-------|----------|-------|--------|-------------------|

### Financial Tracking
| Metric | Underwriting | Actual to Date | Variance |
|--------|-------------|---------------|----------|
| Occupancy | XX% | XX% | +/-XX% |
| Gross Revenue | $XXX,XXX | $XXX,XXX | +/-$XX,XXX |
| Operating Expenses | $XXX,XXX | $XXX,XXX | +/-$XX,XXX |
| NOI | $XXX,XXX | $XXX,XXX | +/-$XX,XXX |

### Next Steps
- [ ] [Action] -- [Owner] -- [Deadline]
```

## Red Flags & Failure Modes

1. **Security deposit miscount**: Verify every security deposit received from seller against every lease. Missing deposits are a direct dollar-for-dollar loss. Request escrow holdback at closing if verification is incomplete.
2. **Utility gap**: If utilities are not transferred to buyer by close, service may be interrupted. For master-metered properties, set up new accounts 30 days before close with effective date at closing.
3. **Tenant payment misdirection**: Tenants may continue paying to old lockbox or old entity for months after close. Issue multiple notices, update tenant portals, and monitor old account for misdirected payments for 90 days.
4. **Vendor contract auto-renewal**: Many vendor contracts auto-renew with 30-60 day cancellation notice. If you miss the window, you are locked in for another year at the old (potentially above-market) rate.
5. **Missing lease amendments**: Sellers commonly fail to deliver all lease amendments. The rent roll may reflect terms from amendments you have not seen. Audit every lease against the rent roll and send estoppels.
6. **Insurance gap at closing**: If buyer's insurance is not bound before seller's policy terminates at close, the property is uninsured. Bind coverage 7 days before close.
7. **Deferred maintenance surprises**: DD may miss issues hidden behind walls or in building systems. Budget a contingency reserve (1-3% of acquisition price) for first-year deferred maintenance discoveries.
8. **Development-to-ops staffing gap**: If PM staff is not hired and trained before TCO, the building opens with no one to manage it. Begin PM procurement 90 days before expected TCO.
9. **Warranty claim deadlines**: Most warranties have strict notice requirements. Missing the 11-month walkthrough before the 1-year warranty expires forfeits warranty rights. Set hard calendar reminders.
10. **Rent commencement triggers missed**: Tenant leases often tie rent commencement to substantial completion of TI or delivery of space. If substantial completion is not formally documented, disputes arise over when rent starts.

## Chain Notes

- **Upstream**: Receives transaction data from `closing-checklist-tracker` (closing process), `dd-command-center` (due diligence findings), `construction-procurement-contracts-engine` (development project closeout), `acquisition-underwriting-engine` (underwriting assumptions for budget calibration).
- **Downstream**: Feeds `property-performance-dashboard` (ongoing property monitoring), `annual-budget-engine` (first stabilized budget), `lease-compliance-auditor` (lease administration setup), `rent-roll-analyzer` (verified rent roll).
- **Parallel**: Coordinates with `insurance-risk-manager` (insurance transition), `leasing-strategy-marketing-planner` (leasing launch), `lease-up-war-room` (lease-up execution for developments), `estoppel-certificate-generator` (post-close estoppel campaign).
- **Data sources**: Closing documents, seller document packages, lease files, vendor contracts, utility account records, building system manuals.
- **Frequency**: Acquisition onboarding is ad-hoc (each acquisition). TI coordination is per-project throughout the asset hold. Development-to-ops transition is once per development project.
