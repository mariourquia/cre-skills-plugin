# Example — Work Order Triage (abridged)

**Prompt:** "Triage the daily work-order queue for Ashford Park."

**Inputs:** WorkOrder table + `reference/normalized/work_order_priority_playbook__middle_market.csv` + `reference/normalized/approved_vendor_list__charlotte.csv` + vendor rate cards.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: maintenance_supervisor
- market: Charlotte
- jurisdiction: Charlotte
- output_type: checklist
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/work_order_triage/`
- `workflows/vendor_dispatch_sla_review/` (invoked on repeat flags)
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/work_order_priority_playbook__middle_market.csv`
- `reference/normalized/approved_vendor_list__charlotte.csv`
- `reference/normalized/vendor_rate_cards__charlotte.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Disbursement above threshold: row 6 or 7.
- Vendor contract signature: row 19.
- Safety-critical scope deferral: row 4.

## Expected output shape

- Priority-assigned queue (P1–P4 counts).
- Dispatch records per WO with vendor/tech, ETA, cost estimate.
- Approval requests where above threshold.
- Entry-notice drafts for jurisdictions that require statutory notice.
- Repeat-WO flags routed to vendor scorecard workflow.

## Confidence banner pattern

```
References: work_order_priority_playbook__middle_market@2026-03-31 (starter),
approved_vendor_list__charlotte@2026-04-01 (starter),
vendor_rate_cards__charlotte@2026-04-01 (sample).
Vendor license/insurance freshness: per-vendor, surfaced at dispatch.
```
