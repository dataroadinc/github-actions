# generate-pr-log

Generates a list of merged PRs since the last tag for release notes
using cargo-version-info.

## Usage

```yaml
- name: Generate PR log
  uses: ./.github/actions/generate-pr-log
  with:
    since-tag: v0.1.0 # optional, defaults to latest tag
    output-file: PR_LOG.md # optional, defaults to PR_LOG.md
```

## Inputs

| Input         | Description             | Required | Default     |
| ------------- | ----------------------- | -------- | ----------- |
| `since-tag`   | Tag to compare from     | No       | Latest tag  |
| `output-file` | File to write PR log to | No       | `PR_LOG.md` |

## Outputs

| Output     | Description         |
| ---------- | ------------------- |
| `pr-count` | Number of PRs found |

## Features

- Uses `cargo version-info pr-log` for unified version management
- Note: PR log generation may not be fully implemented yet in
  cargo-version-info, but this action provides the interface

## What it does

1. Sets up cargo-version-info (dependency)
2. Calls `cargo version-info pr-log` with appropriate parameters
3. Generates markdown list of merged pull requests

## Dependencies

- `setup-cargo-version-info` (called automatically)

## Output

Creates a markdown file with a list of merged pull requests.

## Example

```yaml
- name: Generate PR log
  uses: ./.github/actions/generate-pr-log
  with:
    since-tag: v${{ steps.version.outputs.version }}
    output-file: PR_LOG.md
```
