# Market Data Reconciliation Rules

Narrative describing how reconciliation in the market_data domain works.

## Reconciliation scope

The market_data connector lands vendor and internal-survey comps, concession observations, occupancy benchmarks, and cost references (payroll, labor, materials, utilities). Unlike PMS, GL, AP, and construction (which are operational), market_data reconciles primarily across sources and against internal observations.

## Totals that must agree

### Cross-source rent agreement

For each (comp_property_id, unit_type_label, as_of_date_bucket), two or more sources reporting the same comp must agree within the conflict_tolerance_percent declared in `market_data/manifest.yaml`. Exceeding the tolerance requires a conflict_adjudication_note.

### Submarket population coverage

For each (market, submarket) where owned_property_count > 0, the comp population is at least the `minimum_comp_count` declared in `market_data/manifest.yaml`. Below-minimum coverage warns; the comp-snapshot skill widens its scope or refuses.

### Concession comparability

Every concession observation decodes to a weeks-equivalent via the canonical formula in `mapping.yaml`. Concession observations whose decoded weeks-equivalent diverges from the raw magnitude by more than a declared rounding tolerance warn for manual review.

### Benchmark provenance tier

Every derived benchmark row carries an `approval_status` (proposed, endorsed, deprecated). Proposed benchmarks are not consumed by IC-memo or LP-facing skills. The review that promotes `proposed` to `endorsed` is tracked in `_core/approval_matrix.md`.

## Tolerances

| Reconciliation | Absolute tolerance | Relative tolerance |
|---|---|---|
| Cross-source rent agreement | 0 | referenced from market_data/manifest.yaml conflict_tolerance_percent |
| Submarket population coverage | referenced from market_data/manifest.yaml minimum_comp_count | 0 |
| Concession comparability | referenced from mapping.yaml rounding tolerance | 0 |
| Benchmark approval status | n/a | n/a |

All non-zero tolerance values live in referenced configuration.

## Escalation triggers

- Population-coverage failure escalates to the asset_mgmt audience because comp-snapshot cannot run without adequate coverage.
- Cross-source conflict exceeding tolerance escalates to the asset_mgmt and leasing_strategy audiences.
- Benchmark approval expiry (endorsement more than the endorsement_max_age_days declared in org overlay) escalates to the asset_mgmt audience.

## Cross-domain reconciliation dependencies

Market data is an enrichment layer; it does not block monthly close. Blockers in market_data cause downstream comp-based skills (comp-snapshot, submarket-truth-serum, rent-optimization-planner) to refuse for affected markets. Operational reports continue.
