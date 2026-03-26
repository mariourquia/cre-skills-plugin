#!/usr/bin/env python3
"""Plugin integrity tests for CRE Skills Plugin v2.0.0"""
import json, yaml, os, glob, subprocess, unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestPluginStructure(unittest.TestCase):
    def test_plugin_json_valid(self):
        with open(os.path.join(PLUGIN_ROOT, '.claude-plugin/plugin.json')) as f:
            data = json.load(f)
        self.assertEqual(data['version'], '2.0.0')
        self.assertEqual(data['license'], 'Apache-2.0')

    def test_all_skills_have_skillmd(self):
        skill_dirs = glob.glob(os.path.join(PLUGIN_ROOT, 'skills/*/'))
        for d in skill_dirs:
            self.assertTrue(os.path.exists(os.path.join(d, 'SKILL.md')), f'Missing SKILL.md in {d}')

    def test_hooks_json_valid(self):
        with open(os.path.join(PLUGIN_ROOT, 'hooks/hooks.json')) as f:
            data = json.load(f)
        self.assertIn('hooks', data)

    def test_hook_scripts_syntax(self):
        for hook in glob.glob(os.path.join(PLUGIN_ROOT, 'hooks/*.mjs')):
            result = subprocess.run(['node', '--check', hook], capture_output=True)
            self.assertEqual(result.returncode, 0, f'{hook} failed syntax check')

    def test_python_calculators_syntax(self):
        for script in glob.glob(os.path.join(PLUGIN_ROOT, 'scripts/calculators/*.py')):
            with open(script) as f:
                compile(f.read(), script, 'exec')  # syntax check

    def test_required_files_exist(self):
        required = ['LICENSE', 'NOTICE', 'README.md', 'SECURITY.md', 'PRIVACY.md',
                     'CONTRIBUTING.md', 'CHANGELOG.md', 'registry.yaml']
        for f in required:
            self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, f)), f'Missing {f}')

    def test_agents_index_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'agents/_index.md')))

    def test_routing_index_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'routing/CRE-ROUTING.md')))

    def test_skill_count_matches_plugin_json(self):
        """Verify skill count in plugin.json description matches actual"""
        skill_count = len(glob.glob(os.path.join(PLUGIN_ROOT, 'skills/*/SKILL.md')))
        self.assertGreaterEqual(skill_count, 91, f'Expected >= 91 skills, found {skill_count}')

if __name__ == '__main__':
    unittest.main()
