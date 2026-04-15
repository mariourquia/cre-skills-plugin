#!/usr/bin/env python3
"""Release hygiene tests.

Fails if stale release artifacts are tracked in git, or if shipped versions
lack release notes.
"""
import os, re, subprocess, unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASES_DIR = os.path.join(PLUGIN_ROOT, 'docs', 'releases')
CHANGELOG = os.path.join(PLUGIN_ROOT, 'CHANGELOG.md')


def current_version():
    import json
    with open(os.path.join(PLUGIN_ROOT, '.claude-plugin', 'plugin.json')) as f:
        return json.load(f)['version']


def tracked_dist_files():
    result = subprocess.run(
        ['git', 'ls-files', 'dist/'],
        cwd=PLUGIN_ROOT, capture_output=True, text=True
    )
    return [line for line in result.stdout.splitlines() if line]


class TestDistCleanliness(unittest.TestCase):
    """dist/ should only contain non-binary artifacts needed at runtime."""

    def test_no_binary_release_artifacts_tracked(self):
        tracked = tracked_dist_files()
        binary_suffixes = ('.dmg', '.exe', '.tar.gz', '.zip', '.sha256', '.pkg', '.msi')
        binaries = [f for f in tracked if f.endswith(binary_suffixes)]
        self.assertEqual(
            binaries, [],
            f"Binary release artifacts must not be tracked in git (they come from releases workflow): {binaries}"
        )


class TestReleaseNotesCoverage(unittest.TestCase):
    """Every shipped version in CHANGELOG must have a matching release notes file."""

    def test_current_version_has_release_notes(self):
        version = current_version()
        notes_path = os.path.join(RELEASES_DIR, f'v{version}-release-notes.md')
        self.assertTrue(
            os.path.exists(notes_path),
            f"Release notes missing for current version v{version}: {notes_path}"
        )

    def test_changelog_versions_have_notes(self):
        """Every [x.y.z] section in CHANGELOG.md must have a release notes file or a reason."""
        with open(CHANGELOG) as f:
            text = f.read()
        versions = re.findall(r'^## \[(\d+\.\d+\.\d+)\]', text, re.MULTILINE)
        missing = []
        for v in versions:
            path = os.path.join(RELEASES_DIR, f'v{v}-release-notes.md')
            if not os.path.exists(path):
                missing.append(v)
        self.assertEqual(
            missing, [],
            f"CHANGELOG entries without release notes: {missing}"
        )


if __name__ == '__main__':
    unittest.main()
