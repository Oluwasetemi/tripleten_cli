"""
Render leaderboard data in a rich table format.

This module provides functionality to display leaderboard data with styling,
including highlighting the current user and colorizing top 3 ranks.
"""

import json
from typing import Any, Dict, List, Optional

# Graceful import fallback
try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Create a dummy Text class for type hints when rich is not available

    class DummyText:
        def __init__(self, text: str, style: Optional[str] = None) -> None:
            self.text = text
            self.style = style

    # Use DummyText as Text for type compatibility
    Text = DummyText  # type: ignore


try:
    from tabulate import tabulate

    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


def render_leaderboard(
    leaderboard_data: List[Dict[str, Any]], current_user_id: str
) -> None:
    """
    Render leaderboard data in a formatted table.

    Args:
        leaderboard_data: List of user dictionaries containing rank, user, xp, completed, streak
        current_user_id: ID of the current user to highlight
    """
    if not leaderboard_data:
        print("No leaderboard data available.")
        return

    if RICH_AVAILABLE:
        _render_with_rich(leaderboard_data, current_user_id)
    elif TABULATE_AVAILABLE:
        _render_with_tabulate(leaderboard_data, current_user_id)
    else:
        _render_basic(leaderboard_data, current_user_id)


def _render_with_rich(
    leaderboard_data: List[Dict[str, Any]], current_user_id: str
) -> None:
    """Render using rich library with styling."""
    console = Console()

    # Create table with styling
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="cyan", width=6, justify="center")
    table.add_column("Name", style="green", min_width=20)
    table.add_column("XP", style="yellow", width=10, justify="right")
    table.add_column("Completed", style="blue", width=10, justify="right")
    table.add_column("Streak", style="red", width=8, justify="right")

    for entry in leaderboard_data:
        rank = entry.get("rank", "N/A")
        user = entry.get("user", "Unknown")
        xp = entry.get("xp", 0)
        completed = entry.get("completed", 0)
        streak = entry.get("streak", 0)
        user_id = entry.get("user_id", "")

        # Apply rank-based styling
        rank_text = _get_rank_styled_text(rank)

        # Check if this is the current user
        is_current_user = user_id == current_user_id

        if is_current_user:
            # Highlight current user row in bold yellow
            table.add_row(
                rank_text,
                Text(str(user), style="bold yellow"),
                Text(str(xp), style="bold yellow"),
                Text(str(completed), style="bold yellow"),
                Text(str(streak), style="bold yellow"),
            )
        else:
            # Regular row
            table.add_row(rank_text, str(user), str(xp), str(completed), str(streak))

    console.print("\n🏆 Leaderboard")
    console.print(table)
    console.print()


def _get_rank_styled_text(rank: Any) -> Text:
    """Get styled text for rank based on position."""
    rank_str = str(rank)

    if rank == 1:
        return Text(rank_str, style="bold gold1")  # Gold for 1st
    elif rank == 2:
        return Text(rank_str, style="bold bright_white")  # Silver for 2nd
    elif rank == 3:
        return Text(rank_str, style="bold color(208)")  # Bronze/Orange for 3rd
    else:
        return Text(rank_str, style="cyan")  # Default cyan


def _render_with_tabulate(
    leaderboard_data: List[Dict[str, Any]], current_user_id: str
) -> None:
    """Render using tabulate library (fallback)."""
    headers = ["Rank", "User", "XP", "Completed", "Streak"]
    table_data = []

    print("\n🏆 Leaderboard")
    print("=" * 60)

    for entry in leaderboard_data:
        rank = entry.get("rank", "N/A")
        user = entry.get("user", "Unknown")
        xp = entry.get("xp", 0)
        completed = entry.get("completed", 0)
        streak = entry.get("streak", 0)
        user_id = entry.get("user_id", "")

        # Add rank indicators for top 3
        if rank == 1:
            rank_display = f"🥇 {rank}"
        elif rank == 2:
            rank_display = f"🥈 {rank}"
        elif rank == 3:
            rank_display = f"🥉 {rank}"
        else:
            rank_display = str(rank)

        # Mark current user
        if user_id == current_user_id:
            user_display = f"→ {user} ←"  # Arrow indicators for current user
        else:
            user_display = user

        table_data.append([rank_display, user_display, xp, completed, streak])

    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


