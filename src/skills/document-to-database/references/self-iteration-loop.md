# Self-Iterating Evaluation Loop

The document-to-database family is built and maintained through a self-iterating evaluation loop: a fixed set of specialist roles propose, implement, test, and document changes against fixtures, and a numeric gate decides whether work can merge or ship. The loop is what keeps the executable layer honest as the family grows.

## The roles

The loop runs as a team of specialist roles, each with a single responsibility:

- **Skill Runner** — drives the calculators end to end on a fixture and captures the canonical JSON output.
- **CRE QA** — checks that the output is institutionally correct CRE (the spine ties, the grains are right, the accounting holds).
- **Rent Roll Specialist** — owns the rent-roll path: charge decomposition, unit/lease facts, GPR and occupancy.
- **T-12 Specialist** — owns the operating-statement path: period detection, sign convention, section totals, NOI.
- **Lease-to-Ledger Reconciliation Specialist** — owns the rent-roll-to-T-12 tie-out: the stated basis, the difference classification, the residual.
- **Data Quality** — owns the rubric realization: the weakest-link grade, the 0-100 score, and the critical-failure set.
- **Database Mapping** — owns the target-model profiles, the DDL, and the load plan.
- **Planning** — sequences the work and defines the acceptance criteria for each change.
- **Implementation** — writes the deterministic, stdlib-only calculator code.
- **Regression** — guards against drift: re-runs golden fixtures and parity tests so a change cannot silently alter a previously-correct number.
- **Documentation** — keeps this skill and its references aligned with the code (the doc you are reading is a product of this role).

## The thresholds

The loop gates on the same numbers the grader emits:

| Gate | Threshold | Also requires |
|---|---|---|
| **Merge** | score >= **85** / 100 | no C grade AND no critical failure |
| **Production** | score >= **92** / 100 | all-A AND no critical failure |

The weakest-link letter is primary and the 0-100 score is secondary, exactly as in `grade_ingestion`. A change that drops any dimension to a C, or that introduces a critical failure, cannot merge regardless of the numeric score.

## The critical-blocks rule

Any critical validation failure blocks merge unless it is explicitly documented as a fixture limitation by the reviewing role — with one exception. A **PII-redaction breach is non-overridable**: it blocks at any score and cannot be waived even as a documented fixture limitation. The enumerated criticals are listed in `data-quality-rules.md`.

A second standing rule governs the reconciliation work specifically: **any forced or low-confidence rent-roll-to-T-12 tie-out routes to human review** rather than being accepted into a merge. A forced tie is impossible by construction (nothing adjusts a number to tie), and a low-confidence tie is exactly the case where the machine is most likely wrong, so it is escalated, not auto-accepted.

## Why the loop is deterministic-friendly

Because every calculator is pure and reads no wall clock (timestamps come from a caller-supplied `as_of`, and `run_id` is injected), a fixture run is byte-reproducible: the same inputs always yield the same JSON. That is what makes the loop trustworthy — the Regression role can assert exact-match golden snapshots, and a proposed change either reproduces the prior numbers or visibly changes them. There is no hidden nondeterminism for a regression to chase. See `security-governance.md` for the determinism / zero-data-retention guarantee and `human-review-workflow.md` for what the review roles act on.
