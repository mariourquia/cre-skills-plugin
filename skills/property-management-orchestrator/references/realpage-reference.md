# RealPage -- Skill Reference

> Last updated: 2026-03-26. Sources: DOJ filings, RealPage product pages, Wikipedia, Propmodo, G2, Capterra, Wilson Sonsini, ProPublica, Yale TAP, multifamily industry publications.

---

## Platform Overview

**Company**: RealPage, Inc. Founded 1998 via acquisition of Rent Roll, Inc. Headquartered in Richardson, TX.

**Ownership**: Thoma Bravo acquired RealPage in April 2021 in an all-cash transaction at $88.75/share, valuing the company at approximately $10.2 billion. Now private.

**Scale**: 24+ million housing units under management worldwide. 13,000+ clients. 7,500+ employees. Dominant in US institutional multifamily; also covers commercial, single-family, student, senior, affordable, and vacation rentals.

**Market Position**: #1 in real estate software market share (13.4% as of 2024), ahead of Yardi, CoStar/STR, and AppFolio. Leading platform for large institutional operators (Greystar, Equity Residential, AvalonBay, Camden, Lincoln Property, American Campus Communities). Revenue management (YieldStar/AIRM) is the product that put RealPage on the map for institutional operators -- and the product at the center of antitrust litigation.

**Revenue Model**: Per-unit monthly subscription plus module add-ons. Pricing is not publicly published. Estimated threshold for enterprise contract negotiation: ~$200K ACV. Commercial pricing runs ~$12.50/month per 10,000 sq ft (office/retail) and ~$7.30 for industrial. Multifamily per-unit pricing varies by product bundle and portfolio size.

**Target Customer**: Institutional property owners and operators managing 5,000+ units. REITs, private equity real estate funds, large property management companies. Not positioned for single-family residential or small landlords (Buildium, a RealPage subsidiary, serves that market).

### Product Suite Evolution

RealPage assembled its platform almost entirely through acquisition:
- 1998: Founded via acquisition of Rent Roll (PMS for multifamily)
- 2012: Acquired YieldStar (revenue management -- algorithmic rent pricing)
- ~2016: Acquired LeasingDesk (screening, insurance)
- ~2017: Acquired Axiometrics (apartment market data -- became Market Analytics)
- 2018: Acquired ClickPay ($218M -- electronic payments, 2.3M units)
- 2019: Acquired On-Site (leasing platform)
- 2019: Acquired Modern Message (resident engagement)
- 2019: Acquired American Utility Management and SimpleBills (utility management)
- 2019: Acquired Stratis (IoT/smart building)
- 2019: Acquired Lease Rent Options / LRO (revenue management competitor, merged with YieldStar)
- 2020: Acquired Buildium (SMB property management)
- 2021: Acquired WhiteSky (bulk internet/MDU connectivity) and Boingo Wireless Multifamily
- 2021: Acquired IMS (Investor Management Services -- waterfall, LP/GP reporting)
- 2025: Acquired Livble (installment rent payment)

This acquisition-heavy history is the root cause of module fragmentation: many products share a brand but were built independently and integrate imperfectly.

---

## Product Suite Map

| Category | Product | Prior Brand / Notes |
|---|---|---|
| Property Management | OneSite | Core PMS; all asset types |
| Resident Experience | LOFT (formerly ActiveBuilding) | Resident portal, payments, community |
| Revenue Management | AI Revenue Management (AIRM) | Formerly YieldStar; DOJ consent decree applies |
| Revenue Management (legacy) | LRO | Merged into AIRM pipeline |
| Leasing & CRM | Knock CRM | Acquired; multifamily-native CRM |
| AI Platform | Lumina AI Workforce | OpenAI partnership; 5 specialized agents |
| Screening | LeasingDesk Screening | CRA-registered; credit, criminal, rental history |
| Insurance | eRenterPlan / DepositFree | Renters insurance + security deposit alternatives |
| Payments | RealPage Payments / ClickPay | ACH, card, money order, installment (Livble) |
| Spend Management | Source-to-Pay / OpsBuyer | Procurement, AP, vendor management |
| Utilities | Utility Management | Billing, submetering, energy management |
| Marketing | ILS Syndication + Contact Center | Lead gen, call capture, ad spend optimization |
| Facilities | Mobile Facilities / Maintenance | Work orders, inspections, preventive maintenance |
| Business Intelligence | RealPage BI | Portfolio dashboards, benchmarking, scorecards |
| Market Analytics | Market Analytics (Lumina-powered) | Formerly Axiometrics; 425+ markets, daily updates |
| Institutional / Investment | AIM + IMS | Asset management, waterfall, LP/GP investor portal |
| Commercial | RealPage Commercial | Office, retail, industrial lease management |
| Affordable Housing | OneSite Affordable | HUD, Section 8, LIHTC compliance modules |
| Student Housing | OneSite Student | By-the-bed leasing, roommate matching |
| Integration Layer | RealPage Exchange (RPX) | 150+ certified AppPartners, standardized APIs |

