# Dealpath Onboarding Runbook

Status: stub (wave_4)
Audience: data_platform_team, investments_lead, finance_systems_team

This runbook walks the first-time setup of the Dealpath deal pipeline
adapter in a new operator environment. It covers sandbox access, API
authentication, asset-master sync, IC pipeline alignment, and deal-doc
storage handshake. Every step is required before the adapter can be
advanced from `stub` to `starter` status per
`adapter_lifecycle.md`.

---

## Step 1 — Sandbox setup

1. Open a Dealpath sandbox environment scoped to the operator org.
   Sandbox ids follow the pattern `dealpath_sandbox_<org_slug>` per
   `source_registry/naming.md`.
2. Seed the sandbox with a minimum viable corpus:
   - at least one deal per `deal_type` in {acquisition, development,
     refi, recap}
   - at least one ic_approved deal with conditions
   - at least one deal that has been renamed post-IC
   - at least one legacy deal with sparse fields
3. Register the sandbox as a new row in
   `source_registry/source_registry.yaml` with `environment = sandbox`,
   `status = stubbed`, and `expected_latency_minutes` sized to the
   sandbox SLA.
4. Confirm sandbox isolation: sandbox credentials MUST NOT be usable
   against the production Dealpath tenant. Validated via
   `security/least_privilege_guidance.md`.

---

## Step 2 — API authentication

1. Request an API key pair from the Dealpath administrator. The key
   MUST be scoped to read-only for the adapter. Write scopes are
   denied by the adapter contract per
   `security/secrets_handling.md`.
2. Store the key in the operator's secrets manager under the path
   declared by `security/secrets_handling.md::dealpath_credentials`.
   The path pattern is `<operator_secrets>/dealpath/<environment>/api_key`.
3. Verify the credential_method matches what is declared in
   `source_registry_entry.yaml` (`api_key_placeholder` at stub; advance
   to `api_key_vaulted` at starter).
4. Exercise the authentication path by hitting a read-only endpoint
   (e.g., `GET /api/v1/deals?limit=1`). The onboarding probe logs to
   `monitoring/auth_probe.yaml`.
5. Rotate the key at least once before promotion to `starter`; record
   the rotation event in `security/audit_trail.md`.

---

## Step 3 — Asset-master sync model

1. Pull the operator's Dealpath asset-master via `GET /api/v1/assets`.
   Normalize via `field_mapping.yaml::asset`.
2. For every Dealpath `asset_id`, create a row in
   `master_data/asset_crosswalk.yaml` with `canonical_id` assigned by
   the master_data minting function (`mint_canonical_asset_id`).
3. For assets that already have an AppFolio PropertyId (operating
   assets acquired before the wave-4 rollout), populate
   `property_master_crosswalk.yaml` with
   `survivorship_rule = appfolio_wins_post_setup` and
   `effective_start = acquired_date`.
4. Flag duplicate asset names in the same market (observed in sample
   data) per `dq_rules.yaml::dp_duplicate_asset_in_market`. Route to
   `master_data/unresolved_exceptions_queue.md` for manual
   disambiguation.
5. Legacy deals (created before wave-4 adoption) land with
   `confidence = medium` per `dp_legacy_sparse_field`.

---

## Step 4 — IC pipeline alignment

1. Map operator-specific Dealpath `pipeline_stage` labels to the
   canonical enum via
   `field_mapping.yaml::deal::pipeline_stage::transform`. Stages
   missing from the canonical set surface as `dp_conformance_stage_enum`
   blockers; extend `map_dealpath_stage` or escalate to investments_lead.
2. Verify IC decision cadence: the operator's IC meeting cadence
   (weekly, bi-weekly, monthly) drives the
   `investment_committee_prep` workflow cadence in
   `workflow_activation_additions.yaml`.
3. Align Dealpath IC approval tiers (`tier1`, `tier2`, `tier3`, `exec_only`)
   to the operator's approval thresholds in
   `reference/normalized/schemas/approval_threshold_policy.yaml`.
   Mismatched tiers block `investment_committee_prep` until resolved.
4. Define the IC membership roster as Dealpath user ids; map to
   canonical employee ids via `employee_crosswalk`.
5. Backfill historical ic_decision rows for the trailing 12 months to
   enable baseline analytics.

---

## Step 5 — Deal-document storage handshake

1. Dealpath stores document metadata (not payloads) via
   `GET /api/v1/deals/{id}/documents`. Adapter ingests the metadata only
   (doc_type, uploaded_at, url_ref); payload fetches are NOT performed
   per `security/pii_sample_policy.md`.
2. Validate that `url_ref` is opaque — the adapter must treat it as a
   citation, not a URL to resolve.
3. Link Dealpath `doc_type = ic_memo` rows to the canonical
   `approval_request.decisions[].memo_doc_ref`. Missing memos warn at
   `dp_completeness_ic_record`.
4. For deal documents that must land in a document-management system
   (DMS), a separate integration path handles the sync. The Dealpath
   adapter does not write to the DMS.

---

## Step 6 — Advance to starter status

Prerequisites to leave `stub`:

- `source_contract.yaml`, `normalized_contract.yaml`, `field_mapping.yaml`
  populated and validated by `tests/test_dealpath_adapter.py`.
- `source_registry_entry.yaml` promoted to `status = active` (not
  `stubbed`).
- `credential_method = api_key_vaulted` with rotation policy recorded.
- Sample DQ rules (`dp_freshness_deals`, `dp_completeness_required_fields`)
  have run at least twice against production-like data with zero
  blocker failures.
- Reconciliation checks (`dp_recon_asset_to_property`,
  `dp_recon_handoff_lag_af`, `dp_recon_dev_deal_to_procore_project`)
  have run without blocker failures on a 30-day observation window.
- `asset_crosswalk.yaml`, `property_master_crosswalk.yaml`, and
  `market_crosswalk.yaml` seeded and reviewed.
- Runbook sign-off from `investments_lead` and
  `chief_investment_officer` recorded.

---

## Step 7 — Known onboarding gotchas

- Dealpath operators often populate `market` as free text, not slug —
  expect heavy market_crosswalk editing in the first week.
- Some operators create a "shadow" deal record to track LOIs before
  sourcing; these land with sparse fields and no milestones. Tag as
  `confidence = medium` and leave in pipeline.
- Dealpath `asset_id` reuse (same id across multiple deals) is legal;
  do NOT deduplicate asset rows.
- `deleted_flag = true` is soft-delete only; does NOT cascade to
  downstream systems. Cascade deletion is denied by the adapter
  contract.
- Legacy deals from pre-wave-4 adoption may reference asset_ids that
  no longer exist in the current Dealpath asset-master; fall back to
  `master_data/unresolved_exceptions_queue.md`.
