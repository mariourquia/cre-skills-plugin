# Update Flow Walk-Through — `approval_threshold_policy`

Scenario: org-level policy review lifts the PM-approvable single-invoice disbursement (`threshold_disbursement_1`) from $5,000 to $7,500.

## 1. Inbound → `reference/raw/approval_threshold_policy/2026/03/policy_defaults__2026-03-31.csv`

Row shape: `(segment, management_mode, threshold_slug, threshold_category, policy_owner_role, amount, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/approval_threshold_policy.yaml`.
- `unit` matches category (dollars for disbursement, months for concessions, days for delinquency).
- `policy_owner_role` matches the role taxonomy.

## 3. Normalization

Write to `reference/normalized/approval_threshold_defaults.csv` (or a per-org override if `scope.org_id` set).

## 4. Approval

**All approval threshold policy changes require explicit human approval** regardless of delta size. Threshold changes are foundational to the approval matrix itself. Auto-approval is disabled for this category.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_04_01_0010
change_type: update
target_kind: approval_threshold
target_ref: reference/normalized/approval_threshold_defaults.csv#atd-disbursement-1
old_value:
  value: 5000
new_value:
  value: 7500
source_name: "Org policy review Q2 2026 (illustrative)"
source_type: internal_record
source_date: 2026-04-01
as_of_date: 2026-03-31
proposed_by: agent:policy_threshold_agent
approved_by: human:coo_owner
proposed_at: 2026-04-01T15:00:00Z
approved_at: 2026-04-02T10:00:00Z
confidence: verified
reason_for_change: |
  Org policy review raised PM-approvable single-invoice disbursement ceiling from $5k to $7.5k
  to reduce routing friction on routine operating spend. All downstream gated actions must
  re-evaluate against the new ceiling.
affected_skills:
  - roles/property_manager
  - roles/regional_manager
  - roles/asset_manager
  - workflows/operating_review
  - workflows/capex_prioritization
  - workflows/unit_turn_make_ready
  - workflows/work_order_triage
affected_overlays:
  - management_mode/third_party_managed
  - management_mode/self_managed
```

## 6. Derived Recomputation

No derived files. But the overlay file(s) that cite the approval matrix must be re-read to surface the updated ceiling in prose.

## 7. Notifications

Every pack that has `threshold_disbursement_1` anywhere in a gated path is logged as affected. The tailoring skill surfaces a "policy change" banner the next time any operating review is produced.

## 8. Archival

Prior row archived to `reference/archives/approval_threshold_policy/2026/03/`.
