# Preview / Staging Mode

## Why

Several skills in this plugin carry `status: beta_rc`, `status: experimental`,
or `status: stable_pending_shakedown`. Those statuses are not cosmetic — they
mean a real operator could consume the output, mistake it for decision-grade
fact, and lose money. Preview mode is the operational contract that prevents
that.

## What it is

Preview mode is a marker system on three layers:

1. **Skill frontmatter** — every SKILL.md with `status: beta_rc`,
   `status: experimental`, or `status: stable_pending_shakedown` MUST carry a
   banner line.
2. **Output wrapper** — when a preview-status skill produces a final artifact,
   its first line is a stamped banner noting the status and what to verify.
3. **Final-marked gate** — a `beta_rc` or `experimental` skill's output cannot
   be routed to a `final_marked_workflow` terminal (board, IC, LP, lender)
   without a human reviewer explicitly acknowledging the preview stamp. A
   `stable_pending_shakedown` skill does **not** trigger the final-marked
   refusal on its own (see below) because its refusal-on-missing-input
   contracts are already enforced by the existing guardrails — instead it
   carries a "Stable, awaiting shakedown" banner so operators know no live
   shakedown log exists yet.

## Sub-statuses

| Status | Meaning | Banner | Final-marked refusal |
|---|---|---|---|
| `experimental` | Scaffolded; behavior unspecified. Output is not trustworthy. | `PREVIEW / STAGING` stamp | Yes — refuses without human ack. |
| `beta_rc` | Feature-complete enough to exercise, but pre-operator. Output may be wrong. | `PREVIEW / STAGING` stamp | Yes — refuses without human ack. |
| `stable_pending_shakedown` | Code complete; refusal contracts active; awaiting first operator shakedown log. Output is contract-conformant but has no validated in-the-wild run. | `Stable, awaiting shakedown` banner | **No** — refusal-on-missing-input is already enforced by the subsystem's guardrail machinery, so the preview gate does not layer on a second refusal. The banner remains required so an operator can tell a shakedown log is still missing. |
| `stable` | Code complete + validated by at least one external operator shakedown + overlay docs complete. | No banner. | Not applicable — treated as production. |

Graduation from `stable_pending_shakedown` → `stable` requires a recorded
shakedown log (see [Graduation](#what-changes-when-a-skill-reaches-status-stable)).

## The banner

Every preview-status SKILL.md file should contain, in the body (not just
frontmatter), a section headed `## Release maturity` that includes the
following markers verbatim so the enforcement test can find them:

```
## Release maturity

- **Status:** <beta_rc | experimental | stable_pending_shakedown>
- **Preview mode:** <active | shakedown>
- **What to verify before trusting the output:**
  - <1-3 skill-specific gotchas>
```

For `beta_rc` and `experimental` the second line reads:

```
- **Preview mode:** active — output carries a `PREVIEW / STAGING` banner
  and is not eligible for final-marked use without human acknowledgement.
```

For `stable_pending_shakedown` the second line reads:

```
- **Preview mode:** shakedown — output carries a `Stable, awaiting shakedown`
  banner. Refusal-on-missing-input contracts are active; the subsystem is
  code-complete and is awaiting its first operator shakedown log. Output is
  eligible for final-marked use, but an operator should still log the first
  live run before trusting the status as `stable`.
```

## The output stamp

When a preview-status skill produces a deliverable, the first block of the
deliverable is a stamp:

```
┌──────────────────────────────────────────────────────────────┐
│ PREVIEW / STAGING OUTPUT · status: <beta_rc | experimental>   │
│ This output is not eligible for board, IC, LP, or lender use │
│ without a human reviewer explicitly acknowledging the stamp. │
│ Stamp acknowledged: [ ] initials: ______  date: ______       │
└──────────────────────────────────────────────────────────────┘
```

If the artifact is markdown, the stamp is a fenced block. If the artifact is
YAML or JSON, the stamp is a top-level `_preview_stamp: { ... }` object. If it
is CSV, the first row is a comment line with the stamp payload.

## The final-marked gate

A skill with `status: beta_rc` or `status: experimental` cannot be the direct
producer of a final-marked workflow output. Either:

- A stable skill (status: `stable`) downstream re-runs the computation against
  operator-supplied overlays and replaces the preview stamp with a real
  source-class tag, OR
- A human reviewer explicitly acknowledges the preview stamp by setting
  `preview_stamp_acknowledged: true` in the workflow state, with initials and
  date captured in the approval audit log.

Absent either, the final-marked workflow refuses. This mirrors the
`_core/executive_output_contract.md` refusal-artifact contract.

`status: stable_pending_shakedown` skills are **not** blocked by the
final-marked gate on their own. Their refusal-on-missing-input contracts are
already enforced by the subsystem's guardrails (e.g., the sealed-close /
close-status floor gate for period-grade workflows, the placeholder scanner,
the executive output contract), and those contracts are what prevent stale
data from reaching a board / IC / LP / lender terminal. What
`stable_pending_shakedown` adds is the "awaiting shakedown" banner so an
operator can see that no live shakedown log has been recorded yet; it is not a
second refusal layer.

## Enforcement

- `tests/test_preview_mode_gate.py` (repo-wide, v4.3) and
  `src/skills/residential_multifamily/tests/test_preview_mode_gate.py`
  (subsystem-scoped) assert that every `status: beta_rc`,
  `status: experimental`, or `status: stable_pending_shakedown` SKILL.md
  contains the Release maturity section with the expected markers and the
  correct banner text for its status.
- The executive-output-contract test (already live) refuses to render a
  final-marked output carrying an unacknowledged preview stamp.
- Neither preview-mode gate test adds a second refusal layer for
  `stable_pending_shakedown`; refusal-on-missing-input stays governed by
  the existing contract machinery (sealed-close, placeholder scanner,
  executive output contract).

## What changes when a skill reaches `status: stable`

Graduation path:

1. `status: experimental` → `status: beta_rc`: feature surface is complete,
   refusal contracts are wired, test coverage exists. Output still carries
   the `PREVIEW / STAGING` stamp.
2. `status: beta_rc` → `status: stable_pending_shakedown`: all pass-2
   hardening items close, tailoring guards are active, preview-mode
   enforcement tests pass. Output carries the `Stable, awaiting shakedown`
   banner. The subsystem is eligible for real use but no operator has
   recorded a live shakedown yet.
3. `status: stable_pending_shakedown` → `status: stable`: at least one
   external operator has completed a full-pipeline run and recorded the
   shakedown log; overlay docs are complete; no open regressions from the
   shakedown. Remove the banner section from SKILL.md, remove the output
   stamp, update `docs/ROADMAP.md`, and note the graduation in
   `CHANGELOG.md` with the shakedown-log evidence trail.

Graduation between any two steps is a governance event; don't skip steps
to ship.
