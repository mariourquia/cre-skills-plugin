#!/usr/bin/env python3
"""Plugin integrity and catalog consistency tests for CRE Skills Plugin v4.0.0"""
import json, os, glob, subprocess, unittest

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_catalog():
    """Load the canonical catalog. Returns None if missing."""
    path = os.path.join(PLUGIN_ROOT, 'catalog', 'catalog.yaml')
    if not os.path.exists(path) or not HAS_YAML:
        json_path = os.path.join(PLUGIN_ROOT, 'dist', 'catalog.json')
        if os.path.exists(json_path):
            with open(json_path) as f:
                return json.load(f)
        return None
    with open(path) as f:
        return yaml.safe_load(f)


class TestPluginStructure(unittest.TestCase):
    """Structural integrity tests."""

    def test_plugin_json_valid(self):
        with open(os.path.join(PLUGIN_ROOT, '.claude-plugin/plugin.json')) as f:
            data = json.load(f)
        self.assertEqual(data['license'], 'Apache-2.0')
        self.assertIn('version', data)

    def test_all_skills_have_skillmd(self):
        skill_dirs = glob.glob(os.path.join(PLUGIN_ROOT, 'skills/*/'))
        complete = [d for d in skill_dirs if os.path.exists(os.path.join(d, 'SKILL.md'))]
        self.assertGreaterEqual(len(complete), 99)

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
            if script.endswith('README.md'):
                continue
            with open(script) as f:
                compile(f.read(), script, 'exec')

    def test_required_files_exist(self):
        required = ['LICENSE', 'NOTICE', 'README.md', 'SECURITY.md', 'PRIVACY.md',
                     'CONTRIBUTING.md', 'CHANGELOG.md']
        for f in required:
            self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, f)), f'Missing {f}')

    def test_agents_index_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'agents/_index.md')))

    def test_routing_index_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'routing/CRE-ROUTING.md')))

    def test_feedback_schemas_valid(self):
        for name in ['feedback-submission.schema.json', 'feedback-config.schema.json']:
            path = os.path.join(PLUGIN_ROOT, 'schemas', name)
            self.assertTrue(os.path.exists(path), f'Missing {name}')
            with open(path) as f:
                data = json.load(f)
            self.assertIn('$schema', data)

    def test_feedback_commands_exist(self):
        for name in ['send-feedback.md', 'report-problem.md']:
            path = os.path.join(PLUGIN_ROOT, 'commands', name)
            self.assertTrue(os.path.exists(path), f'Missing commands/{name}')

    def test_redaction_script_syntax(self):
        script = os.path.join(PLUGIN_ROOT, 'scripts', 'redact-feedback.mjs')
        self.assertTrue(os.path.exists(script))
        result = subprocess.run(['node', '--check', script], capture_output=True)
        self.assertEqual(result.returncode, 0)

    def test_feedback_docs_exist(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'docs/feedback-system.md')))


