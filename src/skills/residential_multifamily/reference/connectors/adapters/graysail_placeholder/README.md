# GraySail Placeholder Adapter

Adapter id: `graysail_placeholder`
Vendor family: `graysail_family`
Connector domain: `manual_uploads` (bounded fallback — see `bounded_assumptions.yaml`)
Status: `stub` (wave_4_gated, classification pending)

## Why this is a placeholder, not a full adapter

The user instruction was: treat GraySail as required in scope, but do not guess
its role. This adapter therefore locks in the repo-evidenced classification
(SOP / policy knowledge store) while refusing to commit to a technical shape
the repo does not yet support.

## Evidence found in the repo

No file inside `src/skills/residential_multifamily/` references GraySail. The
subsystem's source_registry, master_data, connector contracts, workflows,
runbooks, schemas, and tests are GraySail-silent.

GraySail is referenced only in external architecture documents outside the
repo (under `~/Downloads/`). Those documents are consistent:

- Listed as one of five systems of record: AppFolio, Dealpath, Procore, Sage
  Intacct, GraySail.
- Characterized as the holder of "SOPs" / internal operating policies.
- Named as the primary tool for the proposed "SOP / Workflow Guidance Agent"
  (role-aware policy search and retrieval).
- Cited as a knowledge source for a company-wide operating playbook.

The external documents do NOT specify: API availability, export shape (file
vs. structured extract), canonical-object coverage, sensitivity tier,
integration mode, credential method, or cadence.

## Classification decision

**Role (confidence medium-high):** SOP / policy knowledge store and
retrieval corpus. Evidence is consistent across multiple external documents
and aligns with a plausible class of system (policy-management SaaS or
internal knowledge platform).

**Technical shape (confidence low):** Undetermined. Treated as
`manual_uploads` domain as the safest-fallback so the adapter can exist
inside the canonical domain enum without implying API or SFTP access the
repo has not observed.

**Status:** `placeholder_pending_clarification`. Implemented as a
`connector_domain: manual_uploads` stub per the adapter manifest schema,
which does not carry a `placeholder_pending_clarification` enum value. The
placeholder intent is captured in `rollout_wave: wave_4_gated`, in the
manifest description, in `classification_worksheet.md`, and in
`bounded_assumptions.yaml`.

## Why the decision is provisional

Four concrete unknowns gate this adapter:

1. **Access mode.** Is GraySail exposed via API, SFTP, email export, shared
   drive, or only through its own UI? Each answer changes the adapter shape.
2. **Content type.** Does GraySail export structured records (vendor
   directory, service-level definitions, approval-matrix rows) or only
   unstructured documents (PDF / HTML / Markdown SOPs)? Each answer changes
   whether canonical mapping is even applicable.
3. **System-of-record scope.** Does GraySail claim authority over any
   operating object already owned by AppFolio, Dealpath, Procore, or Sage
   Intacct? If yes, the source-of-truth matrix (see
   `../../../_core/stack_wave4/source_of_truth_matrix.md`) must be extended.
4. **Sensitivity posture.** Does any GraySail content contain resident PII,
   employee PII, vendor tax ids, contract dollar values, or legal-strategy
   language? Each answer changes the `pii_classification`,
   `financial_sensitivity`, and `legal_sensitivity` tags required in the
   `source_registry.yaml` entry.

## Most likely GraySail roles and adapter impact

Ranked by plausibility given the repo-external evidence.

| Candidate role | Plausibility | Adapter impact if confirmed |
|---|---|---|
| SOP / policy knowledge store (retrieval corpus for workflow guidance) | high | Adapter forks into `graysail_sop_store` under `manual_uploads` or into a new `knowledge_source` domain once the canonical ontology supports it. Primary output is a document index, not operating records. |
| Policy and approval-matrix repository (structured approval definitions) | medium | Adapter forks into `graysail_approval_policies`; feeds `_core/approval_matrix.md` comparison checks but does not mutate canonical; reconciliation against declared approval matrix becomes a new check. |
| Vendor SOP / service-level catalog (standard service categories, SLAs, scope documents) | medium | Adapter forks into `graysail_service_catalog` under `ap`; feeds vendor-side SLA definitions into `vendor_dispatch_sla_review`. |
| Training / onboarding document library (role-based playbooks) | low-medium | Adapter remains under `manual_uploads`; primary consumer is role-based onboarding workflows (not currently in canonical 27). |
| Project / data aggregator across AppFolio / Dealpath / Procore / Sage Intacct | low | If confirmed, this is a SECONDARY adapter that overlays existing primary adapters; reconciliation rules must treat GraySail as a DERIVED source and defer to primary systems on disagreement. |

