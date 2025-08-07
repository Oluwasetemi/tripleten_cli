# TripleTen CLI Development Makefile
#
# This Makefile provides convenient commands for common development tasks.
# Run 'make help' to see all available commands.

# Variables - detect virtual environment
ifdef VIRTUAL_ENV
    PYTHON := python
    PIP := pip
else
    PYTHON := python3
    PIP := pip3
endif
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy
TOX := tox
BANDIT := bandit
SAFETY := safety

# Default target
.DEFAULT_GOAL := help

# Phony targets (targets that don't create files)
.PHONY: help install install-dev clean test test-unit test-integration test-slow test-coverage lint format type-check security build docs serve-docs clean-docs tox all check pre-commit

help: ## Show this help message
	@echo "TripleTen CLI Development Commands"
	@echo "=================================="
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation
install: ## Install package in development mode
	$(PIP) install -e .

install-dev: ## Install package with development dependencies
	$(PIP) install -e ".[dev]"

install-pre-commit: ## Install pre-commit hooks
	pre-commit install
	pre-commit install --hook-type commit-msg

# Cleaning
clean: ## Remove build artifacts, cache files, and temporary files
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .tox/
	rm -rf docs/_build/

# Testing
test: ## Run all tests
	$(PYTEST) tests/

test-unit: ## Run unit tests only
	$(PYTEST) tests/ -m "not slow and not integration"

test-integration: ## Run integration tests only
	$(PYTEST) tests/ -m "integration"

test-slow: ## Run slow tests only
	$(PYTEST) tests/ -m "slow"

test-coverage: ## Run tests with coverage report
	$(PYTEST) tests/ --cov=tripleten_cli --cov=client --cov=render --cov-report=html --cov-report=xml --cov-report=term-missing

test-parallel: ## Run tests in parallel
	$(PYTEST) tests/ -n auto

test-watch: ## Run tests and watch for changes
	$(PYTEST) tests/ --looponfail

# Code Quality
lint: ## Run all linting tools
	$(FLAKE8) src/ tests/
	$(BLACK) --check --diff src/ tests/
	$(ISORT) --check-only --diff src/ tests/

format: ## Format code with black and isort
	$(BLACK) src/ tests/
	$(ISORT) src/ tests/

type-check: ## Run type checking with mypy
	$(MYPY) src/ --ignore-missing-imports

# Security
security: ## Run security analysis
	$(BANDIT) -r src/ -ll
	$(SAFETY) check

security-report: ## Generate detailed security reports
	$(BANDIT) -r src/ -f json -o bandit-report.json
	$(SAFETY) check --json --output safety-report.json

# Build
build: ## Build package
	$(PYTHON) -m build

build-check: ## Check built package
	$(PYTHON) -m twine check dist/*

# Documentation
docs: ## Build documentation
	sphinx-apidoc -o docs/api src/
	sphinx-build -b html docs/ docs/_build/html

serve-docs: ## Serve documentation locally
	cd docs/_build/html && $(PYTHON) -m http.server 8000

clean-docs: ## Clean documentation build files
	rm -rf docs/_build/
	rm -rf docs/api/

# Tox (Multiple environment testing)
tox: ## Run tox for all environments
	$(TOX)

tox-parallel: ## Run tox in parallel
	$(TOX) -p

tox-recreate: ## Recreate tox environments
	$(TOX) -r

# Combined targets
all: clean install-dev lint type-check test-coverage security build ## Run full development workflow

check: lint type-check test-unit ## Quick quality checks (fast)

pre-commit: format lint type-check test-unit ## Run pre-commit checks

ci: ## Simulate CI pipeline
	$(MAKE) clean
	$(MAKE) install-dev
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test-coverage
	$(MAKE) security
	$(MAKE) build
	$(MAKE) build-check

# Development helpers
dev-setup: ## Set up development environment
	$(MAKE) install-dev
	$(MAKE) install-pre-commit
	@echo "Development environment is ready!"
	@echo "Run 'make check' to verify everything works."

requirements: ## Generate requirements.txt files
	$(PIP) freeze > requirements-dev.txt
	$(PIP) install --dry-run --report - . | jq -r '.install[] | select(.metadata.name != "tripleten-cli") | .metadata.name + "==" + .metadata.version' > requirements.txt

# Database/Config management
clean-config: ## Remove local configuration files
	rm -rf ~/.config/tripleten-cli/
	rm -rf ~/.local/share/tripleten-ci/

reset-dev: clean clean-config ## Full development reset
	$(MAKE) dev-setup

# Release helpers
version-patch: ## Bump patch version
	@echo "Current version: $$(grep version pyproject.toml | head -1 | sed 's/.*= //' | tr -d '\"')"
	@read -p "Enter new patch version: " version && \
	sed -i.bak "s/version = .*/version = \"$$version\"/" pyproject.toml && \
	rm pyproject.toml.bak && \
	echo "Version updated to $$version"

version-minor: ## Bump minor version
	@echo "Current version: $$(grep version pyproject.toml | head -1 | sed 's/.*= //' | tr -d '\"')"
	@read -p "Enter new minor version: " version && \
	sed -i.bak "s/version = .*/version = \"$$version\"/" pyproject.toml && \
	rm pyproject.toml.bak && \
	echo "Version updated to $$version"

# Debug and troubleshooting
debug-env: ## Show development environment info
	@echo "Python version: $$($(PYTHON) --version)"
	@echo "Pip version: $$($(PIP) --version)"
	@echo "Virtual environment: $$VIRTUAL_ENV"
	@echo "Python path: $$(which $(PYTHON))"
	@echo "Current directory: $$(pwd)"
	@echo "Git branch: $$(git branch --show-current 2>/dev/null || echo 'Not a git repository')"

test-verbose: ## Run tests with verbose output
	$(PYTEST) tests/ -v -s

test-failed: ## Re-run only failed tests
	$(PYTEST) tests/ --lf

test-specific: ## Run specific test (usage: make test-specific TEST=test_name)
	$(PYTEST) tests/ -k "$(TEST)" -v

# Performance
profile-tests: ## Profile test execution time
	$(PYTEST) tests/ --durations=10

benchmark: ## Run performance benchmarks
	$(PYTEST) tests/ -m benchmark --benchmark-only

# Documentation shortcuts
docs-live: ## Build and serve docs with live reload
	sphinx-autobuild docs/ docs/_build/html --host 0.0.0.0 --port 8000

# Git hooks simulation
pre-push: ## Run checks before pushing
	$(MAKE) clean
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test-coverage
	$(MAKE) security

# Package verification
install-test: ## Test installation of built package
	$(PIP) install dist/*.whl --force-reinstall
	tripleten --version

# Environment info
env: ## Show all environment variables
	env | grep -E "(PYTHON|PIP|VIRTUAL|PATH)" | sort
