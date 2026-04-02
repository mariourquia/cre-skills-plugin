# Retail Deep-Dive Module

**Status**: v3.0 Deep-Dive Module -- Currently a stub framework

## Asset-Type-Specific Input Fields

| Field | Type | Notes |
|---|---|---|
| `retail_format` | enum | strip_center, community_center, power_center, lifestyle, mall, mixed_use_ground_floor |
| `anchor_tenants` | list | anchor tenant names, SF, and lease expiration dates |
| `inline_tenant_count` | int | number of non-anchor inline tenants |
| `percentage_rent_tenants` | int | number of tenants with percentage rent clauses |
| `co_tenancy_clauses` | int | number of leases with co-tenancy provisions |
| `common_area_sf` | int | total common area including parking lot and landscaping |
| `food_court` | boolean | food court or food hall present |
| `outparcel_count` | int | number of outparcels (owned or ground-leased) |

## Workflow Outline (Full Module Scope)

- **Percentage Rent Administration**: Track tenant sales reporting deadlines, audit submitted sales figures, calculate percentage rent triggers, reconcile breakpoints, and generate percentage rent invoices.
- **Co-Tenancy Monitoring**: Track co-tenancy trigger conditions (anchor occupancy, overall occupancy thresholds), model financial impact of co-tenancy rent reductions, and proactively manage anchor replacement timelines.
- **Common Area Programming & Marketing**: Seasonal event programming, holiday decorations, farmers markets, pop-up shop coordination, marketing fund administration, and social media/foot traffic analytics.
- **Tenant Sales Reporting & Analysis**: Aggregate tenant sales data, calculate sales per SF by category, benchmark against ICSC/regional averages, identify underperformers, and produce quarterly sales trend reports.
- **Parking & Access Management**: Parking lot maintenance, striping, lighting, signage, shared parking allocation, employee parking enforcement, and ADA parking compliance.

## Key Metrics (Retail-Specific)

| Metric | Target Range | Notes |
|---|---|---|
| Tenant sales PSF | $250-$450+ | Varies significantly by format and trade area |
| Percentage rent collections | Track annual | As % of total rent; highly variable |
| CAM per SF | $5.50-$8.50 | Varies by center type and services included |
| Parking lot maintenance per space | $150-$300/yr | Includes sweeping, striping, repair, lighting |
| Tenant retention rate | 65-75% | Higher for anchor tenants |
| Foot traffic trend | Positive YoY | Measured via mobile analytics or counters |
| Co-tenancy exposure ($) | Quantify annually | Total rent at risk if triggers activated |
| Seasonal sales lift | >15% | Q4 vs. annual average for most retail formats |

## Integration Points

- **cam-reconciliation-calculator**: Retail-specific CAM calculations with merchant association fees
- **lease-abstract-extractor**: Percentage rent clause extraction and breakpoint calculation
- **tenant-retention-engine**: Retail tenant renewal strategy with sales-based retention analysis
- **lease-negotiation-analyzer**: Co-tenancy renegotiation and exclusive use enforcement

---

TODO: Full implementation targeted for v3.0
