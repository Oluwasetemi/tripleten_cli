"""Tests for the render module."""

import json
from unittest.mock import Mock, patch

import pytest

from tripleten_cli.render import (
    RICH_AVAILABLE,
    TABULATE_AVAILABLE,
    _get_rank_styled_text,
    _render_basic,
    _render_with_rich,
    _render_with_tabulate,
    render_from_json_file,
    render_from_json_string,
    render_leaderboard,
)


class TestRenderLeaderboard:
    """Test suite for render_leaderboard function."""

    @pytest.fixture
    def sample_leaderboard_data(self):
        """Sample leaderboard data for testing."""
        return [
            {
                "rank": 1,
                "user": "Alice",
                "user_id": "alice123",
                "xp": 2500,
                "completed": 15,
                "streak": 10,
            },
            {
                "rank": 2,
                "user": "Bob",
                "user_id": "bob456",
                "xp": 2200,
                "completed": 12,
                "streak": 8,
            },
            {
                "rank": 3,
                "user": "Charlie",
                "user_id": "charlie789",
                "xp": 1980,
                "completed": 11,
                "streak": 6,
            },
            {
                "rank": 4,
                "user": "Diana",
                "user_id": "diana012",
                "xp": 1750,
                "completed": 9,
                "streak": 4,
            },
            {
                "rank": 5,
                "user": "Eve",
                "user_id": "eve345",
                "xp": 1500,
                "completed": 8,
                "streak": 3,
            },
        ]

    @pytest.fixture
    def empty_leaderboard_data(self):
        """Empty leaderboard data for testing."""
        return []

    def test_render_leaderboard_empty_data(self, empty_leaderboard_data):
        """Test rendering with empty leaderboard data."""
        with patch("builtins.print") as mock_print:
            render_leaderboard(empty_leaderboard_data, "test_user")
            mock_print.assert_called_once_with("No leaderboard data available.")

    @patch("tripleten_cli.render.RICH_AVAILABLE", True)
    def test_render_leaderboard_uses_rich_when_available(self, sample_leaderboard_data):
        """Test that render_leaderboard uses rich when available."""
        with patch("tripleten_cli.render._render_with_rich") as mock_rich_render:
            render_leaderboard(sample_leaderboard_data, "alice123")
            mock_rich_render.assert_called_once_with(
                sample_leaderboard_data, "alice123"
            )

    @patch("tripleten_cli.render.RICH_AVAILABLE", False)
    @patch("tripleten_cli.render.TABULATE_AVAILABLE", True)
    def test_render_leaderboard_uses_tabulate_when_rich_unavailable(
        self, sample_leaderboard_data
    ):
        """Test that render_leaderboard uses tabulate when rich is unavailable."""
        with patch(
            "tripleten_cli.render._render_with_tabulate"
        ) as mock_tabulate_render:
            render_leaderboard(sample_leaderboard_data, "alice123")
            mock_tabulate_render.assert_called_once_with(
                sample_leaderboard_data, "alice123"
            )

    @patch("tripleten_cli.render.RICH_AVAILABLE", False)
    @patch("tripleten_cli.render.TABULATE_AVAILABLE", False)
    def test_render_leaderboard_uses_basic_when_no_libraries(
        self, sample_leaderboard_data
    ):
        """Test that render_leaderboard uses basic rendering when no libraries available."""
        with patch("tripleten_cli.render._render_basic") as mock_basic_render:
            render_leaderboard(sample_leaderboard_data, "alice123")
            mock_basic_render.assert_called_once_with(
                sample_leaderboard_data, "alice123"
            )


