# generate-manifest

Generate manifest.json for runtime distribution with version,
checksums, and download URLs.

## Usage

```yaml
- name: Generate manifest
  id: manifest
  uses: ./.github/actions/generate-manifest
  with:
    version: 0.2.0
    git-commit: ${{ github.sha }}
    artifacts-dir: artifacts
    output-file: manifest.json
    base-url: /downloads/v0.2.0
```

## Inputs

| Input           | Description                    | Required | Default         |
| --------------- | ------------------------------ | -------- | --------------- |
| `version`       | Version string (e.g., `0.2.0`) | Yes      | -               |
| `git-commit`    | Git commit SHA                 | Yes      | -               |
| `artifacts-dir` | Directory containing artifacts | Yes      | `artifacts`     |
| `output-file`   | Output manifest.json file path | Yes      | `manifest.json` |
| `base-url`      | Base URL for downloads         | Yes      | -               |

## Outputs

| Output          | Description                     |
| --------------- | ------------------------------- |
| `manifest-path` | Path to generated manifest.json |

## Features

- Generates JSON manifest with version, timestamp, and commit info
- Scans artifacts directory for desktop and CLI artifacts
- Calculates SHA256 checksums for each artifact
- Parses platform and architecture from filenames
- Validates JSON syntax

## What it does

1. Creates manifest JSON structure with placeholders
2. Scans artifacts directory for desktop-_ and cli-_ directories
3. For each artifact file:
   - Calculates file size and SHA256 checksum
   - Parses platform (macos/windows/linux) and arch (arm64/x64) from
     filename
   - Builds JSON object with metadata
4. Updates manifest with artifact arrays
5. Validates JSON syntax

## Dependencies

None (uses standard Unix tools: `jq`, `sha256sum`/`shasum`, `stat`)

## Example

```yaml
- name: Generate manifest
  id: manifest
  uses: ./.github/actions/generate-manifest
  with:
    version: ${{ steps.version.outputs.version }}
    git-commit: ${{ github.sha }}
    artifacts-dir: artifacts
    output-file: manifest.json
    base-url:
      https://github.com/${{ github.repository
      }}/releases/download/v${{ steps.version.outputs.version }}
```

## Manifest Structure

```json
{
  "version": "0.2.0",
  "released_at": "2024-01-01T12:00:00Z",
  "git_commit": "abc123...",
  "artifacts": {
    "desktop": [...],
    "cli": [...],
    "backend": []
  },
  "checksums_url": "/downloads/v0.2.0/sha256sums.txt"
}
```

## Notes

- Artifact filenames should follow pattern:
  `*-{platform}-{arch}-*.{ext}` (e.g.,
  `myapp-desktop-macos-arm64-v0.2.0.dmg`)
- Currently expects `desktop-*` and `cli-*` directory prefixes
- Platform and arch are parsed from filenames using regex
