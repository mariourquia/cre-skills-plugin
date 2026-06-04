---
title: AMOS Skill Manifest — Contract
status: draft
owner: Mario Urquia
last_reviewed: 2026-06-03
sources_of_truth:
  - scripts/amos-manifest-build.py
  - docs/integrations/amos-skill-manifest.schema.json
  - docs/integrations/amos-skill-manifest.sample.json
  - scripts/catalog-build.py
  - docs/architecture/v5-micro-skill-architecture.md
  - docs/plans/v5-analysis/09-amos-integration.md
  - amos-prototype:data/icomm/prose-frontier/room-tabs.ts
  - amos-prototype:data/icomm/prose-frontier/plugin-skills.ts
  - amos-prototype:data/icomm/prose-frontier/source-manifest.ts
---

# AMOS Skill Manifest — Contract

`dist/amos-skill-manifest.json` lets **AMOS consume the CRE Skills Plugin as a
governed skill layer without hardcoding any skill**. It is a generated **superset
of `dist/catalog.json`** carrying the v5 governance fields, plus two crosswalks
computed in code (not prose) that collapse the plugin's governance vocabulary
onto AMOS's.

- **Generator:** `scripts/amos-manifest-build.py` (also emitted by
  `scripts/catalog-generate.py` on a normal run).
- **Schema:** `docs/integrations/amos-skill-manifest.schema.json`.
- **Committed sample:** `docs/integrations/amos-skill-manifest.sample.json` — a
  byte-for-byte excerpt of the full export (the 8 v5 priority skills + 4 pilot
  entries). `dist/` is gitignored, so the sample is the tracked proof of shape.

```bash
python3 scripts/catalog-build.py            # (re)build dist/catalog.json (enriched)
python3 scripts/amos-manifest-build.py      # -> dist/amos-skill-manifest.json
python3 scripts/amos-manifest-build.py --as-of 2026-06-03T00:00:00Z   # deterministic
```

