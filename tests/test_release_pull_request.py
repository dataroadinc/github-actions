"""A needed version bump opens a release pull request; it never writes to main."""

import importlib.util
import json
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SOURCE = pathlib.Path(__file__).parents[1] / '.github/actions/prepare-cargo-release/release.py'
spec = importlib.util.spec_from_file_location('release_pull_request', SOURCE)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleasePullRequestTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        previous = pathlib.Path.cwd()
        os.chdir(self.directory.name)
        self.addCleanup(os.chdir, previous)
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Release test')
        self.git('config', 'user.email', 'release@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', '/dev/null')
        pathlib.Path('Cargo.toml').write_text('[package]\nname="example"\nversion="1.2.3"\n')
        self.git('add', 'Cargo.toml')
        self.git('commit', '-m', 'chore(release): prepare 1.2.3')
        self.git('-c', 'tag.gpgsign=false', 'tag', 'v1.2.3')
        self.git('remote', 'add', 'origin', self.directory.name)
        env = patch.dict(os.environ, GITHUB_REF='refs/heads/main', GITHUB_REPOSITORY='owner/example')
        env.start()
        self.addCleanup(env.stop)

    def git(self, *args):
        return subprocess.check_output(['git', *args], text=True, stderr=subprocess.DEVNULL).strip()

    def mock_commands(self, responses):
        """`gh` calls answer from `responses` in order; `cargo version-info bump`
        edits the manifest like the real tool; everything else runs."""
        real_run = subprocess.run
        calls = []

        def run(args, **kwargs):
            if args[0] == 'gh':
                calls.append(args)
                stdout, code, stderr = responses.pop(0)
                return subprocess.CompletedProcess(args, code, stdout, stderr)
            if args[:3] == ['cargo', 'version-info', 'bump']:
                version = args[args.index('--version') + 1]
                pathlib.Path('Cargo.toml').write_text(f'[package]\nname="example"\nversion="{version}"\n')
                return subprocess.CompletedProcess(args, 0, '', '')
            return real_run(args, **kwargs)

        return patch.object(release.subprocess, 'run', side_effect=run), calls

    def test_unreleased_fix_opens_a_release_pull_request_and_does_not_release(self):
        self.git('commit', '--allow-empty', '-m', 'fix(core): repair')
        source = self.git('rev-parse', 'HEAD')
        responses = [
            ('{"draft": false}', 0, ''),          # releases/tags/v1.2.3: completed
            ('', 1, 'gh: Not Found (HTTP 404)'),  # release branch does not exist yet
            ('{}', 0, ''),                        # create branch ref at source
            (json.dumps({'data': {'createCommitOnBranch': {'commit': {'oid': 'abc'}}}}), 0, ''),
            ('[]', 0, ''),                        # no open release PR
            ('{"number": 7}', 0, ''),             # PR created
        ]
        mock, calls = self.mock_commands(responses)
        with mock, patch.object(release, 'output') as output:
            release.prepare()
        output.assert_called_once_with(revision=source, release='false', version='1.2.3')
        commit_call = calls[3]
        self.assertIn('graphql', commit_call)
        create_pr = calls[5]
        self.assertIn('repos/owner/example/pulls', create_pr)
        self.assertIn('title=chore(release): prepare 1.2.4', create_pr)
        self.assertIn(f'head={release.RELEASE_BRANCH}', create_pr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), source, 'main is never written')

    def test_existing_release_branch_and_pull_request_are_refreshed(self):
        self.git('commit', '--allow-empty', '-m', 'feat(core): extend')
        responses = [
            ('{"draft": false}', 0, ''),
            ('{"object": {"sha": "old"}}', 0, ''),  # branch exists
            ('{}', 0, ''),                          # force-reset branch to source
            (json.dumps({'data': {'createCommitOnBranch': {'commit': {'oid': 'abc'}}}}), 0, ''),
            ('[{"number": 7}]', 0, ''),             # open release PR exists
            ('{}', 0, ''),                          # PR title/body refreshed
        ]
        mock, calls = self.mock_commands(responses)
        with mock, patch.object(release, 'output'):
            release.prepare()
        self.assertIn('force=true', calls[2])
        self.assertIn('repos/owner/example/pulls/7', calls[5])
        self.assertIn('title=chore(release): prepare 1.3.0', calls[5])

    def test_merged_release_commit_publishes_its_own_revision(self):
        pathlib.Path('Cargo.toml').write_text('[package]\nname="example"\nversion="1.2.4"\n')
        self.git('commit', '-am', 'chore(release): prepare 1.2.4')
        head = self.git('rev-parse', 'HEAD')
        responses = [('{"draft": false}', 0, '')]
        mock, _ = self.mock_commands(responses)
        with mock, patch.object(release, 'output') as output:
            release.prepare()
        output.assert_called_once_with(revision=head, release='true', version='1.2.4')

    def test_stale_main_checkout_never_prepares(self):
        self.git('commit', '--allow-empty', '-m', 'fix(core): repair')
        stale = self.git('rev-parse', 'HEAD~1')
        self.git('checkout', '-q', '--detach', stale)
        with patch.object(release, 'output') as output:
            release.prepare()
        output.assert_called_once_with(revision=stale, release='false', version='')


if __name__ == '__main__':
    unittest.main()
