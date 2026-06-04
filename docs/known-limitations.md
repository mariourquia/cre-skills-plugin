# Known Limitations (v5.0.0)

> Status: released (v5.0.0)
> Owner: Mario Urquia
> Last reviewed: 2026-06-03
> This is the honest, single-page statement of what v5.0.0 does **not** do.
> The README "Known Limitations" section summarizes these; this file is the
> long-form companion. If a v5 collateral piece implies more than this, it is wrong.

v5.0.0 is honest about its scope. The release delivers a governable skill
taxonomy, an AMOS skill-manifest export, a canonical data-grade ladder, and a
targeted finance-placeholder guard. It does **not** deliver universal runtime
governance, live connectors, or an autonomous orchestrator. The limitations below
are deliberate and named.

## Governance and enforcement

- **No live connectors.** Every connector contract and every vendor adapter in
  the repo is `status: stub`. There is **no live API feed** to any system. The
  only `active` ingestion shape is a shared-drive / email **file drop**
  (Excel / manual upload). See [`docs/connectors/CAPABILITY-MATRIX.md`](connectors/CAPABILITY-MATRIX.md)
  for the per-vendor honest state (CoStar is **not-supported-live** per its AI-use
  T&C; Yardi / MRI / RealPage are **blocked-by-vendor**).

- **The generalized cross-skill governance scanner is v5.1.** Decision-grade
  runtime enforcement (source-class tagging, refusal-on-missing-input,
  period-seal, the placeholder scanner) is **deployed and running only inside the
  `residential_multifamily` subsystem.** Across the rest of the corpus, v5.0.0
  ships the `final_marked` selector plus the **targeted finance-placeholder guard**
  on a named allowlist (`acquisition-underwriting-engine`, `ic-memo-generator`,
  `comp-snapshot`, `fund-lp-reporting`, `jv-waterfall-architect`,
  `opportunity-zone-underwriter`, `cost-segregation-analyzer`). That guard is a
  **presence-of-discipline check**, not a runtime scanner of emitted output. A
  fully-generalized, corpus-wide runtime data scanner (every cell of every skill
  checked at emit time) is a **v5.1** item. Do not assume universal enforcement.

- **The four canonical connector contract schemas are v5.1.** `debt`, `entity`,
  `valuation`, and the promotion of `funds` (with investor reporting) into a
  connector entity contract do **not** exist in the repo yet. The nine existing
  connector contracts (`pms, gl, crm, ap, market_data, construction, hr_payroll,
  manual_uploads, deal_pipeline`) are v5.0.0 stubs. The `source_class` provenance
  field and `max_staleness` consume-time refusal are **specified** (and crosswalked
  in [`docs/DATA_GRADES.md`](DATA_GRADES.md) §2) but the connector runtime that
  emits and enforces them is **v5.1**.

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

## Packaging and distribution

- **The Windows `.exe` is not locally buildable on macOS.** The Windows installer
  is produced on **CI / Windows only** (Inno Setup, `scripts/create-exe.iss`); it
  cannot be built from a macOS dev machine. The macOS DMG is locally buildable
  (`scripts/create-dmg.sh`).

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
