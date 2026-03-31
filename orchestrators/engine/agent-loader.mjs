/**
 * Agent Loader -- Reads agent markdown and skill reference files, concatenates into a prompt.
 *
 * Export: loadAgent(agentConfig, pluginRoot)
 * Returns: { agentId, prompt, skillCount, charCount }
 */

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const SEPARATOR = '\n\n---\n\n';

/**
 * Load an agent's prompt by reading its markdown file and all referenced skill files.
 *
 * @param {object} agentConfig - Agent configuration from pipeline config
 * @param {string} agentConfig.agentId - Unique agent identifier
 * @param {string} agentConfig.file - Relative path to agent markdown file
 * @param {string[]} [agentConfig.skillRefs] - Relative paths to skill markdown files
 * @param {string} pluginRoot - Absolute path to the plugin root directory
 * @returns {{ agentId: string, prompt: string, skillCount: number, charCount: number }}
 */
export function loadAgent(agentConfig, pluginRoot) {
  const agentId = agentConfig.agentId;
  const agentFile = join(pluginRoot, agentConfig.file);
  const skillRefs = agentConfig.skillRefs || [];

  // Read agent markdown
  let agentPrompt = '';
  if (existsSync(agentFile)) {
    agentPrompt = readFileSync(agentFile, 'utf-8');
  } else {
    agentPrompt = `[Agent file not found: ${agentConfig.file}]`;
  }

  // Read and concatenate skill reference files
  const skillParts = [];
  let loadedSkillCount = 0;

  for (const ref of skillRefs) {
    const skillPath = join(pluginRoot, ref);
    if (existsSync(skillPath)) {
      const content = readFileSync(skillPath, 'utf-8');
      skillParts.push(`<!-- skill: ${ref} -->\n${content}`);
      loadedSkillCount++;
    } else {
      skillParts.push(`<!-- skill not found: ${ref} -->`);
    }
  }

  // Assemble full prompt
  const parts = [agentPrompt];
  if (skillParts.length > 0) {
    parts.push(`<!-- Referenced Skills (${loadedSkillCount}/${skillRefs.length}) -->`);
    parts.push(...skillParts);
  }

  const prompt = parts.join(SEPARATOR);

  return {
    agentId,
    prompt,
    skillCount: loadedSkillCount,
    charCount: prompt.length,
  };
}