---

## Core Modules

### OneSite (Property Management & Accounting)

**What it is**: The flagship PMS. Described as "the multifamily industry's leading property management system." Handles the complete property operations lifecycle from prospect to move-out.

**Key Features**:

*Leasing & Resident Lifecycle*
- Prospect tracking, waitlist management, appointment scheduling
- Online application, identity verification, income verification
- Lease generation, eSignature, document management
- Move-in / move-out / transfer processing with unit condition workflows
- Lease expiration tracking and automated renewal workflows
- Delinquency management and collections workflow
- Resident ledger management

*Accounting & Financial Management*
- Property-level and corporate-level general ledger (GAAP)
- Accounts payable with custom approval workflows
- Accounts receivable with automated payment matching
- Bank reconciliation with automated GL-to-bank matching (RealPage Bank Feeds)
- Budgeting, forecasting, and variance analysis via Budget Variance Portal
- Month-end close automation (claimed 80% time savings; some tasks 7 min → 30 sec with Lumina AI)
- Job cost tracking for capital projects and renovations
- Digital disbursements (ACH/check automation for vendor payments, resident refunds)
- GAAP-compliant fixed asset management
- CAM reconciliation (commercial and mixed-use)

*Operations*
- Real-time portfolio views: properties, buildings, floor plans, units, availability
- Document management with standardized workflows
- Spend management and vendor oversight integration
- Compliance and risk management dashboards
- Staff training via built-in Learning Management System

*Asset Type Variants*
- OneSite Conventional: Standard multifamily
- OneSite Affordable: HUD National Standards (NSPIRE), Section 8, LIHTC, HOME, HOPWA compliance
- OneSite Student: By-the-bed, roommate matching, parental guarantors
- OneSite Senior: AL/IL-specific workflows
- OneSite Military: BAH, government lease compliance

**Data entities in OneSite**: Property > Building > Floor Plan > Unit > Lease > Resident (Tenant). Ancillary entities: Vendor, Work Order, GL Account, Bank Account, Prospect, Application.

**Lumina AI within OneSite**: Lumina AI Operations Agent handles move-in audits, renewals processing, reporting, and month-end close tasks. Lumina AI Finance Agent handles invoice coding, GL error detection, and account reconciliation.

---

### LOFT / ActiveBuilding (Resident Experience)

**What it is**: All-in-one resident-facing app and portal, rebranded from ActiveBuilding to LOFT. Formerly a standalone company; acquired by RealPage. Used alongside OneSite, not a replacement.

**Key Features**:
- Resident portal: online rent payment, lease details view, service request submission, package notifications
- Community hub: event RSVPs, amenity reservations, neighbor messaging (opt-in)
- Smart access integration: keyless entry, guest access management, smart home device control (via Stratis IoT)
- Package management: carrier notifications, package locker integration
- Amenity management: scheduling, capacity control, guest approval, charge-to-account
- Rewards and loyalty: points, gift card redemptions, exclusive offers (resident retention tool)
- eCommerce: in-app add-on services marketplace (pet rent, parking, storage, renters insurance upsell)
- Maintenance request tracking with status updates
- Digital lease renewal workflow with in-app signing

**Integration**: Bidirectionally synced with OneSite for lease data, payment posting, and work order creation.

---

### Revenue Management (AI Revenue Management / AIRM / YieldStar)

**What it is**: Algorithmic pricing engine that recommends daily rent prices for each floor plan and unit. Originally YieldStar (acquired 2012), later merged with LRO (Lease Rent Options, acquired 2019). Rebranded as AI Revenue Management (AIRM) -- the DOJ consent decree applies to this product. PMS-agnostic: integrates with non-RealPage property management systems.

**How it works**:

