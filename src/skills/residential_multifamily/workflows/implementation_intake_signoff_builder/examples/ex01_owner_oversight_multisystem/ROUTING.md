# Routing

## Axis Resolution

| Axis | Resolved to | Why |
|---|---|---|
| `asset_class` | `residential_multifamily` | Owner-oversight multifamily portfolio |
| `segment` | `middle_market` | Default segment for the example packet |
| `form_factor` | `urban_mid_rise` | Example portfolio tilt |
| `lifecycle_stage` | `stabilized` | Existing operating assets with active reporting and legacy carryover |
| `management_mode` | `owner_oversight` | One region remains file-only through a third-party manager |
| `role` | `reporting_finance_ops_lead` | Intake and packet assembly lead |
| `workflow` | `implementation_intake_signoff_builder` | Explicit implementation intake and sponsor sign-off request |
| `output_type` | `memo` | Leadership packet is the target artifact |

## Packs Loaded

- `workflows/implementation_intake_signoff_builder/`
- `overlays/management_mode/owner_oversight/`
- `reference/connectors/_core/third_party_manager_oversight.md`
- `reference/connectors/source_registry/source_registry.yaml`
- `tailoring/MISSING_DOC_MATRIX.md`

## Mode Sequence

1. `executive_overview`
2. `source_by_source_implementation_discovery`
3. `field_level_export_and_file_inventory`
4. `crosswalk_and_identity_mapping`
5. `reporting_calendar_and_sla`
6. `approval_and_controls`
7. `missing_doc_chase`
8. `signoff_packaging`
