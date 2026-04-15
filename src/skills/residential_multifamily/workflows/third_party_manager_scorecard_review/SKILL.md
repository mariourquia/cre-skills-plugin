---
name: Third-Party Manager Scorecard Review
slug: third_party_manager_scorecard_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  TPM scorecard rubric weights, benchmark sets, and SLA bands are overlay-driven. PMA
  terms and audit escalation paths are PMA-specific; each PMA should have its own
  overlay record.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [third_party_managed, owner_oversight]
  role: [asset_manager, portfolio_manager, third_party_manager_oversight_lead, reporting_finance_ops_lead]
  output_types: [scorecard, memo, kpi_review, email_draft]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/collections_benchmarks__{region}_mf.csv
    - reference/normalized/turn_benchmarks__{market}.csv
    - reference/normalized/tpm_scorecard_rubric__{org}.yaml
    - reference/normalized/pma_terms__{pma_id}.yaml
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - report_timeliness
  - kpi_completeness
  - variance_explanation_completeness
  - budget_adherence_tpm
  - staffing_vacancy_rate_tpm
  - tpm_collections_performance
  - tpm_turn_performance
  - service_level_adherence
  - approval_response_time_tpm
  - audit_issue_count_and_severity
escalation_paths:
  - kind: material_performance_gap
    to: asset_manager -> portfolio_manager -> executive
  - kind: audit_finding_critical
    to: asset_manager + legal -> approval_request(row 3 if compliance/fair-housing exposure)
  - kind: pma_amendment_or_termination
    to: asset_manager or portfolio_manager + legal -> approval_request(row 19)
approvals_required:
  - pma_amendment_or_termination
  - material_performance_gap_action
description: |
  Owner-oversight review of third-party property manager performance. Scores against the
  PMA's service standards and the overlay's rubric, computes adherence metrics, flags
  audit findings, produces the scorecard memo and the TPM-facing communication draft.
  Runs monthly per property and quarterly per PMA. Material performance gaps and any
  PMA amendment or termination are gated.
---

# Third-Party Manager Scorecard Review

## Workflow purpose

Hold the third-party manager accountable with a defensible, data-driven scorecard anchored to the PMA and the operating outcomes the owner expects. Surface material performance gaps early so remediation is an ordinary conversation rather than a rupture. Ensure every audit finding is tracked to resolution. Route PMA amendment or termination through the correct approval path.

This pack is flagship-depth. It is where ownership's oversight layer converts a TPM's operating output into an ownership-grade judgment. It is also where PMA integrity lives: service standards, reporting cadence, data quality, approval responsiveness, and audit posture.

## Trigger conditions

- **Explicit:** "TPM scorecard", "third-party manager review", "PMA performance review", "owner-oversight review", "TPM quarterly scorecard".
- **Implicit:** month close with TPM-submitted report; audit finding opened; TPM requests approval beyond overlay band; performance metric drift; PMA anniversary approaching; TPM reporting lapse.
- **Recurring:** monthly per property for tactical scorecard; quarterly per PMA for strategic review.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| TPM-submitted owner report | report | required | monthly |
| Property monthly operating reviews | packs | required | from `workflows/monthly_property_operating_review` |
| Asset management reviews | packs | required | from `workflows/monthly_asset_management_review` |
| PMA terms overlay | yaml | required | service standards, SLAs, reporting requirements |
| Scorecard rubric overlay | yaml | required | weights |
| Audit findings log | table | required | open and closed |
| Approval request ledger | table | required | for TPM-initiated requests and owner response times |
| Market benchmarks | csv | required | for relative performance |

## Outputs

| Output | Type | Shape |
|---|---|---|
| TPM scorecard | `scorecard` | per rubric dimension, per asset, composite |
| Material gap memo | `memo` | where and why; remediation path |
| Audit follow-up list | `checklist` | by severity and age |
| TPM-facing communication | `email_draft` | `draft_for_review`; tone per overlay |
| Remediation action plan | `checklist` | owner-side and TPM-side items |
| PMA-review output (quarterly) | `memo` | anniversary-aligned |
| Approval request bundle | list | for material performance action, PMA amendment |

