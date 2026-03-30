# AppFolio Property Manager -- Skill Reference

> Last updated: 2026-03-26. Sources: AppFolio.com product pages, official API documentation (GitHub gist, Bold BI connector docs, Stack API explorer), Capterra/G2/SoftwareConnect user reviews, third-party integration documentation (Celigo, EliseAI, Skywalk), CAMAudit competitive analysis, AppFolio Q3 2025 earnings call, AppFolio newsroom announcements.

---

## Platform Overview

### Market Position

AppFolio, Inc. (NASDAQ: APPF) is the dominant mid-market property management platform in the U.S., headquartered in Santa Barbara, CA. As of 2025-2026 data, AppFolio holds approximately 12% market share in the property management software category, ahead of RealPage (~5%) in unit count served, though RealPage and Yardi retain enterprise dominance by revenue and complex commercial use cases.

AppFolio's differentiated positioning: automation-first, AI-native, unified platform with the lowest operational complexity per unit managed of any enterprise-grade solution. The platform manages over 5 million units. Primary competitor set: Yardi Breeze Premier (mid-market overlap), Buildium (sub-500 units), Entrata (multifamily enterprise), RealPage (large multifamily), MRI Software (commercial and mixed-use enterprise).

**When AppFolio wins**: Growing residential and multifamily portfolios (50-10,000 units) that prioritize automation, mobile-first workflows, and per-unit economics over deep customization. Strong for student housing, affordable housing (HUD-subsidized), HOAs, and mixed residential/commercial portfolios under ~3,000 units.

**When AppFolio loses**: Complex commercial NNN portfolios (Yardi or MRI better), 10,000+ unit institutional operators needing deep custom reporting, operators requiring native QuickBooks integration without middleware, portfolios with sophisticated equity waterfall needs beyond AppFolio Investment Manager's capabilities.

### Product Tiers

| Tier | Target | Per Unit/Month (Residential) | Min Units | Key Differentiators |
|------|--------|------------------------------|-----------|---------------------|
| Core | 50-500 units, lean teams | ~$1.40-$1.49 | 50 | Full PM operations, basic API (read-only), standard reporting |
| Plus | 500-5,000 units, growth operators | ~$3.00-$3.20 | Varies | Affordable housing, advanced budgeting, AppFolio Stack Premium, purchase orders, API read access |
| Max | 5,000+ units, enterprise | ~$5.00 | Minimums apply | Full read/write Database API, Leasing CRM, Leasing Signals, dedicated CSM |

Community Associations: $0.80-$0.85/unit/month. Commercial: $1.50/unit/month. Pricing is not publicly listed for Max; direct quote required. Charges apply to occupied units only, which reduces cost during high-turnover periods. One-time setup fee required.

**AppFolio Investment Manager** (separate product): Core plan from $650/month. Includes investor CRM, fundraising workflows, investment financials, and asset tracking. Premier tier adds SQL export, full API access, Zapier integration.

### Property Types Supported

- Residential (single-family, multifamily)
- Student housing
- Affordable housing (HUD Project-Based Section 8, LIHTC with compliance workflows)
- Community associations / HOA
- Commercial (office, retail, industrial -- with known limitations for complex NNN)
- Mixed-use portfolios
- Manufactured housing

---

## Core Modules

### Accounting

AppFolio accounting is a full double-entry general ledger system built for property management trust accounting, not a general-purpose accounting platform. All financial activity flows through a single database; no external sync required between PM and accounting modules.

**General Ledger**
- Full double-entry GL with customizable chart of accounts
- Accounts organized by standard categories: assets, liabilities, equity, revenue, expenses
- GL accounts linked to properties and unit types for property-level P&L
- Supports both Cash and Accrual accounting basis (selectable per report run)
- GL groups for expense pooling (required for CAM reconciliation workflows -- accounts must be explicitly added to GL groups or they will not appear in CAM reconciliation output)
- Auditing Center tracks all staff changes, edits, and activities with user/property/date filter; supports fraud investigation workflows
- Reversed transaction visibility in GL reports

**Accounts Payable**
- Vendor bill entry with approval workflows (Bill Approval Flows, released Spring 2025)
- Bill approval routes automatically based on vendor type, GL account, and dollar amount thresholds
- Bulk bill uploads supporting resident, owner, and vendor payables in a single file (Plus/Max: identify payees by ID or name)
- Purchase Orders and Inventory Tracking module (Plus/Max tier)
- PO approval workflows with routing and auto-approval options (Summer 2025)
- Integration with AvidXchange for AP automation and zero-transaction-fee supplier payments
- Smart Bill Entry (AI-assisted data extraction from invoices)

**Accounts Receivable / Rent Collection**
- Tenant ledger tracking charges, payments, credits, and balances
- Online rent collection via Resident Portal (eCheck/ACH, credit card, debit card, electronic cash)
- eCheck fee: $2.49/transaction to resident or $1.00/transaction absorbed by PM (as of Aug 2023)
- Credit/debit card fee: ~3.5% + $0.25
- Electronic cash payment: $3.99 per transaction up to $2,000
- Autopay setup: fixed amount or outstanding balance, resident-configurable
- Late fee automation: configurable rules trigger automatically based on lease terms
- Payment plan tracking for deferred charges
- Three-day ACH settlement window (reported as a friction point by some users)
- Delinquency report with current and as-of-date views; filterable, groupable, column-configurable

**Bank Reconciliation**
- Automated bank reconciliation with secure bank feed integration
- Three-way reconciliation (bank statement / GL / trust account)
- GL Auditing Center usable as troubleshooting tool to identify out-of-balance conditions; filter by cash account and sort by last-edited timestamp to isolate recent changes

**Budgeting and Forecasting**
- Property-level and portfolio-level budget creation
- Budget vs. Actual variance reporting
- Multi-year income statement views (e.g., trailing 5-year)
- Advanced Budgeting module available in Plus/Max tiers

