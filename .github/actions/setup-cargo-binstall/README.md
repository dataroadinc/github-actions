# setup-cargo-binstall

Installs `cargo-binstall` for fast binary installations with caching.

## Usage

```yaml
- name: Setup cargo-binstall
  uses: ./.github/actions/setup-cargo-binstall
```

## Features

- Caches the binary between runs
- Cross-platform support (Linux, macOS, Windows)
- Automatic PATH configuration
- No dependencies required

## What it does

1. Checks for cached `cargo-binstall` binary
2. Installs via official install script if not cached
3. Adds `~/.cargo/bin` to PATH
4. Verifies installation

## After this step

```bash
cargo-binstall --version  # Check version
cargo binstall tool-name  # Install tools
```

## Dependencies

None - this is the base action that other setup actions depend on.

## Cross-Platform Support

Works on:

- Linux (ubuntu-latest, ubuntu-24.04, etc.)
- macOS (macos-latest, macos-15-xlarge, etc.)
- Windows (windows-latest)

Windows binaries are handled with `.exe` extension automatically.
