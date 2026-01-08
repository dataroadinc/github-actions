# setup-cargo-edit

Installs `cargo-edit` (provides `cargo set-version`, `cargo add`,
etc.) with caching.

## Usage

```yaml
- name: Setup cargo-edit
  uses: ./.github/actions/setup-cargo-edit
```

## Features

- Uses cargo-binstall for fast installation
- Caches the binary between runs
- Pins to version 0.13.0 for consistency
- Cross-platform support
- Required for Cocogitto version bumping

## What it does

1. Sets up cargo-binstall (dependency)
2. Checks for cached `cargo-edit` binary
3. Installs via cargo-binstall if not cached
4. Adds `~/.cargo/bin` to PATH
5. Verifies installation

## After this step

```bash
cargo set-version 0.1.0    # Set version in Cargo.toml
cargo add serde            # Add dependencies
cargo rm old-dep           # Remove dependencies
```

## Dependencies

- `setup-cargo-binstall` (called automatically)

## Cross-Platform Support

Works on:

- Linux (ubuntu-latest, ubuntu-24.04, etc.)
- macOS (macos-latest, macos-15-xlarge, etc.)
- Windows (windows-latest)

## Version

Currently pinned to version 0.13.0. To update, edit `action.yml` and
change the version in the cache key and install command.
