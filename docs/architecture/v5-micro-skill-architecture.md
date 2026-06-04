---
title: v5 Micro-Skill Architecture
status: draft
owner: Mario Urquia
last_reviewed: 2026-06-03
sources_of_truth:
  - src/catalog/catalog.schema.json
  - scripts/catalog-build.py
  - CONTRIBUTING.md
  - docs/plans/v5-analysis/09-amos-integration.md
---

# v5 Micro-Skill Architecture

> Phase-1 architecture artifact for the v5.0.0 release. Companion to
> `docs/plans/v5-skill-modernization-plan.md` (trust-hardening track) and
> `docs/plans/v5-analysis/09-amos-integration.md` (AMOS contract).
> Branch: `release/v5-skill-modernization` (single branch/PR for all v5 work).

## 1. Why

The industry direction is away from monolithic "mega-skills" toward atomic,
composable, governable units. The CRE Skills Plugin already has a real
orchestrator runtime, a governed ingestion family, and (in `residential_multifamily`)
source-class + refusal machinery. What it lacks is an **explicit classification
taxonomy** that (a) distinguishes a conductor from an atomic tool, (b) carries
the governance metadata an agent ecosystem needs, and (c) lets **AMOS consume
the plugin as a governed skill layer without hardcoding each skill**.

AMOS has already *designed* that contract (`PluginSkillRef`, `WorkflowStep`,
`SourceManifestEntry.extractionSkill`, the deck strict resolver — see
`09-amos-integration.md`). v5's job is to make the plugin the **producer** of it.

**This is primarily a metadata + validation + export effort, not a content
rewrite and not stub-skill inflation.** Per the focused-scope decision, v5.0.0
ships the taxonomy, reclassifies the priority mega-skills, classifies the corpus
(by derivation), and exports the AMOS manifest. Net new shipped micro-skills: **0**
(every "candidate micro-skill" below is either an existing skill reclassified, or
a backlog item documented honestly — we do not ship name-only stubs).

## 2. Classification model

`type` (existing: skill | agent | command | calculator | workflow | orchestrator)
stays. We add `classification`, which subdivides `type: skill` and gives every
item an agent-ecosystem role:

| classification | What it is | Atomic? | Example |
|---|---|---|---|
| `micro` | Small, schema-bound, source-grounded, reusable tool. One narrow job. | yes | `t12-normalizer`, `loan-sizing-engine` |
| `normal` | Bounded business task, one clear deliverable. | yes | `capital-raise-machine`, `lease-negotiation-analyzer` |
| `orchestrator` | Multi-phase conductor that composes skills/agents. Declares `decomposes_to`. | no | `amos-icomm-demo-orchestrator`, `document-to-database` |
| `workspace` | Business-facing surface / router over a workflow domain. | no | `residential_multifamily`, `fund-lp-reporting` |
| `agent` | Role/persona worker (mirrors `type: agent`). | n/a | `acquisitions-analyst` |
| `calculator` | Deterministic quantitative tool (mirrors `type: calculator`). | yes | `debt_sizing` |

**Derivation (so we do NOT edit 127 files):** `catalog-build.py` derives a default
classification — `workspace` if `category == workspace` or `pack_type == router`;
`orchestrator` if the slug is in an explicit `ORCHESTRATOR_SLUGS` set or the
description opens with "orchestrator"/"conductor"/"command center"; `calculator`/`agent`
mirror `type`; otherwise `normal`. SKILL.md frontmatter `classification:` overrides
the derived value. Only the priority/pilot skills carry an explicit override; the
rest are derived. Result: every catalog item has a classification with zero blanket
edits.

### runtime_role (how it executes)

`callable_tool` | `workflow_conductor` | `workspace_router` | `deterministic_calculator`
| `agent_persona` | `reference_only` | `human_review_surface`. Derived from
classification with frontmatter override.

## 3. Governance metadata (the AMOS-facing fields)

