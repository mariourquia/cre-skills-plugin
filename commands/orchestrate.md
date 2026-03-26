---
name: orchestrate
description: "Run a CRE workflow orchestrator -- coordinates multiple skills and agents into a multi-phase pipeline with checkpoints, verdicts, and challenge layers. Available orchestrators: acquisition, capital-stack, hold-period, disposition, development, fund-management, research, strategy, portfolio, lp-intelligence."
---

# CRE Orchestrator

You are orchestrating a multi-agent CRE workflow pipeline. Follow these steps precisely.

## Step 1: Parse the Request

Extract the orchestrator name from the user's input. Map shorthand names to config files:

| Input | Config File |
|-------|------------|
| `acquisition` | `orchestrators/configs/acquisition.json` |
| `capital-stack` | `orchestrators/configs/capital-stack.json` |
| `hold-period` | `orchestrators/configs/hold-period.json` |
| `disposition` | `orchestrators/configs/disposition.json` |
| `development` | `orchestrators/configs/development.json` |
| `fund-management` | `orchestrators/configs/fund-management.json` |
| `research` | `orchestrators/configs/research-intelligence.json` |
| `strategy` | `orchestrators/configs/investment-strategy.json` |
| `portfolio` | `orchestrators/configs/portfolio-management.json` |
| `lp-intelligence` | `orchestrators/configs/lp-intelligence.json` |

If the user does not specify an orchestrator, list all 10 with one-line descriptions and ask which to run.

## Step 2: Load the Orchestrator

1. Read the orchestrator config JSON from `orchestrators/configs/{name}.json`.
2. Read the orchestrator prompt from `orchestrators/prompts/{prompt-file}.md`. Map orchestrator IDs to prompts:
   - `acquisition` -> `master-orchestrator.md` (uses phase-level prompts for DD, UW, financing, legal, closing)
   - `capital-stack` -> `financing-orchestrator.md`
   - `hold-period` -> `asset-management-orchestrator.md`
   - `disposition` -> `disposition-orchestrator.md`
   - `development` -> uses phase-level prompts as defined in config
   - `fund-management` -> `fund-management-orchestrator.md`
   - `research` -> `research-intelligence-orchestrator.md`
   - `strategy` -> `investment-strategy-orchestrator.md`
   - `portfolio` -> `portfolio-management-orchestrator.md`
   - `lp-intelligence` -> `lp-intelligence-orchestrator.md`
3. Read `orchestrators/thresholds.json` for verdict thresholds.
4. If the user specifies an investor type, read the matching investor profile from `orchestrators/investor-profiles/{type}.json` and merge thresholds per the `thresholdSelectionProtocol` in `thresholds.json`.

## Step 3: Confirm Pipeline Scope

Before launching, confirm with the user:
- **Orchestrator**: Name and description from the config.
- **Phases**: List each phase name and weight.
- **Entity**: What deal, property, fund, or portfolio is being evaluated. Gather required inputs if not already provided.
- **Investor type**: If applicable, which investor profile to apply. If unspecified, use base thresholds.
- **Challenge layer**: Whether to run the post-pipeline challenge layer (default: yes for acquisition, no for others).

Wait for user confirmation before proceeding.

## Step 4: Execute Phase by Phase

For each phase in the orchestrator config, in declared order:

### 4a. Check Dependencies
- Verify all `upstreamDependencies` have status COMPLETED or CONDITIONAL.
- Verify all `requiredDataKeys` from upstream phases are available.
- If an `earlyStartCriteria` is defined and met, launch eligible agents early.

### 4b. Dispatch Agents
For each agent defined in the phase:
1. Read the agent's markdown file (from `agents/` directory).
2. Read all `skillRefs` referenced by the agent (from `skills/` directory).
3. Dispatch the agent as a subagent (using the Agent tool) with:
   - The agent prompt (from its .md file)
   - The skill methodology (from skillRefs)
   - The deal/property/fund data
   - Any upstream phase outputs
   - The applicable thresholds (base or investor-type-merged)
