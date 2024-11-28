# Contributing to Vellum Python SDKs

Thank you for your interest in contributing to the Vellum Python SDKs! This document provides guidelines and instructions for contributing.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/vellum-ai/vellum-python-sdks.git
```

2. Setup your development environment:

```bash
make setup
```

3. Verify installation is correct by running tests and ensuring success:

```bash
make test
```

## Tooling

This section talks through the tooling you should be familiar with to contribute to the Vellum Python SDKs.

### Fern

[Fern](https://buildwithfern.com/) is used to auto-generate the Vellum Python SDKs. It's a CLI tool that can generate SDKs in a variety of languages. All files not specified in the `.fernignore` file are assumed to be auto-generated and should not be modified manually. All files and directories specified there explicitly are assumed to be manually maintained and are open to direct contribution from this repository.

### Poetry

[Poetry](https://python-poetry.org/) is used to manage dependencies, build, and publish the Vellum Python SDKs. It manages a virtual environment in the `.venv` directory and allows you to install dependencies in an isolated environment. It additionally supports building and publishing to PyPI.

## Development

Each contribution should be made in its own branch, and accompanied with a test:

- `src/vellum/workflows/**/tests` - if unit testing the relevant file is sufficient for testing the new feature
- `tests/workflows` - if you need to test the new feature in the context of an entire workflow
- `vellum_ee/**/tests` - if you need to test the new feature in the context of Vellum Enterprise feature, such as serialization
- `tests/client` - these tests are generated automatically by [Fern](https://buildwithfern.com/) and should not be modified manually

To actually run the tests:

- `make test` - runs the test while spinning up Fern's mock server. Useful for running their tests specifically. Supports a `file` argument for running a specific file or directory.
- `make test-raw` - runs the test just using poetry. Useful for running tests that don't require the mock server, such as all Workflows SDK tests. Supports a `file` argument for running a specific file or directory.
