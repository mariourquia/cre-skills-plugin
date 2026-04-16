# Preview / Staging Mode

## Why

Several skills in this plugin carry `status: beta_rc` or `status: experimental`.
Those statuses are not cosmetic — they mean a real operator could consume the
output, mistake it for decision-grade fact, and lose money. Preview mode is the
operational contract that prevents that.

## What it is

Preview mode is a marker system on three layers:

1. **Skill frontmatter** — every SKILL.md with `status: beta_rc` or
   `status: experimental` MUST carry a banner line.
2. **Output wrapper** — when a preview-status skill produces a final artifact,
   its first line is a stamped banner noting the status and what to verify.
3. **Final-marked gate** — a preview-status skill's output cannot be routed to a
   `final_marked_workflow` terminal (board, IC, LP, lender) without a human
   reviewer explicitly acknowledging the preview stamp.

## The banner

Every preview-status SKILL.md file should contain, in the body (not just
frontmatter), a section headed `## Release maturity` that includes the
following markers verbatim so the enforcement test can find them:

```
## Release maturity

- **Status:** <beta_rc | experimental>
- **Preview mode:** active — output carries a `PREVIEW / STAGING` banner
  and is not eligible for final-marked use without human acknowledgement.
- **What to verify before trusting the output:**
  - <1-3 skill-specific gotchas>
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

## Enforcement

- `tests/test_preview_mode_gate.py` (planned — v4.3) asserts that every
  `status: beta_rc` / `status: experimental` SKILL.md contains the Release
  maturity section with the expected markers.
- The executive-output-contract test (already live) refuses to render a
  final-marked output carrying an unacknowledged preview stamp.

## What changes when a skill reaches `status: stable`

When a skill graduates to `status: stable`:

1. Remove the preview banner section from SKILL.md.
2. Remove the preview stamp from the output template.
3. Update `docs/ROADMAP.md` to reflect graduation.
4. Note the graduation in `CHANGELOG.md` under the next release, with
   the evidence trail (tests added, external-operator shakedown, overlay
   doc complete).

Graduation is a governance event; don't skip it to ship.
