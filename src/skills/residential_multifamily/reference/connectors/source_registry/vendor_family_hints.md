# Vendor Family Hints

Non-binding orientation notes. The connector layer is vendor-neutral: the core of this subsystem carries no vendor code, credentials, or adapters. These hints exist only to help operators recognize which vendor family a given source probably belongs to so they can pick the correct `vendor_family` value when registering a new source in `source_registry.yaml`.

This file is a stub hint document, not a vendor adapter catalog. Every statement below is a general observation; any real integration must be validated against the vendor's actual current documentation and terms.

The `vendor_family` field in the source registry is intentionally an open string (not an enum) so new families can be added without a schema change. The list below is the starter set the stubs in `source_registry.yaml` reference.

## pms domain

### yardi_family

- Typically exports property, unit, lease, ledger, delinquency, prospect, work-order, and turn data.
- Property codes are often short alphanumeric strings that do not match operating names; the `property_master_crosswalk.yaml` resolves the mismatch.
- Lease lifecycle is modeled with a rich state machine; lease events such as legal notice served and skip may live as free-form notes rather than structured events. Expect partial event coverage.
- Unit renumbering after renovation is common; manual master-data updates are often required.

### realpage_family

- Similar object coverage to the yardi family but often with different internal identifiers and a stronger emphasis on rent-roll exports.
- Lead and tour data are sometimes split across the PMS and a separate leasing CRM module; confirm which module emits the data during adapter build.
- Lease concession tracking may use abbreviated codes that require mapping against the subsystem's concession taxonomy.

### entrata_family

- Commonly used both as a PMS and a leasing CRM. The same vendor family may appear as the source for both `pms`-domain and `crm`-domain feeds.
- Prospect data tends to be richer than in PMS-only systems. Protected-class guardrails (see ontology.md `Lead.preferences` and `Lead.notes`) must be enforced on import.

### appfolio_family

- Often used by smaller portfolios. Payment tendering and AP workflows are tightly integrated inside the same platform.
- Vendor records, agreements, and payment records all may live together in the same export, which is why the registry stub lists the `ap` domain rather than splitting across pms and ap.

## gl domain

### generic_erp

- Placeholder label for any corporate ERP that owns the general ledger: examples include MRI, Sage Intacct, NetSuite, Microsoft Dynamics, and in-house ledgers. This family does not pick one vendor.
- Chart of accounts structures vary widely; the canonical mapping is carried in `../master_data/account_crosswalk.yaml`.
- Budget and forecast tables may be stored in an FP&A system (Adaptive Insights, Anaplan, Planful, or a spreadsheet) separate from the ledger. The starter registry captures one shared-drive budget fallback (`budget_shared_drive_dropbox`) for this scenario.
- Capex may be posted at parent project level with child splits kept elsewhere; `capex_project_crosswalk.yaml` resolves.

## crm domain

### entrata_family (crm role)

- See the pms section for caveats. When entrata_family is used on the CRM side only, expect lead / tour / application coverage without lease or ledger data.

### realpage_family (leasing CRM modules)

- Typically exports lead and tour data in the same shape as the PMS module but with its own identifier space.

### generic_crm

- Placeholder label for specialized leasing CRMs or portfolio-wide sales tooling not native to a PMS. Schema coverage varies significantly; confirm during adapter build.

## ap domain

### appfolio_family

- See pms section.

### generic_erp

- Corporate ERPs that own AP also appear here. Vendor dedup against the construction tracker's vendor master is the common hard case and is resolved via `vendor_master_crosswalk.yaml`.

## market_data domain

### costar_family

- Broadest market coverage. Concession data is typically derived and should be treated as estimate, not audited lease data.
- Submarket taxonomy does not align with internal submarket labels; mapping lives inside the `../market_data/` connector.

### generic_market_data

- Placeholder for RealPage Market Analytics, Apartment List index, Yardi Matrix, or operator-owned comp pools. Quality and cadence vary.

## construction domain

### procore_family

- Commonly used for active construction tracking. Commonly overlaps with the GL for capex projects, change orders, and draw requests; `capex_project_crosswalk.yaml`, `change_order_crosswalk.yaml`, and `draw_request_crosswalk.yaml` resolve identity.
- Vendor (subcontractor) records overlap with AP; `vendor_master_crosswalk.yaml` resolves.

### generic_construction_tracker

- Placeholder for Sage 300 Construction and Real Estate, CMiC, Buildertrend, and operator-built tools. Coverage of bid packages, change orders, draws, and schedule milestones varies by product.

## hr_payroll domain

### generic_hr_payroll

- Placeholder for any HRIS / payroll system: Workday, ADP, Paychex, BambooHR, in-house, etc.
- The hardest identity problem is that an employee may be assigned across multiple properties; the subsystem resolves this via `employee_crosswalk.yaml` with an explicit list of property assignments.
- Contractors are often comingled with employees in payroll exports and must be flagged distinctly. See `employee_crosswalk.yaml`.

## manual_upload domain

### spreadsheet_workflow

- Covers budget, forecast, and ad-hoc uploads authored in a spreadsheet and dropped via a shared drive or email.
- The hardest problems are property name mismatches and inconsistent spreadsheet schemas; the crosswalk layer resolves the first, the mapping layer resolves the second.

### operator_owner_portal

- Third-party operator-owned portals or SFTP drops. File names and internal schemas vary by operator.
- When a third-party operator is the PMS for the asset, this source can stand in for the pms domain entirely. Stub lifecycle is always `planned` or `stubbed` until the per-operator adapter is validated.

### utility_billing_intake

- Utility providers submit invoices in non-standard formats; most deployments will need an OCR or normalization step upstream of the connector layer.

### compliance_intake

- Generic label for vendor insurance certificates, regulatory program reporting, and other compliance artifacts. Cadence is on_demand or quarterly. Legal sensitivity is typically high.

## Disclaimer

Vendor names are referenced only for orientation. This subsystem does not depend on any particular vendor and does not ship vendor adapters. The connector contracts in `../pms/`, `../gl/`, `../crm/`, `../ap/`, `../market_data/`, and `../construction/` are the authoritative interface; the source registry names specific source instances of those contracts; vendor families are a human-readable cue for which contract applies.
