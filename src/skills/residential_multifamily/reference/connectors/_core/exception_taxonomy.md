# Exception Taxonomy

Exceptions are the audit trail of everything that went wrong in the
integration layer. Every data-quality check, every reconciliation pass,
every workflow activation gate that fails produces an exception. This
document defines the categories, the severity ladder, the default routing,
the escalation policy, and the dwell-time SLAs.

## Structure of an exception

An exception record lives at
`reference/connectors/_core/exceptions/<YYYY>/<MM>/<exception_id>.json`
and carries:

- `exception_id` - pattern `ex_<yyyy_mm_dd>_<category>_<sequence>`.
- `category` - one of the categories defined below.
- `subcategory` - domain-specific refinement.
- `severity` - `critical`, `blocker`, `warning`, `info`.
- `source_scope` - connector, entity, workflow, metric, or file that
  triggered the exception.
- `detected_at` - UTC timestamp.
- `detected_by` - rule or check slug.
- `payload` - structured facts (observed vs expected, counts, references).
- `status` - `open`, `acknowledged`, `in_remediation`, `resolved`,
  `waived`.
- `dwell_time_target` - SLA window for the exception.
- `routed_to` - role slug or audience name.
- `escalation_chain` - array of role slugs in escalation order.
- `related_exceptions` - array of related exception ids.
- `resolution_notes` - free text.
- `resolved_at` - UTC timestamp when status transitions to `resolved`.

Applies across all eight connectors: `pms`, `gl`, `crm`, `ap`,
`market_data`, `construction`, `hr_payroll`, `manual_uploads`.

## Categories

### dq_blocker

Data-quality failures that prevent promotion of a row or a landing.

Examples: null-critical field, duplicate primary key, unit-count
reconciliation fail, lease-status sum not equal to unit count, charge-
payment tie-out fail, commitment-CO-draw reconciliation fail, enum value
unmapped with row rejection.

- Default severity: `blocker`.
- Default routing: domain owner (per connector `manifest.yaml`).
- Escalation policy: if open past `dwell_time_target`, escalate to
  regional-ops or asset-mgmt depending on the affected workflow.
- Dwell-time SLA: one business day for pms/gl/ap/construction; two business
  days for market_data and manual_uploads.

### dq_warning

Data-quality anomalies that do not block promotion but should be reviewed.

Examples: out-of-band occupancy value, concession rate shift above
watchlist band, late-arriving row that supersedes a recent one, status
transition skipping states (`notice` → `terminated` without `move_out`),
identity resolution `proposed` rather than `resolved`.

- Default severity: `warning`.
- Default routing: domain owner.
- Escalation policy: summarize daily to domain owner; escalate if
  unreviewed past three business days.
- Dwell-time SLA: three business days.

### reconciliation_mismatch

Cross-source reconciliation failures.

Examples: PMS unit count differs from property master, GL actuals do not
reconcile to source GL totals, AP invoice total differs from commitment
balance, draw totals differ from approved payment history.

- Default severity: `blocker` by default; `warning` when the mismatch is
  inside tolerance.
- Default routing: finance-reporting or the relevant domain owner.
- Escalation policy: open past SLA escalates to asset-mgmt.
- Dwell-time SLA: two business days.

### identity_unresolved

Source-side identifiers that do not resolve to canonical identifiers.

Examples: PMS `PropCode` with no match in `property_crosswalk.csv`, vendor
name with no match in `vendor_master`, lease with unresolved unit, rent
comp with unresolved property.

- Default severity: `blocker` when the row is required-for-load,
  `warning` otherwise.
- Default routing: domain owner; for unresolved proposals, the workflow
  owner of the resolution proposal queue.
- Escalation policy: open past SLA escalates to asset-mgmt or compliance-
  risk as relevant.
- Dwell-time SLA: three business days.

### schema_drift

Source-side schema changes detected at landing or during mapping.

Examples: field added, field removed, field renamed, type changed, enum
added, enum removed, primary-key structure changed, grain changed.

- Default severity: `warning` when additive and optional; `blocker` when
  a required canonical field loses its source.
- Default routing: domain owner.
- Escalation policy: open past SLA escalates to the integration-layer
  owner for vendor adapter updates.
- Dwell-time SLA: five business days.

### stale_source

Required inputs past their staleness ceiling.

Examples: market rent benchmark past refresh cadence, rent comp source
older than acceptance window, manager-submitted file for prior period
missing.

- Default severity: `warning` by default; `blocker` when the workflow's
  `minimum_confidence_threshold` is `medium` or higher and no substitute
  exists.
- Default routing: market-analytics owner (for market_data), domain owner
  otherwise.
- Escalation policy: persistent staleness across two cycles escalates to
  asset-mgmt.
- Dwell-time SLA: the stale ceiling itself (no extra dwell once over).

### mapping_override_pending

A mapping override was requested but is not yet approved. Rows depending
on the override enter quarantine.

- Default severity: `warning`.
- Default routing: connector maintainer + approval routing.
- Escalation policy: open past SLA escalates to asset-mgmt.
- Dwell-time SLA: three business days.

### approval_override_pending

An approval matrix threshold override was requested but is not yet
decided. Relevant approvals hold.

- Default severity: `warning`.
- Default routing: org-defined primary approver for the workflow kind.
- Escalation policy: open past SLA escalates to the org-defined backup
  approver.
