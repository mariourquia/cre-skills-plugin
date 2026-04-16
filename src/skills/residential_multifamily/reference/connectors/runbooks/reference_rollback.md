# Runbook: Reference Rollback

status_tag: reference

A benchmark or reference update introduced error and must be rolled back to the prior values.

## 1. Trigger

- A published `reference/derived/<benchmark>__<scope>.csv` update (see `benchmark_refresh.md`) is later identified as incorrect.
- Consumer audience reports outputs that changed in an unexpected direction after the refresh.
- A downstream workflow shows systematic variance tied to the refresh window.
- Independent validation (internal or external) contradicts the new benchmark.

## 2. Symptoms

- `benchmark_update_log` entry for the prior refresh is recent.
- Workflow outputs that use the benchmark show directional anomalies.
- Variance narratives in `monthly_property_operating_review` or `monthly_asset_management_review` call out the benchmark as the driver.
- A large number of `mapping_override_pending` or `manual_correction_required` exceptions cluster post-refresh.

## 3. Likely causes (ranked)

1. Source-data quality issue that was not detected at refresh time.
2. Methodology change applied inadvertently during refresh (for example, scope filter shifted).
3. Crosswalk drift, the benchmark's sources rolled up to the wrong groupings.
4. Type or unit issue, values arithmetically correct but in the wrong unit.
5. Upstream correction after publication, the source provider itself corrected their data after the refresh was published.

## 4. Immediate actions (minute-by-minute, numbered)

1. Freeze downstream use of the affected benchmark. Emit a `confidence_downgrade` to `low` for the benchmark; flag every workflow that reads it to use the prior version.
2. Identify the bad change precisely. Read the `benchmark_update_log` entry: source set, methodology, scope, confidence band, approver.
3. Open a rollback `ApprovalRequest` per `_core/approval_matrix.md` row 20 (canonical-data change). Approvers mirror the refresh approvers. Rollbacks are never self-approved.
4. Restore the prior version. The prior `reference/derived/<benchmark>__<scope>.csv` snapshot is retained per `layer_design.md` retention policy (planned). Revert the live file to the prior snapshot; retain the bad version under `reference/derived/_archive/<benchmark>__<scope>__<bad_version>.csv`.
5. Re-publish. Emit a `benchmark_refresh_published` event for the rollback version with a `confidence_band` that matches the prior value's published band, not the bad band.
6. Write the rollback entry to `benchmark_update_log` naming: benchmark slug, scope, bad version, restored version, root cause, approver. Cross-reference the bad refresh's log entry.
7. Notify affected skill packs. Packs that emitted outputs using the bad benchmark receive a correction event; consumers decide whether to re-run outputs or wait until the next scheduled run.
8. Open a corrective-action plan for the next refresh. The next refresh will not publish until the root cause is understood and guarded against.

## 5. Escalation path

- `data_owner` and `business_owner` for the benchmark source.
- `finance_reporting` signs off on rollbacks of finance-adjacent benchmarks.
- `compliance_risk` signs off on rollbacks of regulatory-program benchmarks.
- `executive` signs off on rollbacks that affected executive, lender, or investor-facing outputs.
- `asset_mgmt` for portfolio-scope rollbacks.
- Subsystem maintainer plus designated reviewer for the canonical-change approval gate.

## 6. Affected workflows

Same as `benchmark_refresh.md`. Every workflow that consumed the bad benchmark may have produced outputs that should be reissued with the rollback in place. Typical:

- `market_rent_refresh`, `rent_comp_intake` (market_rent, concession_observation).
- `monthly_property_operating_review`, `reforecast`, `budget_build` (payroll, labor, utility).
- `capex_estimate_generation`, `bid_leveling_procurement_review`, `change_order_review`, `capital_project_intake_and_prioritization`, `cost_to_complete_review` (materials, vendor_rate, capex_cost_library, schedule_duration_assumption).
- `third_party_manager_scorecard_review` (payroll bands).

## 7. Recovery steps

- With the rollback in place, re-run any workflow whose output materially depended on the bad benchmark and was consumed by a downstream decision. Note which outputs supersede the prior ones.
- Issue a correction note to downstream consumers. If any outputs crossed an approval gate (draw, contract, investor submission), coordinate with `legal_counsel` on whether the gate needs revisiting.
- Open a root-cause review within a short window (cadence per overlay; typically one week).
- Plan the next refresh: include a specific guard that detects the root cause (for example, an added reconciliation check, a pre-publish diff threshold, a second validator audience).

## 8. Verification steps

- `reference/derived/<benchmark>__<scope>.csv` matches the prior snapshot.
- `benchmark_update_log` rollback entry exists and is approved.
- Affected workflows run cleanly on the restored benchmark.
- No residual outputs in production still cite the bad version.
- The bad version is archived, not deleted.

## 9. Post-incident review hooks

- Rollback event logged in `_core/change_log_conventions.md` format.
- Root-cause review produces a corrective-action list; each item is tracked to closure.
- If the root cause is structural (methodology, scope, source quality), add a permanent guard to the refresh workflow.
- `executive` monthly operations review notes the rollback and the next-refresh plan.
- Any rollback tied to a regulatory-program benchmark is re-reviewed by `compliance_risk` to confirm no filing obligation was compromised.
