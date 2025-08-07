# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Testing
- Run all tests: `pytest` or `make test`
- Run tests with coverage: `pytest --cov=tripleten_cli --cov=client --cov=render --cov-report=html --cov-report=xml --cov-report=term-missing` or `make test-coverage`
- Run unit tests only: `pytest -m "not slow and not integration"` or `make test-unit`
- Run integration tests: `pytest -m integration` or `make test-integration`
- Run tests in parallel: `pytest -n auto` or `make test-parallel`
- Run specific test: `pytest tests/test_cli.py::test_specific_function`

### Code Quality
- Format code: `black src/ tests/` and `isort src/ tests/` or `make format`
- Lint code: `flake8 src/ tests/` or `make lint`
- Type checking: `mypy src/ --ignore-missing-imports` or `make type-check`
- Run all quality checks: `make check` (fast) or `make pre-commit`

### Build and Package
- Build package: `python -m build` or `make build`
- Install in development mode: `pip install -e ".[dev]"` or `make install-dev`
- Clean build artifacts: `make clean`

### Security Analysis
- Security scan: `bandit -r src/ -ll` and `safety check` or `make security`

### Development Setup
- Full development setup: `make dev-setup`
- Install pre-commit hooks: `pre-commit install` or `make install-pre-commit`

## Architecture Overview

### Package Structure
The project uses a src layout with the main package in `src/tripleten_cli/`:
- `src/tripleten_cli/cli.py` - Click CLI commands and main interface
- `src/tripleten_cli/config.py` - Configuration management with TOML files
- `src/tripleten_cli/client.py` - HTTP client for TripleTen API with clipboard authentication
- `src/tripleten_cli/render.py` - Rich table rendering for leaderboards with highlighting

### Key Design Patterns
1. **Configuration Management**: Uses platformdirs for cross-platform config directories, TOML files for settings, singleton pattern for config access
2. **CLI Architecture**: Click-based with grouped commands, default command is leaderboard, watch mode for real-time updates
3. **API Client**: Direct HTTP client connecting to `https://hub.tripleten.com/internal_api//gamification/leaderboard` (note double slash), browser cookie-based authentication with clipboard integration, mimics Firefox headers exactly, transforms `top_members` API response to `leaderboard` format for CLI compatibility
4. **Authentication**: Clipboard-first login approach using pyperclip, automatic cookie parsing and domain setting, secure local storage with restricted permissions
5. **Rich Display**: Uses Rich library for styled tables with rank highlighting and user identification, fallback display when render module unavailable
6. **Error Handling**: Custom ConfigError and AuthenticationError exceptions, graceful degradation with warnings, fallback to sample data when API fails

### Module Dependencies
- The CLI imports client and render modules from within the package (`src/tripleten_cli/`)
- Config module is self-contained with platform-specific directory handling
- Rich console output with fallback plain text tables
- PyPerClip for clipboard integration (graceful fallback when unavailable)

### Testing Strategy
- Unit tests for individual components
- Integration tests for API interactions
- CLI tests using click.testing.CliRunner
- Coverage requirements set to 80%
- Test markers: slow, integration, unit, client, render, cli, config

### Configuration System
- Uses TOML format stored in platform-appropriate config directories
- Secure file permissions (0o600) on Unix systems
- Singleton config manager with property-based access
- Default values: default_period="all_time", default_interval=30

### Build System
- Uses setuptools with pyproject.toml configuration
- Entry point: `tripleten = "tripleten_cli.cli:tripleten"`
- Supports Python 3.9+
- Development dependencies include full testing and quality toolchain
