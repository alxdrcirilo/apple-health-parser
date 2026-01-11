import subprocess


def test_cli_help():
    """Very simple test - just check that CLI help works without errors."""
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.main", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CLI to export data" in result.stdout


def test_cli_without_args():
    """Test CLI shows help when no arguments provided."""
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.main"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout


def test_cli_invalid_option():
    """Test CLI handles invalid options gracefully."""
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.main", "--invalid-option"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
