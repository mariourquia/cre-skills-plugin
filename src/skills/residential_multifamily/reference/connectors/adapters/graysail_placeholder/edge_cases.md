# GraySail Placeholder: Edge Cases

Status: deferred_until_classification_closes
Owner: data_platform_team
Audience: data platform operators, asset management operators, compliance reviewers.

## Purpose

This file catalogs the edge cases that can arise while `graysail_placeholder`
is still a `stub`. Each edge case describes a failure mode, the safe posture
the adapter takes today, and the path out via
`runbooks/graysail_classification_path.md`.

No edge case below may be resolved in the placeholder itself. Every
resolution routes through the classification runbook checkpoints
(C1-C8) and the eventual fork into `graysail_<role>_<pattern>`.

## EC-1 -- Classification not closed but operator wants to onboard

**Scenario.** An operator requests live-data onboarding of GraySail
before the classification worksheet is filled out and the classification
path runbook is closed.

**Safe posture today.**
- `manifest.yaml::status` stays `stub`.
- `source_registry_entry.yaml::credential_method` stays `none`.
- No adapter code attempts a fetch.
- `dq_rules.yaml::gs_classification_pending_blocker` fires at
  `severity: warning`, surfacing the gap in the monitoring surface.

**Path out.**
- Do **not** bypass the worksheet. Return the request to the operator
  with a pointer to `classification_worksheet.md` Sections 1-5.
- Track the request as an inbound classification-pending item;
  aggregate into the quarterly review declared in
  `bounded_assumptions.yaml::review_cadence`.

**Do not.** Do not sideload a credentialed connection in the placeholder
directory. Do not create a "temporary" fetch path. Do not override
`credential_method` in a local config.

## EC-2 -- GraySail referenced by workflow but not classified

**Scenario.** A canonical workflow in `workflows/` (or a proposed
workflow under review) mentions GraySail in its design as if it were an
active source. `workflow_relevance_map.yaml::candidate_dependencies`
lists the workflow but it has not been confirmed through Checkpoint C5.

**Safe posture today.**
- The workflow activation fragment in
  `workflow_activation_additions.yaml` holds
  `partial_mode_behavior: blocked_pending_classification` for every
  listed workflow.
- `dq_rules.yaml::gs_workflow_dependency_blocked` fires when any
  workflow attempts to resolve GraySail as primary or secondary.
- The workflow runs its canonical fallback (declared in
  `workflow_relevance_map.yaml::fallback_if_graysail_absent`); no
  degradation occurs because GraySail is not required.

**Path out.**
- Close Checkpoint C5 in `runbooks/graysail_classification_path.md`.
- For each candidate workflow, declare the status as
  `confirmed_primary`, `confirmed_secondary`, or
  `retired_candidate`.
- Update `workflow_activation_additions.yaml` with the confirmed role
  before retiring `blocked_pending_classification`.

**Do not.** Do not allow a canonical workflow design document to treat
GraySail as primary without a matching Checkpoint C5 close. A mismatch
between workflow design and the classification path is itself a
compliance finding.

## EC-3 -- GraySail data referenced post-acquisition

**Scenario.** An acquisition closes on a property set that the seller's
operations team used GraySail for. The incoming data set includes
GraySail-origin records, but the buyer has not yet run classification
against its own GraySail instance (or the seller did not use one).

**Safe posture today.**
- Incoming GraySail rows land in `manual_uploads` per the fallback
  domain posture in `bounded_assumptions.yaml::domain_fallback_manual_uploads`.
- Rows carry `status: sample` and flow through the generic
  `manual_uploads` ingestion surface; they are **not** attributed to
  the placeholder adapter.
- No canonical workflow reads the rows because
  `gs_classification_pending_blocker` is firing.

**Path out.**
- If the buyer intends to continue using GraySail for the acquired
  property set, advance classification per Checkpoint C3 (operating
  pattern: `subset`) and Checkpoint C6 (source-of-truth matrix update
  scoped to the acquired property set).
- If the buyer intends to migrate off GraySail, treat the incoming
  rows as `legacy_historical` (Step 1 branch) and declare the cutover
  date in the forked adapter's `source_registry_entry.yaml`.

**Do not.** Do not commingle GraySail-origin rows with AppFolio /
Intacct / Procore / Dealpath-origin rows without the GraySail row in
the source-of-truth matrix declaring the survivorship rule.

## EC-4 -- GraySail used as historical-only without operator confirmation

**Scenario.** An operator asserts that GraySail is only a historical
read source for pre-cutover data, so classification can be skipped. The
operator has not filled out Section 1 question 4 (transactional vs.
reference vs. document) or provided a cutover date.

**Safe posture today.**
- The placeholder remains `stub`. Historical-only status is a Step 1
  branch (`legacy_historical`), not an exemption from classification.
- `gs_classification_pending_blocker` continues to fire.
- No DQ rule relaxation is permitted because the cutover-date
  invariant is not yet declared.

