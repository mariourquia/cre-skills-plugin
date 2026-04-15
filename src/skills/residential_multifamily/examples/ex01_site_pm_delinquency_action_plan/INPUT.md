# Example 01 — INPUT

## User prompt

> "Give me a delinquency action plan for Ashford Park. We are at 6.8% on the 30+ bucket and the regional wants a plan by Friday. Include an aging-bucket breakdown, who we escalate on, and draft comms I can send after legal review. Stay inside middle-market policy."

## Session context

- asker.role: `property_manager`
- asker.org_id: `examples_org`  (org overlay present at `overlays/org/examples_org/` for illustration)
- property lookup: `property_id = ashford_park_charlotte_01`
- property master: `property_name=Ashford Park`, `segment=middle_market`, `form_factor=garden`, `lifecycle_stage=stabilized`, `management_mode=third_party_managed`, `market=Charlotte`, `submarket=South End`, `unit_count_rentable=248`.
- Week ending: `2026-04-12`
- Prior week `delinquency_rate_30plus`: 6.4% (trend: up).
- AR snapshot as of `2026-04-12` (from rent roll export): 21 residents in 30+ bucket, $62,400 open balance above 30 days.
- Payment plans: 4 active (3 compliant, 1 in breach).
- Known constraints: operator policy disallows autonomous pay-or-quit issuance; non-standard payment plans route.

## Reference availability snapshot

- `reference/normalized/market_rents__charlotte_mf.csv` — present, status: sample, as_of 2026-03-31.
- `reference/normalized/collections_benchmarks__southeast_mf.csv` — present, status: sample, as_of 2026-03-31.
- `reference/normalized/approval_threshold_defaults.csv` — present, status: starter, as_of 2026-03-15.
- `reference/normalized/delinquency_playbook_middle_market.csv` — present, status: starter, as_of 2026-03-15.
- Org overlay approval matrix at `overlays/org/examples_org/approval_matrix.yaml` — present.

## Decision / autonomy context

- decision_severity expected: `recommendation` (plan proposal; no autonomous execution).
- Gated actions likely: any pay-or-quit notice (row 1), any eviction-track action (row 2), any non-standard payment plan (row 13).
