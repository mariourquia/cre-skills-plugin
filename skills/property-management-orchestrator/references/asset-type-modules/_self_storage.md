# Self-Storage Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `total_units` | int | total rentable storage units |
| `unit_mix` | object | breakdown by size (5x5, 5x10, 10x10, 10x15, 10x20, 10x30) with count and rate |
| `climate_controlled_pct` | float | percentage of units with climate control |
| `drive_up_units` | int | number of ground-level drive-up access units |
| `interior_units` | int | number of interior-access units (hallway) |
| `rv_boat_parking` | int | number of outdoor vehicle/RV/boat parking spaces |
| `gate_access_system` | string | access control system vendor and model |
| `security_cameras` | int | number of surveillance cameras on property |

## Workflow Outline (Full Module Scope)

- **Revenue Management & Pricing**: Dynamic rate optimization using occupancy-based pricing tiers, street rate vs. web rate management, existing customer rate increase (ECRI) programs, promotional pricing lifecycle management, and competitor rate monitoring.
- **Unit Mix & Availability Optimization**: Track demand by unit size, identify oversupplied and undersupplied sizes, model partition wall moves for unit reconfiguration, and optimize climate-controlled vs. non-climate mix based on demand signals.
- **Access Control & Security**: Manage gate access systems (code generation, delinquent lockout, access log monitoring), security camera system maintenance, lighting adequacy, and perimeter security. Track unauthorized access attempts and after-hours activity.
- **Climate Monitoring**: Temperature and humidity monitoring for climate-controlled buildings, alert thresholds for system failures, tenant notification protocols for climate excursions, and insurance claim documentation for climate-related damage.
- **Lien & Auction Process**: Manage state-specific self-storage lien law compliance: delinquency notification timelines, lien filing procedures, auction notice requirements, auction execution (live or online), and proceeds accounting. Every step has jurisdiction-specific statutory requirements.

## Key Metrics (Self-Storage-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| Physical occupancy | 88-94% | Optimal range; above 94% indicates pricing opportunity |
| Revenue per available SF (RevPASF) | Track monthly | Primary revenue management KPI |
| ECRI success rate | >85% | Percentage of existing customers accepting rate increase |
| Average length of stay (months) | 12-18 | Longer = more stable revenue |
| Online reservation conversion | >30% | From website inquiry to move-in |
| Delinquency rate (>30 days) | <5% | Lower than other asset types due to lien leverage |
| Gate access incidents/month | <3 | Unauthorized access or system failures |
| Climate excursion events/year | 0 | Any temperature/humidity breach in controlled units |

## Integration Points

- **rent-optimization-planner**: Dynamic pricing strategy and rate increase modeling
- **tenant-delinquency-workout**: Delinquency management adapted for self-storage lien law context
- **building-systems-maintenance-manager**: Climate control systems, gate access hardware, security systems
- **property-performance-dashboard**: Self-storage-specific KPI dashboard with RevPASF tracking

---

TODO: Full implementation targeted for v3.0
