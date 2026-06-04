# Fund & LP Reporting — Routing Logic

This reference documents how the `fund-lp-reporting` workspace classifies an
incoming fund-management request and routes it to the right specialist skill,
and which industry reporting standards govern the LP-facing artifacts produced
downstream. It satisfies the CONTRIBUTING router/workspace reference
requirement: the workspace produces no analytics directly — it routes — so its
reference content is the routing contract plus the standards its outputs must
conform to.

## 1. Classification axes

Each request is classified along three axes before routing:

| Axis | Values | Drives |
|---|---|---|
| Lifecycle stage | `formation` \| `capital_raise` \| `reporting` \| `compliance` | Which specialist branch |
| Artifact class | `internal_workpaper` \| `lp_facing` \| `regulatory_filing` | Whether the IC / sign-off gate applies |
| Source posture | `traceable` \| `unresolved` | Whether the refusal trigger fires |

`lp_facing` and `regulatory_filing` artifacts are decision-grade: a NAV,
distribution, or performance figure in either class must trace to the fund model
or data room. An `unresolved` source posture on a decision-grade artifact stops
routing and escalates to fund counsel / IC review (see the skill's
`refusal_trigger`).

## 2. Routing table

| Request signal | Branch | Specialist skills (in order) |
|---|---|---|
| "form a fund", PPM, Reg D, entity | Fund Formation | `fund-formation-toolkit` → `sec-reg-d-compliance` → `fund-raise-negotiation-engine` |
| "raise capital", pitch deck, data room | Capital Raise | `lp-pitch-deck-builder` → `capital-raise-machine` → `investor-lifecycle-manager` |
| "quarterly update", NAV, attribution, distribution | Reporting & Attribution | `quarterly-investor-update` → `performance-attribution` → `distribution-notice-generator` |
| LP data request, DDQ, side-letter scope | LP Servicing | `lp-data-request-generator` → `fund-terms-comparator` |
| "compliance", audit, fee calc | Compliance & Ops | `fund-operations-compliance-dashboard` → `investor-lifecycle-manager` |

The workspace composes (see `decomposes_to` in frontmatter):
`lp-data-request-generator`, `fund-terms-comparator`,
`distribution-notice-generator`, `quarterly-investor-update`,
`performance-attribution`, `fund-raise-negotiation-engine`.

## 3. Reporting standards the LP-facing outputs conform to

Downstream specialist outputs (quarterly letters, capital accounts, NAV,
distribution notices, performance attribution) are expected to align with the
two reporting standards that institutional LPs and consultants apply to U.S.
private real estate funds:

- **ILPA Reporting Standards** (Institutional Limited Partners Association):
  the LP-facing reporting framework — the ILPA Reporting Template (fees, expenses,
  carried interest, partner-level capital account roll-forward) and the
  Capital Call / Distribution Notice templates. Routing tags any `lp_facing`
  artifact that touches fees, carry, or capital accounts as ILPA-aligned so the
  specialist skill emits the expected line items and notice fields.

- **NCREIF-PREA Reporting Standards** (the joint NCREIF / PREA standards for
  U.S. private real estate): the valuation, performance-measurement, and
  fund-level disclosure conventions — time-weighted and since-inception IRR
  presentation, the income / appreciation / leverage return decomposition that
  `performance-attribution` produces, and fair-value reporting cadence.
  Reporting-branch routing tags performance and NAV artifacts as
  NCREIF-PREA-aligned.

Naming these standards here is the routing contract's commitment, not a claim
that the workspace audits conformance: the specialist skills produce the
artifacts; this reference records which standard each LP-facing artifact class is
held to so the human reviewer at the IC / counsel gate knows the benchmark.

## 4. Escalation

- Ambiguous lifecycle stage → ask the user one scoping question (which stage).
- Decision-grade artifact with an unresolved NAV / distribution / performance
  figure → fail closed per the skill's `refusal_trigger`; do not release to an LP.
- Regulatory filing → always route through `sec-reg-d-compliance` and require the
  `investment_committee_approval_required` human gate before release.
