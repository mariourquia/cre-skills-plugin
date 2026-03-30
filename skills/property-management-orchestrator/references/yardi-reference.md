# Yardi Voyager -- Skill Reference

> Last updated: 2026-03-26. Sources: Yardi.com product pages, developer documentation, user reviews, partner resources.

---

## Platform Overview

### Market Position

Yardi Systems is the dominant enterprise property management platform in commercial real estate. Founded 1984, privately held, headquartered in Santa Barbara. The platform claims more than 450 active interface partners and services more vendors, APIs, units, and square footage than any competitor. Yardi Voyager competes directly with RealPage and MRI Software at the enterprise tier; AppFolio and Entrata at mid-market. In property management category market share metrics, RealPage leads at ~5%, Yardi Voyager at ~1.7% (distinct from broader Yardi product lines which rank higher overall).

Primary differentiator: single-database architecture across all modules. No middleware, no nightly syncs, no file imports between components. Every module -- tenant portal, maintenance work orders, investment accounting, construction management -- reads and writes the same underlying database. This eliminates the data reconciliation overhead that plagues multi-vendor stacks.

### Product Tiers

| Tier | Target | Threshold | Notes |
|---|---|---|---|
| Yardi Breeze | Small portfolios | Under ~300 units | SaaS, simplified UI, residential and basic commercial |
| Yardi Breeze Premier | Mid-market | 100-800 units | Adds commercial recoveries, job costing, investment accounting |
| Yardi Voyager | Enterprise | 500+ units, complex structures | Full module set, configurable workflows, investment suite, commercial |
| Yardi Voyager 7S | Enterprise SaaS | Same as Voyager | Browser-agnostic, mobile-enabled SaaS deployment on Yardi Cloud |
| Yardi Voyager 8 | Enterprise (current) | Same as Voyager | Modernized UI, Virtuoso AI integration, Report Builder, AR/renewals dashboards |

Breeze and Voyager share the same underlying database architecture, enabling straightforward tier migrations.

### Pricing Model

Pricing is not publicly listed for Voyager; Yardi requires direct contact for quotes. Observed pricing data:

- **SaaS (UK GSI pricing as reference)**: Voyager Select at £0.0200/sq ft/yr; CommercialCafe Tenant Portal at £0.0080/sq ft/yr; Private Cloud at £50,000 flat fee/yr
- **Per-unit floor**: Minimum ~$150/month reported; some sources cite $1,200/month minimum for full enterprise
- **Professional services**: ~$150/hour for implementation
- **Interface partner fees**: $25,000/year per interface for third-party vendors connecting via Yardi's Standard Interface Partner Program
- **Implementation timeline**: 3-12 months depending on portfolio size and customization depth
- **Customization**: Bespoke report customization generates additional fees; one reviewer cited a jump from $30,000 to $150,000 annually during migration

---

## Product Suite Map

```
Yardi Platform
├── Core PM
│   ├── Voyager Residential
│   ├── Voyager Commercial
│   ├── Voyager Affordable Housing
│   ├── Voyager PHA (Public Housing Authorities)
│   ├── Voyager Senior Living
│   ├── Voyager Student Housing
│   ├── Voyager Single Family
│   └── Voyager Condo/Co-op/HOA
│
├── Leasing & Marketing
│   ├── RentCafe Suite (residential)
│   │   ├── RentCafe Leasing (CRM, online applications, screening)
│   │   ├── RentCafe Living (resident portal, payments, work orders)
│   │   └── REACH by RentCafe (digital marketing agency)
│   └── CommercialCafe Suite (commercial)
│       ├── CommercialCafe Tenant Portal
│       ├── CommercialCafe Marketing (ILS, brochures)
│       ├── CommercialCafe.com (ILS listing site)
│       └── Deal Manager (commercial deal pipeline)
│
├── Financials & Procurement
│   ├── Procure to Pay Suite
│   │   ├── PayScan (AP automation, invoice processing)
│   │   ├── Smart AP (AI OCR for invoices)
│   │   ├── Bill Pay (payment processing)
│   │   ├── Marketplace (MRO procurement, 2M+ products)
│   │   ├── VendorCafe (vendor portal, self-service)
│   │   └── VendorShield (vendor credentialing, COI compliance)
│   └── Advanced Budgeting & Forecasting (AB&F)
│
├── Investment Management Suite
│   ├── Investment Manager (investor portal, CRM, distributions)
│   ├── Investment Accounting (fund-level GL, waterfalls, K-1s)
│   ├── Acquisition Manager (deal sourcing, pipeline, due diligence)
│   ├── Debt Manager (loan tracking, covenants, collateral)
│   └── Performance Manager (configurable dashboards, KPI tracking)
│
├── Construction & Facilities
│   ├── Construction Manager (project tracking, draw requests, contracts)
│   ├── Maintenance IQ (work orders, preventive maintenance, unit turns)
│   └── Facility Manager (commercial maintenance automation)
│
├── Analytics & BI
│   ├── Yardi Elevate Suite (Asset IQ, Revenue IQ, Forecast IQ, Senior IQ)
│   ├── Data Connect (Voyager-to-Power BI secure feed)
│   ├── Yardi Spreadsheet Reporting / YSR (Excel/Word custom reports)
│   └── Yardi Matrix (external market data, comps, rent surveys)
│
├── Energy & Sustainability
│   ├── Utility Invoice Processing
│   ├── Utility Billing (submeter-based resident billing)
│   ├── Sustainability Reporting (ENERGY STAR, GRESB, ESG)
│   ├── Energy Reporting & Analytics
│   ├── Energy Efficiency
│   └── Energy Procurement
│
├── AI Platform
│   ├── Yardi Virtuoso (umbrella AI platform)
│   │   ├── Virtuoso AI Agents (pre-built automation workflows)
│   │   ├── Virtuoso Composer (no-code agent builder)
│   │   ├── Virtuoso Marketplace (curated agent library)
│   │   └── Virtuoso Connectors (MCP bridge to external LLMs)
│   ├── Smart Lease (AI lease abstraction)
│   ├── Chat IQ (AI resident/tenant chat, voice, email)
│   └── Smart AP (invoice OCR via PayScan)
│
└── Compliance & Specialty
    ├── RightSource (affordable housing compliance reviews)
    ├── ScreeningWorks Pro (applicant screening)
    ├── TenantShield (commercial COI compliance)
    ├── Aspire (LMS, staff training)
    └── Yardi Kube Suite (coworking space management)
```

