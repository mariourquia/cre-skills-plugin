# Unresolved Exceptions Queue

Workflow and schema for crosswalk rows whose identity cannot be auto-resolved. Rows in this state are not written to the crosswalk YAML files. They are parked here until a reviewer can resolve or retire them.

The queue is intentionally a narrative file plus a structured block, not a standalone YAML. The volume of unresolved exceptions should be low on a healthy deployment; a file-based queue is adequate for the scale of this subsystem's starter state.

## When a row lands here

A raw record is routed to this queue when the normalization pipeline cannot assign a canonical id at the required confidence. The typical reasons:

1. No automated match rule matched with confidence above the `unresolved -> low` threshold.
2. A fuzzy match produced multiple candidate canonical ids with comparable scores.
3. A composite match key has a missing or null field that the match rule requires.
4. A manual override expired and the default survivorship cannot assign identity.
5. The source registry does not have an entry for the `source_name` provenance value the record carries.

## Workflow

1. Pipeline records the exception with the fields below.
2. Reviewer (named on the exception) receives a notification via whatever alerting the operator has wired to the reconciliation checks.
3. Reviewer investigates, then either:
   - Accepts a suggested canonical id, creating a new crosswalk row with `match_method = manual`, `match_confidence = medium`, and a new entry in `change_log.md`.
   - Creates a new canonical id if the record represents a new business record not previously known to the subsystem; adds the row with `match_method = manual`, `match_confidence = high` if the new id is definitive, `medium` if provisional.
   - Marks the record as `do_not_ingest` with a reason; the raw record is retained in `reference/raw/<domain>/_rejected/` but does not propagate.
4. The exception's `resolution` field is populated; the queue entry is closed (marked `closed: true`) and retained for audit.

## Exception record schema

Each exception record carries the following fields. Records are kept in the `entries` block below; closed entries remain in the file and are not deleted.

| Field | Type | Required | Notes |
|---|---|---|---|
| `exception_id` | string | yes | snake_case slug, stable. |
| `opened_at` | ISO-8601 datetime | yes | |
| `source_system` | string | yes | matches a `source_id` in the registry. |
| `source_primary_key` | string | yes | source-local id of the unresolved record. |
| `target_canonical_object` | string | yes | the canonical object name (e.g., `property`, `vendor`, `resident_account`). |
| `reason` | enum | yes | one of `no_match`, `ambiguous_match`, `missing_match_key`, `expired_override`, `unknown_source`, `other`. |
| `candidate_canonical_ids` | list | no | ranked suggestions from the pipeline, if any. |
| `required_reviewer_role` | string | yes | role that must resolve the exception. |
| `escalation_path` | string | yes | who escalates if review does not happen within the SLA. |
| `pii_sensitivity` | enum | yes | mirrors the source's PII classification. |
| `legal_sensitivity` | enum | yes | mirrors the source's legal sensitivity. |
| `sla_hours` | integer | yes | time budget for reviewer action. |
| `resolution` | string | no | populated when closed. Names the canonical id assigned or `do_not_ingest`. |
| `closed` | boolean | yes | false while pending; true once resolved. |
| `closed_at` | ISO-8601 datetime | no | populated when closed. |

## Starter queue

The entries below illustrate the kinds of exceptions the queue is designed to hold. Every entry below is `status: sample` and does not reference a real record.

```yaml
status_tag: sample

entries:

  - exception_id: exc_ambig_prop_2025_08_14
    opened_at: "2025-08-14T09:42:00Z"
    source_system: accounts_payable_primary
    source_primary_key: AP-ORL-999
    target_canonical_object: property
    reason: ambiguous_match
    candidate_canonical_ids:
      - prop_orl_011
      - prop_orl_012
    required_reviewer_role: ap_manager
    escalation_path: corporate_controller
    pii_sensitivity: moderate
    legal_sensitivity: moderate
    sla_hours: 72
    resolution: null
    closed: false

  - exception_id: exc_missing_phone_email_2025_09_03
    opened_at: "2025-09-03T14:18:00Z"
    source_system: marketing_crm
    source_primary_key: LEAD-CRM-712004
    target_canonical_object: resident_account
    reason: missing_match_key
    candidate_canonical_ids: []
    required_reviewer_role: leasing_director
    escalation_path: regional_ops_director
    pii_sensitivity: high
    legal_sensitivity: high
    sla_hours: 120
    resolution: null
    closed: false

  - exception_id: exc_expired_override_vendor_2026_01_05
    opened_at: "2026-01-05T08:00:00Z"
    source_system: accounts_payable_primary
    source_primary_key: AP-PEST-4401
    target_canonical_object: vendor
    reason: expired_override
    candidate_canonical_ids:
      - vendor_v_00891
    required_reviewer_role: ap_manager
    escalation_path: corporate_controller
    pii_sensitivity: low
    legal_sensitivity: moderate
    sla_hours: 96
    resolution: null
    closed: false

  - exception_id: exc_unknown_source_2026_02_17
    opened_at: "2026-02-17T16:05:00Z"
    source_system: unknown_sftp_drop
    source_primary_key: UNKNOWN-DROP-001
    target_canonical_object: property
    reason: unknown_source
    candidate_canonical_ids: []
    required_reviewer_role: data_platform_team
    escalation_path: corporate_controller
    pii_sensitivity: moderate
    legal_sensitivity: moderate
    sla_hours: 48
    resolution: null
    closed: false
    notes: |
      Source name on the raw record does not resolve to a registry entry.
      Either a new registry entry is needed or the file was dropped in the
      wrong directory. Record is held at raw until resolution.

  - exception_id: exc_resident_dedup_2026_03_22
    opened_at: "2026-03-22T11:30:00Z"
    source_system: marketing_crm
    source_primary_key: LEAD-CRM-781445
    target_canonical_object: resident_account
    reason: ambiguous_match
    candidate_canonical_ids:
      - resident_rac_001218
      - resident_rac_001219
    required_reviewer_role: leasing_director
    escalation_path: regional_ops_director
    pii_sensitivity: high
    legal_sensitivity: high
    sla_hours: 72
    resolution: null
    closed: false
    notes: |
      Two candidate canonical ids tied on composite match score. Reviewer
      must never use protected-class attributes to break the tie. Allowed
      tiebreakers: chronological order of first contact, address match,
      named co-applicant overlap.
```

## SLA defaults

Default SLAs by PII / legal sensitivity:

| PII / legal sensitivity | SLA hours |
|---|---|
| restricted | 24 |
| high | 72 |
| moderate | 96 |
| low | 120 |
| none | 168 |

SLAs are informational defaults; operators may tighten them in deployment configuration.
