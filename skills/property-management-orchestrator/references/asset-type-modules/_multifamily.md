# Multifamily Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `total_units` | int | total residential unit count |
| `unit_mix` | object | breakdown by bedroom count (studio, 1BR, 2BR, 3BR+) with count and avg rent |
| `affordable_units` | int | number of income-restricted units (LIHTC, Section 8, inclusionary) |
| `affordable_program` | enum | LIHTC, Section_8, inclusionary, market_rate_only |
| `amenity_package` | list | fitness center, pool, clubhouse, dog park, coworking, package lockers, etc. |
| `parking_type` | enum | surface, structured, underground, none |
| `parking_ratio` | float | spaces per unit |
| `laundry_model` | enum | in_unit, common_area, hybrid |

## Workflow Outline (Full Module Scope)

- **Unit-Level Operations**: Track individual unit condition, turnover history, rent roll accuracy, and maintenance cost per unit. Generate unit-level P&L for value-add renovation targeting.
- **Resident Services & Retention**: Design resident event calendars, manage amenity programming, track resident satisfaction by building/floor, and generate retention offers calibrated to renewal probability and replacement cost.
- **Turnover Acceleration**: Manage the full turn pipeline from notice to move-in ready. Track turn time, turn cost, and make-ready quality by unit type. Flag units exceeding target turn time.
- **Amenity Management**: Track amenity utilization rates, maintenance costs, and contribution to rent premiums. Recommend amenity investments with ROI analysis.
- **Affordable Compliance**: Track income certifications, rent limits, utility allowances, and annual compliance reporting for LIHTC/Section 8 units.

## Key Metrics (Multifamily-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| Turnover rate (annual) | 40-55% | Varies by market; lower is better |
| Average turn time (days) | 3-7 standard, 14-21 value-add | From move-out to move-in ready |
| Cost per turn | $2,200-$3,500 | Standard turn; excludes value-add renovation |
| Concession rate | 2-4% of gross rent | Market dependent; lower in tight markets |
| Amenity utilization | >40% of residents | Measured monthly for major amenities |
| Resident event attendance | >15% per event | Higher for community-building events |
| Online review score | >4.0 / 5.0 | Google, Apartments.com, ApartmentRatings |
| Renewal conversion rate | >55% | Of eligible leases offered renewal |

## Integration Points

- **tenant-retention-engine**: Renewal probability scoring and NPV-based retention offers
- **rent-optimization-planner**: Unit-level mark-to-market and effective rent NPV
- **lease-up-war-room**: Pre-stabilization lease-up operations and absorption tracking
- **annual-budget-engine**: Unit-level revenue budgeting and expense allocation

---

TODO: Full implementation targeted for v3.0