**CAM Reconciliation**
- Pro-rata allocation by square footage supported
- GL groups used to pool CAM-eligible expenses
- Commercial CAM reconciliation available but has documented limitations:
  - BOMA gross-up methodology not fully supported
  - Fixed/variable expense bifurcation for occupancy adjustment (NNN cap at 1.0) is not available
  - Setup complexity: GL accounts must be manually added to GL groups or they are silently excluded from reconciliation
  - Designed primarily for residential/HOA CAM (common area charges), not complex NNN structures
  - Third-party tool CAMAudit explicitly calls out AppFolio as insufficient for institutional commercial NNN

**Tax and Compliance**
- 1099 generation (Form 1099-MISC and 1099-NEC for vendors)
- Tax Withholding Management (released Spring 2025): set up, track, and automate withholdings for investors -- federal, state, and international; custom withholding types

**Trust Accounting**
- Built-in trust account separation (tenant security deposits, owner funds)
- Separate trust account GL structure enforced by the platform
- Owner draw/distribution workflows with automatic reconciliation

**Known Accounting Limitations**
- No native QuickBooks integration; third-party middleware (Skywalk API, AvidXchange, or CSV export) required
- Bill payment bank account defaulting issues reported: with multiple bank accounts, bills may not default to the correct account, causing balance sheet anomalies in the Cash section
- Accounting module UI cited as "difficult to navigate" and "requiring more steps than necessary" in user reviews
- Additional fees module lacks start/end date functionality in Core/Plus tiers (Max only)
- Hard to reverse errors without contacting AppFolio support; the system is "unforgiving" for data entry mistakes

---

### Leasing

**Lead-to-Lease Workflow**
1. Vacancy posted to company website and ILS syndication partners
2. Prospect submits inquiry via digital channel (email, text, website form)
3. Guest card automatically created and leasing team alerted
4. Self-scheduled, self-guided, or virtual showing coordinated
5. Online application submitted (mobile-optimized, branded)
6. Automated screening report generated (FolioScreen)
7. Manager reviews and approves applicant
8. Approved resident signs lease via e-signature
9. Online rent and deposit payment collected

**Online Applications and Screening**
- FolioScreen Trusted Renter: criminal/background check, income verification, ID verification, employment verification, fraud detection
- Standardized screening criteria for Fair Housing compliance
- Application data auto-populates lease without re-entry
- Zillow partnership (April 2025): Zillow rental application data pre-populates AppFolio application for shared prospects

**Lease Generation and E-Signatures**
- Customizable lease templates
- E-signature via integrated tool (no third-party DocuSign required for standard leases)
- Online lease execution with full audit trail

**Lease Renewal Workflows**
- Bulk renewal preparation: send renewal offers to large tenant cohorts simultaneously
- Predefined offer menus (tenants select from options)
- Default offer with automatic lease date, rent amount, and status update on expiration
- Realm-X Flows renewal automation: autotriggers on lease expiration proximity, with configurable lead times
- 8% reported overnight increase in renewal rates by one AppFolio customer using Realm-X Flows renewal template

**Leasing CRM** (Max tier, also available as add-on)
- Single guest card per prospect tracked across portfolio
- Automated lead assignment to team members (Spring 2025)
- Advanced lead attribution tracking to source channel
- To-do list prioritization for leasing agents
- Portfolio-wide tour booking and closing rate metrics

**Leasing Signals** (Max tier)
- Market rate intelligence for confident pricing decisions
- Compares managed units against comparable properties
- Does not share proprietary data externally

---

### Maintenance

**Work Order Management**
- Resident-submitted online requests with photo uploads from Resident Portal or mobile app
- Work order lifecycle: submission → triage → assignment → in-progress → completion → billing
- Drag-and-drop calendar scheduler for in-house technician assignment
- Vendor portal for third-party technicians: work order access, photo uploads, status updates
- Automated billing: custom owner invoices generated using preset rules
- Financial integration: work order charges passable to resident or property owner in minimal clicks
- Mobile app mirrors full desktop functionality: create work orders, assign vendors, approve estimates, process payments

**Smart Maintenance / Realm-X Maintenance Performer**
- AI-powered intake: responds to residents 24/7 via text, email, or voice in multiple languages
- Photo analysis: identifies maintenance issues from resident-submitted images
- Triage and prioritization: distinguishes emergencies from routine requests
- Automated vendor dispatch: routes to in-house technician or Lula Vendor Network (vetted contractors in 40+ metro areas) based on availability and PM configuration
- Real-time field updates and coordination

**Unit Turn Board**
- Automatically created on resident notice-to-vacate
- Consolidates all turn tasks in one view: work orders, inspections, cleaning, repairs
- Tracks vacancy duration and turn time metrics
- Summer 2025 enhancement: PO approval workflows and enhanced automation integrated into unit turns

**Mobile Inspections**
- On-site inspections managed entirely in mobile app
- Photo documentation with gallery view and editing
- Before/after photo capture for move-in/move-out conditions
- Inspection reports accessible via Resident Portal

**Vendor Management**
- Vendor records with contact info, service categories, insurance compliance tracking
- NetVendor integration for vendor credentialing and COI management
- Lula Vendor Network for on-demand vetted contractors (fully automated dispatch when combined with Smart Maintenance)

**Move-In / Move-Out Automation**
- Automatic lead-paint disclosure reminders for pre-1978 properties
- Recurring work order templates for standard make-ready tasks (carpet, paint)
- Before/after inspection integration with security deposit disposition
- Automatic unit turn creation on notice submission

---

### Rent Collection

See Accounting > Accounts Receivable section for fee structure. Key operational details:

- Resident Portal and mobile app (iOS/Android) for all payment methods
- Autopay enrollment by resident with PM-configured parameters
- Automated late fee assessment based on lease rules
- Payment plan tracking for residents on deferred payment arrangements
- Electronic cash payment option (3rd-party cash networks) for unbanked residents
- Automated rent reminder notifications (email or push notification, resident-configurable)

