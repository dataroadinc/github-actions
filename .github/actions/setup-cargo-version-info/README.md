# setup-cargo-version-info

Installs `cargo-version-info` with caching for unified version
management.

## Usage

```yaml
- name: Setup cargo-version-info
  uses: ./.github/actions/setup-cargo-version-info
```

## Features

- Uses cargo-binstall for fast installation
- Caches the binary between runs
- Cross-platform support
- Automatically configures PATH

## What it does

1. Sets up cargo-binstall (dependency)
2. Checks for cached `cargo-version-info` binary
3. Installs via cargo-binstall if not cached
4. Adds `~/.cargo/bin` to PATH
5. Verifies installation

## After this step

```bash
cargo version-info --help           # See available commands
cargo version-info current          # Get current version
cargo version-info next            # Calculate next version
cargo version-info changelog       # Generate changelog
cargo version-info badge all       # Generate badges
```

## Dependencies

- `setup-cargo-binstall` (called automatically)

## Cross-Platform Support

Works on:

- Linux (ubuntu-latest, ubuntu-24.04, etc.)
- macOS (macos-latest, macos-15-xlarge, etc.)
- Windows (windows-latest)

## Related Actions

This action is used by:

- `generate-changelog`
- `generate-pr-log`
- `generate-release-page`
- `generate-build-badges`
- `get-version`
- `calculate-next-version`
