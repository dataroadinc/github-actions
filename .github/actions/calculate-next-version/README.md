# calculate-next-version

Determine next patch version from latest GitHub release using
cargo-version-info.

## Usage

```yaml
- name: Calculate next version
  id: next
  uses: ./.github/actions/calculate-next-version
```

## Outputs

| Output    | Description                                  |
| --------- | -------------------------------------------- |
| `version` | Next patch version (e.g., `0.0.6`)           |
| `latest`  | Latest release version (e.g., `0.0.5`)       |
| `tag`     | Next tag name with v prefix (e.g., `v0.0.6`) |

## Features

- Uses `cargo version-info next` to calculate next patch version
- Queries GitHub releases to find latest version
- Outputs in GitHub Actions format

## What it does

1. Sets up cargo-version-info (dependency)
2. Queries GitHub API for latest release
3. Calculates next patch version
4. Outputs version and tag information

## Dependencies

- `setup-cargo-version-info` (called automatically)

## Example

```yaml
- name: Calculate next version
  id: next
  uses: ./.github/actions/calculate-next-version

- name: Use next version
  run: echo "Next version: ${{ steps.next.outputs.version }}"
  run: echo "Next tag: ${{ steps.next.outputs.tag }}"
```
