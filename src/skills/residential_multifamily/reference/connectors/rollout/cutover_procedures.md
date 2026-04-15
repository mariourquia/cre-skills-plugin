# Cutover Procedures

status_tag: reference

General cutover procedure for moving from one integration-layer state to another. Not wave-specific. Used by `../runbooks/cutover_manual_to_system.md`, `../runbooks/connector_deprecation.md`, and any other transition that repoints consumer workflows from one source to another.

## When to use this procedure

- Moving from manual file drop to direct system integration.
- Replacing one system source with another (vendor change, consolidation).
- Repointing a crosswalk that affects many downstream workflows.
- Switching from one benchmark methodology to another.
- Retiring a source and activating its replacement.

## Five phases

A cutover has five ordered phases. Skipping a phase is not permitted; truncating a phase's duration requires explicit sign-off from the affected audiences.

### Phase 1, Readiness

Entry: the replacement path is `status: active` or equivalent; the source being cut over is still `active`.

Activities:

- Confirm both paths are producing data on their normal cadence.
- Confirm crosswalks reference both paths correctly during the cutover.
- Confirm consumer workflows can query either path.
- Publish the cutover plan to affected audiences.
- Schedule the parallel-run window.

Exit: all parties confirm readiness; no outstanding blocker on either path.

### Phase 2, Parallel run

Entry: Phase 1 exit.

Activities:

- Both paths land data simultaneously for a defined window. Window length is operator-configurable; typical bands:
  - Short for high-frequency critical feeds (for example, daily sources may parallel-run for one cadence cycle plus a stability buffer).
  - Longer for low-frequency feeds (quarterly sources require at least one full cycle of both).
- For every cadence, reconcile the two paths per canonical object. Persist the comparison to the cutover log.
- Classify each comparison: `tie`, `replacement_better`, `source_better`, `divergent`.
- Observe confidence bands on both paths. The replacement's confidence must reach or exceed the source's confidence for a sustained window before Phase 3.
- Treat any `divergent` classification as blocking; halt the cutover until it is understood and resolved.

Exit: the replacement reaches equal or higher confidence than the source for the declared stability window and no divergent-meaning deltas remain open.

### Phase 3, Cutover gate

Entry: Phase 2 exit.

Activities:

- Collect sign-offs per the cutover scope:
  - `data_owner` of both paths.
  - `business_owner` of both paths.
  - Primary consumer audience (`finance_reporting`, `asset_mgmt`, `regional_ops`, `construction`, `compliance_risk`, `site_ops`).
  - `executive` if the cutover affects executive-facing reporting.
  - `compliance_risk` for regulatory-program cutovers.
  - `legal_counsel` for contractual or legally sensitive cutovers.
- Open the cutover `ApprovalRequest` if the cutover crosses an approval-floor category in `_core/approval_matrix.md` (for example, a change to a canonical benchmark crosses row 20).
- On approval, schedule the cutover moment. Communicate the exact moment to affected audiences.

Exit: sign-offs complete; cutover scheduled.

### Phase 4, Cutover

Entry: Phase 3 exit.

Activities:

- At the scheduled moment:
  - The source path transitions to `status: deprecated` (or an intermediate `active_shadow` if the operator uses shadow status; the subsystem's registry schema accepts the main statuses only, so shadow behavior is implemented as post-deprecation landing retention).
  - The replacement path becomes the sole primary source for the affected scope.
  - Crosswalks repoint to the replacement `source_id`.
- Emit observability events: `registry_status_transition`, `cutover_parallel_run_step` summarizing the final comparison.
- Monitor the first post-cutover landing carefully. Reconciliation must pass.

Exit: the first post-cutover cadence completes green.

### Phase 5, Stabilization

Entry: Phase 4 exit.

Activities:

- Continue monitoring for a defined stability window.
- Retain the source path's landings during the window without promoting them (for post-hoc reconciliation if needed).
- If a regression surfaces, execute the rollback steps in `../runbooks/cutover_manual_to_system.md` or `../runbooks/connector_deprecation.md`.
- At the end of the window:
  - Retire the source path's adapter (credentials, infrastructure).
  - Retain the raw archive permanently per `layer_design.md` (planned).
  - Log the cutover completion per `_core/change_log_conventions.md`.

Exit: the replacement is operating as the sole primary source; the deprecated path is retired except for archived raw files.

## Cutover log

Every cutover maintains a cutover log that includes:

- Cutover id (stable snake_case slug).
- Source path `source_id`.
- Replacement path `source_id`.
- Phase 2 comparison entries per cadence.
- Phase 3 sign-offs.
- Phase 4 transition timestamp.
- Phase 5 stabilization observations.
- Post-stabilization retrospective.

The cutover log is retained for audit beyond the retention period of the deprecated source's registry entry.

## No-shortcut rules

- No cutover bypasses Phase 2. A "we already know it works" assertion is not a substitute for parallel-run evidence.
- No cutover bypasses sign-offs. If an audience is unavailable, the cutover waits, not the audience.
- No cutover retroactively fills in the cutover log. If the log was incomplete at the time, the cutover is incomplete.
- No cutover is silent. Every audience whose workflows read from the affected sources is notified at Phase 3 and again at Phase 4.

## Relationship to waves

A cutover is not a wave. A wave is a scope expansion; a cutover is a source swap within scope. The two can coincide (Wave 2 may include a cutover from a manual source to a system source) but the procedures are distinct. Wave sign-offs come from `rollout_waves.md`; cutover sign-offs come from here.

## Relationship to overlays

Cutovers may require overlay updates (for example, repointing a threshold reference or updating a vendor-list hint). Those updates follow the overlay governance process in `_core/BOUNDARIES.md` and `tailoring/DIFF_APPROVAL_PREVIEW.md`. A cutover does not grant temporary permission to modify overlays outside governance.
