# Medical Office Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `medical_specialties` | list | specialties present in building (primary care, dental, imaging, surgery center, etc.) |
| `regulated_waste_generator` | boolean | whether any tenant generates regulated medical waste |
| `surgery_center` | boolean | ambulatory surgery center present (triggers additional compliance) |
| `extended_hours` | boolean | whether building operates beyond standard business hours (evenings, weekends) |
| `backup_power` | enum | none, partial_generator, full_generator, ups_plus_generator |
| `medical_gas_systems` | boolean | piped medical gases (oxygen, nitrous oxide, vacuum) present |
| `hipaa_physical_controls` | boolean | whether common areas require HIPAA physical safeguard compliance |
| `imaging_equipment` | boolean | MRI, CT, X-ray equipment present (triggers shielding and structural requirements) |

## Workflow Outline (Full Module Scope)

- **Medical Waste Management**: Coordinate regulated medical waste (RMW) pickup schedules, maintain waste manifests, verify hauler licensing, track sharps container placement and replacement, and ensure compliance with state-specific medical waste regulations.
- **HIPAA Physical Safeguard Compliance**: Manage physical access controls (badge access, visitor management, after-hours lockdown), signage compliance, document destruction services, common area privacy (waiting area separation), and security camera placement restrictions near patient areas.
- **Specialty HVAC & Mechanical**: Manage HVAC systems requiring precise temperature and humidity control (imaging rooms, surgery suites, labs). Track air exchange rates, pressure relationships (negative pressure for isolation, positive for surgery), and filter replacement schedules (HEPA where required).
- **Extended Hours & After-Hours Access**: Manage building access for practices operating evenings/weekends, after-hours HVAC scheduling and billing, cleaning schedule coordination around patient hours, and emergency access protocols for medical emergencies in the building.
- **Tenant Compliance Monitoring**: Track tenant compliance with lease-required medical licensing, malpractice insurance, DEA registration (if applicable), state health department inspections, and patient safety certifications.

## Key Metrics (Medical Office-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| HVAC uptime for critical areas | >99.5% | Surgery centers, imaging, labs require near-continuous operation |
| Medical waste pickup compliance | 100% | No missed pickups; regulatory penalties for non-compliance |
| After-hours HVAC recovery rate | >95% | Billing accuracy for extended-hours tenants |
| Tenant insurance compliance | 100% | Medical malpractice + GL + WC for all practices |
| Emergency power test frequency | Monthly | Generator load testing per code and lease requirements |
| Patient complaint rate | <2/month | Building-level complaints (parking, access, temperature) |
| Cleaning infection control score | >4.5/5.0 | Quarterly audit using healthcare-grade standards |
| Building access incident rate | 0 | Unauthorized access to restricted areas |

## Integration Points

- **building-systems-maintenance-manager**: Specialty HVAC, medical gas systems, emergency power maintenance
- **coi-compliance-checker**: Medical malpractice insurance verification, specialized coverage requirements
- **compliance-regulatory-response-kit**: Health department inspection coordination, ADA compliance
- **vendor-invoice-validator**: Medical waste hauler invoice verification against manifests

---

TODO: Full implementation targeted for v3.0