Elevate Suite sits between base Voyager and Yardi Matrix: it aggregates Voyager operational data and enriches it with benchmarking from Matrix. Deal Manager, Asset IQ, Forecast IQ, Construction Manager, and Facility Manager are all modules within or adjacent to Elevate.

---

## Core Modules

### Financial Management (GL, AP, AR, Budgeting)

**General Ledger**
- Property-based GL: each property operates as its own accounting entity
- GAAP and IFRS compliant
- Chart of accounts organized into hierarchical tree: assets (1000s), liabilities (2000s), equity (3000s), revenue (4000s), operating expenses (5000s)
- Account trees enable virtual remapping for owner/investor reporting without maintaining separate COAs
- Non-postable accounts serve as category headers; postable accounts receive transactions
- Segmented approach: single expense account with property segment distinguishes property-level activity (preferred by most large operators) vs. separate property-level accounts
- Recurring journal entries post on schedule (monthly, quarterly, annually)
- Multi-entity consolidation supported for fund-level and portfolio-level financials
- Intercompany transactions across entities

**Accounts Receivable**
- Charge codes define billing items (rent, CAM, parking, utilities, late fees)
- Automated late fee calculation and posting
- Delinquency tracking with Collections Dashboard (Voyager 8)
- Batch billing across portfolio
- Straight-line rent calculations (GAAP compliance for commercial)
- Retail overage billing (percentage rent for retail tenants)
- CAM recovery billing and year-end reconciliation

**Accounts Payable**
- Invoice entry, approval routing, payment processing
- Three-way matching: invoice vs. PO vs. receiving document
- Payment options: EFT, virtual credit card, check
- Vendor setup with 1099 tracking
- Duplicate invoice detection
- PayScan / Smart AP for AI-powered invoice automation (see Procurement section)

**Budgeting**
- Base Voyager: property-level budget entry, variance reporting vs. actuals
- Advanced Budgeting & Forecasting (AB&F) adds:
  - Model property framework refreshed annually from actual rent roll
  - Market Leasing Assumptions (MLAs): renewal probability, unit downtime, rent terms, TI allowances, leasing commissions
  - Historical GL data transfer with customizable parameters
  - Inflation tables for multi-year forecasts and DCF valuations
  - Seasonal expense schedules
  - Account relationship-based projections
  - Scenario/what-if modeling without affecting live lease records
  - Check In/Check Out for multi-user concurrent budget editing
  - Function Groups for batch portfolio-wide forecasting runs
  - Task Runner for off-hours batch processing
  - Real-time workflow visibility across budget cycle participants
  - Excel copy/paste for bulk data updates

**Standard Financial Reports**
- Income statements (property-level and consolidated)
- Balance sheets
- Trial balances
- Rent rolls (detailed and summary)
- GL analytics (transaction-level drill-down)
- Segment analytics (by entity, property, department)
- AR/AP analytics (delinquency, vendor invoice aging)
- Bank analytics (reconciliation, cash management)
- Tenancy schedules

**Yardi Spreadsheet Reporting (YSR)**
- Replaces legacy Crystal Reports
- Connects Voyager data to Excel and Word templates
- 40+ pre-built Voyager Analytics data sources; custom SQL queries also supported
- Report Packets: automated distribution of multiple reports in PDF, Excel, or combined formats
- Robotic Process Automation (RPA): scheduled execution, consolidated report grouping, conditional email distribution
- Yardi Correspondence: bulk communications with electronic signature capability
- Used for: institutional owner packages, lender compliance, executive dashboards, portfolio KPI summaries

---

### Leasing & Marketing (RentCafe)

**RentCafe Leasing**
- CRM IQ: prospect and applicant lifecycle management; guest cards, pipeline tracking
- Online leasing: digital applications, fraud prevention, electronic lease signing
- Applicant screening integration via ScreeningWorks Pro
- Guest card, payment, screening result, and document auto-population in Voyager -- no manual re-entry
- Chat IQ: AI bot answering inquiries across chat, text, email, and voice using live property data
- REACH by RentCafe: full-service digital marketing (SEO, PPC, reputation management, social media)
- RentCafe.com ILS: apartment search site and listing syndication network

