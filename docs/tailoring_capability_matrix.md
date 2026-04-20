# Tailoring Capability Matrix

Published with the internal-beta release. Describes what the tailoring subsystem (at `src/skills/residential_multifamily/tailoring/`) **actually does today** vs. what governance docs (`AUDIENCE_MAP.md`, `DIFF_APPROVAL_PREVIEW.md`, `PREVIEW_PROTOCOL.md`, `MISSING_DOC_MATRIX.md`) describe as the full target behavior.

Per claim, the matrix gives a status and points at the code path + test that proves it.

| # | Claim | Governance source | Status | Runtime path | Test coverage |
|---|---|---|---|---|---|
| 1 | Audience selection — a user's role drives which question banks are presented | `AUDIENCE_MAP.md` (8-audience split) | **Partial** | `tailoring_tui.py::load_question_banks()` loads all banks; does not filter by role. 11 YAML banks on disk (8 new: executive, regional_ops, asset_mgmt, finance_reporting, development, construction, compliance_risk, site_ops; 3 legacy retained: coo, cfo, reporting). | `test_tailoring_tui.py::QuestionBankLoadingTests` (all banks load; role-based filtering not asserted) |
| 2 | Conflict surfacing — when two audiences answer the same overlay key with different values, both answers are visible in the diff preview | `DIFF_APPROVAL_PREVIEW.md` §3, §7 refusal condition 7 | **Proven** (2026-04) | `tailoring_tui.py::compute_diff()` now records every non-chosen usable source on `DiffEntry.conflicting_sources` and sets `has_conflict=True` when answers disagree. Earlier version silently kept only the first source. | `test_tailoring_tui.py::ConflictSurfacingTests` (3 tests: agreement, disagreement, lone-source) |
| 3 | Deterministic preview order — diff entries render in stable alphabetical order by overlay key | `PREVIEW_PROTOCOL.md` rule 4 | **Proven** | `compute_diff()` iterates `sorted(target_to_questions.items())`. | Asserted implicitly by `DiffComputationTests` (added / modified / unchanged tests depend on deterministic ordering) |
| 4 | Preview bundle written to disk as YAML at `tailoring/sessions/{org_id}/{session_id}__preview.yaml` | `DIFF_APPROVAL_PREVIEW.md` line 16-17 | **Implemented (v4.3)** | `tailoring_tui.py::emit_preview_bundle()` renders YAML with session / diff_summary / diff_entries / proposed_overlay / guard_violations sections. Writing the file from `_finalize()` is wired in v4.3-pass2. | `PreviewBundleTests::test_preview_contains_required_sections` |
| 5 | Approval-floor check — a tailoring answer cannot lower an approval threshold below the canonical floor in `_core/approval_matrix.md` | `DIFF_APPROVAL_PREVIEW.md` §5, §7 refusal condition 2 | **Implemented (v4.3)** | `tailoring_tui.py::guard_approval_floor_not_lowered()` compares numeric approval-threshold paths in proposed overlay against current; refuses if any drop. Raising a floor is permitted. | `ApprovalFloorGuardTests` (3 tests: lower refused, raise allowed, add permitted) |
| 6 | Canonical-definition redefinition refusal — a tailoring answer targeting a frozen metric field (e.g. `_core/metrics.yaml#economic_occupancy.numerator`) is refused with a `REDEFINITION_ATTEMPT` marker | `DIFF_APPROVAL_PREVIEW.md` §2, §7 refusal condition 1 | **Implemented (v4.3)** | `tailoring_tui.py::guard_no_canonical_redefinition()` parses `_core/ontology.md` and `_core/metrics.md` headers, refuses any proposed-overlay key at canonical scope that carries a `redefinition` or `rename` directive. | `CanonicalRedefinitionGuardTests` (2 tests) |
| 7 | Missing-doc blocker — a p1 document that remains missing past the blocker threshold refuses to render a dependent preview | `MISSING_DOC_MATRIX.md` §"Blocker criteria" (lines 117-124) | **Implemented (v4.3)** | `tailoring_tui.py::guard_missing_doc_blockers()` walks every question-bank trigger and refuses if any references a `doc_catalog.yaml` slug with no entry. Tolerates both string and dict trigger shapes. | `MissingDocBlockerGuardTests` (2 tests: missing refused, known slug passes) |
| 8 | Version-drift detection — a tailoring session against a stale base snapshot is flagged | `customization-guide.md` §Health Check | **Not applicable** | The `Health Check` system applies to the skill-customization subsystem (`lib/customization.mjs`), not to org-overlay tailoring. Marked here so reviewers do not look for it in the wrong place. | n/a |
| 9 | 8-audience architecture fully deployed — legacy banks (`coo.yaml`, `cfo.yaml`, `reporting.yaml`) are retired | `AUDIENCE_MAP.md` §Retirement | **Partial** | The three legacy banks are still present on disk and still loaded. `AUDIENCE_MAP.md` documents the legacy-retention window. No code path filters or emits a deprecation warning. | None of the TUI tests check that legacy banks no longer load. |
| 10 | Missing-doc catalog integrity — every `missing_doc_triggers[*].doc_slug` in a question bank resolves to a `doc_catalog.yaml` entry | `MISSING_DOC_MATRIX.md`, inferred from test | **Proven** (2026-04) | Added 16 doc entries to `doc_catalog.yaml` for the new audiences (compliance_risk, executive, finance_reporting, site_ops). Previously 24 doc_slugs were referenced but not cataloged. | `DocCatalogTests::test_missing_doc_triggers_resolve_to_catalog` (passes; used to fail) |

## Interpretation

- Claims marked **Proven** have a runtime code path and a test that exercises it on `main`.
- Claims marked **Partial** have some runtime behavior but the governance doc describes more. The README [Known Limitations](../README.md#known-limitations) section lists these as caveats.
- Claims marked **Not implemented** are governance-only at this point. The docs remain as the forward spec; they are not a current-behavior promise. Do not rely on them.

## Deliberate next steps (tracked but not done in this pass)

Tailoring Pass 2 Objective 4 is **closed as of v4.3**. Claims 4, 5, 6, and
7 (preview-bundle emission, approval-floor guard, canonical-redefinition
refusal, missing-doc blocker) are all Implemented, with tests listed in
the matrix above. Remaining items are open follow-ups that are intentionally
scoped outside Obj 4:

1. **Legacy bank retirement** (claim 9) — emit a warning when a legacy bank
   is loaded; remove legacy banks once all orgs have migrated. Test:
   legacy-bank load path emits the warning. Status: **Partial** (banks
   retained for the legacy-retention window per `AUDIENCE_MAP.md`); graduation
   depends on org migration completion.
2. **Role-based bank filtering** (claim 1 follow-up) — `load_question_banks()`
   currently loads all banks; add explicit filtering by the asker's role so
   an audience that does not need a given bank does not see it in the
   preview. Status: unscoped; tracked in `docs/ROADMAP.md` under
   "Post-v4.3 open items".

Objective 4 closure: all four originally-deferred items landed in v4.3.
The subsystem graduated to `status: stable_pending_shakedown` in the same
release; see `docs/releases/v4.3.0-release-notes.md`.
