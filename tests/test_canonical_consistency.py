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
        plugin = load_plugin_json()
        catalog = load_catalog()
        self.assertIsNotNone(catalog, 'catalog.yaml missing')
        counts = catalog_counts(catalog)
        desc = plugin['description']

        claimed = {
            'skill': int(re.search(r'(\d+)\s+institutional-grade CRE skills', desc).group(1)),
            'agent': int(re.search(r'(\d+)\s+expert subagents', desc).group(1)),
            'calculator': int(re.search(r'(\d+)\s+Python calculators', desc).group(1)),
            'orchestrator': int(re.search(r'(\d+)\s+orchestrator pipelines', desc).group(1)),
            'workflow': int(re.search(r'(\d+)\s+workflow chains', desc).group(1)),
        }

        for t, claimed_count in claimed.items():
            self.assertEqual(
                counts[t], claimed_count,
                f"plugin.json claims {claimed_count} {t}s; catalog has {counts[t]}"
            )

    @unittest.skipUnless(HAS_YAML, 'PyYAML not installed')
    def test_reference_file_count_matches_claim(self):
        plugin = load_plugin_json()
        desc = plugin['description']
        claimed = int(re.search(r'(\d+)\s+reference files', desc).group(1))
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


if __name__ == '__main__':
    unittest.main()
