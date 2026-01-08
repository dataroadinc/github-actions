# generate-build-badges

Generates build artifact status badges using cargo-version-info.

## Usage

```yaml
- name: Generate build badges
  uses: ./.github/actions/generate-build-badges
  with:
    release-tag: v0.1.3 # optional, used for context
    output-file: BUILD_BADGES.md # optional, defaults to BUILD_BADGES.md
```

## Inputs

| Input         | Description                    | Required | Default           |
| ------------- | ------------------------------ | -------- | ----------------- |
| `release-tag` | Release tag (used for context) | No       | -                 |
| `output-file` | File to write badges to        | No       | `BUILD_BADGES.md` |

## Features

- Uses `cargo version-info badge all` for unified version management
- Badges are generated from Cargo.toml metadata, not from release
  artifacts
- Fully generic - no project-specific hardcoding

## What it does

1. Sets up cargo-version-info (dependency)
2. Calls `cargo version-info badge all` to generate badges
3. Writes badges to the specified output file

## Dependencies

- `setup-cargo-version-info` (called automatically)

## Output

Creates a markdown file with build badges.

## Example

```yaml
- name: Generate build badges
  uses: ./.github/actions/generate-build-badges
  with:
    release-tag: v${{ steps.version.outputs.version }}
    output-file: BUILD_BADGES.md
```
