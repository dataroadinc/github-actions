# Contributing to github-actions

Thank you for your interest in contributing! This project uses
[Angular Conventional Commits](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
(also known as the
[Conventional Commits](https://www.conventionalcommits.org/)
specification) and [Cocogitto](https://github.com/cocogitto/cocogitto)
for automated changelog generation.

## Commit Message Format

We follow the **Angular Conventional Commits** specification. Each
commit message should be structured as follows:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature (appears in changelog)
- **fix**: A bug fix (appears in changelog)
- **docs**: Documentation changes (appears in changelog)
- **refactor**: Code refactoring (appears in changelog)
- **perf**: Performance improvements (appears in changelog)
- **build**: Changes to build system (appears in changelog)
- **revert**: Reverts a previous commit (appears in changelog)
- **style**: Code style changes (omitted from changelog)
- **test**: Adding or updating tests (omitted from changelog)
- **ci**: CI/CD changes (omitted from changelog)
- **chore**: Other changes (omitted from changelog)

### Scope (Optional)

The scope provides additional context:

- `actions`: Changes to GitHub Actions
- `workflows`: Changes to workflow files
- `setup-*`: Changes to specific setup actions (e.g., `setup-cocogitto`)
- `docs`: Documentation
- `deps`: Dependency updates

### Examples

```bash
# Feature commits
feat(actions): add new reusable action
feat(setup-cocogitto): add version parameter support

# Bug fix commits
fix(workflows): correct workflow syntax error
fix(actions): handle missing input parameters

# Documentation commits
docs: update README with action usage
docs(actions): improve action documentation

# Refactoring commits
refactor(actions): simplify action logic
refactor: extract common action patterns

# Chore commits (won't appear in changelog)
chore: update dependencies
test: add tests for action validation
ci: update GitHub Actions workflow
```

## Breaking Changes

For breaking changes, add `!` after the type/scope and include a
`BREAKING CHANGE:` section in the footer:

```bash
feat(actions)!: change action input format

BREAKING CHANGE: Action inputs changed from
positional to named parameters
```

## Development Workflow

### 1. Fork and Clone

```bash
git clone git@github.com:YOUR_USERNAME/github-actions.git
cd github-actions
```

### 1.5. Setup Git Hooks

Run the setup script to configure git hooks:

```bash
./setup-hooks.sh
```

This configures git to use the `.githooks` directory and enforce
Conventional Commits on all commits.

**Note**: You need `cocogitto` installed to validate commits:

```bash
cargo install cocogitto
```

### 2. Create a Branch

```bash
git checkout -b feat/my-new-feature
# or
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write code
- Add tests
- Update documentation
- Ensure tests pass (if applicable)
- Follow GitHub Actions best practices

### 4. Commit Changes

Use Angular Conventional Commits format:

```bash
git add .
git commit -m "feat(actions): add new feature"
```

**Tip**: Install Cocogitto locally to validate commits:

```bash
cargo install cocogitto
cog check  # Validate commits
```

### 5. Push and Create Pull Request

```bash
git push origin feat/my-new-feature
```

Then create a Pull Request on GitHub.

## Releasing a New Version

Only maintainers can release new versions. The process is automated:

### 1. Update Version in Action Files

```bash
# Edit action.yml files and bump the version
vim .github/actions/my-action/action.yml
```

### 2. Commit the Version Bump

```bash
git add .
git commit -m "chore: bump version to v0.0.2"
git push origin main
```

### 3. Automatic Release Process

When version tags are created, the CI workflow will automatically:

1. ✅ Run all checks
2. 📝 Generate changelog using Cocogitto (from conventional commits)
3. 📌 Create a git tag (e.g., `v0.0.2`)
4. 🎉 Create a GitHub Release with the changelog

**No manual tagging required!** The workflow detects version changes
and handles everything.

## Changelog Generation

The changelog is generated automatically from commit messages:

- **Included**: `feat`, `fix`, `docs`, `refactor`, `perf`, `build`,
  `revert`
- **Excluded**: `style`, `test`, `ci`, `chore`

This encourages meaningful commit messages and creates a clean,
user-focused changelog.

## Code Review

All contributions go through code review:

- Ensure CI passes (all checks must be green)
- Follow GitHub Actions best practices
- Add tests for new actions (if applicable)
- Update documentation
- Use Angular Conventional Commits format

## Questions?

Feel free to open an issue for questions or discussions!