**RentCafe Living (Resident Portal)**
- Move-in guided checklist
- Online rent payment: multiple payment options, recurring payments, ACH at no charge
- Maintenance request submission with photo uploads
- Lease renewal signing
- Rewards program tracking
- Unified login from application through residency
- Native mobile app

**Voyager 8 Renewals Dashboard**
- Tiles tracking expiring leases, pending proposals, move-out tasks
- Bulk editing across multiple leases simultaneously
- Automated workflow: pending, signed, countersigned status tracking
- Automated rent adjustment logic tied to renewal terms

---

### Maintenance (Maintenance IQ)

- Mobile work order creation, assignment, and real-time tracking
- Preventive maintenance scheduling with drag-and-drop tools
- Recurring work order templates
- Inspection management: configurable templates, photo capture, damaged item tracking
- Unit turns and rehabs: milestone tracking, cost monitoring, vacancy day reduction
- Real-time dashboard: unified view of work orders, rehabs, and inspections
- Technician mobile app: on-site task completion, photo documentation, parts ordering via Yardi Marketplace
- AI Maintenance IQ (announced 2025): faster diagnosis, automated documentation
- Integration with VendorCafe for vendor bid management and invoice visibility
- Integration with Facility Manager for commercial properties

**Facility Manager (Commercial)**
- Automation of commercial maintenance workflows
- Preventive maintenance scheduling across commercial portfolio
- Integration with Deal Manager and Construction Manager

---

### Commercial Management (COMMERCIALCafe)

**Voyager Commercial Core**
- Lease administration: industrial, office, and retail properties
- All lease terms in one location: rent schedules, escalations, options, clauses
- Straight-line rent (GAAP) automated calculation
- CAM reconciliation: pro-rata allocation by square footage, year-end true-up, automated reconciliation letters
- Retail percentage rent / overage billing
- Recoveries: expense books, reconciliation, amendments
- Tenant billing automation
- Supported property types: office, industrial, retail, airports, government, harbors, parks

**CAM Reconciliation Workflow**
1. Designate property as commercial, configure tenants with pro-rata shares
2. Tag CAM-related payables to recoverable expense accounts during AP entry
3. Year-end: run automated reconciliation -- calculates tenant share vs. estimated payments
4. System generates additional charge or credit; automated reconciliation letters emailed to tenants

**CommercialCafe Tenant Portal**
- Self-service lease payments, autopay setup, ledger viewing
- Maintenance request submission with photo upload and status notifications
- Retail sales data entry (for percentage rent tracking)
- Native mobile app (iOS and Android)
- TenantShield: insurance/COI compliance tracking (self-service and full-service tiers)

**CommercialCafe Marketing**
- Automated custom listings, email campaigns, brochures
- Google Analytics integration for campaign tracking
- Photography and virtual tour services
- CommercialCafe.com ILS and Yardi Listing Network syndication

**Deal Manager**
- Commercial deal pipeline from lead to lease execution
- Real-time pipeline visibility with CRM interface
- Automatic comparison of deal economics to budgets and prior leases
- Metrics tracked: NER, GAAP rent, TI allowances, leasing commissions, lease term
- Customizable approval workflows tied to financial thresholds
- Legal module: auto-generates lease documents from templates and clause libraries, routes approvals, captures e-signatures
- Activity feeds, task management, document centralization
- Mobile access for brokers and leasing teams
- Integration with Voyager Commercial and Elevate Suite -- executed leases sync to accounting immediately

**Smart Lease (AI Lease Abstraction)**
- OCR scanning of commercial lease documents
- ML-based clause detection trained on portfolio-specific patterns
- Data extracted directly into Voyager Commercial lease records
- Human review-and-approve workflow; manual drag-and-drop for missed clauses
- AI Q&A assistant: natural language queries about lease terms within Voyager
- Bulk processing queue for portfolio-wide onboarding
- Current scope: new commercial leases; renewals planned

---

### Procurement (PayScan, Procure to Pay)

**PayScan / Smart AP**
- Smart AP (AI/OCR engine): extracts vendor, property, dates, PO numbers, invoice notes, totals on upload
- Automated approval routing via configurable workflows
- Email alerts for pending approvals
- Exception flagging: three-way match failures, budget threshold breaches, unregistered vendors, duplicate invoices, missing documentation
- Exception queue with designated handlers and resolution time tracking
- Payment options: virtual credit card, EFT, automatic check writing
- Electronic payables import directly to Voyager, linked to POs

**Procure to Pay Suite Components**
- **Marketplace**: 2M+ MRO products, customizable purchasing workflows, spend analytics
- **VendorCafe**: vendor self-service portal, registration, onboarding, invoice status visibility, payment detail access
- **VendorShield**: automated vendor credentialing, COI compliance monitoring, Workers Comp expiry tracking
- **Bill Pay**: automated final payment stage, multiple payment methods

**Common AP Workflows**
- Purchase order creation and approval
- Invoice receipt and three-way match
- Budget-based routing (e.g., two-layer review for invoices over $5,000)
- Regional manager sign-off for capital expenditures above thresholds
- Automated coding across all invoice fields

---

### Construction Management

