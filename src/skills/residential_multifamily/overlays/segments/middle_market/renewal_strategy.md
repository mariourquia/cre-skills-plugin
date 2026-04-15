# Middle-Market Renewal Strategy

Renewals are the lowest-cost source of revenue growth and the highest-leverage tool
for stabilizing turnover. The middle-market renewal strategy is: differentiate offers
by the in-place-to-market gap, make offers early enough to allow a dialogue, and
protect the resident relationship with plain-language communication.

## Core principle

Renewal offers are not flat percentages applied across the book. Each renewal offer
is framed by:

- The in-place-to-market gap for the unit (see `market_to_lease_gap` and
  `loss_to_lease`).
- The unit's recent service history (work orders, repeat issues).
- The resident's payment history and tenure.
- Local market velocity and competitor concessions.

The specific bracket-by-bracket offer logic lives in
`reference/derived/role_kpi_targets.csv` under rows prefixed with
`row_mm_renewal_offer_`. The overlay references those rows rather than embedding
numbers.

## Offer timing

Renewal offers are generated well in advance of lease expiry to allow negotiation
and to collect the resident's stated intent before the notice-to-vacate window opens.
The target `renewal_offer_rate` band lives in
`reference/derived/role_kpi_targets.csv#row_mm_renewal_offer_rate`; shortfalls
against the band trigger a pipeline review.

## Retention pathways

When a resident signals they may leave, the retention pathway is documented:

1. Understand the driver (price, service, life-event, competitor offer).
2. If price-driven and the in-place-to-market gap supports it, offer a narrower
   increase within the approved band. Concessions as retention tools are exceptional
   and governed by `concession_policy.md`.
3. If service-driven, escalate the service issue into the work-order system with a
   root-cause tag and close the loop with the resident.
4. If life-event-driven, offer transfer-in-place options where the portfolio and
   site inventory support it.

## Reporting surfaces

Renewal performance rolls up through `renewal_offer_rate`,
`renewal_acceptance_rate`, `rent_growth_renewal`, and blended trade-out. Ownership
reporting emphasizes the rent-growth-renewal vs. in-place-to-market gap relationship;
see `reporting_emphasis.md`.

## Fair-housing discipline

Renewal offers are policy-driven. Systematic disparities in offer bands by resident
attribute proxies are a fair-housing risk; scans are part of the guardrails stack
and outliers route to human review.
