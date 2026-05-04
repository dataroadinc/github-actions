# package-artifacts

Package downloaded build artifacts into zip files for release.

## Usage

```yaml
- name: Package artifacts
  id: package
  uses: ./.github/actions/package-artifacts
  with:
    artifacts-dir: artifacts/
    output-dir: release-packages
```

## Inputs

| Input           | Description                    | Required | Default            |
| --------------- | ------------------------------ | -------- | ------------------ |
| `artifacts-dir` | Directory containing artifacts | No       | `artifacts/`       |
| `output-dir`    | Directory to output zip files  | No       | `release-packages` |

## Outputs

| Output          | Description                |
| --------------- | -------------------------- |
| `package-count` | Number of packages created |

## Features

- Packages each artifact directory as a separate zip file
- Preserves directory structure within each zip
- Useful for preparing artifacts before upload to release

## What it does

1. Scans artifacts directory for subdirectories
2. Creates zip file for each subdirectory
3. Outputs zip files to specified output directory
4. Returns count of packages created

## Dependencies

None

## Example

```yaml
- name: Download artifacts
  uses: actions/download-artifact@v7
  with:
    path: artifacts/

- name: Package artifacts
  id: package
  uses: ./.github/actions/package-artifacts
  with:
    artifacts-dir: artifacts/
    output-dir: release-packages

- name: Upload packages
  run:
    echo "Created ${{ steps.package.outputs.package-count }} packages"
```

## Notes

- Expects artifacts directory to contain subdirectories
- Each subdirectory becomes a separate zip file
- Zip files are named after the subdirectory name