---

### Tenant / Resident Portal

**Access**: Web (any browser) and dedicated mobile app (AppFolio Online Portal, iOS and Android)

**Available Functions**
- Online rent payment (one-time and autopay)
- Maintenance request submission with photo upload and status tracking
- Lease document viewing and download
- Communication with property management team
- FolioGuard renters insurance purchase and policy management
- Inspection report access
- Push notification preferences for payment reminders

**FolioSpace** (Next-generation resident experience app, previewed at FUTURE 2024)
- Enhanced resident lifecycle experience beyond standard portal
- Positioning: deeper resident engagement and retention tooling
- Status as of 2026-03-26: released/preview, details limited in public documentation

---

### Owner Portal

**Owner-Facing Dashboard**
- Income and expense summary by property
- Contribution and disbursement totals
- Occupancy rate and rent collection statistics
- Income/expense breakdown widgets
- Customizable dashboard: add/remove elements, drag-and-drop layout, resizable widgets, saved preferences

**Financial Statements Available to Owners**
- Owner statements with beginning and ending balances
- P&L / income statement
- Published reports (PM controls what is visible)
- Document downloads

**Communication**
- PM-to-owner email and SMS via the same multi-channel inbox
- Maintenance update notifications
- Proactive alerts on urgent maintenance items requiring owner approval

**Owner Portal Access**
- 24/7 self-service web and mobile access
- Board member check/invoice approvals for HOA communities
- Architectural review workflow participation

---

### Investor Portal (AppFolio Investment Manager)

Separate product from core Property Manager. Core plan $650/month.

**Investor-Facing Features**
- Personal dashboard: investment positions, asset information, invested/distributed capital totals
- Transactions tab: distributions and contributions with filter
- Documents and Tax Forms tabs: K-1s, operating agreements, quarterly/annual reports
- Document upload to investment manager with automatic email notification
- Capital call response: "Send Funds" payment instructions, transfer confirmation
- 24/7 access via web and iOS/Android apps

**Investment Manager Platform Features**
- Fund structure modeling: investments holding positions in other investments (replicates legal entity hierarchy)
- Integrated GL: automates contributions, distributions, and accounting reconciliation
- Waterfall calculation tool: handles complex fund structures (described as "best-in-class" by AppFolio)
- Distribution payment processing
- Investor CRM: lead capture, offering interest collection, capital raise history, task management, email communication
- AppFolio Alpha (AI tool for asset management KPIs)
- Custom KPIs and asset performance dashboards

**Technical Limits (Investor Portal)**
- U.S. bank accounts only for electronic contributions; no FBO/FFC accounts
- ACH single transaction limit: $250,000
- ACH daily limit per entity: $500,000
- ACH daily transaction count per entity: 10

---

### Marketing

**ILS Syndication**
- Native free syndication to: Zillow, Apartments.com, Zumper, Blue Moon, Engrain
- Syndication to dozens of additional pay-to-list sites (premium placement options)
- Zillow Listing Spotlight (partnership launched Oct 2025): premium advertising for single-family or sub-25-unit buildings; flexible exposure boost on Zillow Rentals
- Apartments.com connection via standard ILS integration

**Website Builder (AppFolio Sites)**
- Modern, mobile-responsive website with native AppFolio integration
- 3D virtual tours for unit self-qualification
- Interactive property maps (amenities, parking)
- Guest card auto-capture from website inquiries

**Lead Tracking**
- Guest card created on first prospect contact
- Advanced lead attribution tracks source channel through to lease (Spring 2025)
- Leasing CRM tracks cross-portfolio activity per prospect

---

### Communications

**Multi-Channel Inbox (Realm-X Messages)**
- Unified inbox for all inbound text and email communications from residents, owners, vendors
- Filter and sort by message type, property, sender
- Suggested responses with personalized details pre-populated by AI
- Context-aware suggested actions (e.g., suggest creating work order from maintenance-related message)

**Bulk Communications**
- Bulk email to residents: available but mass email to owners requires copy-paste workaround (documented limitation)
- Bulk text to multiple tenants: not available natively in a single operation (documented limitation)
- Text and email templates for standardized communications

**Automated Notifications**
- Rent due reminders (resident-configurable)
- Late payment notices
- Maintenance request status updates
- Capital call notifications (investor portal)
- FolioGuard insurance policy event notifications (cancellations, renewals, late payments)

**Realm-X Leasing Performer**
- 24/7 email, text, and voice response to prospects
- Creates detailed guest cards automatically
- Offers self-scheduling with calendar integration and drive-time calculations
- 73% higher lead-to-showing conversion rate reported in AppFolio data

**Realm-X Resident Messenger Performer**
- Handles resident inquiries about rent, payments, lease terms, renewals
- Pulls live data from AppFolio to provide fact-based responses
- Operates across all resident communication channels at scale

---

### Inspections

- Mobile inspection workflows (iOS/Android)
- Inspection templates for move-in, move-out, periodic
- Photo documentation with gallery view, editing, and before/after comparison
- Inspection reports published to Resident Portal
- Integration with Unit Turn Board workflow
- Third-party inspection tools available via Stack Marketplace: HappyCo, RentCheck, SnapInspect, zInspector

---

### Insurance

**FolioGuard Renters Insurance**
- Tenant-purchased via Resident Portal (same login used for rent payment)
- Best-in-class liability coverage up to $100,000
- PM automatically added as additional interested party on policy
- Automatic compliance tracking: policy status, cancellations, renewals tracked in AppFolio PM database
- PM notified of policy events (cancellation, renewal, late payment)
- Scales to institutional portfolio without manual tracking overhead

---

### Utility Management / RUBS Billing

