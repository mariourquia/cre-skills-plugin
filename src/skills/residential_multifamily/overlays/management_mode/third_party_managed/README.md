# Third-Party-Managed Mode Overlay

Applies when a third-party property manager operates on behalf of the owner. Loads
alongside `owner_oversight` when the asker is owner-side. The TPM overlay is the
site's posture; the owner-oversight overlay is the owner-side posture.

## What this overlay shifts

- Approval routing: site PM to TPM regional to TPM executive; additional owner-side
  approvals layered on per the property-management agreement (PMA).
- Reporting: TPM delivers an owner-facing monthly package on a defined cadence.
  The TPM also participates in the quarterly deep-dive.
- Service-standard escalation paths include owner-side escalation when the TPM
  chain cannot resolve or when an issue has owner-material implications.
- Contract signatory posture: the TPM signs vendor agreements within PMA-defined
  authority; items outside authority route to the owner AM or owner portfolio
  manager.

<a id="pma_reference"></a>

## PMA reference

The property-management agreement is the controlling contract surface. The overlay
references the org's PMA artifact (loaded via the org overlay) rather than
embedding terms. Typical PMA provisions that the overlay reads from:

- Approval thresholds for disbursement, procurement, capex, and change orders.
- Reporting cadence and deliverable list.
- Fee structure (management fee, construction-management fee, leasing fee,
  renewal fee) — informational here, not a skill surface.
- Term, termination, and transition provisions.

<a id="owner_signoff_paths"></a>

## Owner-side sign-off paths

- Disbursement above the PMA-defined owner-signoff threshold: route to owner AM.
- Contract awards above the PMA-defined threshold: route to owner AM.
- Capex and change orders: follow the approval matrix tiers with owner AM layered
  per the PMA.
- Legal notices, eviction filings, lease deviations, fair-housing-risk items, and
  safety-critical decisions follow the approval matrix regardless of PMA.

## Interaction with owner_oversight

When the asker is owner-side (asset manager, portfolio manager, oversight lead),
the router loads `owner_oversight` alongside this overlay. The `owner_oversight`
overlay specifies the TPM-scorecard, report-timeliness, variance-completeness, and
audit-issue-tracking surfaces that the owner uses to oversee the TPM.
