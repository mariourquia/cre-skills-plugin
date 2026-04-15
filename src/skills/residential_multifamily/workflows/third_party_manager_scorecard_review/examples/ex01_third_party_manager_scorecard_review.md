# Example — Third-Party Manager Scorecard Review (abridged)

**Prompt:** "Run the monthly TPM scorecard for our Charlotte portfolio."

**Inputs:** TPM-submitted owner reports + property monthly operating reviews + asset management reviews + PMA terms overlay + rubric overlay + audit log + approval-request ledger + market benchmarks.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- management_mode: third_party_managed + owner_oversight
- market: Charlotte
- pma_id: pma_charlotte_mf
- role: asset_manager / third_party_manager_oversight_lead
- output_type: scorecard
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/third_party_manager_scorecard_review/`
- `workflows/monthly_property_operating_review/` (per asset)
- `workflows/monthly_asset_management_review/` (per asset)
- `overlays/segments/middle_market/`
- `overlays/management_mode/owner_oversight/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/collections_benchmarks__southeast_mf.csv`
- `reference/normalized/turn_benchmarks__charlotte.csv`
- `reference/normalized/tpm_scorecard_rubric__{org}.yaml`
- `reference/normalized/pma_terms__pma_charlotte_mf.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Material performance-gap action (overlay-defined).
- Row 19 PMA amendment or termination.
- Row 3 fair-housing or compliance exposure.

## Expected output shape

- TPM scorecard with 10-dimension composite, per-asset rows, tier (yellow / orange / red).
- Material gap memo.
- Audit follow-up list.
- TPM-facing communication draft (`draft_for_review`).
- Remediation action plan.

## Confidence banner pattern

```
References: tpm_scorecard_rubric__{org}@2026-03-31 (starter),
pma_terms__pma_charlotte_mf@2026-03-31 (sample, PMA overlay pending PMA redline),
turn_benchmarks__charlotte@2026-03-31 (starter),
collections_benchmarks__southeast_mf@2026-02-28 (starter).
```
