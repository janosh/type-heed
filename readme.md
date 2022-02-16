# Type Heed

[![Tests](https://github.com/janosh/type-heed/actions/workflows/test.yml/badge.svg)](https://github.com/janosh/type-heed/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/janosh/type-heed/main.svg)](https://results.pre-commit.ci/latest/github/janosh/type-heed/main)
[![Requires Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/downloads)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Python code formatter (and [`pre-commit`](https://pre-commit.com) hook) for auto-removing [`mypy`](https://github.com/python/mypy) `#type: ignore` comments from lines that no longer cause type errors.

## Installation

```sh
pip install type-heed
```

## Usage

### CLI

```sh
type-heed path/to/file.py
# or
type-heed **/*.py
```

### As `pre-commit` hook

Add this to your `.pre-commit-config.yaml`:

```yml
repos
  - repo: https://github.com/janosh/type-heed
    rev: v0.1.0
    hooks:
      - id: type-heed
```
