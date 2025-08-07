# Step 6: Filtering, Watching, and Update Detection - Usage Guide

## Overview
Step 6 implements advanced filtering, watching, and update detection functionality for the leaderboard command. This includes period filtering, efficient change detection, and continuous monitoring with timestamps.

## Features Implemented

### 1. Period Filtering
The `leaderboard` command now properly passes the period parameter to the client:

```bash
# Different time periods
python -m src.tripleten_cli.cli leaderboard --period all_time
python -m src.tripleten_cli.cli leaderboard --period 30_days
python -m src.tripleten_cli.cli leaderboard --period 7_days
```

**Period Mapping:**
- `all_time` → `all` (client format)
- `30_days` → `month` (client format)
- `7_days` → `week` (client format)

### 2. Watch Mode with Change Detection
When `--watch` is enabled, the command continuously monitors for data changes:

```bash
# Watch mode with default interval (30 seconds)
python -m src.tripleten_cli.cli leaderboard --watch

# Watch mode with custom interval
python -m src.tripleten_cli.cli leaderboard --watch --interval 10

# Watch mode with specific period
python -m src.tripleten_cli.cli leaderboard --period 7_days --watch --interval 15
```

**Watch Mode Behavior:**
- Fetches current data every `interval` seconds
- Computes SHA256 hash of JSON data for change detection
- Only clears console and re-renders if data has changed (efficiency)
- Displays refresh information and timestamps
- Handles Ctrl-C gracefully

### 3. Timestamp Footer
Every refresh includes a timestamp showing when data was last fetched:

```
Last refreshed: 2025-08-07 03:44:59
Refreshing every 30 seconds. Press Ctrl+C to exit.
```

### 4. Graceful Exit
Proper Ctrl-C handling with different messages:
- Watch mode: "Watch mode stopped."
- Regular mode: "Leaderboard display interrupted."

## Technical Implementation

### Change Detection Algorithm
```python
def has_data_changed(data: Dict[str, Any]) -> bool:
    """Check if data has changed since last fetch."""
    current_hash = compute_data_hash(data)
    if previous_hash is None or current_hash != previous_hash:
        previous_hash = current_hash
        return True
    return False
```

### Hash Computation
Uses SHA256 with sorted JSON keys for consistent hashing:
```python
def compute_data_hash(data: Dict[str, Any]) -> str:
    json_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_string.encode()).hexdigest()
```

### Console Management
- Uses `rich.console.Console().clear()` for clean refreshes
- Only clears and re-renders when data actually changes
- Maintains timestamp and watch status information

## Configuration Integration

### Default Values
Configuration-based defaults are used when options aren't specified:
```python
config = get_config()
if period is None:
    period = config.default_period  # e.g., "all_time"
if interval is None:
    interval = config.default_interval  # e.g., 30
```

### Client Integration
- Dynamically imports and initializes HTTP client
- Maps CLI period format to client-expected format
- Handles API failures with fallback to sample data
- Integrates with existing render module for display

## Error Handling

### API Failures
If the API client fails, the system gracefully falls back:
```
Warning: API fetch failed: [error details]
Falling back to sample data...
```

### Module Import Issues
If client/render modules are unavailable, built-in fallbacks are used:
```
Warning: Could not initialize client: [error details]
```

### Configuration Errors
Configuration issues don't prevent operation:
```
Warning: Configuration error: [error details]
[continues with hardcoded defaults]
```

## Performance Considerations

### Efficient Updates
- Only re-renders when data actually changes
- Hash comparison is much faster than deep object comparison
- Console clearing only happens on actual changes

### Network Efficiency
- Respects configured refresh intervals
- Handles network errors gracefully
- Maintains connection through HTTP client session

### Memory Management
- Hash values stored efficiently
- Previous data not retained (only hash)
- Clean resource management

## Example Output

### Normal Mode
```bash
$ python -m src.tripleten_cli.cli leaderboard --period 7_days

🏆 Leaderboard
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Rank  ┃ User                 ┃ XP       ┃ Completed   ┃ Streak  ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│   1   │ Alice Johnson        │     2450 │          12 │       8 │
│   2   │ Bob Smith            │     2320 │          11 │       5 │
│   3   │ Carol Davis          │     2180 │          10 │      12 │
└───────┴──────────────────────┴──────────┴─────────────┴─────────┘

Last refreshed: 2025-08-07 03:44:59
```

### Watch Mode
```bash
$ python -m src.tripleten_cli.cli leaderboard --watch --interval 10

🏆 Leaderboard
[table content here]

Refreshing every 10 seconds. Press Ctrl+C to exit.
Last refreshed: 2025-08-07 03:44:59
```

## Testing

Run the comprehensive test suite:
```bash
python test_step6_implementation.py
```

This tests all implemented features without running the blocking CLI interface.
