/**
 * Profile Loader -- Loads investor profile JSON files with alias resolution.
 *
 * Export: loadProfile(investorType, pluginRoot)
 * Returns: parsed profile object
 */

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

// ---------------------------------------------------------------------------
// Alias map: shorthand -> canonical profile filename (without .json)
// ---------------------------------------------------------------------------

const ALIASES = Object.create(null);
ALIASES['pension-fund'] = 'institutional';
ALIASES['endowment'] = 'institutional';
ALIASES['sovereign-wealth'] = 'institutional';
ALIASES['pe'] = 'private-equity';
ALIASES['private-equity-fund'] = 'private-equity';
ALIASES['family-office'] = 'family-office';
ALIASES['familyOffice'] = 'family-office';
ALIASES['hnw'] = 'individual-hnw';
ALIASES['high-net-worth'] = 'individual-hnw';
ALIASES['individual'] = 'individual-hnw';
ALIASES['small-operator'] = 'small-operator';
ALIASES['operator'] = 'small-operator';
ALIASES['syndicator'] = 'syndicator';
ALIASES['reit'] = 'reit';

// ---------------------------------------------------------------------------
// Profile loader
// ---------------------------------------------------------------------------

/**
 * Load an investor profile from the investor-profiles directory.
 *
 * @param {string} investorType - Investor type name or alias
 * @param {string} pluginRoot - Absolute path to the plugin root directory
 * @returns {object} Parsed profile JSON
 * @throws {Error} If profile file is not found
 */
export function loadProfile(investorType, pluginRoot) {
  if (!investorType || typeof investorType !== 'string') {
    throw new Error('investorType is required');
  }

  // Resolve alias
  const aliasDesc = Object.getOwnPropertyDescriptor(ALIASES, investorType);
  const resolved = aliasDesc !== undefined ? aliasDesc.value : investorType;

  const profileDir = join(pluginRoot, 'orchestrators', 'investor-profiles');

  // Try exact match first, then with .json extension
  const candidates = [
    join(profileDir, `${resolved}.json`),
    join(profileDir, resolved),
  ];

  for (const candidate of candidates) {
    if (existsSync(candidate)) {
      const raw = readFileSync(candidate, 'utf-8');
      return JSON.parse(raw);
    }
  }

  // List available profiles for the error message
  const availableMsg = `Looked for: ${resolved}.json in ${profileDir}`;
  throw new Error(`Investor profile not found for type "${investorType}" (resolved: "${resolved}"). ${availableMsg}`);
}
