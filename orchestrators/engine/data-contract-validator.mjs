/**
 * Data Contract Validator -- Validates phase output against a contract specification.
 *
 * Export: validateDataContract(phaseOutput, contractSpec)
 * Returns: { valid, missingKeys, typeErrors, warnings }
 */

// ---------------------------------------------------------------------------
// Safe path navigation (prototype-pollution-safe)
// ---------------------------------------------------------------------------

function safeNavigate(obj, path) {
  if (!obj || !path) return undefined;
  const parts = path.split('.');
  let current = obj;
  for (const part of parts) {
    if (current === null || current === undefined) return undefined;
    if (typeof current !== 'object') return undefined;
    const desc = Object.getOwnPropertyDescriptor(current, part);
    if (desc === undefined) return undefined;
    current = desc.value;
  }
  return current;
}

// ---------------------------------------------------------------------------
// Type checking
// ---------------------------------------------------------------------------

function checkType(value, expectedType) {
  if (expectedType === 'string') return typeof value === 'string';
  if (expectedType === 'number') return typeof value === 'number' && !Number.isNaN(value);
  if (expectedType === 'boolean') return typeof value === 'boolean';
  if (expectedType === 'object') return value !== null && typeof value === 'object' && !Array.isArray(value);
  if (expectedType === 'array') return Array.isArray(value);
  // Unknown type: accept anything
  return true;
}

function typeName(value) {
  if (value === null) return 'null';
  if (value === undefined) return 'undefined';
  if (Array.isArray(value)) return 'array';
  if (Number.isNaN(value)) return 'NaN';
  return typeof value;
}

// ---------------------------------------------------------------------------
// Contract validation
// ---------------------------------------------------------------------------

/**
 * Validate phase output against a data contract specification.
 *
 * @param {object} phaseOutput - The output data from a phase
 * @param {object} contractSpec - Contract spec where each key maps to { type, required, description }
 * @returns {{ valid: boolean, missingKeys: string[], typeErrors: Array<{key: string, expected: string, actual: string}>, warnings: string[] }}
 */
export function validateDataContract(phaseOutput, contractSpec) {
  const missingKeys = [];
  const typeErrors = [];
  const warnings = [];

  if (!contractSpec || typeof contractSpec !== 'object') {
    return { valid: true, missingKeys, typeErrors, warnings: ['No contract spec provided'] };
  }

  if (!phaseOutput || typeof phaseOutput !== 'object') {
    // If contract has any required keys, this is invalid
    const specKeys = Object.getOwnPropertyNames(contractSpec);
    for (const key of specKeys) {
      const spec = Object.getOwnPropertyDescriptor(contractSpec, key);
      if (spec && spec.value && spec.value.required) {
        missingKeys.push(key);
      }
    }
    return { valid: missingKeys.length === 0, missingKeys, typeErrors, warnings: ['Phase output is null or not an object'] };
  }

  const specKeys = Object.getOwnPropertyNames(contractSpec);

  for (const key of specKeys) {
    const specDesc = Object.getOwnPropertyDescriptor(contractSpec, key);
    if (!specDesc) continue;
    const spec = specDesc.value;
    if (!spec || typeof spec !== 'object') continue;

    // Navigate potentially dotted key paths in the output
    const value = key.includes('.') ? safeNavigate(phaseOutput, key) : (() => {
      const d = Object.getOwnPropertyDescriptor(phaseOutput, key);
      return d === undefined ? undefined : d.value;
    })();

    const isRequired = spec.required === true;
    const expectedType = spec.type;

    if (value === undefined || value === null) {
      if (isRequired) {
        missingKeys.push(key);
      } else {
        // Optional and missing: fine
      }
      continue;
    }

    // Type check
    if (expectedType && !checkType(value, expectedType)) {
      typeErrors.push({
        key,
        expected: expectedType,
        actual: typeName(value),
      });
    }
  }

  const valid = missingKeys.length === 0 && typeErrors.length === 0;
  return { valid, missingKeys, typeErrors, warnings };
}