**Construction Manager**
- Portfolio-wide visibility: track job progress, compare jobs by status, risk, and cost per SF
- Job costing: budget vs. actual, commitments, change orders
- Billing and draw requests: by actual cost, percent complete, or project schedule
- Draw packages: streamlined digital submission
- RFP management: creation, publication, bidding, bid comparison, bid leveling
- Contract lifecycle: creation, e-signatures, meeting coordination
- Vendor management via VendorCafe integration: bid comparison, cost variance analysis
- Customizable reports: budget amounts, revisions, commitments, change orders, billing amounts
- Custom job cost analytics
- Mobile app for field managers: payables, scanned images, approvals, contract updates
- Supports: capital expenditures, unit renovations, ground-up development
- Integration with Voyager, Deal Manager, Facility Manager, VendorCafe

---

### Investment Management Suite

**Investment Manager (Investor Relations)**
- Branded self-service investor portal with configurable dashboards
- Published metrics: distributions, returns, property-level KPIs, investment performance summaries
- Self-service document downloads: statements, tax documents, historical records
- Digital subscription workflows for new deal onboarding
- Deal room environment for tracking investor communications on new opportunities
- CRM: contact management, automated communication workflows, investor/advisor relationships
- Mobile-optimized
- Role-based access controls; advanced encryption and secure login

**Investment Accounting (Fund-Level)**
- Fund-level general ledger supporting any ownership structure: partnerships, closed-end funds, open-end funds
- Automated capital calls and waterfall distributions
- Preferred return and promote calculations
- Automated period-end financial consolidations
- K-1 generation, investor statements, regulatory filings via pre-built templates
- Reduces monthly reporting cycles from 2-3 weeks to 2-3 days (reported by users)
- Direct connection to Voyager property management data -- no manual data transfer or reconciliation

**Acquisition Manager**
- Deal sourcing and evaluation pipeline
- Deal analysis, due diligence management
- Document collection and storage
- Electronic signature capture
- Integration with Voyager and Investment Manager

**Debt Manager**
- Loan tracking across borrower and investor perspectives
- Covenant monitoring
- Collateral management
- Integration with property management system for borrower-side operations

**Performance Manager**
- Configurable dashboards with user-definable metrics
- Real-time investment performance tracking
- Portfolio-level KPI aggregation

---

### Energy & Sustainability

**Energy Suite Components**
1. **Utility Invoice Processing**: digitizes invoices, automates payment workflows, minimizes late fees
2. **Utility Billing**: submeter connectivity, cost allocation, automated resident/tenant invoicing
3. **Sustainability Reporting**: ENERGY STAR benchmarking and electronic submission, GRESB data submission, ESG disclosures
4. **Energy Efficiency**: data-driven insights on consumption reduction
5. **Energy Procurement**: budget certainty, volatility protection for energy contracts
6. **Energy Reporting & Analytics**: cost, consumption, demand, and emissions tracking; drilldown to utility meter level; portfolio benchmarking

**Data Integration**
- Consolidates energy, water, and waste data from invoices and vendors
- Deadline monitoring and automated regulatory report submission
- Full drill-down to individual meter level
- Residential: Energy Suite; Commercial: Pulse Suite

**Compliance**
- ENERGY STAR: automated benchmarking and Portfolio Manager submission
- GRESB: annual real estate ESG assessment support
- Local disclosure law tracking (e.g., NYC LL97, BERDO, Chicago MBEA)

---

## Analytics & BI Layer

### Yardi Elevate Suite

Elevate occupies the operational space between base Voyager analytics and Yardi Matrix market data. It aggregates Voyager operational data and enriches it with predictive and benchmarking capabilities.

**Component Modules**
- **Asset IQ**: operational performance insights, portfolio health dashboards
- **Revenue IQ**: rent and pricing optimization, dynamic pricing recommendations
- **Forecast IQ**: predictive analytics for revenue and NOI forecasting
- **Senior IQ**: senior living asset performance (sector-specific)
- **Deal Manager**: commercial deal analytics (see Commercial section)
- **Construction Manager**: capital project performance (see Construction section)
- **Facility Manager**: maintenance automation and analytics

All Elevate modules feed from Voyager data, ensuring no data reconciliation between operational and analytical layers.

**Key Capabilities**
- Real-time portfolio visibility across all Voyager data
- Multifaceted lease structure management: percentage rent, CAM fees, TI allowances
- Enhanced rent rolls and lease abstract management
- Predictive insights for cross-functional optimization
- Target audience: commercial portfolio professionals managing office, retail, industrial, mixed-use

### Yardi Data Connect

- Secure data feed from Voyager to Microsoft Power BI
- Automates dataflows from multiple Voyager databases into Power BI
- Starter pack: hundreds of pre-built customizable dimensions and measures
- Users can modify existing KPIs or create custom metrics
- Supports third-party data source incorporation alongside Voyager data
- Security model: inherits Voyager property-level security, row-level protections in Power BI, workspace-level access controls
- Clients typically begin extracting insights on day one; custom metric expansion follows
- Also integrates with Qlik (Replicate product) for data replication

### Yardi Matrix (External Market Intelligence)

Separate product from Voyager; sold independently or as complement. Covers:
- **Multifamily**: properties 50+ units across 180+ markets; rent, occupancy, supply pipeline, rent growth trends; monthly rent survey
- **Commercial**: office, industrial, self-storage, vacant land data
- **Affordable housing**: fully affordable properties with program, ownership, and subsidy tracking
- **Competitive market analysis**: submarket and custom micro-market rent rate history
- **Comps**: full ownership/management contacts, loan maturity schedules, sales history
- **Data depth**: property-level, owner-level, submarket-level