class TestRenderWithRich:
    """Test suite for _render_with_rich function."""

    @pytest.fixture
    def sample_leaderboard_data(self):
        """Sample leaderboard data for testing."""
        return [
            {
                "rank": 1,
                "user": "Alice",
                "user_id": "alice123",
                "xp": 2500,
                "completed": 15,
                "streak": 10,
            },
            {
                "rank": 2,
                "user": "Bob",
                "user_id": "bob456",
                "xp": 2200,
                "completed": 12,
                "streak": 8,
            },
            {
                "rank": 3,
                "user": "Charlie",
                "user_id": "charlie789",
                "xp": 1980,
                "completed": 11,
                "streak": 6,
            },
        ]

    @pytest.mark.skipif(not RICH_AVAILABLE, reason="Rich library not available")
    def test_render_with_rich_creates_table(self, sample_leaderboard_data):
        """Test that _render_with_rich creates a proper table."""
        with patch("tripleten_cli.render.Console") as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            with patch("tripleten_cli.render.Table") as mock_table_class:
                mock_table = Mock()
                mock_table_class.return_value = mock_table

                _render_with_rich(sample_leaderboard_data, "alice123")

                # Verify table creation and configuration
                mock_table_class.assert_called_once_with(
                    show_header=True, header_style="bold magenta"
                )

                # Verify columns are added
                assert mock_table.add_column.call_count == 5

                # Verify rows are added (3 data rows)
                assert mock_table.add_row.call_count == 3

                # Verify console prints
                assert mock_console.print.call_count == 3

    @pytest.mark.skipif(not RICH_AVAILABLE, reason="Rich library not available")
    def test_render_with_rich_highlights_current_user(self, sample_leaderboard_data):
        """Test that _render_with_rich highlights the current user."""
        with patch("tripleten_cli.render.Console") as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            with patch("tripleten_cli.render.Table") as mock_table_class:
                mock_table = Mock()
                mock_table_class.return_value = mock_table

                with patch("tripleten_cli.render.Text") as mock_text_class:
                    _render_with_rich(sample_leaderboard_data, "alice123")

                    # Should create Text objects for highlighted user
                    assert (
                        mock_text_class.call_count >= 4
                    )  # At least 4 Text objects for current user row

    def test_get_rank_styled_text_gold(self):
        """Test rank styling for 1st place."""
        if not RICH_AVAILABLE:
            pytest.skip("Rich library not available")

        from tripleten_cli.render import Text

        styled_text = _get_rank_styled_text(1)

        assert isinstance(styled_text, Text)
        assert styled_text.style == "bold gold1"

    def test_get_rank_styled_text_silver(self):
        """Test rank styling for 2nd place."""
        if not RICH_AVAILABLE:
            pytest.skip("Rich library not available")

        from tripleten_cli.render import Text

        styled_text = _get_rank_styled_text(2)

        assert isinstance(styled_text, Text)
        assert styled_text.style == "bold bright_white"

    def test_get_rank_styled_text_bronze(self):
        """Test rank styling for 3rd place."""
        if not RICH_AVAILABLE:
            pytest.skip("Rich library not available")

        from tripleten_cli.render import Text

        styled_text = _get_rank_styled_text(3)

        assert isinstance(styled_text, Text)
        assert styled_text.style == "bold color(208)"

    def test_get_rank_styled_text_default(self):
        """Test rank styling for other places."""
        if not RICH_AVAILABLE:
            pytest.skip("Rich library not available")

        from tripleten_cli.render import Text

        styled_text = _get_rank_styled_text(5)

        assert isinstance(styled_text, Text)
        assert styled_text.style == "cyan"

    def test_render_with_rich_missing_data_fields(self):
        """Test _render_with_rich with missing data fields."""
        if not RICH_AVAILABLE:
            pytest.skip("Rich library not available")

        incomplete_data = [
            {"rank": 1, "user": "Alice"},  # Missing xp, completed, streak, user_id
            {"xp": 1500, "completed": 10},  # Missing rank, user, streak, user_id
        ]

        with patch("tripleten_cli.render.Console") as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            with patch("tripleten_cli.render.Table") as mock_table_class:
                mock_table = Mock()
                mock_table_class.return_value = mock_table

                # Should not raise exception
                _render_with_rich(incomplete_data, "alice123")

                # Should still add rows
                assert mock_table.add_row.call_count == 2