**Path out.**
- Close Checkpoint C1 with the explicit `legacy_historical` branch
  selected in `classification_worksheet.md` Section 1 question 4.
- Close Checkpoint C3 by declaring the cutover date and requiring the
  invariant `row.as_of_date < cutover_date` on every historical row.
- Close Checkpoint C6 with a source-of-truth matrix row that sets
  GraySail as `audit_only` for every canonical object with an explicit
  cutover-date cutoff.

**Do not.** Do not let "historical-only" act as a classification
shortcut. The historical-only branch still requires a source-of-truth
matrix row, a cutover-date invariant, and operator sign-off.

## EC-5 -- GraySail vendor master overlap with AppFolio / Intacct / Procore unconfirmed

**Scenario.** Operator documentation suggests GraySail may hold a
vendor-service-catalog or approval-matrix fragment. The five confirmed
systems already have partial vendor coverage: AppFolio (service
dispatch), Intacct (tax id / AP primary), Procore (construction
commitments). Whether GraySail authoritatively adds vendor rows or
merely describes vendor behavior is unknown.

**Safe posture today.**
- `dq_rules.yaml::gs_overlap_with_other_sources_unmonitored` fires,
  surfacing that vendor-master overlap is not monitored.
- No vendor row is attributed to GraySail in
  `source_of_truth_matrix.md`. AppFolio + Intacct + Procore retain the
  three-way vendor reconciliation rule as declared.
- The candidate workflow `vendor_dispatch_sla_review` in
  `workflow_relevance_map.yaml` is blocked_until_classified.

**Path out.**
- Close Checkpoint C1 with Step 1 role = `other` (service catalog /
  approval-matrix) or `reporting_feed` (read-only overlay).
- Close Checkpoint C6 with source-of-truth matrix rows for any
  canonical vendor-adjacent object GraySail touches; the default
  posture is `audit_only` or `secondary`, never primary, unless the
  operator explicitly demotes AppFolio / Intacct / Procore.
- Declare reconciliation tolerance bands citing
  `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
  for every field GraySail contests.

**Do not.** Do not add a GraySail vendor row to canonical without the
three-way reconciliation rule being revised in the source-of-truth
matrix. Silent vendor-master overlap is the failure mode this edge case
exists to prevent.

## EC-6 -- Multi-instance GraySail across portfolio segments

**Scenario.** The operator runs two GraySail instances: one for a
conventional-multifamily segment, one for an affordable-housing
segment. The two instances may carry different SOP sets, different
approval matrices, or different data shapes.

**Safe posture today.**
- The placeholder adapter is singular; it does not differentiate
  instances.
- `classification_worksheet.md` Section 6 question 25 asks about
  instance architecture but is informational for Wave 4C sequencing.
- No instance-specific configuration is accepted in the placeholder.

**Path out.**
- Close Checkpoint C3 with the operating pattern set to `subset` per
  Step 3 of the classification path.
- For each instance, fork a separate adapter:
  `graysail_<role>_subset_conventional`,
  `graysail_<role>_subset_affordable`. Do not try to multiplex two
  instances inside a single forked adapter.
- Declare `applicable_property_set` on each forked adapter's
  `source_registry_entry.yaml`.
- If the affordable instance carries regulatory-program content,
  route through the `overlays/regulatory/` interaction check declared
  in `classification_worksheet.md` Section 4 question 16 and require
  compliance_risk sign-off.

**Do not.** Do not treat two GraySail instances as interchangeable
sources of the same canonical row. A property in the conventional set
must not receive data from the affordable-segment GraySail instance and
vice versa.

## EC-7 -- GraySail-only properties during cutover

**Scenario.** During a GraySail migration (either onto or off of
GraySail), a subset of properties is served only by GraySail while the
rest use another system. For the GraySail-only subset, AppFolio /
Intacct / Procore have no rows, so the source-of-truth matrix's fallback
chain (e.g., `intacct -> appfolio`) cannot resolve.

**Safe posture today.**
- The placeholder remains `stub`; no row is written to canonical.
- `gs_workflow_dependency_blocked` and
  `gs_overlap_with_other_sources_unmonitored` both fire.
- Workflows for the GraySail-only property subset run in
  `blocked_pending_classification` and defer to the canonical fallback
  declared in `workflow_relevance_map.yaml`.

**Path out.**
- Close Checkpoint C3 with the operating pattern set to
  `legacy_parallel` (if migration is in flight) or `subset` (if the
  GraySail-only subset is steady-state).
- Declare the cutover date per property in the forked adapter's
  `source_registry_entry.yaml::cutover_schedule` (new field introduced
  only in the fork, never here).
- Close Checkpoint C6 with source-of-truth matrix rows scoped to the
  applicable property set; confirm the survivorship rule for each
  canonical object during the cutover window.
- Add dual-run reconciliation citing
  `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
  until the cutover closes.

