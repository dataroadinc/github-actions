# setup-cocogitto

Installs Cocogitto (`cog`) for version management and changelog
generation, with caching.

## Usage

```yaml
- name: Setup Cocogitto
  uses: ./.github/actions/setup-cocogitto
```

## Features

- Uses cargo-binstall for fast installation
- Caches the binary between runs
- Pins to version 6.5.0 for consistency
- Cross-platform support
- Automatically installs cargo-edit dependency

## What it does

1. Sets up cargo-binstall (dependency)
2. Sets up cargo-edit (dependency, required for version bumping)
3. Checks for cached `cocogitto` binary
4. Installs via cargo-binstall if not cached
5. Adds `~/.cargo/bin` to PATH
6. Verifies installation

## After this step

```bash
cog --version           # Check cocogitto version
cog bump --patch        # Bump patch version (uses cargo set-version)
cog changelog           # Generate changelog
```

## Dependencies

- `setup-cargo-binstall` (called automatically)
- `setup-cargo-edit` (called automatically, required for version
  bumping)

## Important

Cocogitto requires `cargo set-version` (from cargo-edit) to be
available for version bumping. This action automatically installs both
tools.

## Cross-Platform Support

Works on:

- Linux (ubuntu-latest, ubuntu-24.04, etc.)
- macOS (macos-latest, macos-15-xlarge, etc.)
- Windows (windows-latest)

## Version

Currently pinned to version 6.5.0. To update, edit `action.yml` and
change the version in the cache key and install command.
