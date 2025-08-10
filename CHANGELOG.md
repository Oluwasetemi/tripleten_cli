# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features that have been added but not yet released

### Changed
- Changes in existing functionality

### Deprecated
- Features that are deprecated and will be removed in future versions

### Removed
- Features that have been removed in this release

### Fixed
- Bug fixes

### Security
- Security improvements

## [0.2.0] - TBD

### Added
- Enhanced error handling and user feedback
- Configuration file validation
- Support for custom API endpoints
- Improved watch mode with change detection
- Rich progress bars for long-running operations

### Changed
- Improved table rendering performance
- Updated dependencies to latest versions
- Better error messages and help text

### Fixed
- Authentication token refresh issues
- Table rendering bugs on different terminal sizes
- Watch mode memory usage optimization

## [0.1.0] - 2025-08-07

### Added
- ✨ **Initial release of TripleTen CLI**
- 🏆 **Rich leaderboard display** with colorful tables and rank styling
- 🔐 **Authentication system** with secure credential storage
- ⚡ **Real-time watch mode** with configurable refresh intervals
- 📊 **Multiple time periods** (all-time, monthly, weekly)
- 🛠️ **Configuration management** with persistent settings
- 🎨 **Beautiful terminal output** using Rich library
- 📝 **Comprehensive CLI interface** built with Click

#### Commands
- `tripleten leaderboard` - Display leaderboard with various options
- `tripleten login` - Authenticate with TripleTen credentials
- `tripleten config` - Manage configuration settings

#### Features
- **Rich Table Rendering**:
  - Gold/silver/bronze styling for top 3 ranks
  - Current user highlighting in bold yellow
  - Auto-formatted columns with proper alignment
  - Graceful fallback for terminals without rich support

- **Authentication**:
  - Secure credential storage in user config directory
  - Session cookie management
  - Login status validation

- **Configuration**:
  - Persistent settings storage
  - Default period and interval customization
  - Configuration file location display
  - Settings validation and error handling

- **Watch Mode**:
  - Real-time leaderboard updates
  - Configurable refresh intervals (default: 30 seconds)
  - Change detection to avoid unnecessary refreshes
  - Graceful keyboard interrupt handling

#### Technical Details
- **Dependencies**: Click, Rich, Requests, PlatformDirs, TOML libraries
- **Python Support**: 3.9+
- **Configuration**: TOML-based configuration files
- **Error Handling**: Comprehensive error messages and fallbacks
- **Code Quality**: Black formatting, isort, flake8 linting, mypy typing
- **Testing**: pytest with comprehensive test coverage

#### Installation Methods
- PyPI package installation
- Development installation from source
- pipx support for isolated installation

---

## 📝 Changelog Guidelines

This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format:

### Types of Changes
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for security improvements

### Version Numbers
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Entry Format
```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description with emoji
- Another new feature

### Changed
- Change description
- Another change

### Fixed
- Bug fix description
- Another bug fix
```

### Emoji Guide
- ✨ New features
- 🐛 Bug fixes
- 🔐 Security improvements
- ⚡ Performance improvements
- 📝 Documentation
- 🎨 UI/UX improvements
- 🔧 Configuration/settings
- 📊 Data/analytics features
- 🛠️ Developer tools
- 🚀 Deployment/release
- ⬆️ Dependency updates
- ♻️ Refactoring
- 🔥 Removed features
- 🚨 Breaking changes

---

## 🔗 Links

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [GitHub Releases](https://github.com/tripleten/tripleten-cli/releases)
- [Contributing Guide](CONTRIBUTING.md)