**RUBS (Ratio Utility Billing System)**
- Allocates single utility bill across multi-unit property without submetering
- Allocation formula factors: number of occupants, unit square footage, owner/tenant split
- Partial allocation to owner for unoccupied units and common areas
- Proration on move-in/move-out: move-out tenant not charged; move-in tenant charged prorated amount based on occupancy days
- Utility stack integrations: Anchor Utility, Conservice, Livable, Utility Management Solutions, Zego Utility

**Affordable Housing Utility Allowances**
- Unit set-asides, income limits, rent limits, and utility allowance tracking in Plus/Max tier

---

## API and Integration Layer

### API Architecture Overview

AppFolio exposes two distinct API surfaces:

| API | Availability | Auth | Direction | Primary Use |
|-----|-------------|------|-----------|-------------|
| Reporting API v2 | Core (read-only), Plus (read-only), Max (read/write) | HTTP Basic Auth (Client ID + Client Secret) | Read (all tiers); Write (Max) | Financial reports, data extraction, BI integration |
| Stack / Database API | Max tier (full read/write); Plus (limited read) | HTTP Basic Auth | Read + Write | CRUD operations on all entity types, custom integrations |

No GraphQL. No official OAuth 2.0 (despite some third-party articles claiming otherwise -- HTTP Basic Auth is the documented authentication method for both APIs).

Credentials retrieved from: Account dropdown → General Settings → Manage API Settings → Reports API Credentials tab.

### Reporting API v2

**Base URL pattern**: `POST https://{ClientID}:{ClientSecret}@{database}.appfolio.com/api/v2/reports/{report_name}.json`

**Rate Limits**
- Standard endpoints: 7 requests per 15 seconds
- Pagination URLs: no rate limiting
- Result sets valid for 30 minutes

**Pagination**: Response includes `next_page_url` when result set exceeds 5,000 rows. Set `paginate_results=false` to retrieve all rows in one response (risk: timeout on large sets).

**Data Types**
- Amount: string with two decimal places (e.g., `"100.00"`)
- Date: ISO 8601 `YYYY-MM-DD`
- DateTime: ISO 8601 UTC `YYYY-MM-DDTHH:MM:SSZ`
- Number: integer

**Common Filter Parameters (available on most report endpoints)**

| Parameter | Values | Notes |
|-----------|--------|-------|
| `property_visibility` | `"active"`, `"hidden"`, `"all"` | Filters by property active status |
| `properties` | property IDs, groups, portfolios, owner IDs | Multi-value filter |
| `accounting_basis` | `"Cash"`, `"Accrual"` | Selects GL accounting method |
| `posted_on_from` / `posted_on_to` | ISO 8601 dates | Transaction post date range |
| `occurred_on_from` / `occurred_on_to` | ISO 8601 dates | Transaction event date range |
| `paginate_results` | `true` / `false` | Controls pagination behavior |
| `from_date` / `to_date` | ISO 8601 dates | General date range filter |

**Available Report Endpoints (confirmed from documentation)**

Financial statements:
- `account_totals.json`
- `balance_sheet.json` (requires properties filter)
- `cash_flow.json`
- `income_statement.json`
- `general_ledger.json`
- `chart_of_accounts.json`

AP/AR detail:
- `aged_payables_summary.json`
- `bill_detail.json`
- `charge_detail.json`
- `check_register.json`
- `deposit_register.json`
- `expense_register.json`
- `income_register.json`
- `additional_fees.json`
- `journal_entries.json`
- `recurring_charges.json`

Operational:
- `purchase_order.json`
- Workflow reports (specific names not fully enumerated in public docs)

**Error Codes**

| Code | Meaning |
|------|---------|
| 400 | Bad Request -- invalid syntax or missing required filter |
| 401 | Unauthorized -- invalid credentials |
| 404 | Report not found or unavailable |
| 406 | Not Acceptable -- missing `Content-Type: application/json` header |
| 429 | Rate limit exceeded |
| 500 | Server error |

### Stack / Database API (Max Tier)

40+ CRUD endpoints covering the full data model. Supports `GET`, `POST`, `PUT` (and some `DELETE`) operations.

**Entity coverage confirmed:**

| Domain | Endpoints |
|--------|-----------|
| Properties | Properties, property groups |
| Units | Units, unit groups |
| Leasing | Tenants, occupancies, leases, leads, listings, rental applications, showings |
| Financial | Bills, charges, recurring charges, GL accounts, journal entries, bank balances |
| Vendors | Vendors, work orders |
| Owners | Owners |
| AR/Collections | Tenant ledgers, delinquent charges, collections placements |
| Community Associations | Board members, homeowners, renters, rules, violations |
| Administrative | Users, attachments, bank accounts |

**Temporal filtering**: Most endpoints support `LastUpdatedAt` and `LastUpdatedAtFrom` for incremental data pulls (change data capture pattern).

**Webhook support**: AppFolio signs outgoing webhooks using RSASSA_PSS_SHA_256. GitHub repo `appfolio/stack-webhook-jws-examples` documents JWS verification. Known webhook topic: `leads` (confirmed by EliseAI integration docs). Other webhook topics not publicly enumerated; contact `database.api.support@appfolio.com` for full list.

**API Support contact**: `database.api.support@appfolio.com`

### Data Export / Import

- All reports exportable to CSV or Excel from UI
- Bulk bill upload via CSV (Plus/Max: payee identified by ID or name)
- No documented bulk import for tenants, leases, or properties via API (CSV migration via AppFolio onboarding team)
- CSV export not as streamlined as some competitors (Buildium cited as more structured for bulk import); common workaround involves scheduled report emails parsed as CSV attachments

### Third-Party Integrations (AppFolio Stack Marketplace)

**Accounting / Financial**
- AvidXchange (AP automation, zero PM transaction fees on supplier payments, real-time payment status)
- SmartProperty, APM Help, Balanced Asset Solutions, OJO Bookkeeping, Optimal, Planet Synergy, ProfitCoach, Proper AI, REA.co, Red Cedar (accounting services)

