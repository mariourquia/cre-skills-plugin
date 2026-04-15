# Org Overlay: Defaults Template

This directory is the starting template the tailoring skill uses when onboarding a
new organization. It is not itself an active org overlay; it is the skeleton that
every new `overlays/org/<org_id>/` directory is copied from.

## Files

- `overlay.yaml`: the skeleton overlay manifest with placeholder tokens in place of
  real values. Conforms to `_core/schemas/overlay_manifest.yaml`.
- `approval_matrix.yaml`: placeholder thresholds and approver lists. Tokens
  beginning with `$TBD_` are resolved by the tailoring interview.
- `interview_status.yaml`: tracks which fields the tailoring skill has collected.
  Each field has `collected`, `source_artifact`, and `notes` keys. The file also
  carries a `missing_docs_queue` the tailoring skill appends to when a source
  artifact is not yet available.
- `README.md`: this file.

## How org overlays are produced

1. The tailoring skill is invoked with a new `org_id` (e.g., `acme_residential`).
2. The skill copies this directory to `overlays/org/acme_residential/`.
3. The skill walks `interview_status.yaml`, asks the org the questions required
   to fill each field, and writes the answers and source artifacts into the copy.
4. As each field is collected, the skill replaces the corresponding placeholder
   token in `overlay.yaml` and `approval_matrix.yaml` with the collected value or
   artifact reference.
5. When every required field is collected, the skill flips `status: template` to
   `status: active` in both files.
6. The org overlay is now authoritative and merges last in the overlay order.

## Merge behavior

Per `overlays/README.md`, org overlays always merge last. The operator's values
win over segment, form factor, lifecycle, management mode, and market overlays on
the same `target_ref`. This is intentional: the org's documented policy is the
ground truth for that org.

## Until the overlay is active

An org overlay in `status: template` is treated as not yet authoritative for gated
actions. Approval matrices fall back to the subsystem's canonical floor (see
`_core/approval_matrix.md`). Skills that require org-specific artifacts (e.g., the
screening policy) surface the missing reference loudly per Design Rule 10.

## What this template does not do

- It does not set default dollar thresholds. Those come from the tailoring
  interview.
- It does not carry the operator's actual screening, concession, vendor, or brand-
  voice policy. Those are loaded as artifacts during tailoring.
- It does not define per-property overrides. Per-property overrides live in
  `overlays/org/<org_id>/properties/<property_id>/` when needed, authored by the
  tailoring skill or by the asset-management team.
