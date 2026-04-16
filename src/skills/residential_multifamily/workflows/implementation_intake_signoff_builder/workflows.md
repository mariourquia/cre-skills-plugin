# Workflow Details

## Operating model

The workflow is built around one session workspace per implementation engagement. A session may be run by one person or enriched across several stakeholders over time. The workflow does not assume a single interview owner and does not assume all evidence arrives at once.

## Session lifecycle

1. Open or resume an engagement.
2. Select the current mode.
3. Load only the question sections that mode requires.
4. Capture answers with an explicit evidence status.
5. Persist the answer immediately.
6. Recompute progress, evidence coverage, confidence, blockers, and next actions.
7. Preview the packet at any time.
8. Pause and resume without losing context.
9. Escalate to sign-off packaging only when confirmed facts, assumptions, blockers, and decisions are explicit.

## Evidence-aware control points

- Every answer is tagged with an evidence status from `evidence_model.yaml`.
- Evidence items are tracked separately from answers so the workflow can distinguish an answer from the artifact that supports it.
- Missing documents open blocker records immediately.
- Conflicting evidence forces exception-resolution mode.
- Third-party-manager-submitted evidence is permitted, but it is marked explicitly and lowers confidence until source-native evidence arrives.

## Artifact assembly order

1. Source inventory and source instance registers.
2. Access model and export or field inventory.
3. Crosswalk and source-of-truth register.
4. Reporting calendar and SLA register.
5. Missing docs, blockers, assumptions, and decision logs.
6. Implementation intake packet.
7. Leader sign-off pack.
8. Action queue.

## Canonical protection

- The workflow may write session state and preview artifacts only.
- The workflow may cite connector contracts, source registry records, crosswalk guidance, and third-party-manager guidance.
- The workflow never edits connector manifests, crosswalk files, overlays, routing rules, or canonical metric definitions as part of intake.
- Any future implementation change request created from this workflow must be handled by a separate approval and build path.
