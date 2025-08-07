"""Main CLI entry point for TripleTen CLI."""

import click
from rich.console import Console

from . import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="tripleten-cli")
def cli() -> None:
    """TripleTen CLI - A command-line interface for the TripleTen educational platform."""
    pass


@cli.command()
def hello() -> None:
    """Say hello from TripleTen CLI."""
    console.print("Hello from TripleTen CLI! 🎓", style="bold green")


if __name__ == "__main__":
    cli()
