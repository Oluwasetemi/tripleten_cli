"""HTTP client module for TripleTen CLI.

This module provides HTTP client functionality with session management,
authentication handling, and leaderboard data fetching.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class AuthenticationError(Exception):
    """Exception raised for authentication errors."""

    pass


class TripleTenHTTPClient:
    """HTTP client for TripleTen API with session management and authentication."""

    BASE_URL = "https://hub.tripleten.com"

    def __init__(self, config_dir: Path):
        """Initialize the HTTP client.

        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self.session = self._create_session()
        self._load_cookies()

    def _create_session(self) -> requests.Session:
        """Create a session with retry configuration and back-off strategy.

        Returns:
            Configured requests session
        """
        session = requests.Session()

        # Configure retry strategy with exponential backoff
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1,  # Will create delays: 0s, 2s, 4s
            raise_on_status=False,
        )

        # Mount adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers to match the browser request
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

        return session

    def _get_cookies_file_path(self) -> Path:
        """Get the path to the cookies file.

        Returns:
            Path to cookies.json file
        """
        return self.config_dir / "cookies.json"

    def _load_cookies(self) -> None:
        """Load cookies from the configuration file and attach to session."""
        cookies_file = self._get_cookies_file_path()

        if not cookies_file.exists():
            return

        try:
            with open(cookies_file, "r") as f:
                cookies_data = json.load(f)

            # Add cookies to session
            for name, value in cookies_data.items():
                self.session.cookies.set(name, value)

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load cookies: {e}", file=sys.stderr)

    def _save_cookies(self) -> None:
        """Save current session cookies to configuration file."""
        cookies_file = self._get_cookies_file_path()

        try:
            # Ensure config directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Convert session cookies to dictionary
            cookies_dict = {
                cookie.name: cookie.value for cookie in self.session.cookies
            }

            with open(cookies_file, "w") as f:
                json.dump(cookies_dict, f, indent=2)

        except IOError as e:
            print(f"Warning: Could not save cookies: {e}", file=sys.stderr)

    def login(self, cookie_string: str) -> None:
        """Set cookies from a browser cookie string.

        Args:
            cookie_string: Full cookie string from browser (like the one you provided)
        """
        # Clear existing cookies
        self.session.cookies.clear()

        # Parse cookie string - handle complex format with URL encoding
        if cookie_string:
            # Split by '; ' but be careful with complex values
            cookie_parts = []
            current_part = ""

            i = 0
            while i < len(cookie_string):
                if i < len(cookie_string) - 1 and cookie_string[i : i + 2] == "; ":
                    if "=" in current_part:
                        cookie_parts.append(current_part.strip())
                        current_part = ""
                        i += 2
                        continue

                current_part += cookie_string[i]
                i += 1

            # Add the last part
            if current_part.strip() and "=" in current_part:
                cookie_parts.append(current_part.strip())

            # Set each cookie
            for cookie_part in cookie_parts:
                if "=" in cookie_part:
                    name, value = cookie_part.split("=", 1)
                    name = name.strip()
                    value = value.strip()

                    # Skip empty cookies
                    if name and value:
                        self.session.cookies.set(
                            name, value, domain="hub.tripleten.com"
                        )

        # Save cookies to file
        self._save_cookies()
        print(f"Set {len(self.session.cookies)} cookies for TripleTen API")

    def _handle_auth_error(self) -> None:
        """Handle authentication errors by raising an exception."""
        raise AuthenticationError(
            "Authentication failed. Please run 'tripleten login' to authenticate."
        )

    def _make_request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> requests.Response:
        """Make an HTTP request with error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            SystemExit: On authentication error (401)
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            # Handle authentication errors
            if response.status_code == 401:
                self._handle_auth_error()

            return response

        except requests.RequestException as e:
            raise ConnectionError(f"Network error: {e}")

    def fetch_leaderboard(self, period: str = "all") -> Dict[str, Any]:
        """Fetch leaderboard data for the specified period.

        Args:
            period: Time period for leaderboard ("all_time", "30_days", "7_days")

        Returns:
            JSON response data as dictionary

        Raises:
            SystemExit: On authentication or network errors
        """
        # Map period to API format
        period_mapping = {"all": "all_time", "month": "30_days", "week": "7_days"}

        api_period = period_mapping.get(period, period)

        # Validate period parameter
        valid_periods = ["all_time", "30_days", "7_days"]
        if api_period not in valid_periods:
            raise ValueError(
                f"Invalid period '{api_period}'. Valid options: {', '.join(valid_periods)}"
            )

        # Make request to TripleTen leaderboard endpoint (note the double slash)
        endpoint = "/internal_api//gamification/leaderboard"
        params = {"period": api_period}

        # Add Referer header for this specific request
        headers = {
            "Referer": f"https://hub.tripleten.com/leaderboard/?period={api_period}"
        }

        response = self._make_request("GET", endpoint, params=params, headers=headers)

        # Check response status
        if response.status_code != 200:
            error_msg = f"API error: {response.status_code} - {response.reason}"
            if response.text:
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg += f" - {error_data['message']}"
                except json.JSONDecodeError:
                    error_msg += f" - {response.text}"
            raise requests.HTTPError(error_msg)

        # Parse JSON response
        try:
            data = response.json()

            # Transform the API response format to match expected CLI format
            if "top_members" in data:
                leaderboard = []
                for rank, member in enumerate(data["top_members"], 1):
                    leaderboard.append(
                        {
                            "rank": rank,
                            "user": member.get("name", "Unknown"),
                            "user_id": member.get("public_uid", ""),
                            "xp": member.get("total_points", 0),
                            "completed": 0,  # Not available in this API format
                            "streak": 0,  # Not available in this API format
                        }
                    )

                return {"leaderboard": leaderboard}

            return data  # type: ignore[no-any-return]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")

    def is_authenticated(self) -> bool:
        """Check if the client has valid authentication.

        Returns:
            True if authenticated, False otherwise
        """
        try:
            # Make a simple authenticated request to check status
            response = self._make_request("GET", "/api/user/profile")
            return response.status_code != 401
        except SystemExit:
            return False

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information.

        Returns:
            User information dictionary or None if not authenticated
        """
        try:
            response = self._make_request("GET", "/api/user/profile")
            if response.status_code == 200:
                result: Dict[str, Any] = response.json()
                return result
            return None
        except SystemExit:
            return None


def create_client(config_dir: Path) -> TripleTenHTTPClient:
    """Factory function to create HTTP client instance.

    Args:
        config_dir: Directory containing configuration files

    Returns:
        Configured HTTP client instance
    """
    return TripleTenHTTPClient(config_dir)