Added to SKILL.md frontmatter (source of truth), flowed into the catalog, and
exported in the AMOS manifest. Unifies with the v5 skill standard already shipped
in WS-0. **Correction (post-review):** the WS-0 frontmatter field stays
`final_marked` (it is already wired into `tests/test_skill_v5_contract.py`,
`CONTRIBUTING.md`, and the RMF `final_marked_workflows.yaml` subsystem — it is NOT
unused). The catalog/manifest emit `decision_grade` as a projection of
`final_marked`; no rename occurs in frontmatter. See §10.

| Field | Type | Required when | Meaning |
|---|---|---|---|
| `classification` | enum | priority/pilot skills (else derived) | §2 |
| `runtime_role` | enum | derived; override optional | §2 |
| `decision_grade` | bool | optional | Can emit a decision-grade artifact (IC memo, valuation, LP report, waterfall). |
| `human_gate` | enum | required if `decision_grade` | `none` \| `review_recommended` \| `approval_required` \| `legal_tax_regulatory_review_required` \| `investment_committee_approval_required` \| `lender_or_investor_review_required` |
| `source_ref_policy` | enum | required if `decision_grade` or AMOS-facing | `not_required` \| `cite_when_available` \| `required_resolvable` \| `required_no_fabrication` |
| `amos_surface` | list | optional | AMOS `RoomTabKey` + landing: `model` \| `leasing` \| `t12` \| `debt` \| `market` \| `diligence` \| `sources` \| `memo` \| `feedback` \| `decision` \| `landing` (see §10) |
| `decomposes_to` | list[id] | required if `classification` ∈ {orchestrator, workspace} | Skills/agents/calculators it composes. |
| `composed_from` | list[id] | optional | Inverse pointer (an orchestrator/workspace that uses this skill). |
| `refusal_trigger` | string | v5_contract | (already shipped) one-sentence fail-closed condition |
| `confidence_default` | enum | v5_contract | (already shipped) confirmed \| estimated \| illustrative |
| `stale_data` | string | v5_contract | (already shipped) freshness caveat |
| `statute_review` | list | conditional | (already shipped) regime-encoding skills |
| `calculator_bridge` | list[id] | conditional | (already shipped) |

## 4. Validation rules (new `tests/test_skill_classification.py` + catalog validator)

Enforced on items that DECLARE the field (opt-in safety, suite stays green):

1. `classification ∈ {orchestrator, workspace}` ⇒ `decomposes_to` non-empty. *Orchestrators/workspaces must not present as atomic.*
2. `decision_grade: true` ⇒ `human_gate != none` AND `source_ref_policy` declared. *No decision-grade output without a human gate + a source posture.*
3. `amos_surface` non-empty ⇒ `source_ref_policy` and `refusal_trigger` declared. *AMOS-facing skills are source-grounded and fail-closed.*
4. `calculator_bridge` slugs resolve to real calculators in `scripts/calculator-registry.json`.
5. `decomposes_to` / `composed_from` ids resolve to real catalog items.
6. Catalog `additionalProperties:false` extended with the new fields (defaults preserve existing catalog validity).
7. Existing parity/preview/version tests stay green; generated surfaces stay drift-free.

## 5. The 8 priority skills — decomposition decisions

Legend: **reclassify_only** = metadata only, no new file; **backlog** = documented for v5.1+, not shipped; **ship_now** = full contract+tests in v5; **reject** = not useful.

