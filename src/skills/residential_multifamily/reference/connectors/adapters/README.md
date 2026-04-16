# Vendor-Family Adapter Stubs

Location: `src/skills/residential_multifamily/reference/connectors/adapters/`

## Purpose

This directory holds vendor-family adapter stubs. Each stub is an ergonomic
overlay on top of a canonical connector (`pms/`, `gl/`, `crm/`, `ap/`,
`market_data/`, `construction/`, `hr_payroll/`, `manual_uploads/`) that
reduces operator ramp time when a known vendor family is present. When an
operator arrives with a recognizable source system, the matching adapter stub
provides example mapping hints, a synthetic example payload, a mapping
template, a normalized-output sample, and a known-gotchas list.

Adapters make the operator-to-canonical mapping conversation shorter. They
do not replace the canonical contract.

## What these are

- Starter templates. Every file is labeled `status: stub` or
  `status: sample` or `status: template`.
- Vendor-family names are generic placeholders
  (`generic_pms_stub`, `generic_erp_stub`, `generic_crm_stub`,
  `generic_ap_stub`, `generic_market_data_stub`,
  `generic_construction_stub`, `excel_file_stub`,
  `generic_hr_payroll_stub`). Operators fork and rename to reflect the
  actual vendor family in use.
- Reference documentation, not live integrations.

## What these are NOT

- Not production connectors.
- Not live credentials, live endpoints, or live vendor API keys. Every file
  in this tree is synthetic.
- Not official vendor implementations. Vendor names referenced inside any
  markdown are orientation-only examples; file paths stay generic.
- Not a substitute for the canonical connector contract. The canonical
  schemas under `pms/`, `gl/`, `crm/`, `ap/`, `market_data/`,
  `construction/`, `hr_payroll/`, and `manual_uploads/` remain the
  source of truth for field names, entity shapes, reconciliation checks,
  and provenance.

## Source-of-truth rule

The canonical normalized model is the contract.

- If an adapter mapping hint disagrees with the canonical schema, the
  canonical schema wins.
- If an adapter sample carries a field name not declared in the canonical
  contract, that field is dropped during normalization unless promoted via
  a schema amendment that goes through the regular canonical review.
- Adapter authors never edit files outside their own adapter directory.

## Adapter lifecycle

Every adapter moves through four stages. Details in `adapter_lifecycle.md`.

- `stub`. Example mappings only. Synthetic payloads. No operator validation.
  All adapters in this directory are shipped at this stage.
- `starter`. Real (sanitized) sample payloads. Mapping template validated
  against real column headers. Tests pass. No live credentials yet.
- `production`. Live credential method registered in `source_registry.yaml`.
  Rollout wave complete. Operator validated. Audience sign-off captured
  (finance_reporting for financial domains, compliance_risk for regulated
  or PII-heavy domains).
- `deprecated`. Replacement adapter named. Dual-run window documented.
  Cutoff date set. Old adapter retained for provenance lookup only.

## Directory layout

```
adapters/
  README.md                                    <- this file
  adapter_manifest.schema.yaml                 <- JSON Schema for manifests
  adapter_lifecycle.md                         <- stage gates
  example_adapter_authoring_guide.md           <- fork-and-fill workflow
  gotchas_and_antipatterns.md                  <- cross-cutting warnings
  vendor_family_registry.yaml                  <- directory of all stubs
  pms_vendor_family_stub/
  gl_vendor_family_stub/
  crm_vendor_family_stub/
  ap_vendor_family_stub/
  market_data_provider_stub/
  construction_platform_stub/
  manual_excel_ingestion_stub/
  hr_payroll_vendor_family_stub/
```

Each per-vendor-family directory follows the same shape:

```
<adapter_slug>/
  manifest.yaml                       <- conforms to adapter_manifest.schema.yaml
  README.md                           <- vendor-family scope and gotchas
  example_raw_payload.jsonl           <- synthetic example, status: sample
  mapping_template.yaml               <- overlay on top of canonical mapping.yaml
  normalized_output_example.jsonl     <- post-mapping, status: sample
  tests/
    __init__.py
    test_adapter.py                   <- schema conformance
```

## Authoring flow

See `example_adapter_authoring_guide.md`. The short version:

1. Fork the closest stub directory under a new slug.
2. Populate `example_raw_payload.jsonl` with real, sanitized payload.
3. Refine `mapping_template.yaml` against real source column headers.
4. Run the adapter's tests locally.
5. Advance `manifest.yaml` `status` from `stub` to `starter`.
6. Register the adapter in `vendor_family_registry.yaml` and register the
   corresponding source system in `../source_registry/source_registry.yaml`.

## Cross-cutting warnings

See `gotchas_and_antipatterns.md`. Headline rules:

- Never silently overwrite a canonical field via an adapter hint.
- Never hardcode credentials in any file under this tree.
- Never bury vendor-specific parsing in shared normalization code.
- Never drop provenance fields during mapping.
- Never let adapter slugs leak into canonical output payloads.

## Quality bar

- Every adapter manifest carries `status: stub` in this pass.
- Every example file carries `status: sample` or `status: template`.
- snake_case throughout. No real vendor credentials. No real property
  names. No PII.
- Every adapter has a `tests/` directory with at least a manifest
  conformance check.
