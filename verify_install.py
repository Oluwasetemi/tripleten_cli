#!/usr/bin/env python3
"""
Installation Verification Script for TripleTen CLI

This script verifies that TripleTen CLI is properly installed and configured.
It checks dependencies, installation methods, and basic functionality.

Usage:
  python verify_install.py
"""

import importlib
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple


def check_python_version() -> Tuple[bool, str]:
    """Check Python version compatibility."""
    required_version = (3, 9)
    current_version = sys.version_info[:2]

    if current_version >= required_version:
        return True, f"✅ Python {current_version[0]}.{current_version[1]} (compatible)"
    else:
        return (
            False,
            f"❌ Python {current_version[0]}.{current_version[1]} (requires 3.9+)",
        )


def check_package_installed(package: str) -> Tuple[bool, str]:
    """Check if a package is installed."""
    try:
        importlib.import_module(package)
        return True, f"✅ {package} installed"
    except ImportError:
        return False, f"❌ {package} not installed"


def check_cli_command() -> Tuple[bool, str]:
    """Check if tripleten CLI command is available."""
    try:
        result = subprocess.run(
            ["tripleten", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, f"✅ TripleTen CLI available: {version}"
        else:
            return False, f"❌ TripleTen CLI command failed: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, "❌ TripleTen CLI command timed out"
    except FileNotFoundError:
        return False, "❌ TripleTen CLI command not found in PATH"
    except Exception as e:
        return False, f"❌ Error running TripleTen CLI: {e}"


def check_config_directory() -> Tuple[bool, str]:
    """Check if configuration directory exists."""
    config_paths = [
        Path.home() / ".config" / "tripleten-cli",  # Linux/macOS
        Path.home() / "AppData" / "Roaming" / "tripleten-cli",  # Windows
        Path.home() / "Library" / "Application Support" / "tripleten-cli",  # macOS
    ]

    for config_path in config_paths:
        if config_path.exists():
            return True, f"✅ Config directory: {config_path}"

    return False, "⚠️  No config directory found (will be created on first use)"


def check_dependencies() -> Dict[str, Tuple[bool, str]]:
    """Check all required dependencies."""
    deps = {
        "click": "click",
        "rich": "rich",
        "requests": "requests",
        "platformdirs": "platformdirs",
    }

    results = {}
    for name, package in deps.items():
        results[name] = check_package_installed(package)

    return results


def check_optional_dependencies() -> Dict[str, Tuple[bool, str]]:
    """Check optional dependencies."""
    optional_deps = {
        "tabulate": "tabulate",
        "asciinema": "asciinema",
    }

    results = {}
    for name, package in optional_deps.items():
        results[name] = check_package_installed(package)

    return results


def run_basic_functionality_test() -> Tuple[bool, str]:
    """Test basic CLI functionality."""
    try:
        # Test help command
        result = subprocess.run(
            ["tripleten", "--help"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0 and "TripleTen CLI" in result.stdout:
            return True, "✅ Basic functionality test passed"
        else:
            return False, f"❌ Help command failed: {result.stderr.strip()}"

    except Exception as e:
        return False, f"❌ Functionality test error: {e}"


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{title}")
    print("=" * len(title))


def print_result(success: bool, message: str) -> None:
    """Print a test result."""
    print(f"  {message}")


def print_installation_help() -> None:
    """Print installation help."""
    print("\n🚀 Installation Options:")
    print("=" * 25)
    print("\n1. Install with pipx (recommended):")
    print("   pip install --user pipx")
    print("   pipx install tripleten-cli")
    print("\n2. Install with pip:")
    print("   pip install tripleten-cli")
    print("\n3. Development installation:")
    print("   git clone https://github.com/tripleten/tripleten-cli.git")
    print("   cd tripleten-cli")
    print("   pip install -e .")


def main() -> None:
    """Run all verification checks."""
    print("🏆 TripleTen CLI Installation Verification")
    print("=" * 50)

    all_passed = True

    # Check Python version
    print_section("Python Version")
    success, message = check_python_version()
    print_result(success, message)
    if not success:
        all_passed = False

    # Check if CLI is installed
    print_section("CLI Installation")
    success, message = check_cli_command()
    print_result(success, message)
    if not success:
        all_passed = False
        print_installation_help()
        return

    # Check dependencies
    print_section("Required Dependencies")
    dep_results = check_dependencies()
    for name, (success, message) in dep_results.items():
        print_result(success, message)
        if not success:
            all_passed = False

    # Check optional dependencies
    print_section("Optional Dependencies")
    opt_results = check_optional_dependencies()
    for name, (success, message) in opt_results.items():
        print_result(success, message)

    # Check configuration
    print_section("Configuration")
    success, message = check_config_directory()
    print_result(success, message)

    # Test basic functionality
    print_section("Functionality Test")
    success, message = run_basic_functionality_test()
    print_result(success, message)
    if not success:
        all_passed = False

    # Summary
    print_section("Summary")
    if all_passed:
        print("  ✅ All checks passed! TripleTen CLI is ready to use.")
        print("\n🎯 Next Steps:")
        print("  1. Login: tripleten login")
        print("  2. View leaderboard: tripleten")
        print("  3. Check config: tripleten config --show")
        print("  4. Get help: tripleten --help")
    else:
        print("  ⚠️  Some checks failed. Please address the issues above.")
        print("\n📚 Documentation:")
        print("  - README: https://github.com/tripleten/tripleten-cli#readme")
        print("  - Issues: https://github.com/tripleten/tripleten-cli/issues")

    print("\n🎉 Happy learning with TripleTen CLI!")


if __name__ == "__main__":
    main()