When Yardi Elevate and Matrix are combined, Voyager operational data benchmarks against Matrix market data for peer comparison and underwriting calibration.

---

## API & Integration Layer

### Architecture Overview

Yardi uses SOAP APIs as the primary programmatic interface. REST endpoints exist for specific newer products but SOAP/XML is the standard for Voyager data access. API documentation is WSDL-based -- each interface has its own WSDL URL; WSDLs serve as the technical specification but lack plain-language endpoint descriptions.

### Available Interfaces (SOAP)

Major interface categories (each requires a separate partner agreement at $25,000/year for third parties):
- **Billing & Payments**: resident transaction data, charge history, payment posting
- **Vendor Invoicing**: invoice submission, status, approval routing
- **Service Requests**: work order creation and status
- **Common Data**: property, unit, prospect, contact data
- **Commercial API**: property, unit, lease, and rent roll export
- **ILS / Unit Availability**: unit availability export for listing syndication (UnitAvailability_Login endpoint)
- **Guest Card**: prospect/lead submission from third-party ILS
- **Screening**: applicant data export, screening result import

### Authentication & Access Patterns

- SOAP with HTTP Basic Authentication (username/password per interface)
- Credentials are interface-specific; separate client instances required per interface
- WSDL URL is the discovery mechanism for each interface
- No publicly documented REST API for core Voyager data
- Newer products (Virtuoso Connectors) use MCP protocol

**Example SOAP endpoint pattern:**
```
https://www.yardipcv.com/{database}/webservices/{InterfaceName}.asmx?op={MethodName}
```
Parameters passed in XML envelope; responses are XML hierarchical structures.

### Yardi Virtuoso Connectors (MCP)

Announced 2025, generally available for early access in late 2025 with broader rollout planned for early 2026:
- Bridges Yardi data to external LLMs via Model Context Protocol (MCP)
- Initial LLM: Claude (Anthropic); additional LLMs planned via MCP compatibility
- Provides real-time, read-oriented access to Voyager operational and financial data
- Connector logic hosted within the chosen LLM's environment
- Enables natural language queries over live Yardi data: portfolio budget variance, maintenance risk, rental trends, financial scenarios
- Supports "Bring Your Own AI Assistant" (BYOAA) workflows
- Data remains protected by Yardi's underlying security protocols at the connector layer
- No manual data extraction or spreadsheet export required

### Yardi Systems Integrator (Standard Interface Partner Program)

- Third-party vendors connecting to Yardi must apply to the Standard Interface Partner Program
- Application requires: contact info for three mutual clients
- Annual fee: $25,000 per interface integrated
- Separate agreement per interface
- Yardi provides credentials after agreement execution; vendor builds integration and beta-tests with pilot client
- 450+ active interface partners in network

### Data Connect & File-Based Integration

- **Data Connect** (Power BI): real-time secure feed, layered security matching Voyager permissions
- **Replicate** (Qlik): real-time data movement to cloud for reporting
- **Document Management for SharePoint**: centralizes documents from Voyager into SharePoint
- **File-based interfaces**: SFTP-based batch exchanges for legacy integrations; CSV/XML formats

### Third-Party Integration Categories

| Category | Examples |
|---|---|
| Tenant screening | ScreeningWorks Pro (native), TransUnion, Experian |
| Payment processing | Built-in (ACH, credit card, virtual card) |
| ILS syndication | RentCafe.com, CommercialCafe.com, Zillow, Apartments.com |
| Document management | SharePoint integration |
| Business intelligence | Power BI (Data Connect), Qlik (Replicate) |
| Access control | Building access systems (resident/tenant data sync) |
| Vendor management | VendorPM and similar COI/compliance platforms |
| AP automation | Bottomline and similar payment automation vendors |
| Insurance | TenantShield (native), third-party COI tracking |
| Energy/utilities | Utility providers, ENERGY STAR Portfolio Manager |
| Smart home / IoT | Partner ecosystem (no dominant native integration documented) |
| EHR (senior living) | Interface partners for electronic health records |

---

## Reporting & Analytics

### Report Taxonomy

**Built-in Financial Reports**
- Income statement (property-level and consolidated)
- Balance sheet
- Trial balance
- General ledger detail
- Cash flow statement
- Variance reports (actual vs. budget, vs. prior year)

**Built-in Operational Reports**
- Rent roll (residential and commercial)
- Occupancy and vacancy reports
- Delinquency / aging reports
- Lease expiration schedules
- Unit availability reports
- Move-in / move-out reports

**Built-in AR/AP Reports**
- Receivables aging
- Vendor invoice aging
- Payment history

**YSR (Custom Excel/Word Reports)**
- Institutional owner packages
- Lender compliance reports
- Executive dashboards
- Portfolio KPI summaries
- Uses 40+ pre-built Voyager Analytics data sources or custom SQL

**Yardi 7S Analytics Modules**
- Financial Analytics: income statements, balance sheets, account tree reporting
- General Ledger Analytics: transaction-level review
- Segment Analytics: by entity, property, department
- Residential/Commercial Analytics: operational and lease-level KPIs
- AR/AP Analytics: delinquency tracking, vendor invoice reporting
- Bank Analytics: reconciliation and cash management
- Tenancy Schedules: structured lease and tenant data

### Owner/Investor Reporting

