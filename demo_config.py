#!/usr/bin/env python3
"""
Demonstration script for TripleTen CLI configuration system.

This script shows how the configuration system works:
- Cross-platform path handling
- Secure file permissions on Unix systems
- TOML file reading/writing
- Default value handling
"""

import os

from src.tripleten_cli.config import ConfigError, get_config


def main():
    """Demonstrate the configuration system."""
    print("TripleTen CLI Configuration System Demo")
    print("=" * 40)

    try:
        # Get configuration instance (singleton)
        config = get_config()

        print(f"Configuration file path: {config.config_path}")
        print(f"Configuration directory: {config.config_path.parent}")
        print(
            f"Platform: {os.name} ({'Windows' if os.name == 'nt' else 'Unix/Linux/macOS'})"
        )
        print()

        # Show initial configuration
        print("Initial configuration:")
        for key, value in config.get_all().items():
            print(f"  {key}: {value}")
        print()

        # Demonstrate setting values
        print("Setting some configuration values...")
        config.session_cookie = "demo_session_cookie_123"
        config.user_id = "demo_user"
        config.default_period = "7_days"
        config.default_interval = 45
        config.set("custom_setting", "custom_value")

        # Show updated configuration
        print("Updated configuration:")
        for key, value in config.get_all().items():
            display_value = value
            if key == "session_cookie" and value:
                # Mask sensitive data for display
                display_value = "****" + value[-8:]
            print(f"  {key}: {display_value}")
        print()

        # Save configuration
        print("Saving configuration...")
        config.save()

        # Show file information
        if config.config_path.exists():
            stat = config.config_path.stat()
            permissions = oct(stat.st_mode)[-3:]
            print(f"Configuration file created: {config.config_path}")
            print(f"File permissions: {permissions}")

            if os.name != "nt":  # Unix-like systems
                expected_permissions = "600"
                if permissions == expected_permissions:
                    print("✅ Secure permissions set correctly (owner read/write only)")
                else:
                    print(
                        f"⚠️  Expected permissions {expected_permissions}, got {permissions}"
                    )
            else:
                print("ℹ️  Windows filesystem - permissions handled by NTFS")

        # Show file contents
        print("\nConfiguration file contents:")
        with open(config.config_path, "r") as f:
            content = f.read()
            for i, line in enumerate(content.split("\n"), 1):
                if line.strip():
                    print(f"  {i:2d}: {line}")

        print("\nDemonstration completed successfully!")

    except ConfigError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