> **Honest framing (read first).** This is a **static, generated export plus a
> documented contract — there is NO live coupling.** No skill is marked
> live-connected: every entry carries `live_connector: false`, always. Per AMOS
> **ADR-0006**, AMOS *references* skills (by `id` + `source_path`); it does not
> invoke them live. The manifest tells AMOS what a skill *is* and what governance
> it *requires*; wiring a live connector is explicitly out of scope (a v5.1+
> target). See the [Honest framing](#honest-framing-no-live-coupling) section.

---

## 1. Root document

| Field | Type | Meaning |
|---|---|---|
| `manifest_version` | string | Semver of **this manifest schema** (currently `1.0`), independent of the plugin release. |
| `plugin_version` | string | The `cre-skills-plugin` release, read from `.claude-plugin/plugin.json` (never hardcoded in the generator). |
| `generated_at` | string (ISO-8601) | Build timestamp. **Determinism-preserving** — see [§4](#4-determinism-of-generated_at). |
| `repo` | string | `mariourquia/cre-skills-plugin`. GitHub deep link = `{repo}/blob/main/{source_path}`. |
| `ref_namespaces` | string[] | Allowed `sourceRef` roots: `["data-room/*", "model/*"]`. A skill's `source_ref_policy.emits` namespaces must match one of these (M-D2). |
| `crosswalks` | object | The two crosswalk tables emitted **as data** (so AMOS reads the projection without re-deriving it). See [§3](#3-the-two-crosswalks). |
| `skills` | array | One `SkillManifestEntry` per catalog item (229 in the 4.5 build; the count tracks the catalog). |

## 2. `SkillManifestEntry` fields

Identity + classification + governance are copied **verbatim from the enriched
catalog**; `demo_status` / `amos_signoff` / `amos_signoff_chain` are **computed**
by the generator.

| Field | Type | Source | Meaning |
|---|---|---|---|
| `id` | string | catalog | Plugin slug. **PRIMARY KEY**. Maps to `PluginSkillRef.skillId`, `SourceManifestEntry.extractionSkill`, `FeedbackItem.routedTo`. |
| `display_name` | string | catalog | Human-readable name. → `PluginSkillRef.displayName`. |
| `type` | enum | catalog | `skill\|agent\|command\|calculator\|workflow\|orchestrator`. |
| `status` | enum | catalog | `stable\|experimental\|stub\|deprecated`. |
| `source_path` | string | catalog | Repo-relative path (`src/skills/<id>/SKILL.md`). → `PluginSkillRef.sourcePath` + GitHub deep link. |
| `version` | string \| null | catalog | Per-item semver from frontmatter. |
| `classification` | enum \| null | catalog | Plugin v5 role: `micro\|normal\|orchestrator\|workspace\|agent\|calculator`. Replaces AMOS's deal-scoped `origin`; AMOS can still bucket cards by it. |
| `runtime_role` | enum \| null | catalog | How it executes: `callable_tool\|workflow_conductor\|workspace_router\|deterministic_calculator\|agent_persona\|reference_only\|human_review_surface`. Crosswalked → `demo_status`. |
| `decision_grade` | bool | catalog | Can emit a decision-grade artifact (IC memo, valuation, LP report, waterfall). Projection of frontmatter `final_marked`. Backs the AMOS tier-1 landing / committed deck slides. |
| `human_gate` | enum | catalog | **CRE-business-semantic** sign-off the output needs before it is acted on: `none\|review_recommended\|approval_required\|legal_tax_regulatory_review_required\|investment_committee_approval_required\|lender_or_investor_review_required`. Stays plugin-side (M-AM2); crosswalked → `amos_signoff`. |
| `source_ref_policy` | object \| null | catalog | Grounding posture (09 shape): `{ emits[], on_unresolvable: refuse\|warn\|cite_best_effort, forbids_fabricated_model_ref: bool }`. Null when the skill has no AMOS-facing grounding contract. |
| `amos_surface` | enum[] | catalog | AMOS `RoomTabKey` + landing placement: `model\|leasing\|t12\|debt\|market\|diligence\|sources\|memo\|feedback\|decision\|landing`. Source of truth: `room-tabs.ts`. Lets AMOS place a skill without a hardcoded map. |
| `decomposes_to` | string[] | catalog | Catalog ids this orchestrator/workspace composes. Powers workflow-timeline ordering. |
| `composed_from` | string[] | catalog | Inverse pointer (orchestrators/workspaces that use this item). |
| `input_artifacts` | string[] | catalog | Named CRE artifacts (OM, T-12, rent roll, …). Binds docs → skill in the source map. → `PluginSkillRef.inputArtifacts`. |
| `outputs` | string[] | catalog | Output artifacts. → `PluginSkillRef.outputArtifacts`. **Sparse in v5** — see [§6 gaps](#6-known-gaps-v51). |
| `chains_to` | string[] | catalog `downstream_items` | Downstream skill ids. |
| `chains_from` | string[] | catalog `upstream_items` | Upstream skill ids. |
| `calculator_file` | string \| null | catalog | Path to the stdlib calculator (when `runtime_role = deterministic_calculator`). Lets AMOS wire a future live connector. |
| `demo_status` | enum | **computed** | `runtime_role` → AMOS `DemoStatus`. See [§3.1](#31-crosswalk-1--runtime_role--amos-demostatus). |
| `amos_signoff` | enum | **computed** | `human_gate` → AMOS sign-off (highest required). See [§3.2](#32-crosswalk-2--human_gate--amos-amos_signoff). |
| `amos_signoff_chain` | enum[] | **computed** | Ordered sign-off ladder up to the primary. Debt/hedging decision-grade skills carry `[am-cfo-signoff, external-attestation]`. |
| `live_connector` | bool (`const false`) | **fixed** | ADR-0006: always `false`. The manifest never claims a live connector. |

## 3. The two crosswalks

Both maps are **total over the plugin enums** (a new plugin value without a
mapping fails `tests/test_amos_manifest.py`). They are emitted under the root
`crosswalks` object as data; the per-skill `demo_status` / `amos_signoff` are the
applied result.

### 3.1 Crosswalk 1 — `runtime_role` → AMOS `DemoStatus`

The plugin has **7** runtime roles; AMOS's `DemoStatus`
(`amos-prototype:…/types.ts`) has **3**. Per `09-amos-integration.md §4`:
`deterministic-calc` stays itself; prompt-guided / orchestrator work is
`preprocessed-fixture`; only documentation/reference whose production target is a
live connector maps to `future-live-connector`.

| Plugin `runtime_role` | AMOS `demoStatus` | Why |
|---|---|---|
| `deterministic_calculator` | `deterministic-calc` | Live stdlib arithmetic on source facts. |
| `callable_tool` | `preprocessed-fixture` | Prompt-guided; output is prepared and reviewed ahead of the demo. |
| `workflow_conductor` | `preprocessed-fixture` | Orchestrator runs prepared in the demo. |
| `workspace_router` | `preprocessed-fixture` | Business-surface router; prepared output. |
| `agent_persona` | `preprocessed-fixture` | Role/persona worker; prepared output. |
| `human_review_surface` | `preprocessed-fixture` | Human-in-the-loop surface; prepared. |
| `reference_only` | `future-live-connector` | Documentation/reference; a live connector is the production target. |

> **Granularity note.** `demo_status` is a function of `runtime_role` alone. AMOS
> may *further* downgrade a specific `preprocessed-fixture` skill to
> `future-live-connector` when the production path needs an **external data
> connector** (e.g. market & sales comps: `comp-snapshot`,
> `submarket-truth-serum`, `market-memo-generator`). That distinction is not
> derivable from `runtime_role`, so the plugin does not assert it here — it is a
> [v5.1 gap](#6-known-gaps-v51) (`needs_external_connector`).

### 3.2 Crosswalk 2 — `human_gate` → AMOS `amos_signoff`

The plugin gate is **CRE-business-semantic and stays in the plugin** (operators
must understand it — M-AM2). The generator emits the AMOS projection. AMOS's
ladder (`09 §3`, ADR-0004 Addendum §1/§3) low→high:
`analyst-review < am-signoff < am-cfo-signoff < external-attestation`.

| Plugin `human_gate` | AMOS `amos_signoff` (base) | Why |
|---|---|---|
| `none` | `analyst-review` | AMOS has no "ungated" tier; analyst-review is the floor. |
| `review_recommended` | `analyst-review` | Advisory review. |
| `approval_required` | `am-signoff` | Asset-manager sign-off. |
| `lender_or_investor_review_required` | `am-cfo-signoff` | External-party-facing package. |
| `investment_committee_approval_required` | `am-cfo-signoff` | IC-level certification. |
| `legal_tax_regulatory_review_required` | `external-attestation` | Statute/regime-encoding output needs an external attest. |

**ADR-0004 debt/hedging escalation.** A **decision-grade** skill that certifies or
restructures debt/coverage carries the **highest** sign-off:
`amos_signoff = external-attestation` with
`amos_signoff_chain = ["am-cfo-signoff", "external-attestation"]`. The escalation
requires **both** `decision_grade: true` **and** membership in `DEBT_HEDGING_SLUGS`
(`amos-icomm-demo-orchestrator`, `loan-sizing-engine`, `capital-stack-optimizer`,
`mezz-pref-structurer`, `debt-covenant-monitor`, `debt-portfolio-monitor`,
`refi-decision-analyzer`, `agency-loan-quote-analyzer`). A debt skill that is not
decision-grade (e.g. `loan-sizing-engine` today, `final_marked: false`) does not
escalate; a decision-grade non-debt skill (e.g. `jv-waterfall-architect`) maps via
the base table (`investment_committee_approval_required → am-cfo-signoff`).

`amos_signoff_chain` is the ordered ladder **up to** the primary, so AMOS can show
the full required sequence (e.g. an `am-signoff` skill yields
`["analyst-review", "am-signoff"]`).

## 4. Determinism of `generated_at`

The generator never wall-clocks by default. Resolution order:

1. `--as-of <iso>` argument (highest);
2. `$AMOS_MANIFEST_AS_OF` environment variable;
3. the **catalog's own `generated_at`** (default) — itself a build input, so a
   manifest built from a fixed catalog is byte-stable;
4. wall-clock — **only** with the explicit `--now` flag.

`scripts/catalog-generate.py` forwards `--as-of` and otherwise inherits the
catalog timestamp. The manifest is a gitignored `dist/` artifact and is kept **out
of** the `catalog-generate.py --check` drift gate (a build artifact cannot fail
the tracked-surface drift check). The committed `*.sample.json` is the tracked,
reviewable proof and is asserted to be a true subset by
`tests/test_amos_manifest.py`.

## 5. AMOS surface → field mapping

Which manifest fields each AMOS surface consumes (from `09-amos-integration.md §2`;
the IC route is a two-tier model room per ADR-0006). The manifest backs the
governance/provenance surfaces; the numeric analyst tabs read governed
facts/model values, not skill metadata.

| AMOS surface | Component | Manifest fields it needs |
|---|---|---|
| **Executive landing** (tier 1) | `prose-frontier-cockpit` + `governance-strip` | `decision_grade` (only decision-grade skills back the landing), aggregate count, `human_gate` / `amos_signoff` (gate count), `amos_surface` ∋ `decision`/`landing`. |
| **Analyst model room** (tier 2) | `room-tabs.ts` (9 tabs) | `amos_surface` (which tab a skill renders on). |
| **Source map / data room** | `ic-source-map-view` + `source-manifest.ts` | `id`, `display_name`, `source_ref_policy`, `input_artifacts` (bind doc → skill via `extractionSkill`). |
| **Workflow timeline** | `ic-workflow-timeline` (`WorkflowStep`) | `id`, `display_name`, `source_path`, `input_artifacts`, `outputs`, `human_gate`, `runtime_role` → `demo_status`, `source_ref_policy`, `decomposes_to`/`chains_to` (ordering). |
| **Skill-layer view** | `ic-skill-layer-view` (`PluginSkillRef`) | the full superset — **the canonical consumer**: `id`, `display_name`, `source_path`, `classification`, `input_artifacts`, `outputs`, `human_gate`, `runtime_role`/`demo_status`, `decision_grade`, `source_ref_policy`. |
| **Feedback / redlines** | `ic-feedback-view` (`FeedbackItem`) | `id` (routing target), `human_gate`/`amos_signoff` (a redline is a gate failing back), `runtime_role`. |
| **Deck / memo** | `lib/deck/registry.ts`, `data/artifacts/registry.ts` | `id` (named in `GovernedGap.connectors`), `decision_grade`, `source_ref_policy` (deck binds resolve-by-reference values, `forbids_fabricated_model_ref`). |

## 6. Known gaps (v5.1)

Fields AMOS would consume that the plugin **cannot yet supply** honestly:

- **`outputs` is sparse.** Many catalog items have `outputs: []`; AMOS's skill
  cards / timeline render `outputArtifacts`. Backfill belongs to the v5.1 SKILL.md
  Output-Format sweep, not this export.
- **`needs_external_connector`.** The plugin cannot say "this skill is a fixture
  *because* it needs a live market/comp/valuation data feed." That nuance lives in
  AMOS's per-skill `demoStatus` today (market & comps). A v5.1 boolean would let
  the plugin drive the `preprocessed-fixture` → `future-live-connector`
  distinction.
- **`produces_artifact_kind` / `governed_metrics`.** No binding from a skill to an
  AMOS `data/artifacts` family (`ic-memo`, `valcomm-deck`, …) or to a versioned org
  metric (DSCR/NOI/TVPI). Proposed in `09 §4`, deferred to v5.1.
- **`pii_policy`.** CAPABILITIES describes aggregate-only / pseudonymization and a
  non-overridable PII-breach block, but no per-skill `pii_policy` enum is exported.
- **`workspace_scope`.** ADR-0004 Addendum §4 RBAC (deal/asset/fund/portfolio) is
  not yet emitted.
- **Corpus-wide runtime enforcement.** See the scope statement below.

## 7. Honest scope statement (M-H1)

The v5 governance metadata is a **catalog/manifest contract + CI validation for the
listed decision-grade / AMOS-facing slugs** (the 8 priority + pilot, enforced by
`tests/test_skill_classification.py` and `tests/test_amos_manifest.py`), **plus
`residential_multifamily`'s deployed runtime enforcement**. It is **NOT yet a
corpus-wide runtime fail-closed guard** — that is v5.1. Do not read the manifest as
asserting universal enforcement.

## 8. Honest framing: no live coupling

- **Static export.** The manifest is generated from the catalog and committed-as-a-
  sample; AMOS fetches/imports it like `catalog.json`. Nothing in the manifest
  executes.
- **No skill is live-connected.** `live_connector` is `false` for every entry,
  asserted by `test_no_entry_claims_a_live_connector`. ADR-0006: skills are
  *referenced* (by `id` + `source_path`), not invoked live.
- **`demo_status` is a maturity label, not a runtime claim.** `deterministic-calc`
  means the plugin *ships* live stdlib arithmetic for that skill; it does **not**
  mean AMOS runs it live in the prototype.
- **The contract is data, not code branches.** AMOS places, gates, and groups
  skills from the manifest fields — it does not hardcode any skill id. Swapping the
  hand-maintained `plugin-skills.ts` for this generated import is a zero-render-code
  change (the schema is a superset of `PluginSkillRef` + `extractionSkill`).

## Appendix — business-facing taxonomy (M-H2)

What `classification` means for a deal team / AM / fund team, and why it drives
which outputs need sign-off:

- **`micro`** — a single narrow, schema-bound tool (one job, source-grounded).
  *Example:* `t12-normalizer`. Cheap to reuse; rarely decision-grade on its own.
- **`normal`** — a bounded business deliverable invoked as one unit. *Example:*
  `lease-negotiation-analyzer`, `acquisition-underwriting-engine`. May be
  decision-grade → needs a human gate.
- **`orchestrator`** — a multi-phase conductor that composes other skills and
  declares `decomposes_to`. *Example:* `amos-icomm-demo-orchestrator`. Because it
  assembles a committee-facing package, its gate is the **highest of its stages**
  (the AMOS ICOMM orchestrator escalates to external-attestation via its debt
  stage).
- **`workspace`** — a business-facing router over a workflow domain. *Example:*
  `residential_multifamily`, `fund-lp-reporting`. Routes work rather than producing
  one artifact; sign-off attaches to the artifacts it routes to.
- **`agent` / `calculator`** — mirror `type`: a role/persona worker, or a
  deterministic quantitative tool.

The rule of thumb: the closer a skill sits to a **committed, externally-delivered,
or IC-facing artifact** (orchestrators assembling a deck, decision-grade memo/
valuation/LP/waterfall skills, debt certifications), the higher its `human_gate`
and therefore its `amos_signoff`. Intermediate analyst tools (`deal-quick-screen`,
a normalizer) stay `analyst-review` and room-only.