*Data Inputs (pre-settlement)*
- Proprietary pool: nonpublic, transactional lease data from participating RealPage clients (this is the practice the DOJ targeted -- sharing competitors' live lease data across the subscriber network)
- Competitor occupancy, rent, and concession data aggregated from the subscriber network
- Market public data: listing prices, vacancies, economic indicators

*Data Inputs (post-DOJ settlement, effective ~2026)*
- Historical data at least 12 months old from competing properties (no real-time competitor feeds)
- Property's own current lease and pricing data
- Publicly available market data
- No forward-looking or active lease data from unaffiliated properties

*Pricing Methodology*
- Logarithmic demand modeling: estimates price elasticity for each floor plan
- Occupancy and leasing velocity forecasting (short-term and long-term)
- Lease expiration management: staggers expirations to avoid concentration risk and vacancy spikes
- Seasonality adjustments
- Amenity premium optimization (balcony, view, floor, renovation tier)
- Daily rent recommendations at the floor plan and unit level
- Renewal pricing separate from new lease pricing

*Workflow*
- System generates a daily recommended rent "floor" per floor plan
- Leasing agents see the recommended price; can accept or override (within configurable guardrails)
- Post-settlement: auto-accept functions require user-set parameters; symmetric guardrails; users can set parameters permitting recommendations below previously defined floors (the old system had asymmetric guardrails that made it harder to price below the floor than above)

*Performance Claims*
- "3% to 7% revenue outperformance vs. market" (RealPage marketing)
- Average 4-day reduction in vacant days
- Reported results for B/C properties: 3-5% NOI lift

**Lease Expiration Management**
- Limits lease expirations in high-demand windows (summer)
- Pricing incentives and penalties to shift expirations
- Portfolio-level expiration staggering across a management company's properties

**Configuration**: Asset-type specific profiles (conventional, lease-up, affordable, student, renovation/value-add).

---

### Spend Management (Source-to-Pay)

**What it is**: End-to-end procurement and AP automation for property operations. Branded "Source-to-Pay." Covers everything from purchase orders through vendor payment.

**Key Features**:
- Online storefront / shopping cart using managed catalogs with negotiated vendor discounts
- Group purchasing organization (GPO) access for volume pricing leverage
- Purchase order creation and approval workflow automation (configurable approval chains)
- Invoice entry, three-way matching (PO / receipt / invoice), exception handling
- Mobile approval app for on-the-go PO approvals
- Corporate vs. site-based purchasing control modes
- Real-time spend-vs-budget visibility
- Vendor credentialing: insurance certificates, W-9, license tracking, compliance expiration alerts
- Vendor marketplace: connect with certified service providers
- Vendor payments: ACH, check, virtual card; cycle time reduced from ~30 days to ~10 days per RealPage claims
- AI-powered OpsBuyer copilot: assists with ordering, sourcing recommendations, and anomaly detection

**Utility Management (integrated module)**
- Utility bill processing and payment
- Submetering for unit-level utility billing
- Energy consumption tracking and variance analysis
- RUBS (Ratio Utility Billing System) support
- Sustainability/ESG reporting on energy and water usage
- Integration with utility data providers

---

### Screening (LeasingDesk)

**What it is**: Tenant screening solution. LeasingDesk is a registered Consumer Reporting Agency (CRA) with the CFPB. Combines credit, criminal, and rental history into a risk-scored applicant report.

**Key Features**:
- Credit report with FICO score integration
- Criminal background check (national, state, county databases)
- Eviction history (national database)
- Rental payment history database (20M+ records -- proprietary RealPage data from OneSite residents)
- Income verification (automated via third-party payroll/bank data providers)
- Identity verification
- Cost of Risk calculator: converts screening data into a predictive risk score with dollar-denominated expected loss estimate
- Ledger-level integration: historical OneSite payment behavior feeds directly into applicant scoring
- Configurable acceptance criteria per property (tiered criteria based on property class, regulatory requirements)
- Compliance: FCRA, Fair Housing, source of income laws (configurable by jurisdiction)

---

### Marketing & Leasing (Knock CRM + Contact Center + ILS)

**What it is**: Full-funnel leasing marketing stack -- from ad spend through signed lease. Knock is an acquired multifamily-native CRM. Contact Center is a managed service for call handling.

**Key Features**:

*Knock CRM*
- Lead capture from all sources: ILS, website, chatbot, phone, walk-in
- Lead deduplication and source attribution
- Pipeline management: prospect status, follow-up scheduling, tour tracking
- Automated follow-up workflows (email, text, in-app)
- Leasing team performance analytics: response time, conversion rate, closing rate, follow-up compliance
- Manager dashboards: portfolio-level leasing velocity, lead volume, cost per lease

*ILS Syndication*
- Pushes unit availability, pricing, photos, floor plans to Zillow, Apartments.com, Rent.com, and others
- Centralized listing management; updates propagate automatically from OneSite availability

*Contact Center (Managed Service)*
- 24/7 call handling by trained leasing agents
- Augmented AI: live call assistance with prospect history, property info, and suggested responses
- All calls recorded and transcribed; keyword search for coaching
- Performance KPIs reported to property management

*AI Leasing Agent (Lumina)*
- Chatbot + voice agent: responds to inquiries via chat, text, email, and phone
- Self-scheduling tours synced directly to leasing team calendar
- Post-tour follow-up automated
- Reported outcomes: 51.7% increase in answered calls, 160% more captured contact records, 125% more tours scheduled, 11 hours saved per leasing agent per property per month

*Online Leasing*
- Fully digital application: online form, ID verification, income verification, co-signer flows
- eSignature on lease documents
- Application fee payment at time of submission
- Configurable screening criteria integrated at application stage

---

### Insurance

**Products**:
- **eRenterPlan**: Renters insurance (personal property + liability). Property managers can mandate enrollment; residents can purchase through the resident portal. Compliance tracking built into OneSite (manager sees insurance status per unit).
- **DepositFree**: Security deposit alternative via surety bond. Reduces upfront move-in cost for resident; owner's risk covered by bond. Tracked in OneSite.
- **Liability to Landlord**: Gap liability policy covering damages caused by residents above standard renter's insurance limits.

---

### Maintenance & Facilities

**What it is**: Work order management, preventive maintenance scheduling, inspections, and asset tracking for on-site facilities teams.

**Key Features**:
- Work order creation from resident service requests (auto-created from LOFT portal, OneSite, or phone)
- Technician assignment, routing, and status tracking (mobile app with offline capability and auto-sync)
- Preventive maintenance scheduling: recurring tasks by frequency or meter reading
- Inspection workflows: move-in, move-out, annual, HUD NSPIRE (for affordable housing)
- Asset tracking: unit-level and building-level inventory of equipment (HVAC, appliances, etc.) with warranty and service history
- Vendor coordination: assign external vendors to work orders; vendor login for status updates
- Parts inventory management
- Mobile Facilities app: iOS/Android, offline mode, geolocation
- Integration: work orders feed cost data into OneSite accounting for maintenance expense tracking

**AI Facilities Agent (Lumina)**
- Triages incoming maintenance requests
- Suggests resolution steps based on historical similar work orders
- Coordinates scheduling between residents, technicians, and vendors

---

### Business Intelligence (BI)

**What it is**: Portfolio analytics and reporting platform native to the RealPage ecosystem. Described as "the multifamily industry's premier analytics solution."

**Key Features**:
- Customizable dashboards: drag-and-drop widgets, role-based access (site, regional, corporate)
- Foundational reports: rent roll, occupancy, delinquency, lease expiration, renewals, collections
- Scorecards: property and portfolio-level KPI scorecards with period-over-period comparisons
- Budget variance portal: actual vs. budget with drill-down to GL line items
- Performance benchmarking: property-level comparison vs. portfolio peers and market comps (built on RealPage's millions-of-units lease transaction dataset)
- Custom reporting: configurable report builder with scheduled distribution
- Data export: Excel, PDF; API access for data warehouse integration
- Operational KPIs tracked: occupancy %, economic occupancy, net effective rent, average days vacant, renewal rate, delinquency %, NOI, NOI margin, expense per unit

**Limitations**:
- Optimized for all-RealPage environments; mixed-PMS portfolios require additional integration work
- Not a general-purpose BI tool (no Snowflake-native connector, no dbt integration); operates inside the RealPage data silo
- Opaque pricing; sold as an add-on to the core platform

---

### Market Analytics

**What it is**: Multifamily market intelligence platform. Formerly Axiometrics. Used for underwriting, comp analysis, budgeting, and market research. Powered by Lumina AI for data acquisition and processing.

**Key Features**:
- Coverage: 425+ US markets, conventional apartments, build-to-rent, student housing
- Frequency: Daily updates on market-level rents, concessions, floor plan performance, occupancy
- Data sources:
  - RealPage proprietary: 30+ year historical lease transaction database (millions of units)
  - Publicly available unit-level data (Lumina AI acquires and processes daily)
  - MSCI Real Capital Analytics: $2.9T in multifamily transactions over 25 years (sales comps)
  - Econometric models for macro trend analysis
- Asset valuation: automated data-driven property valuation, rapid comp analysis
- 5-year forecasting: econometric outlook for rent growth, occupancy, supply pipeline
- Submarket granularity: market > submarket > niche level performance indicators
- Mobile apps: iOS and Android
- Use cases: acquisition underwriting, pro forma assumptions, disposition pricing, lender underwriting, budget preparation, strategic planning

---

### Investment Management (AIM + IMS)

**What it is**: Two platforms serving institutional investors and fund managers. AIM (Asset and Investment Management) is portfolio analytics and asset management. IMS (Investor Management Services, acquired 2021) is LP/GP investor relations and waterfall automation. Combined, the platforms serve ~600 GPs supporting ~90,000 LPs.

**AIM (Asset Investment Management)**
- Portfolio reporting across multifamily, commercial, office, retail, industrial, storage, senior, student, hospitality
- Asset-level and portfolio-level performance dashboards
- Data collection automation and normalization across systems
- Financial modeling integration
- KPI benchmarking vs. market and peer set
- AI/ML-powered data management services (validation, normalization, anomaly detection)
- Custom reporting for board presentations and investor communications

**IMS (Investor Management Services)**
- Investor portal: self-service performance dashboards, distribution history, capital account statements
- Waterfall engine: automated complex waterfall calculation (replaces fragile Excel models)
- Capital call management: commitment tracking, funding notifications, outstanding capital management
- Distribution processing: automated distribution calculation and disbursement
- Document management: K-1s, financial statements, deal documents, fund docs in a secure deal room
- CRM: investor relationship management with engagement history and communication records
- Investor reporting: LP statements, fund-level performance, IRR/equity multiple tracking

---

## Revenue Management Deep Dive

### Algorithmic Pricing Mechanics (Pre-Settlement)

YieldStar/AIRM operated as a multi-sided data network: participating subscribers contributed nonpublic lease transaction data (actual signed lease rents, not asking prices) which was aggregated, anonymized, and used to train pricing models for all subscribers. This meant Competitor A's actual lease-up velocity and net effective rents were feeding into Competitor B's pricing recommendations in the same submarket.

The DOJ characterized this as: "RealPage's software used nonpublic, competitively sensitive information shared by landlords to set rental prices in violation of Sections 1 and 2 of the Sherman Act." The DOJ case alleged that approximately 90% of price change recommendations were accepted by property managers, and that the platform explicitly discouraged rent negotiation with prospects.

### DOJ Consent Decree (November 2025)

Filed November 24, 2025; pending court approval as of early 2026. Key terms:

**Prohibited Practices**:
- Cannot use nonpublic data from competing properties in pricing models
- Cannot use real-time or forward-looking lease data from unaffiliated properties
- Cannot report pricing information at granularity narrower than state-wide level
- Cannot operate mechanisms that prop up minimum price floors or encourage convergence toward common pricing ranges

**Required Changes**:
- Historical data cutoff: only competitor data 12+ months old permitted
- Auto-accept functions must require user-set parameters (no silent auto-accept)
- Guardrails must be symmetric: system must allow recommendations to go below floors, not just above
- Users must be able to configure parameters permitting below-floor recommendations
- Software redesign to remove anticompetitive architecture

**Compliance Obligations**:
- Court-appointed monitor for 3 years post-approval
- Written antitrust compliance policy
- RealPage becomes a government cooperator in DOJ's ongoing case against landlord defendants
- DOJ inspection rights

**Duration**: 7 years from entry; DOJ can terminate after 4 years.

**Financial terms**: No financial penalties, no admission of wrongdoing.

### State-Level Bans (as of early 2026)

| Jurisdiction | Law | Status | Notes |
|---|---|---|---|
| California | AB 325 (amends Cartwright Act) | Effective Jan 1, 2026 | Bans algorithmic pricing using competitor data |
| New York | Donnelly Act amendment | Effective Dec 15, 2025 | Residential rental specific; RealPage suing NY (First Amendment challenge) |
| San Francisco | Municipal ordinance | Effective Aug 2024 | First city ban |
| Jersey City, Minneapolis, Philadelphia, Portland, San Diego, Seattle | Municipal ordinances | Various | City-level bans |
| Colorado | Legislature passed ban | Vetoed by Governor Polis, May 2025 | -- |

### Private Litigation

20+ class action lawsuits consolidated into MDL in Middle District of Tennessee (Nashville). As of October 2025, preliminary settlements filed: Greystar ($50M), additional landlords total $141.8M combined. Defendants agreed to restrict data sharing with RealPage and cooperate with plaintiffs pursuing claims against RealPage and remaining defendants. RealPage itself has not settled the private litigation.

### Ongoing Risk Profile

The DOJ settlement resolves federal executive branch action but does not extinguish:
- MDL private class action (pending settlement approvals; RealPage remains a defendant)
- State AG actions (New Jersey sued RealPage in April 2025)
- Constitutional challenge (RealPage suing NY -- outcome could affect state bans nationally)
- The 2026 antitrust environment: Wilson Sonsini notes "algorithmic pricing" as a top enforcement priority for 2026
- Product viability risk: the data network advantage is substantially degraded by the 12-month historical-only restriction; the core competitive edge of AIRM was real-time competitor data

---

## API & Integration Layer

### RealPage Exchange (RPX)

RPX is the integration marketplace and API platform. 150+ certified AppPartners across:
- Communications & Automation: chatbots, AI assistants, IVR
- Resident Services: package management, loyalty rewards, onboarding
- Operations: facilities management, vendor credentialing, compliance
- Financial Services: payment processing, collections, AP automation
- Smart Building: access control, IoT sensors, energy management
- Identity & Screening: ID verification, income verification

**Partner certification tiers**:
- AppPartner: certified for use across all RealPage clients; listed in Integration Marketplace
- Registered Vendor: approved for specific RealPage customers only
- All integrations must go through RPX registration/certification; legacy non-RPX connections being phased out

### API Architecture

- API key authentication (primary); OAuth available for some endpoints
- OpenAPI/Swagger specs available; Postman collections supported
- REST-based; event-based framework being introduced for key business functions
- RealPage is modernizing APIs: converting older SOAP/legacy APIs to REST
- Developer portal: `developer.realpage.com` (gated; requires RPX registration to access full docs)

**Available API categories** (from developer portal and partner documentation):
- Prospects/Leads API: create, read, update prospect records
- Leasing API: application submission, status, lease data
- Residents API: resident profile, ledger balance, contact info
- Units/Availability API: unit status, floor plan data, pricing
- Payments API: payment posting, payment method management
- Maintenance/Work Orders API: create, update, close work orders
- Inspections API: inspection results, unit condition data
- Accounting API: GL entries, AP data, vendor records
- Market Data API: comp data access (Market Analytics)

**Event-based framework**: Webhooks/event streams being introduced for real-time notifications on lease events (move-in, move-out, payment, application status changes). Not universally available across all modules as of early 2026.

**Data feeds and exports**: Scheduled flat-file exports (CSV/SFTP) remain common for BI warehouse integrations. Direct API access to operational data requires RPX certification.

### Notable Partner Integrations

- Smart home / access control: Latch, SmartRent, ButterflyMX, Schlage, Yale
- IoT / utilities: Demand Logic, PointCentral, GridPoint
- Payment alternatives: Bilt Rewards, Till (income-based rent), Livble (installment -- now acquired)
- Collections: Rent Recover, National Credit Systems
- Insurance: Rhino (deposit alternative), LeaseTrack
- Internet/MDU: WhiteSky (owned), Boingo (owned), Xfinity Communities
- Maintenance/field ops: ServiceMax integrations
- Investor reporting: Yardi Investment Management (data bridge for mixed-system portfolios)

---

## Reporting & Analytics

### Standard Financial Reports (OneSite)
- Rent Roll (current and historical)
- Delinquency Report
- Lease Expiration Schedule
- Move-In / Move-Out Summary
- Vacancy Report (physical and economic)
- Month-End Financial Package: Income Statement, Balance Sheet, Cash Flow, Trial Balance, Bank Reconciliation
- Budget Variance Report
- Accounts Payable Aging
- Accounts Receivable Aging
- Vendor Payment History

### BI Platform (RealPage BI)
- Role-based dashboards: site manager, regional, VP, CFO/COO views
- Scorecards with traffic light status indicators
- Benchmarking: property vs. portfolio peers, portfolio vs. market comps
- Operational KPIs: occupancy, EO%, NER, leasing velocity, renewal %, collections %
- Financial KPIs: GPR, net rental income, NOI, NOI margin, expense per unit, expense ratio
- Custom reports: drag-and-drop report builder, scheduled email distribution
- Export: Excel, PDF; searchable data grids

### Market Analytics Reports
- Submarket rent trend reports (daily updated)
- Concessions tracking (free months, parking, move-in specials)
- Supply pipeline: under construction, planned, permits
- Sales comp database (MSCI-powered)
- Asset valuation estimates
- 5-year rent and occupancy forecasts
- Competitive set analysis (custom comp set builder)

### Owner / Investor Reporting (AIM + IMS)
- Fund-level financial statements
- Asset-level performance vs. underwriting
- Distribution statements and waterfall detail
- Capital account statements (current balance, contributions, distributions, IRR, equity multiple)
- K-1 delivery via investor portal
- Investor portal: 24/7 self-service access to performance, distributions, documents

---

## Scale Characteristics

**Institutional Scale Support**
- Designed for portfolios from mid-size (5,000+ units) to the largest in the industry (Greystar: 800,000+ units; AvalonBay: 90,000+ units; Equity Residential: 80,000+ units)
- Multi-entity accounting: supports complex organizational structures (fund, GP entity, SPE, property-level entities) within a single ledger environment
- Multi-property portfolio views: consolidated dashboards across hundreds of properties
- Corporate vs. site-based workflow modes: centralized procurement, leasing, and accounting available for hub-and-spoke operating models
- Centralized leasing center support: contact center and Knock CRM enable off-site leasing teams to handle multiple properties

**Centralized Operations Model**
- Revenue management (AIRM) operates at the portfolio level; pricing decisions can be managed centrally by a revenue management team rather than at individual properties
- Spend management centralizes procurement with property-level visibility but corporate approval chains
- Business intelligence enables regional and corporate teams to monitor property performance without site-level access

**Geographic Scope**
- US-focused; some Canadian properties supported
- Market Analytics covers 425+ US markets
- No significant international presence for property operations (RealPage does not support IFRS accounting or non-US lease frameworks)

**Corporate Reporting**
- Consolidated financial reporting across entities
- Budget-to-actual reporting at property, regional, and portfolio level
- Investor-level reporting via IMS for fund managers
- AIM handles cross-asset-type portfolio reporting (multifamily + commercial + BTR + student in one view)

---

## Known Limitations & Gaps

### DOJ / Regulatory Risk
- Revenue management product fundamentally redesigned by consent decree; the 12-month historical-only data restriction substantially degrades the real-time market signal advantage AIRM provided
- State bans (CA, NY, and 6+ cities) prohibit the product entirely in major markets as of Jan 2026; impacts clients with large coastal portfolios
- Private MDL litigation ongoing; RealPage not yet settled; exposure to damages award
- Regulatory risk is a live concern for any operator evaluating AIRM adoption in CA or NY
- RealPage's constitutional challenge to NY law (First Amendment) is high-stakes; outcome will have national implications

### Module Fragmentation
- Platform is an acquisition stack: OneSite, LOFT, Knock, AIRM, IMS, LeasingDesk, ClickPay, Market Analytics, and Spend Management were all independent products with separate codebases
- Integration quality varies: OneSite <-> LOFT <-> Knock CRM integration is generally solid; AIM <-> IMS integration still maturing
- Different login portals for different modules; unified SSO is partial
- Data model inconsistencies across modules (e.g., unit identifiers and lease structures may not be identical between OneSite and Knock)
- Some acquired products (LeasingDesk, ClickPay) retain legacy UX that has not been fully modernized

### User Experience Complaints (from G2, Capterra, Software Advice reviews)
- "Overly compartmentalized": managing multiple properties requires selecting each property individually
- Menus and navigation not intuitive; items "not in expected locations"
- No quick resident/vehicle search across the portfolio (requires property-level navigation)
- Invoice processing has "far too many steps"
- Support is fragmented: users often redirected between departments
- Learning curve is steep for new staff; training investment required
- GUI requires numerous clicks for basic tasks
- ComplaintsBoard: 2.4/5 rating

### Integration Complexity
- RPX certification process required for all integrations; can take weeks to months
- Legacy non-RPX integrations being phased out, forcing partner recertification
- API documentation is gated behind RPX registration; not publicly accessible
- Event-based (webhook) framework is not yet available across all modules
- SFTP/flat-file data exports remain common for BI integrations -- not real-time

### Pricing and Contract Risk
- No published pricing; custom quotes required
- Long-term contracts standard; exit is expensive
- Module add-on structure: full platform value requires purchasing multiple add-ons; total cost can be significant
- Pricing is opaque; smaller operators report cost disproportionate to value if they don't use the full suite

### Competitive Gaps vs. Yardi
- Yardi Voyager: deeper compliance and regulatory support (HUD, Section 8, LIHTC) in some jurisdictions
- Yardi: stronger for mixed-use commercial portfolios with complex CAM and lease structures
- Yardi: finance-first teams prefer Yardi's accounting depth and GL configurability
- AppFolio: faster onboarding, simpler UX, better for operators who don't need institutional analytics

---

## Integration Patterns for CRE Orchestrator

### Data Extraction Patterns

**Occupancy and Leasing Data**
- Source: OneSite Units/Availability API or SFTP export (Rent Roll, Occupancy Report)
- Frequency: Daily pull sufficient for most reporting; hourly available via API for active lease-up properties
- Key fields: `unit_id`, `floor_plan_id`, `market_rent`, `effective_rent`, `occupancy_status`, `lease_start`, `lease_end`, `resident_id`
- Use case: Feed into NOI model, occupancy dashboard, budget variance monitoring

**Financial Data**
- Source: OneSite Accounting API or scheduled SFTP export (GL, AR, AP)
- Frequency: Monthly close data; daily for AR/AP aging
- Key fields: `gl_account`, `period`, `actual`, `budget`, `variance`, `property_id`, `entity_id`
- Use case: NOI actuals, budget-to-actual, expense tracking, investor reporting prep

**Market Comps / Underwriting Data**
- Source: Market Analytics API or manual export
- Frequency: Daily updates available; weekly pulls typical for underwriting workflows
- Key fields: `market`, `submarket`, `avg_effective_rent`, `occupancy_rate`, `concessions_pct`, `new_supply_units`, `absorption`
- Use case: Acquisition underwriting (comp rents, market occupancy, supply pipeline), budget assumptions, disposition pricing

**Revenue Management Signals**
- Source: AIRM pricing recommendations API (post-settlement: historical comps + own-property data only)
- Key fields: `floor_plan_id`, `recommended_rent`, `current_market_rent`, `recommended_date`, `override_flag`
- Use case: Monitor pricing vs. recommendation compliance; track revenue management lift vs. market
- Note: Post-DOJ settlement, AIRM data quality for competitive benchmarking is reduced; supplement with Market Analytics

**Investor Reporting Data**
- Source: IMS API or IMS investor portal exports
- Key fields: `fund_id`, `property_id`, `capital_contributed`, `capital_distributed`, `current_value`, `irr`, `equity_multiple`, `distribution_date`
- Use case: LP reporting packages, fund-level performance monitoring, waterfall validation

### Monitoring Patterns

**Occupancy Degradation Alert**
- Poll OneSite occupancy daily; trigger alert if occupancy drops >200 bps below budget or falls below 90% for >7 days
- Cross-reference AIRM pricing recommendations: are rents being held above market despite softening occupancy?

**Lease Expiration Concentration**
- Pull lease expiration schedule from OneSite monthly
- Flag if >15% of leases expire in a single 30-day window (concentration risk)
- Feed into renewal pricing strategy in AIRM

**Revenue Management Compliance**
- Pull AIRM recommendations vs. actual leasing rents from OneSite
- Track override rate (pct of recommendations not accepted by leasing team)
- Benchmark actual NER vs. AIRM recommended NER; persistent underperformance signals pricing management issue

**Expense Variance Monitoring**
- Pull AP data from OneSite Accounting or Spend Management weekly
- Flag line items with >20% variance vs. budget for VP review
- Utilities: compare actual utility cost per unit to benchmarks from RealPage Utility Management or ENERGY STAR

**Maintenance SLA Tracking**
- Pull open work orders from Facilities API daily
- Flag work orders open >72 hours (emergency) or >7 days (non-emergency) without resolution
- Monitor work order volume trends for predictive maintenance planning

### Revenue Management Integration Guidance (Post-DOJ)

Given the consent decree, an orchestrator integrating AIRM must account for:
1. AIRM pricing recommendations are now based on 12-month-lagged competitor data -- they are less current than pre-settlement
2. Supplement AIRM with Market Analytics daily feeds for real-time competitive benchmarking
3. Monitor override rates closely; the new symmetric guardrail design means leasing teams have more latitude to price below floors -- track whether this is being used appropriately or overused
4. In CA and NY markets: AIRM is effectively prohibited; use Market Analytics + in-house pricing models or third-party RMS (Yardi Revenue IQ, Entrata's pricing module, or purpose-built alternatives)
5. Document pricing decision process for compliance purposes; the DOJ consent decree requires audit trails

### Architectural Notes for Agent Development

- Authentication: API key per property management company; scoped to client's data only
- Rate limits: not publicly documented; enterprise clients typically negotiate per-call limits
- Best pattern for bulk data: SFTP scheduled export for historical data + API for incremental updates
- Webhook/event subscription: available for key lease lifecycle events (not yet all modules); subscribe to `lease_signed`, `move_in_complete`, `payment_posted`, `work_order_created` events where available
- Data normalization: RealPage unit IDs and property codes are client-defined, not universal -- an orchestrator must maintain a client-specific mapping table
- Multi-entity: a single API key may cover multiple properties; use `property_id` filter on all queries to avoid cross-property data leakage in reporting
- IMS data: accessible via separate IMS API credentials; different auth and base URL from OneSite APIs
- Market Analytics: separate API contract and authentication from property management APIs; often sold and provisioned separately
