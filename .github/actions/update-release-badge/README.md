# update-release-badge

Update a specific badge in a GitHub release body.

## Usage

```yaml
- name: Update release badge
  uses: ./.github/actions/update-release-badge
  with:
    release-tag: v0.0.1
    badge-name: "CLI macOS ARM"
    status: success # success, failure, or pending
```

## Inputs

| Input         | Description                          | Required | Default   |
| ------------- | ------------------------------------ | -------- | --------- |
| `release-tag` | Release tag (e.g., `v0.0.1`)         | Yes      | -         |
| `badge-name`  | Badge name/identifier                | Yes      | -         |
| `status`      | Status: success, failure, or pending | Yes      | `pending` |

## Features

- Updates individual badges in release body
- Supports success (green ✓), failure (red ✗), and pending (gray ○)
  statuses
- Uses shields.io badges
- Replaces existing badges or skips if not found

## What it does

1. Gets current release body
2. Finds badge by name
3. Replaces badge with new status
4. Updates release body

## Dependencies

None (uses `gh` CLI which is available in GitHub Actions runners)

## Example

```yaml
- name: Update badge after build
  uses: ./.github/actions/update-release-badge
  with:
    release-tag: v${{ steps.version.outputs.version }}
    badge-name: "CLI macOS ARM"
    status: success
```

## Badge Statuses

- `success` - Green badge with ✓
- `failure` - Red badge with ✗
- `pending` - Gray badge with ○

## Notes

- Badge must already exist in release body (created by
  `generate-build-badges` or `generate-release-page`)
- If badge not found, action exits successfully without error
- Badge names should match exactly (case-sensitive)
