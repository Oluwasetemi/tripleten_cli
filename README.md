# TripleTen CLI

A command-line interface tool for the TripleTen educational platform that provides utilities for students, instructors, and administrators.

## Purpose

The TripleTen CLI is designed to streamline common tasks in the TripleTen learning environment, including:
- Project management and scaffolding
- Assignment submission and tracking
- Code quality checks and formatting
- Learning progress monitoring
- Integration with TripleTen services

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tripleten/tripleten-cli.git
   cd tripleten-cli
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Usage

After installation, you can use the `tripleten` command:

```bash
# Display version and help
tripleten --version
tripleten --help

# Example command
tripleten hello
```

## Development

### Setting up the development environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Code Quality Tools

This project uses several tools to maintain code quality:

- **Black**: Code formatter
- **isort**: Import statement organizer
- **flake8**: Linter for style guide enforcement
- **mypy**: Static type checker
- **pre-commit**: Git hook framework

### Running Tests

```bash
pytest
```

### Running Code Quality Checks

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass and code quality checks succeed
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact support@tripleten.com or open an issue in the GitHub repository.