class TestCatalogIntegrity(unittest.TestCase):
    """Catalog source-of-truth tests."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def test_catalog_exists(self):
        self.assertIsNotNone(self.catalog, 'Catalog not found. Run: python scripts/catalog-build.py')

    def test_catalog_has_items(self):
        if not self.catalog:
            self.skipTest('No catalog')
        self.assertGreater(len(self.catalog['items']), 100)

    def test_catalog_schema_exists(self):
        path = os.path.join(PLUGIN_ROOT, 'catalog', 'catalog.schema.json')
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            schema = json.load(f)
        self.assertIn('$defs', schema)
        self.assertIn('CatalogItem', schema['$defs'])

    def test_all_items_have_required_fields(self):
        if not self.catalog:
            self.skipTest('No catalog')
        required = ['id', 'display_name', 'type', 'status', 'source_path']
        for item in self.catalog['items']:
            for field in required:
                self.assertIn(field, item, f'Item {item.get("id", "?")} missing {field}')

    def test_valid_types(self):
        if not self.catalog:
            self.skipTest('No catalog')
        valid = {'skill', 'agent', 'command', 'calculator', 'workflow', 'orchestrator'}
        for item in self.catalog['items']:
            self.assertIn(item['type'], valid, f'{item["id"]} has invalid type: {item["type"]}')

    def test_valid_statuses(self):
        if not self.catalog:
            self.skipTest('No catalog')
        valid = {'stable', 'experimental', 'stub', 'deprecated'}
        for item in self.catalog['items']:
            self.assertIn(item['status'], valid, f'{item["id"]} has invalid status: {item["status"]}')

    def test_no_duplicate_ids_within_type(self):
        if not self.catalog:
            self.skipTest('No catalog')
        seen = {}
        for item in self.catalog['items']:
            key = f"{item['type']}:{item['id']}"
            self.assertNotIn(key, seen, f'Duplicate: {key}')
            seen[key] = True

    def test_source_paths_exist(self):
        if not self.catalog:
            self.skipTest('No catalog')
        for item in self.catalog['items']:
            path = os.path.join(PLUGIN_ROOT, item['source_path'])
            self.assertTrue(os.path.exists(path),
                          f'{item["type"]} {item["id"]}: source_path not found: {item["source_path"]}')


class TestCatalogConsistency(unittest.TestCase):
    """Cross-surface consistency tests derived from catalog."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def test_skill_count_matches_filesystem(self):
        if not self.catalog:
            self.skipTest('No catalog')
        catalog_skills = [i for i in self.catalog['items'] if i['type'] == 'skill']
        fs_skills = glob.glob(os.path.join(PLUGIN_ROOT, 'skills/*/SKILL.md'))
        self.assertEqual(len(catalog_skills), len(fs_skills),
                        f'Catalog has {len(catalog_skills)} skills but filesystem has {len(fs_skills)}')

    def test_agent_count_matches_filesystem(self):
        if not self.catalog:
            self.skipTest('No catalog')
        catalog_agents = [i for i in self.catalog['items'] if i['type'] == 'agent']
        fs_agents = []
        for md in glob.glob(os.path.join(PLUGIN_ROOT, 'agents/**/*.md'), recursive=True):
            if os.path.basename(md) != '_index.md':
                fs_agents.append(md)
        self.assertEqual(len(catalog_agents), len(fs_agents),
                        f'Catalog has {len(catalog_agents)} agents but filesystem has {len(fs_agents)}')

    def test_command_count_matches_filesystem(self):
        if not self.catalog:
            self.skipTest('No catalog')
        catalog_cmds = [i for i in self.catalog['items'] if i['type'] == 'command']
        fs_cmds = glob.glob(os.path.join(PLUGIN_ROOT, 'commands/*.md'))
        self.assertEqual(len(catalog_cmds), len(fs_cmds))

    def test_calculator_count_matches_filesystem(self):
        if not self.catalog:
            self.skipTest('No catalog')
        catalog_calcs = [i for i in self.catalog['items'] if i['type'] == 'calculator']
        fs_calcs = [f for f in glob.glob(os.path.join(PLUGIN_ROOT, 'scripts/calculators/*.py'))
                    if not os.path.basename(f).startswith('__')]
        self.assertEqual(len(catalog_calcs), len(fs_calcs))

    def test_stub_items_hidden_from_default(self):
        if not self.catalog:
            self.skipTest('No catalog')
        for item in self.catalog['items']:
            if item['status'] in ('stub', 'deprecated'):
                self.assertTrue(item.get('hidden_from_default_catalog', False),
                              f'{item["id"]} is {item["status"]} but not hidden from default catalog')


class TestRouterBehavior(unittest.TestCase):
    """Router selection behavior tests."""

    def test_router_loads_catalog(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'routing/skill-dispatcher.mjs'), '--list'],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertGreater(data['count'], 50)

    def test_router_high_confidence_match(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'routing/skill-dispatcher.mjs'), 'underwrite a deal'],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data['confidence'], 'high')
        self.assertIsNotNone(data['recommendation'])
        self.assertIn('underwriting', data['recommendation']['skill'])

    def test_router_excludes_hidden_by_default(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'routing/skill-dispatcher.mjs'), '--list'],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        # space-planning-redesign-orchestrator is a stub, should be excluded
        self.assertNotIn('space-planning-redesign-orchestrator', data['skills'])

    def test_router_includes_hidden_with_flag(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'routing/skill-dispatcher.mjs'), '--list', '--include-hidden'],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        self.assertIn('space-planning-redesign-orchestrator', data['skills'])

    def test_router_returns_alternatives(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'routing/skill-dispatcher.mjs'), 'deal analysis'],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        self.assertIn('alternatives', data)

    def test_router_reports_source(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'routing/skill-dispatcher.mjs'), 'test query'],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        self.assertIn('source', data)


