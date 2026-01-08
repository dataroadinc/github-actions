# setup-dotenvage

Installs `dotenvage` with caching for environment file processing.

## Usage

```yaml
- name: Setup dotenvage
  uses: ./.github/actions/setup-dotenvage
```

## Features

- Uses cargo-binstall for fast installation
- Caches the binary between runs
- Cross-platform support
- Automatically configures PATH

## What it does

1. Sets up cargo-binstall (dependency)
2. Checks for cached `dotenvage` binary
3. Installs via cargo-binstall if not cached (pinned to version 0.0.9)
4. Adds `~/.cargo/bin` to PATH
5. Verifies installation

## After this step

```bash
dotenvage --help  # See available commands
```

## Dependencies

- `setup-cargo-binstall` (called automatically)

## Cross-Platform Support

Works on:

- Linux (ubuntu-latest, ubuntu-24.04, etc.)
- macOS (macos-latest, macos-15-xlarge, etc.)
- Windows (windows-latest)

## Version

Currently pinned to version 0.0.9. To update, edit `action.yml` and
change the version in the cache key and install command.
