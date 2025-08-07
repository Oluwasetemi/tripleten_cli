"""Tests for the main CLI module."""

from click.testing import CliRunner

from tripleten_cli.main import cli


def test_cli_version() -> None:
    """Test that CLI version command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_help() -> None:
    """Test that CLI help command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "TripleTen CLI" in result.output


def test_hello_command() -> None:
    """Test the hello command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["hello"])
    assert result.exit_code == 0
    assert "Hello from TripleTen CLI!" in result.output