class TestRenderWithTabulate:
    """Test suite for _render_with_tabulate function."""

    @pytest.fixture
    def sample_leaderboard_data(self):
        """Sample leaderboard data for testing."""
        return [
            {
                "rank": 1,
                "user": "Alice",
                "user_id": "alice123",
                "xp": 2500,
                "completed": 15,
                "streak": 10,
            },
            {
                "rank": 2,
                "user": "Bob",
                "user_id": "bob456",
                "xp": 2200,
                "completed": 12,
                "streak": 8,
            },
            {
                "rank": 3,
                "user": "Charlie",
                "user_id": "charlie789",
                "xp": 1980,
                "completed": 11,
                "streak": 6,
            },
        ]

    @pytest.mark.skipif(not TABULATE_AVAILABLE, reason="Tabulate library not available")
    def test_render_with_tabulate_creates_table(self, sample_leaderboard_data):
        """Test that _render_with_tabulate creates a proper table."""
        with patch("tripleten_cli.render.tabulate") as mock_tabulate:
            mock_tabulate.return_value = "Mocked table output"

            with patch("builtins.print") as mock_print:
                _render_with_tabulate(sample_leaderboard_data, "alice123")

                # Verify tabulate is called with correct parameters
                mock_tabulate.assert_called_once()
                args, kwargs = mock_tabulate.call_args

                assert len(args[0]) == 3  # 3 data rows
                assert args[1] == ["Rank", "User", "XP", "Completed", "Streak"]
                assert kwargs.get("tablefmt") == "grid"

                # Verify print statements
                assert mock_print.call_count >= 3

    @pytest.mark.skipif(not TABULATE_AVAILABLE, reason="Tabulate library not available")
    def test_render_with_tabulate_highlights_current_user(
        self, sample_leaderboard_data
    ):
        """Test that _render_with_tabulate highlights the current user."""
        with patch("tripleten_cli.render.tabulate") as mock_tabulate:
            mock_tabulate.return_value = "Mocked table output"

            _render_with_tabulate(sample_leaderboard_data, "alice123")

            # Get the table data passed to tabulate
            args, _ = mock_tabulate.call_args
            table_data = args[0]

            # Check that Alice (current user) is highlighted with arrows
            alice_row = table_data[0]  # First row should be Alice
            assert "→ Alice ←" in alice_row[1]

    @pytest.mark.skipif(not TABULATE_AVAILABLE, reason="Tabulate library not available")
    def test_render_with_tabulate_rank_medals(self, sample_leaderboard_data):
        """Test that _render_with_tabulate adds medal emojis for top 3."""
        with patch("tripleten_cli.render.tabulate") as mock_tabulate:
            mock_tabulate.return_value = "Mocked table output"

            _render_with_tabulate(sample_leaderboard_data, "alice123")

            args, _ = mock_tabulate.call_args
            table_data = args[0]

            # Check medal emojis for top 3
            assert "🥇 1" in table_data[0][0]  # Gold for 1st
            assert "🥈 2" in table_data[1][0]  # Silver for 2nd
            assert "🥉 3" in table_data[2][0]  # Bronze for 3rd