| # | Skill | Decision | classification | decomposes_to (existing) | human_gate | Proposed micro-skills |
|---|---|---|---|---|---|---|
| 1 | amos-icomm-demo-orchestrator | reclassify_only | orchestrator | document-to-data-room-extractor, rent-roll-analyzer, t12-normalizer, pca-reserve-analyzer, loan-sizing-engine, acquisition-underwriting-engine, sensitivity-stress-test, ic-memo-generator, ic-red-team-challenger | investment_committee_approval_required | all already exist; none new |
| 2 | document-to-database | reclassify_only | orchestrator | normalize_tokens, map_charge_codes, validate_payload, map_to_target_model, emit_sql_ddl, emit_load_plan, grade_ingestion | review_recommended | entity-resolution-map, range-validate → **backlog** |
| 3 | document-to-warehouse-pipeline | reclassify_only | orchestrator | document-to-data-room-extractor, warehouse-to-exhibit-mapper, reconcile_rent_roll_t12 | review_recommended | duplicate-record-detect, control-total-tieout → **backlog** |
| 4 | property-management-orchestrator | reclassify_only | orchestrator | work-order-triage, vendor-invoice-validator, building-systems-maintenance-manager, tenant-event-planner, variance-narrative-generator, debt-covenant-monitor, property-performance-dashboard | review_recommended | maintenance-sla-classifier, pm-monthly-exception-summary → **backlog** |
| 5 | residential_multifamily | reclassify_only | workspace | (its internal workflow packs) | approval_required (per its approval_matrix) | renewal-risk-score, delinquency-queue-prioritize → **backlog** (respect shakedown status; do not alter) |
| 6 | lease-negotiation-analyzer | reclassify_only | normal | n/a (scenario selector is internal) | legal_tax_regulatory_review_required | anchor-replacement-analysis, co-tenancy-cascade-test → **backlog** (internal modes today) |
| 7 | sourcing-outreach-system | reclassify_only | orchestrator | target-screen, lead-score, broker-message-draft (internal phases) | review_recommended (human approval before any outbound) | lead-score, crm-next-action → **backlog** |
| 8 | fund-lp-reporting / capital-raise-machine | reclassify_only | workspace / normal | lp-data-request-generator, fund-terms-comparator, distribution-notice-generator, quarterly-investor-update, performance-attribution, fund-raise-negotiation-engine | lender_or_investor_review_required | lp-request-scope-classifier, mfn-cascade-impact-check → **backlog** |

**Rationale for zero ship_now new skills:** every candidate either already exists
(reclassify) or would be a name-only stub (backlog). Shipping stubs would violate
the "no stub spam" mandate and the repo's "no placeholder in final-marked paths"
posture. The v5 value is the governable taxonomy + honest backlog, not skill count.

## 6. AMOS manifest contract

Per `09-amos-integration.md`: ship `dist/amos-skill-manifest.json` (generated by
`catalog-generate.py`) as a superset of `dist/catalog.json` carrying the §3
governance fields, plus `docs/integrations/amos-skill-manifest.md` documenting the
contract, and a checked-in `dist/amos-skill-manifest.sample.json` excerpt. AMOS
consumes it to render: executive landing (decision_grade + human_gate aggregate),
analyst model room (amos_surface tab placement), source map (source_ref_policy +
input_artifacts), workflow timeline (decomposes_to ordering), skill-layer view
(full entry), feedback/redlines (human_gate), deck/memo (decision_grade +
source_ref_policy `required_no_fabrication`). No skill is hardcoded into AMOS;
every governance attribute is data.

## 7. Reconciliation with the focused-scope decision

- `classification` + `runtime_role`: **whole corpus** via derivation (zero-edit) + explicit overrides for the 8.
- Full `v5_contract` conformance (3 sections + decision_grade + human_gate + source_ref_policy + amos_surface in frontmatter): **pilot set** — the 8 priority skills + the WS-1a regulatory three + ~10 high-traffic skills (target ~20).
- New micro-skills: **0 shipped**, backlog documented here + in ROADMAP.
- Generalized governance scanner, valuation/investor connectors, full 127 conformance: **v5.1** (unchanged).

## 8. Workstream additions (folded into the task list)

- C-1 catalog schema + build derivation + `test_skill_classification.py` (validation rules §4).
- C-2 reclassify the 8 priority skills (explicit frontmatter) + corpus derivation overrides.
- C-3 AMOS manifest generator + docs + sample.
- C-4 README v5 banner + this doc + migration v4.5→v5 + known limitations.
- Then the trust-track tail: DATA_GRADES.md + governance note (WS-3), debt/entity connector contracts (WS-4), bump+regen (WS-8), package+release (WS-9).

