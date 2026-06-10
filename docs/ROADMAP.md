# Public Roadmap

Last updated: 2026-06-09 · Plugin version: v5.2.0

This is the plan for where `cre-skills-plugin` goes from here. It groups
the pending work by release and by track. Items carry a size (S / M / L /
XL), dependencies, and explicit acceptance criteria so outside contributors
can pick up any row and know what "done" means.

Conventions:

- **S** ≈ half a day. **M** ≈ 2–5 days. **L** ≈ 1–3 weeks. **XL** ≈ a quarter.
- Items without an owner are open for contribution.
- "Stable" status on a subsystem means: no placeholder data in final-marked
  paths, decision-grade contract enforced by tests, overlay docs complete,
  **and** at least one real-operator shakedown on file.
- `stable_pending_shakedown` is the code-complete, contract-active sub-status
  that a subsystem occupies between `beta_rc` and `stable` while it waits
  for that first shakedown log. See `docs/PREVIEW_MODE.md`.

## Editions: open core and the paid pro edition

`cre-skills-plugin` is the free, open-source core (Apache-2.0). As of 2026-06-09
the project is open-core: this repo stays the free knowledge layer, and a
separate, private, paid edition, **cre-skills-pro**, is the institution-grade
governance layer built on top of it (lifecycle hooks, four-eyes approvals,
deal-state memory, audit, setup TUI). Net-new skills and the governance harness
land in `cre-skills-pro`. The tracks below that concern governance, approvals,
team collaboration, licensing, and SOC 2 (see [Enterprise / commercial
track](#enterprise--commercial-track-separate-cadence)) are delivered through the
paid edition; the connector, calculator, and skill-contract tracks continue in
this free core.

---

## Current release: v5.2.0 (2026-06-04)

Skill-contract + governance-metadata foundation release. No catalog growth (still
127 / 54 / 21 / 10 / 6; **0 net new skills**). No live connector, no live AMOS
coupling, no production **runtime** enforcement is introduced.

**Shipped in v5.2.0:**

- **Full-corpus tiered skill contract.** Tier 1: all 127 skills carry valid,
  non-null `classification` + `runtime_role` + the v5.2 forward-compat fields,
  enum-validated corpus-wide (`tests/test_skill_contract_corpus.py`). Tier 2: the
  9 decision-grade / `final_marked` carriers reach full `v5_contract: true`
  conformance.
- **Consumer-ready governance metadata (manifest `1.1`).** The four forward-compat
  manifest fields are now **populated**: `produces_artifact_kind` (plugin-namespaced
  enum), `pii_policy` (refined to a sensitivity ladder `none` →
  `business_contact` → `tenant_or_personal` → `sensitive_financial`, default `none`,
  PHI excluded), `workspace_scope` (widened), `outputs[]` (backfilled).
- **Corpus-wide STATIC governance scanner.** `scripts/governance-scan.py` validates
  governance *declarations* over SKILL.md frontmatter + the generated
  catalog/manifest, with per-rule severity and data-driven fixtures
  (`tests/test_governance_scan.py`). It is **not** runtime emitted-output
  enforcement.
- **Connector / source-class no-live invariants** pinned top-level
  (`tests/test_connector_stub_invariants.py`): every connector/adapter stays
  `status: stub`; no entity declares a live `source_class`.

See `docs/releases/v5.2.0-release-notes.md`. The **generalized runtime
emitted-output scanner**, the connector **runtime** enforcement of
`source_class`/`max_staleness`, and live/runnable connector adapters remain
deferred — tracked below.

---

## Previous release: v5.1.0 (2026-06-04)

Governance-hardening release. No catalog growth (still 127 / 54 / 21 / 10 / 6;
**0 net new skills**). No live connector, no live AMOS coupling, no production
runtime enforcement was introduced.

**Shipped in v5.1.0:**

- **Calculator fidelity.** Monte Carlo beta variables now inherit the
  Gaussian-copula correlation (was silently dropped); `fund_fee_modeler`
  promote-sensitivity labeled `grade: screening` / `linear_fee_drag_approximation`
  (not a DCF-IRR); `transfer_tax` / `proration_calculator` / `quick_screen` refuse
  value-domain degeneracy (incl. the proration unparseable-date traceback);
  `debt_sizing` gains `interest_only` aliases. All test-backed.
- **Connector contract schemas (stubs).** The four canonical contracts — `debt`,
  `entity` (legal/ownership, distinct from `master_data`), `valuation`, `funds`
  (+ pseudonymized `investor_report`) — authored as `status: stub`, conforming to
  the connector meta-schemas with round-tripping samples.
- **`source_class` schema enforcement.** Canonical enum in
  `_schema/source_class.yaml`, wired into `entity_contract.schema.yaml`, validated
  by `tests/test_connector_source_class.py`. `max_staleness` declared on the new
  contracts.
- **AMOS forward-compat fields (emitted, then unpopulated).** `produces_artifact_kind`,
  `pii_policy` (default `none`), `workspace_scope` emitted in the manifest;
  `live_connector` stays `false`; `--emit-sample` regenerator added. (v5.2.0 then
  **populated** these and bumped the manifest contract to `1.1` — see the current
  release above.)

See `docs/releases/v5.1.0-release-notes.md`.

---

## Previous release: v5.0.0 (2026-06-03)

Single consolidating release. The source had been version-stamped to 4.4.0
then 4.5.0 but neither tag was ever cut (last published tag: `v4.3.0`).
v5.0.0 folds both never-tagged releases plus a trust-hardening pass and a
new micro-skill governance architecture into one tagged release. Catalog
counts are unchanged (127 skills / 54 agents / 21 MCP tools / 10
orchestrators / 6 workflow chains); **zero new stub skills** were added.

**Shipped in v5.0.0:**

- **Trust hardening.** `opportunity-zone-underwriter`,
  `cost-segregation-analyzer`, and `climate-risk-assessment` corrected to
  current law (OBBBA OZ both-regimes + permanent 100% cost-seg bonus; TCFD
  re-anchored to IFRS S2 / ISSB). Python calculators now refuse degenerate
  input via a typed envelope; JV waterfall catch-up base excludes
  return-of-capital and is relabeled screening-grade. Privacy/feedback
  default reconciled to the true `ask_each_time`. Installer + doc counts
  corrected to 127 / 54 / 21.
- **v5 micro-skill architecture.** Catalog classification taxonomy
  (`micro` / `normal` / `orchestrator` / `workspace`) + governance metadata
  (`decision_grade`, `human_gate`, `source_ref_policy`, `amos_surface`, …),
  a jsonschema catalog validator (`tests/test_skill_classification.py`), the
  v5 skill contract standard (`CONTRIBUTING.md` + `tests/test_skill_v5_contract.py`),
  and the AMOS skill-manifest export. 8 mega-skills reclassified.
- **Honest scope docs.** `docs/DATA_GRADES.md` (canonical six-grade ladder),
  `docs/connectors/CAPABILITY-MATRIX.md` (per-vendor connector truth — all
  stub/planned), `docs/known-limitations.md`.
- **Consolidated v4.4.0** (document → warehouse → deck guidance chain) and
  **v4.5.0** (executable document-to-database ingestion family + the
  orchestrator-engine deal-state / approval-gate / variant / calculator-bridge
  work).

See `docs/releases/v5.0.0-release-notes.md`.

`residential_multifamily` remains `status: stable_pending_shakedown`
(v1.0.0-rc1) — code-complete, contracts active, awaiting the first operator
shakedown log before graduation to `status: stable`.

---

## v5.x — Remaining governance runtime (deferred from v5.2.0)

The honest deferrals that remain after v5.2.0. v5.2.0 added the full-corpus tiered
skill contract, the populated forward-compat manifest fields (`1.1`), the
corpus-wide **static** governance scanner, and the connector no-live invariants. The
remaining **v5.x** scope is the generalized runtime **governance** scanner below,
static-scanner refinement, docs / contract alignment, manifest capability metadata,
no-live invariant enforcement, and optional non-live interface scaffolding. Connector
**runtime** enforcement (`source_class` / `max_staleness`) and runnable / vendor
adapters are **not** v5.x — they are the **v6** real-world-data track (see the
**Real-world data integration — connector track** section below).

### Full 127-skill v5-contract conformance sweep — SHIPPED (v5.2.0)
**Done.** v5.2.0 brought every skill to the Tier-1 contract floor (non-null
`classification` + `runtime_role` + the forward-compat fields, enum-validated
corpus-wide by `tests/test_skill_contract_corpus.py`) and the 9 decision-grade /
`final_marked` carriers to full `v5_contract: true` (Refusal Behavior / Confidence
and Provenance / Known Limitations + the frontmatter fields). The catalog now
carries classification + governance metadata for all 127.

### Generalized cross-skill governance scanner (RUNTIME) — L
**v5.2.0 shipped the corpus-wide STATIC scanner** — `scripts/governance-scan.py`,
which validates governance *declarations* over SKILL.md frontmatter + the generated
catalog/manifest (per-rule severity; fixtures in `tests/test_governance_scan.py`).
What **remains deferred** is the **RUNTIME emitted-output scanner**: tagging/refusing
every cell of every decision-grade skill *at emit time* for source-class tagging and
placeholder leakage, generalizing the `residential_multifamily` runtime machinery to
the whole plugin. The runtime leg outside RMF is still the `final_marked` selector
plus the targeted finance-placeholder discipline guard.

Acceptance: a **runtime** scanner that tags/refuses emitted output across the
decision-grade corpus, with tests — beyond the v5.2.0 static declaration scanner and
the RMF subsystem.

> **Connector runtime and runnable adapters moved to v6.** The four connector
> contract schemas (`debt`, `entity`, `valuation`, `funds` + investor reporting)
> shipped in v5.1.0 as `status: stub` with a schema-enforced `source_class` enum, and
> v5.2.0 pinned the no-live invariants. The connector **runtime** that emits and
> enforces `source_class` / `max_staleness`, and the first runnable /
> `status: starter` adapters, are the **v6** real-world-data track — see the
> **Real-world data integration — connector track** section below for their
> acceptance criteria.

---

## Post-v4.3 open items (target: 4–6 weeks)

Goal: land the operator shakedown, expand behavioral tests beyond
structural integrity, and extend preview-mode coverage. These items
are independent of the v4.4 agent orchestration work listed below —
some may ship as point releases (v4.3.x) rather than in v4.4.

### Record the first residential_multifamily shakedown log — S
Acceptance: an operator (ours or a partner) runs the full residential
multifamily pipeline end-to-end against an anonymized-or-real org
overlay and records the run at `docs/shakedown_logs/residential_multifamily/<date>.md`
with inputs, outputs, refusal artifacts encountered, and any open
regressions. On clean log (no open regressions) the subsystem's SKILL.md
flips from `stable_pending_shakedown` → `stable` and the Release
maturity section is retired.

### Runtime template resolver (Obj 2b) — M
Today `reference_manifest.yaml` declares `fallback_behavior` values like
`use_prior_period`, `use_portfolio_average`, `proceed_with_default`. The
runtime does not carry an explicit confidence downgrade through to the
output when it takes those paths.

Acceptance: a runtime resolver helper that, on non-`refuse` fallback, tags
the output cell's provenance (source-class per Obj 8 contract) as
`[overlay:fallback]` and emits a log line.

### Install smoke tests (Obj 11 continued) — M
Five cells still marked `gap` in `docs/install_smoke_test_matrix.md` after
v4.3:

1. Upgrade (v4.2.x → v4.3.0).
2. Uninstall then reinstall.
3. Corrupted-config recovery.
4. Cowork ZIP import smoke.
5. Claude Desktop chat-tab manual MCP handshake smoke.

Portable-ZIP structural smoke landed in v4.3
(`tests/install_smoke/test_portable_zip.py` +
`.github/workflows/portable-zip-smoke.yml`); cross-runtime invocation
remains a gap on that row.

Acceptance: each remaining cell flips to `covered` with a backing test
path under `tests/install_smoke/`.

### Behavioral calculator tests (cat 1) — M
Expand from structural integrity to behavior for the three most
critical calculators: Monte Carlo, debt sizing, JV waterfall.

Acceptance: `tests/test_calculator_behavior_monte_carlo.py`,
`tests/test_calculator_behavior_debt_sizing.py`,
`tests/test_calculator_behavior_waterfall.py`. Each tests: happy path on
synthetic deal data, three degenerate inputs, and at least one known
regression snapshot.

### Multi-model CI smoke (cat 1) — S
Add a CI job that pins `claude-opus-4-6`, `claude-sonnet-4-6`, and
`claude-haiku-4-5-20251001`, invokes `scripts/smoke_skill_invocation.py`
for five high-surface-area skills, and asserts the output passes the
executive output contract parser. The Grok/Gemini/Codex cross-runtime
check stays on the portable-ZIP path (see v4.4 below).

---

## v4.4 — Agent orchestration upgrade (target: Q3)

Goal: take orchestrators from templates to lightweight runtime.

### Autonomous orchestration engine v0 (cat 2) — XL
Today `/cre-skills:orchestrate` is template prose; Claude acts as the
conductor. Build a lightweight engine (Node/TS in `src/orchestrator/`)
that handles:

- Phase sequencing (FSM reading the phase yaml).
- Checkpointing (resume after interruption).
- Verdict aggregation (GO / CONDITIONAL / KILL with rationale).
- Challenge-layer resolution (track unresolved debate, escalate).

Acceptance: `/cre-skills:orchestrate acquisition --engine v0` runs end-to-
end on a synthetic deal without a human in the loop except at approval
gates; generates an audit log.

### Tool-calling for calculators from orchestrators (cat 2) — L
Orchestrator phases can request a calculator run directly rather than
emitting Python code to the user. Exposes `calculators/*` through the MCP
server with typed inputs / outputs.

### Persistent workflow state (cat 2) — M
Session-level state today; add a deal-scoped persistence layer
(`~/.claude/cre-skills/deals/<deal_id>/state.json`) so long-running
pipelines can pick up across sessions.

### Human-in-the-loop approval gates (cat 2) — M
Formalize approval gates via `approval_matrix.md` rows for each
orchestrator phase; block progression without signed gate; append to
`approval_audit_log.jsonl`. IC / LOI / board output always gated.

### Orchestrator variants per firm type (cat 2) — M
Pre-built variants:

- acquisition: core_plus / value_add / opportunistic
- equity_raise: fund / single_asset / co_investment
- disposition: stabilized / opportunistic_exit / recap
- asset_class: multifamily / office / industrial / retail / hospitality / data_center

Acceptance: each variant ships an overlay under
`src/orchestrators/<slug>/variants/<variant>/` with its own phase list,
approval matrix, and example.

---

## Real-world data integration — connector track (v6, target: 2027)

The deep connector buildout — the **v6** real-world / live data-integration track.
v5.0.0 shipped the honest capability matrix and the `source_class` / `max_staleness`
contract spec; **v5.1.0 landed the four canonical contract schemas** (`status: stub`)
and the schema-enforced `source_class` enum; **v5.2.0 pinned the connector no-live
invariants**. Everything below is **v6**: the connector **runtime** that emits
`source_class` and refuses past `max_staleness`, the first valuation and
investor-reporting connectors at `status: starter` (beyond `stub`, runnable against a
sandbox), and the vendor-specific adapters. Live connector readiness is subject to
vendor terms, security review, and org-specific configuration.

**Acceptance (connector runtime):** a connector runtime that stamps `source_class` on
emitted records and refuses on `max_staleness` violation, with tests — beyond the
static schema check shipped in v5.1.0.

**Acceptance (first adapters):** a valuation connector and an investor-reporting
connector at `status: starter` (beyond `stub`), each runnable against a sandbox
instance.

### Yardi Voyager connector (cat 3) — XL
Build the Voyager connector beyond the current wave-5 adapter stub. Five
role profiles already defined (primary_operating, primary_accounting,
primary_leasing_only, legacy_historical, parallel_partial). Make each
runnable against a sandbox instance.

### AppFolio connector (cat 3) — L
Same shape as Yardi but AppFolio-specific. Work against the v4.x wave-5
scaffolding.

### MRI / RealPage connectors (cat 3) — XL each
Paid competitive parity. Blocked on vendor sandbox access.

### Argus Enterprise import/export (cat 3) — L
Argus `.gsf` / `.gsfx` binary + `.csv` pro forma ingest; canonical
normalization into our DCF schema.

### CoStar / CommercialEdge comps ingest (cat 3) — M
Rate-limited API ingest; overlay onto
`reference/normalized/market_rents__{market}_mf.csv` and the sale comp
files. Licensing model depends on the customer's subscription — plugin
ships the adapter, not the data.

### Procore + Intacct posted-spend reconciliation (cat 3) — M
Already scaffolded in wave 5; lift from sample data to live posted-spend
and construction commitment reconciliation. Close the
`reconciliation_checks.yaml` drift items.

### Document intelligence (cat 3) — L
Lease abstract, PSA redline, env report, CoI parsing. Depends on an
OCR + structured-extraction backbone. Optional Tesseract / AWS Textract /
local vision-model paths.

### Private-cloud handling + SSO (cat 3, cat 5) — XL
"No data leaves the firm" posture: private cache, private MCP endpoint,
SAML/OIDC SSO for enterprise. Paired with the SOC 2 track.

---

## v6.0 — Domain completeness + sector expansion (target: 2027)

### residential_multifamily → stable (cat 4) — L
Acceptance:
- `status: stable_pending_shakedown` → `status: stable` (after the first operator
  shakedown log; see "Record the first residential_multifamily shakedown log" above).
- Remove all `sample / starter / illustrative / placeholder` tags from
  operational `reference/normalized/` files (replace with operator-supplied
  overlays per the tailoring flow).
- Yardi + AppFolio connectors at `status: stable`.
- External operator shakedown report (3+ firms).

### Regulatory / affordable compliance (cat 4) — L
Six phase-1 scaffolding workflows become runnable:
`agency_reporting_prep`, `compliance_calendar_review`, `file_audit_prep`,
`income_certification_cycle`, `recertification_batch`, `rent_limit_test`.

LIHTC (4% / 9%), Section 8 HAP, rent stabilization (NYC RSL), LIHTC
recapture math, HUD MAT / REAC cycles, tax credit calculators.

### Specialized sub-sectors (cat 4) — L each
- **Office**: TI/LC structuring, blend-and-extend math.
- **Industrial**: triple-net lease, bump schedules, last-mile logistics siting.
- **Retail**: percentage rent, breakpoint / overage, co-tenancy clauses.
- **Hospitality**: RevPAR / ADR / occupancy bands, management agreements.
- **Data center / infrastructure**: per-kW lease, power pricing, hyperscale colo.

### Advanced calculators (cat 4) — M each
- Full Argus-style multi-scenario DCF.
- ESG / carbon-accounting (LL97 / BPS / Fitwel / LEED scoring aggregation).
- Portfolio optimizer (mean-variance + efficient frontier over illiquid
  asset class with hold-period constraints).
- Sensitivity tornado charts (text + CSV + optional Plotly).

---

## Enterprise / commercial track (separate cadence)

This track is the paid **cre-skills-pro** edition: the institution-grade
governance layer, developed in a separate private repository on its own cadence
(not part of this free core's release line). The items below are the pro
edition's scope. The honest enforcement note from [SECURITY.md](../SECURITY.md):
client-side hooks are a guardrail plus tamper-evident audit on self-install;
truly enforced governance (unbypassable approvals, a server-held audit trail)
requires managed deployment plus a server-side approval/identity service.

### Licensing & tiering (cat 5) — L
Free (community), Pro (individual / small team), Enterprise (firm).
Plug into Anthropic private marketplace. Opt-in usage telemetry.

### Admin & governance (cat 5) — L
Firm-wide catalog customization w/ approval workflow, RBAC (analyst vs.
principal), audit trail, brand watermarking.

### SOC 2 (cat 5) — XL
Pen test, audit logs, data residency options, redaction hardening.

### Team collaboration (cat 5) — L
Shared workspaces, comment threads on outputs, versioned deal files,
investor-portal export.

### Usage analytics (cat 5) — M
MCP-exposed dashboard: usage stats, time-saved metrics, most-used skills
per team.

---

## UX / polish (continuous)

### Tailoring TUI polish (cat 6) — M
Covered in v4.3 Obj 4 continued. Audience-specific bundling (junior
analyst vs. CIO view) is the stretch item.

### Installer experience (cat 6) — M
- Automatic Node / Python / Claude version detection with halt on missing.
- Rollback on failure.
- Silent / enterprise deployment mode (no prompts).

### Output quality (cat 6) — ongoing
Executive output contract (already shipped for residential_multifamily)
rolled out across all skills. Visualization support: tables, simple
charts via text, optional image gen.

### Onboarding (cat 6) — M
- Interactive tutorial workflows (`/cre-skills:tutorial acquisition`).
- Sample deal datasets under `docs/sample_deals/`.
- Expand `docs/WHAT-TO-USE-WHEN.md` matrix.

### Cross-surface parity (cat 6) — M
Hooks, orchestrators, calculators on Cowork and Claude Desktop Chat tab.

---

## Docs / community / portability (cat 7)

### API / embedding layer (cat 7) — L
Expose the skill + calculator + orchestrator surface as an API for third-
party embedding. Separate from the Claude-native plugin surface.

### Community (cat 7) — S
- Public contribution guidelines with bounties.
- Discord / Slack for CRE + AI users.
- Good-first-issue labels on this roadmap's S items.

### Cross-model portability (cat 7) — M
Tested prompts + fallback behaviors on Grok / Gemini / Codex. Ties to
v4.3 multi-model CI smoke.

### Deferred (explicitly out of scope)

- Case studies and benchmarks. Blocked behind real operator shakedown.
- Pricing page, sales collateral, enterprise demo scripts. Not part of
  the plugin roadmap.

---

## How to contribute

1. Pick an **S** or **M** row that has no owner.
2. Open an issue on the repo citing the row title.
3. Open a branch and an early PR. The maintainer reviews eagerly on
   pass-1 to prevent wasted work.
4. Tests first for every behavioral item.
5. No new dependencies without a note in the PR body.

## Not in scope

- Autonomous decision-making without human review on any final-marked
  output. The plugin assists operators; it does not sign.
- Data collection beyond what `PRIVACY.md` describes.
- Cryptocurrency / tokenized-real-estate gimmicks.
- Anything that requires sending sensitive deal data to a third-party
  service without explicit user consent.