## Required context

Asset_class, segment, management_mode, market, pma_id, loan context (if covenant impact).

## Process

### Step 1. Inherit property and asset outputs.

Pull each TPM-managed property's monthly operating review and the corresponding asset management review. Both are inputs; the scorecard consumes, does not recompute.

### Step 2. Report timeliness and data quality.

- `report_timeliness`: share of required reports delivered on or before PMA due date.
- `kpi_completeness`: share of PMA-required KPIs populated.
- `variance_explanation_completeness`: share of material variances with explanations.

Each dimension scored per rubric overlay; missing or late reports are material gaps.

### Step 3. Operating performance.

- Property-level performance vs. market benchmark: `tpm_collections_performance`, `tpm_turn_performance`.
- `budget_adherence_tpm` vs. controllable lines.
- `service_level_adherence` against PMA SLAs (response times, lead times, entry-notice compliance).
- `staffing_vacancy_rate_tpm` against PMA-approved roster.

### Step 4. Oversight responsiveness.

- `approval_response_time_tpm`: median days from TPM approval request to owner decision. This scorecard is bidirectional — owner-side delays show up here too. Owner-side median above overlay threshold flags owner-process review.

### Step 5. Audit posture.

- `audit_issue_count_and_severity`: open audit findings by severity; age of oldest critical finding.
- Any critical finding open beyond overlay window is a scorecard red.
- Fair-housing or compliance findings route per row 3 automatically and are surfaced in the scorecard without revealing confidential details.

### Step 6. Scorecard composition.

Apply rubric weights; compute composite score per asset and per PMA. Surface top drivers up and down. Track trend over trailing 6 and 12 months.

### Step 7. Material gap identification (decision point).

- **Yellow:** one dimension below rubric band for one period; remediation plan requested, no approval.
- **Orange:** two dimensions below rubric band, or one dimension below for two consecutive periods; remediation plan with explicit owner-side actions; `approval_request` for material action (overlay-governed; typically asset_manager + portfolio_manager).
- **Red:** three or more dimensions below rubric band or any critical audit finding beyond window; `approval_request` row 19 path opens for PMA amendment or termination consideration with legal.

### Step 8. TPM-facing communication.

Produce the communication draft with overlay tone and clear asks. `draft_for_review`. Never sent without owner-side approval.

### Step 9. Quarterly PMA review.

At quarter end, produce the PMA-anniversary-aligned review with strategic view: PMA term, market context, contracted fees vs. performance, term and amendment history.

### Step 10. Confidence banner.

Every reference cited with `as_of_date` and `status`. PMA-specific overlay `as_of_date` surfaced.

### Branches

- If the scorecard reveals a fair-housing or compliance finding in the TPM's operations: route immediately per row 3; the scorecard memo notes the flag but does not detail; counsel leads.
- If the scorecard implies PMA fee structure misalignment: route as separate evaluation; do not bundle with operational remediation.
- If the scorecard is red for two consecutive months: escalate to executive review; portfolio_manager + asset_manager + legal path opens row 19 for possible PMA change.
- If the TPM is in the middle of a market-wide operating shock (e.g., a hurricane) that distorts metrics: note context, discount a dimension with explicit rationale, and consult overlay for force-majeure treatment.

## Metrics used

`report_timeliness`, `kpi_completeness`, `variance_explanation_completeness`, `budget_adherence_tpm`, `staffing_vacancy_rate_tpm`, `tpm_collections_performance`, `tpm_turn_performance`, `service_level_adherence`, `approval_response_time_tpm`, `audit_issue_count_and_severity`.

