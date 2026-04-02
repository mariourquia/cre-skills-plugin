# Industrial Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `clear_height_ft` | int | clear ceiling height in feet |
| `dock_doors` | int | number of loading dock doors |
| `drive_in_doors` | int | number of grade-level drive-in doors |
| `trailer_parking_spaces` | int | number of trailer parking stalls in yard |
| `yard_sf` | int | total exterior yard/staging area in square feet |
| `rail_served` | boolean | rail spur or rail siding access |
| `environmental_phase` | enum | none, phase_1_clean, phase_1_rec, phase_2_active, remediation |
| `tenant_lease_structure` | enum | triple_net, modified_gross, absolute_net |

## Workflow Outline (Full Module Scope)

- **Dock & Door Operations**: Dock door maintenance scheduling (springs, levelers, seals, bumpers), dock door utilization tracking, drive-in door maintenance, and dock area cleanliness standards.
- **Yard & Lot Management**: Trailer parking allocation and enforcement, yard surface maintenance (grading, drainage, pothole repair), perimeter fencing and security, stormwater management, and truck route maintenance.
- **Environmental Compliance**: Phase I/II tracking, stormwater pollution prevention plan (SWPPP) maintenance, hazardous materials storage compliance, spill response protocols, and air quality permits for tenant operations.
- **Exterior Maintenance**: Roof inspections (critical for large-footprint buildings), parking lot maintenance, exterior lighting, landscaping (minimal), signage, and building envelope (tilt-up panel joints, metal panel corrosion).
- **Tenant Coordination**: Minimal day-to-day interaction typical for NNN industrial; focus on lease compliance (use restrictions, environmental obligations, insurance requirements), annual property inspections, and capital obligation tracking.

## Key Metrics (Industrial-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| Operating expense ratio | 0.22-0.34 | Very low due to NNN structure |
| R&M cost per SF | $0.80-$1.30 | Lowest of all asset types |
| Dock door maintenance per door/yr | $550-$800 | Includes springs, levelers, seals |
| Roof repair cost per SF | $0.10-$0.25 | Annual average; large roofs = significant total |
| NNN recovery rate | 93-98% | Percentage of expenses recovered from tenants |
| Tenant retention rate | 68-80% | Typically high due to relocation cost |
| Average days to lease | 60-90 | Market dependent; shorter in tight markets |
| Yard surface maintenance per SF | $0.05-$0.15 | Annual for gravel/asphalt maintenance |

## Integration Points

- **carbon-audit-compliance**: Industrial emissions, energy benchmarking, BPS compliance
- **building-systems-maintenance-manager**: Roof systems, fire suppression, dock equipment lifecycle
- **coi-compliance-checker**: NNN tenant insurance verification and environmental liability coverage
- **lease-abstract-extractor**: NNN expense pass-through provisions, environmental obligations

---

TODO: Full implementation targeted for v3.0
