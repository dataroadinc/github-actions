# generate-release-page

Generates a complete release page combining badges, PR log, and
changelog using cargo-version-info.

## Usage

```yaml
- name: Generate release page
  uses: ./.github/actions/generate-release-page
  with:
    release-tag: v0.1.3
    output-file: RELEASE_PAGE.md # optional, defaults to RELEASE_PAGE.md
```

## Inputs

| Input         | Description                   | Required | Default           |
| ------------- | ----------------------------- | -------- | ----------------- |
| `release-tag` | Release tag (e.g., `v0.1.3`)  | Yes      | -                 |
| `output-file` | File to write release page to | No       | `RELEASE_PAGE.md` |

## Features

- Uses `cargo version-info release-page` for unified version
  management
- Combines badges, PR log, and changelog into a single document

## What it does

1. Sets up cargo-version-info (dependency)
2. Calls `cargo version-info release-page` with the release tag
3. Generates complete release page markdown

## Dependencies

- `setup-cargo-version-info` (called automatically)

## Output

Creates a markdown file with the complete release page.

## Example

```yaml
- name: Generate release page
  uses: ./.github/actions/generate-release-page
  with:
    release-tag: v${{ steps.version.outputs.version }}
    output-file: RELEASE_PAGE.md
```
