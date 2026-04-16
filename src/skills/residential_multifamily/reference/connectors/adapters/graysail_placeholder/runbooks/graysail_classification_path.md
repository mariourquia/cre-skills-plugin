# GraySail Classification Path

Status: deferred_until_classification_closes
Owner role: data_platform_team
Accountability chain: data_platform_team -> asset_mgmt_director -> executive
Audience: data platform operators driving the GraySail onboarding decision.

## Purpose

This runbook is the **decision tree** that converts the bounded
`graysail_placeholder` stub into a classified adapter. It is the only
canonical path to move the adapter out of `stub` status. Until every
required checkpoint below closes, the adapter remains a placeholder and
every downstream workflow continues to run in
`blocked_pending_classification` for GraySail as declared in
`workflow_activation_additions.yaml`.

The worksheet at `../classification_worksheet.md` carries the detailed
question bank. This file is the **sequencing and branching logic** that
tells the operator which section of the worksheet is on the critical
path at each decision.

Cross-references:

- `../manifest.yaml` (adapter definition, status: stub)
- `../bounded_assumptions.yaml` (explicit assumptions and blast-radius)
- `../provisional_source_contract.yaml` (placeholder entity envelopes)
- `../workflow_relevance_map.yaml` (candidate workflow dependencies, all blocked_until_classified)
- `../dq_rules.yaml` (gs_* deferred-mode DQ rules)
- `../source_registry_entry.yaml` (fragment, status placeholder_pending_clarification)
- `../../../../_core/stack_wave4/source_of_truth_matrix.md` (row deferred until this runbook closes)
- `../../../../_core/stack_wave4/open_questions_and_risks.md` (ontology and workflow extensions)

## How to use this runbook

1. Start at **Step 1** and walk each branch in order. Do not skip.
2. At every decision point, mark the answer in
   `../classification_worksheet.md` (Section 1-5). This runbook is a
   sequencing aid; the worksheet is the record of truth.
3. When a branch reaches a **next action** or **checkpoint**, do not
   advance the adapter until the checkpoint's deliverable lands in the
   adapter directory.
4. At the end of the tree, if every checkpoint closes, fork this adapter
   into a renamed slug: `graysail_<role>_<pattern>` (for example,
   `graysail_sop_store_api_subset`, `graysail_approval_policies_sftp_all`,
   `graysail_service_catalog_export_legacy_parallel`). Do **not**
   overwrite the placeholder in place. The placeholder directory is
   preserved as the classification trail.

## Step 1 -- Role identification

Drives which canonical domain and which worksheet questions matter most.

**Question:** What does GraySail hold at the operator?

Branches:

- `pms` -- property management system traffic (resident, lease, work
  order, turn, rent roll)
  - **Interpretation:** GraySail is a PMS in disguise, or a secondary
    PMS for a portfolio subset.
  - **Blast radius:** source-of-truth matrix for `property`, `unit`,
    `lease`, `lease_event`, `charge`, `payment`, `work_order`, `vendor`
    changes; AppFolio is no longer sole PMS primary.
  - **Next action:** run `../classification_worksheet.md` Section 1
    questions 2-4 against each PMS object family; STOP if any object
    overlaps AppFolio without a survivorship rule.
  - **Template:** `../provisional_source_contract.yaml` ->
    `entities.sop_document_placeholder` is **not** applicable; instead,
    fork into a starter that replicates the shape of
    `adapters/appfolio_pms/source_contract.yaml` against sanitized
    samples.

- `gl` -- general-ledger traffic (journal entries, budget lines,
  forecasts, actuals, close-calendar rules)
  - **Interpretation:** GraySail carries accounting data.
  - **Blast radius:** source-of-truth matrix for `budget_line`,
    `forecast_line`, `actual_line`, `variance_explanation` is affected;
    Sage Intacct is no longer sole GL primary post-close.
  - **Next action:** run `../classification_worksheet.md` Section 1
    questions 2-4; require finance_reporting sign-off before any live
    sample lands.
  - **Template:** fork against
    `adapters/sage_intacct_gl/source_contract.yaml`.

