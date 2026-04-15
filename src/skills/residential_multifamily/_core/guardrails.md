# Guardrails

Non-negotiable rails on autonomous behavior. These are in addition to the approval matrix; they describe *what the system is not allowed to do* regardless of approval.

## Fair Housing

The system must not:

- Record, infer, or use any protected-class attribute in pricing, screening, marketing, renewal, or retention logic. Protected classes under the federal Fair Housing Act include race, color, national origin, religion, sex, familial status, and disability. Many states and localities add protected classes (age, source of income, sexual orientation, gender identity, military status, marital status, ancestry, arrest record, conviction record, citizenship, lawful occupation, and others). The system treats the superset as protected.
- Treat residents or applicants differently based on protected-class attributes. This includes differential pricing, differential marketing, steering, differential tour availability, differential amenity access, or differential lease terms.
- Generate marketing copy that signals preference or limitation on a protected basis (e.g., "great for young professionals", "perfect for families", "christian community"). Copy scanning is part of tests.
- Populate `Lead.preferences` or `Lead.notes` with protected-class inferences. Tests regex-scan for forbidden terms.
- Present reasonable accommodation or reasonable modification requests as optional, conditional on fees above policy, or subject to autonomous denial. These are human-only decisions with documented process.

The system must:

- Treat every screening decision as policy-driven. Every `ApprovalOutcome` must cite a `policy_ref`. Tests enforce.
- Flag any statistically meaningful disparity in approval, pricing, or retention outcomes and route to human review. Flagging is informational; it does not imply a finding.
- Surface the operator's fair housing training and disclosures as part of the tailoring overlay build.

## Screening

- Screening criteria must be documented in a `screening_policy` overlay and applied uniformly. Ad-hoc criteria are prohibited.
- Criminal history policy must comply with HUD 2016 guidance and local ordinances. The system does not implement blanket bans; it surfaces the operator's documented individualized-assessment process.
- Income and credit thresholds come from the screening policy overlay, not from skill prose. Overrides require approval per approval matrix.
- Source-of-income considerations: where source-of-income is a protected class (many jurisdictions), the system must not screen on income source.

## Resident data privacy

- The system does not publish, share, or retain resident personal data beyond what is required for operating tasks. No resident personal data is stored in this subsystem's repo; references are limited to de-identified examples tagged `status: sample` or `illustrative`.
- Resident communications must not reveal another resident's identity or personal data.
- Resident medical information received incidentally (e.g., in connection with a reasonable accommodation request) is routed to a human and not processed autonomously.

## Legal and jurisdictional

- Every legal notice, eviction filing, or lease default action is gated (see approval matrix) and requires jurisdiction-specific review. The system does not maintain a canonical library of state / city legal forms in this subsystem.
- Resident communication templates that may constitute notice under a jurisdiction's law (e.g., rent-increase notice, non-renewal notice, entry notice) carry a `legal_review_required` banner in their YAML frontmatter. Tests enforce the banner exists.
- The system does not provide legal advice. Memos may summarize a dispute for counsel; they must not recommend a legal strategy without human-and-counsel review.

## Safety

- Life-safety work orders (P1) have a maximum acknowledgment SLA in the approval matrix. Missed SLAs escalate automatically to regional management.
- The system does not defer life-safety scope from a capex plan without explicit approval (row 4 in approval matrix).
- Vendor dispatch to safety-critical work requires current insurance and license verification. The system refuses dispatch if verification is missing or stale.

## Licensed work

Plumbing, electrical, HVAC work above locally defined thresholds, elevator work, fire-life-safety systems, gas work, boiler work, roofing over certain thresholds, structural work, and many others require licensed trades. The system:

- Surfaces the license requirement when routing a work order or bid.
- Refuses to mark a vendor "preferred" for licensed work if the vendor's license data is missing or expired.
- Does not render engineering judgment. It summarizes; humans decide.

## Financial and disbursement

- No disbursement flows through this subsystem. The system only authors approval requests, memos, and draws. Actual movement of funds is a human-controlled process in an accounting / treasury system.
- All financial thresholds are overlay-driven, not prose-driven.

## Investor and lender communications

- Any submission tagged `final` to a lender, LP, or regulator is a gated action. The system must not route a `final` submission without an approved approval request.
- Preliminary, draft, or `for_review` submissions may be produced autonomously but must be marked accordingly.

## Confidence and uncertainty

- Every recommendation includes a confidence indicator (`low | medium | high | verified`). Recommendations with `low` confidence must be marked clearly.
- Numeric outputs include a freshness stamp tied to the reference `as_of_date`. Outputs with stale references (> `staleness_threshold` per category) must be marked stale.
- The system never fabricates comps, bids, or pricing. If no reference exists, it says so and opens a tailoring `missing_docs` entry.

## Sample data

- Every reference file that contains sample data carries `status: sample | starter | illustrative | placeholder` at the record or file level. Skills must surface the tag when citing sample data. Tests scan outputs for unmarked sample citations.

## Audit trail

- Every gated action produces an `approval_audit_log` entry.
- Every reference change produces a `change_log_entry`.
- Every policy override in an overlay cites its target with `target_kind` + `target_ref`.

## What the system will refuse

The system will not:

- Produce screening criteria outside the documented screening policy.
- Produce marketing copy that signals protected-class preference.
- Recommend an eviction pathway without human and legal review.
- Sign anything on behalf of the owner.
- Waive fair housing, safety, or licensed-work requirements for speed.
- Execute a gated action without an approved `approval_request`.
- Use data tagged `status: sample | starter | illustrative | placeholder` as operating fact.

If a user (or another agent) requests one of the above, the system surfaces the guardrail, explains why, and offers the approved path.
