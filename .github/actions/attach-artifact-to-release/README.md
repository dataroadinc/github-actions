# attach-artifact-to-release

Attach build artifact to release and regenerate full release page.

## Usage

```yaml
- name: Attach artifact to release
  uses: ./.github/actions/attach-artifact-to-release
  with:
    release-tag: v0.0.1
    artifact-name: my-binary
    artifact-path: ./target/release/my-binary
```

## Inputs

| Input           | Description                        | Required | Default |
| --------------- | ---------------------------------- | -------- | ------- |
| `release-tag`   | Release tag (e.g., `v0.0.1`)       | Yes      | -       |
| `artifact-name` | Artifact name                      | Yes      | -       |
| `artifact-path` | Path to artifact file or directory | Yes      | -       |

## Features

- Attaches files or directories to GitHub release
- Automatically packages directories as zip files
- Cross-platform support (handles Windows differently)
- Regenerates release page after attaching artifact
- Uses `--clobber` to replace existing artifacts with same name

## What it does

1. Checks if release exists
2. Packages artifact (zips directories, copies files)
3. Uploads to GitHub release
4. Regenerates release page using `generate-release-page` action

## Dependencies

- `generate-release-page` (called automatically)

## Example

```yaml
- name: Build binary
  run: cargo build --release

- name: Attach artifact to release
  uses: ./.github/actions/attach-artifact-to-release
  with:
    release-tag: v${{ steps.version.outputs.version }}
    artifact-name: my-app
    artifact-path: ./target/release/my-app
```

## Notes

- Directories are automatically zipped before upload
- Windows uses PowerShell `Compress-Archive`, Linux/macOS uses `zip`
- Artifacts with the same name are replaced (clobbered)
- Release page is automatically regenerated after upload