- **Yardi Correspondence**: bulk communication tool replacing manual letter/email workflows; used for owner statements, rent notices, delinquency letters
- **Report Packets**: group multiple reports for automated distribution (PDF, Excel, combined)
- **RPA (Robotic Process Automation)**: scheduled execution, conditional email distribution, data validation -- converts multi-day reporting cycles into automated exception-monitoring workflows
- **Investment Manager portal**: self-service investor access to distributions, returns, K-1s, historical documents

### Voyager 8 Report Builder

- Drag-and-drop custom report creation from property, unit, prospect, and resident tables
- Pivot-style reports buildable in minutes without IT involvement
- Smart filtering by property, property list, date range
- Saved reports for consistent reuse

### Benchmarking

- Yardi Elevate modules (Asset IQ, Revenue IQ) benchmark against portfolio peers
- Yardi Matrix integration enables external market benchmarking (asking rents, occupancy, supply pipeline)
- ENERGY STAR and GRESB benchmarking via Energy Suite

---

## Workflow Automation

### Workflow Designer

Yardi's workflow system is configurable at implementation. Workflows wrap accountability around user roles and automate routing for:
- Purchase orders
- Invoices and payables
- Work orders
- Vendor setup
- Leasing approvals
- Lease renewals
- Budget modifications
- Capital expenditure requests

**Approval Chain Configuration**
- Multi-layer approval: e.g., two-level review for invoices over $5,000
- Regional manager sign-off for lease renewals above rent thresholds
- Automated email notifications at each workflow step
- Timeout reminders for items pending too long
- Workflows can auto-attach to expense types so any PO/Invoice/Payable with that code follows the configured chain

### Scheduled Automation

- Recurring journal entries post on configurable schedule (monthly, quarterly, annually)
- Automated late fee calculation and posting on charge due dates
- Automated rent adjustment on lease escalation dates (CPI, fixed, step-up)
- Automated CAM estimate billing monthly; year-end reconciliation trigger
- Budget variance alerts when actuals deviate beyond configured thresholds
- Maintenance preventive work order auto-creation on schedule
- Report Packets auto-distribute on configured schedule
- RPA jobs run after-hours for batch operations

### Virtuoso AI Agents (2025+)

Pre-built agents in Virtuoso Marketplace automate:
- Work order review and purchase order preparation (saves 15-30 min/property/day)
- Month-end financial reconciliation (reported reduction from 20+ hours to under 5 hours/property)
- Vendor invoice routing and AP processing (60% reduction in AP processing time reported)
- Maintenance coordination workflows

**Virtuoso Composer**: no-code drag-and-drop interface for building custom agent flows. Teams can design, test, and deploy agents without developer involvement.

---

## Data Model

### Entity Hierarchy

```
Management Company (top-level entity, owns the Yardi database/instance)
  └── Fund / Investment Entity (for investment-managed portfolios)
      └── Property (accounting entity; each property is its own GL)
          ├── Building (physical structure within property)
          │   └── Unit / Space (leasable unit; residential unit or commercial suite)
          │       └── Lease (binding agreement between landlord and tenant)
          │           ├── Tenant / Resident (person or company on lease)
          │           ├── Charge Codes (rent, CAM, parking, storage, utilities)
          │           ├── Rent Schedule (base rent, escalations, concessions)
          │           └── Recoveries (CAM estimates, year-end true-up)
          ├── Vendor (AP payee; linked to property for expense coding)
          └── Work Order (maintenance task; linked to unit or common area)
```

**Commercial-Specific Additions**
- Space hierarchy supports multi-tenant floors, suites, and common areas
- Lease record holds: lease type (NNN, gross, modified gross), options (renewal, expansion, termination), pro-rata share, base year, exclusions
- Recoveries: expense books with controllable/non-controllable distinction; admin fee markup
- Retail: sales reporting periods, breakpoint definitions for percentage rent

**Residential-Specific Additions**
- Unit type classification (studio, 1BR, 2BR, etc.)
- Amenity tracking at unit and property level
- Concession tracking (free rent periods, move-in specials)
- Subsidy tracking for affordable housing (HAP contracts, vouchers)

### GL Structure

- Each property is its own GL entity with its own chart of accounts instance
- Account numbers follow configured numbering convention (standard: 1000s-5000s as above)
- Account trees allow virtual remapping of COA for reporting purposes without changing underlying account structure
- Segments: most large operators use a segmented approach -- one expense account (e.g., 5100) with a property segment code distinguishing each property's activity
- Inter-entity journal entries for management fees, overhead allocations, and intercompany loans

### Single-Database Architecture

All modules share one database. Consequence: zero data lag between operational and financial views. When a resident pays rent through RentCafe, the payment posts to the GL and appears on financial reports immediately. When a lease is executed via online leasing, charge codes and start dates propagate to AR billing, lease administration, and financial analytics with no manual re-entry.

---

## Scale Characteristics

### Portfolio Size

- Designed for 500+ unit operations; no documented upper limit
- Enterprise clients manage 10,000 to 100,000+ units on single instances
- Yardi is used by institutional operators, REITs, private equity real estate funds, pension fund advisors, and large owner-operators
- Supports multiple portfolios and asset types on a single platform (residential, commercial, affordable housing, senior living all on same GL)

### Multi-Entity & Global

