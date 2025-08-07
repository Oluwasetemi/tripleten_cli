# TripleTen CLI Testing Guide

This document provides comprehensive information about the testing setup, conventions, and best practices for the TripleTen CLI project.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Test Categories](#test-categories)
- [Mocking and Fixtures](#mocking-and-fixtures)
- [Continuous Integration](#continuous-integration)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)

## Overview

The TripleTen CLI project uses a comprehensive testing strategy with:

- **pytest** as the main testing framework
- **pytest-asyncio** for async test support
- **responses** library for HTTP API mocking
- **freezegun** for time-based testing
- **pytest-cov** for coverage reporting
- **tox** for multi-environment testing

## Test Structure

```
tests/
├── __init__.py
├── test_cli.py          # CLI interface tests
├── test_config.py       # Configuration management tests
├── test_client.py       # HTTP client tests
├── test_render.py       # Rendering functionality tests
├── test_main.py         # Main module tests
└── conftest.py          # Shared fixtures (if needed)
```

### Test Coverage Areas

#### 1. Configuration Management (`test_config.py`)
- ✅ Config file read/write operations
- ✅ TOML parsing and validation
- ✅ Cross-platform directory handling
- ✅ Secure permissions on Unix systems
- ✅ Default value management
- ✅ Property-based access patterns

#### 2. HTTP Client (`test_client.py`)
- ✅ Session management and cookies
- ✅ Authentication handling
- ✅ API request/response patterns
- ✅ Error handling and retry logic
- ✅ Network timeout scenarios
- ✅ Cookie persistence across sessions

#### 3. Rendering Engine (`test_render.py`)
- ✅ Rich library integration
- ✅ Tabulate fallback functionality
- ✅ Basic text rendering
- ✅ User highlighting logic
- ✅ JSON data parsing
- ✅ Edge case handling

#### 4. CLI Interface (`test_cli.py`)
- ✅ Command-line argument parsing
- ✅ Watch mode and diff logic
- ✅ Configuration integration
- ✅ Error handling and fallbacks
- ✅ Interactive prompts
- ✅ Data change detection

## Running Tests

### Quick Test Commands

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run only unit tests (fast)
make test-unit

# Run integration tests
make test-integration

# Run specific test file
pytest tests/test_config.py

# Run specific test method
pytest tests/test_config.py::TestConfig::test_save_and_load
```

### Using Pytest Directly

```bash
# Basic test run
pytest tests/

# With coverage
pytest tests/ --cov=tripleten_cli --cov=client --cov=render

# Verbose output
pytest tests/ -v

# Stop on first failure
pytest tests/ -x

# Run tests in parallel
pytest tests/ -n auto

# Watch for changes
pytest tests/ --looponfail
```

### Test Markers

Tests are categorized using pytest markers:

```bash
# Run only unit tests
pytest -m "unit"

# Run only integration tests
pytest -m "integration"

# Skip slow tests
pytest -m "not slow"

# Run specific component tests
pytest -m "client"
pytest -m "render"
pytest -m "config"
```

## Test Coverage

### Coverage Requirements

- Minimum coverage: **80%**
- Target coverage: **90%+**
- Critical modules: **95%+**

### Coverage Reports

```bash
# Generate HTML coverage report
make test-coverage

# View coverage in browser
open htmlcov/index.html

# Terminal coverage report
pytest --cov=tripleten_cli --cov-report=term-missing
```

### Coverage Configuration

Coverage is configured in `pytest.ini` and `tox.ini`:

```ini
[coverage:run]
source = src/tripleten_cli, client, render
omit = */tests/*, setup.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

## Test Categories

### Unit Tests (Fast)

- Test individual functions and methods
- Use mocks for external dependencies
- Run in isolation
- Should be fast (<1s each)

```python
def test_config_get_set(config_instance):
    config_instance.set("test_key", "test_value")
    assert config_instance.get("test_key") == "test_value"
```

### Integration Tests

- Test component interactions
- Use real HTTP calls (with responses mocking)
- Test CLI commands end-to-end
- May be slower but more comprehensive

```python
@responses.activate
def test_client_leaderboard_fetch():
    responses.add(responses.GET, "/api/leaderboard", json={"data": []})
    result = client.fetch_leaderboard("all")
    assert result == {"data": []}
```

### Slow Tests

- Performance tests
- Large dataset processing
- Network timeout scenarios
- Only run during full CI or manually

```python
@pytest.mark.slow
def test_large_leaderboard_rendering():
    large_data = [{"rank": i, "user": f"User{i}"} for i in range(10000)]
    render_leaderboard(large_data, "current_user")
```

## Mocking and Fixtures

### Common Test Patterns

#### Configuration Mocking

```python
@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config for testing."""
    with patch.object(Config, '_get_config_dir', return_value=tmp_path):
        yield Config()
```

#### HTTP Client Mocking

```python
@responses.activate
def test_api_call():
    responses.add(responses.GET, "https://api.example.com", json={"success": True})
    result = client.make_request("GET", "/endpoint")
    assert result["success"] is True
```

#### CLI Testing

```python
def test_cli_command():
    runner = CliRunner()
    result = runner.invoke(cli_command, ["--option", "value"])
    assert result.exit_code == 0
    assert "expected output" in result.output
```

### Time-based Testing

```python
from freezegun import freeze_time

@freeze_time("2024-01-01 12:00:00")
def test_timestamp_generation():
    timestamp = get_current_timestamp()
    assert timestamp == "2024-01-01 12:00:00"
```

## Continuous Integration

### GitHub Actions Workflow

The CI pipeline runs:

1. **Linting**: Code formatting and style checks
2. **Type Checking**: MyPy static analysis
3. **Unit Tests**: Fast tests across Python versions
4. **Integration Tests**: Component interaction tests
5. **Security Scanning**: Bandit and Safety checks
6. **Coverage Reporting**: Upload to Codecov

### Multi-Environment Testing

Using tox for testing across Python versions:

```bash
# Test all environments
tox

# Test specific Python version
tox -e py311

# Parallel testing
tox -p

# Recreate environments
tox -r
```

## Development Workflow

### Pre-commit Hooks

```bash
# Install pre-commit hooks
make install-pre-commit

# Run pre-commit checks
make pre-commit
```

### Test-Driven Development

1. Write failing test
2. Implement minimal code to pass
3. Refactor and improve
4. Ensure all tests pass

### Adding New Tests

1. Choose appropriate test file
2. Use descriptive test names
3. Add appropriate markers
4. Include docstrings
5. Mock external dependencies
6. Test both success and failure cases

```python
class TestNewFeature:
    """Test suite for new feature functionality."""

    def test_feature_success_case(self):
        """Test that feature works correctly with valid input."""
        result = new_feature("valid_input")
        assert result == "expected_output"

    def test_feature_error_handling(self):
        """Test that feature handles errors gracefully."""
        with pytest.raises(ValueError):
            new_feature("invalid_input")
```

## Troubleshooting

### Common Issues

#### Import Errors

```python
# Add parent directory to path for root-level imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

#### Mock Not Working

```python
# Ensure you're patching the right location
# Patch where the function is used, not where it's defined
with patch('module_using_function.function_name') as mock_func:
    # test code
```

#### Async Test Issues

```python
# Use pytest-asyncio for async tests
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

#### Coverage Not Showing

```bash
# Ensure coverage is measuring the right modules
pytest --cov=src/tripleten_cli --cov=client --cov=render

# Check coverage configuration in pytest.ini
```

### Debugging Tests

```bash
# Run with debugging output
pytest tests/ -v -s

# Drop into debugger on failure
pytest tests/ --pdb

# Run only failed tests from last run
pytest tests/ --lf

# Show test execution times
pytest tests/ --durations=10
```

### Performance Issues

```bash
# Profile test execution
pytest tests/ --durations=0

# Run tests in parallel
pytest tests/ -n auto

# Use pytest-benchmark for performance tests
pytest tests/ --benchmark-only
```

## Best Practices

### Test Writing Guidelines

1. **One Concept Per Test**: Each test should verify one specific behavior
2. **Descriptive Names**: Test names should clearly describe what is being tested
3. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
4. **Independent Tests**: Tests should not depend on each other
5. **Mock External Dependencies**: Don't rely on external services in tests

### Assertion Guidelines

```python
# Good: Specific assertions
assert result.status_code == 200
assert "error" not in result.output
assert len(data) == 5

# Avoid: Vague assertions
assert result is not None
assert result
```

### Mock Guidelines

```python
# Good: Mock at the boundary
with patch('requests.get') as mock_get:
    mock_get.return_value.json.return_value = {"data": "test"}

# Avoid: Over-mocking internal functions
```

This testing setup provides comprehensive coverage for all aspects of the TripleTen CLI, ensuring reliability, maintainability, and confidence in the codebase.
