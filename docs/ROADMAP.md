# Public Roadmap

Last updated: 2026-06-03 · Plugin version: v5.0.0

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

## Current release: v5.0.0 (2026-06-03)

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

## v5.1 — Generalized governance + connector contracts (next)

The honest deferrals from v5.0.0. v5.0.0 shipped the metadata, the validator,
and the honest capability matrix; v5.1 turns the specified-but-not-enforced
pieces into runtime.

### Full 127-skill v5-contract conformance sweep — L
v5.0.0 opted a pilot slice into `v5_contract: true` and corrected the
decision-grade / AMOS-facing skills. v5.1 extends the contract (Refusal
Behavior / Confidence and Provenance / Known Limitations sections + the new
frontmatter fields) across the full corpus.

Acceptance: `tests/test_skill_v5_contract.py` enforces the contract on every
non-exempt skill (not just the opted-in slice), and the catalog carries
classification + governance metadata for all 127.

### Generalized cross-skill governance scanner — L
v5.0.0 ships the `final_marked` selector plus a **targeted** finance-placeholder
guard over a named allowlist — a presence-of-discipline check, not a runtime
scanner of emitted output. v5.1 builds the corpus-wide runtime data scanner
(every cell of every decision-grade skill checked at emit time for source-class
tagging and placeholder leakage), generalizing the `residential_multifamily`
machinery to the whole plugin.

Acceptance: a runtime scanner that tags/refuses emitted output across the
decision-grade corpus, with tests, not just the RMF subsystem.

### Four canonical connector contract schemas — M
`debt`, `entity`, `valuation`, and the promotion of `funds` (with investor
reporting) into a connector entity contract do not exist yet. The nine existing
contracts (`pms, gl, crm, ap, market_data, construction, hr_payroll,
manual_uploads, deal_pipeline`) are v5.0.0 stubs.

Acceptance: the four new contract schemas land with the `source_class`
provenance field and the `max_staleness` consume-time refusal **enforced** at a
connector runtime (specified in `docs/DATA_GRADES.md` §2 in v5.0.0; enforced in
v5.1).

### Valuation + investor connectors — L
Beyond the four contract schemas, the first valuation and investor-reporting
connectors (the AMOS-facing surfaces) move from contract to runnable adapter
against a sandbox.

Acceptance: a valuation connector and an investor-reporting connector at
`status: starter` (beyond `stub`), each runnable against a sandbox instance.

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

## Real-world data integration — connector track (v5.1 → v6, target: H2)

The deep connector buildout. v5.0.0 shipped the honest capability matrix and the
`source_class` / `max_staleness` contract spec; v5.1 lands the four canonical
contract schemas + the runtime that enforces them (see the v5.1 section above).
The vendor-specific adapters below sit on top of that and span v5.1 → v6.

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
- `status: beta_rc` → `status: stable`.
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