- Multi-entity management: unlimited properties, buildings, and funds within one database
- Joint venture structures supported via ownership layering in Investment Accounting
- Global deployment options:
  - **Single global database**: centralized reporting, standardized configuration, lower infrastructure cost; trade-off is performance latency for geographically distant users and single point of failure
  - **Multiple regional databases**: regional regulatory compliance, better local performance, data sovereignty; trade-off is fragmented reporting requiring consolidation tools (e.g., DataFreedom or Data Connect)
- Multi-currency: systematic currency conversions and consolidations for cross-border portfolios
- Multi-language: supported for global deployments (specific language coverage not publicly documented in detail)

### Security & Compliance

- **Role-Based Access Control**: ~5,000 individual permissions configurable through user group assignments
- Property-level security: users restricted to properties within their purview; closed property access blocked
- Function-level permissions: button-level control, charge code/GL security, delete access, check/ACH authorization, posting rights
- Audit logging: User Security Analytic reports, Security Permissions reports, transaction change logs
- **SOC Compliance**: annual SOC 2, biannual SOC 1 (SSAE 18), PCI, Sarbanes-Oxley data storage compliance
- CSA Star Level 2 certified (Cloud Security Alliance)
- AES 256-bit encryption for data at rest
- YardiOne: SSO integration, MFA, stronger password policy enforcement
- Cloud-hosted (Yardi Cloud): multiple firewall layers, intrusion prevention systems

### Performance Considerations

- Single-database architecture simplifies consistency but concentrates load
- Timeout issues cited frequently in user reviews, especially under heavy concurrent usage
- Adobe Flex legacy components remain in parts of the platform (Voyager 7S era) -- being replaced in Voyager 8
- Performance latency is the primary driver for organizations to consider regional database splits in global deployments

---

## Known Limitations & Gaps

### Complexity & Learning Curve

- Extremely steep learning curve; new users require substantial ramp-up time before leveraging full capability
- Configuration complexity requires dedicated Yardi administrators or consultant engagement
- ~5,000 permissions must be deliberately configured; permission drift is a real operational risk at scale
- Implementation timeline: 3-12 months; organizations with complex portfolios or legacy data typically hit the 9-12 month range
- Yardi offers eLearning (Aspire LMS) and YASC (annual user conference) for training, but self-service documentation is limited compared to modern SaaS products

### UI & UX

- Voyager 7S interface described as "Web 1.0 look and feel" -- functional but dated
- Navigation can be inefficient; multiple steps required for common tasks
- Voyager 8 addresses this with modernized UI, Collections Dashboard, Renewals Dashboard, and Report Builder
- Legacy Adobe Flex components still present in some modules

### Customization Constraints

- Report customization generates additional fees (users report steep charges for custom reports)
- Workflow Designer is powerful but requires deep system knowledge to configure correctly
- Customizations must be re-validated after major version upgrades
- API access for third parties requires the $25,000/year per-interface fee -- significant barrier for smaller integration partners

### Customer Support

- Most frequent complaint in user reviews: support quality is inadequate
- Long wait times, inconsistent knowledge among support staff
- Escalations for customization needs often go unresolved
- Better outcomes reported with authorized Yardi consulting partners than direct Yardi support

### Cost Structure

- Total cost of ownership is high: licensing + implementation professional services + ongoing administration + per-interface API fees + customization charges
- Migration costs can escalate dramatically (reported $30,000 to $150,000 jump during version migrations)
- Pricing opacity: no published rates; requires sales engagement for any quote

### Performance & Technical Debt

- Frequent timeout errors reported by enterprise users during peak usage
- Some modules still depend on older framework components (Adobe Flex)
- Performance at very large scale (100,000+ units globally) may require regional database architecture, adding reporting complexity

### Feature Gaps (vs. Competitors)

- AppFolio and Entrata rated higher for ease of use and modern UX at mid-market
- RealPage rated higher for advanced revenue management analytics
- MRI Software rated comparably for enterprise commercial; stronger in certain niche compliance scenarios
- Yardi's AI features (Virtuoso) are newer and still maturing vs. some pure-play AI property tech tools

---

## Integration Patterns for CRE Orchestrator

### How an AI Orchestration Agent Interacts with Yardi