4. Agents with no declared `dependencies` within the phase may be dispatched in parallel.
5. Agents with dependencies wait for the specified upstream agents to complete.

### 4c. Collect and Validate
- Collect each agent's output: findings, red flags, data gaps, metrics, and recommendations.
- Apply `validationRules` from the config. Retry agents that fail validation (up to retry limits).
- Write a checkpoint for each agent.

### 4d. Phase Verdict
Apply the phase's `verdictLogic`:
- Check pass/fail/conditional thresholds.
- Check dealbreaker conditions.
- Check minimum agent completion requirements.
- Produce a phase verdict: typically COMPLETED, CONDITIONAL, or FAILED.
- If FAILED and the phase is critical, halt the pipeline and report to the user.

### 4e. Report Phase Results
After each phase completes, report to the user:
- Phase name and verdict
- Key findings (top 3-5)
- Red flags (if any)
- Data gaps (if any)
- Key metrics produced
- Recommendation for next phase

Ask whether to proceed to the next phase, adjust inputs, or abort.

## Step 5: Pipeline Verdict

After all phases complete, apply the orchestrator-level verdict logic:
- Aggregate phase verdicts and agent outputs.
- Apply the verdict vocabulary from `checkpointConfig.verdictValues` (e.g., GO/CONDITIONAL/NO-GO, SELL/HOLD/REFI, BUILD/KILL/DEFER).
- List conditions precedent if the verdict is CONDITIONAL.
- Quantify key metrics across the pipeline.

## Step 6: Challenge Layer (Optional)

If the challenge layer is enabled:

1. Read `orchestrators/challenge-layer/config.json`.
2. **Tier 1** (always-run): Dispatch all 8 perspective agents sequentially with the pipeline outputs and verdict.
3. **Tier 2** (conditional): Evaluate each trigger condition against the deal data. For triggered groups, dispatch agents in parallel.
4. **Tier 3** (on-request): Ask the user if any additional perspectives are desired.
5. **Synthesis**: The Deal Team Lead agent synthesizes all challenge outputs into:
   - Challenge summary
   - Verdict confirmation or revision
   - Unresolved disagreements (using `schemas/disagreement.schema.json` format)
   - Conditions precedent
   - IC recommendation

## Step 7: Final Report

Produce a structured final report:

### Pipeline Report: {Orchestrator Name}
- **Entity**: {deal/property/fund name}
- **Investor Type**: {type or "base thresholds"}
- **Verdict**: {FINAL VERDICT}
- **Conditions Precedent**: {if CONDITIONAL, list all conditions}

#### Phase Summary
| Phase | Verdict | Key Findings | Red Flags |
|-------|---------|-------------|-----------|
| {phase 1} | {verdict} | {findings} | {flags} |
| ... | ... | ... | ... |

#### Key Metrics
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| {metric} | {value} | {threshold} | PASS/FAIL |

#### Challenge Layer (if run)
- **Verdict Change**: {confirmed / revised from X to Y}
- **Unresolved Disagreements**: {count and summary}
- **Reversal Triggers**: {active triggers with probabilities}

#### Recommendations
{Numbered list of recommended actions}

#### Cross-Chain Handoff
If the verdict triggers a cross-chain handoff (per `engine/handoff-registry.json`), note the next orchestrator and the data that would flow to it.

## Error Handling

- If an agent fails after retries, log the failure, mark it in the checkpoint, and continue with remaining agents (per `failurePolicy: continue-on-agent-failure`).
- If a critical agent fails and cannot be retried, halt the phase and report to the user with options: skip the agent, provide manual input, or abort the pipeline.
- If the user requests a pause, write all checkpoints and report resumption instructions.

## Notes

- All orchestrator configs conform to `orchestrators/engine/pipeline-engine-schema.json`.
- Cross-chain handoffs follow contracts in `orchestrators/engine/handoff-registry.json`.
- Investor-type thresholds are merged per the protocol in `orchestrators/thresholds.json`.
- The challenge layer is most valuable for acquisition pipelines but can be applied to any orchestrator.
