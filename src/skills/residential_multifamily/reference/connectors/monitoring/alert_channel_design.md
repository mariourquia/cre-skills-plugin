# Alert Channel Design, Integration Layer

status_tag: reference

Channel structure for alerts emitted by the integration layer. Vendor-neutral. The subsystem recommends a channel role pattern; the operator maps each role to the product they actually use (Slack, Teams, PagerDuty, Opsgenie, email, or any combination).

## Channel roles

Each channel role is a destination pattern, not a specific channel. An operator can collapse multiple roles into a single channel or split them further, but every alert in `alert_policies.yaml` must resolve to at least one of these roles.

### Operations channel role

Audience: on-call engineers, data-owners, technical-owners, business-owners. Routine dq_warning, stale_source, identity_unresolved, mapping_override_pending alerts flow here. High-volume surface; expected to remain actionable rather than becoming noise.

Recommended structure:

- `ops_pms`
- `ops_gl`
- `ops_crm`
- `ops_ap`
- `ops_market_data`
- `ops_construction`
- `ops_hr_payroll`
- `ops_manual_uploads`

or a single `ops_integration` channel if the operator's volume is low enough to justify consolidation.

### Compliance channel role

Audience: `compliance_risk` and the compliance-officer role. `fair_housing_sensitive`, `legal_sensitive`, regulatory-program-impacting schema drift, and any exception tagged with a regulatory program flow here.

Recommended structure: a single `compliance_alerts_restricted` channel with narrow membership. Not a broadcast surface. All entries are retained per the compliance-retention overlay.

### Legal channel role

Audience: `legal_counsel`. Fair-housing-sensitive incidents, legal-sensitive incidents, and any approval-gate breach with litigation exposure flow here. Highest restriction; membership limited to legal and any named deputy.

Recommended structure: a single `legal_restricted` channel with sealed history per retention policy.

### Executive channel role

Audience: `executive`. Summary alerts only, a periodic digest of breach counts, aging items, and SLO status. Not a stream; executives do not triage raw alerts.

Recommended structure: a read-only `executive_digest` channel populated by the monthly and quarterly reporting workflows (`executive_operating_summary_generation`, `monthly_asset_management_review`, `quarterly_portfolio_review`).

### On-call page role

Audience: `on_call_ops`. Critical-severity alerts only: `normalization_failed`, `schema_drift_detected`, `reconciliation_blocker_failed`, `approval_gate_breach_imminent`, `fair_housing_field_touched`, `legal_sensitive_field_touched`.

Recommended structure: a pager rotation with an escalation policy that rolls through tiers per `exception_routing.yaml`.

## Channel hygiene principles

1. One alert, one channel. An alert should be loud in one destination, quiet in all others. Avoid cc-storm patterns where every audience receives every alert.
2. Restricted categories are never echoed to broad channels. Fair-housing-sensitive and legal-sensitive alerts are never posted to a general ops channel.
3. Every channel has a named steward. The steward reviews mute rules, retention, and membership quarterly.
4. Alerts carry a `related_runbook` link directly into the message payload. Operators open the runbook from the alert in one click.
5. Every alert message includes the `alert_id`, severity, source, affected entities or workflows, and dwell-time budget.

## Mapping channel roles to vendor products

The subsystem does not specify a chat product. Operators map channel roles as follows:

| Channel role | Possible vendor mappings |
|---|---|
| Operations | a channel per domain in the operator's chat product, with threaded discussion per incident |
| Compliance | a restricted channel plus a compliance-retention archive (often a case-management product) |
| Legal | a restricted channel, often with matter-based access control |
| Executive | a read-only digest feed or an email digest |
| On-call page | a paging product with escalation policies; chat integration is secondary |

## Mute and suppression

Mute rules belong in the alert policy, not in the channel. Channels should not silently drop alerts. The `mute_policy` field in `alert_policies.yaml` names the only valid suppressors, typically planned outage windows, planned cutover windows, and planned maintenance windows. Every suppression is recorded as an observability event of type `alert_muted` (see `observability_events.yaml`).

## Do-not-publish destinations

The following destinations never receive integration-layer alerts:

- Resident-facing channels.
- Vendor-facing channels.
- Owner or LP-facing channels.
- Any public-facing surface.
- Broad all-hands channels when the alert includes fair-housing or legal content.

Any appearance of an alert in a do-not-publish destination is an incident of category `legal_sensitive` and triggers `fair_housing_sensitive_flag.md` containment (even when the underlying data is not fair-housing-scoped) because the leak itself is a control failure.

## Onboarding a new channel

When the operator adds a new channel or consolidates an existing one:

1. Update `overlays/org/<org_id>/alert_channels.yaml` (operator-specific; not in this directory) to declare which channel role the channel serves.
2. Confirm membership.
3. Pin the `alert_policies.yaml` version and the runbook index.
4. Confirm the steward.
5. Verify the new channel passes the smoke test: fire a test alert of each severity and confirm routing.

## Relationship to ticketing

Alerts and tickets are distinct surfaces:

- An alert is an ephemeral signal that routes attention.
- A ticket is a durable artifact that tracks remediation.

The operator's ticketing product is out of scope here; the subsystem requires only that every incident of severity warning or critical result in a durable artifact (ticket, issue, case, or equivalent) that persists beyond the alert.
