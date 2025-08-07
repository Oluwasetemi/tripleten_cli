# TripleTen HTTP Client

A robust HTTP client module for the TripleTen CLI that provides session management, authentication handling, and API interaction capabilities.

## Features

- **Session Management**: Uses `requests.Session` with persistent cookies
- **Retry Strategy**: Implements exponential backoff with urllib3 Retry for reliability
- **Authentication Handling**: Automatic detection of 401 errors with user-friendly messages
- **Cookie Persistence**: Saves and loads cookies from configuration files
- **Leaderboard API**: Easy access to leaderboard data with period filtering

## Usage

### Basic Setup

```python
from pathlib import Path
from client import create_client

# Initialize client with config directory
config_dir = Path.home() / ".tripleten"
client = create_client(config_dir)
```

### Authentication

```python
# Login with cookie string (typically called by CLI login command)
cookie_string = "session_id=abc123; csrf_token=def456"
client.login(cookie_string)

# Check authentication status
if client.is_authenticated():
    print("User is authenticated")
else:
    print("Please run 'tripleten login' to authenticate")
```

### Fetching Leaderboard Data

```python
# Fetch all-time leaderboard
leaderboard = client.fetch_leaderboard("all")

# Fetch monthly leaderboard
monthly_data = client.fetch_leaderboard("month")

# Fetch weekly leaderboard
weekly_data = client.fetch_leaderboard("week")

# Fetch daily leaderboard
daily_data = client.fetch_leaderboard("day")
```

### User Information

```python
# Get current user info
user_info = client.get_user_info()
if user_info:
    print(f"User: {user_info['name']}")
```

## Configuration

The client stores cookies in `~/.tripleten/cookies.json` by default. The configuration directory can be customized when creating the client.

## Error Handling

- **401 Unauthorized**: Automatically prompts user to run `tripleten login`
- **Network Errors**: Displays user-friendly error messages and exits gracefully
- **Invalid Periods**: Validates leaderboard period parameters
- **JSON Errors**: Handles malformed API responses

## Retry Strategy

The client implements an exponential backoff retry strategy:
- **Total Retries**: 3 attempts
- **Status Codes**: Retries on 429, 500, 502, 503, 504
- **Methods**: Only retries safe methods (HEAD, GET, OPTIONS)
- **Backoff**: Exponential delays: 0s, 2s, 4s

## Dependencies

- `requests>=2.25.0`
- `urllib3>=1.26.0`

## Testing

Run the test suite with:

```bash
python -m unittest test_client.py -v
```

## API Endpoints

The client is configured to use the TripleTen API with these endpoints:

- `GET /api/leaderboard` - Fetch leaderboard data
- `GET /api/user/profile` - Get user profile information

## Base URL

Update the `BASE_URL` constant in the client to match your environment:

```python
BASE_URL = "https://practicum.yandex.com"  # Production
```