- Dwell-time SLA: two business days.

### manual_correction_required

A row or a value needs human correction outside the normal pipeline.

Examples: PII retention cleanup, secret shredding, known vendor-side data
error that will not be fixed at source.

- Default severity: `blocker` by default (the affected row stays
  quarantined), `warning` when the correction is downstream-only.
- Default routing: compliance-risk + domain owner.
- Escalation policy: open past SLA escalates to the integration-layer
  owner.
- Dwell-time SLA: three business days.

### policy_violation

A proposed action violates canonical policy (approval floor, fair-housing
rule, safety rule).

Examples: proposed concession exceeds canonical cap, proposed tenant-screening
practice crosses fair-housing guardrail, safety-related work-order
deferred past SLA.

- Default severity: `critical`.
- Default routing: compliance-risk.
- Escalation policy: any policy violation auto-escalates to the canonical
  escalation chain on detection. Not time-gated.
- Dwell-time SLA: zero; immediate.

### fair_housing_sensitive

Any event that touches protected-class handling, reasonable accommodation,
or pattern detection on demographic proxies.

Examples: application denial reason with protected-class proximity,
advertising language with protected-class implication, reasonable
accommodation request pending.

- Default severity: `critical`.
- Default routing: compliance-risk + legal.
- Escalation policy: auto-escalate on detection; human review required
  before any workflow continues.
- Dwell-time SLA: zero; immediate.

### legal_sensitive

Legal-hold, litigation, eviction, or counsel-review territory.

Examples: eviction filing status, lease dispute, subpoena on resident
records, litigation hold on any data stream.

- Default severity: `critical`.
- Default routing: compliance-risk + legal.
- Escalation policy: auto-escalate; human review required before any
  workflow continues.
- Dwell-time SLA: zero; immediate.

## Severity ladder summary

| Severity | Effect on workflows | Default alerting |
|---|---|---|
| `critical` | All affected workflows refuse; escalation chain activated immediately | Immediate to compliance-risk; no batching |
| `blocker` | Workflow activation refuses; scorecard declines composite | Immediate to domain owner; daily rollup elsewhere |
| `warning` | Workflow activates with confidence downgrade; exception surfaced in output | Daily digest to domain owner |
| `info` | No effect on workflow; retained for audit | Weekly digest |

## Routing tree

The default routes compile from this tree. Org overlays may replace the
default target with an org-scoped role, but only to add specificity - they
may not skip a default target.

```
exception.category
├── dq_blocker                → domain_owner(connector)
├── dq_warning                → domain_owner(connector)
├── reconciliation_mismatch   → finance_reporting | domain_owner
├── identity_unresolved       → domain_owner(connector)
├── schema_drift              → domain_owner(connector) + integration_layer_owner
├── stale_source              → market_analytics | domain_owner
├── mapping_override_pending  → connector_maintainer + approval_routing
├── approval_override_pending → primary_approver(workflow)
├── manual_correction_required → compliance_risk + domain_owner
├── policy_violation          → compliance_risk (auto-escalate)
├── fair_housing_sensitive    → compliance_risk + legal (auto-escalate)
└── legal_sensitive           → compliance_risk + legal (auto-escalate)
```

## Escalation chain

Per-exception escalation chains are defined in
`overlays/org/<org_id>/escalation_chains.yaml`. A canonical default chain
lives in `_core/approval_matrix.md` and applies when the org overlay is
silent. Typical default chain (paraphrased, exact values live in the org
overlay):

1. Domain owner.
2. Role lead for the affected workflow.
3. Asset management.
4. Compliance-risk.
5. Executive.

An auto-escalate exception skips steps one and two and goes directly to
compliance-risk (and legal when the category names legal involvement).

## Dwell-time SLAs

| Category | Default dwell SLA |
|---|---|
| dq_blocker | 1 business day (pms/gl/ap/construction); 2 business days (market_data, manual_uploads) |
| dq_warning | 3 business days |
| reconciliation_mismatch | 2 business days |
| identity_unresolved | 3 business days |
| schema_drift | 5 business days |
| stale_source | no extra; over at staleness ceiling |
| mapping_override_pending | 3 business days |
| approval_override_pending | 2 business days |
| manual_correction_required | 3 business days |
| policy_violation | 0 (immediate) |
| fair_housing_sensitive | 0 (immediate) |
| legal_sensitive | 0 (immediate) |

Org overlays may tighten dwell SLAs but may not loosen them below
canonical defaults.

## Exception closure

An exception closes when:

- `resolved` - the condition that triggered it is resolved. `resolved_at`
  is stamped. Downstream recompute runs if required.
- `waived` - a reviewer with appropriate approval authority waives the
  exception. The waiver requires an `approved_by` reference. Waiver is
  logged to `approval_override_log.yaml` when the waiver contradicts
  canonical policy; to `exception_waiver_log.yaml` otherwise.

Closure is append-only. A reopened exception is a new exception with a
`related_exceptions` link back.

## Reporting

The integration layer emits daily and weekly exception digests scoped to
each audience. The digests source from the exception store directly; they
do not introduce new calculations. Digest templates live at
`reference/connectors/_core/reporting_templates/exception_digest__<audience>.md`
and are read-only to tailoring.
