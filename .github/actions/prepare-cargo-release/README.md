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

On main, when the unreleased history calls for a new version, `cargo version-info`
prepares the version and its configured companion files on the `release/pending`
branch (reset to the current main so the branch carries exactly one commit), records
it through GitHub's GraphQL API as a verified commit, and opens or refreshes the
pull request `chore(release): prepare <version>`. Main itself is never written:
every merge into main requires the owner's approval (or an agent acting for the
owner), and the release commit is no exception. That run returns `release=false`.
Once the release pull request is squash-merged, the next main run finds the
manifest version without a tag and returns `release=true` with that exact merge
revision, which the calling pipeline validates, tags and publishes. A main
checkout that is no longer the remote head never prepares anything. PR runs
return their checked-out revision without mutation.

Requires `contents: write`, a full git checkout, Python 3.11+, Rust and GitHub CLI.
No publishing token is used here. Registry publication belongs exclusively to the
calling pipeline after its validation gate.
