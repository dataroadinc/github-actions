"""Regression tests for the reusable Cargo release workflow contract."""

from pathlib import Path
import unittest


WORKFLOW = (
    Path(__file__).parents[1] / ".github" / "workflows" / "cargo-crate-ci.yml"
).read_text(encoding="utf-8")


class CargoCrateCiContractTests(unittest.TestCase):
    """Protect explicit, idempotent release retries."""

    def test_force_release_runs_version_check_and_release(self) -> None:
        """A caller-requested retry must not be suppressed by an existing tag."""
        self.assertIn("      force-release:\n", WORKFLOW)
        self.assertIn("        type: boolean\n", WORKFLOW)
        self.assertIn(
            "github.event_name == 'push' || inputs.force-release",
            WORKFLOW,
        )
        self.assertIn(
            "release_required: ${{ inputs.force-release || "
            "steps.gv.outputs.version_changed == 'true' }}",
            WORKFLOW,
        )
        self.assertIn(
            "if: needs.version-check.outputs.release_required == 'true'",
            WORKFLOW,
        )


if __name__ == "__main__":
    unittest.main()
