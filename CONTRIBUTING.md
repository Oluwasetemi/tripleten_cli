# Contributing to TripleTen CLI

We love your input! We want to make contributing to TripleTen CLI as easy and transparent as possible, whether it's:

- 🐛 Reporting a bug
- 💡 Discussing the current state of the code
- 🚀 Submitting a fix
- 🎯 Proposing new features
- 🧑‍💻 Becoming a maintainer

## 📋 Table of Contents

1. [Development Process](#development-process)
2. [Getting Started](#getting-started)
3. [Code Standards](#code-standards)
4. [Testing](#testing)
5. [Pull Request Process](#pull-request-process)
6. [Bug Reports](#bug-reports)
7. [Feature Requests](#feature-requests)
8. [Community Guidelines](#community-guidelines)

## 🔄 Development Process

We use [GitHub Flow](https://guides.github.com/introduction/flow/index.html), so all code changes happen through pull requests. Pull requests are the best way to propose changes to the codebase:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- A code editor (VS Code recommended)

### Local Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/tripleten-cli.git
   cd tripleten-cli
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # On Linux/macOS
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Verify your setup**
   ```bash
   # Run tests
   pytest

   # Check code style
   pre-commit run --all-files

   # Test CLI
   tripleten --version
   ```

### Project Structure

```
tripleten-cli/
├── src/tripleten_cli/          # Main package
│   ├── __init__.py
│   ├── cli.py                  # Click CLI commands
│   ├── config.py               # Configuration management
│   └── main.py                 # Entry point
├── tests/                      # Test files
├── docs/                       # Documentation
├── client.py                   # HTTP client for TripleTen API
├── render.py                   # Rich table rendering
├── pyproject.toml              # Project configuration
├── README.md                   # Main documentation
├── CONTRIBUTING.md             # This file
└── CHANGELOG.md                # Version history
```

## 📏 Code Standards

We maintain high code quality standards:

### Python Code Style

- **Formatter**: [Black](https://black.readthedocs.io/) with 88-character line length
- **Import Sorting**: [isort](https://pycqa.github.io/isort/)
- **Linting**: [flake8](https://flake8.pycqa.org/)
- **Type Checking**: [mypy](https://mypy.readthedocs.io/)

### Running Code Quality Tools

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

### Code Guidelines

1. **Functions and Classes**
   - Use descriptive names
   - Add type hints
   - Include docstrings for public functions

2. **Error Handling**
   - Use appropriate exception types
   - Provide helpful error messages
   - Log errors appropriately

3. **CLI Design**
   - Follow Click conventions
   - Provide help text for all commands and options
   - Use consistent naming patterns

### Example Code Style

```python
from typing import Optional, Dict, Any

import click
from rich.console import Console

console = Console()

def fetch_leaderboard_data(
    period: str,
    config: Config
) -> Optional[Dict[str, Any]]:
    """Fetch leaderboard data from the TripleTen API.

    Args:
        period: Time period for data ('all', 'month', 'week')
        config: Configuration object with authentication

    Returns:
        Leaderboard data dictionary or None if failed

    Raises:
        AuthenticationError: If not properly authenticated
        APIError: If API request fails
    """
    # Implementation here
    pass
```

## 🧪 Testing

We use pytest for testing. All contributions should include appropriate tests.

### Test Types

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **CLI Tests**: Test command-line interface

### Writing Tests

```python
import pytest
from click.testing import CliRunner

from tripleten_cli.cli import tripleten

def test_leaderboard_command():
    """Test basic leaderboard command."""
    runner = CliRunner()
    result = runner.invoke(tripleten, ['leaderboard', '--help'])
    assert result.exit_code == 0
    assert 'Display TripleTen leaderboard' in result.output

def test_config_show():
    """Test config show command."""
    runner = CliRunner()
    result = runner.invoke(tripleten, ['config', '--show'])
    assert result.exit_code == 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tripleten_cli

# Run specific test file
pytest tests/test_cli.py

# Run tests in parallel
pytest -n auto
```

## 🔀 Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes**
   ```bash
   pytest
   pre-commit run --all-files
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

### Commit Message Convention

We use [Conventional Commits](https://conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Build/tooling changes

Examples:
```
feat: add watch mode to leaderboard command
fix: handle authentication errors gracefully
docs: update installation instructions
style: format code with black
refactor: extract API client logic
test: add integration tests for config management
chore: update dependencies
```

### PR Template

When submitting a PR, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or properly documented)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and checks
2. **Code Review**: Maintainers review your code
3. **Feedback**: Address any requested changes
4. **Approval**: PR gets approved and merged

## 🐛 Bug Reports

We use GitHub issues to track bugs. Great bug reports include:

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command `tripleten ...`
2. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots or terminal output.

**Environment:**
- OS: [e.g. macOS 12.0, Ubuntu 20.04, Windows 11]
- Python version: [e.g. 3.9.7]
- TripleTen CLI version: [e.g. 0.1.0]

**Additional context**
Any other relevant information.
```

### Before Submitting a Bug Report

1. **Check existing issues** - Your issue might already be reported
2. **Use the latest version** - Update to the latest version first
3. **Isolate the problem** - Create a minimal test case

## 💡 Feature Requests

We welcome feature suggestions! Please provide:

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions you've thought about.

**Additional context**
Any other relevant information, mockups, or examples.
```

### Feature Development Process

1. **Discussion**: Open an issue to discuss the feature
2. **Design**: Agree on the approach and API design
3. **Implementation**: Implement the feature
4. **Review**: Code review and testing
5. **Documentation**: Update docs and examples

## 🤝 Community Guidelines

### Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

### Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Requests**: Code review, implementation discussion

### Recognition

Contributors are recognized in:
- `CHANGELOG.md` for each release
- GitHub contributors page
- Special thanks in release notes

## 🏆 Contributor Recognition

We value all contributions! Contributors are recognized through:

- **GitHub Contributors**: Automatic recognition on the repo
- **Changelog**: Notable contributions mentioned in releases
- **Thanks**: Personal appreciation from maintainers

### Types of Contributions

- 🐛 **Bug fixes** - Help keep the project stable
- 🚀 **Features** - Add new capabilities
- 📖 **Documentation** - Help others understand and use the project
- 🧪 **Testing** - Improve code reliability
- 🎨 **Design** - Improve user experience
- 💡 **Ideas** - Suggest improvements and new directions

## ❓ Questions?

Don't hesitate to ask! You can:

1. **Open a GitHub Discussion** for general questions
2. **Open an Issue** for specific problems
3. **Join our community** channels (if available)

---

Thank you for contributing to TripleTen CLI! 🎉

Together, we're making the TripleTen learning experience better for everyone.
