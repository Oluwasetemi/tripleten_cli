"""TripleTen CLI interface with Click."""

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import ConfigError, get_config

# Import client and render modules from the package
try:
    from .client import create_client  # type: ignore[attr-defined]
    from .render import render_leaderboard  # type: ignore[attr-defined]
except ImportError:
    # Fallback if modules are not available
    create_client = None  # type: ignore[assignment]
    render_leaderboard = None  # type: ignore[assignment]

console = Console()


def map_period_to_client(period: str) -> str:
    """Map CLI period format to client expected format.

    Args:
        period: Period in CLI format (all_time, 30_days, 7_days)

    Returns:
        Period in client format (all, month, week)
    """
    period_mapping = {"all_time": "all", "30_days": "month", "7_days": "week"}
    return period_mapping.get(period, "all")


def compute_data_hash(data: Dict[str, Any]) -> str:
    """Compute hash of data for change detection.

    Args:
        data: Dictionary containing leaderboard data

    Returns:
        SHA256 hash of the JSON data
    """
    # Convert to JSON string with sorted keys for consistent hashing
    json_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_string.encode()).hexdigest()


def get_current_timestamp() -> str:
    """Get current timestamp formatted for display.

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="tripleten")
@click.pass_context
def tripleten(ctx: click.Context) -> None:
    """TripleTen CLI - A command-line interface for TripleTen educational platform."""
    if ctx.invoked_subcommand is None:
        # Default to leaderboard command when no subcommand is provided
        ctx.invoke(leaderboard)


@tripleten.command()
@click.option(
    "--period",
    type=click.Choice(["all_time", "30_days", "7_days"]),
    default=None,
    help="Time period for leaderboard data.",
)
@click.option(
    "--watch", "-w", is_flag=True, help="Watch mode - continuously refresh leaderboard."
)
@click.option(
    "--interval",
    type=int,
    default=None,
    help="Refresh interval in seconds (for watch mode).",
)
def leaderboard(period: Optional[str], watch: bool, interval: Optional[int]) -> None:
    """Display TripleTen leaderboard (default command)."""
    # Get configuration and apply defaults
    try:
        config = get_config()
        if period is None:
            period = config.default_period
        if interval is None:
            interval = config.default_interval
    except ConfigError as e:
        console.print(f"[yellow]Warning: Configuration error: {e}[/yellow]")
        # Fallback to hardcoded defaults
        if period is None:
            period = "all_time"
        if interval is None:
            interval = 30

    # Initialize client if available
    client = None
    if create_client is not None:
        try:
            config_dir = (
                config._config_dir
                if hasattr(config, "_config_dir")
                else Path.home() / ".config" / "tripleten-cli"
            )
            client = create_client(config_dir)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not initialize client: {e}[/yellow]")

    # Variables for change detection
    previous_hash = None
    last_refresh_time = None

    def fetch_leaderboard_data() -> Optional[Dict[str, Any]]:
        """Fetch leaderboard data from API or use fallback."""
        nonlocal last_refresh_time
        last_refresh_time = get_current_timestamp()

        if client:
            try:
                # Map period to client format and fetch data
                client_period = map_period_to_client(period)
                data = client.fetch_leaderboard(client_period)
                return data
            except Exception as e:
                console.print(f"[yellow]Warning: API fetch failed: {e}[/yellow]")
                console.print("[yellow]Falling back to sample data...[/yellow]")

        # Fallback to sample data - this code is reachable when client fails
        return {
            "leaderboard": [
                {
                    "rank": 1,
                    "user": "Alice Johnson",
                    "user_id": "alice123",
                    "xp": 2450,
                    "completed": 12,
                    "streak": 8,
                },
                {
                    "rank": 2,
                    "user": "Bob Smith",
                    "user_id": "bob456",
                    "xp": 2320,
                    "completed": 11,
                    "streak": 5,
                },
                {
                    "rank": 3,
                    "user": "Carol Davis",
                    "user_id": "carol789",
                    "xp": 2180,
                    "completed": 10,
                    "streak": 12,
                },
                {
                    "rank": 4,
                    "user": "David Wilson",
                    "user_id": "david012",
                    "xp": 2050,
                    "completed": 10,
                    "streak": 3,
                },
                {
                    "rank": 5,
                    "user": "Eva Brown",
                    "user_id": "eva345",
                    "xp": 1890,
                    "completed": 9,
                    "streak": 15,
                },
            ]
        }

    def display_leaderboard_data(
        data: Dict[str, Any], show_footer: bool = True
    ) -> None:
        """Display leaderboard data using render module or fallback."""
        console.clear()

        # Get current user ID from config for highlighting
        current_user_id = config.user_id if hasattr(config, "user_id") else ""

        if render_leaderboard is not None and "leaderboard" in data:
            # Use render module if available
            try:
                render_leaderboard(data["leaderboard"], current_user_id or "")
            except Exception as e:
                console.print(f"[yellow]Warning: Render failed: {e}[/yellow]")
                _display_fallback_table(data)
        else:
            # Fallback display
            _display_fallback_table(data)

        # Show footer with refresh info
        if show_footer:
            if watch:
                console.print(
                    f"\n[dim]Refreshing every {interval} seconds. Press Ctrl+C to exit.[/dim]"
                )
            if last_refresh_time:
                console.print(f"[dim]Last refreshed: {last_refresh_time}[/dim]")

    def _display_fallback_table(data: Dict[str, Any]) -> None:
        """Fallback table display when render module is not available."""
        # Create a fallback leaderboard table
        table = Table(
            title=f"TripleTen Leaderboard - {period.replace('_', ' ').title()}"
        )
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Name", style="magenta", width=20)
        table.add_column("XP", style="green", width=10)
        table.add_column("Completed", style="yellow", width=10)
        table.add_column("Streak", style="blue", width=10)

        # Extract leaderboard data
        leaderboard_data = data.get("leaderboard", [])

        for entry in leaderboard_data:
            rank = str(entry.get("rank", "N/A"))
            user = entry.get("user", "Unknown")
            xp = str(entry.get("xp", 0))
            completed = str(entry.get("completed", 0))
            streak = str(entry.get("streak", 0))

            table.add_row(rank, user, xp, completed, streak)

        console.print(table)

    def has_data_changed(data: Dict[str, Any]) -> bool:
        """Check if data has changed since last fetch."""
        nonlocal previous_hash
        current_hash = compute_data_hash(data)

        if previous_hash is None or current_hash != previous_hash:
            previous_hash = current_hash
            return True
        return False

    try:
        # Initial display
        data = fetch_leaderboard_data()
        if data:
            has_data_changed(data)  # Initialize hash
            display_leaderboard_data(data)
        else:
            console.print("[red]Error: Could not fetch leaderboard data[/red]")
            return

        if watch:
            while True:
                time.sleep(interval)

                # Fetch new data
                new_data = fetch_leaderboard_data()
                if new_data:
                    # Only re-render if data changed
                    if has_data_changed(new_data):
                        display_leaderboard_data(new_data)
                    # Note: We don't re-display if data hasn't changed
                    # but the timestamp will still be updated for the next display

    except KeyboardInterrupt:
        if watch:
            console.print("\n[yellow]Watch mode stopped.[/yellow]")
        else:
            console.print("\n[yellow]Leaderboard display interrupted.[/yellow]")


@tripleten.command()
@click.option(
    "--cookies",
    default="",
    help="Full cookie string from your browser (copy from Developer Tools). If not provided, will try to read from clipboard.",
)
@click.option(
    "--clipboard",
    is_flag=True,
    default=True,
    help="Read cookies from clipboard (default behavior)",
)
def login(cookies: str, clipboard: bool) -> None:
    """Login to TripleTen using browser cookies."""
    try:
        config = get_config()
    except ConfigError as e:
        console.print(f"[red]Error loading configuration: {e}[/red]")
        return

    # Try to get cookies from clipboard if not provided
    if not cookies and clipboard:
        console.print("[yellow]Attempting to read cookies from clipboard...[/yellow]")
        try:
            import pyperclip

            clipboard_content = pyperclip.paste()
            if clipboard_content and ("=" in clipboard_content):
                cookies = clipboard_content.strip()
                console.print(
                    "[green]✅ Cookies read from clipboard successfully![/green]"
                )
            else:
                console.print(
                    "[yellow]No valid cookie data found in clipboard.[/yellow]"
                )
        except ImportError:
            console.print(
                "[yellow]pyperclip not available. Please install with: pip install pyperclip[/yellow]"
            )
        except Exception as e:
            console.print(f"[yellow]Could not read from clipboard: {e}[/yellow]")

    # If still no cookies, prompt the user
    if not cookies:
        cookies = click.prompt("Cookie string from browser", type=str, default="")

    if not cookies:
        console.print(
            "[yellow]No cookies provided. CLI will use sample data only.[/yellow]"
        )
        return

    console.print("[yellow]Setting up authentication with browser cookies...[/yellow]")

    try:
        # Initialize client if available
        if create_client is not None:  # type: ignore[truthy-function]
            config_dir = (
                config._config_dir
                if hasattr(config, "_config_dir")
                else Path.home() / ".config" / "tripleten-cli"
            )
            client = create_client(config_dir)

            # Set the cookies
            client.login(cookies)

            # Test the authentication by trying to fetch user info
            console.print("[yellow]Testing authentication...[/yellow]")

            # Try to make a test request to verify cookies work
            try:
                # This will try to fetch leaderboard data to test auth
                test_data = client.fetch_leaderboard("all")

                console.print("✅ [green]Successfully authenticated![/green]")
                console.print(
                    f"[dim]Cookies saved to: {config_dir / 'cookies.json'}[/dim]"
                )

                # Try to extract user info if possible
                if test_data and isinstance(test_data, dict):
                    console.print(
                        "[dim]Authentication test successful - API is accessible[/dim]"
                    )

            except Exception as e:
                console.print(
                    f"[yellow]Warning: Could not verify authentication: {e}[/yellow]"
                )
                console.print(
                    "[yellow]Cookies have been saved, but may need to be refreshed if requests fail[/yellow]"
                )

        else:
            console.print("[red]Error: Client module not available[/red]")
            return

    except Exception as e:
        console.print(f"[red]Error setting up authentication: {e}[/red]")
        return


@tripleten.command()
@click.option("--show", is_flag=True, help="Show current configuration.")
@click.option(
    "--set",
    "set_option",
    type=(str, str),
    multiple=True,
    help="Set configuration option (key value pairs).",
)
@click.option("--path", is_flag=True, help="Show configuration file path.")
def config(show: bool, set_option: tuple, path: bool) -> None:
    """Show or edit stored settings."""
    try:
        config_manager = get_config()
    except ConfigError as e:
        console.print(f"[red]Error loading configuration: {e}[/red]")
        return

    if path:
        console.print("[bold]Configuration file path:[/bold]")
        console.print(f"[cyan]{config_manager.config_path}[/cyan]")
        return

    if show or (not show and not set_option):
        # Show current configuration
        console.print("[bold]Current Configuration:[/bold]")
        console.print(f"[dim]Location: {config_manager.config_path}[/dim]\n")

        config_data = config_manager.get_all()

        # Mask sensitive data
        display_data = config_data.copy()
        if "session_cookie" in display_data and display_data["session_cookie"]:
            display_data["session_cookie"] = (
                "****" + display_data["session_cookie"][-8:]
            )

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")

        for key, value in display_data.items():
            # Show None values as "(not set)"
            display_value = "(not set)" if value is None else str(value)
            table.add_row(key, display_value)

        console.print(table)

    if set_option:
        # Set configuration options
        console.print("[bold]Setting configuration:[/bold]")

        updated = False
        for key, value in set_option:
            try:
                # Validate and set configuration options
                if key == "default_period":
                    config_manager.default_period = value
                elif key == "default_interval":
                    try:
                        config_manager.default_interval = int(value)
                    except ValueError:
                        console.print(f"[red]Error: {key} must be an integer[/red]")
                        continue
                elif key in ["session_cookie", "user_id"]:
                    # Allow setting these directly for advanced users
                    if value.lower() in ["none", "null", ""]:
                        config_manager.set(key, None)
                    else:
                        config_manager.set(key, value)
                else:
                    # Generic setting for other configuration options
                    config_manager.set(key, value)

                updated = True
                console.print(f"✅ Set [cyan]{key}[/cyan] = [green]{value}[/green]")

            except ValueError as e:
                console.print(f"[red]Error setting {key}: {e}[/red]")
                continue

        if updated:
            try:
                config_manager.save()
                console.print(
                    f"\n[green]Configuration saved to {config_manager.config_path}[/green]"
                )
            except ConfigError as e:
                console.print(f"[red]Error saving configuration: {e}[/red]")


if __name__ == "__main__":
    tripleten()
