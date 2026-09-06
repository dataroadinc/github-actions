# Conventional Commit

Use from a trusted `pull_request_target` workflow on opened, edited,
synchronize, reopened and ready_for_review. Do not check out PR code or
interpolate its title into shell commands. Requires only pull-requests read.

The shared policy requires `type(scope): description`, permits a breaking `!`,
and accepts feat, fix, build, chore, docs, style, ci, refactor, perf, test, revert.
Scope is mandatory and lowercase. The current PR title is fetched from GitHub.

This early check complements, but does not replace, the merge-time title check
in `merge-tested-dependabot` and commit-history validation in
`prepare-cargo-release`. Human squash merges must use the validated PR title.
Repository policy must enforce the check where the authorized release writer
can still create version commits; do not silently weaken existing protections.

## Release pull requests

A pull request opened by the release pipeline with the workflow token raises no
`pull_request` event. Give the workflow a `workflow_dispatch` trigger with a
`pull_request` input and pass it as `pull-request`; the action then validates
that PR's title instead of the event payload's.
