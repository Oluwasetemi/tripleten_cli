#!/usr/bin/env python3
"""
Demonstration script for render.py showing all features
"""

import json

from render import (
    RICH_AVAILABLE,
    TABULATE_AVAILABLE,
    render_from_json_file,
    render_from_json_string,
    render_leaderboard,
)


def main():
    print("🏆 LEADERBOARD RENDER DEMO")
    print("=" * 50)
    print(f"Rich library: {'✓ Available' if RICH_AVAILABLE else '✗ Not Available'}")
    print(
        f"Tabulate library: {'✓ Available' if TABULATE_AVAILABLE else '✗ Not Available'}"
    )

    # Sample leaderboard data
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
        {
            "rank": 6,
            "user": "Frank",
            "user_id": "frank678",
            "xp": 7500,
            "completed": 22,
            "streak": 7,
        },
    ]

    print("\n\n🎯 DEMO 1: Current User Highlighting")
    print("Current user: Alice (rank 1 - should be highlighted in bold yellow)")
    print("-" * 60)
    render_leaderboard(sample_data, "alice123")

    print("\n\n🎯 DEMO 2: Different Current User")
    print("Current user: Charlie (rank 3 - should be highlighted in bold yellow)")
    print("-" * 60)
    render_leaderboard(sample_data, "charlie789")

    print("\n\n🎯 DEMO 3: Rank Colors (Top 3)")
    print("Notice the rank colors:")
    print("• Rank 1: Gold")
    print("• Rank 2: Silver")
    print("• Rank 3: Bronze")
    print("-" * 60)
    render_leaderboard(sample_data, "nonexistent_user")  # No user highlighting

    print("\n\n🎯 DEMO 4: JSON String Parsing")
    print("Loading from JSON string with 'leaderboard' wrapper")
    print("-" * 60)
    wrapped_json = json.dumps({"leaderboard": sample_data[:3]})  # Just top 3
    render_from_json_string(wrapped_json, "bob456")

    print("\n\n🎯 DEMO 5: Creating JSON File and Loading It")
    print("Creating test.json and loading from file")
    print("-" * 60)
    # Create a test JSON file
    with open("test_leaderboard.json", "w") as f:
        json.dump(sample_data, f, indent=2)

    render_from_json_file("test_leaderboard.json", "diana012")

    print("\n\n🎯 DEMO 6: Error Handling")
    print("Testing with empty data:")
    render_leaderboard([], "any_user")

    print("\nTesting with non-existent file:")
    render_from_json_file("nonexistent.json", "any_user")

    print("\n" + "=" * 60)
    print("✨ RENDER.PY FEATURES SUMMARY:")
    print("✓ Rich table display with styling (when available)")
    print("✓ Tabulate fallback (when rich not available)")
    print("✓ Basic text fallback (when neither available)")
    print("✓ Current user highlighting (bold yellow)")
    print("✓ Top 3 rank colorization (gold/silver/bronze)")
    print("✓ Graceful import handling")
    print("✓ JSON file and string parsing")
    print("✓ Multiple JSON format support")
    print("✓ Error handling and validation")
    print("=" * 60)


if __name__ == "__main__":
    main()
