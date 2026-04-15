#!/usr/bin/env python3
"""Orchestrator reference integrity tests.

Fails if handoff-registry references orchestrator IDs without matching configs,
or if any orchestrator config references skills that don't exist.
"""
import json, os, unittest

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORCH_DIR = os.path.join(PLUGIN_ROOT, 'src', 'orchestrators')
CONFIG_DIR = os.path.join(ORCH_DIR, 'configs')
SKILLS_DIR = os.path.join(PLUGIN_ROOT, 'src', 'skills')


def deployed_skill_slugs():
    return {
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, d))
        and os.path.exists(os.path.join(SKILLS_DIR, d, 'SKILL.md'))
    }


def config_orchestrator_ids():
    """Every config file `<name>.json` maps to orchestrator ID `<name>-orchestrator`."""
    ids = set()
    for f in os.listdir(CONFIG_DIR):
        if f.endswith('.json'):
            ids.add(f[:-5] + '-orchestrator')
    return ids


class TestHandoffRegistryIntegrity(unittest.TestCase):
    """Every handoff source and target must point to a real orchestrator."""

    def setUp(self):
        with open(os.path.join(ORCH_DIR, 'handoff-registry.json')) as f:
            self.registry = json.load(f)
        self.valid_ids = config_orchestrator_ids()

    def test_all_handoff_sources_resolve(self):
        broken = [
            h['id'] for h in self.registry['handoffs']
            if h['from']['orchestratorId'] not in self.valid_ids
        ]
        self.assertEqual(broken, [], f"Handoffs with unknown source: {broken}")

    def test_all_handoff_targets_resolve(self):
        broken = [
            h['id'] for h in self.registry['handoffs']
            if h['to']['orchestratorId'] not in self.valid_ids
        ]
        self.assertEqual(broken, [], f"Handoffs with unknown target: {broken}")

    def test_no_handoff_id_duplicates(self):
        ids = [h['id'] for h in self.registry['handoffs']]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate handoff ids: {ids}")


class TestOrchestratorConfigReferences(unittest.TestCase):
    """Every skill referenced in an orchestrator config must be deployed."""

    def setUp(self):
        self.valid_skills = deployed_skill_slugs()

    def _walk_config_skill_refs(self, obj, refs):
        """Collect any value that looks like a skill slug under keys named 'skill'/'skills'."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ('skill', 'skill_id', 'skillSlug') and isinstance(v, str):
                    refs.add(v)
                elif k in ('skills', 'skill_chain') and isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            refs.add(item)
                        elif isinstance(item, dict):
                            self._walk_config_skill_refs(item, refs)
                else:
                    self._walk_config_skill_refs(v, refs)
        elif isinstance(obj, list):
            for item in obj:
                self._walk_config_skill_refs(item, refs)

    def test_all_config_skill_refs_are_deployed(self):
        broken = {}
        for f in os.listdir(CONFIG_DIR):
            if not f.endswith('.json'):
                continue
            with open(os.path.join(CONFIG_DIR, f)) as fh:
                cfg = json.load(fh)
            refs = set()
            self._walk_config_skill_refs(cfg, refs)
            missing = sorted(refs - self.valid_skills)
            if missing:
                broken[f] = missing
        self.assertEqual(broken, {}, f"Orchestrator configs reference missing skills: {broken}")


class TestPromptConfigConsistency(unittest.TestCase):
    """Every wired prompt must have a matching config; no orphans allowed.

    Design references that do not have a config live in
    docs/orchestrator-references/, not src/orchestrators/prompts/.
    """

    PROMPTS_DIR = os.path.join(ORCH_DIR, 'prompts')

    def _prompt_basenames(self):
        # Strip "-orchestrator.md" so the basename matches the config filename.
        return {
            f[:-len('-orchestrator.md')]
            for f in os.listdir(self.PROMPTS_DIR)
            if f.endswith('-orchestrator.md')
        }

    def _config_basenames(self):
        return {f[:-len('.json')] for f in os.listdir(CONFIG_DIR) if f.endswith('.json')}

    def test_no_orphan_prompt_files(self):
        prompt_names = self._prompt_basenames()
        config_names = self._config_basenames()
        orphans = sorted(prompt_names - config_names)
        self.assertEqual(
            orphans, [],
            "Orchestrator prompts must have a matching config under "
            "src/orchestrators/configs/. Move design references to "
            f"docs/orchestrator-references/. Orphans: {orphans}"
        )


class TestOrchestratorCountMatchesCatalog(unittest.TestCase):
    """Claimed 10 orchestrators = 10 configs = 10 catalog entries."""

    def test_config_count_is_ten(self):
        configs = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
        self.assertEqual(
            len(configs), 10,
            f"Expected 10 orchestrator configs; found {len(configs)}: {sorted(configs)}"
        )

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_catalog_orchestrator_count_matches_configs(self):
        with open(os.path.join(PLUGIN_ROOT, 'src', 'catalog', 'catalog.yaml')) as f:
            catalog = yaml.safe_load(f)
        catalog_orchs = [i for i in catalog.get('items', []) if i.get('type') == 'orchestrator']
        configs = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
        self.assertEqual(
            len(catalog_orchs), len(configs),
            f"Catalog has {len(catalog_orchs)} orchestrators, configs dir has {len(configs)}"
        )


if __name__ == '__main__':
    unittest.main()
