# Update Flow Walk-Through — `vendor_rate`

Scenario: Piedmont Pest Pros renegotiates the monthly pest-control bundle for 2026-Q3, raising per-unit price from $4.25 to $4.65.

## 1. Inbound → `reference/raw/vendor_rate/2026/03/vendor_ratecard__2026-03-31.csv`

Row shape: `(market, vendor_name, service_slug, service_category, contract_term_months, price_amount, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/vendor_rate.yaml`.
- Required: `vendor_name`, `service_slug`, `unit`.
- Plausibility: magnitude checks by `service_category`.

## 3. Normalization

Write to `reference/normalized/vendor_rates__<market>_mf.csv`.

## 4. Approval

Auto-approve for vendor rate changes < 10% and total annual commitment below `threshold_contract_award`.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_15_0004
change_type: update
target_kind: reference_record
target_ref: reference/normalized/vendor_rates__charlotte_mf.csv#vr-charlotte-pestpro-monthly
old_value:
  value: 4.25
new_value:
  value: 4.65
source_name: "Vendor quarterly rate card 2026-Q1 (illustrative)"
source_type: vendor_bid
source_date: 2026-03-15
as_of_date: 2026-02-28
proposed_by: agent:vendor_rate_agent
approved_by: human:regional_manager
proposed_at: 2026-03-15T10:00:00Z
approved_at: 2026-03-15T13:30:00Z
confidence: high
reason_for_change: |
  Piedmont Pest Pros renegotiated monthly pest control bundle; per-unit rate up $0.40.
affected_skills:
  - workflows/operating_review
  - roles/property_manager
  - roles/maintenance_supervisor
```

## 6. Derived Recomputation

No direct derived recomputation; annual budget picks up on next run.

## 7. Notifications

Logged impact on operating review, property manager, maintenance supervisor.

## 8. Archival

Prior row archived to `reference/archives/vendor_rate/2026/02/`.
