# publish-draft-release

Publish an existing draft release for the given version.

## Usage

```yaml
- name: Publish draft release
  uses: ./.github/actions/publish-draft-release
  with:
    version: 0.0.1
```

## Inputs

| Input     | Description                    | Required | Default |
| --------- | ------------------------------ | -------- | ------- |
| `version` | Version number (e.g., `0.0.1`) | Yes      | -       |

## Features

- Publishes draft releases to make them public
- Handles already-published releases gracefully
- Skips if release doesn't exist

## What it does

1. Checks if release exists for the version tag
2. Checks if release is a draft
3. Publishes draft release if found
4. Skips if already published or doesn't exist

## Dependencies

None (uses `gh` CLI which is available in GitHub Actions runners)

## Example

```yaml
- name: Publish draft release
  uses: ./.github/actions/publish-draft-release
  with:
    version: ${{ steps.version.outputs.version }}
```

## Notes

- Only publishes draft releases
- Published releases are immutable, so this action will skip if
  already published
- Use this after all artifacts have been attached and release page has
  been generated
