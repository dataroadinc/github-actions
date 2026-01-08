# setup-dioxus

Installs Dioxus CLI with caching.

## Usage

```yaml
- name: Setup Dioxus CLI
  uses: ./.github/actions/setup-dioxus
  with:
    version: 0.7.2 # Required: Dioxus CLI version to install
```

## Inputs

| Input     | Description                        | Required | Default |
| --------- | ---------------------------------- | -------- | ------- |
| `version` | Dioxus CLI version (e.g., `0.7.2`) | Yes      | -       |

## Features

- Downloads prebuilt binaries from GitHub releases
- Caches the binary between runs
- Cross-platform support (Linux, macOS, Windows)
- Automatically configures PATH

## What it does

1. Checks for cached Dioxus CLI binary
2. Downloads from GitHub releases if not cached
3. Extracts and installs to `~/.cargo/bin`
4. Adds `~/.cargo/bin` to PATH

## After this step

```bash
dx --version  # Check Dioxus CLI version
dx build      # Build Dioxus application
```

## Dependencies

None

## Cross-Platform Support

Works on:

- Linux (x86_64, aarch64)
- macOS (x86_64, aarch64)
- Windows (x86_64)

## Example

```yaml
- name: Setup Dioxus CLI
  uses: ./.github/actions/setup-dioxus
  with:
    version: 0.7.2
```
