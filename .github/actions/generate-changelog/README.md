# generate-changelog

Generates a changelog from conventional commits using
cargo-version-info.

## Usage

```yaml
- name: Generate changelog
  uses: ./.github/actions/generate-changelog
  with:
    release-tag: v0.1.3
    output-file: CHANGELOG.md # optional, defaults to CHANGELOG.md
```

## Inputs

| Input         | Description                  | Required | Default        |
| ------------- | ---------------------------- | -------- | -------------- |
| `release-tag` | Release tag (e.g., `v0.1.3`) | Yes      | -              |
| `output-file` | File to write changelog to   | No       | `CHANGELOG.md` |

## Features

- Uses `cargo version-info changelog` for unified version management
- Automatically handles tags that don't exist yet
- Falls back to generating changelog from previous tag to HEAD
- Smart handling of first release (no previous tag)

## What it does

1. Sets up cargo-version-info (dependency)
2. Calls `cargo version-info changelog --at <tag> --output <file>`
3. Generates changelog based on conventional commits

## Dependencies

- `setup-cargo-version-info` (called automatically)

## Output

Creates a markdown file with the changelog for the specified release.

## Example

```yaml
- name: Generate changelog
  uses: ./.github/actions/generate-changelog
  with:
    release-tag: v${{ steps.version.outputs.version }}
    output-file: CHANGELOG.md
```
