# Routing Example 02 — Asset manager asks for monthly review on a TPM-managed urban mid-rise

**Inbound request:**

> "Pull me the monthly AM review for Liberty Apartments. We're behind on budget — I want to see what happened and what the TPM is doing about it."

## Axis resolution

| Axis | Resolved to |
|---|---|
| `asset_class` | `residential_multifamily` |
| `segment` | `middle_market` (from property master) |
| `form_factor` | `urban_mid_rise` |
| `lifecycle_stage` | `stabilized` |
| `management_mode` | `third_party_managed` (+ `owner_oversight` loaded because asker is owner-side) |
| `role` | `asset_manager` |
| `workflow` | `monthly_asset_management_review` |
| `market` | `Nashville` |
| `output_type` | `operating_review` |
| `decision_severity` | `recommendation` |

## Packs loaded

- `roles/asset_manager/`.
- `roles/third_party_manager_oversight_lead/` — loaded as secondary because `owner_oversight` mode is active.
- `workflows/monthly_asset_management_review/`.
- `workflows/third_party_manager_scorecard_review/` — invoked within the AM review for the TPM's scorecard.
- `overlays/segments/middle_market/`.
- `overlays/form_factor/urban_mid_rise/`.
- `overlays/lifecycle/stabilized/`.
- `overlays/management_mode/third_party_managed/` and `.../owner_oversight/`.

## References loaded

- Property master + budget + T-12 references.
- `reference/normalized/market_rents__nashville_mf.csv`.
- `reference/normalized/concession_benchmarks__nashville_mf.csv`.
- `reference/normalized/collections_benchmarks__southeast_mf.csv`.
- `reference/normalized/tpm_scorecard_weights.csv`.

## Gates

- Any `final` submission to LPs / lenders would require approval. This review is internal; no gate triggered unless the AM asks for a `final` external version.
- Any recommended vendor change or contract amendment triggers approval matrix row 19.

## Output shape

- Variance narrative by P&L line, with TPM-provided explanations captured and an owner-side assessment of completeness (metric: `variance_explanation_completeness`).
- TPM scorecard snapshot (timeliness, KPI completeness, budget adherence, staffing vacancy, SLA adherence).
- Portfolio-level flags (is this property moving onto the watchlist?).
- Action list for the AM's next TPM meeting.
