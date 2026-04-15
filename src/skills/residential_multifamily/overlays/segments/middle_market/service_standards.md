# Middle-Market Service Standards

Service-standard posture for middle-market properties. The anchoring promise is:
reliable, respectful, and timely. Residents expect to be heard quickly, for routine
requests to be handled quickly, and for urgent requests to be handled immediately.

## Response-time cadence

Four response-time surfaces are tracked:

- Lead response (inbound applicant contacts the property). Same-business-day human
  reply is the default; median target band lives in
  `reference/derived/role_kpi_targets.csv#row_mm_lead_response_time`.
- Resident inquiry (existing resident contacts the office, non-emergency). Same-day
  acknowledgement; resolution target depends on topic.
- Work order acknowledgement (auto-acknowledgement plus triage). Triage target by
  priority tier lives in the priority-tier reference rows.
- Escalated complaint (resident escalation to regional). Acknowledgement target is
  next-business-day; resolution path documented case-by-case.

Actual numeric targets live in the reference layer. Reference rows are cited by slug
in the overlay.yaml.

## Work-order priority tiers

Work orders are classified P1 through P4. The SLAs for each priority tier are stored
in `reference/derived/role_kpi_targets.csv` under rows prefixed with
`row_mm_work_order_sla_`. The posture is:

- P1 (life-safety, security, active leak, loss of habitability): immediate dispatch,
  acknowledgement within minutes, resolution or stabilization same day. See
  guardrails for life-safety escalation.
- P2 (significant comfort or function loss, e.g., no A/C in heat, no heat in cold,
  appliance down): next-day resolution target.
- P3 (routine repair): within-week resolution target.
- P4 (minor cosmetic, routine cleaning, nice-to-have): within-two-week resolution
  target.

Aging past tier SLA is a reportable event; repeat work orders on the same unit within
a defined window trigger a root-cause review per `repeat_work_order_rate`.

## Amenity and common-area cadence

Amenity cleanliness and common-area maintenance cadence are stricter than the
all-segment default. The cadence per amenity (pool, fitness, package room, corridors,
mail area, elevators where present, laundry rooms, trash rooms, leasing office,
business center) lives in `reference/derived/role_kpi_targets.csv` under
`row_mm_amenity_cadence_*`. The overlay points at those rows rather than listing
frequencies in prose.

## Escalation posture

The PM owns first-response. Regional is copied on escalations after the documented
attempt window; owner-side is copied on escalations with potential material impact
per the approval matrix's fair-housing-risk and life-safety categories.
