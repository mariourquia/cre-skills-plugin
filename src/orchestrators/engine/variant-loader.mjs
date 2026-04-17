/**
 * variant-loader.mjs
 *
 * Resolves and applies variant overlays on top of a base pipeline
 * config. See docs/orchestrator-v0-design.md section 4.
 *
 * A variant lives at
 *   src/orchestrators/configs/<pipeline>/variants/<variant>/
 * and contains at minimum a `phases.json` with the shape:
 *   {
 *     "variant": "<slug>",
 *     "description": "...",
 *     "phase_weight_overrides": { "<phase_id>": <weight>, ... },
 *     "added_approval_gates": [
 *       { "gate_id": "...", "phase": "...", "required_approvers": [...],
 *         "approval_matrix_row": <int>, "evidence_required": [...] }
 *     ]
 *   }
 *
 * This loader is deliberately narrow: it does NOT read the variant's
 * `approval_matrix.yaml` (that file drives the human-facing approval
 * matrix and zero-dep Node has no YAML parser). The executor consumes
 * only weight overrides and the added_approval_gates list.
 */

import { readFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const VARIANT_SLUG_RE = /^[a-z][a-z0-9_]{0,64}$/;

export function variantDir(pluginRoot, pipelineId, variantSlug) {
  return join(
    pluginRoot,
    'orchestrators',
    'configs',
    pipelineId,
    'variants',
    variantSlug,
  );
}

export function variantExists(pluginRoot, pipelineId, variantSlug) {
  if (!variantSlug) return false;
  if (!VARIANT_SLUG_RE.test(variantSlug)) return false;
  const dir = variantDir(pluginRoot, pipelineId, variantSlug);
  if (!existsSync(dir)) return false;
  try {
    return statSync(dir).isDirectory();
  } catch {
    return false;
  }
}

export function loadVariantOverlay(pluginRoot, pipelineId, variantSlug) {
  if (!variantExists(pluginRoot, pipelineId, variantSlug)) {
    return null;
  }
  const phasesPath = join(
    variantDir(pluginRoot, pipelineId, variantSlug),
    'phases.json',
  );
  if (!existsSync(phasesPath)) {
    throw new Error(
      `Variant "${variantSlug}" for pipeline "${pipelineId}" is missing phases.json at ${phasesPath}`,
    );
  }
  const overlay = JSON.parse(readFileSync(phasesPath, 'utf-8'));
  if (overlay.variant !== variantSlug) {
    throw new Error(
      `Variant file declares variant="${overlay.variant}" but was loaded as "${variantSlug}"`,
    );
  }
  return overlay;
}

/**
 * Apply a variant overlay to a base pipeline config. Returns a new
 * config object; does not mutate the input. If overlay is null,
 * returns the base config unchanged.
 *
 * Merge rules:
 *  - phase_weight_overrides: override each phase's `weight`. Unknown
 *    phase ids raise (the variant references a phase the base doesn't
 *    declare — that's a variant authoring bug).
 *  - added_approval_gates: for each gate whose `phase` matches a base
 *    phase, append a sanitized gate spec to that phase's
 *    `approval_gates` array (creating it if absent).
 */
export function applyVariantOverlay(baseConfig, overlay) {
  if (!overlay) return baseConfig;

  const basePhaseIds = new Set((baseConfig.phases || []).map((p) => p.phaseId));
  const weightOverrides = overlay.phase_weight_overrides || {};
  const addedGates = overlay.added_approval_gates || [];

  for (const phaseId of Object.keys(weightOverrides)) {
    if (!basePhaseIds.has(phaseId)) {
      throw new Error(
        `Variant "${overlay.variant}" overrides weight on unknown phase "${phaseId}"`,
      );
    }
  }
  for (const gate of addedGates) {
    if (!gate.phase || !basePhaseIds.has(gate.phase)) {
      throw new Error(
        `Variant "${overlay.variant}" adds approval gate on unknown phase "${gate.phase}"`,
      );
    }
    if (!gate.gate_id) {
      throw new Error(
        `Variant "${overlay.variant}" has an approval gate missing gate_id`,
      );
    }
  }

  const merged = {
    ...baseConfig,
    variant: overlay.variant,
    phases: (baseConfig.phases || []).map((phase) => {
      const newPhase = { ...phase };
      if (phaseId_has(weightOverrides, phase.phaseId)) {
        newPhase.weight = weightOverrides[phase.phaseId];
      }
      const gatesForThisPhase = addedGates
        .filter((g) => g.phase === phase.phaseId)
        .map(sanitizeGateSpec);
      if (gatesForThisPhase.length > 0) {
        newPhase.approval_gates = [
          ...(phase.approval_gates || []),
          ...gatesForThisPhase,
        ];
      }
      return newPhase;
    }),
  };

  return merged;
}

function phaseId_has(obj, key) {
  return Object.prototype.hasOwnProperty.call(obj, key);
}

function sanitizeGateSpec(gate) {
  return {
    gate_id: gate.gate_id,
    required_approvers: gate.required_approvers || [],
    approval_matrix_row: gate.approval_matrix_row,
    evidence_required: gate.evidence_required || [],
  };
}
