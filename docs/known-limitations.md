# Known Limitations (v5.2.0)

> Status: released (v5.2.0)
> Owner: Mario Urquia
> Last reviewed: 2026-06-04
> Source-of-truth code this doc describes:
> - `scripts/governance-scan.py` (the corpus-wide **static** governance scanner shipped in v5.2.0)
> This is the honest, single-page statement of what v5.2.0 does **not** do.
> The README "Known Limitations" section summarizes these; this file is the
> long-form companion. If a v5 collateral piece implies more than this, it is wrong.

v5.2.0 is honest about its scope. It is a skill-contract + governance-metadata
foundation release: the full-corpus tiered skill contract, consumer-ready
forward-compat manifest fields (manifest contract `1.1`), a corpus-wide **static**
governance scanner (`scripts/governance-scan.py`), and the connector no-live
invariants — on top of v5.1.0's connector contract schemas + schema-enforced
`source_class` enum and v5.0.0's governable taxonomy and data-grade ladder. It does
**not** deliver universal **runtime** governance, live connectors, or an autonomous
orchestrator. The limitations below are deliberate and named.

## Governance and enforcement

- **No live connectors.** Every connector contract and every vendor adapter in
  the repo is `status: stub`. There is **no live API feed** to any system. The
  only `active` ingestion shape is a shared-drive / email **file drop**
  (Excel / manual upload). See [`docs/connectors/CAPABILITY-MATRIX.md`](connectors/CAPABILITY-MATRIX.md)
  for the per-vendor honest state (CoStar is **not-supported-live** per its AI-use
  T&C; Yardi / MRI / RealPage are **blocked-by-vendor**).

- **The corpus-wide governance scanner is STATIC; the generalized RUNTIME scanner
  remains deferred.** v5.2.0 ships `scripts/governance-scan.py`, a corpus-wide
  **static + generated-artifact** scanner that validates governance **declarations**
  over SKILL.md frontmatter + the generated catalog/manifest (per-rule severity;
  fixtures in `tests/test_governance_scan.py`). What it does **not** do — and what
  **remains deferred (v5.x)** — is **runtime** emitted-output enforcement: tagging
  or refusing every cell of every decision-grade skill *at emit time* (source-class
  tagging, refusal-on-missing-input, period-seal, the placeholder scanner). That
  machinery is **deployed and running only inside the `residential_multifamily`
  subsystem.** Across the rest of the corpus, the runtime leg is still the
  `final_marked` selector plus the **targeted finance-placeholder guard** on a named
  allowlist (`acquisition-underwriting-engine`, `ic-memo-generator`,
  `comp-snapshot`, `fund-lp-reporting`, `jv-waterfall-architect`,
  `opportunity-zone-underwriter`, `cost-segregation-analyzer`) — a
  **presence-of-discipline check**, not a runtime scanner of emitted output. Do not
  assume universal runtime enforcement.

- **The four connector contract schemas exist as stubs; the connector runtime does
  not.** `debt`, `entity` (legal/ownership cap-structure, distinct from
  `master_data`), `valuation`, and `funds` (+ pseudonymized `investor_report`) were
  authored in v5.1.0 as `status: stub` contracts conforming to the connector
  meta-schemas. `source_class` is now a schema-enforced enum
  (`_schema/source_class.yaml` + `entity_contract.schema.yaml` +
  `tests/test_connector_source_class.py`) and `max_staleness` is declared on the
  new contracts. **But nothing runs:** no adapter executes, no record is emitted,
  and the consume-time `max_staleness` refusal + `source_class` stamping at a
  connector runtime remain **deferred**. All 13 connector contracts (the 9 prior +
  these 4) are stubs; **0 are live/implemented.** The connector **runtime**
  (consume-time `max_staleness` refusal + `source_class` stamping at emit time) and
  any runnable / vendor adapters are the **v6** real-world-data track, **not** v5.x —
  see [`docs/ROADMAP.md`](ROADMAP.md). v5.x scope is limited to the static no-live
  invariants, schema validation, and (optionally) non-live interface scaffolding.

## Orchestration

