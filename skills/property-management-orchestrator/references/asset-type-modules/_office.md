# Office Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `rentable_sf` | int | total rentable square feet (BOMA measured) |
| `common_area_factor` | float | load factor / loss factor (e.g., 1.15 for 15% load) |
| `floor_plate_sf` | int | typical floor plate size |
| `parking_ratio` | float | spaces per 1,000 RSF |
| `base_year_structure` | enum | base_year, expense_stop, modified_gross, triple_net |
| `after_hours_hvac_rate` | float | hourly charge for after-hours HVAC |
| `conference_center` | boolean | shared conference facility on-site |
| `lobby_renovation_date` | int | year of last lobby renovation |

## Workflow Outline (Full Module Scope)

- **Tenant Improvement Coordination**: Manage TI projects from design approval through construction and punchlist. Track TI allowance burn rates, change orders, and landlord vs. tenant responsibilities per lease.
- **Base Building Services Management**: Janitorial specifications and audits, day porter deployment, lobby presentation standards, common area maintenance scheduling, and conference facility operations.
- **Energy & Sustainability Management**: After-hours HVAC tracking and billing, BAS optimization, ENERGY STAR benchmarking, LED retrofit tracking, and tenant energy guide distribution.
- **Tenant Experience Program**: Lobby ambassador service, tenant app adoption, building-wide event programming, fitness center management, and food service coordination (if applicable).
- **Stacking Plan & Space Planning**: Maintain digital stacking plan, track contiguous availability, coordinate with leasing on prospect tour readiness, and manage spec suite programs.

## Key Metrics (Office-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| Janitorial cost per RSF | $1.40-$2.20 | Class A; Class B typically 15-20% lower |
| Security cost per RSF | $0.80-$1.50 | Varies by market and building profile |
| After-hours HVAC recovery rate | >95% | Of charges billed vs. actual cost |
| Tenant retention rate | 65-75% | Higher for credit tenants with long terms |
| Average TI project duration | 60-120 days | From lease execution to tenant occupancy |
| Lobby presentation score | >4.0 / 5.0 | Internal audit quarterly |
| ENERGY STAR score | >75 | Top quartile for building type |
| Elevator wait time (peak) | <45 seconds | Measured during morning arrival |

## Integration Points

- **building-systems-maintenance-manager**: Base building MEP systems, elevator, BAS maintenance
- **cam-reconciliation-calculator**: Base year / expense stop reconciliation calculations
- **stacking-plan-builder**: Visual stacking plan generation from rent roll
- **leasing-operations-engine**: Tour readiness, spec suite coordination, prospect pipeline

---

TODO: Full implementation targeted for v3.0
