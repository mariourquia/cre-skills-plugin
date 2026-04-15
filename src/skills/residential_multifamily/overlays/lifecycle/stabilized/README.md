# Stabilized Lifecycle Overlay

Default steady-state lifecycle posture. When a property has reached the
stabilization threshold (see lease-up overlay), the stabilized overlay replaces
lease-up in the merge order. Segment and form-factor overlays continue to apply;
the stabilized overlay simply asserts the default preleased window and confirms
reporting emphasis defers to the segment.

## What this overlay does

- Applies the default 30-day preleased window.
- Confirms reporting emphasis returns to the segment's primary surfaces.
- Does not shift staffing, finish standards, or concession posture beyond what the
  segment already dictates.

## What triggers a shift away from stabilized

- Entering a value-add renovation program: load renovation overlay alongside.
- Preparing for refi / disposition / partnership buyout: load recap_support overlay
  alongside.
- Post-casualty or major-system-failure stabilization period: loads on a case basis,
  not codified here.

## Merge order reminder

Segment, form_factor, lifecycle (stabilized), management_mode, market, org. Later
overlays override earlier on the same target_ref.
