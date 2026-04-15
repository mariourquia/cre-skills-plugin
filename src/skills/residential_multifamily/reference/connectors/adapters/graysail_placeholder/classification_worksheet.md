# GraySail Classification Worksheet

Purpose: structured operator interview to finalize GraySail's classification.
Answers feed `manifest.yaml`, `source_registry_entry.yaml`,
`workflow_relevance_map.yaml`, and the source-of-truth matrix under
`../../../_core/stack_wave4/source_of_truth_matrix.md`.

Until every required question is answered, this adapter remains a stub and
workflows must not hard-depend on GraySail output. See
`runbooks/graysail_ambiguity_handling.md` for interim posture.

## Section 1: role and scope

1. In one or two sentences, what is GraySail used for at the operator?
   Pick the closest description or write your own:
   - `sop_and_policy_knowledge_store`
   - `approval_matrix_and_governance_policies`
   - `vendor_service_catalog_and_slas`
   - `training_and_onboarding_playbooks`
   - `project_or_data_aggregator_across_other_systems`
   - `other` (describe)

2. Which of the five systems of record does GraySail overlap with, if any?
   Multi-select: AppFolio, Dealpath, Procore, Sage Intacct, none.

3. Does GraySail claim authority (system-of-record status) for any
   operational object today? If yes, name the objects (e.g.,
   `approval_matrix_row`, `service_category`, `vendor_agreement`).

4. Is GraySail a transactional system, a reference data store, or a
   document / knowledge store? Pick one. If mixed, describe the mix.

## Section 2: access and ingestion

5. How does the operator currently pull data out of GraySail?
   - API (REST, GraphQL, other)
   - SFTP scheduled export
   - Shared-drive dump
   - Email drop
   - Manual export from the GraySail UI
   - No extraction today; consumed only inside the GraySail UI

6. If an API is available, is an OAuth / API-key method documented? If
   yes, who is the operator contact for credentialing?

7. What cadence is realistic for data refresh?
   - real-time, hourly, daily, weekly, monthly, quarterly, on_demand.

8. What latency (from source update to arrival in operator's ingestion
   surface) is acceptable? Minutes.

9. Does GraySail expose a document diff / change-log view? Answer
   (yes / no) feeds schema drift detection strategy in `dq_rules.yaml`.

## Section 3: content type and shape

10. Are GraySail records documents (PDF, DOCX, HTML, Markdown, wiki
    pages) or structured records (JSON, CSV, database rows)? If mixed,
    describe the split.

11. Do GraySail records reference canonical operating objects the
    subsystem already owns (Property, Lease, Vendor, CapexProject,
    Workflow, etc.)? If yes, how are those references encoded (property
    id, vendor id, role slug, workflow slug, free-form prose)?

12. Does GraySail retain version history? How is the active version
    identified (effective-date, version number, status tag)?

13. How are SOPs tagged for audience (executive, regional_ops,
    asset_mgmt, finance_reporting, development, construction,
    compliance_risk, site_ops)? Tagging model feeds the 8-audience
    routing.

## Section 4: sensitivity and governance

14. Does GraySail content contain resident PII, employee PII, or
    contractor PII? If yes, which fields?

15. Does GraySail content contain contract dollar values, margin data,
    fee schedules, or vendor tax ids? If yes, what is the current
    sensitivity classification internally?

16. Does GraySail content contain regulatory-program instructions
    (affordable housing, fair-housing guidance, HUD/LIHTC policy)?
    Answer feeds the `overlays/regulatory/` interaction check.

17. Who at the operator owns the GraySail content? (data_owner,
    business_owner, technical_owner role labels.)

18. What sign-off posture is expected before GraySail content is used
    by a workflow? Specifically, is finance_reporting, compliance_risk,
    or site_ops sign-off required?

## Section 5: workflow dependencies

19. Which of the 27 canonical workflows in `../../../../../workflows/`
    currently reference GraySail content implicitly (through operator
    habit or training) or explicitly (through written procedure)?
    Answer feeds `workflow_relevance_map.yaml`.

20. Is there a proposed new workflow that would exist ONLY because
    GraySail exists? For example, a `sop_guidance_lookup` workflow, a
    `policy_exception_review` workflow, or a `role_onboarding` workflow.
    If yes, describe.

21. Does any workflow currently treat GraySail as its authoritative
    source for a metric, threshold, approval rule, or SLA? If yes, which
    workflow and which value?

22. Are there known workflows that would break (or degrade) if GraySail
    became unavailable for a cadence window? Answer feeds
    `blocked_workflows.md`.

## Section 6: integration footprint

23. Does GraySail produce data that feeds another system (AppFolio,
    Dealpath, Procore, Sage Intacct, manual spreadsheets)? If yes, is
    the flow bidirectional?

24. Does GraySail consume data from any of the other systems of record?
    If yes, which and how (API pull, manual copy, email)?

25. Is GraySail under active roadmap change at the operator (replacement,
    migration, retirement)? Answer feeds `rollout_wave` sizing.

## Scoring summary

Complete answers to Sections 1, 2, 3, and 5 are required before the
adapter can advance from `stub` to `starter`. Section 4 is required
before any live-data sample is accepted. Section 6 is informational for
rollout-wave assignment.

Until Sections 1-5 are complete, the adapter stays at `stub` and its
workflows remain `blocked_until_classified`. See
`runbooks/graysail_classification_path.md` for the fork-and-rename flow
that runs once the worksheet is complete.
