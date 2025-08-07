#!/usr/bin/env python3
"""
Debug script to test the exact API call being made by the CLI.
"""

import json

import requests


def test_api_call():
    """Test the API call with detailed debugging."""

    # Your cookie string
    cookies_string = "__hstc=213200907.02b07a356598b552781acdcec89516aa.1752781222108.1753722562728.1753968476687.9; hubspotutk=02b07a356598b552781acdcec89516aa; __stripe_mid=9cebb4e6-b62b-4a7f-bce0-176e080df43dfd8f81; ahoy_visitor=d381d27b-639f-461a-9122-07a6514e064d; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc3pNakV4TnpNd01sMHNJaVF5WVNReE1TUXlOMVIxYTJWdmJqSm5Wa2c2Tkdaek9VWkhiM1V1SWl3aU1UYzFNamM0MVRRek1TNDRNVEUzTURFNElsMD0iLCJleHAiOiIyMDI2LTA3LTE3VDE5OjQzOjUxLjgxMVoiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdXNlcl90b2tlbiJ9fQ%3D%3D--af06cfef62e867bb86ddddc3d4539bb3c5b537fb; user_session_identifier=MIS3QY%2FgXz198uqrTSJQR7MsvhqS8dsiyZLF2slbC6x8okIx%2F0uU8Ba%2FgOq0rjaqgTMazAM2YNwiV0Q23afYs%2BM%2FqQ7w6FbnZaT%2FKlOJ2artEEE9zgy9YLbnKMhEA23pXBhqh10NkoGZKE1gtNLEjDtQp4qZo45NgkrUFGydVCtrEdqRJk%2FUdSiqZyDIOf7qg%2FiflztQYf173VSW2SqFSyvRnA9ucLDrD8WkUMkvtlvXm031Dqm3zDfwG%2B8AfyLJNfxJ3vHI4S9i82DcUw%3D%3D--t05Sb2qLjWU1j8zt--tgOImVfPBgXqcv%2BjpfL7ww%3D%3D; __stripe_mid=9cebb4e6-b62b-4a7f-bce0-176e080df43dfd8f81; browser_time_zone=America/Bogota; cf_clearance=9HgkNUpUMffQcWeBPEdJq5Ey4uBbGNWHzzA8IcFjbQ0-1754552955-*******-ctUNQvtWTQlqEN5yQkmXFw17X0mmK2D5HwR1UXO86qpFUvqSgp8faJpvQWGnsGKGLfBp2GrBLywdVE2WHycVjKQhYpSw3LfP0v7bDrGnF3D6hTVrhyFpNgSU9GpIUEYlOyR88CLiBkUfExtIwJijWwA2o2NwHJwSld1YF3K7X3sBUfJHo7lRLCm8RUmZJYYkKG1AkN_rbeAst0sU3ih_ezZ48dWAwdWwTeFjkFH0f8Q; _gcl_au=1.1.296026949.1752781432; _ga_MM8XRJL4KR=GS2.1.s1753108117$o26$g0$t1753108117$j60$l0$h0; _ga=GA1.1.651110119.1752781432; _ga_2938F36GJY=GS2.1.s1753761330$o40$g1$t1753761375$j15$l0$h0; _ga_SY30N92ZP8=GS2.1.s1753761330$o40$g1$t1753761375$j15$l0$h0; _ga_TXMVE71H94=GS2.1.s1753615583$o4$g0$t1753615583$j60$l0$h1585361409; __cf_bm=5HF8pqN.AHT_i7rcebFCJcTBy2rNCgLlAGAKaLPkpBg-1754553624-*******-PIzo1BuHkXpTSu6b7iHKTxLYYGP1YV7N_OsDXAdOpyMe_HgR4Ta0AzSF1s1Wv6vk3lqUTzdUvF3GmxNwyfYcwrUQ0MWQdBUztVfBvZZCCfc; ahoy_visit=d39b684d-718f-4c9c-abb9-18c83c5fffd1; auto_login_return_uri=https%3A%2F%2Ftripleten.com%2Fhome%2Fweb%2F; cookies_enabled=true; _circle_session=WKj5EadfNJH8dtxMLlLappGpOWOdaOYV27eXPXvGRRABgPvE23oXumjvGa1q3dipDG7n5lY6hTDqF67XckwRgTfB145lpbrj4cadg8XWKe4Np%2Fyxnvj78klZiOtGSXqOSd5A4WGzyfiv0vxXl8SxOkBKzTMWne1K9ZODPp%2F4NQJ9m2PSLFC2xUPVTfyVqZMpsX978fpnjXYZjHK5jwmBtag0W7eqDoYC%2Bk7F8sMtycPM8Wd5psqslgJNWtMDQItSKYOpa767zLtTSsMmq23SKU%2Bw0ggFxyjA6h45PSKxPnOG5qdynYGfMU%2FvnAOKaTRdVRNGMBx65C3Fa8oUOb3%2FZ3mCytTz3j59hxCkHsMwGdrmrY%2BCLu3ldlz7uNorqX9wOgdFnF0E%2Bem19WsVcuiOJKLTLMIJHt1CqfoWe%2FDEWbasDW6T9KUZrRAeO3JEb48m8EG%2FPjhFWrpu6MeJZ6B%2B23%2BQw85dzyDzVplbUkpGfezHAe5e8TIZaDcNyMcGnT5HRsxDiOBvwdRWF%2FdKK9d4tpEo1XtKCG%2FJmfIRNFAQCVGqrdnVTJAEhnMcr1wwvzfRhdoN5aIchBAxC6k%3D--zfFZvojyGxI7aMX5--7bMcU2EmkRGt4lka8A3FOQ%3D%3D; __hssrc=1; __stripe_sid=d66475a2-c785-44a2-ad2e-834d436daddd5e7abf; ph_phc_WhtnSDfNsIYmOv068S1ZfCVtRLna6Wu9sCUcRO1IC4X_posthog=%7B%22distinct_id%22%3A%22200094517%22%2C%22%24sesid%22%3A%5B1754553634148%2C%2201988376-dfaa-745d-a114-dd776f48fd84%22%2C1754552262559%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Ftripleten.com%2Fhome%2Fweb%2F%22%7D%7D"

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
