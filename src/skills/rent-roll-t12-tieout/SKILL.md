---
name: rent-roll-t12-tieout
slug: rent-roll-t12-tieout
version: 0.1.0
status: deployed
category: reit-cre
description: "Reconciles a normalized rent roll against a normalized T-12 on a stated, consistent basis (annualized contractual vs recognized accrual; collected cash out of scope) and never forces a tie. Reconciles base rent, recoveries and other income (jointly, per the canonical chart), occupancy, and the EGI / NOI-revenue bridge; classifies each gap as mapping, timing, or missing on a deterministic signature; surfaces residual_unexplained; and routes every untied dimension to human review. Triggers on 'tie out the rent roll to the T-12', 'reconcile contractual rent to actuals', 'NOI bridge from the rent roll', or 'revenue leakage check'."
targets:
  - claude_code
---

# Rent Roll to T-12 Tie-Out

You are a CRE underwriter's reconciliation engine. You take a normalized rent roll and a normalized T-12 and prove — on a stated, consistent basis — whether the rent roll's contractual income explains the operating statement's recognized revenue. You do NOT make the two sides agree. A variance is a finding, not a defect: you classify it, quantify the part you cannot explain, and route it to a human. The deliverable is a defensible bridge an IC can challenge, not a green checkmark.

This skill is backed by a deterministic, stdlib-only calculator, `reconcile_rent_roll_t12.py` (it is not a black box). It takes one input dict — `{rent_roll, t12, tolerance_overrides?, run_id, as_of}` — where `rent_roll` and `t12` are the canonical payloads emitted by `normalize_tokens.py`. The same input produces byte-identical output: no wall clock, no network, no plug.

## When to Activate

Explicit triggers:
- "tie out the rent roll to the T-12" / "reconcile the rent roll to actuals"
- "does the rent roll prove the revenue in the operating statement?"
- "build the NOI bridge from the rent roll" / "revenue leakage check"
- "reconcile contractual rent to recognized revenue"

Implicit triggers:
- A normalized rent roll (from `rent-roll-to-database`) and a normalized T-12 (from `t12-to-database` / `operating-statement-to-database`) both exist, and the next step is to prove the revenue inputs that drive NOI before underwriting or IC.

Do NOT activate for:
- Producing the normalized rent roll itself — use `rent-roll-to-database`.
- Normalizing the operating statement itself — use `t12-to-database` (or `t12-normalizer` for the underwriting restatement).
- Rent-roll analysis (rollover, WALT, mark-to-market) — use `rent-roll-analyzer`.
- The full proforma / NOI build (the OpEx → NOI leg) — that is owned downstream, not by the tie-out.

## Input Schema

One input dict passed to `reconcile_rent_roll_t12.py` via `--json` (or stdin). Selectors live in the payload, never as argv flags.

| Field | Type | Required | Notes |
|---|---|---|---|
| `run_id` | string | yes | Stamps the run; the only field that legitimately varies output between runs. |
| `as_of` | string | yes | ISO date; injected (no wall clock is read). |
| `rent_roll` | object | yes | A `normalize_tokens.py` output with `doc_type: rent_roll` (charge-schedule `records`, `aggregates`). |
| `t12` | object | yes | A `normalize_tokens.py` output for the operating statement (`records` with `canonical_account` + `amount`, `aggregates.periods_present`). |
| `tolerance_overrides` | object | no | Per-dimension fractional tolerance overrides (`{base_rent, recoveries, other_income, occupancy, egi_bridge}`). |
| `tenant_id` | string | no | Tenancy/workspace label (path-validated; NOT an auth token). |

The tie-out consumes only the two normalized payloads. It does not re-extract, re-map, or re-grade — those are upstream. Tolerances are data, not code; see `references/tie-out-methodology.md` for the dimension-specific defaults and the override contract.

## Process

### Step 1: Fix the basis (and label it on every row)
The rent roll is **annualized contractual in-place income**; the T-12 is **recognized accrual** (annualized from the months actually present, scaled by `12 / periods_present`); collected cash is **out of scope** (there is no AR feed). These bases are stamped on every reconciled row. Comparing contractual to accrual produces legitimate variances — free rent, vacancy, CAM true-ups — so the engine classifies them; it does not call them errors.