## 9. Risks

| ID | Risk | Mitigation |
|---|---|---|
| A1 | Schema extension breaks existing catalog consumers | All new fields optional with defaults; `additionalProperties:false` extended, not removed; regen + parity gate |
| A2 | Reclassifying RMF perturbs its shakedown contract | RMF gets `classification: workspace` only; status/pack_type/approval_matrix untouched; RMF 298-suite must stay green |
| A3 | decomposes_to ids drift as skills rename | Validator resolves ids against the catalog; CI fails on a dangling id |
| A4 | AMOS manifest implies live integration | Manifest documents capability states honestly; no skill marked live-connected |
| A5 | Classification derivation mis-buckets a skill | Explicit frontmatter override always wins; the 8 + pilot are explicit |

## 10. Post-review revisions (AUTHORITATIVE — supersede §2–§9 where they conflict)

Folded from the Phase-1 review wave (agentic-architecture, data-governance, AMOS-integration, CRE-operating-partner — all Conditional approve). Binding on implementation.

### Wiring (make the metadata real, not decorative)
- **M-A1 — `catalog-build.py:scan_skills` MUST read and emit the new frontmatter keys** (`classification`, `runtime_role`, `final_marked`, `human_gate`, `source_ref_policy`, `amos_surface`, `decomposes_to`, `composed_from`) into the item dict, plus the derived `classification`/`runtime_role` defaults. Without this, the fields never reach `catalog.json` and every rule below is vacuous. This is the gating C-1 step.
- **M-A2 — Add a REAL validator test** `tests/test_skill_classification.py` that (a) `jsonschema.validate`s `dist/catalog.json` against the extended `catalog.schema.json` (currently NO test does this — the schema is unenforced), and (b) enforces the §4 rules. Extending the schema alone protects nothing.
- **M-A3 — Do NOT rename `final_marked`.** Keep it as the frontmatter field (wired into WS-0 + RMF). The catalog/manifest project it to `decision_grade`. RMF's internal `final_marked_workflows.yaml` is a different namespace — untouched.

### Enforcement model (close the omission hole)
- **M-D1 — Allowlist enforcement, not field-presence.** Maintain explicit `DECISION_GRADE_SLUGS` and `AMOS_FACING_SLUGS` sets (the 8 priority + ~12 pilot). Rules 2–3 fire on **membership**: a listed skill MISSING `human_gate`/`source_ref_policy`/`refusal_trigger` is a CI failure. Non-listed skills are advisory (honest scope — §M-H1).
- **M-D2 — `source_ref_policy` is an OBJECT, not a flat enum** (adopt the 09 shape): `{ emits: [namespace...], on_unresolvable: refuse|warn|cite_best_effort, forbids_fabricated_model_ref: bool }`. For AMOS-facing decision-grade skills, `forbids_fabricated_model_ref: true` + a CI check that any declared `model/*`/`data-room/*` namespace is in the manifest root `ref_namespaces`.
- **M-D3 — Reconcile, don't fork, `source_class`.** Add `docs/DATA_GRADES.md` as the single crosswalk across the four deployed vocabularies (RMF executive `[operator|derived|benchmark|overlay|placeholder]`, fallback_resolver `overlay:fallback`, ingest `classification` = `source-fact|calculated|modeled-assumption|requires-review`, and the connector `source_class` from WS-4). `confidence_default` and `source_ref_policy` reference this ladder; no new 5th enum.
- **M-D4 — Add freshness/confidence to the decision-grade gate (advisory metadata, not new runtime):** optional `data_freshness` + `confidence_floor` fields documented for decision-grade skills; reuse provenance.py bands. Not gating in v5 (runtime wiring is v5.1) but documented as the intended control.

