"""An already published version is not sufficient evidence for a successful retry."""
import importlib.util
import pathlib
import unittest

source = pathlib.Path(__file__).parents[1] / '.github/actions/publish-tested-crate/publish.py'
spec = importlib.util.spec_from_file_location('publish', source)
publish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publish)


class PublishedRevisionTests(unittest.TestCase):
    def test_exact_revision_can_resume(self):
        publish.verify_revision({'git': {'sha1': 'tested'}}, 'tested')

    def test_different_revision_cannot_be_called_success(self):
        with self.assertRaises(ValueError):
            publish.verify_revision({'git': {'sha1': 'other'}}, 'tested')

    def test_missing_identity_cannot_be_called_success(self):
        with self.assertRaises(ValueError):
            publish.verify_revision({}, 'tested')
