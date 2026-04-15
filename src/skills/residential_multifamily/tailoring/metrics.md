# Metrics tracked by tailoring

The tailoring pack is a meta-skill that produces an organization overlay. Its metrics are
session-level and queue-level rather than property-level. None of these metrics are
canonical property-operations metrics. They are declared here because tests and the
tailoring TUI consume them. If any of these metrics gain cross-pack relevance, they must
be promoted to `_core/metrics.md` and registered in `alias_registry.yaml` in the same
commit.

| Slug | What it measures | Grain | Unit |
|---|---|---|---|
| `completeness_score` | Share of questions in a scope answered and not blocked by a pending doc. Numerator is answered_and_unblocked_count; denominator is total_questions_in_scope. Scope is audience, session, or org. | per scope | percent |
| `confidence_score` | Self-reported or derived confidence per answer, aggregated by scope. Derived confidence looks at whether the answer was (a) grounded in a document in `doc_catalog.yaml`, (b) chosen from canonical choices, or (c) free-text. Weights live in the tailoring TUI source, not here. | per scope | 0_to_1 |
| `missing_docs_queue_depth` | Count of entries in `missing_docs_queue.yaml` with status in {open, received}. Partitioned by priority (p1, p2, p3). | per session, per org | count |
| `sign_off_queue_depth` | Count of entries in `sign_off_queue.yaml` with status `pending`. Partitioned by approver role. | per session, per org | count |

## Target bands

Target bands for these metrics are overlay-driven; see `overlays/org/{org_id}/tailoring_targets.yaml` once tailoring has been signed off for the org. Defaults:

- `completeness_score`: audience-level completeness is the primary acceptance gate; banding lives in the org overlay.
- `confidence_score`: low confidence on a p1-priority answer is a sign-off-queue escalation.
- `missing_docs_queue_depth` p1: operational blocker; other queue depths are informational.
- `sign_off_queue_depth`: informational; does not gate further interview steps.

## QA and reconciliation

- `completeness_score` is computed on every session save; it must never include questions flagged `pending_doc` in the numerator.
- `confidence_score` is recomputed on every answer change.
- Queue depth metrics are derived from the queue YAML files, not stored separately. The tailoring TUI reads and writes the queue files; it does not cache the counts.
