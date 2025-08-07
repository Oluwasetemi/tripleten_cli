#!/usr/bin/env python3
"""Example usage of the TripleTen HTTP client."""

from pathlib import Path

from client import create_client


def main():
    """Demonstrate client usage."""
    # Set up configuration directory (typically ~/.tripleten)
    config_dir = Path.home() / ".tripleten"

    # Create client instance
    client = create_client(config_dir)

    # Check authentication status
    if client.is_authenticated():
        print("✓ Client is authenticated")

        # Get user info
        user_info = client.get_user_info()
        if user_info:
            print(f"User: {user_info.get('name', 'Unknown')}")
    else:
        print("✗ Client is not authenticated")
        print("Run 'tripleten login' first")
        return

    # Example: Fetch leaderboard data
    try:
        print("\nFetching leaderboard data...")

        # Fetch all-time leaderboard
        leaderboard = client.fetch_leaderboard("all")
        print(f"All-time leaderboard: {len(leaderboard.get('users', []))} users")

        # Fetch monthly leaderboard
        monthly = client.fetch_leaderboard("month")
        print(f"Monthly leaderboard: {len(monthly.get('users', []))} users")

    except SystemExit:
        print("Failed to fetch leaderboard data")


def demo_login():
    """Demonstrate login functionality."""
    # config_dir = Path.home() / ".tripleten"
    # client = create_client(config_dir)

    # Example cookie string (this would normally come from the login command)
    # cookie_string = "session_id=abc123; csrf_token=def456"
    # client.login(cookie_string)
    # print("Logged in successfully")


if __name__ == "__main__":
    main()
