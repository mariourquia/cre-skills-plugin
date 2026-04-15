# Rollout, Integration Layer

status_tag: reference

The rollout is wave-based and progressive, not all-or-nothing. This directory defines the waves, the minimum viable data for each workflow, pilot property guidance, go-live checklist, rollback plan, success metrics, post-launch cadence, cutover procedures, and the pilot-to-production gate.

## Why waves, not a big-bang cutover

A residential multifamily portfolio integrates many sources into many workflows. Deploying all at once would mean a single failure could block the entire subsystem. Waves isolate risk, let the operator validate each integration against real operational workflows, and surface crosswalk and reconciliation issues one domain at a time.

Waves are sequenced so that upstream dependencies land before consumers. Master data and source registry come first; operational workflows activate in the wave where their data is already fresh and reconciled.

## File map

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `rollout_waves.md` | Wave definitions (0 through 4) with entry, exit, acceptance, rollback-trigger, duration bands, required sign-offs. |
| `minimum_viable_data.md` | For each canonical workflow, the minimum viable data package required to activate it meaningfully. |
| `pilot_property_guidance.md` | How to pick a pilot property or portfolio. |
| `go_live_checklist.md` | Step-by-step go-live checklist. |
| `rollback_plan.md` | Per-wave rollback protocol. |
| `success_metrics.md` | Qualitative rollout success metrics. |
| `post_launch_monitoring_cadence.md` | Weekly, monthly, quarterly reviews and outputs. |
| `cutover_procedures.md` | General cutover procedure, not specific to any wave. |
| `pilot_to_production_gate.md` | Criteria for moving any domain from pilot to production. |

## Relationship to runbooks and monitoring

Rollout defines the plan; runbooks and monitoring define the operations that keep it true. Rollout documents point to runbooks and monitoring for remediation detail; they do not duplicate that content.

## No numbers in prose

Rollout success metrics are stated as qualitative bands. The operator sets numeric thresholds in their overlay. Dollar magnitudes, percent targets, and exact counts belong in `overlays/org/<org_id>/`.

## Canonical workflow and audience slugs

Rollout documents reference the 27 canonical workflows (see `../../workflows/`) and the 8 canonical audiences (see `tailoring/AUDIENCE_MAP.md`). Any rollout artifact that names a workflow or audience must use the canonical slug.
