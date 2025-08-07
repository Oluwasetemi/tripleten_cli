#!/usr/bin/env python3
"""
Test script to verify the TripleTen API connection works with the new implementation.
"""

import os
import sys
from pathlib import Path

# Set PYTHONPATH to include the current directory
os.environ["PYTHONPATH"] = str(Path(__file__).parent)

# Import the installed tripleten CLI to test the functionality
try:
    from tripleten_cli.cli import tripleten

    print("✅ Successfully imported tripleten CLI")
except ImportError as e:
    print(f"❌ Failed to import tripleten CLI: {e}")
    sys.exit(1)

# Use the imported tripleten to suppress F401
_ = tripleten

# Also test direct import
sys.path.insert(0, str(Path(__file__).parent))

try:
    from client import create_client

    print("✅ Successfully imported client module")
except ImportError as e:
    print(f"❌ Failed to import client: {e}")
    print(
        "This might be due to missing dependencies. Make sure you ran 'pip install -e .[dev]'"
    )


def test_api_connection():
    """Test the API connection without real cookies."""
    print("Testing TripleTen API connection...")

    # Create a temporary config directory for testing
    config_dir = Path.home() / ".config" / "tripleten-cli-test"
    config_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Create client
        client = create_client(config_dir)
        print("✅ Client created successfully")
        print(f"✅ Base URL: {client.BASE_URL}")
        print(f"✅ Config directory: {config_dir}")

        # Test headers
        headers = dict(client.session.headers)
        print(f"✅ Headers configured: {len(headers)} headers set")
        print(f"   User-Agent: {headers.get('User-Agent', 'Not set')}")
        print(f"   Accept: {headers.get('Accept', 'Not set')}")

        # Test cookie parsing (with dummy data)
        test_cookie = "test_cookie=test_value; another_cookie=another_value"
        client.login(test_cookie)
        print(f"✅ Cookie parsing works: {len(client.session.cookies)} cookies set")

        print("\n🔧 Ready to test with real cookies!")
        print("Usage:")
        print("1. Copy your browser cookies from Developer Tools")
        print("2. Run: tripleten login")
        print("3. Paste the cookie string when prompted")
        print("4. Run: tripleten leaderboard")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    finally:
        # Clean up test directory
        import shutil

        if config_dir.exists():
            shutil.rmtree(config_dir)


if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)