**Construction Management**
- Procore (project financials sync -- added 2025)
- Northspyre
- Banner

**Maintenance**
- AppWork, Breezeway, HappyCo, Jack Jaffa, Lowe's, Lowe's Pro Supply, Lula (vendor network), NetVendor (vendor credentialing), Property Meld, RentCheck, SnapInspect, Sortly (inventory), The Home Depot Pro, zInspector

**Marketing and Leasing**
- 30 Lines, Apartments247, Birdeye, Engrain, Knock, LeadSimple, Opiniion, PetScreening, PlanOmatic, Pynwheel, REBA Rent, Rently, RentVision, Respage, SafeRent Solutions, Showdigs, ShowMojo, Tenant Turner, Tour24, Zillow Listing Spotlight

**Resident Experience**
- Amazon Hub Apartment Locker, Amazon Key, ButterflyMX (access control), Homebase, Livable, Livly, PointCentral, RemoteLock, Rent Dynamics, SmartRent

**Utility Management**
- Anchor Utility, Conservice, Livable, Utility Management Solutions, Zego Utility

**Delinquency / Collections**
- Aldous & Associates, Axela Technologies, Genesis, Hunter Warfield, Pay Ready, Possession Partner (evictions -- added Spring 2025)

**Document Management**
- CondoCerts, HomeWiseDocs

**Communications**
- Page Per Page, SimpleVoIP

**Notable absences**: No native QuickBooks integration (frequently cited user complaint). No Salesforce native connector. No MRI or Yardi data bridge.

---

## Reporting and Analytics

### Standard Report Library

**Financial Statements**
- Balance Sheet (cash and accrual)
- Income Statement / P&L (cash and accrual, by property or portfolio)
- Cash Flow Statement
- General Ledger (filterable by property, GL account, date range, user who created/edited)
- Trial Balance
- Budget vs. Actual

**AR / Rent Roll**
- Rent Roll: Unit, Tenant, Status, Rent, Deposit, Lease Start, Lease End
- Delinquency Report (current) and Delinquency as-of-date
- Aged Payables Summary
- Charge Detail

**AP / Disbursements**
- Check Register
- Deposit Register
- Expense Register
- Bill Detail
- Purchase Order Report

**Operational**
- Vacancy Report
- Unit Turn tracking and metrics
- Days-to-Lease
- Occupancy Report
- Inspection Reports

**Owner and Investor Reports**
- Owner Statement (beginning/ending balance, categorized transactions)
- Owner Performance Report
- Investor Portal statements (published by PM, labeled "Reporting & Statements")
- K-1 and tax form distribution via Investor Portal

**Affordable Housing Compliance**
- TRACS submission history and error messages (visible in-app for HUD properties)
- HAP Request tracking and reconciliation

### Custom Reporting (Report Builder)

- Base report selected from library
- Additional columns added from other reports as long as the data exists in the system
- Configurable filters, groupings, and column selections
- Custom metrics available: average days-to-lease, average arrears, vacancy duration, repair/maintenance cost per unit
- Reports saved for recurring use or exported as CSV/Excel
- Scheduled Reports: automated report delivery via email on configurable cadence
- Multi-year statements (trailing 5-year income statement example)
- Report Builder limited by AppFolio's internal data model -- cannot join arbitrary external data sources

### Dashboards and KPIs

- Owner Portal: customizable widget dashboard (occupancy, rent collection, income/expense, disbursements)
- Investor Portal: investment position summary, total invested/distributed, asset-level KPIs
- AppFolio Alpha (Investment Manager): custom KPIs, asset performance dashboards, AI-assisted insights
- Realm-X Assistant: conversational data pull ("show me delinquency for property X") for operational queries
- Leasing Signals (Max): market rate benchmarking dashboard

### Analytics Positioning vs. Competitors

AppFolio is not a BI platform. It does not compete with Yardi's Advanced Reporting or RealPage's predictive analytics. The Report Builder is strong for operational reports but lacks:
- Data warehouse export (no native Snowflake/BigQuery push)
- SQL access to underlying database (Investment Manager Premier has SQL export)
- Custom calculated fields beyond the built-in column library
- Cohort analysis or time-series trend visualization

For institutional analytics, teams extract data via Reporting API v2 and push to external BI tools (Power BI, Tableau, Looker).

---

## Workflow Automation

### Realm-X Platform

AppFolio's AI and automation suite launched under the Realm-X brand. Four components:

**1. Realm-X Assistant**
- Conversational interface for operational queries and bulk actions
- Executes tasks via natural language: pull reports, send bulk messages, update records
- Surfaces performance insights on demand

**2. Realm-X Messages**
- Centralized inbox for all resident/owner/vendor communications
- AI-generated suggested responses with context-aware actions
- Immediate notification on reply

**3. Realm-X Flows**
- Rule-based workflow automation engine running 24/7
- Autotriggers on events (lease expiration proximity, move-out notice, delinquency threshold)
- Pre-built templates: lease renewal, unit turn, delinquency follow-up
- Activity Logs (Spring 2025): tracks template changes (who changed what and when) for compliance and troubleshooting
- Example result: 8% overnight renewal rate increase using Flows renewal template

**4. Realm-X Performers (Agentic AI -- launched Apartmentalize 2025)**
- Fully autonomous AI agents operating within AppFolio's data and workflow layer
- Update records and populate reports in real time
- Designed to execute without human intervention after configuration

**Leasing Performer**
- Responds to prospect inquiries 24/7 via email, text, and voice
- Creates guest cards automatically
- Schedules showings with calendar integration and drive-time calculation
- Manages full lead-to-lease lifecycle hand-off to human team
- Result: 73% higher lead-to-showing conversion reported

**Maintenance Performer**
- Intakes and triages maintenance requests
- Analyzes photos submitted by residents
- Asks follow-up questions for diagnosis
- Creates prioritized work orders
- Dispatches to in-house technician or Lula Vendor Network
- Provides multilingual 24/7 support
- Coordinates field updates

