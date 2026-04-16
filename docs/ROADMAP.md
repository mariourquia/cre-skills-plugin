# Public Roadmap

Last updated: 2026-04-16 · Plugin version: v4.2.0

This is the plan for where `cre-skills-plugin` goes from here. It groups
the pending work by release and by track. Items carry a size (S / M / L /
XL), dependencies, and explicit acceptance criteria so outside contributors
can pick up any row and know what "done" means.

Conventions:

- **S** ≈ half a day. **M** ≈ 2–5 days. **L** ≈ 1–3 weeks. **XL** ≈ a quarter.
- Items without an owner are open for contribution.
- "Stable" status on a subsystem means: no placeholder data in final-marked
  paths, decision-grade contract enforced by tests, overlay docs complete,
  and at least one real-operator shakedown on file.

## Current release: v4.2.0 (2026-04-16)

Internal-beta hardening close. `residential_multifamily` at `beta_rc`
(v0.6.0). See `docs/releases/v4.2.0-release-notes.md` and
`docs/implementation_hardening_status.md`. Remaining-pass-2 deferred items
moved into v4.3 below.

---

## v4.3 — Near-term hardening (target: 4–6 weeks)

Goal: finish the remaining non-enhancement items from pass 2, unlock the
first round of behavioral tests beyond structural integrity, and land the
preview-mode gate.

### Preview / staging mode (cat 1, last bullet) — S
Flag any `status: beta_rc` or `status: experimental` skill in output so a
human reviewer can block it before a decision-grade artifact leaves the
system. See `docs/PREVIEW_MODE.md` for the spec.

Acceptance:
- `docs/PREVIEW_MODE.md` describes the contract.
- Every beta_rc / experimental SKILL.md carries a boxed banner marker.
- `tests/test_preview_mode_gate.py` fails if the marker is absent or if a
  final-marked workflow runs without a staging-mode acknowledgement flag.

### Runtime template resolver (Obj 2b) — M
Today `reference_manifest.yaml` declares `fallback_behavior` values like
`use_prior_period`, `use_portfolio_average`, `proceed_with_default`. The
runtime does not carry an explicit confidence downgrade through to the
output when it takes those paths.

Acceptance: a runtime resolver helper that, on non-`refuse` fallback, tags
the output cell's provenance (source-class per Obj 8 contract) as
`[overlay:fallback]` and emits a log line.

### Tailoring pass 2 (Obj 4 continued) — L
Four items listed in `docs/tailoring_capability_matrix.md` as **Not
implemented**:

1. Approval-floor refusal (tailoring cannot lower an approval threshold).
2. Canonical-definition redefinition refusal (cannot rename a canonical
   metric/type).
3. Preview-bundle YAML emission (operator can review all diffs before
   commit).
4. Missing-doc blocker transitions (if a question bank trigger has no doc
   catalog entry, the TUI refuses instead of silently collapsing).

Acceptance: each of the four gains a test assertion in
`test_tailoring_tui.py` and a corresponding implementation; capability
matrix doc flips each to **Implemented**.

### Install smoke tests (Obj 11 continued) — M
Six cells marked `gap` in `docs/install_smoke_test_matrix.md`:

1. Upgrade (v4.1.x → v4.2.0).
2. Uninstall then reinstall.
3. Corrupted-config recovery.
4. Cowork ZIP import smoke.
5. Portable ZIP import smoke.
6. Claude Desktop chat-tab manual MCP handshake smoke.

Acceptance: each cell flips to `covered` with a backing test path under
`tests/install_smoke/`.

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

## v5.0 — Real-world data integration (target: H2)

This is a breaking release because the connector contract hardens.

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
