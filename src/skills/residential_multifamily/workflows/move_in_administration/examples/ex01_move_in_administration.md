# Example — Move-In Administration (abridged)

**Prompt:** "Prep move-in for unit 214 at Ashford Park on 2026-05-01."

**Inputs:** executed lease + turn-ready status + `reference/normalized/move_in_documents__charlotte.yaml` + `reference/normalized/utility_setup_guides__charlotte.yaml`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: property_manager
- market: Charlotte
- jurisdiction: Charlotte
- output_type: checklist
- decision_severity: recommendation

## Expected packs loaded

- `workflows/move_in_administration/`
- `overlays/segments/middle_market/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/move_in_documents__charlotte.yaml`
- `reference/normalized/utility_setup_guides__charlotte.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Fair-housing row 3 if any welcome copy fails the term-list scan.

## Expected output shape

- Readiness checklist with blockers, owners, due dates.
- Document packet assembled per jurisdiction overlay.
- Utility transfer instruction draft.
- Welcome communication draft.
- Move-in event record scheduled.
- Post-move-in follow-up scheduled.

## Confidence banner pattern

```
References: move_in_documents__charlotte@2026-03-31 (sample),
utility_setup_guides__charlotte@2026-03-31 (starter).
Data freshness: turn workflow state live through 2026-04-28.
```