class TestRenderBasic:
    """Test suite for _render_basic function."""

    @pytest.fixture
    def sample_leaderboard_data(self):
        """Sample leaderboard data for testing."""
        return [
            {
                "rank": 1,
                "user": "Alice",
                "user_id": "alice123",
                "xp": 2500,
                "completed": 15,
                "streak": 10,
            },
            {
                "rank": 2,
                "user": "Bob",
                "user_id": "bob456",
                "xp": 2200,
                "completed": 12,
                "streak": 8,
            },
        ]

    def test_render_basic_output_format(self, sample_leaderboard_data):
        """Test that _render_basic produces expected output format."""
        with patch("builtins.print") as mock_print:
            _render_basic(sample_leaderboard_data, "alice123")

            # Check that multiple print statements were made
            assert mock_print.call_count >= 5

            # Check specific content in print calls
            # Check if print was called with arguments
            print_calls = []
            for call in mock_print.call_args_list:
                if call.args:  # Check if there are positional arguments
                    print_calls.append(call.args[0])
                elif call.kwargs:  # Check if there are keyword arguments
                    print_calls.append(str(call.kwargs))

            # Header should be present
            assert any("🏆 Leaderboard" in call for call in print_calls)

            # Column headers should be present
            assert any("Rank" in call and "User" in call for call in print_calls)

    def test_render_basic_highlights_current_user(self, sample_leaderboard_data):
        """Test that _render_basic highlights the current user."""
        with patch("builtins.print") as mock_print:
            _render_basic(sample_leaderboard_data, "alice123")

            # Check if print was called with arguments
            print_calls = []
            for call in mock_print.call_args_list:
                if call.args:  # Check if there are positional arguments
                    print_calls.append(call.args[0])
                elif call.kwargs:  # Check if there are keyword arguments
                    print_calls.append(str(call.kwargs))

            # Check that Alice is highlighted with arrows
            assert any("→ Alice ←" in call for call in print_calls)

    def test_render_basic_rank_medals(self, sample_leaderboard_data):
        """Test that _render_basic adds medal emojis for top ranks."""
        sample_data_with_third = sample_leaderboard_data + [
            {
                "rank": 3,
                "user": "Charlie",
                "user_id": "charlie789",
                "xp": 1980,
                "completed": 11,
                "streak": 6,
            }
        ]

        with patch("builtins.print") as mock_print:
            _render_basic(sample_data_with_third, "alice123")

            # Check if print was called with arguments
            print_calls = []
            for call in mock_print.call_args_list:
                if call.args:  # Check if there are positional arguments
                    print_calls.append(call.args[0])
                elif call.kwargs:  # Check if there are keyword arguments
                    print_calls.append(str(call.kwargs))

            # Check for medal emojis
            assert any("🥇1" in call for call in print_calls)  # Gold for 1st
            assert any("🥈2" in call for call in print_calls)  # Silver for 2nd
            assert any("🥉3" in call for call in print_calls)  # Bronze for 3rd

    def test_render_basic_missing_fields(self):
        """Test _render_basic with missing data fields."""
        incomplete_data = [
            {"rank": 1, "user": "Alice"},  # Missing other fields
            {"xp": 1500, "completed": 10},  # Missing rank and user
        ]

        with patch("builtins.print") as mock_print:
            # Should not raise exception
            _render_basic(incomplete_data, "alice123")

            # Should still produce output
            assert mock_print.call_count >= 3