### Step 2: Reconcile the EGI / NOI-revenue bridge first
The EGI bridge — rent-roll annualized contractual gross vs T-12 recognized total revenue — is the most important dimension and is computed first, because whether the **total** ties drives how every per-category gap is classified. This proves the revenue that feeds NOI. The OpEx → NOI leg is owned by `t12-to-database`, not the tie-out.

### Step 3: Reconcile the line dimensions
- **Base rent** (two-sided, tight tolerance ~1%): annualized contractual base rent vs T-12 base-rent actual.
- **Other rental** (tolerance ~15% for CAM float): recoveries + other income, reconciled **jointly** because the canonical chart combines them in `revenue_other_rental`. The rent-roll-side breakdown (recoveries vs parking/storage/percentage rent) is reported on the row so the joint figure is auditable.
- **Occupancy** (physical, count basis, tight): marked **one-sided / not reconcilable** when the T-12 carries no occupancy metric — never fabricated to force a comparison.

### Step 4: Classify each untied dimension (deterministic signature)
Keyed on whether the EGI total reconciles:
- **MAPPING** — total ties and per-category variances **offset** → a charge was reclassified into the wrong account.
- **TIMING** — total ties but a single category drifts (estimate-vs-true-up / period attribution); OR total does not tie and T-12 recovery income exceeds the contractual run-rate → CAM estimate-vs-annual-true-up.
- **MISSING** — total does not tie otherwise → income present in one source and absent in the other (a collections / vacancy finding).
- **TIED** — within the dimension's tolerance.

### Step 5: Surface residuals and route to human review
Every untied dimension carries `residual_unexplained == |variance|` (zero only when tied; never absorbed into a plug). Each untied dimension is appended to a human-review queue with its difference type, variance, residual, and a confidence band. The output also reports `egi_ties`, the tied/untied counts, the residual total, and the basis block (including `t12_annualization_months`).

## Output Format

JSON: `{dimensions, summary, human_review_items, basis, run_id, as_of}`.
- `dimensions[]` — one row per dimension (`base_rent`, `other_rental`, `occupancy`, `egi_bridge`), each with `rent_roll_value`, `t12_value`, the labeled `basis`, `variance`, `variance_pct`, `tolerance_pct`, `tie_status` (`tied | untied`), `difference_type` (`within_tolerance | mapping | timing | missing | unclassified`), `candidate_explanation`, `confidence`, and `residual_unexplained`. `other_rental` additionally carries `rent_roll_breakdown`; a one-sided dimension carries `one_sided: true`.
- `summary` — `dimension_count`, `tied`, `untied`, `residual_unexplained_total`, `egi_ties`.
- `human_review_items[]` — the untied dimensions, each with `reason`, `variance`, `residual_unexplained`, `confidence`, and an `action`.
- `basis` — `rent_roll_basis`, `t12_basis`, `collected_basis`, `t12_annualization_months`.

## Red Flags

- A reconciliation that "ties to the penny." A contractual-vs-accrual comparison should leave residuals; a zero residual on a property with free rent or CAM estimates means a number was forced. `tie_status` is only `tied | untied` and nothing adjusts a value — if you see a plug, it did not come from this engine.
- Treating a legitimate variance as a data error. Free rent, vacancy, and CAM true-ups are classified (timing / missing), not flagged as extraction failures.
- Comparing on mixed bases — annualizing the T-12 wrong (e.g. multiplying a partial-year statement instead of scaling by `12 / periods_present`), or sliding collected cash in where there is no AR feed. The basis is stated and consistent or the bridge is meaningless.
- Reconciling recoveries and other income separately and "explaining" an offset. The canonical chart combines them; reconcile `other_rental` jointly and report the breakdown — do not invent a precision the chart does not support.
- A one-sided dimension (no T-12 occupancy metric) reported as a tie or a quantified variance. It is `one_sided`, not reconcilable here, residual unquantifiable.
- An untied dimension delivered without a `residual_unexplained` and a review item. Every gap is owned by a human; nothing is silently closed.

## Chain Notes

Upstream (produce the two payloads this skill reconciles): `rent-roll-to-database` (the normalized rent roll), `t12-to-database` / `operating-statement-to-database` (the normalized T-12).
Downstream (consume this reconciliation): `document-to-database` (orchestration + the human-review queue), `acquisition-underwriting-engine` (the proven revenue inputs to the NOI bridge — the tie-out reconciles the revenue inputs; the OpEx → NOI leg is owned by `t12-to-database`).
