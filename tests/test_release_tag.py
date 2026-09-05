"""Real git regression for immutable release identity and retry semantics."""

import importlib.util
import os
import pathlib
import subprocess
import tempfile
import unittest

SOURCE = pathlib.Path(__file__).parents[1] / '.github/actions/tag-tested-release/tag.py'
spec = importlib.util.spec_from_file_location('tag', SOURCE)
tag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tag)


class TagTests(unittest.TestCase):
    def test_exact_revision_retry_and_conflicting_tag(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            subprocess.run(['git', 'init', '--bare', '-q', str(root / 'remote')], check=True)
            subprocess.run(['git', 'init', '-q', str(root / 'work')], check=True)
            original = pathlib.Path.cwd()
            os.chdir(root / 'work')
            try:
                for key, value in [('user.name', 'test'), ('user.email', 'test@example.com'), ('commit.gpgsign', 'false')]:
                    subprocess.run(['git', 'config', key, value], check=True)
                subprocess.run(['git', 'remote', 'add', 'origin', str(root / 'remote')], check=True)
                pathlib.Path('Cargo.toml').write_text('[package]\nname="fixture"\nversion="0.1.0"\n')
                subprocess.run(['git', 'add', 'Cargo.toml'], check=True)
                subprocess.run(['git', 'commit', '-qm', 'initial'], check=True)
                first = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
                tag.tag_release('0.1.0', first)
                tag.tag_release('0.1.0', first)
                subprocess.run(['git', 'commit', '--allow-empty', '-qm', 'second'], check=True)
                second = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
                with self.assertRaisesRegex(ValueError, 'different revision'):
                    tag.tag_release('0.1.0', second)
                with self.assertRaisesRegex(ValueError, 'manifest version'):
                    tag.tag_release('0.1.1', second)
                self.assertEqual(subprocess.check_output(['git', 'rev-parse', 'v0.1.0^{commit}'], text=True).strip(), first)
            finally:
                os.chdir(original)
