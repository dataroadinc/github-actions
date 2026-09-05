"""Release decisions must include unattended changes without duplicate releases."""

import importlib.util
import pathlib
import unittest

SOURCE = pathlib.Path(__file__).parents[1] / '.github/actions/prepare-cargo-release/release.py'
spec = importlib.util.spec_from_file_location('release', SOURCE)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleasePlanTests(unittest.TestCase):
    def test_dependency_updates_release_a_patch(self):
        self.assertEqual(release.next_version('0.1.1', '0.1.1', ['build(deps): update serde']), '0.1.2')

    def test_features_release_a_minor(self):
        self.assertEqual(release.next_version('1.2.3', '1.2.3', ['feat(tree): add scopes']), '1.3.0')

    def test_breaking_changes_override_features(self):
        for message in ['fix(tree)!: change format', 'feat(tree): change\n\nBREAKING CHANGE: wire shape']:
            self.assertEqual(release.next_version('1.2.3', '1.2.3', [message]), '2.0.0')

    def test_docs_and_ci_alone_do_not_release(self):
        self.assertIsNone(release.next_version('0.1.1', '0.1.1', ['docs(readme): clarify', 'ci(test): adjust runner']))

    def test_unreleased_manual_bump_is_preserved(self):
        self.assertEqual(release.next_version('0.2.0', '0.1.1', ['chore(release): prepare']), '0.2.0')

    def test_published_release_commit_does_not_loop(self):
        self.assertIsNone(release.next_version('0.1.2', '0.1.2', []))

    def test_failed_release_does_not_require_a_new_version(self):
        self.assertEqual(release.next_version('0.1.2', '0.1.1', ['fix(tree): repair']), '0.1.2')

    def test_first_release_uses_manifest(self):
        self.assertEqual(release.next_version('0.1.0', None, ['feat(tree): initial']), '0.1.0')

    def test_history_is_not_limited_to_latest_commit(self):
        self.assertEqual(release.next_version('0.1.1', '0.1.1', ['fix(tree): repair', 'docs(readme): clarify']), '0.1.2')

    def test_unknown_commit_type_releases_conservatively(self):
        self.assertEqual(release.next_version('0.1.1', '0.1.1', ['Update source']), '0.1.2')

    def test_lower_manifest_is_refused(self):
        with self.assertRaises(ValueError):
            release.next_version('0.1.0', '0.1.1', ['fix(tree): repair'])


if __name__ == '__main__':
    unittest.main()
