# setup-cargo-fmt-toml

Installs `cargo-fmt-toml` for formatting and normalizing Cargo.toml
files, with caching.

## Usage

```yaml
- name: Setup cargo-fmt-toml
  uses: ./.github/actions/setup-cargo-fmt-toml
```

## Features

- Uses cargo-binstall for fast installation
- Caches the binary between runs
- Cross-platform support
- Automatically configures PATH

## What it does

1. Sets up cargo-binstall (dependency)
2. Checks for cached `cargo-fmt-toml` binary
3. Installs via cargo-binstall if not cached
4. Adds `~/.cargo/bin` to PATH
5. Verifies installation

## After this step

```bash
cargo fmt-toml              # Format all Cargo.toml files
cargo fmt-toml --check      # Check if formatting is needed
cargo fmt-toml --dry-run    # Preview changes
```

## Dependencies

- `setup-cargo-binstall` (called automatically)

## Cross-Platform Support

Works on:

- Linux (ubuntu-latest, ubuntu-24.04, etc.)
- macOS (macos-latest, macos-15-xlarge, etc.)
- Windows (windows-latest)
