# TripleTen CLI

A beautiful command-line interface tool for the TripleTen educational platform that provides utilities for students, instructors, and administrators.

[![PyPI version](https://badge.fury.io/py/tripleten-cli.svg)](https://badge.fury.io/py/tripleten-cli)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

- 🏆 **Beautiful Leaderboards**: Rich, colorful tables with user highlighting and rank styling
- 🔐 **Secure Authentication**: Login with your TripleTen credentials
- ⚡ **Real-time Updates**: Watch mode with configurable refresh intervals
- 🎨 **Rich Terminal Output**: Styled tables, progress bars, and visual feedback
- 🛠️ **Flexible Configuration**: Customizable settings and preferences
- 📊 **Multiple Time Periods**: View all-time, monthly, and weekly leaderboards

## 🚀 Installation

### Option 1: Install with pipx (Recommended)

[pipx](https://pypa.github.io/pipx/) installs CLI tools in isolated environments, preventing dependency conflicts:

```bash
# Install pipx (if not already installed)
python -m pip install --user pipx
python -m pipx ensurepath

# Install TripleTen CLI
pipx install tripleten-cli

# Verify installation
tripleten --version
```

### Option 2: Install with pip

```bash
# Install from PyPI
pip install tripleten-cli

# Or install latest development version
pip install git+https://github.com/tripleten/tripleten-cli.git
```

### Option 3: Development Installation

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

### Verify Installation

After installation, you can verify everything is working correctly:

```bash
# Run the installation verification script
python verify_install.py

# Or test manually
tripleten --version
tripleten --help
tripleten config --show
```

The verification script checks:
- ✅ Python version compatibility
- ✅ CLI command availability
- ✅ Required dependencies
- ✅ Configuration directory
- ✅ Basic functionality

## 🔐 Authentication

The CLI uses browser cookies for authentication, making it easy and secure:

### Quick Setup (Recommended)

1. **Login to TripleTen** in your browser at [hub.tripleten.com](https://hub.tripleten.com)
2. **Copy cookies**: Open Developer Tools (F12) → Network → Find leaderboard request → Copy cookies
3. **Run login**:
   ```bash
   tripleten login
   ```
   The CLI will automatically read cookies from your clipboard!

### Alternative Methods

```bash
# Provide cookies directly
tripleten login --cookies "your_cookie_string_here"

# Skip clipboard reading
tripleten login --no-clipboard
```

Your cookies are securely stored in your configuration directory (`~/.config/tripleten-cli/` on Linux/macOS, `%APPDATA%\tripleten-cli\` on Windows).

## 📊 Sample Commands & Rich Table Output

### Basic Leaderboard Display

```bash
# Show default leaderboard (all-time)
tripleten
```

**Output:**
```
🏆 Leaderboard
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃  Rank  ┃ Name                 ┃         XP ┃  Completed ┃   Streak ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│   1    │ Marina Viriyalova    │        114 │          0 │        0 │
│   2    │ Oluwasetemi Ojo      │        104 │          0 │        0 │
│   3    │ Ayomide Onifade      │         64 │          0 │        0 │
│   4    │ Ernest Bonat         │         61 │          0 │        0 │
│   5    │ Ekaterina Terentyeva │         45 │          0 │        0 │
└────────┴──────────────────────┴────────────┴────────────┴──────────┘

Last refreshed: 2025-08-07 05:28:12
```

### Weekly Leaderboard

```bash
tripleten leaderboard --period 7_days
```

### Real-time Watch Mode

```bash
# Watch mode with 30-second refresh
tripleten leaderboard --watch --interval 30

# Short form
tripleten -w --interval 60
```

**Watch Mode Output:**
```
🏆 Leaderboard
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃  Rank  ┃ Name                 ┃         XP ┃  Completed ┃   Streak ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│   1    │ Oluwasetemi Ojo      │         43 │          0 │        0 │
│   2    │ Marina Viriyalova    │         19 │          0 │        0 │
│   3    │ Luiz Araujo          │         10 │          0 │        0 │
│   4    │ Ernest Bonat         │          8 │          0 │        0 │
│   5    │ Kate Mangubat        │          8 │          0 │        0 │
└────────┴──────────────────────┴────────────┴────────────┴──────────┘

Refreshing every 30 seconds. Press Ctrl+C to exit.
Last refreshed: 2025-01-07 03:57:44
```

### 🎨 Rich Table Features

- **🥇 Gold Rank 1**: First place shows in gold styling
- **🥈 Silver Rank 2**: Second place shows in silver styling
- **🥉 Bronze Rank 3**: Third place shows in bronze styling
- **✨ Current User Highlighting**: Your row is highlighted in bold yellow
- **📏 Auto-formatting**: Numbers are right-aligned, ranks centered
- **🔄 Live Updates**: Tables refresh in place without clearing screen

### Configuration Examples

```bash
# Show current settings
tripleten config --show

# Set default refresh interval
tripleten config --set default_interval 45

# Set default time period
tripleten config --set default_period 7_days

# Show config file location
tripleten config --path
```

**Config Output:**
```
Current Configuration:
Location: ~/.config/tripleten-cli/config.toml

┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Setting          ┃ Value                                       ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ default_period   │ all_time                                    │
│ default_interval │ 30                                          │
│ session_cookie   │ ****def456                                  │
│ user_id          │ alice123                                    │
└──────────────────┴─────────────────────────────────────────────┘
```

### Usage

After installation, you can use the `tripleten` command:

```bash
# Display version and help
tripleten --version
tripleten --help

# Default command - show leaderboard
tripleten

# View leaderboard for different periods
tripleten leaderboard --period all_time
tripleten leaderboard --period 30_days
tripleten leaderboard --period 7_days

# Watch mode - continuously refresh leaderboard
tripleten leaderboard --watch --interval 60
tripleten leaderboard -w --interval 30

# Login to save authentication credentials
tripleten login
tripleten login --username user@example.com

# Configuration management
tripleten config --show
tripleten config --set theme dark
tripleten config --set refresh_interval 60
```

## Commands

### `leaderboard` (default)
Display the TripleTen leaderboard with student rankings and scores.

**Options:**
- `--period [all_time|30_days|7_days]`: Time period for leaderboard data (default: all_time)
- `--watch, -w`: Watch mode - continuously refresh leaderboard
- `--interval INTEGER`: Refresh interval in seconds for watch mode (default: 30)

**Examples:**
```bash
tripleten leaderboard --period 7_days
tripleten leaderboard --watch --interval 60
```

### `login`
Authenticate with TripleTen using browser cookies.

**Options:**
- `--cookies TEXT`: Full cookie string from your browser (copy from Developer Tools). If not provided, will try to read from clipboard.
- `--clipboard`: Read cookies from clipboard (default behavior)

**Examples:**
```bash
# Auto-read from clipboard (recommended)
tripleten login

# Provide cookies directly
tripleten login --cookies "your_cookie_string_here"
```

### `config`
Show or edit stored configuration settings.

**Options:**
- `--show`: Display current configuration (default if no other options)
- `--set <key> <value>`: Set configuration options (can be used multiple times)

**Examples:**
```bash
tripleten config --show
tripleten config --set theme dark --set refresh_interval 60
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

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or sharing ideas, your help is appreciated.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Ensure all tests pass and code quality checks succeed
5. Submit a pull request

### Detailed Contribution Guide

For detailed information on:
- 🚀 Development setup and workflow
- 📏 Code standards and style guidelines
- 🧪 Testing requirements and best practices
- 🔀 Pull request process and templates
- 🐛 Bug reporting guidelines
- 💡 Feature request process

Please see our [**Contributing Guide**](CONTRIBUTING.md).

### Types of Contributions Welcome

- 🐛 **Bug Reports**: Help us identify and fix issues
- 🚀 **Feature Requests**: Suggest new capabilities
- 📖 **Documentation**: Improve guides and examples
- 🧪 **Testing**: Add test coverage and edge cases
- 🎨 **UI/UX**: Enhance terminal output and user experience
- 💡 **Ideas**: Share thoughts on project direction

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎥 Demo

### Terminal Recording

We provide a demo script to showcase all CLI features. You can run it directly or use it to create your own terminal recording:

```bash
# Run the interactive demo
python demo_terminal.py

# Record with asciinema (if installed)
asciinema rec tripleten-demo.cast -c "python demo_terminal.py"

# Convert to GIF (requires agg: npm install -g @asciinema/agg)
agg tripleten-demo.cast tripleten-demo.gif
```

The demo showcases:
- 📦 Installation process
- 🏆 Leaderboard display with rich tables
- ⚡ Watch mode with real-time updates
- 🔐 Authentication workflow
- ⚙️ Configuration management
- 🎨 Rich table features and styling

### Alternative Recording Tools

- **[terminalizer](https://terminalizer.com/)**: `npm install -g terminalizer`
- **[ttyd](https://github.com/tsl0922/ttyd)**: Web-based terminal sharing
- **[asciinema](https://asciinema.org/)**: Terminal session recording

## 📚 Documentation

- **[README.md](README.md)**: Main documentation (this file)
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Detailed contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)**: Version history and release notes
- **API Documentation**: Available in source code docstrings

## Support

For support, please contact o.ojo@tripleten-team.com or open an issue in the GitHub repository.
