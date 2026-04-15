---
template_slug: tpm_audit_issue_log
title: Third-Party Manager Audit Issue Log
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [third_party_managed, owner_oversight]
  role: [third_party_manager_oversight_lead, asset_manager, portfolio_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used: []
produced_by: workflows/third_party_manager_scorecard_review
---

# TPM Audit Issue Log

**Property.** {{property_name}} ({{property_id}})
**TPM.** {{tpm_name}}
**Log owner.** {{log_owner}}
**Last updated.** {{last_updated}}

## Severity rubric

- S1: critical (fair-housing, compliance, financial integrity, safety).
- S2: material (financial, policy, reporting, SLA breach with material impact).
- S3: minor (process, documentation, non-material SLA).
- S4: observation (improvement recommendation).

## Open issues

| # | Severity | Date opened | Issue | Category | Owner (TPM) | Target close | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | {{issue_1_sev}} | {{issue_1_opened}} | {{issue_1}} | {{issue_1_cat}} | {{issue_1_owner}} | {{issue_1_target}} | {{issue_1_status}} | {{issue_1_notes}} |
| 2 | {{issue_2_sev}} | {{issue_2_opened}} | {{issue_2}} | {{issue_2_cat}} | {{issue_2_owner}} | {{issue_2_target}} | {{issue_2_status}} | {{issue_2_notes}} |
| 3 | {{issue_3_sev}} | {{issue_3_opened}} | {{issue_3}} | {{issue_3_cat}} | {{issue_3_owner}} | {{issue_3_target}} | {{issue_3_status}} | {{issue_3_notes}} |
| 4 | {{issue_4_sev}} | {{issue_4_opened}} | {{issue_4}} | {{issue_4_cat}} | {{issue_4_owner}} | {{issue_4_target}} | {{issue_4_status}} | {{issue_4_notes}} |

### Category legend

- `fair_housing`, `screening_policy`, `collections`, `reporting`, `budget`, `sla`, `staffing`, `vendor_mgmt`, `resident_comms`, `safety`, `data_access`, `contract_compliance`.

## Closed issues (this period)

| # | Severity | Issue | Closed date | Resolution | Audit-follow-up |
|---|---|---|---|---|---|
| {{closed_1_id}} | {{closed_1_sev}} | {{closed_1}} | {{closed_1_closed}} | {{closed_1_resolution}} | {{closed_1_followup}} |

## Rollup metrics

- Open S1 count: {{open_s1_count}}
- Open S2 count: {{open_s2_count}}
- `audit_issue_count_and_severity` composite: {{audit_composite}}

## Escalations

{{escalations_narrative}}

---

*Template status: starter.*
