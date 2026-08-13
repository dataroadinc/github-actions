# legra-ai/github-actions

Reusable GitHub Actions for Rust CI/CD workflows.

## Overview

This repository contains reusable composite actions for common CI/CD tasks
in Rust projects. All actions provide caching and consistent behavior
across workflows.

## Available Actions

See [`.github/actions/README.md`](.github/actions/README.md) for complete
documentation of all available actions.

### Quick Links

- **[Setup Actions](.github/actions/README.md#setup-actions)** - Install
  development tools (cargo-binstall, cargo-edit, cocogitto, etc.)
- **[Version Management](.github/actions/README.md#version-management-actions)** -
  Get and calculate versions
- **[Changelog & Release](.github/actions/README.md#changelog--release-actions)** -
  Generate changelogs, PR logs, release pages, and badges
- **[Release Management](.github/actions/README.md#release-management-actions)** -
  Create releases, attach artifacts, update badges

## Usage

Reference actions using the path syntax:

```yaml
- name: Setup Cocogitto
  uses: legra-ai/github-actions/.github/actions/setup-cocogitto@main
  with:
    version: 6.5.0 # Optional, defaults to env var or 6.5.0

- name: Generate changelog
  uses: legra-ai/github-actions/.github/actions/generate-changelog@main
  with:
    release-tag: v0.1.0
```

## Versioning

- **Initial release**: `v0.0.1`
- Use `@main` until all bugs are ironed out
- After stabilization, bump to `v1.0.0` and use `@v1` going forward

## License

Creative Commons Attribution-ShareAlike 4.0 International

See [LICENSE](LICENSE) for details.
