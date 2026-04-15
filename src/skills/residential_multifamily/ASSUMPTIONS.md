# Assumptions

Where Phase 1 made choices that were not fully specified, they are logged here for later review.

## Scope

- **Phase 1 depth lives in `middle_market`.** Affordable and luxury are stubs. High-rise is stubbed within form factor. BTR, student, senior, mixed-use, and international are not included.
- **Segmentation axis values** are fixed at three (`middle_market`, `affordable`, `luxury`). Alternate segmentations (e.g., "workforce" vs. "class B" vs. "class C") can be expressed via overlay adds; they do not replace the canonical three.

## Defaults

- `lifecycle_stage` default is `stabilized`. Development, construction, lease_up, renovation, and recap_support are resolved only when user context or property master indicates.
- `preleased_window` default is 30 days. `lease_up` overlay raises to 60 days.
- `renewal_offer_lead_time` default is 90 days.
- `delinquency_threshold_dollars` default is $25 per org overlay.
- `vacancy_threshold_days` (TPM staffing metric) default is 21.
- Effective-rent definition for rent-growth metrics: `base_rent - (concessions_total / term_months)`.
- Same-store set for `same_store_noi_growth`: owned through both comparison periods, excludes `lease_up` and `recap_support`.
- Controllable opex excludes property tax, insurance, management fee, debt service, depreciation at the site level; management fee is treated as controllable at the owner level.

## Reference data

- All starter reference rows are sample values, not live data. Every row carries a `status` tag.
- Sample markets used for examples: Charlotte, Atlanta, Dallas, Phoenix, Nashville. These choices are illustrative; the subsystem is geography-neutral.
- Sample segment / form / stage combinations used for examples: middle_market / garden / stabilized as the flagship; middle_market / urban_mid_rise / stabilized with `third_party_managed`; middle_market / garden / renovation; middle_market / suburban_mid_rise / lease_up.

## Metric contracts

- Where multiple definitions of a concept exist in the industry (e.g., make-ready days, delinquency, rent growth), one canonical definition is declared. Alternate definitions require new metric slugs, not redefinition.
- `turnover_rate` excludes unit-to-unit transfers where the resident account persists (the household did not "turn over"). This is a known departure from some operators' conventions; overlays may override.
- `rent_growth_new_lease` excludes classic-to-renovated unit-type conversions (those belong to renovation ROI metrics).

## Approval matrix

- Dollar thresholds are placeholder in the default org overlay. The tailoring skill's interview flow captures real thresholds during onboarding.
- Default approvers are two-role (e.g., property_manager + regional_manager). Orgs that require three-role approvals for certain categories express that in their org overlay.

## Interaction with existing `cre-skills-plugin` skills

- This subsystem is additive. Existing flat skills (`leasing-operations-engine`, `capex-prioritizer`, `annual-budget-engine`, `building-systems-maintenance-manager`, etc.) remain in place; they may be invoked by packs in this subsystem via `metrics_used` and `reference_manifest` references when a multifamily-specific pack would duplicate existing logic.
- A future migration phase may consolidate multifamily-specific logic out of flat skills into this subsystem; that migration is out of scope for Phase 1.

## Tests

- The test suite validates structural invariants and naming rules but does not evaluate business-logic correctness at sample-data scale (there is not enough sample data to meaningfully test business logic). Tests rely on schemas and cross-reference checks.
- Tests are additive to the existing `tests/` tree and do not modify existing `test_plugin_integrity.py` or `test_calculator_correctness.py`.

## Known gaps

- Jurisdictional legal form library is not included. Legal notices carry `legal_review_required` banners and are not drafted-final by the system.
- Resident PII handling assumes the subsystem does not ingest live PII. The plugin runtime is responsible for PII boundaries; this subsystem declares de-identified-sample-only for its own reference files.
- Federal and state Fair Housing training materials are not part of this subsystem; the tailoring skill asks the operator to confirm its training program.
- Amortization treatment within DSCR is left to per-loan overlays (loans vary; there is no single canonical).
- Cost escalation assumptions for development and construction are starter only; operators are expected to set their own curves per market via org overlay.
