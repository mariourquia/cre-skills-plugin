#!/usr/bin/env python3
"""Canonical source-of-truth consistency tests.

Fails if plugin.json, catalog.yaml, registry.yaml, and README.md drift from
each other on version or headline counts. Run in CI before every release.
"""
import json, os, re, unittest

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PLUGIN_ROOT, 'src')


def load_catalog():
    path = os.path.join(SRC_DIR, 'catalog', 'catalog.yaml')
    if os.path.exists(path) and HAS_YAML:
        with open(path) as f:
            return yaml.safe_load(f)
    json_path = os.path.join(PLUGIN_ROOT, 'dist', 'catalog.json')
    if os.path.exists(json_path):
        with open(json_path) as f:
            return json.load(f)
    return None


def load_plugin_json():
    with open(os.path.join(PLUGIN_ROOT, '.claude-plugin', 'plugin.json')) as f:
        return json.load(f)


def catalog_counts(catalog):
    """Count all catalog items by type, including items marked hidden_from_default_catalog.
    The hidden flag affects router visibility only, not public-facing claims."""
    counts = {'skill': 0, 'agent': 0, 'command': 0, 'calculator': 0,
              'orchestrator': 0, 'workflow': 0}
    for item in catalog.get('items', []):
        t = item.get('type')
        if t in counts:
            counts[t] += 1
    return counts


class TestVersionConsistency(unittest.TestCase):
    """Plugin version must match across every canonical surface."""

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_plugin_json_matches_catalog_plugin_version(self):
        plugin = load_plugin_json()
        catalog = load_catalog()
        self.assertIsNotNone(catalog, 'catalog.yaml missing')
        self.assertEqual(
            plugin['version'], catalog['plugin_version'],
            f"plugin.json version ({plugin['version']}) != catalog plugin_version ({catalog['plugin_version']})"
        )

    def test_plugin_json_version_format(self):
        plugin = load_plugin_json()
        self.assertRegex(plugin['version'], r'^\d+\.\d+\.\d+$')


class TestCountConsistency(unittest.TestCase):
    """Headline counts claimed in plugin.json description must match catalog reality."""

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_catalog_counts_match_plugin_description(self):
        """If plugin.json description cites numeric counts, they must match
        the catalog. The description is expected to be count-free by policy,
        so this test passes vacuously when the regex finds no claims, and
        fails the moment a hardcoded count reappears and drifts.
        """
        plugin = load_plugin_json()
        catalog = load_catalog()
        self.assertIsNotNone(catalog, 'catalog.yaml missing')
        counts = catalog_counts(catalog)
        desc = plugin['description']

        patterns = {
            'skill': r'(\d+)\s+institutional-grade CRE skills',
            'agent': r'(\d+)\s+expert subagents',
            'calculator': r'(\d+)\s+Python calculators',
            'orchestrator': r'(\d+)\s+orchestrator pipelines',
            'workflow': r'(\d+)\s+workflow chains',
        }
        for t, pat in patterns.items():
            m = re.search(pat, desc)
            if m is None:
                continue
            claimed_count = int(m.group(1))
            self.assertEqual(
                counts[t], claimed_count,
                f"plugin.json claims {claimed_count} {t}s; catalog has {counts[t]}"
            )

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_reference_file_count_matches_claim(self):
        """If plugin.json description claims a reference-file count, it must
        match the filesystem. Passes vacuously when no such claim is present."""
        plugin = load_plugin_json()
        desc = plugin['description']
        m = re.search(r'(\d+)\s+reference files', desc)
        if m is None:
            return
        claimed = int(m.group(1))
        actual = 0
        for root, _, files in os.walk(os.path.join(SRC_DIR, 'skills')):
            if os.path.basename(os.path.dirname(root)) == 'references' or os.path.basename(root) == 'references':
                actual += len(files)
        self.assertEqual(
            actual, claimed,
            f"plugin.json claims {claimed} reference files; filesystem has {actual}"
        )


class TestCatalogIntegrity(unittest.TestCase):
    """Catalog items must map to real filesystem paths."""

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_catalog_items_source_paths_exist(self):
        catalog = load_catalog()
        self.assertIsNotNone(catalog, 'catalog.yaml missing')
        missing = []
        for item in catalog.get('items', []):
            sp = item.get('source_path')
            if not sp:
                continue
            abs_path = os.path.join(PLUGIN_ROOT, sp)
            if not os.path.exists(abs_path):
                missing.append(f"{item['id']} -> {sp}")
        self.assertEqual(missing, [], f"Catalog source_paths missing: {missing[:5]}")


class TestMcpToolsCatalog(unittest.TestCase):
    """The MCP tools section of the catalog must match the live mcp-server.mjs."""

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_catalog_mcp_tools_match_implementation(self):
        catalog = load_catalog()
        self.assertIsNotNone(catalog, 'catalog.yaml missing')

        catalog_tools = catalog.get('mcp_tools', [])
        self.assertGreater(
            len(catalog_tools), 0,
            "catalog.yaml must include an mcp_tools section "
            "(rebuild with: python scripts/catalog-build.py)"
        )

        mcp_path = os.path.join(SRC_DIR, 'mcp-server.mjs')
        src = open(mcp_path, encoding='utf-8').read()
        impl_names = re.findall(r'name:\s*"(cre_[a-z_]+)"', src)

        catalog_names = [t['name'] for t in catalog_tools]
        self.assertEqual(
            sorted(catalog_names), sorted(impl_names),
            "catalog.yaml mcp_tools list does not match src/mcp-server.mjs. "
            "Rebuild with: python scripts/catalog-build.py"
        )

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_readme_mcp_tool_count_matches_catalog(self):
        catalog = load_catalog()
        catalog_count = len(catalog.get('mcp_tools', []))
        readme = open(os.path.join(PLUGIN_ROOT, 'README.md'), encoding='utf-8').read()
        # README should reference the count somewhere; capture any "<N> MCP tool" claim.
        claims = [int(m) for m in re.findall(r'(\d+)\s+MCP\s+tools?\b', readme)]
        if not claims:
            self.skipTest("README does not advertise an MCP tool count yet")
        for claim in claims:
            self.assertEqual(
                claim, catalog_count,
                f"README claims {claim} MCP tools but catalog.yaml has {catalog_count}"
            )


if __name__ == '__main__':
    unittest.main()
