"""Regression tests for the automatic Cargo release workflow contract."""

from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
WORKFLOW = (ROOT / ".github/workflows/cargo-auto-version-bump.yml").read_text(
    encoding="utf-8"
)
ACTION = (ROOT / ".github/actions/generate-changelog/action.yml").read_text(
    encoding="utf-8"
)


class CargoAutoVersionBumpContractTests(unittest.TestCase):
    """Protect release ordering around changelog generation."""

    def test_changelog_uses_existing_bumped_commit_before_tag_creation(self) -> None:
        """Changelog generation must not resolve a tag that is not created yet."""
        self.assertIn("  revision:\n", ACTION)
        self.assertIn('--at "${{ inputs.revision }}"', ACTION)
        self.assertIn("          revision: HEAD\n", WORKFLOW)
        self.assertNotIn("          release-tag: v${{ env.NEW_VERSION }}\n", WORKFLOW)


if __name__ == "__main__":
    unittest.main()
