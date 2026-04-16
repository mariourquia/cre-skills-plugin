# Tailoring Capability Matrix

Published with the internal-beta release. Describes what the tailoring subsystem (at `src/skills/residential_multifamily/tailoring/`) **actually does today** vs. what governance docs (`AUDIENCE_MAP.md`, `DIFF_APPROVAL_PREVIEW.md`, `PREVIEW_PROTOCOL.md`, `MISSING_DOC_MATRIX.md`) describe as the full target behavior.

Per claim, the matrix gives a status and points at the code path + test that proves it.

| # | Claim | Governance source | Status | Runtime path | Test coverage |
|---|---|---|---|---|---|
| 1 | Audience selection — a user's role drives which question banks are presented | `AUDIENCE_MAP.md` (8-audience split) | **Partial** | `tailoring_tui.py::load_question_banks()` loads all banks; does not filter by role. 11 YAML banks on disk (8 new: executive, regional_ops, asset_mgmt, finance_reporting, development, construction, compliance_risk, site_ops; 3 legacy retained: coo, cfo, reporting). | `test_tailoring_tui.py::QuestionBankLoadingTests` (all banks load; role-based filtering not asserted) |
| 2 | Conflict surfacing — when two audiences answer the same overlay key with different values, both answers are visible in the diff preview | `DIFF_APPROVAL_PREVIEW.md` §3, §7 refusal condition 7 | **Proven** (2026-04) | `tailoring_tui.py::compute_diff()` now records every non-chosen usable source on `DiffEntry.conflicting_sources` and sets `has_conflict=True` when answers disagree. Earlier version silently kept only the first source. | `test_tailoring_tui.py::ConflictSurfacingTests` (3 tests: agreement, disagreement, lone-source) |
| 3 | Deterministic preview order — diff entries render in stable alphabetical order by overlay key | `PREVIEW_PROTOCOL.md` rule 4 | **Proven** | `compute_diff()` iterates `sorted(target_to_questions.items())`. | Asserted implicitly by `DiffComputationTests` (added / modified / unchanged tests depend on deterministic ordering) |
| 4 | Preview bundle written to disk as YAML at `tailoring/sessions/{org_id}/{session_id}__preview.yaml` | `DIFF_APPROVAL_PREVIEW.md` line 16-17 | **Partial** | `_export_summary()` writes a markdown summary. A YAML preview-bundle file with the six documented sections (file actions, canonical citations, conflicts, sign-offs, floor check, summary) is **not yet written**. | No test. |
| 5 | Approval-floor check — a tailoring answer cannot lower an approval threshold below the canonical floor in `_core/approval_matrix.md` | `DIFF_APPROVAL_PREVIEW.md` §5, §7 refusal condition 2 | **Not implemented** | `compute_diff()` does not load or compare against `_core/approval_matrix.md`. `DiffEntry.approval_matrix_row` is populated but no floor value is read. | No test. |
| 6 | Canonical-definition redefinition refusal — a tailoring answer targeting a frozen metric field (e.g. `_core/metrics.yaml#economic_occupancy.numerator`) is refused with a `REDEFINITION_ATTEMPT` marker | `DIFF_APPROVAL_PREVIEW.md` §2, §7 refusal condition 1 | **Not implemented** | `compute_diff()` has no knowledge of canonical definitions. | No test. |
| 7 | Missing-doc blocker — a p1 document that remains missing past the blocker threshold refuses to render a dependent preview | `MISSING_DOC_MATRIX.md` §"Blocker criteria" (lines 117-124) | **Not implemented** | `_trigger_missing_docs()` queues missing-doc requests; status transitions to `blocked` after threshold are not implemented. Dependent keys are excluded from the diff (marked `pending_doc`) but the preview still renders. | `QueueAppendTests::test_append_missing_doc` only covers queue-append. No blocker transition test. |
| 8 | Version-drift detection — a tailoring session against a stale base snapshot is flagged | `customization-guide.md` §Health Check | **Not applicable** | The `Health Check` system applies to the skill-customization subsystem (`lib/customization.mjs`), not to org-overlay tailoring. Marked here so reviewers do not look for it in the wrong place. | n/a |
| 9 | 8-audience architecture fully deployed — legacy banks (`coo.yaml`, `cfo.yaml`, `reporting.yaml`) are retired | `AUDIENCE_MAP.md` §Retirement | **Partial** | The three legacy banks are still present on disk and still loaded. `AUDIENCE_MAP.md` documents the legacy-retention window. No code path filters or emits a deprecation warning. | None of the TUI tests check that legacy banks no longer load. |
| 10 | Missing-doc catalog integrity — every `missing_doc_triggers[*].doc_slug` in a question bank resolves to a `doc_catalog.yaml` entry | `MISSING_DOC_MATRIX.md`, inferred from test | **Proven** (2026-04) | Added 16 doc entries to `doc_catalog.yaml` for the new audiences (compliance_risk, executive, finance_reporting, site_ops). Previously 24 doc_slugs were referenced but not cataloged. | `DocCatalogTests::test_missing_doc_triggers_resolve_to_catalog` (passes; used to fail) |

## Interpretation

- Claims marked **Proven** have a runtime code path and a test that exercises it on `main`.
- Claims marked **Partial** have some runtime behavior but the governance doc describes more. The README [Known Limitations](../README.md#known-limitations) section lists these as caveats.
- Claims marked **Not implemented** are governance-only at this point. The docs remain as the forward spec; they are not a current-behavior promise. Do not rely on them.

## Deliberate next steps (tracked but not done in this pass)

1. **Preview-bundle YAML emission** (claim 4) — add `_export_preview_bundle()` that writes `sessions/{org_id}/{session_id}__preview.yaml` with the six `DIFF_APPROVAL_PREVIEW.md` sections. Test: round-trip read-after-write + structural schema check.
2. **Approval-floor check** (claim 5) — load `_core/approval_matrix.md` + `overlays/org/_defaults/thresholds.yaml`; for every diff entry whose `approval_matrix_row` is set, compare `proposed_value` against the canonical floor; refuse and surface the floor in the diff. Test: synthetic diff with a lowered threshold must produce a refusal.
3. **Canonical-definition redefinition refusal** (claim 6) — load frozen fields from `_core/metrics.yaml` and refuse any overlay write targeting them. Test: synthetic question attempting to rewrite `numerator` must produce a `REDEFINITION_ATTEMPT`.
4. **Missing-doc blocker transition** (claim 7) — walk `missing_docs_queue.yaml`, apply blocker criteria (p1 + substitute_behavior=refuse_to_render + age ≥ threshold) → transition status to `blocked` → refuse dependent preview render. Test: queued p1 doc with stale timestamp must mark the relevant preview as blocked.
5. **Legacy bank retirement** (claim 9) — emit a warning when a legacy bank is loaded; remove legacy banks once all orgs have migrated. Test: legacy-bank load path emits the warning.

The tracker row for this work lives in `docs/implementation_hardening_status.md` under Obj 4.
