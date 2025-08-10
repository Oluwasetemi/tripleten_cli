#!/usr/bin/env python3
"""
Terminal Demo Script for TripleTen CLI

This script demonstrates the key features of the TripleTen CLI
for recording a demo GIF or video.

Usage:
  python demo_terminal.py

Requirements:
  - asciinema (for recording): pip install asciinema
  - or use any terminal recording tool like terminalizer

Recording commands:
  # Using asciinema
  asciinema rec tripleten-demo.cast -c "python demo_terminal.py"

  # Convert to GIF (requires agg)
  agg tripleten-demo.cast tripleten-demo.gif
"""

import subprocess
import sys
import time
from typing import List


def run_command(cmd: List[str], delay: float = 2.0, show_command: bool = True) -> None:
    """Run a command and wait."""
    if show_command:
        # Type out the command
        command_str = " ".join(cmd)
        print(f"$ {command_str}")
        time.sleep(1)

    # Run the command
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("Command timed out...")
    except Exception as e:
        print(f"Error running command: {e}")

    time.sleep(delay)


def type_text(text: str, delay: float = 0.05) -> None:
    """Simulate typing text character by character."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def clear_screen() -> None:
    """Clear the terminal screen."""
    subprocess.run(["clear"], check=False)


def demo_intro() -> None:
    """Show demo introduction."""
    clear_screen()
    print("🏆 TripleTen CLI Demo")
    print("=" * 50)
    print()
    type_text("Welcome to the TripleTen CLI demonstration!")
    type_text("This demo showcases the key features of our beautiful CLI tool.")
    print()
    time.sleep(2)


def demo_installation() -> None:
    """Demo installation commands."""
    print("📦 Installation with pipx (recommended):")
    print()
    type_text("# Install pipx if you don't have it")
    type_text("python -m pip install --user pipx")
    print()
    type_text("# Install TripleTen CLI")
    type_text("pipx install tripleten-cli")
    print()
    time.sleep(2)


def demo_version() -> None:
    """Demo version check."""
    print("✅ Verify installation:")
    print()
    run_command(["tripleten", "--version"])


def demo_help() -> None:
    """Demo help command."""
    print("❓ Get help:")
    print()
    run_command(["tripleten", "--help"])


def demo_leaderboard() -> None:
    """Demo leaderboard display."""
    print("🏆 Display leaderboard:")
    print()
    run_command(["tripleten"], delay=3.0)


def demo_different_periods() -> None:
    """Demo different time periods."""
    print("📅 Different time periods:")
    print()

    print("Weekly leaderboard:")
    run_command(["tripleten", "leaderboard", "--period", "7_days"], delay=3.0)

    print("Monthly leaderboard:")
    run_command(["tripleten", "leaderboard", "--period", "30_days"], delay=3.0)


def demo_config() -> None:
    """Demo configuration commands."""
    print("⚙️ Configuration management:")
    print()

    print("Show current configuration:")
    run_command(["tripleten", "config", "--show"], delay=3.0)

    print("Set default refresh interval:")
    run_command(["tripleten", "config", "--set", "default_interval", "45"], delay=2.0)


def demo_login() -> None:
    """Demo login process (simulated)."""
    print("🔐 Authentication:")
    print()
    type_text("# Login to TripleTen (credentials will be prompted securely)")
    type_text("tripleten login --username your.email@example.com")
    print()
    print("Username: your.email@example.com")
    print("Password: ********")
    print("✅ Successfully logged in!")
    print("Welcome back, your.email@example.com!")
    time.sleep(2)


def demo_watch_mode_intro() -> None:
    """Demo watch mode introduction."""
    print("⚡ Watch mode (real-time updates):")
    print()
    type_text("# Start watch mode with 5-second intervals for demo")
    type_text("tripleten leaderboard --watch --interval 5")
    print()
    print("🏆 Leaderboard")
    print("┏━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━")
    print("┃  Rank  ┃ User            ┃         XP ┃  Completed ┃   Streak")
    print("┡━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━")
    print("│   1    │ Alice           │      15000 │         45 │       12")
    print("│   2    │ Bob             │      12500 │         38 │        8")
    print("│   3    │ Charlie         │      11000 │         35 │       15")
    print("│   4    │ Diana           │       9500 │         30 │        5")
    print("│   5    │ Eve             │       8000 │         25 │        3")
    print("└────────┴─────────────────┴────────────┴────────────┴────────")
    print()
    print("Refreshing every 5 seconds. Press Ctrl+C to exit.")
    print("Last refreshed: 2025-01-07 15:30:15")

    # Simulate a few refreshes
    for i in range(3):
        time.sleep(2)
        print(f"Last refreshed: 2025-01-07 15:30:{20 + i*5}")

    print()
    print("^C")
    print("Watch mode stopped.")
    time.sleep(1)


def demo_rich_features() -> None:
    """Demo rich table features."""
    print("🎨 Rich Table Features:")
    print()
    type_text("✨ Beautiful styling with rank colors:")
    type_text("  🥇 Gold for 1st place")
    type_text("  🥈 Silver for 2nd place")
    type_text("  🥉 Bronze for 3rd place")
    print()
    type_text("✨ Current user highlighting in bold yellow")
    type_text("✨ Auto-formatted columns and alignment")
    type_text("✨ Graceful fallback for different terminals")
    print()
    time.sleep(2)


def demo_outro() -> None:
    """Show demo conclusion."""
    print("🎉 Demo Complete!")
    print("=" * 50)
    print()
    type_text("Thank you for watching the TripleTen CLI demo!")
    print()
    type_text("Key features demonstrated:")
    type_text("  🏆 Beautiful leaderboard tables")
    type_text("  ⚡ Real-time watch mode")
    type_text("  🔐 Secure authentication")
    type_text("  ⚙️ Flexible configuration")
    type_text("  📅 Multiple time periods")
    type_text("  🎨 Rich terminal output")
    print()
    type_text("Get started: pipx install tripleten-cli")
    type_text("Documentation: https://github.com/Oluwasetemi/tripleten-cli")
    print()
    time.sleep(2)


def main() -> None:
    """Run the complete demo."""
    try:
        demo_intro()
        demo_installation()
        demo_version()
        demo_help()
        demo_leaderboard()
        demo_different_periods()
        demo_login()
        demo_config()
        demo_watch_mode_intro()
        demo_rich_features()
        demo_outro()

    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Thanks for watching!")
        sys.exit(0)


if __name__ == "__main__":
    print("🎬 Starting TripleTen CLI Demo...")
    print("Press Ctrl+C to stop at any time.")
    time.sleep(2)
    main()
