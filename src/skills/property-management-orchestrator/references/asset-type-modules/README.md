# Asset-Type Modules Index

This directory contains asset-type-specific extension modules for the property-management-orchestrator skill. Each module provides type-specific input fields, workflow modifications, key metrics, and integration points that supplement the core 10 workflows.

## Module Status

All modules are currently in **stub framework** status. Full implementation is targeted for v3.0.

## Module Inventory

| Module File | Asset Type | Scope | Key Differentiators |
|---|---|---|---|
| `_multifamily.md` | Multifamily | Unit-level ops, resident services, amenity management, turnover acceleration | Unit mix, concessions, resident events, amenity programming, affordable housing compliance |
| `_office.md` | Office | TI coordination, base building services, after-hours HVAC, conference facilities | Tenant improvement projects, janitorial specifications, energy management, lobby presentation |
| `_retail.md` | Retail | Percentage rent, co-tenancy, common area programming, tenant sales | Sales reporting, percentage rent audits, co-tenancy enforcement, seasonal programming |
| `_industrial.md` | Industrial | Yard/lot ops, dock management, clear height, environmental | Dock door maintenance, yard management, environmental compliance, minimal tenant interaction |
| `_mixed_use.md` | Mixed-Use | Component allocation, shared systems, cross-use conflicts | Pro-rata expense allocation, shared parking, noise/access conflicts between uses |
| `_medical.md` | Medical Office | Medical waste, HIPAA physical, specialty HVAC, after-hours access | Biohazard waste management, HIPAA physical safeguards, extended hours, specialty HVAC |
| `_self_storage.md` | Self-Storage | Unit mix optimization, access control, climate monitoring, lien/auction | Revenue management, gate access systems, climate-controlled units, lien law compliance |
| `_hospitality.md` | Hospitality | Guest experience, F&B, housekeeping, franchise compliance, RevPAR | Daily operations cadence, brand standards, housekeeping management, food safety |

## Usage

When the property-management-orchestrator identifies the asset type from the property profile, it loads the corresponding module stub to supplement its core workflows with type-specific logic. For mixed-use properties, multiple modules are loaded and results are aggregated at the property level.

## v3.0 Roadmap

Full module implementation will include:

- Complete workflow overrides and extensions per asset type
- Type-specific report templates
- Expanded KPI benchmarks per asset type and subtype
- Integration with downstream skills tuned for each asset type
- Automated asset-type detection from property profile data