class TestRenderFromJsonFile:
    """Test suite for render_from_json_file function."""

    def test_render_from_json_file_valid_file(self, tmp_path):
        """Test rendering from valid JSON file."""
        # Create test JSON file
        json_data = {
            "leaderboard": [
                {
                    "rank": 1,
                    "user": "Alice",
                    "user_id": "alice123",
                    "xp": 2500,
                    "completed": 15,
                    "streak": 10,
                }
            ]
        }

        json_file = tmp_path / "test_leaderboard.json"
        with open(json_file, "w") as f:
            json.dump(json_data, f)

        with patch("tripleten_cli.render.render_leaderboard") as mock_render:
            render_from_json_file(str(json_file), "alice123")

            mock_render.assert_called_once_with(json_data["leaderboard"], "alice123")

    def test_render_from_json_file_list_format(self, tmp_path):
        """Test rendering from JSON file with list format."""
        json_data = [
            {
                "rank": 1,
                "user": "Alice",
                "user_id": "alice123",
                "xp": 2500,
                "completed": 15,
                "streak": 10,
            }
        ]

        json_file = tmp_path / "test_leaderboard.json"
        with open(json_file, "w") as f:
            json.dump(json_data, f)

        with patch("tripleten_cli.render.render_leaderboard") as mock_render:
            render_from_json_file(str(json_file), "alice123")

            mock_render.assert_called_once_with(json_data, "alice123")

    def test_render_from_json_file_users_format(self, tmp_path):
        """Test rendering from JSON file with 'users' key format."""
        json_data = {
            "users": [
                {
                    "rank": 1,
                    "user": "Alice",
                    "user_id": "alice123",
                    "xp": 2500,
                    "completed": 15,
                    "streak": 10,
                }
            ]
        }

        json_file = tmp_path / "test_leaderboard.json"
        with open(json_file, "w") as f:
            json.dump(json_data, f)

        with patch("tripleten_cli.render.render_leaderboard") as mock_render:
            render_from_json_file(str(json_file), "alice123")

            mock_render.assert_called_once_with(json_data["users"], "alice123")

    def test_render_from_json_file_not_found(self):
        """Test rendering from non-existent JSON file."""
        with patch("builtins.print") as mock_print:
            render_from_json_file("non_existent_file.json", "alice123")

            mock_print.assert_called_once()
            assert "not found" in mock_print.call_args[0][0]

    def test_render_from_json_file_invalid_json(self, tmp_path):
        """Test rendering from invalid JSON file."""
        json_file = tmp_path / "invalid.json"
        with open(json_file, "w") as f:
            f.write("invalid json content")

        with patch("builtins.print") as mock_print:
            render_from_json_file(str(json_file), "alice123")

            mock_print.assert_called_once()
            assert "Invalid JSON format" in mock_print.call_args[0][0]

    def test_render_from_json_file_single_dict(self, tmp_path):
        """Test rendering from JSON file with single dictionary."""
        json_data = {"rank": 1, "user": "Alice", "user_id": "alice123", "xp": 2500}

        json_file = tmp_path / "test_single.json"
        with open(json_file, "w") as f:
            json.dump(json_data, f)

        with patch("tripleten_cli.render.render_leaderboard") as mock_render:
            render_from_json_file(str(json_file), "alice123")

            mock_render.assert_called_once_with([json_data], "alice123")


class TestRenderFromJsonString:
    """Test suite for render_from_json_string function."""

    def test_render_from_json_string_valid(self):
        """Test rendering from valid JSON string."""
        json_data = {
            "leaderboard": [
                {"rank": 1, "user": "Alice", "user_id": "alice123", "xp": 2500}
            ]
        }
        json_string = json.dumps(json_data)

        with patch("tripleten_cli.render.render_leaderboard") as mock_render:
            render_from_json_string(json_string, "alice123")

            mock_render.assert_called_once_with(json_data["leaderboard"], "alice123")

    def test_render_from_json_string_list_format(self):
        """Test rendering from JSON string with list format."""
        json_data = [{"rank": 1, "user": "Alice", "user_id": "alice123", "xp": 2500}]
        json_string = json.dumps(json_data)

        with patch("tripleten_cli.render.render_leaderboard") as mock_render:
            render_from_json_string(json_string, "alice123")

            mock_render.assert_called_once_with(json_data, "alice123")

    def test_render_from_json_string_invalid(self):
        """Test rendering from invalid JSON string."""
        invalid_json = "invalid json content"

        with patch("builtins.print") as mock_print:
            render_from_json_string(invalid_json, "alice123")

            mock_print.assert_called_once()
            assert "Invalid JSON format" in mock_print.call_args[0][0]

    def test_render_from_json_string_exception_handling(self):
        """Test exception handling in render_from_json_string."""
        with patch("json.loads", side_effect=Exception("Test exception")):
            with patch("builtins.print") as mock_print:
                render_from_json_string('{"valid": "json"}', "alice123")

                mock_print.assert_called_once()
                assert "Error parsing leaderboard data" in mock_print.call_args[0][0]


