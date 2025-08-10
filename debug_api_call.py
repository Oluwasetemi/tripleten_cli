#!/usr/bin/env python3
"""
Debug script to test the exact API call being made by the CLI.
"""

import json

import requests


def test_api_call():
    """Test the API call with detailed debugging."""

    # Your cookie string
    cookies_string = ""

    # Create session
    session = requests.Session()

    # Set headers exactly like the browser
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=4",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }
    )

    # Parse cookies manually
    for cookie in cookies_string.split("; "):
        if "=" in cookie:
            name, value = cookie.split("=", 1)
            session.cookies.set(name.strip(), value.strip(), domain=".tripleten.com")

    print(f"🍪 Set {len(session.cookies)} cookies")

    # Test the exact URL and parameters
    url = "https://hub.tripleten.com/internal_api/gamification/leaderboard"
    params = {"period": "all_time"}
    headers = {"Referer": "https://hub.tripleten.com/leaderboard/?period=all_time"}

    print(f"🌐 Making request to: {url}")
    print(f"📋 Parameters: {params}")
    print(f"📄 Additional headers: {headers}")

    try:
        response = session.get(url, params=params, headers=headers)

        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Response Length: {len(response.text)} chars")
        print(f"🔧 Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ JSON Response: {json.dumps(data, indent=2)}")

                if "leaderboard" in data:
                    leaderboard = data["leaderboard"]
                    print(f"🏆 Leaderboard entries: {len(leaderboard)}")
                    for i, entry in enumerate(leaderboard[:3]):  # Show first 3
                        print(f"  {i+1}. {entry}")
                else:
                    print("⚠️ No 'leaderboard' key found in response")

            except json.JSONDecodeError as e:
                print(f"❌ JSON Error: {e}")
                print(f"📄 Raw response: {response.text[:500]}...")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"📄 Response: {response.text[:500]}...")

    except Exception as e:
        print(f"💥 Request failed: {e}")


if __name__ == "__main__":
    test_api_call()