**Do not.** Do not advance the adapter to `starter` while any
GraySail-only property set lacks a cutover schedule. Mid-cutover
silence is a common contamination path.

## EC-8 -- GraySail claims system-of-record on an object AppFolio / Intacct / Procore / Dealpath already owns

**Scenario.** Classification reveals that GraySail authoritatively
holds a canonical operating object that one of the five confirmed
systems already owns. Example: GraySail claims primary authority on
`approval_matrix_row`, which `_core/approval_matrix.md` currently owns.

**Safe posture today.**
- The placeholder asserts `no_canonical_object_coverage` per
  `bounded_assumptions.yaml::no_canonical_object_coverage`.
- The conflict cannot surface in canonical workflows because no
  GraySail-authoritative row exists today.

**Path out.**
- Close Checkpoint C1 with the conflict named.
- Run Checkpoint C6 as a high-risk branch: the source-of-truth matrix
  rewrite requires finance_reporting + compliance_risk +
  asset_mgmt_director sign-off, not just data_platform_team.
- Declare the disagreement-resolution rule explicitly in the matrix
  row. Default posture: the confirmed system remains primary; GraySail
  becomes secondary with reconciliation commentary within tolerance
  band citing
  `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
- If the operator insists GraySail must override, route the change
  through canonical change-control per
  `../../../../_core/stack_wave4/open_questions_and_risks.md`. Do not
  handle the override inside the adapter layer.

**Do not.** Do not let a forked GraySail adapter silently overwrite an
AppFolio / Intacct / Procore / Dealpath row. Every conflict is
surfaced; canonical wins by default.

## EC-9 -- Sensitivity tier reclassification after samples land

**Scenario.** Sample records collected during Checkpoint C3 reveal
higher sensitivity than the operator declared in Section 4 (e.g.,
operator said "financial: none" but a sample carries a vendor tax id,
or operator said "no resident PII" but a sample carries a resident name
in SOP narrative).

**Safe posture today.**
- This edge case is pre-gated: samples are not permitted to land until
  Checkpoint C4 closes with the operator's sensitivity declaration.
- If samples arrive ahead of C4, they are quarantined and the adapter
  remains `stub`.

**Path out.**
- Halt sample ingestion.
- Return to Checkpoint C4 with the revised sensitivity tier.
- Obtain the revised sign-off chain (compliance_risk if PII,
  finance_reporting if financial).
- Update `bounded_assumptions.yaml::confidentiality_posture_unknown`
  remediation path in the forked adapter to reflect the confirmed
  posture.
- Quarantined samples are destroyed per the subsystem's sample-disposal
  procedure; they are not retained in the adapter directory.

**Do not.** Do not attempt to redact or sanitize the quarantined
samples in place. Sanitization is a separate workflow with its own
sign-off chain; conflating it with sample intake is itself a
compliance finding.

## EC-10 -- Operator abandons classification mid-path

**Scenario.** Checkpoints C1-C4 close, but the operator stalls on C5
(workflow dependency confirmation) or C6 (source-of-truth matrix
update). Months pass. The adapter is partially classified but cannot
fork.

**Safe posture today.**
- The adapter remains `stub`. Partial classification does not advance
  it.
- Every `gs_*` rule stays at `severity: warning`.
- Every candidate workflow stays
  `blocked_pending_classification`.
- The "GraySail row deferred" open item in
  `../../../../_core/stack_wave4/source_of_truth_matrix.md` remains.

**Path out.**
- Escalate to the accountability chain declared in
  `bounded_assumptions.yaml::accountability_chain`
  (`data_platform_team -> executive`).
- Set a classification-abandonment decision point: if the operator
  cannot close C5 or C6 within two quarterly review cycles, retire
  the adapter. Retirement:
  - Mark `manifest.yaml::status` as `deprecated` with
    `deprecation_metadata.replacement_adapter_id: none`.
  - Preserve the placeholder directory as the classification trail.
  - Update `source_of_truth_matrix.md` to remove the deferred row and
    replace it with an explicit "GraySail not in scope" note.

**Do not.** Do not let partial classification grant partial activation.
Partial-state activation is the failure mode that the
`gs_classification_pending_blocker` master gate exists to prevent.

## Cross-references

- `classification_worksheet.md` -- operator question bank
- `runbooks/graysail_classification_path.md` -- decision tree and
  checkpoints
- `dq_rules.yaml` -- deferred-mode DQ rules firing while this adapter
  is a stub
- `workflow_relevance_map.yaml` -- candidate workflow dependencies
- `workflow_activation_additions.yaml` -- partial-mode behavior on each
  candidate workflow
- `bounded_assumptions.yaml` -- the assumptions this adapter runs under
- `../../../../_core/stack_wave4/source_of_truth_matrix.md` -- the
  canonical matrix GraySail must land in before forking
- `../../../../_core/stack_wave4/open_questions_and_risks.md` --
  canonical change-control entries for ontology / workflow extensions
