# Acquisition · value_add variant

One of three v4.4 variants on the acquisition orchestrator
(core_plus / value_add / opportunistic). Each variant overrides phase
weights, the approval matrix, and the example deal so a firm can pick
the closest match to their investment thesis without rebuilding the
orchestrator.

## What this variant overrides

- Phase weight shift: due-diligence stays at 0.25, but underwriting
  gains weight (0.30) and legal gains weight (0.15) because value-add
  deals carry more execution risk at those stages.
- Approval matrix: capex approval floor drops from $250K to $100K —
  more scrutiny on the capex plan because the thesis depends on it.
- Example deal: value-add multifamily, 240 units, going-in cap 5.2%,
  stabilized cap 6.1%, $18k/unit capex.

## Files

- `phases.json` — phase overrides. Keys merge over the base acquisition
  config; any key present here wins.
- `approval_matrix.yaml` — approval-floor overrides.
- `example_deal.json` — illustrative deal for tests and walkthroughs.

## How the executor loads a variant

```
node src/orchestrators/engine/executor.mjs \\
  --pipeline acquisition \\
  --strategy value_add \\
  --deal-id sample_value_add_01
```

The executor (v4.4+) reads the base config at
`src/orchestrators/configs/acquisition.json`, then merges any files
under `src/orchestrators/configs/acquisition/variants/value_add/`.
Variant files never add phases that the base does not declare; they
can only override weights, thresholds, and example data. New phases
belong in the base config.

## Acceptance criteria (v4.4)

- `phases.json` loads and merges cleanly.
- `approval_matrix.yaml` loads with lower capex threshold than base.
- Integration test asserts the executor emits a phase plan whose
  underwriting weight equals 0.30 when variant = value_add.
