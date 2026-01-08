#!/usr/bin/env bash
set -euo pipefail

# Setup git hooks for this repository
# This script configures git to use the .githooks directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="${SCRIPT_DIR}/.githooks"

echo "Setting up git hooks..."

# Check if .githooks directory exists
if [ ! -d "$HOOKS_DIR" ]; then
  echo "Error: .githooks directory not found at $HOOKS_DIR" >&2
  exit 1
fi

# Configure git to use .githooks
git config core.hooksPath .githooks

echo "✓ Git hooks configured to use .githooks directory"
echo ""
echo "Hooks will now be enforced for all commits."
echo ""
echo "Note: Make sure cocogitto is installed:"
echo "  cargo install cocogitto"