An external AI orchestrator (like this codebase's agents) interacts with Yardi through several access patterns, ordered from lowest friction to highest:

#### Pattern 1: Virtuoso Connectors (MCP) -- Preferred for 2026+

- Yardi's MCP connector exposes live Voyager data to Claude and other MCP-compatible LLMs
- The orchestrator agent queries Yardi data in natural language without managing SOAP/XML
- Use cases: portfolio budget variance queries, NOI monitoring, delinquency flags, maintenance risk assessment, lease expiration alerts
- Access: requires early access enrollment with Yardi; available through Virtuoso platform
- Data is real-time; read-oriented; no write operations documented yet
- Grounded responses reduce hallucination risk -- AI answers are anchored to live operational data

#### Pattern 2: Yardi Data Connect (Power BI) -- For Reporting Extraction

- Data Connect feeds Voyager data into Power BI as structured datasets
- Orchestrator can consume Power BI datasets via Power BI REST API for structured financial and operational data
- Use cases: pulling income statements, rent rolls, occupancy metrics, AR aging into downstream analysis
- Requires existing Power BI environment; Data Connect licensing
- Security: inherits Voyager property-level permissions; row-level security in Power BI

#### Pattern 3: SOAP API (Interface Partner Program) -- For Transactional Write Operations

- Required for any write operations: posting payments, creating work orders, submitting invoices, updating lease data
- Requires Yardi Interface Partner Program enrollment ($25,000/year per interface)
- Authentication: HTTP Basic Auth per interface instance
- Protocol: SOAP/XML; WSDL-based endpoint discovery
- Python SDK available (open source: `yhavin/yardi-sdk` on GitHub) -- covers Billing & Payments, Vendor Invoicing, Service Requests, Common Data
- XML responses require parsing; hierarchical structure varies by interface
- Separate client instances required per interface type

#### Pattern 4: File-Based Export/Import -- For Bulk Operations

- Voyager supports SFTP-based file exchange (CSV, XML) for bulk data operations
- Common for: GL export to external accounting systems, bulk lease import during onboarding, utility bill import
- Not real-time; batch cadence only
- Suitable for: data warehouse ingestion, bulk tenant communications, mass import of historical data

### Orchestrator Agent Use Cases by Module

| Module | Orchestrator Access Pattern | Data Available | Write Possible |
|---|---|---|---|
| Financial (GL, P&L) | MCP Connectors, Data Connect, YSR export | Income statements, balance sheets, trial balance, variance | No (read-only via MCP) |
| Rent Roll | MCP Connectors, Commercial API (SOAP), Data Connect | Unit, lease, tenant, rent, expiration, options | No |
| Lease Administration | Smart Lease API (within Voyager), SOAP | Lease terms, clauses, CAM, escalations | Via Smart Lease UI |
| AR / Collections | Data Connect, Billing & Payments SOAP | Delinquency, charge codes, payment history | Post payments via SOAP |
| AP / Invoices | Vendor Invoicing SOAP, Smart AP | Invoice status, approval chain status | Submit invoices, route approvals |
| Work Orders | Service Requests SOAP | Work order status, assignments, costs | Create/update work orders |
| Budgets | YSR export, Data Connect | Budget vs. actual, variance | Via AB&F UI or SFTP import |
| Investment Reporting | Investment Manager API, Data Connect | Distributions, NAV, returns, K-1 data | No documented write |
| Energy/Utilities | Energy Suite API (partner-level) | Consumption, cost, ENERGY STAR scores | Invoice submission |
| Market Data | Yardi Matrix API (separate product) | Comps, rent surveys, supply pipeline | Read-only |

### Monitoring Patterns

An orchestrator monitoring a Yardi-managed portfolio should watch for:

1. **Delinquency spikes**: AR aging via Billing & Payments SOAP or Data Connect -- trigger collection workflow when 60+ day balances exceed threshold
2. **Budget variance alerts**: GL actuals vs. budget via Data Connect -- flag properties exceeding 10% variance; escalate to asset management
3. **Lease expiration risk**: rent roll data -- identify leases expiring within 12 months with no renewal activity; trigger leasing outreach
4. **CAM reconciliation deadlines**: lease record data -- flag properties approaching year-end without completed reconciliation setup
5. **Work order aging**: Service Requests SOAP -- flag open work orders older than SLA threshold; escalate to property manager
6. **Invoice approval bottlenecks**: Vendor Invoicing SOAP -- identify invoices pending approval longer than configured threshold; send escalation
7. **Capital project overruns**: Construction Manager data via Data Connect -- flag jobs where committed costs exceed budget by defined percentage
8. **Investor reporting deadlines**: Investment Manager data -- trigger report packet generation and distribution workflow
9. **ESG/compliance deadlines**: Energy Suite and local ordinance tracking -- flag properties with approaching benchmark submission deadlines
10. **Vacancy duration**: Maintenance IQ / rent roll -- flag units with turn times exceeding portfolio average; escalate to regional manager

### Key Data Fields for Underwriting / Acquisition Analysis

When using Yardi data to support acquisition analysis via this orchestrator:

- **Rent roll fields**: `unit_id`, `tenant_name`, `lease_start`, `lease_end`, `base_rent`, `rent_psf`, `square_footage`, `pro_rata_share`, `options` (renewal/expansion/termination), `rent_escalation_type`, `cam_estimate`
- **CAM fields**: `expense_book_id`, `controllable_expenses`, `non_controllable_expenses`, `admin_fee_pct`, `base_year`, `cap_pct`
- **Financial fields**: `gl_account`, `property_id`, `period`, `actual_amount`, `budget_amount`, `variance_pct`
- **Market data (Matrix)**: `asking_rent`, `effective_rent`, `occupancy_rate`, `concession_pct`, `new_supply_units`, `absorption_rate`

### Integration Limitations to Design Around

1. **No public REST API for core Voyager data**: SOAP only; build SOAP client abstraction layer
2. **Per-interface cost**: budget $25K+/year per data type if going through formal partner program; explore MCP Connectors as lower-friction alternative
3. **WSDL gaps**: endpoint descriptions are sparse; test each endpoint empirically; maintain a schema registry internally
4. **No real-time webhooks documented**: orchestrator must poll on schedule rather than react to Yardi events
5. **Write operations require partner enrollment**: read-only use cases via MCP Connectors can proceed faster
6. **Security inheritance**: respect Voyager's property-level security in any data pipeline; do not aggregate data across entities the user does not have access to
7. **Performance**: avoid hammering SOAP endpoints during business hours; schedule bulk extracts for off-peak windows
8. **Version sensitivity**: customizations and integrations must be re-validated after Voyager version upgrades (7S to 8 is a significant UI/API shift)
