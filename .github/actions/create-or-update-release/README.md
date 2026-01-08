# create-or-update-release

Create a new release or update existing one with fresh content and
placeholder badges.

## Usage

```yaml
- name: Create or update release
  id: release
  uses: ./.github/actions/create-or-update-release
  with:
    version: 0.0.1
```

## Inputs

| Input     | Description                    | Required | Default |
| --------- | ------------------------------ | -------- | ------- |
| `version` | Version number (e.g., `0.0.1`) | Yes      | -       |

## Outputs

| Output            | Description                                    |
| ----------------- | ---------------------------------------------- |
| `release-id`      | GitHub release ID                              |
| `release-created` | Whether a new release was created (true/false) |

## Features

- Creates draft release if it doesn't exist
- Deletes and recreates existing releases (published releases are
  immutable)
- Ensures tag points to current HEAD
- Creates placeholder release body ("Building...")
- Full release page generated when artifacts are attached

## What it does

1. Checks if release exists for the version tag
2. Deletes existing release if found (to allow recreation)
3. Deletes existing tag if found (via GitHub API to bypass repository
   rules)
4. Creates new draft release with placeholder content
5. Returns release ID for use in subsequent steps

## Dependencies

None (uses `gh` CLI which is available in GitHub Actions runners)

## Example

```yaml
- name: Create or update release
  id: release
  uses: ./.github/actions/create-or-update-release
  with:
    version: ${{ steps.version.outputs.version }}

- name: Use release ID
  run: echo "Release ID: ${{ steps.release.outputs.release-id }}"
```

## Notes

- Always creates a draft release (publish separately with
  `publish-draft-release` action)
- Uses GitHub API to delete tags, bypassing repository rules
- Tag is automatically created by `gh release create` pointing to HEAD
