# Middle-Market Concession Policy

Concession posture for middle-market properties. The governing principle is:
concessions close documented gaps vs. market, they do not substitute for durable
pricing discipline. Concessions are a tool, not a habit.

## When concessions are used

- To close a measurable gap between asking rent and market rent. The gap is
  documented via `market_to_lease_gap` and the comp set used.
- To break a stubborn vacancy on a unit with a documented condition or layout
  disadvantage.
- To match a competitor's posted concession where doing nothing would cost velocity
  and pricing integrity.

Concessions are not used as a blanket discount across all new leases. Blanket
discounting signals a pricing problem that must be solved upstream.

## Caps and escalation

Two caps govern the segment:

- Maximum free months on a standard new lease of the default term length. Cap token
  `middle_market_concession_free_months_max` is defined in
  `reference/derived/role_kpi_targets.csv#row_mm_concession_free_months_max`.
- Maximum marketing gift card or move-in credit per lease. Cap token
  `middle_market_concession_gift_card_max` is defined in
  `reference/derived/role_kpi_targets.csv#row_mm_concession_gift_card_max`.

Concessions above either cap require approval under
`_core/approval_matrix.md#row_13_concession_over_policy`. The approval package must
include the documented market gap, the comp set, and a near-term pricing recovery
plan.

## Renewal concessions

Renewal concessions are tracked separately from new-lease concessions (see
`_core/metrics.md#concession_rate` filters override). Renewal concessions are
exceptional, used only for specific retention cases documented per
`renewal_strategy.md`.

## Fair-housing discipline

Concessions are applied policy-first, not relationship-first. Uneven application of
concessions creates fair-housing exposure (see `_core/guardrails.md#fair_housing`).
The system scans for concession-pattern disparities and routes outliers to human
review; flagging is informational, not determinative.
