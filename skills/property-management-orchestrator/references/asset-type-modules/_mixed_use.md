# Mixed-Use Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `components` | list | list of component objects, each with: type (residential, office, retail, hotel), sf, units_or_suites, occupancy |
| `shared_systems` | list | building systems shared across components (HVAC, elevator, parking, lobby, security) |
| `allocation_method` | enum | sf_pro_rata, component_metered, hybrid |
| `shared_parking_spaces` | int | total shared parking spaces |
| `parking_allocation` | object | spaces allocated by component and time-of-day |
| `condominium_structure` | boolean | whether components are in separate condo units with separate tax lots |
| `master_association` | boolean | whether a master association governs shared elements |
| `component_pm_structure` | enum | single_pm_all, separate_pm_per_component, hybrid |

## Workflow Outline (Full Module Scope)

- **Component-Level Allocation**: Allocate shared expenses (utilities, security, maintenance, insurance) across components using the defined allocation method. Reconcile at the property level and produce component-level P&Ls that roll up to a consolidated statement.
- **Shared Systems Management**: Manage building systems that serve multiple components -- shared HVAC plants, central chiller/boiler, shared elevator banks, master fire alarm, shared parking structures. Track usage metering where available and allocate costs accordingly.
- **Cross-Use Conflict Resolution**: Manage conflicts inherent in mixed-use properties: noise transmission between retail/residential, loading dock scheduling across uses, shared lobby and elevator traffic management, odor control from food service to office/residential, and security access tiering.
- **Shared Parking Operations**: Time-of-day parking allocation (office daytime, residential evening, retail peak hours), shared parking ratio analysis, valet operations, parking revenue optimization, and EV charging station management.
- **Consolidated Reporting**: Produce a single monthly report that shows both component-level detail and consolidated property performance. Each component is benchmarked against its own asset-type peer set, while the consolidated view shows total property NOI and value.

## Key Metrics (Mixed-Use-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| Allocation accuracy | <2% variance | Between metered/actual and allocated amounts |
| Cross-use complaints | <3/month | Noise, access, parking conflicts between components |
| Shared parking utilization (peak) | 85-95% | Across all uses at peak demand period |
| Component NOI contribution | Track by component | Each component as % of total property NOI |
| Shared cost per SF | Track by component | Common area/shared system cost allocated per component |
| Consolidated operating expense ratio | Varies | Blended; should fall between component-type benchmarks |
| Master association budget variance | <5% | If master association structure exists |
| Component occupancy delta | <500bps | Difference between highest and lowest component occupancy |

## Integration Points

- **cam-reconciliation-calculator**: Multi-component CAM allocation with distinct lease structures per use
- **annual-budget-engine**: Component-level budgeting rolling up to consolidated property budget
- **stacking-plan-builder**: Visual stacking plan showing all components and shared spaces
- **property-performance-dashboard**: Consolidated and component-level performance tracking

---

TODO: Full implementation targeted for v3.0