class TestFeedbackConfigParity(unittest.TestCase):
    """Verify feedback config is consistent across code and docs."""

    def test_telemetry_enabled_by_default(self):
        path = os.path.join(PLUGIN_ROOT, 'hooks', 'telemetry-init.mjs')
        with open(path) as f:
            content = f.read()
        self.assertIn("telemetry: true", content,
                      'telemetry-init.mjs should default telemetry to true (opt-out model)')

    def test_feedback_defaults_ask_each_time(self):
        path = os.path.join(PLUGIN_ROOT, 'hooks', 'telemetry-init.mjs')
        with open(path) as f:
            content = f.read()
        self.assertIn("mode: 'ask_each_time'", content,
                      'telemetry-init.mjs should default feedback mode to ask_each_time')
        self.assertIn("cre-skills-feedback-api.vercel.app", content,
                      'telemetry-init.mjs should have feedback backend URL configured')

    def test_privacy_md_not_future(self):
        path = os.path.join(PLUGIN_ROOT, 'PRIVACY.md')
        with open(path) as f:
            content = f.read()
        self.assertNotIn('Not Available Yet', content,
                        'PRIVACY.md should not claim remote submission is "Not Available Yet"')

    def test_feedback_docs_consistent_default(self):
        path = os.path.join(PLUGIN_ROOT, 'docs', 'feedback-system.md')
        with open(path) as f:
            content = f.read()
        self.assertIn('ask_each_time', content,
                      'feedback-system.md should reflect ask_each_time default')

    def test_privacy_md_reflects_opt_out(self):
        path = os.path.join(PLUGIN_ROOT, 'PRIVACY.md')
        with open(path) as f:
            content = f.read()
        self.assertIn('Enabled by Default', content,
                      'PRIVACY.md should reflect opt-out telemetry model')
        self.assertIn('opt out', content.lower(),
                      'PRIVACY.md should explain how to opt out')

    def test_first_run_notice_explains_tracking(self):
        path = os.path.join(PLUGIN_ROOT, 'hooks', 'telemetry-init.mjs')
        with open(path) as f:
            content = f.read()
        self.assertIn('NEVER tracked', content,
                      'First-run notice should explain what is never tracked')
        self.assertIn('opt out', content.lower(),
                      'First-run notice should explain how to opt out')


class TestDocReferences(unittest.TestCase):
    """Verify docs don't reference missing files."""

    def test_catalog_files_exist(self):
        expected = [
            'catalog/catalog.schema.json',
            'catalog/catalog.yaml',
            'dist/catalog.json',
            'scripts/catalog-build.py',
            'scripts/catalog-generate.py',
        ]
        for f in expected:
            self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, f)), f'Missing {f}')

    def test_output_styles_exist(self):
        expected = ['exec-brief.md', 'ic-memo.md', 'pm-action-list.md',
                    'lender-brief.md', 'lp-update.md']
        for f in expected:
            self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'output-styles', f)),
                          f'Missing output-styles/{f}')

    def test_adr_exists(self):
        self.assertTrue(os.path.exists(
            os.path.join(PLUGIN_ROOT, 'docs/adr/0001-catalog-source-of-truth.md')))

    def test_migration_doc_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'docs/MIGRATION.md')))

    def test_release_checklist_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'docs/release-checklist.md')))

    def test_mcp_server_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, 'mcp-server.mjs')))

    def test_mcp_json_exists(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN_ROOT, '.mcp.json')))
        with open(os.path.join(PLUGIN_ROOT, '.mcp.json')) as f:
            data = json.load(f)
        self.assertIn('mcpServers', data)
        self.assertIn('cre-skills', data['mcpServers'])


class TestMcpServer(unittest.TestCase):
    """MCP server behavioral tests."""

    def test_mcp_server_syntax(self):
        result = subprocess.run(
            ['node', '--check', os.path.join(PLUGIN_ROOT, 'mcp-server.mjs')],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, 'mcp-server.mjs failed syntax check')

    def test_mcp_initialize(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'mcp-server.mjs')],
            input='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n',
            capture_output=True, text=True, timeout=5
        )
        data = json.loads(result.stdout.strip())
        self.assertEqual(data['result']['serverInfo']['name'], 'cre-skills')

    def test_mcp_tools_list(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'mcp-server.mjs')],
            input='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n',
            capture_output=True, text=True, timeout=5
        )
        lines = [l for l in result.stdout.strip().split('\n') if l.strip()]
        data = json.loads(lines[-1])
        tools = data['result']['tools']
        self.assertGreaterEqual(len(tools), 8)
        tool_names = [t['name'] for t in tools]
        self.assertIn('cre_route', tool_names)
        self.assertIn('cre_list_skills', tool_names)
        self.assertIn('cre_workspace_create', tool_names)

    def test_mcp_route_tool(self):
        result = subprocess.run(
            ['node', os.path.join(PLUGIN_ROOT, 'mcp-server.mjs')],
            input='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"cre_route","arguments":{"query":"underwrite a deal"}}}\n',
            capture_output=True, text=True, timeout=5
        )
        lines = [l for l in result.stdout.strip().split('\n') if l.strip()]
        data = json.loads(lines[-1])
        content = json.loads(data['result']['content'][0]['text'])
        self.assertEqual(content['confidence'], 'high')
        self.assertIn('underwriting', content['recommendation']['skill'])


if __name__ == '__main__':
    unittest.main()