### AMOS alignment
- **M-AM1 — `amos_surface` = AMOS `RoomTabKey` + `landing`** (corrected in §3). Source of truth: amos-prototype `room-tabs.ts`.
- **M-AM2 — `human_gate` stays CRE-business-semantic in the plugin** (`none|review_recommended|approval_required|legal_tax_regulatory_review_required|investment_committee_approval_required|lender_or_investor_review_required`) because operators must understand it (operating-partner must-fix). The **manifest generator emits an `amos_signoff` crosswalk** to AMOS's `analyst-review|am-signoff|am-cfo-signoff|external-attestation`. Debt/hedging-exposed decision-grade skills (amos-icomm-demo-orchestrator's debt stage, capital-stack/loan skills) map to `am-cfo-signoff` + `external-attestation` per AMOS ADR-0004.
- **M-AM3 — Ship the explicit `runtime_role → demoStatus` projection in the generator** (7→3 collapse; AMOS `DemoStatus = preprocessed-fixture|deterministic-calc|future-live-connector`). Not prose — a table in `catalog-generate.py`.
- **M-AM4 — Manifest is a STATIC generated artifact + documented contract; no live coupling.** Honest capability states; no skill marked live-connected (ADR-0006: skills are referenced, not invoked live).

### Business credibility + honest framing
- **M-H1 — Honest scope statement** in the architecture doc + README + manifest docs: the v5 governance metadata is a **catalog/manifest contract + CI validation for the listed decision-grade/AMOS-facing slugs**, plus RMF's deployed runtime enforcement. It is NOT yet a corpus-wide runtime fail-closed guard (that is v5.1). Do not imply universal enforcement.
- **M-H2 — Business-facing taxonomy paragraph** (operator language) in README + `docs/integrations/amos-skill-manifest.md`: what orchestrator/workspace/normal/micro mean for a deal team / AM / fund team and why classification affects which outputs need sign-off.
- **M-H3 — Release narrative leads with what is delivered** (governable taxonomy, AMOS manifest, honest decomposition map, trust fixes) — `micro-skill` never appears in a headline without the "0 new stubs; reclassify + backlog" qualifier.

### Targeted governance guard (WS-3, bounded)
- **M-G1 — Ship a real, targeted finance-placeholder guard** (not the full generalized scanner) covering the named decision-grade slugs: `acquisition-underwriting-engine`, `ic-memo-generator`, `comp-snapshot`, `fund-lp-reporting`, `jv-waterfall-architect` (+ the WS-1a three already done). A test asserts these fail closed on an unresolved `$X`/placeholder token in a final-marked path. The fully-generalized corpus-wide scanner remains v5.1.

### Specific skill fixes
- **M-S1 — `fund-lp-reporting`:** rebucket `human_gate` to `investment_committee_approval_required` (it routes LP NAV/distribution notices, not lender covenant packages) and resolve its zero-`references/` contract violation (ship a one-page `references/routing-logic.md` OR formalize the router/workspace reference exemption in CONTRIBUTING and apply it). Name ILPA + NCREIF-PREA reporting standards in the routing reference.
- **M-S2 — OZ + climate factual fixes are DONE in WS-1a** (commit 8b55a75); the operating-partner reviewer flagged them without that context. cost-seg also done. No further action beyond confirming statute_review present.

### Taxonomy precision
- **M-T1 — Objective `micro` vs `normal` tie-breaker:** `micro` = single narrow job, declares an input/output contract, at most one `calculator_bridge`, and no `decomposes_to`. `normal` = a bounded business deliverable that may compose internally but is invoked as one unit. Encode the test as a documented heuristic, not a hard gate (derivation defaults `normal`; explicit override for true micros).
- **M-T2 — `decomposes_to` consistency (nice-to-have):** for orchestrators that also appear in `src/orchestrators/engine/handoff-registry.json`, a non-gating test warns if `decomposes_to` and the runtime handoff graph diverge.