## Reference files used

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/collections_benchmarks__{region}_mf.csv`
- `reference/normalized/turn_benchmarks__{market}.csv`
- `reference/normalized/tpm_scorecard_rubric__{org}.yaml`
- `reference/normalized/pma_terms__{pma_id}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Yellow: remediation plan requested; no approval.
- Orange: `approval_request` per overlay for material action.
- Red or critical audit beyond window: row 19 for PMA amendment/termination consideration; legal involved.
- Fair-housing / compliance finding: row 3 (counsel-led).
- Owner-side delay signal (`approval_response_time_tpm`): owner-process review.

## Required approvals

- Material performance-gap action (overlay-defined).
- PMA amendment or termination (row 19).
- Any public-facing response to audit/compliance finding (row 3).

## Failure modes

1. Scorecard without PMA basis. Fix: PMA overlay required.
2. Absolute metrics without market benchmark. Fix: benchmarks mandatory for relative context.
3. Ignoring owner-side response times. Fix: `approval_response_time_tpm` bidirectional; owner-side flagged.
4. Private audit detail leaked in TPM-facing draft. Fix: scorecard notes flag, counsel handles communications.
5. Seasonal distortions unadjusted. Fix: overlay governs seasonal adjustment.
6. PMA amendment proposed without legal. Fix: row 19 required.
7. Sample data as authoritative. Fix: confidence banner.

## Edge cases

- **TPM managing in multiple markets:** asset-level scorecards rolled to PMA-level for quarterly review; variance by market surfaced.
- **New PMA (first 3-6 months):** rubric adjustments per overlay; ramp period defined.
- **PMA with incentive structure:** tie scorecard dimensions to incentive KPIs per PMA; scorecard note explicit.
- **PMA renewal approaching:** strategic review inputs to renewal decision; routes via `workflows/owner_approval_routing` if renewal decision needed.
- **TPM bought by another operator (M&A):** scorecard pauses auto-actions; legal review.

## Example invocations

1. "Run the monthly TPM scorecard for our Charlotte portfolio."
2. "Quarterly PMA review for PMA X; include strategic view."
3. "TPM Y missed report three times this quarter. Build the scorecard and the remediation plan."

## Example outputs

### Output — Monthly TPM scorecard (abridged, Charlotte portfolio, March 2026)

**Report timeliness.** `report_timeliness` within band for the quarter.

**Data quality.** `kpi_completeness` and `variance_explanation_completeness` within band.

**Operating performance.** `tpm_collections_performance` within band at benchmark. `tpm_turn_performance` slightly above benchmark (slower turns); yellow. `budget_adherence_tpm` within band.

**Service levels.** `service_level_adherence` within band.

**Staffing.** `staffing_vacancy_rate_tpm` one position above overlay threshold at one asset; yellow.

**Oversight responsiveness.** `approval_response_time_tpm` median within band. Owner-side responsiveness within band.

**Audit posture.** `audit_issue_count_and_severity` two low findings, no critical; both within overlay window.

**Composite.** Two yellows; overall within acceptable band. Remediation plan requested.

**TPM-facing communication.** `draft_for_review`; asks scoped to the two yellow dimensions.

**Approvals.** None this period. Remediation plan is an owner ask, not an approval.

**Confidence banner.** `tpm_scorecard_rubric__{org}@2026-03-31, status=starter`. `pma_terms__pma_charlotte_mf@2026-03-31, status=sample (PMA overlay pending PMA redline)`. `turn_benchmarks__charlotte@2026-03-31, status=starter`. `collections_benchmarks__southeast_mf@2026-02-28, status=starter`.

### Output — Quarterly PMA review (abridged, PMA X, Q1 2026)

**Strategic view.** Composite trend across trailing 6 and 12 months.

**Operating performance.** Per-asset contributions; one asset carrying a yellow for two consecutive quarters.

**PMA term and fees.** Term X years remaining; fee structure aligned with overlay.

**Recommendation.** Continue; adopt a formal remediation plan on the persistent yellow asset. No PMA amendment this quarter.

**Confidence banner.** References surfaced.
