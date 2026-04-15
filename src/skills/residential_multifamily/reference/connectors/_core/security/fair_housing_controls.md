# Fair-Housing Controls - Integration-Layer Design

Fair-housing-aware design applies to every stage of the integration layer. Data that describes residents, prospects, or applicants can never route through a pipeline that uses protected-class attributes - directly or via proxy - as match keys, model inputs, routing inputs, or decisioning features. Every resident-facing action that could touch a housing decision requires human approval, an audit trail, and periodic compliance review.

This doc operationalizes the fair-housing posture for the integration layer only. The subsystem-wide fair-housing banner and the canonical gated-action list live in `_core/approval_matrix.md` (action three on the approval table) and in per-role fair-housing guidance attached to each tailored audience.

## Protected-class attributes - catalog

The following attribute classes are protected under US federal fair-housing statute and commonly applicable state and local overlays. Operators under other jurisdictions extend this list through an org overlay; they never shrink it.

- race, color, ethnicity
- national_origin
- religion
- sex, gender_identity, sexual_orientation
- familial_status (presence or expected presence of children in the household)
- disability, disability_history, accommodation_request_detail
- source_of_income (in jurisdictions that protect this class)
- marital_status (in jurisdictions that protect this class)
- age (in jurisdictions that protect this class for housing)
- military_status, veteran_status (in jurisdictions that protect this class)
- any other class protected by overlay-declared jurisdiction

All of these attributes map to `pii_classification.md` entry `protected_class_attributes: forbidden_in_processed_output`.

## Protected-class proxies - catalog

Attributes that correlate with protected classes strongly enough to be treated as proxies. Using a proxy is equivalent to using the attribute itself under this policy.

- `neighborhood_demographic_composition` - never a match key, never a routing key.
- `zip_code` when joined with demographic overlays - requires overlay-declared approval before any model use.
- `school_district` when joined with demographic overlays - same.
- `language_preference_primary` as a screening or targeting feature - forbidden.
- `surname_phonetic_cluster` - forbidden as a clustering, matching, or targeting feature.
- `household_size` when combined with `resident_ages` - treated as familial_status; forbidden as a decisioning feature.
- `photo_of_applicant` - forbidden as a feature for any automated decisioning pipeline.
- `voice_recording_of_applicant` - forbidden as a feature for any automated decisioning pipeline.
- `employer_industry_coded_for_income_band` - requires compliance_risk review before any model use.

A new candidate proxy is evaluated under the "if we used this feature on residents of different protected classes, would outcomes differ?" test. If the answer is yes, the attribute is a proxy.

## Forbidden practices

Enumerated. Each forbidden practice has a matching detection rule in `security_testing_guidance.md` or a matching reviewer gate.

- **Matching residents on protected-class proxies.** Forbidden across every connector and every derived benchmark. Proxy fields may not feed crosswalks, dedup rules, or cluster assignments.
- **Using screening results to feed predictive decisioning without human review.** Screening outcomes (background_check_result, credit_score, eviction_history) never feed an automated decision that renders or communicates a housing decision. A human approver must sign the decision.
- **Targeting marketing by protected-class proxies.** Prospect CRM routing, marketing spend allocation, and tour scheduling never use a protected-class proxy as a targeting input.
- **Denying service via automation alone.** No adverse action (denial, non-renewal, eviction, lease-term change) may be executed without a human approval trail.
- **Silent rendering of a protected-class attribute.** Any rendered output that accidentally includes a protected-class attribute is a severity-one exception; remediation is immediate redaction plus audit record plus ApprovalRequest with `subject_object_type: policy_exception`.
- **Using a fair-housing complaint narrative to target follow-up.** Narratives under `fair_housing_complaint_detail` are `restricted`, legal_hold capable, and may not route to any site_ops or regional_ops workflow; they route only to compliance_risk and legal counsel.
- **Creating a derived feature whose definition references a protected class.** A feature that reads "applicants with household_size above X when also presenting children" encodes familial_status; forbidden as a model input.

## Required practices

Also enumerated.

