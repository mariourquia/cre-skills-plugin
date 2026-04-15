# Example — Weekly Delinquency Tracker Prep (abridged)

**Prompt:** "Pull this week's delinquency tracker at Ashford Park and flag cases approaching legal-notice threshold."

**Inputs:** AR aging snapshot + prior-week tracker + delinquency playbook reference + payment plan log.

**Output shape:** see `templates/weekly_delinquency_tracker.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: assistant_property_manager
- market: (asker-provided)
- output_type: kpi_review
- decision_severity: informational

## Expected packs loaded

- `roles/assistant_property_manager/`
- `workflows/delinquency_collections/` (data-prep branch)
- `workflows/rent_roll_hygiene_check/`
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/delinquency_playbook_middle_market.csv`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/role_kpi_targets.csv`

## Gates potentially triggered

- None by the APM directly. Cases at legal-notice threshold are surfaced to the property_manager,
  who opens approval_request (row 1) before any notice is served.

## Confidence banner pattern

```
References: delinquency_playbook@overlay-default (status: starter, org overlay pending);
approval_thresholds@overlay-default (status: starter, org overlay pending).
Data freshness: AR aging snapshot at run time; payment plan log live.
```
