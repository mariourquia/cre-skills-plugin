# Lease-Up Lifecycle Overlay

The lease-up overlay covers the period from TCO through stabilized occupancy.
Lease-up posture differs from stabilized posture in five places:

1. Preleased window widens to 60 days.
2. Stabilization-pace-vs-plan and lease-up-pace-post-delivery become primary KPIs.
3. Concession flexibility exists within a defined floor.
4. Marketing intensity is higher; funnel targets are tighter.
5. Leasing staffing is heavier; a reversion trigger returns ratios to segment /
   form-factor defaults at stabilization.

<a id="war_room_cadence"></a>

## Lease-up war-room cadence

- Weekly lease-up war room: PM, regional, marketing lead, owner AM (and TPM oversight
  lead in TPM mode). Agenda is fixed: traffic by source, tour completion, application
  volume, approvals, executed leases, move-ins, notice exposure, concession mix,
  pricing adjustments.
- Daily standup at the site during peak lease-up weeks. Fifteen minutes, focused on
  today's tours and today's pipeline blockers.
- Monthly owner-side review with the full lease-up scorecard.

<a id="marketing_intensity"></a>

## Marketing intensity

- Paid source mix, organic source mix, referral activation, broker/locator
  engagement, and community partnership cadence are tracked throughout lease-up.
- The marketing plan is living: any source underperforming its funnel benchmark for
  two weeks is reviewed and either adjusted or replaced.
- Pricing moves are tied to absorption; absorption below the lease-up-pace band
  triggers a pricing review before triggering a concession review.

## Stabilization trigger

Stabilization is declared when leased occupancy has held above the stabilization
threshold for the required duration (threshold and duration live in
`reference/derived/role_kpi_targets.csv#row_lifecycle_lease_up_stabilization_threshold`).
At that point, the lease-up overlay is replaced by the stabilized overlay in the
merge order, staffing ratios revert, and reporting emphasis returns to the
segment's primary surfaces.