- **Human approval for any action touching screening outcomes.** Any integration-layer action that would activate a workflow based on screening data materializes an ApprovalRequest conforming to `_core/schemas/approval_request.yaml` with `subject_object_type: lease_deviation` or `policy_exception` as applicable.
- **Audit trail for approval decisions.** Every approval in this category writes an `approval_action` record per `audit_trail.md` including the approver identity, the approval_request_id, and the rationale field from the ApprovalRequest.
- **Periodic review by compliance_risk.** The compliance_risk audience receives a recurring review of all approved fair-housing-adjacent decisions. Cadence is operator-set; periodicity is a manifest requirement, not a dollar or numeric threshold.
- **Alerting on fair-housing-sensitive exceptions.** Any exception tagged `fair_housing_sensitive` in the integration layer's exception taxonomy routes directly to compliance_risk with no delay. Silent resolution is forbidden (see `unsafe_defaults_registry.md`).
- **Fair-housing banner in every resident-facing draft.** Drafts of resident communications carry the subsystem-wide fair-housing banner until a human approves and sends. See the canonical banner requirement in `_core/` subsystem docs for tailored roles.

## Screening workflow - canonical posture

Screening data flows:

1. The PMS or screening-vendor connector lands raw screening records under `reference/raw/pms/` (or a dedicated screening connector if the operator separates the feed).
2. Normalization preserves the outcome code and strips free-text narratives that could describe protected-class attributes. Narrative text routes to a legal_hold queue, not into normalized.
3. Derived workflows receive the outcome code only. No derived metric exposes individual screening scores or individual outcome rationales.
4. Any workflow that would act on a negative outcome materializes an ApprovalRequest routed to property_manager plus regional_manager plus (if the outcome implicates a protected class) compliance_risk and legal counsel.
5. The approved action renders a human-readable decision letter; the decision is not automated.

## Marketing and lead routing

Prospect CRM flows:

1. The CRM connector lands raw leads with campaign source and contact channel.
2. Normalization strips protected-class attributes and proxies. If a lead source inadvertently passes a proxy (e.g., a third-party targeting service), the mapping drops it.
3. Derived lead-scoring features are allow-listed. A feature not on the allow-list cannot enter the scoring model.
4. The allow-list is reviewed by compliance_risk on a recurring cadence and any addition requires an ApprovalRequest.

## Accommodation requests

Accommodation-request data is highly sensitive. Requests under the reasonable-accommodation framework:

- Route only to compliance_risk and to the named property_manager, not to site_ops bulk queues.
- Are classified `high` with no rendering to any audience outside the specific request-handling workflow.
- Are retained under extended retention and may be subject to legal hold.
- Generate an ApprovalRequest for any approval or denial; both outcomes require the same human-approval gate.

## Exception taxonomy integration

The integration-layer exception taxonomy (owned by a separate agent under `reference/connectors/_core/`) includes a `fair_housing_sensitive` tag. Exceptions carrying that tag:

- Never silently resolve.
- Always route to compliance_risk.
- Always create an ApprovalRequest for resolution.
- Always write an audit record, including the tag.

The exception payload carries no resident narrative. It carries a coded reason, the record id, the connector_id, and the proposed resolution.

## Alerting

Fair-housing-sensitive alerts:

- Never silenced by a cadence or batching policy.
- Route directly to compliance_risk.
- Are tagged in the monitoring layer (owned by a separate agent) as `severity: high`.
- Trigger an ApprovalRequest at the moment of detection.

## Review cadence

The compliance_risk audience performs a recurring fair-housing review that covers:

- Every allow-list addition for marketing and lead-scoring features.
- Every screening-outcome-driven action taken in the period.
- Every accommodation-request outcome in the period.
- Every fair-housing-sensitive exception resolved in the period.

Findings from the review may tighten the proxy list or the allow-list; they may not loosen the canonical forbidden-practice list.

## Related

- `_core/approval_matrix.md` - canonical gated-action list; fair-housing complaint handling appears there.
- `pii_classification.md` - `protected_class_attributes` classification.
- `audit_trail.md` - audit record schema for approval actions.
- `legal_hold_and_retention.md` - legal hold posture for fair-housing complaint narratives.
- `tests/test_regulatory_isolation.py` - tests that canonical regulatory isolation is respected (covers fair-housing posture).
