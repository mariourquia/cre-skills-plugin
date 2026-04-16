# Evidence Request Catalog — implementation_intake_signoff_builder

Request evidence only when it materially increases implementation confidence or removes a blocker.

| Evidence request | When to ask | What it proves | Typical owner | Blocking severity if missing | Used by |
|---|---|---|---|---|---|
| Screenshot of export menu or API settings | Export path is described verbally but not shown | Export really exists in the live instance | systems admin | medium | source inventory, access model |
| Sample export file | Team says "we can export it" but no file exists in-session | Actual layout, tabs, columns, null behavior, sample values | reporting lead or admin | high | export & field inventory |
| Field dictionary or report definition | Sample file exists but business meaning is ambiguous | Column semantics and expected usage | systems admin or analyst | high | export & field inventory |
| Reporting calendar | Finance or operations cadence is mentioned vaguely | Actual deadlines, sequence, and owners | controller or reporting lead | high | reporting calendar & SLA register |
| Mapping spreadsheet / crosswalk | IDs are known to exist but ownership or precedence is unclear | Matching logic, overrides, legacy mapping posture | data lead or finance systems | high | crosswalk rules register |
| Approval matrix or policy memo | Team can name approvers but threshold logic is unclear | Required approvals and legal review path | COO, CFO, controller | high | approvals & controls, leader sign-off pack |
| Org chart or owner list | Role labels are known but named approvers are not | Named ownership for sign-off and access | COO or implementation sponsor | medium | leader sign-off pack |
| Process notes / SOP | Export or reporting process depends on tribal knowledge | Operational cadence and exception handling | ops lead or controller | medium | intake packet, blocker log |
| Benchmark pack or owner report sample | Reporting scope is known but output expectation is fuzzy | Deliverable shape and consumer expectation | CFO or asset management lead | medium | sign-off pack |
| Property / entity / vendor list | Coverage is described broadly without concrete scope | Real portfolio footprint and join keys | finance lead or systems admin | high | source inventory, crosswalk rules |

## Red lines

- Do not request or store passwords, tokens, API keys, client secrets, or private keys.
- If a user pastes a secret, redact it immediately and replace it with a placeholder.
- If only verbal confirmation exists for a blocking field, keep the field in `assumed`
  or `inferred` state unless a file, screenshot, or live evidence is produced.
