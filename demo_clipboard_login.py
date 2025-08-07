#!/usr/bin/env python3
"""
Demo script to show how the clipboard login functionality works.
"""

import pyperclip

# Sample cookie string (not real authentication data)
sample_cookies = (
    "test_cookie=sample_value; session_id=demo123; user_token=example_token"
)


def demo_clipboard_login():
    print("🔧 Demo: Clipboard-based Login")
    print("=" * 40)

    print("1. First, let's simulate copying cookies to clipboard...")
    pyperclip.copy(sample_cookies)
    print(f"✅ Copied to clipboard: {sample_cookies[:50]}...")

    print("\n2. Now you can run:")
    print("   tripleten login")
    print("   (It will automatically read from clipboard)")

    print("\n3. Or you can explicitly disable clipboard reading:")
    print("   tripleten login --no-clipboard")

    print("\n4. Or provide cookies directly:")
    print('   tripleten login --cookies "your_cookie_string_here"')

    print("\n📋 Current clipboard content:")
    print(f"   {pyperclip.paste()[:100]}...")


if __name__ == "__main__":
    demo_clipboard_login()
