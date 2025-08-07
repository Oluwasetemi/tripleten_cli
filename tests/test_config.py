"""Tests for the configuration module."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from tripleten_cli.config import Config, ConfigError


class TestConfig:
    """Test suite for Config class."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary directory for configuration testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def config(self, temp_config_dir):
        """Create a Config instance with temporary directory."""
        with patch.object(Config, "_get_config_dir", return_value=temp_config_dir):
            return Config()

    def test_config_initialization(self, config, temp_config_dir):
        """Test configuration initialization."""
        assert config._config_dir == temp_config_dir
        assert config._config_path == temp_config_dir / "config.toml"
        assert config._config_data == config.DEFAULT_CONFIG

    def test_config_directory_creation(self, temp_config_dir):
        """Test configuration directory is created."""
        config_dir = temp_config_dir / "subdir"
        with patch.object(Config, "_get_config_dir", return_value=config_dir):
            Config()
            assert config_dir.exists()

    def test_default_values(self, config):
        """Test default configuration values."""
        assert config.default_period == "all_time"
        assert config.default_interval == 30
        assert config.session_cookie is None
        assert config.user_id is None

    def test_set_and_get(self, config):
        """Test setting and getting configuration values."""
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
        assert config.get("nonexistent_key") is None
        assert config.get("nonexistent_key", "default") == "default"

    def test_delete(self, config):
        """Test deleting configuration keys."""
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"

        config.delete("test_key")
        assert config.get("test_key") is None

    def test_update(self, config):
        """Test updating configuration with dictionary."""
        update_data = {
            "key1": "value1",
            "key2": "value2",
        }
        config.update(update_data)

        assert config.get("key1") == "value1"
        assert config.get("key2") == "value2"

    def test_get_all(self, config):
        """Test getting all configuration data."""
        config.set("test_key", "test_value")
        all_config = config.get_all()

        assert "default_period" in all_config
        assert "default_interval" in all_config
        assert "test_key" in all_config
        assert all_config["test_key"] == "test_value"

    def test_session_cookie_property(self, config):
        """Test session cookie property."""
        assert config.session_cookie is None

        config.session_cookie = "test_cookie"
        assert config.session_cookie == "test_cookie"

        config.session_cookie = None
        assert config.session_cookie is None

    def test_user_id_property(self, config):
        """Test user ID property."""
        assert config.user_id is None

        config.user_id = "test_user"
        assert config.user_id == "test_user"

        config.user_id = None
        assert config.user_id is None

    def test_default_period_property(self, config):
        """Test default period property."""
        assert config.default_period == "all_time"

        config.default_period = "30_days"
        assert config.default_period == "30_days"

        with pytest.raises(ValueError):
            config.default_period = "invalid_period"

    def test_default_interval_property(self, config):
        """Test default interval property."""
        assert config.default_interval == 30

        config.default_interval = 60
        assert config.default_interval == 60

        with pytest.raises(ValueError):
            config.default_interval = 0

        with pytest.raises(ValueError):
            config.default_interval = "not_a_number"

    def test_save_and_load(self, config):
        """Test saving and loading configuration."""
        # Set some values
        config.session_cookie = "test_cookie"
        config.user_id = "test_user"
        config.default_period = "7_days"
        config.default_interval = 60

        # Save configuration
        config.save()
        assert config.config_path.exists()

        # Create a new config instance and verify it loads the saved data
        with patch.object(Config, "_get_config_dir", return_value=config._config_dir):
            new_config = Config()

        assert new_config.session_cookie == "test_cookie"
        assert new_config.user_id == "test_user"
        assert new_config.default_period == "7_days"
        assert new_config.default_interval == 60

    @pytest.mark.skipif(os.name == "nt", reason="Unix-specific permissions test")
    def test_secure_permissions(self, config):
        """Test that config file has secure permissions on Unix systems."""
        config.session_cookie = "test_cookie"
        config.save()

        # Check file permissions (should be 0o600)
        file_stat = config.config_path.stat()
        file_mode = file_stat.st_mode & 0o777
        assert file_mode == 0o600

    def test_invalid_toml_handling(self, config):
        """Test handling of invalid TOML files."""
        # Write invalid TOML to config file
        with open(config.config_path, "w") as f:
            f.write("invalid toml content [[[")

        # Should raise ConfigError when loading
        with pytest.raises(ConfigError):
            config.load()

    def test_config_path_property(self, config, temp_config_dir):
        """Test config path property."""
        expected_path = temp_config_dir / "config.toml"
        assert config.config_path == expected_path

    @pytest.mark.integration
    def test_platformdirs_integration(self, temp_config_dir):
        """Test that platformdirs is used correctly."""
        with patch(
            "tripleten_cli.config.platformdirs.user_config_dir"
        ) as mock_user_config_dir:
            mock_user_config_dir.return_value = str(temp_config_dir)
            config = Config()

            mock_user_config_dir.assert_called_once_with(
                appname="tripleten-cli", appauthor="TripleTen"
            )
            assert config._config_dir == temp_config_dir


class TestTOMLCompatibility:
    """Test TOML library compatibility across Python versions."""

    def test_tomli_import_python_310(self):
        """Test tomli is used for Python < 3.11."""
        # This test verifies the import logic without actually changing Python version
        if sys.version_info < (3, 11):
            import tripleten_cli.config

            # Should import tomli as tomllib for older Python versions
            assert hasattr(tripleten_cli.config, "tomllib")

    def test_tomllib_import_python_311(self):
        """Test tomllib is used for Python >= 3.11."""
        if sys.version_info >= (3, 11):
            import tripleten_cli.config

            # Should import standard library tomllib for newer Python versions
            assert hasattr(tripleten_cli.config, "tomllib")


def test_get_config_singleton():
    """Test that get_config returns a singleton instance."""
    from tripleten_cli.config import get_config

    config1 = get_config()
    config2 = get_config()

    assert config1 is config2  # Should be the same instance


class TestConfigError:
    """Test ConfigError exception."""

    def test_config_error_inheritance(self):
        """Test that ConfigError inherits from Exception."""
        error = ConfigError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
