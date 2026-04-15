# Runbook: Unmapped Account Handling

status_tag: reference

A GL account code appears in an inbound feed that is not in `master_data/account_crosswalk.yaml`.

## 1. Trigger

- Monitoring alert `unmapped_gl_account` fires during gl normalization.
- Reconciliation check `budget_actual_alignment` reports a variance against an unmapped bucket.
- `identity_unresolved` exception of sub-category `account` appears in the queue.
- Chart-of-accounts change or new expense type introduced upstream.

## 2. Symptoms

- Normalized gl records carry `canonical_account: unmapped`.
- Budget vs actual reports show an "unmapped" line that accumulates values.
- `finance_reporting` or `asset_mgmt` audience reviews variance narratives and finds values they cannot tie to a canonical account.
- `monthly_property_operating_review` and `reforecast` workflows emit warnings.

## 3. Likely causes (ranked)

1. New upstream account added (new vendor category, new expense type, new capex bucket) without a paired crosswalk update.
2. Upstream account renamed; the old key exists in the crosswalk but the new key does not.
3. Account code reused upstream for a different purpose, more dangerous; the crosswalk may now mis-route historical records.
4. Data entry error upstream (typo, wrong account selected), the row belongs elsewhere.
5. Regulatory-program-specific account that requires a regulatory-overlay-aware crosswalk entry.

## 4. Immediate actions (minute-by-minute, numbered)

1. Accumulate the unmapped records into the `unmapped` bucket as declared in `mapping.yaml` for the gl connector; do not reject them at landing. Reconciliation reports the bucket magnitude.
2. Open a `dq_warning` or `dq_blocker` exception depending on magnitude relative to the total; magnitude classification follows `_core/exception_taxonomy.md` (planned) and applicable overlay thresholds.
3. Notify `data_owner` for the gl source and the `finance_reporting` audience. For capex-impacting accounts, also notify `construction` and `asset_mgmt`.
4. Pull the source system's chart-of-accounts description for the unmapped code. Classify: new account, renamed account, reused account, data-entry error, regulatory-only.
5. Draft a crosswalk proposal for `master_data/account_crosswalk.yaml`. Map the upstream account to a canonical account slug from `_core/ontology.md`. If no canonical slug fits, escalate to the subsystem maintainer, a new canonical account requires an ontology change.
6. Open an approval request per `_core/approval_matrix.md` row 20 (alias registry and canonical-data change). Approvers are system maintainer plus designated reviewer; `finance_reporting` must sign off on any revenue or major-expense mapping.
7. For data-entry errors upstream, do not remap. Instead, escalate to the source owner to correct the record upstream and re-emit.
8. Once the crosswalk change is approved, apply it, re-run normalization for the affected window, and clear the `unmapped` bucket entries that now resolve.

## 5. Escalation path

- First responder: `on_call_ops`.
- `data_owner` for the gl source.
- `finance_reporting` for categorization approval.
- `asset_mgmt` for property-level impact.
- `construction` for capex-account categorization impact.
- `compliance_risk` if the account is specific to a regulatory program (for example, HAP subsidy receivable, LIHTC reserve).
- `executive` only if the unmapped balance crosses a materiality threshold defined in `overlays/org/<org_id>/approval_matrix.yaml`.

## 6. Affected workflows

- `monthly_property_operating_review`
- `monthly_asset_management_review`
- `executive_operating_summary_generation`
- `quarterly_portfolio_review`
- `budget_build`
- `reforecast`
- `draw_package_review` (if the account is capex or development-adjacent)
- `cost_to_complete_review` (capex)
- `change_order_review` (capex)
- `third_party_manager_scorecard_review` (for owner-side GL oversight of manager-reported P&L)

## 7. Recovery steps

- Apply the approved `account_crosswalk.yaml` update.
- Re-run gl normalization for the affected landings. Records that resolve move from the `unmapped` bucket to their canonical account.
- Recompute derived benchmarks, variance narratives, and workflow outputs that depended on the period.
- For regulatory accounts, notify `compliance_risk` to confirm the mapping preserves the program's reporting taxonomy.
- Archive the crosswalk proposal and approval artifact.

## 8. Verification steps

- `unmapped` bucket magnitude trends to zero for the newly mapped codes.
- Budget vs actual reports reconcile.
- `budget_actual_alignment` reconciliation check returns to pass.
- Variance narratives in `monthly_property_operating_review` parse cleanly without "unmapped" entries.
- No residual exception of category `identity_unresolved` sub-category `account` for these codes.

## 9. Post-incident review hooks

- Log the crosswalk change to the subsystem change log per `_core/change_log_conventions.md`.
- Retain the approval artifact.
- Chronic unmapped patterns (same upstream system, many new codes per month) prompt a review of the source's chart-of-accounts governance with `business_owner` and `finance_reporting`.
- `finance_reporting` reviews the unmapped bucket size at the monthly close; a persistent bucket is a control gap.
