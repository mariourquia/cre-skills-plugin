# Hospitality Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `room_count` | int | total guest rooms |
| `room_mix` | object | breakdown by type (standard, deluxe, suite, penthouse) with count and rack rate |
| `franchise_brand` | string | hotel brand/flag (Marriott, Hilton, IHG, independent, etc.) |
| `franchise_agreement_expiry` | date | franchise/management agreement expiration |
| `f_and_b_outlets` | int | number of food and beverage outlets (restaurant, bar, banquet, room service) |
| `meeting_space_sf` | int | total meeting/conference/banquet square footage |
| `franchise_pip` | object | property improvement plan requirements with deadline and estimated cost |
| `star_rating` | float | current star rating (AAA, Forbes, or self-assessed) |

## Workflow Outline (Full Module Scope)

- **Daily Operations Cadence**: Manage the hotel daily operating rhythm: morning standup, room availability and rate management, housekeeping deployment, engineering dispatch, guest complaint resolution, night audit, and daily revenue flash report.
- **Housekeeping Management**: Staffing models (rooms per housekeeper per shift), room inspection protocols (random audit percentage), linen par levels, guest supply inventory, deep cleaning rotation schedules, and laundry operations (in-house vs. outsourced).
- **Food & Beverage Operations**: Menu engineering, food cost control (target 28-32% food cost), beverage cost control (target 18-22%), kitchen equipment maintenance, health department inspection readiness, banquet event order (BEO) management, and room service logistics.
- **Brand/Franchise Compliance**: Track Property Improvement Plan (PIP) requirements and deadlines, brand standard audits (mystery shopper scores), quality assurance self-inspections, brand-mandated technology and systems upgrades, and franchise fee reconciliation.
- **Revenue Management**: Daily rate optimization (ADR), occupancy forecasting, RevPAR tracking, channel management (OTA vs. direct vs. group vs. wholesale), guest segmentation, and loyalty program administration.

## Key Metrics (Hospitality-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| RevPAR (Revenue Per Available Room) | Market dependent | Primary revenue KPI; benchmark vs. comp set |
| ADR (Average Daily Rate) | Market dependent | Track vs. prior year and comp set |
| Occupancy rate | 65-80% | Varies by market, day of week, season |
| GOP margin (Gross Operating Profit) | 35-45% | Higher for limited-service; lower for full-service |
| Food cost percentage | 28-32% | Of F&B revenue |
| Rooms per housekeeper per shift | 14-17 | Full-service; 18-22 for limited-service |
| Guest satisfaction score | >4.2/5.0 | Brand survey or OTA review aggregate |
| TripAdvisor/Google rating | >4.0/5.0 | Monitor weekly; respond to all negative reviews |

## Integration Points

- **building-systems-maintenance-manager**: Hotel MEP systems, kitchen equipment, laundry equipment lifecycle
- **vendor-invoice-validator**: F&B vendor invoices, linen service, OTA commission reconciliation
- **annual-budget-engine**: Hotel operating budget with departmental P&L (rooms, F&B, other operated depts)
- **compliance-regulatory-response-kit**: Health department, fire safety, liquor license, ADA compliance

---

TODO: Full implementation targeted for v3.0