**Resident Messenger Performer**
- Handles resident FAQs: rent balance, payment history, lease terms, renewal options
- Pulls live AppFolio data to provide accurate fact-based responses
- Operates across all resident communication channels

### Built-In Automation Rules (Non-AI)

| Workflow | Mechanism |
|----------|-----------|
| Late fee assessment | Configurable rule on lease; triggers on day X after due date |
| Rent reminder | Automated email/SMS before due date; resident-configurable |
| Unit turn creation | Auto-triggered on notice-to-vacate submission |
| Lease renewal offer | Scheduled X days before expiration; bulk or individual |
| Tax withholding | Auto-calculated per investor based on withholding type config |
| Work order billing | Auto-generate owner invoice per preset billing rules |
| Lead assignment | Auto-assign new leads to team members (Spring 2025) |
| Bill approval routing | Auto-route bills by vendor type, GL account, amount (Spring 2025) |
| Scheduled reports | Email delivery on configured cadence |

---

## Data Model

### Core Entity Hierarchy

```
Organization (AppFolio Account / Database Instance)
├── Property
│   ├── PropertyId (unique)
│   ├── PropertyType (residential, commercial, HOA, student, affordable)
│   ├── Address
│   ├── PropertyGroup (for portfolio-level grouping)
│   ├── PortfolioId (for owner-based grouping)
│   ├── ActiveStatus
│   └── Units[]
│       ├── UnitId (unique)
│       ├── PropertyId (FK)
│       ├── UnitGroupId (for unit-type grouping)
│       ├── SquareFootage
│       ├── BedBath
│       └── Occupancies[]
│           ├── OccupancyId (unique)
│           ├── UnitId (FK)
│           ├── Tenants[] (one or more per occupancy)
│           │   ├── TenantId
│           │   ├── FirstName, LastName
│           │   ├── PhoneNumber, Email
│           │   ├── MoveInOn
│           │   └── MoveOutOn
│           └── Lease
│               ├── LeaseStartDate
│               ├── LeaseEndDate
│               ├── LeaseSignedDate
│               ├── MonthlyRent
│               └── RecurringCharges[]
│                   ├── ChargeId
│                   └── GlAccountId (FK)
│
├── Owner
│   ├── OwnerId
│   ├── ContactInfo
│   ├── Properties[] (owned properties)
│   └── OwnershipPercentage
│
├── Vendor
│   ├── VendorId
│   ├── ContactInfo
│   ├── ServiceCategories
│   └── InsuranceDocuments
│
├── GL Account
│   ├── GlAccountId
│   ├── AccountName
│   ├── AccountType (asset, liability, equity, revenue, expense)
│   ├── GlGroupId (for CAM and expense pooling)
│   └── PropertyAssociation
│
├── Transactions
│   ├── Bills (AP)
│   │   ├── BillId, VendorId, PropertyId, GlAccountId
│   │   └── Amount, PostedDate, Status
│   ├── Charges (AR)
│   │   ├── ChargeId, TenantId, GlAccountId
│   │   └── Amount, DueDate, Status
│   ├── Payments
│   │   ├── PaymentId, TenantId or OwnerId
│   │   └── Amount, Method, PostedDate
│   └── Journal Entries
│       └── GlAccountId, Debit/Credit, Amount, PostedDate
│
├── Work Orders
│   ├── WorkOrderId, PropertyId, UnitId
│   ├── Status, Priority, Category
│   ├── AssignedTo (TechnicianId or VendorId)
│   └── LinkedCharges[]
│
├── Leads (Leasing)
│   ├── LeadId, PropertyId
│   ├── ProspectContact
│   ├── Source, Status
│   └── GuestCardId
│
└── Bank Accounts
    ├── BankAccountId
    ├── AssociatedProperties[]
    └── AccountType (operating, trust)
```

### Key Relationships

- One Property has many Units
- One Unit has one active Occupancy at a time (historical occupancies retained)
- One Occupancy has one or more Tenants (co-tenants) and one Lease
- Charges and Recurring Charges reference both Occupancy/Tenant and GL Account
- Work Orders link to Unit, Property, and optionally Occupancy (for billable items)
- Owners link to Properties via ownership records (with percentage)
- GL Accounts link to GL Groups (required for CAM reconciliation)
- All financial transactions reference a GL Account ID

### GL Account Structure

Standard property management chart of accounts categories:

| Category | Examples |
|----------|---------|
| Assets | Cash (operating), Cash (trust -- security deposits), Cash (trust -- owner funds), Accounts Receivable, Prepaid Expenses |
| Liabilities | Security Deposits Held, Tenant Prepayments, AP Outstanding |
| Equity | Owner Capital, Retained Earnings |
| Revenue | Rental Income, Late Fees, Application Fees, Pet Fees, Parking Income, Laundry Income, NSF Fees, Management Fees Received (non-PM side) |
| Expenses | Repairs & Maintenance, Utilities (electric, water, gas), Insurance, Property Taxes, Management Fees, Landscaping, Cleaning, Capital Improvements, HOA Dues |

Trust accounting uses separate GL accounts to enforce segregation: security deposit trust account is distinct from operating account at the GL level, not just the bank level.

---

## Scale Characteristics

### Supported Scale

- **Minimum**: 50 units (hard minimum; pricing floor applies)
- **Practical small tier**: 50-500 units (Core plan, lean team optimization)
- **Growth tier**: 500-5,000 units (Plus plan, benefits from automation ROI)
- **Enterprise**: 5,000-10,000+ units (Max plan, full API access, dedicated CSM)
- **Platform ceiling**: AppFolio claims no hard ceiling; over 5 million units on platform total. Max plan launched early 2024 specifically for "large operators with complex and diversified portfolios."
- **One reported per-account practical limit**: ~10,000 units per account before complexity management (not a hard limit; enterprise customers can exceed this)