- `crm` -- leasing pipeline, leads, tours, applications, approval
  outcomes
  - **Interpretation:** GraySail is a CRM overlay or replacement.
  - **Blast radius:** source-of-truth matrix for `lead`, `showing`,
    `application`, `approval_outcome` changes; AppFolio CRM claim
    contested.
  - **Next action:** run `../classification_worksheet.md` Section 1
    questions 2-4; require compliance_risk sign-off (fair-housing
    exposure).
  - **Template:** fork against canonical
    `reference/connectors/crm/source_contract.yaml` (if present) or
    extend `adapters/crm_vendor_family_stub/`.

- `reporting_feed` -- read-only aggregate of other systems (a BI layer)
  - **Interpretation:** GraySail is derived, not primary, for any
    operating object. It is a **secondary** source at best.
  - **Blast radius:** reconciliation checks only; GraySail is informative
    and cannot break ties.
  - **Next action:** require reconciliation commentary defining the
    drift tolerance vs. primary source; cite
    `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
    once created; default posture is
    `silent_audit` within the band, `warning` outside.
  - **Template:** extend `../provisional_source_contract.yaml` into
    `entities.reconciliation_snapshot_placeholder` and fork accordingly.

- `legacy_historical` -- pre-cutover data archive; not authoritative for
  anything post-cutover
  - **Interpretation:** GraySail is a cold-storage read source for
    history only; no live write path.
  - **Blast radius:** low; historical-only data cannot contaminate
    current operating workflows if the cutover-date boundary is
    enforced. A single misplaced row can quietly extend the historical
    window if boundary enforcement is weak.
  - **Next action:** declare the cutover date in
    `../source_registry_entry.yaml`; add a DQ rule asserting
    `row.as_of_date < cutover_date`; require operator sign-off to
    confirm the historical-only posture and cutover date.
  - **Template:** keep `../provisional_source_contract.yaml` envelope
    but add a cutover-date invariant; fork into
    `graysail_legacy_historical`.

- `other` -- SOP / policy knowledge store, approval-matrix repository,
  vendor service catalog, training library, or other operator-specific
  role
  - **Interpretation:** aligns with the current working hypothesis per
    `../bounded_assumptions.yaml::role_hypothesis_sop_knowledge_store`.
  - **Blast radius:** depends on whether content references canonical
    objects; default posture is `no_canonical_object_coverage` and
    workflow references remain blocked.
  - **Next action:** run `../classification_worksheet.md` Section 1
    question 1 (operator's own description); then Section 1 question 3
    (does GraySail claim authority for any operational object?).
  - **Template:** `../provisional_source_contract.yaml` (keep as-is
    for SOP/policy document shapes).

## Step 2 -- Access path

Drives `ingestion_mode`, `cadence`, and `credential_method` in the
`source_registry.yaml` entry.

**Question:** How does the operator pull data out of GraySail today?

Branches:

- `api` -- REST, GraphQL, or vendor SDK
  - **Next action:** require the operator to name the credentialing
    contact (Section 2 question 6); add `credential_method: oauth` or
    `api_key` to the forked adapter's source-registry entry; route
    secret rotation through the subsystem security runbook.
  - **Template:** `../provisional_source_contract.yaml` extended with
    concrete endpoint definitions (matching the shape of
    `adapters/dealpath_deal_pipeline/source_registry_entry.yaml` at
    `ingestion_mode: api`).

- `sftp` -- scheduled file drop
  - **Next action:** require cadence window (Section 2 question 7), file
    shape (CSV / JSON / DOCX / PDF), and retention window; add
    `credential_method: ssh_key`; declare the freshness expectation
    before `gs_freshness_pending` can be promoted to a non-warning
    severity.
  - **Template:** extend `../provisional_source_contract.yaml` with
    file-shape declarations; fork into
    `graysail_<role>_sftp_<pattern>`.

- `export` -- manual export from GraySail UI to shared drive / email
  - **Next action:** treat as `ingestion_mode: manual_upload`; declare
    `expected_latency_minutes: unknown_until_cadence_confirmed`; require
    operator commitment to a cadence window before workflows light up.
  - **Template:** extend `../provisional_source_contract.yaml`; fork
    into `graysail_<role>_export_<pattern>`.

- `portal` -- read-only through the GraySail web UI, no extraction path
  - **Next action:** document the limitation in the forked
    `source_registry_entry.yaml::known_limitations`; gate any downstream
    workflow on a retrieval-agent deliverable; do not promote beyond
    `stub` until extraction path exists.
  - **Template:** no template advancement possible at this branch;
    stay at stub and return to Step 1 when extraction becomes feasible.

- `unknown` -- operator has not yet surveyed extraction paths
  - **Next action:** do not advance. Return the worksheet to the
    operator with Section 2 flagged as the blocker.
  - **Template:** none.

## Step 3 -- Operating pattern

Drives the partial-mode activation logic in
`workflow_activation_additions.yaml`.

**Question:** Across the portfolio, is GraySail the operating system for
every property, a subset, or a legacy parallel?

Branches:

- `all` -- every property in scope uses GraySail for the classified
  role
  - **Interpretation:** whole-portfolio activation.
  - **Next action:** require a full crosswalk against AppFolio /
    Intacct / Procore / Dealpath property master to ensure no
    orphans; add `gs_referential_pending` promotion criterion.
  - **Partial_mode_behavior on forked adapter:** `active` once DQ gates
    pass.

- `subset` -- a defined subset of the portfolio uses GraySail; the rest
  use another system
  - **Interpretation:** portfolio-level segmentation. GraySail applies
    only to a named property set.
  - **Next action:** declare the property set explicitly in the forked
    `source_registry_entry.yaml::applicable_property_set`; require
    reconciliation against the declared set; any property not in the
    set must not receive GraySail-derived data.
  - **Partial_mode_behavior on forked adapter:** `partial_scope_active`.

- `legacy_parallel` -- GraySail operates alongside another system for
  the same property set, with a cutover in-flight
  - **Interpretation:** dual-run. GraySail is declared
    `legacy_secondary`; the other system is `primary`.
  - **Next action:** declare the cutover date; add a dual-run DQ rule
    that compares GraySail output against primary within tolerance band
    per `reference/normalized/schemas/reconciliation_tolerance_band.yaml`;
    require finance_reporting sign-off before dual-run closes.
  - **Partial_mode_behavior on forked adapter:** `dual_run_audit_only`
    until cutover; `deprecated` after cutover.

## Step 4 -- Data sensitivity

Drives `pii_classification`, `financial_sensitivity`,
`legal_sensitivity` on the forked `source_registry_entry.yaml` and
triggers the sign-off chain.

**Question:** What sensitivity tiers does GraySail content carry?

Branches:

- `resident_pii` -- resident names, SSNs, government ids, credit
  reports, unit-level occupant details
  - **Next action:** require compliance_risk sign-off before any live
    sample lands; add fair-housing review to onboarding checklist;
    route through
    `adapters/../_core/security/` posture declared in the subsystem
    security runbook; set `pii_classification: resident`.

- `financial` -- contract dollar values, margin data, fee schedules,
  vendor tax ids
  - **Next action:** require finance_reporting sign-off before any live
    sample lands; set `financial_sensitivity: restricted`.

- `legal` -- contract language, letters of intent, legal-strategy
  memos, regulatory-program guidance
  - **Next action:** require compliance_risk + legal sign-off; set
    `legal_sensitivity: restricted`; bar sample transmission through
    uncontrolled channels (email, chat).

- `none` -- operator-confirmed public or low-sensitivity content only
  - **Next action:** declare explicitly; keep the posture
    reversible by adding the sensitivity triage to the quarterly
    review in `../bounded_assumptions.yaml::review_cadence`.

Sensitivity branches compose: more than one can fire simultaneously.
The strictest-tier rule wins; sign-off chains aggregate.

## Checkpoints

Every deliverable below must land in the adapter directory (either the
placeholder or the eventual fork) before classification closes. Each
checkpoint maps to a specific worksheet section or runbook branch.

### Checkpoint C1 -- role confirmation
- **Deliverable:** operator response to
  `../classification_worksheet.md` Section 1 questions 1-4, logged in
  that worksheet with the operator's name, role, and date.
- **Accepts:** one of `pms`, `gl`, `crm`, `reporting_feed`,
  `legacy_historical`, `other_sop_policy`.
- **Blocker:** if the operator cannot answer within one review cycle,
  the placeholder remains at `stub` and all `gs_*` DQ rules stay at
  `severity: warning`.

### Checkpoint C2 -- access path declaration
- **Deliverable:** operator response to Section 2 questions 5-9,
  including cadence, latency, and credentialing contact.
- **Accepts:** one of `api`, `sftp`, `export`, `portal`, `unknown`.
- **Blocker:** `unknown` or `portal` blocks advancement.

### Checkpoint C3 -- content shape disclosure
- **Deliverable:** operator response to Section 3 questions 10-13,
  accompanied by two to three sanitized sample records illustrating the
  shape (no real PII, no real financial values, no real vendor ids).
- **Accepts:** a shape description concrete enough to replace
  `../provisional_source_contract.yaml` with a real source contract.
- **Blocker:** missing samples or sensitivity-review failure blocks
  advancement.

### Checkpoint C4 -- sensitivity triage
- **Deliverable:** operator response to Section 4 questions 14-18
  plus the sign-off chain for any `resident_pii`, `financial`, or
  `legal` branch that fired.
- **Accepts:** explicit sensitivity classification and named sign-off
  contacts.
- **Blocker:** missing sign-off blocks live-sample ingestion.

### Checkpoint C5 -- workflow dependency confirmation
- **Deliverable:** operator response to Section 5 questions 19-22;
  updated `../workflow_relevance_map.yaml` where a candidate dependency
  is confirmed or retired.
- **Accepts:** for each candidate workflow, a status in
  `{confirmed_primary, confirmed_secondary, retired_candidate}`.
- **Blocker:** at least one confirmed dependency must exist, or the
  adapter is retired rather than forked.

### Checkpoint C6 -- source-of-truth matrix update
- **Deliverable:** a pull request to
  `../../../../_core/stack_wave4/source_of_truth_matrix.md` that adds
  the GraySail row with explicit primary / secondary / fallback for
  every canonical object GraySail touches, and a disagreement
  resolution rule per row.
- **Accepts:** matrix row reviewed by data_platform_team +
  asset_mgmt_director + (finance_reporting if GL branch,
  compliance_risk if CRM or sensitivity branch).
- **Blocker:** matrix conflict without a resolution rule blocks
  advancement.

### Checkpoint C7 -- rollout-wave sequencing
- **Deliverable:** confirmed rollout wave in
  `../../../../_core/stack_wave4/stack_rollout_wave4.md`, with explicit
  dependency on earlier waves and explicit gating DQ rules.
- **Accepts:** a wave slot not earlier than Wave 4C per
  `../bounded_assumptions.yaml::rollout_wave_gated`.
- **Blocker:** attempts to promote earlier than Wave 4C without full
  classification are rejected.

### Checkpoint C8 -- adapter fork and rename
- **Deliverable:** a new adapter directory
  `reference/connectors/adapters/graysail_<role>_<pattern>/` populated
  with the real source contract, starter-stage tests, DQ rules with
  concrete `severity: blocker` replacing the `warning` placeholders,
  and a forked source_registry entry.
- **Accepts:** the forked adapter passes
  `run_adapter_manifest_checks` at status `starter`, carries
  `example_raw_payload.jsonl`, `normalized_output_example.jsonl`, and
  `mapping_template.yaml`.
- **Blocker:** C1-C7 must all close before C8 begins.

## Closure rule

When all eight checkpoints close:

1. Fork this adapter into `graysail_<role>_<pattern>`. Preserve the
   placeholder directory as the classification trail; mark it
   `deprecated` with `replacement_adapter_id` in `deprecation_metadata`.
2. Advance the forked adapter's `status` from `stub` to `starter`.
3. Retire every `gs_*` DQ rule whose deferred-mode concern has been
   answered; replace with concrete per-object rules under the forked
   adapter's `dq_rules.yaml`.
4. Update `../../../../_core/stack_wave4/source_of_truth_matrix.md` to
   remove the "GraySail row deferred" open item.
5. Retire `blocked_pending_classification` from every workflow in
   `workflow_activation_additions.yaml` and replace with the confirmed
   `role` and activation rules.

When closed, fork this adapter into `graysail_<role>_<pattern>` and
advance status to starter.

## Until closure

- Every `gs_*` DQ rule stays at `severity: warning`.
- Every workflow reference stays `blocked_pending_classification`.
- Every `classification_pending` field in
  `../provisional_source_contract.yaml` stays flagged.
- The source-of-truth matrix row stays deferred.
- The placeholder directory is the only GraySail surface in the
  subsystem.
