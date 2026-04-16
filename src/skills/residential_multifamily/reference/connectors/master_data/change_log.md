# Change Log

Audit trail for every crosswalk update in this directory. Entries never get deleted; corrections are recorded as additional entries.

## Schema

Each entry conforms to the following shape. Entries are maintained in the `log` block below; newer entries are appended to the top.

| Field | Type | Required | Notes |
|---|---|---|---|
| `log_id` | string | yes | snake_case slug, stable. |
| `changed_at` | ISO-8601 datetime | yes | |
| `changed_by` | string | yes | role or named reviewer. |
| `crosswalk_file` | string | yes | file name relative to this directory. |
| `canonical_id` | string | yes | the canonical id the change touches. |
| `source_system` | string | conditional | required when the change touches a specific row's source mapping. |
| `source_primary_key` | string | conditional | required when the change touches a specific row's source mapping. |
| `change_type` | enum | yes | one of `row_added`, `row_closed`, `row_reopened`, `confidence_changed`, `override_applied`, `override_expired`, `override_renewed`, `survivorship_updated`, `match_method_upgraded`, `match_method_downgraded`, `retired`, `corrected`. |
| `prior_value_summary` | string | conditional | required when `change_type` modifies an existing value. |
| `new_value_summary` | string | conditional | required when `change_type` adds or modifies a value. |
| `reason` | string | yes | human-readable justification. |
| `related_exception_id` | string | no | when resolution of an `unresolved_exceptions_queue` entry triggered this change. |
| `related_override_id` | string | no | when an override in `manual_overrides.yaml` triggered this change. |

## Starter log

Every entry below is `status: sample`. The entries illustrate the kinds of change events the log is designed to hold. None refers to a real record.

