# setup-cargo-propagate-features

Installs `cargo-propagate-features` with caching for feature
propagation.

## Usage

```yaml
- name: Setup cargo-propagate-features
  uses: ./.github/actions/setup-cargo-propagate-features
```

## Features

- Uses cargo-binstall for fast installation
- Caches the binary between runs
- Cross-platform support
- Automatically configures PATH

## What it does

1. Sets up cargo-binstall (dependency)
2. Checks for cached `cargo-propagate-features` binary
3. Installs via cargo-binstall if not cached
4. Adds `~/.cargo/bin` to PATH
5. Verifies installation

## After this step

```bash
cargo propagate-features --help  # See available commands
```

## Dependencies

- `setup-cargo-binstall` (called automatically)

## Cross-Platform Support

Works on:

- Linux (ubuntu-latest, ubuntu-24.04, etc.)
- macOS (macos-latest, macos-15-xlarge, etc.)
- Windows (windows-latest)
