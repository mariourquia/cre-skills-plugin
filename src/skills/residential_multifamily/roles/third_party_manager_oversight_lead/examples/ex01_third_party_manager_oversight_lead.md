# Example — Monthly TPM Scorecard (abridged)

**Prompt:** "Build this month's TPM scorecard for all 3 TPMs and all 12 TPM-managed properties. Flag any property or TPM breaching the PMA-specified threshold."

**Inputs:** TPM-submitted monthly reports (per property); PMA master + SLA catalog + required-KPI list per TPM; scorecard weights reference; audit findings log.

**Output shape:** see `templates/monthly_tpm_scorecard__middle_market.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- management_mode: third_party_managed + owner_oversight
- role: third_party_manager_oversight_lead
- output_type: scorecard
- decision_severity: recommendation

## Expected packs loaded

- `roles/third_party_manager_oversight_lead/`
- `workflows/tpm_scorecard_review/`
- `workflows/tpm_audit_sampling/` (if audit slice due)
- `overlays/management_mode/third_party_managed/`
- `overlays/management_mode/owner_oversight/`
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/pma_clause_library__middle_market.csv`
- `reference/normalized/tpm_scorecard_weights__middle_market.csv`
- `reference/normalized/required_kpi_list_by_pma.csv`
- `reference/normalized/service_level_catalog__middle_market.csv`
- `reference/normalized/audit_sampling_protocol__middle_market.csv`
- `reference/derived/role_kpi_targets.csv`

## Gates potentially triggered

- Any composite below PMA-specified threshold generates a remedy-notice draft (legal-reviewed; row 19 framework).
- Any material fair-housing concern at a TPM-managed property routes row 3 via legal.
- Any PMA amendment or termination consideration routes row 19 via asset_manager / legal /
  (for termination) portfolio_manager + ceo_executive_leader.

## Confidence banner pattern

```
References: pma_clause_library@{as_of_date} (per TPM); scorecard_weights@{as_of_date};
required_kpi_list@{as_of_date}; audit_sampling_protocol@{as_of_date} (statuses per record).
TPM inputs: monthly owner packages for the period just closed (status per TPM report).
```