### Multi-Entity and Portfolio Management

- Multiple properties per account with property group and portfolio segmentation
- Owner-level portfolio views
- Portfolio-level and property-level financial reporting
- Investment Manager supports nested fund structures (investments holding positions in other investments)
- Role-based access: users assigned to specific properties or portfolios; PM controls what owners and investors see

### Role-Based Access Control

- User roles configurable for staff (leasing agents, maintenance technicians, accountants, managers)
- Property-level access scoping: staff can be restricted to specific properties
- Owner portal access controlled by PM (PM decides what data owners can view)
- Investor portal access controlled by investment manager
- Board member portals for HOA approval workflows

### Audit Trail

- Auditing Center: all staff changes, edits, and activities with user/property/date filtering
- GL General Ledger tracks transaction creation user and last-edited user (columns addable to GL report)
- Realm-X Flows Activity Logs (Spring 2025): tracks workflow template changes with attribution

### Performance at Scale

- Platform is cloud-hosted SaaS (AppFolio manages infrastructure)
- No on-premises deployment option
- API rate limit of 7 requests per 15 seconds for reporting API suggests rate-limiting is relevant for high-frequency polling; webhook-based architectures preferred for real-time use cases
- Large report extracts (5,000+ rows) require pagination; full-dataset pulls (paginate_results=false) risk timeout on very large portfolios

---

## Known Limitations and Gaps

### Commercial Real Estate

- **NNN lease complexity**: No BOMA gross-up methodology. Cannot bifurcate fixed vs. variable expenses with occupancy adjustment capping at 1.0. Complex NNN structures require workarounds or third-party tools (Stratafolio, CAMAudit).
- **Residential-first architecture**: Commercial features added over time; not designed from ground up for commercial. As portfolios grow in commercial complexity (multiple tenant types, varying exclusions, cap structures), friction increases significantly.
- **Percentage rent**: Limited native support for percentage rent billing against tenant sales reports (custom GL workaround required).
- **CAM setup complexity**: GL accounts must be manually added to GL groups or they silently drop from CAM reconciliation. No warning displayed.

### Accounting

- **No native QuickBooks sync**: Requires middleware (AvidXchange, Skywalk API, or CSV export). Frequently cited as a gap for property managers who also use QuickBooks for entity-level books.
- **Bank account defaulting**: With multiple bank accounts, bill payments may not default to the correct account, causing balance sheet errors in the Cash section.
- **Error correction**: Data entry errors are difficult to reverse without contacting AppFolio support; no self-service undo for some transaction types.
- **Additional fees**: Start/end date functionality not available in Core/Plus; Max only.

### Communications

- **Bulk owner email**: Mass email to owners requires manual copy-paste workaround; no native bulk-to-owners broadcast.
- **Bulk tenant SMS**: Cannot send a single text to multiple tenants simultaneously.

### Reporting and Analytics

- **No data warehouse push**: No native Snowflake, BigQuery, Redshift, or Databricks connector. API extraction and ETL required.
- **No SQL access for Property Manager**: Standard and Plus tiers have no SQL-level access. Max has Database API (REST, not SQL). Investment Manager Premier adds SQL export.
- **Custom calculated fields limited**: Report Builder only pulls fields that exist in the AppFolio data model; cannot create derived metrics beyond basic aggregations.
- **No predictive analytics**: No revenue optimization, demand forecasting, or predictive maintenance. These require third-party tools or custom ML pipelines consuming AppFolio data via API.

### Integrations

- **API tiered behind Max plan**: Full read/write API access only on the most expensive tier. Plus has limited read-only. Core has none. This is a significant constraint for teams wanting to build custom integrations without upgrading.
- **No webhooks catalog**: Webhook topics are not publicly documented (only `leads` confirmed). Operators must contact AppFolio to understand the full event stream.
- **Rate limiting**: 7 requests/15 seconds on Reporting API limits real-time data pipeline design. Workarounds: paginated polling, webhook-based triggers, scheduled batch pulls.

### Support and Product Maturity

- **Customer support**: Phone support by appointment only (not direct); reported average wait time of approximately one week for a 15-minute session. Chat preferred by users for faster resolution.
- **Feature pacing**: Recurring user complaint that AppFolio prioritizes new feature releases over fixing existing defects. "Overly focused on rolling out new features instead of fixing existing ones."
- **Learning curve**: 3-way bank reconciliation and some accounting workflows cited as unintuitive; "more steps than necessary" for basic tasks.

### Scale Ceiling

AppFolio is generally considered appropriate up to ~10,000 units per account, beyond which operators with complex portfolios (institutional commercial, mixed international structures, multi-fund investment vehicles) typically migrate to Yardi Voyager or MRI Software. The Max plan with Database API extended this ceiling when launched in 2024, and rapid adoption was reported by AppFolio in Q3 2025 earnings. The platform does not have a hard unit ceiling, but operational complexity management becomes the constraining factor before any system limit.

---

## Integration Patterns for CRE Orchestrator

This section documents how an AI agent or orchestration layer should interact with AppFolio data and workflows at institutional scale.

### Data Extraction Patterns

**Pattern 1: Scheduled Batch Extract (Reporting API v2)**
Best for: financial reporting, owner reporting packages, delinquency monitoring, rent roll snapshots.

```
1. Authenticate: HTTP Basic Auth with Client ID + Client Secret
2. POST to endpoint: https://{db}.appfolio.com/api/v2/reports/{report}.json
3. Include filter parameters: property_visibility, date range, accounting_basis
4. Handle pagination: check for next_page_url in response; loop until null
5. Parse JSON response; validate Amount as string with two decimal places
6. Rate limit: stay under 7 req/15s; implement exponential backoff on 429
7. Cache result sets (valid for 30 min per AppFolio docs)
```

