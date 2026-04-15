# Construction Identity Resolution

How projects, commitments, change orders, and draws in the construction connector crosswalk to canonical identifiers.

## Crosswalk pointers

- `reference/connectors/master_data/construction_project_registry.yaml`: canonical project_id registry.
- `reference/connectors/master_data/vendor_ap_construction_bridge.yaml`: vendor_id bridge to AP.
- `reference/connectors/master_data/property_crosswalk.yaml`: property identity (shared).
- `reference/connectors/master_data/commitment_bridge.yaml`: commitment_id reconciliation between construction and GL.

## Match methods

| Method | Use | Confidence |
|---|---|---|
| `exact` | Construction-native project_id, commitment_id, change_order_id, draw_request_id when the construction system is authoritative. | Highest. |
| `composite` | (project_id, vendor_id, scope_description_hash) when a commitment exists in construction and GL with different native ids. | High. Primary cross-system reconciliation key. |
| `fuzzy` | Normalized scope description + vendor name match when composite fails; low confidence. | Low. |
| `manual` | Operator-adjudicated mapping recorded in commitment_bridge with reviewer, timestamp, and reason. | Authoritative. |

## Confidence scoring

Every commitment_bridge row carries `confidence_tier`. Low-confidence matches hold downstream reconciliation (capex spend versus draws) until adjudicated.

## Hard cases

### Same capex project appearing in both GL and construction tracking

The GL tracks capex postings against `capex_project_id` (see `gl.capex_actual`); the construction system tracks the same project under its native project_id. The construction_project_registry declares a canonical project_id and maps both source systems to it. Failure mode: capex spend versus draws appears off because the two systems reference different project ids. Mitigation: registry-backed join.

### Multiple budget versions

A project carries baseline, current, approved, and proposed budget scenarios, all for the same project_id, same as_of_date, but different scenario labels. The `current_of_record` pointer in `construction/manifest.yaml` declares which scenario is canonical for reporting at each cycle. Failure mode: reporting silently flips between baseline and current, breaking variance. Mitigation: `con_multiple_budget_versions_flagged`.

### Owner-contingency versus contractor-contingency

Two distinct contingency pools carry different accountability. Owner contingency is released by the owner for scope changes owner-side; contractor contingency is controlled by the GC for bidding-error absorption. They must not be commingled in budget reporting or draw requests. Failure mode: drawing owner contingency against contractor-side overruns masks a bidding miss. Mitigation: `con_contingency_classification_correct` requires classification on every contingency line.

### Pending versus approved change orders

Only `status = approved` COs count toward the commitment ceiling extension. Pending and pending_approval COs are tracked separately and do not authorize additional spend. Draw requests that reference pending COs are flagged. Failure mode: drawing against pending COs is the leading indicator of cost overrun. Mitigation: `con_pending_vs_approved_co_separated`.

### Revised completion dates

Schedule_milestone carries `baseline_date`, `current_forecast_date`, and (when complete) `actual_date`. The baseline_date is frozen at project approval; current_forecast_date updates with each review; actual_date is filled when the milestone is achieved. The forecast_revision_history array preserves every update so slippage is visible. Failure mode: without revision history, slippage is invisible. Mitigation: `con_revised_completion_date_history`.

### Mixed rehab and operating capex coding

Unit turns include rehab scope that may qualify as capex (above the capitalization threshold) or opex. The construction system tracks the rehab project while the GL posts to capex or opex accounts. Failure mode: cross-system coding mismatch distorts NOI and renovation-yield metrics. Mitigation: `con_rehab_vs_opex_capex_coding_correct`.

## Failure modes summary

| Failure | Symptom | Check |
|---|---|---|
| Project id mismatch between GL and construction | Capex spend versus draws off | construction_project_registry gap |
| Multiple budget versions without current_of_record | Reporting flips between scenarios | `con_multiple_budget_versions_flagged` |
| Owner vs contractor contingency commingled | Bidding miss hidden | `con_contingency_classification_correct` |
| Pending CO drawn against | Overrun signal missed | `con_pending_vs_approved_co_separated` |
| Revised completion without history | Slippage invisible | `con_revised_completion_date_history` |
| Rehab miscoded between capex and opex | NOI and renovation-yield distorted | `con_rehab_vs_opex_capex_coding_correct` |
