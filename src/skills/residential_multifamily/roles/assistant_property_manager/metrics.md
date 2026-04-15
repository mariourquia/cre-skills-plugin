# Metrics used by assistant_property_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `delinquency_rate_30plus` | First-touch triage owner; the signal the APM watches weekly. | Weekly |
| `collections_rate` | Daily posting discipline drives this directly. | Weekly, monthly |
| `bad_debt_rate` | Write-off recommendations originate from APM ledger review. | Monthly, T12 |
| `application_conversion` | APM owns the screening pipeline mechanics. | Weekly |
| `approval_rate` | Screening discipline; fair-housing watchpoint the APM enforces on data entry. | Weekly |
| `move_in_conversion` | APM administers move-in mechanics; conversion losses often trace here. | Weekly |
| `lead_response_time` | Data-pull owner for PM's funnel review. | Daily (SLA tracking) |
| `tour_conversion` | Data-pull owner for PM. | Weekly |
| `renewal_offer_rate` | Gap-check owner; an APM-identified gap becomes the PM's action. | Weekly |
| `open_work_orders` | Administrative completeness (category, vendor, invoice pending) — not triage. | Weekly |