**Pattern 2: Incremental Change Detection (Stack API, Max tier)**
Best for: real-time property/tenant/lease data sync, CRM enrichment, portfolio monitoring dashboards.

```
1. Use LastUpdatedAt / LastUpdatedAtFrom filter on entity endpoints
2. Poll on configurable cadence (5-min for high-frequency use cases, respecting rate limits)
3. Maintain local cursor (last_sync_timestamp) per entity type
4. Handle 429s with backoff; handle 401s by regenerating credentials
5. Write to internal data store (PostgreSQL, data lake) for downstream analytics
```

**Pattern 3: Webhook-Driven Event Processing (Stack API, Max tier)**
Best for: leasing pipeline monitoring, maintenance escalation, payment event processing.

```
1. Register webhook endpoint with AppFolio (contact database.api.support@appfolio.com)
2. Verify JWS signature on all incoming webhooks (RSASSA_PSS_SHA_256)
3. Parse event topic (e.g., "leads") and payload
4. Trigger orchestrator workflow based on event type
5. Acknowledge receipt immediately (return 200); process async to avoid timeout
```

### Report Consumption Patterns

**Financial Reporting Package (Monthly)**
```
Reports to pull per property/portfolio:
- income_statement.json (cash and accrual, property-level and aggregate)
- balance_sheet.json (requires properties filter)
- cash_flow.json
- general_ledger.json (for audit/reconciliation)
- aged_payables_summary.json
- charge_detail.json (for AR aging)

Orchestrator responsibility:
- Schedule pulls on the 2nd business day of each month (after month-end close)
- Transform currency strings to decimals before computation
- Aggregate property-level P&Ls to fund/portfolio level
- Compare to prior period and budget; flag variances > threshold
- Generate owner reporting package; push to Investor Portal or distribute via email
```

**Delinquency Monitoring (Weekly or Daily)**
```
- Pull charge_detail.json or delinquency endpoint
- Flag accounts > X days past due
- Cross-reference with payment_plans to exclude tenants on active plans
- Trigger Realm-X Flows delinquency follow-up automation via API write (Max tier)
  or alert PM staff via webhook/notification integration
```

**Rent Roll Snapshot (On-Demand or Weekly)**
```
- Pull occupancies from Stack API: /occupancies endpoint
- Join with unit data: /units endpoint
- Join with lease data: /leases endpoint
- Construct rent roll: unit, tenant name, lease start/end, monthly rent, status
- Compare to prior snapshot to detect vacancies, new leases, lease expirations
```

### Workflow Triggering Patterns

**Lease Expiration Pipeline**
```
1. Query occupancies where LeaseEndDate within 90/60/30 days
2. Check if renewal offer already sent (lead status or occupancy flag)
3. If not: trigger Realm-X Flows renewal template via AppFolio (or alert leasing team)
4. Track renewal conversion rate; report weekly
```

**Maintenance Escalation**
```
1. Webhook on work order creation (if webhook available) or poll work_orders endpoint
2. Flag work orders: status = open, created_at > 48h, no assigned vendor
3. Escalate to PM or trigger Realm-X Maintenance Performer dispatch
4. Track open work order aging; alert on SLA breach
```

**Owner Distribution Automation**
```
1. On month-end close (date trigger):
   - Pull owner statement data via income_statement.json and balance_sheet.json
   - Validate distribution amount against trust account balance
   - Write distribution record via Stack API (Max tier)
   - Trigger owner payment via AppFolio payment processing
   - Publish owner statement to Owner Portal
```

### Monitoring Patterns

**Portfolio Health Dashboard**
```
Pull daily or weekly:
- Occupancy rate: (occupied units / total units) per property
- Delinquency rate: (past-due balance / total rent billed)
- Days-to-lease: from vacancy date to new lease start
- Work order aging: open orders by age bucket
- Maintenance cost per unit: work order billings / unit count

Alert thresholds (configurable):
- Occupancy < 93% for > 14 days
- Delinquency > 5% of rent roll
- Average days-to-lease > 21 days
- Open work orders > 30 days without resolution
```

**API Health and Data Quality Monitoring**
```
- Track API response times and error rates per endpoint
- Alert on sustained 429 (rate limit pressure) or 500 (system errors)
- Validate Amount field format (string with two decimals) on ingestion
- Cross-check balance sheet: total assets should equal total liabilities + equity
- Flag orphan records: charges without associated GL account, work orders without property
```

### Authentication and Credential Management

```python
# Credential setup pattern
import base64

client_id = os.environ["APPFOLIO_CLIENT_ID"]
client_secret = os.environ["APPFOLIO_CLIENT_SECRET"]
database = os.environ["APPFOLIO_DATABASE"]  # subdomain: {database}.appfolio.com

# Basic Auth header construction
credentials = f"{client_id}:{client_secret}"
encoded = base64.b64encode(credentials.encode()).decode()
headers = {
    "Authorization": f"Basic {encoded}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Base URL
base_url = f"https://{database}.appfolio.com/api/v2/reports"
```

Credential rotation: AppFolio allows credential regeneration from the API Settings page; coordinate rotation with dependent systems to avoid 401 interruptions. Store in secrets manager (Azure Key Vault, AWS Secrets Manager), not in environment files or repos.

### Tier Requirements for Orchestrator Integration

| Capability | Core | Plus | Max |
|-----------|------|------|-----|
| Financial report extraction | Partial | Yes | Yes |
| Full entity CRUD (tenants, leases, units, vendors) | No | No | Yes |
| Webhook event subscriptions | No | No | Yes |
| Write-back (create work orders, update records) | No | No | Yes |
| Bulk bill upload via API | No | Yes | Yes |
| Leasing CRM data access | No | No | Yes |
| Leasing Signals data | No | No | Yes |

**Minimum viable orchestrator integration**: Max tier is required for a full bidirectional orchestration pattern. Plus tier supports read-only reporting extraction. Core is insufficient for programmatic integration beyond scheduled report emails.
