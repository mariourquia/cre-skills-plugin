# Orchestrator Engine v0 — Design Reference

v4.4 scope, in progress. Captures what the existing executor
(`src/orchestrators/engine/executor.mjs`) does today, what v4.4 adds on
top of it, and the acceptance criteria for each increment. This
document is the source of truth for the orchestrator-v0 work; the
roadmap issue body points here.

## What exists on `main` today

- `src/orchestrators/engine/executor.mjs` — CLI-driven runner with arg
  parsing, pipeline config loading, phase dispatch (stubbed agent
  calls), checkpoint write/read, final verdict aggregation.
- `src/orchestrators/engine/handoff-router.mjs` — cross-pipeline hand-
  off routing.
- `src/orchestrators/engine/challenge-executor.mjs` — challenge-layer
  executor (the adversarial review step).
- `src/orchestrators/engine/data-contract-validator.mjs` — per-phase
  contract validation.
- `src/orchestrators/engine/agent-loader.mjs` — agent registry.
- `src/orchestrators/configs/*.json` — 10 pipeline configs (acquisition,
  capital-stack, development, disposition, fund-management,
  hold-period, investment-strategy, lp-intelligence,
  portfolio-management, research-intelligence).
- `src/orchestrators/schemas/` — disagreement and reversal-trigger
  schemas.

The executor today does phase sequencing, dispatch stubbing, and
checkpoint writing. It **does not yet** do persistent deal-scoped
state, typed approval gates, variant selection, or calculator tool
calls directly.

## v4.4 additions

Each item below lands as a self-contained PR, not a single megaPR.

### 1. Persistent deal-scoped state

**What:** `~/.claude/cre-skills/deals/<deal_id>/state.json` carries the
full orchestrator state so a session can be interrupted and resumed
days later.

**Schema:** `src/orchestrators/schemas/deal_state.schema.json` (added
in this commit). Keys:

- `deal_id` (string, UUID or operator slug)
- `pipeline` (string, one of 10 orchestrator ids)
- `variant` (string, optional — e.g. `value_add`, `core_plus`)
- `phase_history` (array of completed phase outcomes)
- `current_phase` (string)
- `verdicts_by_phase` (object keyed by phaseId → {verdict, rationale, timestamp})
- `approval_gate_log` (array of approval-gate events)
- `created_at`, `updated_at` (ISO-8601)
- `run_id` (executor run UUID)

**Acceptance:** executor --resume <deal_id> reads state.json and
continues. Integration test writes state, kills process, resumes,
asserts continuation.

### 2. Typed approval gates

**What:** Each orchestrator phase may declare an `approval_gate`
block. When the executor reaches it, progression blocks until the gate
is cleared in the state file (human signs off).

**Schema:** added to `src/orchestrators/schemas/approval_gate.schema.json`.
Keys:
- `gate_id` (string, unique within pipeline)
- `required_approvers` (array of role strings, from approval_matrix.md)
- `approval_matrix_row` (integer, cites which row authorizes)
- `evidence_required` (array of artifact paths)
- `status` (one of: `pending`, `approved`, `approved_with_conditions`,
  `denied`, `expired`)
- `approved_at`, `approved_by`, `conditions_text`

**Acceptance:** executor refuses to enter the next phase until every
declared gate in the current phase is `approved` or
`approved_with_conditions`. Integration test: set up acquisition
pipeline with a gate on phase `ic-memo`, confirm executor halts with
`awaiting_approval` verdict.

### 3. Calculator tool-calling

**What:** Orchestrator phases can declare a `tool_calls` list that
invokes a calculator directly rather than emitting Python code back
to the user.

**Wiring:** new helper at `src/orchestrators/engine/calculator-bridge.mjs`
that invokes `scripts/calculator-invoker.py` with typed inputs and
returns typed outputs. MCP server exposes the same surface for IDEs.

**Acceptance:** a phase that declares `tool_calls: [{tool:
"debt-sizing", inputs: {...}}]` receives the structured result
without the user manually running the calculator.

### 4. Variants per firm type

**What:** An orchestrator config may branch by variant. Current
configs already read a `--strategy` flag (core-plus, value-add, etc.)
but do not route to variant-specific phase lists. v4.4 adds a
`variants/<variant_slug>/` directory under each orchestrator config
dir whose contents override phase lists / agent weights / approval
matrices / examples.

**First example:** `src/orchestrators/configs/acquisition/variants/value_add/`
with:
- `phases.json` — override
- `approval_matrix.yaml` — tighter approval thresholds for value-add
  (higher capex → more scrutiny)
- `example_deal.json`

**Acceptance:** `executor --pipeline acquisition --strategy value_add`
loads the variant's phase list; integration test asserts phase
sequencing matches the variant override.

### 5. Human-in-the-loop audit log

**What:** Every approval-gate decision appends to
`~/.claude/cre-skills/deals/<deal_id>/audit_log.jsonl` with the same
event schema as `approval_audit_log.jsonl` in the residential_multifamily
subsystem (event, actor, timestamp, gate_id, approval_matrix_row,
evidence_hashes).

**Acceptance:** audit log grows monotonically; test verifies no
in-place rewrites.

## What's explicitly NOT in v4.4

- Full replacement of the agent-dispatch stub with live Claude API
  calls. Today agents return stub payloads; v4.4 keeps that behavior.
  Live agent dispatch lands in v5.0 alongside the real-world data
  connectors.
- Multi-tenant orchestration (one deal at a time per host).
- Remote state storage. Local JSON only.

## Implementation order

1. Add schemas (this commit).
2. Wire approval-gate helper into the existing executor (separate PR).
3. Add calculator-bridge (separate PR).
4. Add first variant + integration test (separate PR).
5. Wire persistent state + audit log (separate PR).

Every step is test-first.