def _render_basic(leaderboard_data: List[Dict[str, Any]], current_user_id: str) -> None:
    """Basic fallback rendering without external libraries."""
    print("\n🏆 Leaderboard")
    print("=" * 70)
    print(f"{'Rank':<6} {'User':<20} {'XP':<10} {'Completed':<10} {'Streak':<8}")
    print("-" * 70)

    for entry in leaderboard_data:
        if entry is None:
            continue  # Skip None entries

        rank = entry.get("rank", "N/A")
        user = entry.get("user", "Unknown")
        xp = entry.get("xp", 0)
        completed = entry.get("completed", 0)
        streak = entry.get("streak", 0)
        user_id = entry.get("user_id", "")

        # Handle None values
        rank = "N/A" if rank is None else rank
        user = "Unknown" if user is None else user
        xp = 0 if xp is None else xp
        completed = 0 if completed is None else completed
        streak = 0 if streak is None else streak

        # Add rank indicators for top 3
        if rank == 1:
            rank_display = f"🥇{rank}"
        elif rank == 2:
            rank_display = f"🥈{rank}"
        elif rank == 3:
            rank_display = f"🥉{rank}"
        else:
            rank_display = str(rank)

        # Mark current user
        if user_id == current_user_id:
            user_display = f"→ {user} ←"
        else:
            user_display = user

        print(
            f"{rank_display:<6} {user_display:<20} {xp:<10} {completed:<10} {streak:<8}"
        )

    print()


def render_from_json_file(json_file_path: str, current_user_id: str) -> None:
    """
    Load leaderboard data from JSON file and render it.

    Args:
        json_file_path: Path to the JSON file containing leaderboard data
        current_user_id: ID of the current user to highlight
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle different JSON structures
        if isinstance(data, list):
            leaderboard_data = data
        elif isinstance(data, dict) and "leaderboard" in data:
            leaderboard_data = data["leaderboard"]
        elif isinstance(data, dict) and "users" in data:
            leaderboard_data = data["users"]
        else:
            leaderboard_data = [data] if isinstance(data, dict) else []

        render_leaderboard(leaderboard_data, current_user_id)

    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{json_file_path}': {e}")
    except Exception as e:
        print(f"Error loading leaderboard data: {e}")


def render_from_json_string(json_string: str, current_user_id: str) -> None:
    """
    Parse leaderboard data from JSON string and render it.

    Args:
        json_string: JSON string containing leaderboard data
        current_user_id: ID of the current user to highlight
    """
    try:
        data = json.loads(json_string)

        # Handle different JSON structures
        if isinstance(data, list):
            leaderboard_data = data
        elif isinstance(data, dict) and "leaderboard" in data:
            leaderboard_data = data["leaderboard"]
        elif isinstance(data, dict) and "users" in data:
            leaderboard_data = data["users"]
        else:
            leaderboard_data = [data] if isinstance(data, dict) else []

        render_leaderboard(leaderboard_data, current_user_id)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format: {e}")
    except Exception as e:
        print(f"Error parsing leaderboard data: {e}")


if __name__ == "__main__":
    # Example usage and testing
    sample_data = [
        {
            "rank": 1,
            "user": "Alice",
            "user_id": "alice123",
            "xp": 15000,
            "completed": 45,
            "streak": 12,
        },
        {
            "rank": 2,
            "user": "Bob",
            "user_id": "bob456",
            "xp": 12500,
            "completed": 38,
            "streak": 8,
        },
        {
            "rank": 3,
            "user": "Charlie",
            "user_id": "charlie789",
            "xp": 11000,
            "completed": 35,
            "streak": 15,
        },
        {
            "rank": 4,
            "user": "Diana",
            "user_id": "diana012",
            "xp": 9500,
            "completed": 30,
            "streak": 5,
        },
        {
            "rank": 5,
            "user": "Eve",
            "user_id": "eve345",
            "xp": 8000,
            "completed": 25,
            "streak": 3,
        },
    ]

    print("Testing render.py with sample data:")
    print(f"Rich available: {RICH_AVAILABLE}")
    print(f"Tabulate available: {TABULATE_AVAILABLE}")

    # Test with different current users
    render_leaderboard(sample_data, "charlie789")  # Charlie should be highlighted