- **The orchestrator runtime `dispatchAgent()` is a documented stub.** The
  autonomous engine that would sequence phases, poll agents, and aggregate
  verdicts is not the real execution path. The **real path is the orchestrate
  prose** (`src/commands/orchestrate.md`): Claude acts as the conductor following
  the documented phase + agent + verdict templates. Deal-state persistence, typed
  approval gates, and the calculator bridge have landed; full verdict aggregation
  and autonomous challenge-layer resolution remain in progress. Treat
  orchestrators as structured prompts, not fire-and-forget pipelines.

## Subsystem maturity

- **`residential_multifamily` is shakedown-pending.** The subsystem is
  `status: stable_pending_shakedown` (v1.0.0-rc1) — code-complete, with
  refusal-on-missing-input contracts active, but every reference file still ships
  as sample / starter / illustrative / placeholder. Decision-grade use requires an
  org overlay (the tailoring interview) to supply real data. Graduation to
  `status: stable` is gated on the first operator shakedown log (see
  [`docs/PREVIEW_MODE.md`](PREVIEW_MODE.md)).

- **Six regulatory / affordable-compliance workflows are phase-1 scaffolding.**
  `compliance_calendar_review`, `income_certification_cycle`, `rent_limit_test`,
  `agency_reporting_prep`, `file_audit_prep`, and `recertification_batch` are
  recognized by the router and have overlay slots, but **no workflow pack implements
  them yet**. The routing rule `r011_regulatory_workflow_explicit` is gated behind an
  explicit `regulatory_program` axis and `rent_limits` / `income_limits` reference
  files; missing references refuse the match. Making these runnable (LIHTC, Section 8
  HAP, rent stabilization, recapture math, HUD cycles) is **v6** work.

- **The tailoring TUI has open follow-ups.** Tailoring Pass 2 Objective 4 is
  **closed** — conflict surfacing, approval-floor guard, canonical-redefinition
  refusal, preview-bundle YAML emission, and missing-doc blocker are all implemented.
  Two follow-ups remain tracked in
  [`docs/tailoring_capability_matrix.md`](tailoring_capability_matrix.md):
  legacy-bank retirement (warn-on-load, then removal once orgs migrate) and
  role-based question-bank filtering (`load_question_banks()` currently loads every
  bank rather than filtering by the asker's role).

## Packaging and distribution

- **The Windows `.exe` is not locally buildable on macOS.** The Windows installer
  is produced on **CI / Windows only** (Inno Setup, `scripts/create-exe.iss`); it
  cannot be built from a macOS dev machine. The macOS DMG is locally buildable
  (`scripts/create-dmg.sh`).

- **The Windows installer does not halt on missing prerequisites.** `Install.ps1`
  defends against UTF-8 BOM edge cases under PowerShell 5.1 and logs detected
  Node / Python / npm versions, but it does **not** currently fail with a remediation
  step when those prerequisites are missing from `%PATH%`. A hard-fail
  (`Fail-If-Missing`) is tracked as future work.

- **The Codex / Gemini / Grok / Manus portable ZIP is experimental.** A structural
  smoke test (`tests/install_smoke/test_portable_zip.py` + the `Portable ZIP Smoke`
  workflow) validates ZIP layout, skills-tree mirroring, the frontmatter contract,
  and runtime-file exclusion. **Cross-runtime invocation** — a skill actually loading
  and running inside one of those CLIs — is **not** tested and remains an explicit
  gap. Treat those surfaces as experimental.

## AMOS integration

- **The AMOS manifest is a static export with no live coupling.**
  `dist/amos-skill-manifest.json` is a **generated artifact** documenting honest
  capability states. No skill is marked live-connected; AMOS references skills as
  data, it does not invoke them live (per AMOS ADR-0006). Regenerating the catalog
  regenerates the manifest; there is no runtime channel between the plugin and a
  running AMOS instance.

## See also

- [`docs/DATA_GRADES.md`](DATA_GRADES.md) — the data-grade ladder and which grades may back a final output.
- [`docs/connectors/CAPABILITY-MATRIX.md`](connectors/CAPABILITY-MATRIX.md) — honest per-vendor connector state.
- [`docs/integrations/amos-skill-manifest.md`](integrations/amos-skill-manifest.md) — the AMOS manifest contract.
- [`docs/MIGRATION.md`](MIGRATION.md) — the v4.5.0 → v5.0.0 migration.
- README [Known Limitations](../README.md#known-limitations) — the summary.