```yaml
status_tag: sample

log:

  - log_id: log_2026_03_31_prop_cta_002_override_renewed
    changed_at: "2026-03-31T15:14:00Z"
    changed_by: regional_ops_director
    crosswalk_file: property_master_crosswalk.yaml
    canonical_id: prop_cta_002
    source_system: east_region_pms
    source_primary_key: P1184
    change_type: override_renewed
    prior_value_summary: |
      Override ovr_prop_cta_002_pms_migration was approaching expiration
      2026-09-01.
    new_value_summary: |
      Override renewed with expires_at 2027-09-01 pending completion of
      full reconciliation window.
    reason: |
      Reconciliation window still in progress; cannot promote identity to
      automated-match confidence yet.
    related_override_id: ovr_prop_cta_002_pms_migration

  - log_id: log_2025_09_16_unit_cta_001_override_expired
    changed_at: "2025-09-16T09:00:00Z"
    changed_by: regional_ops_director
    crosswalk_file: unit_crosswalk.yaml
    canonical_id: unit_cta_001_3101
    source_system: east_region_pms
    source_primary_key: "3A"
    change_type: override_expired
    prior_value_summary: |
      Override ovr_unit_cta_001_3101_relabel active since 2024-09-16.
    new_value_summary: |
      Override retired; mapping confirmed as stable by operator review.
    reason: |
      Annual review window confirmed the post-renovation relabel is stable.
      Underlying crosswalk row remains current.
    related_override_id: ovr_unit_cta_001_3101_relabel

  - log_id: log_2025_07_02_draw_rdu_004_resubmit
    changed_at: "2025-07-02T14:22:00Z"
    changed_by: construction_manager
    crosswalk_file: draw_request_crosswalk.yaml
    canonical_id: draw_rdu_004_hvac_2025_dr_002
    source_system: construction_tracker_primary
    source_primary_key: P-CR-HVAC-001-DR-002b
    change_type: row_added
    new_value_summary: |
      Second submission approved; row added with effective_start 2025-06-27.
    reason: |
      Lender approved the resubmission after the first attempt was
      rejected for insufficient supporting documentation.
    related_override_id: ovr_draw_rdu_004_hvac_dr002_resubmit

  - log_id: log_2025_06_19_draw_rdu_004_rejected
    changed_at: "2025-06-19T11:05:00Z"
    changed_by: construction_manager
    crosswalk_file: draw_request_crosswalk.yaml
    canonical_id: draw_rdu_004_hvac_2025_dr_002
    source_system: construction_tracker_primary
    source_primary_key: P-CR-HVAC-001-DR-002a
    change_type: row_closed
    prior_value_summary: |
      First submission row open since 2025-06-01.
    new_value_summary: |
      Row closed with effective_end 2025-06-19.
    reason: |
      Lender rejected the submission. Canonical id preserved; resubmission
      will open a new row with the same canonical id.

  - log_id: log_2025_01_01_vendor_v_00412_rename
    changed_at: "2025-01-01T00:00:00Z"
    changed_by: ap_manager
    crosswalk_file: vendor_master_crosswalk.yaml
    canonical_id: vendor_v_00412
    source_system: accounts_payable_primary
    source_primary_key: AP-ELEC-881
    change_type: row_added
    prior_value_summary: |
      Prior row for AP-ELEC-881 closed with effective_end 2024-12-31 due
      to vendor rename.
    new_value_summary: |
      New row added with effective_start 2025-01-01 carrying new legal
      name "Ridge Power Systems LLC".
    reason: |
      Vendor rename with tax id continuity confirmed by AP. Canonical id
      preserved.
    related_override_id: ovr_vendor_v_00412_rename

  - log_id: log_2024_12_01_prop_atl_007_split
    changed_at: "2024-12-01T00:00:00Z"
    changed_by: regional_ops_director
    crosswalk_file: property_master_crosswalk.yaml
    canonical_id: prop_atl_007_legacy
    source_system: east_region_pms
    source_primary_key: P0884
    change_type: retired
    prior_value_summary: |
      Combined-asset canonical record open since 2022-08-15.
    new_value_summary: |
      Canonical record retired with effective_end 2024-11-30. Successor
      canonical ids prop_atl_007a and prop_atl_007b opened.
    reason: |
      Assemblage operationally split into two properties after phase-2
      delivery. Historical records remain tied to prop_atl_007_legacy;
      current operations run under the successor canonical ids.

  - log_id: log_2024_09_16_unit_cta_001_relabel
    changed_at: "2024-09-16T00:00:00Z"
    changed_by: regional_ops_director
    crosswalk_file: unit_crosswalk.yaml
    canonical_id: unit_cta_001_3101
    source_system: east_region_pms
    source_primary_key: "3A"
    change_type: row_added
    prior_value_summary: |
      Prior row for source_primary_key "301" closed with effective_end
      2024-09-15 due to post-renovation relabel.
    new_value_summary: |
      New row added with effective_start 2024-09-16.
    reason: |
      Post-renovation relabel; PMS did not emit an automated mapping row.
    related_override_id: ovr_unit_cta_001_3101_relabel

  - log_id: log_2024_02_28_resident_rac_000412_converged
    changed_at: "2024-02-28T00:00:00Z"
    changed_by: leasing_director
    crosswalk_file: resident_account_crosswalk.yaml
    canonical_id: resident_rac_000412
    source_system: east_region_pms
    source_primary_key: R000412
    change_type: row_added
    new_value_summary: |
      PMS row added; composite match against CRM row
      LEAD-CRM-553912 confirmed on first PMS extract.
    reason: |
      Lead-to-lease convergence. Composite match on phone + email +
      last-name-normalized; protected-class attributes not used.

  - log_id: log_2023_08_15_unit_rdu_004_split
    changed_at: "2023-08-15T00:00:00Z"
    changed_by: regional_ops_director
    crosswalk_file: unit_crosswalk.yaml
    canonical_id: unit_rdu_004_2204_legacy
    source_system: east_region_pms
    source_primary_key: "204"
    change_type: retired
    prior_value_summary: |
      Combined-unit canonical record open since 2023-02-01.
    new_value_summary: |
      Canonical record retired with effective_end 2023-08-14. Successor
      canonical ids unit_rdu_004_2204a and unit_rdu_004_2204b opened.
    reason: |
      Unit split during value-add; two new units created physically.
      Historical lease tied to the retired canonical id.
```

## 2026-04-15 Wave-5 Yardi adapter integration

Added Yardi rows to: property_master_crosswalk, unit_crosswalk, lease_crosswalk, vendor_master_crosswalk, account_crosswalk, capex_project_crosswalk, dev_project_crosswalk, asset_crosswalk, market_crosswalk, submarket_crosswalk, resident_account_crosswalk.

Source: `reference/connectors/adapters/yardi_multi_role/crosswalk_additions.yaml`.
Yardi remains in classification-pending posture per `yardi_multi_role/runbooks/yardi_classification_path.md`. Crosswalk rows carry status: provisional until classification closes.
Authored_by: skill_factory_agent. Reviewed_by: pending.

## Reporting cadence

The log is the system of record for crosswalk evolution. Any audit of master data history is expected to cite log entries by `log_id`. The log is reviewed at least once per rollout wave; the review produces a summary that includes counts per `change_type`, any entries missing required fields, and any open reconciliation issues surfaced by the entries.
