# Routing Example 01 — Site PM asks for a delinquency action plan

**Inbound request (abridged):**

> "Give me a delinquency action plan for Ashford Park. We're at 6.8% on the 30+ bucket and the regional wants a plan by Friday."

## Axis resolution

| Axis | Resolved to | Source of resolution |
|---|---|---|
| `asset_class` | `residential_multifamily` | default |
| `segment` | `middle_market` | property master (`Property.segment`) |
| `form_factor` | `garden` | property master |
| `lifecycle_stage` | `stabilized` | default (property is not in lease-up / renovation) |
| `management_mode` | `third_party_managed` | property master |
| `role` | `property_manager` | asker's role tag |
| `workflow` | `delinquency_collections` | inferred from request text |
| `market` | `Charlotte` | property master |
| `submarket` | `South End` | property master |
| `output_type` | `checklist` + `memo` | request signals "action plan" |
| `decision_severity` | `recommendation` | no action taken by system; PM executes |

## Packs loaded

- `roles/property_manager/` (primary pack).
- `workflows/delinquency_collections/` (workflow pack).
- `overlays/segments/middle_market/` (segment overlay).
- `overlays/form_factor/garden/` (form overlay).
- `overlays/lifecycle/stabilized/` (lifecycle overlay).
- `overlays/management_mode/third_party_managed/` (mode overlay).
- `overlays/org/<org_id>/` if org overlay exists.

## References loaded

- `reference/normalized/market_rents__charlotte_mf.csv` (for market-to-lease gap context).
- `reference/normalized/collections_benchmarks__southeast_mf.csv` (for benchmark framing).
- `reference/normalized/approval_threshold_defaults.csv` or org overlay equivalent (for dollar thresholds triggering approval gates).
- `reference/normalized/delinquency_playbook_middle_market.csv` (stage-by-stage playbook).

## Gates surfaced

- Any recommendation that crosses into `legal_notice` or `eviction_filing` (approval matrix rows 1–2) requires `approval_request` before execution.
- Any non-standard payment plan requires approval matrix row 13.

## System output shape

- Short KPI snapshot (current 30+ bucket, trend, benchmark comparison) citing reference with `as_of_date`.
- Playbook by aging bucket with owner, due date, approval gate, and template links.
- Draft resident communications (portal message + email) marked `draft_for_review`; legal-sensitive ones marked `legal_review_required`.
- Escalation block for legal-sensitive cases.
- Confidence banner citing reference freshness.
