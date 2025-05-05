[![unit tests](https://github.com/DominiqueFuchs/resx-hooks/actions/workflows/main.yml/badge.svg)](https://github.com/DominiqueFuchs/resx-hooks/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DominiqueFuchs/resx-hooks/main.svg)](https://results.pre-commit.ci/latest/github/DominiqueFuchs/resx-hooks/main)

# resx-hooks

This package provides [pre-commit](https://pre-commit.com/) hooks to validate .resx XML localization files commonly used in .NET projects. It helps ensure consistent localization across different language resources by automatically checking for issues before code is committed.

## Hooks

### check-all

Includes all hooks listed below for convenience.

### check-keys-consistency

Ensures all .resx files have the same set of resource keys. This helps prevent missing translations or orphaned keys across different language files.

### check-empty-values

Detects and reports any resource entries that have empty or whitespace-only values. This helps identify missing translations that might have been overlooked.

### check-placeholders

Validates that string format placeholders (like `{0}` or `%s`) are consistent across all translations of the same resource key. This prevents runtime formatting errors caused by mismatched placeholders.

## Usage

```yaml
repos:
-   repo: https://github.com/DominiqueFuchs/resx-hooks
    rev: v0.2.0
    hooks:
    -   id: check-keys-consistency
    -   id: check-empty-values
    -   id: check-placeholders
```

If needed, you can also target specific files or patterns:

```yaml
-   id: check-keys-consistency
    args: ['path/to/Resources/*.resx']
```