In every scenario, the canonical subsystem base is immutable. The adapter
never writes to canonical metrics or ontology. Any classification that
requires a new canonical object (e.g., `SopRecord`, `PolicyDocument`,
`ApprovalMatrixRow`) is surfaced as an open question in
`../../../_core/stack_wave4/open_questions_and_risks.md`; this adapter
cannot introduce canonical objects on its own.

## Required follow-up evidence

Needed before the placeholder can advance past `stub`:

- **User documentation from the operator.** One-paragraph description of
  what GraySail is, who uses it, and what types of content it holds. See
  `classification_worksheet.md` question bank.
- **Two or three sanitized sample exports.** Enough to see shape and
  sensitivity tier. No real PII. No real vendor identifiers. No real
  contract dollar amounts in prose.
- **Workflow confirmation.** Which canonical workflows (from
  `../../../../../workflows/`) depend on GraySail content today, implicitly
  or explicitly? Answer feeds `workflow_relevance_map.yaml`.
- **Access pathway.** Does the operator expect to ingest GraySail via API,
  SFTP, shared drive, email drop, or manual upload? Answer feeds the
  `ingestion_mode` field in `source_registry_entry.yaml`.
- **System-of-record claim.** Does GraySail ever override a claim made by
  AppFolio / Dealpath / Procore / Sage Intacct? Answer feeds the
  source-of-truth matrix.
- **Classification sensitivity triage.** Operator assessment of PII,
  financial, and legal sensitivity of GraySail content; cannot be inferred
  from the placeholder.

## Blocked fields

Fields that cannot be populated until classification is confirmed. Each is
documented here so any future fork preserves the block list rather than
guessing.

- `source_registry.yaml::ingestion_mode` — blocked.
- `source_registry.yaml::cadence` — blocked.
- `source_registry.yaml::credential_method` — held at `none` as a
  placeholder, not a commitment.
- `source_registry.yaml::object_coverage` — held at a single placeholder
  slug pending ontology extension; see `source_registry_entry.yaml`.
- `source_registry.yaml::pii_classification` — blocked.
- `source_registry.yaml::financial_sensitivity` — blocked.
- `source_registry.yaml::legal_sensitivity` — blocked.
- `source_registry.yaml::expected_latency_minutes` — blocked.
- canonical-object mapping across every entity under
  `../../pms/`, `../../gl/`, `../../crm/`, `../../ap/`,
  `../../market_data/`, `../../construction/`, `../../hr_payroll/`,
  `../../manual_uploads/` — blocked. This adapter maps no canonical
  operating objects.

## Non-destructive integration stub design

This adapter is deliberately inert. Concretely:

- Reads nothing from GraySail. The adapter carries no credentials, no
  endpoint configuration, and no fetch logic.
- Writes nothing to the canonical normalized layer. No reconciliation check,
  derived metric, or workflow activation rule reads this adapter.
- Logs only what was attempted. If a future fork adds a live fetch path,
  the fetch attempt and its outcome are logged through the standard
  integration audit trail (see `../../_core/lineage.md`); no side effects
  flow into canonical data structures.
- Carries sample files that are obviously synthetic. Sample filenames and
  contents use `sample_` and `placeholder_` prefixes and the `status:
  sample` status tag per the stub-stage invariants.
- Does not appear in `vendor_family_registry.yaml` active listings until
  classification is confirmed. The registry fragment in
  `source_registry_entry.yaml` is a proposal, not a commitment.

## Files in this directory

```
manifest.yaml                      <- adapter manifest (schema-conformant stub)
README.md                          <- this file
classification_worksheet.md        <- operator interview for classification
bounded_assumptions.yaml           <- explicit assumptions, blast radius, remediation
provisional_source_contract.yaml   <- abstract placeholder shapes
workflow_relevance_map.yaml        <- candidate workflow dependencies, blocked-until-classified
blocked_workflows.md               <- what degrades and how until classified
dq_rules.yaml                      <- minimal DQ surface (no content-level rules)
source_registry_entry.yaml         <- fragment, status placeholder_pending_clarification
example_raw_payload.jsonl          <- synthetic placeholder payload (stub-stage test harness)
normalized_output_example.jsonl    <- synthetic placeholder canonical shape
mapping_template.yaml              <- scaffold, status_tag: template
runbooks/
  graysail_classification_path.md  <- how to convert placeholder into active adapter
  graysail_ambiguity_handling.md   <- what to do while awaiting classification
tests/
  test_adapter.py                  <- placeholder-structure tests, no data hallucination
```

## Quality bar

- Status: `stub`. No live credentials.
- Every sample record carries `status: sample`.
- No real SOP content, no real policy language, no real contract language.
- No hardcoded numeric thresholds in prose; the adapter does not introduce
  any thresholds.
- Canonical subsystem wins on every conflict; this placeholder never
  overrides a canonical claim.
- No canonical ontology extension is introduced by this placeholder. Any
  need for one is surfaced as an open question in the wave-4 cross-cutting
  docs.
