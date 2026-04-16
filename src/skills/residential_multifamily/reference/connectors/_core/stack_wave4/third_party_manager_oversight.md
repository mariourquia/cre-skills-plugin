# Third-Party Manager Oversight — Wave 4

Status: wave_4_authoritative
Audience: asset_mgmt, regional_ops, compliance_risk

When properties are managed by a third party (TPM), the owner-side stack must
deliver oversight using whatever data the manager submits. Wave 4 supports both
self-managed and TPM modes without redefining canonical metrics.

## Three TPM data scenarios

| Scenario | Manager Stack | Owner Stack | Confidence Default |
|---|---|---|---|
| Manager operates in AppFolio with shared instance | appfolio_prod (shared) | appfolio_prod | high |
| Manager exports periodic files (no shared system) | manager-internal | manual_sources_expanded | medium |
| Owner relies on Intacct + manually delivered site data | intacct + manual_sources_expanded | intacct + manual | medium-low |

## Oversight capabilities

| Capability | Source dependency | Degradation mode (when missing) |
|---|---|---|
| Scorecard completeness | manual + appfolio (when shared) | partial scorecard with `data_gap_annotations` |
| KPI timeliness | manual file submission cadence | `recon_tpm_file_submission_lag` warns then blocks |
| Collections oversight | appfolio (preferred) or manager-export collections file | partial; cannot project bad debt without ledger detail |
| Turn oversight | appfolio (preferred) or manager-export turn list | turn cycle time unobservable without move-out + make-ready trail |
| Staffing oversight | hr_payroll (preferred) or manager-submitted staffing roster | benchmark only; cannot validate against actual headcount |
| Budget adherence | intacct + manager-submitted budget file | requires reviewer attestation if no shared GL |
| Report timeliness | manual file submission timestamp | submission lag tracked; escalation per `escalation_matrix.md` |
| Approval response tracking | manual approval matrix submission | approval audit weakened without manager-side workflow data |
| Exception aging | manager-side exception submission OR derived from appfolio | derived where possible; manual where not |
| Missing backup detection | file family registry (`manual_sources_expanded.file_family_registry.yaml`) | every expected file flagged when overdue |

## Confidence flags for TPM-derived outputs

Outputs derived from TPM file submissions carry a `tpm_data_confidence` flag:

| Flag | Meaning | When applied |
|---|---|---|
| `tpm_high` | Live system access (e.g., shared AppFolio instance) | All scorecard fields populated, recon green |
| `tpm_medium` | Periodic file submission, cadence met, recon within band | Standard TPM oversight mode |
| `tpm_low` | Periodic submission, cadence missed once or recon drift | Operator surfaced for follow-up |
| `tpm_unverified` | Multiple cadence misses or recon failure | Output blocked from `executive_operating_summary_generation` until resolved |

## TPM-specific runbooks

- `runbooks/tpm_late_submission.md` (proposed; integrate via `manual_sources_common_issues.md`)
- `runbooks/tpm_data_dispute.md` (proposed)
- `runbooks/manual_override_approval.md` (existing)
- `runbooks/missing_file_handling.md` (existing)
- `runbooks/exception_queue_review.md` (existing)

## Workflows that must support TPM mode

| Workflow | TPM Mode Behavior |
|---|---|
| `monthly_property_operating_review` | Falls back to manager-submitted scorecard if no shared system |
| `third_party_manager_scorecard_review` | Always TPM-mode; checks file submission completeness, KPI timeliness, recon health |
| `delinquency_collections` | Runs from manager-export ledger if no shared AppFolio; confidence reduced |
| `vendor_dispatch_sla_review` | Manager-side data preferred; flagged when missing |
| `executive_operating_summary_generation` | Aggregates self-managed + TPM-managed; `tpm_data_confidence` flag carried through |

## What TPM oversight cannot replace

- Real-time work order intervention (depends on manager system access)
- Resident-facing communication oversight (manager retains)
- Vendor selection at site level (manager governance)

When these gaps materially affect canonical workflow output, the gap is named
explicitly in the output per design rule 10 (`no silent failure`).
