# Merge tested Dependabot update

Use in a `workflow_run` handler for the repository's complete CI workflow, with
`types: [completed]`. Permissions: `contents: write`, `pull-requests: write`,
`actions: write`. Do not check out PR code in this privileged handler.

Only successful PR runs from this repository can merge. The PR must be authored
by Dependabot, target main, and still have the exact tested head. The REST merge
uses that SHA as a compare-and-swap guard. All dependency update sizes use the
same CI gate. Main must also run its full validation before release.

After squash merge, explicitly dispatches `ci.yml` on main: bot-token merges do
not trigger push workflows. Callers must support `workflow_dispatch` and should
schedule a daily main run to recover unattended publication failures. Branch
rules still apply; merge refusals fail the workflow instead of bypassing them.