class TestModuleImports:
    """Test module import handling."""

    def test_rich_availability(self):
        """Test RICH_AVAILABLE constant reflects actual import status."""
        try:
            import rich.console  # noqa: F401

            expected_available = True
        except ImportError:
            expected_available = False

        # Import the module and check the constant
        import tripleten_cli.render as render

        assert render.RICH_AVAILABLE == expected_available

    def test_tabulate_availability(self):
        """Test TABULATE_AVAILABLE constant reflects actual import status."""
        try:
            import tabulate  # noqa: F401

            expected_available = True
        except ImportError:
            expected_available = False

        import tripleten_cli.render as render

        assert render.TABULATE_AVAILABLE == expected_available

    def test_text_fallback_when_rich_unavailable(self):
        """Test Text class fallback when rich is not available."""
        # This test verifies the fallback Text class exists in the module
        import tripleten_cli.render as render

        # The Text class should always be available (either from rich or fallback)
        assert hasattr(render, "Text")


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_user_id(self):
        """Test rendering with empty user ID."""
        data = [{"rank": 1, "user": "Alice", "user_id": "alice123", "xp": 2500}]

        # Since rich is available, _render_with_rich should be called instead
        with patch("tripleten_cli.render.RICH_AVAILABLE", False):
            with patch("tripleten_cli.render.TABULATE_AVAILABLE", False):
                with patch("tripleten_cli.render._render_basic") as mock_render:
                    render_leaderboard(data, "")
                    mock_render.assert_called_once_with(data, "")

    def test_none_user_id(self):
        """Test rendering with None user ID."""
        data = [{"rank": 1, "user": "Alice", "user_id": "alice123", "xp": 2500}]

        # Since rich is available, _render_with_rich should be called instead
        with patch("tripleten_cli.render.RICH_AVAILABLE", False):
            with patch("tripleten_cli.render.TABULATE_AVAILABLE", False):
                with patch("tripleten_cli.render._render_basic") as mock_render:
                    render_leaderboard(data, None)
                    mock_render.assert_called_once_with(data, None)

    def test_malformed_leaderboard_entries(self):
        """Test rendering with malformed leaderboard entries."""
        malformed_data = [
            {"rank": "not_a_number", "user": None, "xp": "also_not_a_number"},
            {"incomplete": "entry"},
            None,  # Invalid entry
        ]

        # Should handle malformed data gracefully
        with patch("tripleten_cli.render.RICH_AVAILABLE", False):
            with patch("tripleten_cli.render.TABULATE_AVAILABLE", False):
                with patch("builtins.print"):
                    render_leaderboard(malformed_data, "test_user")

    def test_very_large_dataset(self):
        """Test rendering with large dataset."""
        large_data = []
        for i in range(1000):
            large_data.append(
                {
                    "rank": i + 1,
                    "user": f"User{i}",
                    "user_id": f"user{i}",
                    "xp": 2500 - i,
                    "completed": 15 - (i // 100),
                    "streak": 10 - (i // 200),
                }
            )

        # Should handle large datasets without issues
        with patch("builtins.print"):
            render_leaderboard(large_data, "user500")

    def test_unicode_characters_in_data(self):
        """Test rendering with Unicode characters in user names."""
        unicode_data = [
            {"rank": 1, "user": "Alice 🏆", "user_id": "alice123", "xp": 2500},
            {"rank": 2, "user": "Bob™", "user_id": "bob456", "xp": 2200},
            {"rank": 3, "user": "Charlotte", "user_id": "charlotte789", "xp": 1900},
        ]

        # Should handle Unicode characters without issues
        with patch("builtins.print"):
            render_leaderboard(unicode_data, "alice123")

    def test_extremely_long_usernames(self):
        """Test rendering with extremely long usernames."""
        long_name_data = [
            {
                "rank": 1,
                "user": "A" * 100,  # 100 character username
                "user_id": "alice123",
                "xp": 2500,
            }
        ]

        # Should handle long names without issues
        with patch("builtins.print"):
            render_leaderboard(long_name_data, "alice123")
