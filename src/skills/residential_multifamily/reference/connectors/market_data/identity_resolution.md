# Market Data Identity Resolution

How comps, submarkets, and benchmarks in the market_data connector crosswalk to canonical identifiers.

## Crosswalk pointers

- `reference/connectors/master_data/market_gazetteer.yaml`: canonical market and submarket registry.
- `reference/connectors/master_data/comp_property_crosswalk.yaml`: comp property identity across vendor feeds.
- `reference/connectors/master_data/unit_type_harmonization.yaml`: unit type taxonomy across vendor formats.
- `reference/connectors/source_registry/`: provenance tier registry (strong / medium / weak) per vendor feed.

## Match methods

| Method | Use | Confidence |
|---|---|---|
| `exact` | Source-native comp_property_id when the vendor carries a stable id. | Highest when registered in comp_property_crosswalk. |
| `composite` | (address_normalized, market, submarket) to match the same comp across two vendors. | High. |
| `fuzzy` | Normalized property name + zip match where address normalization fails. | Medium. Queued for review. |
| `manual` | Operator-adjudicated mapping in comp_property_crosswalk. | Authoritative. |

## Confidence scoring

Every market_data record carries `provenance_tier` resolved from `source_registry/`. Downstream skills (comp-snapshot, submarket-truth-serum) down-weight `medium` and `weak` observations. Records with `weak_provenance_flag = true` are retained but flagged in downstream outputs.

## Hard cases

### Conflicting sources

Two vendors may publish asking rents for the same comp_property with different numbers (one polls the property website, the other uses broker-reported data). The conflict_tolerance_percent declared in `market_data/manifest.yaml` bounds the permissible delta; outside the band, both observations retain but carry a `conflict_adjudication_note`. Failure mode: without conflict flagging, the higher source silently dominates and skews the comp median. Mitigation: `md_conflicting_sources_flagged`.

### Stale comps

Rent comps must reflect recent asking rents. Stale observations (older than the rent_comp_coverage_window_days declared in the manifest) are allowed in the historical record but excluded from the current benchmark. Failure mode: using a stale comp as if it were current produces a misleading market signal. Mitigation: `md_freshness_sla` plus the benchmark derivation filters by as_of_date window.

### Outlier rents

An asking rent far outside the plausible band for a (market, submarket, unit_type_label) triad is either a data-entry error or a legitimate price leader. The plausible band is declared in `overlays/segments/<segment>/overlay.yaml`, NOT hardcoded. Failure mode: an outlier silently inflates the benchmark. Mitigation: `md_outlier_rent_detection` quarantines and requires review.

### Missing submarket tags

Observations without a submarket tag either collapse to the market median (distorting submarket-level analysis) or require a `submarket_unknown` flag with a reason. Failure mode: silent collapse. Mitigation: `md_submarket_tag_required`.

### Inconsistent unit mix comparability

Vendor A reports a one-bedroom as `1BR_700-800sf`; vendor B reports `1Bdrm_Standard`. The unit_type_harmonization crosswalk maps vendor labels to canonical unit_type_labels. Failure mode: two observations for the same floor plan appear as different unit types, fragmenting the comp set. Mitigation: mapping required before landing; unmapped labels are rejected per the enum_conformance template.

### Duplicate benchmark loads

Two landings of the same vendor feed for the same as_of_date produce duplicate rows. The dedup_rule in `mapping.yaml` collapses exact duplicates; near-duplicates with different source_row_ids but identical values are flagged. Failure mode: doubled comp count distorts population-coverage checks. Mitigation: `market_data_duplicate_primary_key` plus the dedup tie-breaker.

### Vendor benchmarks with weak provenance

Some vendor feeds are surveys rather than transaction data; others aggregate broker input with unclear methodology. The source_registry tiers each feed (strong / medium / weak). Failure mode: weak-provenance observations treated as authoritative overstate precision. Mitigation: `md_weak_provenance_warning` flags; downstream skills down-weight per the tier.

## Failure modes summary

| Failure | Symptom | Check |
|---|---|---|
| Conflicting sources not flagged | Higher source dominates benchmark | `md_conflicting_sources_flagged` |
| Stale comp treated as current | Misleading market signal | `md_freshness_sla` |
| Outlier not quarantined | Benchmark inflated | `md_outlier_rent_detection` |
| Missing submarket tag | Submarket analysis distorted | `md_submarket_tag_required` |
| Unit mix labels not harmonized | Fragmented comp set | enum_conformance on unit_type_label |
| Duplicate benchmark load | Double-counted comps | `market_data_duplicate_primary_key` |
| Weak-provenance feed not flagged | Overstated precision | `md_weak_provenance_warning` |
