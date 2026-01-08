# get-version

Get current version from Cargo.toml and compare with latest git tag
using cargo-version-info.

## Usage

```yaml
- name: Get version
  id: version
  uses: ./.github/actions/get-version
```

## Outputs

| Output               | Description                                     |
| -------------------- | ----------------------------------------------- |
| `version`            | Current version from Cargo.toml (e.g., `0.0.1`) |
| `version_changed`    | Whether version changed since last tag          |
| `latest_tag_version` | Version from latest git tag (e.g., `0.0.1`)     |

## Features

- Uses `cargo version-info current` to get version from Cargo.toml
- Uses `cargo version-info changed` to compare with latest git tag
- Outputs in GitHub Actions format for easy use in workflows

## What it does

1. Sets up cargo-version-info (dependency)
2. Gets current version from Cargo.toml
3. Compares with latest git tag
4. Outputs version information and change status

## Dependencies

- `setup-cargo-version-info` (called automatically)

## Example

```yaml
- name: Get version
  id: version
  uses: ./.github/actions/get-version

- name: Check if version changed
  if: steps.version.outputs.version_changed == 'true'
  run: echo "Version changed to ${{ steps.version.outputs.version }}"
```
