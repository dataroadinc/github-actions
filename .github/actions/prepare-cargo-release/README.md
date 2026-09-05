# Prepare Cargo release

Run after a full-history checkout of the workflow revision. Pass its `revision`
output to **every** validation, build and publication checkout. Only release when
`release` is `true` and all repository checks succeed. Main release workflows must
use one concurrency group with `cancel-in-progress: false`.

The action compares all commits since the latest reachable stable version tag.
Fixes and dependency changes produce a patch; `feat` a minor;
`!` or `BREAKING CHANGE` a major. Documentation, style and CI-only changes do not
release. A higher manifest version is respected. No tag baseline uses the manifest.
Every considered commit must match the scoped Conventional Commit policy shared
with PR-title and merge-time validation. Invalid headers fail, including during
manual bumps and initial releases; no unknown-message patch fallback exists.

On main, `cargo version-info` prepares the version and its configured companion
files. GitHub's GraphQL API records a verified commit with an expected-head guard.
The resulting revision is returned, never a later fetched main. This commit is
validated by downstream jobs in this same workflow (the bot push does not trigger
another pipeline). PR runs return their checked-out revision without mutation.

Requires `contents: write`, a full git checkout, Python 3.11+, Rust and GitHub CLI.
No publishing token is used here. Registry publication belongs exclusively to the
calling pipeline after its validation gate.
