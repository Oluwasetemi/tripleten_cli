"""Configuration and credential management for TripleTen CLI.

This module handles reading and writing configuration data to a TOML file
located in the appropriate user configuration directory for each platform.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import platformdirs

# Handle TOML libraries for different Python versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w


class ConfigError(Exception):
    """Exception raised for configuration-related errors."""

    pass


class Config:
    """Configuration manager for TripleTen CLI.

    Handles reading and writing configuration data including:
    - session_cookie: Authentication session cookie
    - user_id: Optional user identifier
    - default_period: Default time period for leaderboard
    - default_interval: Default refresh interval for watch mode
    """

    # Configuration file name
    CONFIG_FILE = "config.toml"

    # Default configuration values
    DEFAULT_CONFIG = {
        "default_period": "all_time",
        "default_interval": 30,
    }

    def __init__(self) -> None:
        """Initialize configuration manager."""
        self._config_dir = self._get_config_dir()
        self._config_path = self._config_dir / self.CONFIG_FILE
        self._config_data: Dict[str, Any] = {}

        # Ensure config directory exists
        self._ensure_config_dir()

        # Load existing configuration
        self.load()

    def _get_config_dir(self) -> Path:
        """Get the configuration directory path for the current platform.

        Returns:
            Path to configuration directory:
            - Linux/macOS: ~/.config/tripleten-cli/
            - Windows: %APPDATA%/tripleten-cli/
        """
        config_dir = platformdirs.user_config_dir(
            appname="tripleten-cli", appauthor="TripleTen"
        )
        return Path(config_dir)

    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists with proper permissions."""
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)

            # Set secure permissions on Unix-like systems
            if os.name != "nt":  # Not Windows
                os.chmod(self._config_dir, 0o700)  # rwx------

        except OSError as e:
            raise ConfigError(f"Failed to create config directory: {e}")

    def _set_secure_permissions(self) -> None:
        """Set secure file permissions on the config file (Unix/Linux/macOS only)."""
        if os.name != "nt" and self._config_path.exists():
            try:
                # Set permissions to 0o600 (rw-------)
                os.chmod(self._config_path, 0o600)
            except OSError as e:
                raise ConfigError(f"Failed to set secure permissions: {e}")

    def load(self) -> None:
        """Load configuration from file.

        If the file doesn't exist, starts with default configuration.
        """
        self._config_data = self.DEFAULT_CONFIG.copy()

        if not self._config_path.exists():
            return

        try:
            with open(self._config_path, "rb") as f:
                file_config = tomllib.load(f)
                self._config_data.update(file_config)
        except (OSError, tomllib.TOMLDecodeError) as e:
            raise ConfigError(f"Failed to load configuration: {e}")

    def save(self) -> None:
        """Save configuration to file with secure permissions."""
        try:
            # Ensure directory exists
            self._ensure_config_dir()

            # Write configuration to file
            with open(self._config_path, "wb") as f:
                tomli_w.dump(self._config_data, f)

            # Set secure permissions
            self._set_secure_permissions()

        except OSError as e:
            raise ConfigError(f"Failed to save configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key to retrieve
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        return self._config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key to set
            value: Value to set
        """
        self._config_data[key] = value

    def delete(self, key: str) -> None:
        """Delete a configuration key.

        Args:
            key: Configuration key to delete
        """
        self._config_data.pop(key, None)

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data.

        Returns:
            Dictionary of all configuration data
        """
        return self._config_data.copy()

    def update(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration with a dictionary of values.

        Args:
            config_dict: Dictionary of configuration values to update
        """
        self._config_data.update(config_dict)

    @property
    def config_path(self) -> Path:
        """Get the path to the configuration file.

        Returns:
            Path to configuration file
        """
        return self._config_path

    # Convenience methods for common configuration values

    @property
    def session_cookie(self) -> Optional[str]:
        """Get the session cookie."""
        value = self.get("session_cookie")
        return value if isinstance(value, str) else None

    @session_cookie.setter
    def session_cookie(self, value: Optional[str]) -> None:
        """Set the session cookie."""
        if value is None:
            self.delete("session_cookie")
        else:
            self.set("session_cookie", value)

    @property
    def user_id(self) -> Optional[str]:
        """Get the user ID."""
        value = self.get("user_id")
        return value if isinstance(value, str) else None

    @user_id.setter
    def user_id(self, value: Optional[str]) -> None:
        """Set the user ID."""
        if value is None:
            self.delete("user_id")
        else:
            self.set("user_id", value)

    @property
    def default_period(self) -> str:
        """Get the default period."""
        value = self.get("default_period", "all_time")
        return str(value)

    @default_period.setter
    def default_period(self, value: str) -> None:
        """Set the default period."""
        valid_periods = ["all_time", "30_days", "7_days"]
        if value not in valid_periods:
            raise ValueError(
                f"Invalid period: {value}. Must be one of: {valid_periods}"
            )
        self.set("default_period", value)

    @property
    def default_interval(self) -> int:
        """Get the default interval."""
        value = self.get("default_interval", 30)
        return int(value)

    @default_interval.setter
    def default_interval(self, value: int) -> None:
        """Set the default interval."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Interval must be a positive integer")
        self.set("default_interval", value)


# Module-level singleton instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get a singleton instance of the configuration manager.

    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
