"""Tests for the CLI module."""

from datetime import date
from pathlib import Path
from unittest import mock

import pytest
from click.testing import CliRunner

from apple_health_parser.scripts.main import main


class TestCLI:
    """Tests for the CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """CLI runner fixture."""
        return CliRunner()

    @pytest.fixture
    def export_file(self) -> str:
        """Export zip file path fixture."""
        return "tests/data/export.zip"

    def test_cli_help(self, runner: CliRunner) -> None:
        """Test CLI --help output shows all options."""
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "--zip_file" in result.output
        assert "--year" in result.output
        assert "--source" in result.output
        assert "Path to the Apple Health export.zip file" in result.output

    def test_cli_missing_zip_file(self, runner: CliRunner) -> None:
        """Test CLI fails when --zip_file is not provided."""
        result = runner.invoke(main, [])

        assert result.exit_code != 0

    def test_cli_with_default_options(
        self, runner: CliRunner, export_file: str, tmp_path: Path
    ) -> None:
        """Test CLI runs with default year (current) and source (all)."""
        with (
            mock.patch("apple_health_parser.scripts.main.Parser") as mock_parser_class,
            mock.patch("apple_health_parser.scripts.main.Plot") as mock_plot_class,
            mock.patch(
                "apple_health_parser.scripts.main.Overview"
            ) as mock_overview_class,
        ):
            mock_parser = mock.MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_plot = mock.MagicMock()
            mock_plot_class.return_value = mock_plot
            mock_overview = mock.MagicMock()
            mock_overview_class.return_value = mock_overview

            result = runner.invoke(main, ["--zip_file", export_file])

            assert result.exit_code == 0
            mock_parser_class.assert_called_once_with(
                export_file=export_file, overwrite=True, verbose=True
            )
            # Verify Plot was called with default year and source=None
            mock_plot_class.assert_called_once()
            call_kwargs = mock_plot_class.call_args[1]
            assert call_kwargs["year"] == date.today().year
            assert call_kwargs["source"] is None

    def test_cli_with_custom_year(
        self, runner: CliRunner, export_file: str, tmp_path: Path
    ) -> None:
        """Test CLI with custom --year option."""
        with (
            mock.patch("apple_health_parser.scripts.main.Parser") as mock_parser_class,
            mock.patch("apple_health_parser.scripts.main.Plot") as mock_plot_class,
            mock.patch(
                "apple_health_parser.scripts.main.Overview"
            ) as mock_overview_class,
        ):
            mock_parser = mock.MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_plot = mock.MagicMock()
            mock_plot_class.return_value = mock_plot
            mock_overview = mock.MagicMock()
            mock_overview_class.return_value = mock_overview

            result = runner.invoke(main, ["--zip_file", export_file, "--year", "2024"])

            assert result.exit_code == 0
            # Verify Plot was called with year=2024
            mock_plot_class.assert_called_once()
            call_kwargs = mock_plot_class.call_args[1]
            assert call_kwargs["year"] == 2024

    def test_cli_with_custom_source(
        self, runner: CliRunner, export_file: str, tmp_path: Path
    ) -> None:
        """Test CLI with custom --source option."""
        source = "Test Apple Watch"
        with (
            mock.patch("apple_health_parser.scripts.main.Parser") as mock_parser_class,
            mock.patch("apple_health_parser.scripts.main.Plot") as mock_plot_class,
            mock.patch(
                "apple_health_parser.scripts.main.Overview"
            ) as mock_overview_class,
        ):
            mock_parser = mock.MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_plot = mock.MagicMock()
            mock_plot_class.return_value = mock_plot
            mock_overview = mock.MagicMock()
            mock_overview_class.return_value = mock_overview

            result = runner.invoke(
                main, ["--zip_file", export_file, "--source", source]
            )

            assert result.exit_code == 0
            # Verify Plot was called with the custom source
            mock_plot_class.assert_called_once()
            call_kwargs = mock_plot_class.call_args[1]
            assert call_kwargs["source"] == source

    def test_cli_with_all_options(
        self, runner: CliRunner, export_file: str, tmp_path: Path
    ) -> None:
        """Test CLI with all custom options."""
        source = "Test Apple Watch"
        year = 2023
        with (
            mock.patch("apple_health_parser.scripts.main.Parser") as mock_parser_class,
            mock.patch("apple_health_parser.scripts.main.Plot") as mock_plot_class,
            mock.patch(
                "apple_health_parser.scripts.main.Overview"
            ) as mock_overview_class,
        ):
            mock_parser = mock.MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_plot = mock.MagicMock()
            mock_plot_class.return_value = mock_plot
            mock_overview = mock.MagicMock()
            mock_overview_class.return_value = mock_overview

            result = runner.invoke(
                main,
                [
                    "--zip_file",
                    export_file,
                    "--year",
                    str(year),
                    "--source",
                    source,
                ],
            )

            assert result.exit_code == 0
            # Verify Plot was called with correct options
            mock_plot_class.assert_called_once()
            call_kwargs = mock_plot_class.call_args[1]
            assert call_kwargs["year"] == year
            assert call_kwargs["source"] == source
            # Verify Overview was called with correct options
            mock_overview_class.assert_called_once()
            overview_kwargs = mock_overview_class.call_args[1]
            assert overview_kwargs["year"] == year
            assert overview_kwargs["source"] == source

    def test_cli_overview_uses_correct_flags(
        self, runner: CliRunner, export_file: str
    ) -> None:
        """Test CLI requests correct flags for activity overview."""
        with (
            mock.patch("apple_health_parser.scripts.main.Parser") as mock_parser_class,
            mock.patch("apple_health_parser.scripts.main.Plot") as mock_plot_class,
            mock.patch(
                "apple_health_parser.scripts.main.Overview"
            ) as mock_overview_class,
        ):
            mock_parser = mock.MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_plot = mock.MagicMock()
            mock_plot_class.return_value = mock_plot
            mock_overview = mock.MagicMock()
            mock_overview_class.return_value = mock_overview

            result = runner.invoke(main, ["--zip_file", export_file])

            assert result.exit_code == 0
            # Check that get_flag_records was called with the activity flags
            calls = mock_parser.get_flag_records.call_args_list
            assert len(calls) == 2  # Once for distance, once for activity overview

            # Second call should be for activity overview flags
            activity_flags_call = calls[1]
            activity_flags = activity_flags_call[1]["flag"]
            assert "HKQuantityTypeIdentifierActiveEnergyBurned" in activity_flags
            assert "HKQuantityTypeIdentifierAppleExerciseTime" in activity_flags
            assert "HKQuantityTypeIdentifierAppleStandTime" in activity_flags
