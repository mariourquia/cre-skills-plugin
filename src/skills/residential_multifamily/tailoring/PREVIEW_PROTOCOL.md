# Preview Protocol

The tailoring skill never writes to `overlays/org/{org_id}/overlay.yaml` directly. Every proposed change is rendered as a human-readable diff between the current overlay state (or `overlays/org/_defaults/` for a new org) and the proposed updates, and is staged in `sign_off_queue.yaml`. A separate commit tool applies approved entries. The tailoring pack stops at the sign-off queue.

## Inputs to diff computation

- **Current state.** The current `overlays/org/{org_id}/overlay.yaml` for an existing org, or `overlays/org/_defaults/overlay.yaml` for a new org.
- **Proposed state.** The session state's proposed keys, excluding any key flagged `pending_doc`.
- **Scope filter.** Optional; limits the diff to a single audience (for audience refresh).

## Diff computation rules

1. Walk the proposed state key-by-key.
2. For each key, compare to the current state. Three outcomes:
   - `unchanged` — current value equals proposed value. Excluded from the diff.
   - `added` — key does not exist in current state. Included in the diff.
   - `modified` — current value differs from proposed value. Included in the diff.
3. For each `added` or `modified` key, capture:
   - The overlay key path (for example `approval_matrix.threshold_disbursement_1`).
   - The prior value (null if `added`).
   - The proposed value.
   - The interview source (bank_slug and question_id that produced the proposal).
   - The approval matrix row that governs the change, if any.
4. Sort the diff entries alphabetically by overlay key for stable rendering.

## Rendering rules

The TUI renders the diff in a YAML-side-by-side style reminiscent of unified diff output but formatted for YAML readability. Both the prior and proposed values are shown. The approver role and approval matrix row (if applicable) are shown inline. Example:

```
--- overlays/org/acme_mf/overlay.yaml  (current: defaults)
+++ overlays/org/acme_mf/overlay.yaml  (proposed)

@@ approval_matrix  ~~ approval_matrix row 6: financial_disbursement_tier_1
-  approval_matrix:
-    threshold_disbursement_1: null        # default placeholder
+  approval_matrix:
+    threshold_disbursement_1: 25000       # from coo_007
   ^ approver_role: coo_operations_leader
   ^ rationale: COO interview set PM autonomous disbursement threshold

@@ service_standards  ~~ (not gated)
-  service_standards:
-    lead_response_target: null
+  service_standards:
+    lead_response_target: same_business_day   # from coo_010
   ^ approver_role: coo_operations_leader
   ^ rationale: COO set lead response SLA for the org

@@ staffing_ratios  ~~ (not gated)
-  staffing_ratios:
-    leasing_units_per_agent: null
+  staffing_ratios:
+    leasing_units_per_agent: 95               # from coo_021
   ^ approver_role: coo_operations_leader
   ^ rationale: COO set leasing staffing norm
```

The numbers in the example above are illustrative of what an operator might answer during their interview; they are not canonical defaults. The canonical defaults under `overlays/org/_defaults/` contain placeholders only.

## Sign-off queue entries produced from the diff

Each `added` or `modified` entry becomes a `sign_off_queue.yaml` entry. For the example above, three entries would open:

```yaml
- queue_entry_id: 01HV6X1R...
  org_id: acme_mf
  session_id: 20260415_acme_coo_01
  overlay_key: approval_matrix.threshold_disbursement_1
  prior_value: null
  proposed_value: 25000
  rationale: COO interview set PM autonomous disbursement threshold.
  interview_source:
    bank_slug: coo
    question_id: coo_007
  approver_role: coo_operations_leader
  approval_matrix_row: 6
  created_at: 2026-04-15T17:32:10Z
  expires_at: 2026-05-15T17:32:10Z
  status: pending
  approver_note: null

- queue_entry_id: 01HV6X1S...
  org_id: acme_mf
  session_id: 20260415_acme_coo_01
  overlay_key: service_standards.lead_response_target
  prior_value: null
  proposed_value: same_business_day
  rationale: COO set lead response SLA for the org.
  interview_source:
    bank_slug: coo
    question_id: coo_010
  approver_role: coo_operations_leader
  approval_matrix_row: null
  created_at: 2026-04-15T17:32:10Z
  expires_at: 2026-05-15T17:32:10Z
  status: pending
  approver_note: null

- queue_entry_id: 01HV6X1T...
  org_id: acme_mf
  session_id: 20260415_acme_coo_01
  overlay_key: staffing_ratios.leasing_units_per_agent
  prior_value: null
  proposed_value: 95
  rationale: COO set leasing staffing norm.
  interview_source:
    bank_slug: coo
    question_id: coo_021
  approver_role: coo_operations_leader
  approval_matrix_row: null
  created_at: 2026-04-15T17:32:10Z
  expires_at: 2026-05-15T17:32:10Z
  status: pending
  approver_note: null
```

## What the preview does not do

- Does not write to `overlays/org/{org_id}/`.
- Does not mutate `overlays/org/_defaults/`.
- Does not mutate any file under `_core/`.
- Does not speculatively fill keys whose source document is `status: open` in the missing-docs queue. Those keys are flagged `pending_doc` and omitted from the diff.

## What the preview always does

- Shows every added and modified key with interview source traceability.
- Opens a sign-off queue entry for each change, with the correct approver role.
- Attaches the approval matrix row where one applies.
- Writes a summary markdown to `tailoring/sessions/{org_id}/{session_id}__summary.md`.

## Approver actions

An approver, using an external tool, reads `sign_off_queue.yaml`, filters by their `approver_role`, and sets `status` to `approved` or `rejected`. The external commit tool then picks up `approved` entries and applies them to `overlays/org/{org_id}/overlay.yaml`, writing a change log entry per change.

The tailoring pack does not automate the approver's action. The pack's contract ends at the sign-off queue.
