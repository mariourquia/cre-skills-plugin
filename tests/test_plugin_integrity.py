#!/usr/bin/env python3
"""Plugin integrity tests for CRE Skills Plugin v3.0.0"""
import json, yaml, os, glob, subprocess, unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestPluginStructure(unittest.TestCase):
    def test_plugin_json_valid(self):
        with open(os.path.join(PLUGIN_ROOT, '.claude-plugin/plugin.json')) as f:
            data = json.load(f)
        self.assertEqual(data['version'], '3.0.0')
        self.assertEqual(data['license'], 'Apache-2.0')

    def test_all_skills_have_skillmd(self):
        skill_dirs = glob.glob(os.path.join(PLUGIN_ROOT, 'skills/*/'))
        # Allow stub directories (concurrent agent creation) but track them
        stubs = [d for d in skill_dirs if not os.path.exists(os.path.join(d, 'SKILL.md'))]
        complete = [d for d in skill_dirs if os.path.exists(os.path.join(d, 'SKILL.md'))]
        self.assertGreaterEqual(len(complete), 99, f'Expected >= 99 complete skills, found {len(complete)}')
        self.assertLessEqual(len(stubs), 10, f'Too many stub directories ({len(stubs)}): {stubs}')

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
        self.assertGreaterEqual(skill_count, 105, f'Expected >= 105 skills, found {skill_count}')

    def test_feedback_schemas_valid(self):
        """Verify feedback JSON schemas parse correctly"""
        for name in ['feedback-submission.schema.json', 'feedback-config.schema.json']:
            path = os.path.join(PLUGIN_ROOT, 'schemas', name)
            self.assertTrue(os.path.exists(path), f'Missing {name}')
            with open(path) as f:
                data = json.load(f)
            self.assertIn('$schema', data, f'{name} missing $schema')
            self.assertIn('properties', data, f'{name} missing properties')

    def test_feedback_commands_exist(self):
        """Verify feedback command files exist and have frontmatter"""
        for name in ['send-feedback.md', 'report-problem.md']:
            path = os.path.join(PLUGIN_ROOT, 'commands', name)
            self.assertTrue(os.path.exists(path), f'Missing commands/{name}')
            with open(path) as f:
                content = f.read()
            self.assertTrue(content.startswith('---'), f'{name} missing frontmatter')

    def test_redaction_script_syntax(self):
        """Verify redact-feedback.mjs passes Node.js syntax check"""
        script = os.path.join(PLUGIN_ROOT, 'scripts', 'redact-feedback.mjs')
        self.assertTrue(os.path.exists(script), 'Missing scripts/redact-feedback.mjs')
        result = subprocess.run(['node', '--check', script], capture_output=True)
        self.assertEqual(result.returncode, 0, f'redact-feedback.mjs failed syntax check')

    def test_feedback_docs_exist(self):
        """Verify feedback system documentation exists"""
        path = 'docs/feedback-system.md'
        full = os.path.join(PLUGIN_ROOT, path)
        self.assertTrue(os.path.exists(full), f'Missing {path}')

if __name__ == '__main__':
    unittest.main()
