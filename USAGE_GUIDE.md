# TripleTen CLI Usage Guide - HTTP API Integration

This guide explains how to use the TripleTen CLI with the new HTTP API integration that directly connects to the TripleTen leaderboard API.

## Authentication Setup

The CLI now uses browser cookies for authentication instead of username/password. This method is more reliable and matches how the web interface works.

### Step 1: Get Your Browser Cookies

1. **Open your browser** and navigate to [https://hub.tripleten.com/leaderboard/](https://hub.tripleten.com/leaderboard/)
2. **Login** to your TripleTen account if you haven't already
3. **Open Developer Tools** (F12 or right-click → "Inspect")
4. **Go to the Network tab**
5. **Refresh the page** (Ctrl+R / Cmd+R)
6. **Find the leaderboard request** (look for a request to `/internal_api/gamification/leaderboard`) or use `copy(document.cookie);`
7. **Right-click on the request** → "Copy" → "Copy as cURL"
8. **Extract the Cookie header** from the cURL command

Example of what you're looking for in the cURL:
```bash
curl 'https://hub.tripleten.com/internal_api//gamification/leaderboard?period=all_time' \
  -H 'Cookie: __hstc=213200907...; remember_user_token=eyJfcm...; user_session_identifier=MIS3QY...'
```

Copy everything after `Cookie: ` and before the next `-H`.

### Step 2: Configure the CLI

Run the login command:

```bash
tripleten login
```

When prompted, paste your complete cookie string. The CLI will:
- Parse and store the cookies securely
- Test the authentication by making a test API call
- Save the cookies for future use

### Step 3: Verify Authentication

Test that everything is working:

```bash
tripleten leaderboard
```

If successful, you should see the actual leaderboard data from TripleTen instead of the fallback sample data.

## Using the CLI

### View Leaderboards

```bash
# Default leaderboard (uses config default, typically all-time)
tripleten

# Specific time periods
tripleten leaderboard --period all_time
tripleten leaderboard --period 30_days
tripleten leaderboard --period 7_days
```

### Watch Mode (Real-time Updates)

```bash
# Watch with default 30-second refresh
tripleten leaderboard --watch

# Custom refresh interval
tripleten leaderboard --watch --interval 60

# Short form
tripleten -w --interval 45
```

### Configuration

```bash
# Show current configuration
tripleten config --show

# Set default time period
tripleten config --set default_period 7_days

# Set default refresh interval
tripleten config --set default_interval 45
```

## API Integration Details

The CLI now connects directly to the TripleTen API:

- **Base URL**: `https://hub.tripleten.com`
- **Endpoint**: `/internal_api/gamification/leaderboard`
- **Parameters**: `period` (all_time, 30_days, or 7_days)
- **Authentication**: Browser cookies
- **Headers**: Matches browser requests exactly

### Period Mapping

The CLI automatically maps periods:
- CLI `all_time` → API `all_time`
- CLI `30_days` → API `30_days`
- CLI `7_days` → API `7_days`

## Troubleshooting

### Authentication Issues

If you see authentication errors:

1. **Check your cookies**: They may have expired. Re-extract fresh cookies from your browser.
2. **Re-login**: Run `tripleten login` again with fresh cookies.
3. **Check browser session**: Make sure you're still logged into TripleTen in your browser.

### API Issues

If the API is not responding:

1. **Check the TripleTen website**: Make sure it's accessible in your browser.
2. **Network issues**: The CLI will fall back to sample data if the API is unreachable.
3. **Check headers**: The CLI mimics browser headers exactly, but server changes might affect this.

### Cookie Format

The cookie string should look like this:
```
__hstc=213200907.02b07a356598b552781acdcec89516aa.1752781222108.1753722562728.1753968476687.9; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc3pN...; user_session_identifier=MIS3QY%2FgXz198uqrTSJQR7MsvhqS8dsiyZLF...
```

Make sure to copy the entire string including all cookies separated by semicolons.

## Files and Storage

- **Config directory**: `~/.config/tripleten-cli/` (Linux/macOS) or `%APPDATA%\tripleten-cli\` (Windows)
- **Configuration file**: `config.toml` (settings and preferences)
- **Cookies file**: `cookies.json` (authentication cookies)

Both files are created with secure permissions to protect your authentication data.

## Security

- Cookies are stored locally with restricted file permissions
- No passwords or sensitive credentials are stored in plain text
- The CLI uses HTTPS for all API communications
- Session cookies automatically expire based on TripleTen's session policies
