import subprocess


def test_export_help():
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.export.main", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CLI to export data" in result.stdout


def test_year_recap_help():
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.recap.main", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CLI to export the year recap" in result.stdout


def test_export_without_args():
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.export.main"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Usage:" in result.stderr


def test_year_recap_without_args():
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.recap.main"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Usage:" in result.stderr


def test_export_invalid_option():
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.export.main", "--invalid-option"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_year_recap_invalid_option():
    result = subprocess.run(
        ["python", "-m", "apple_health_parser.scripts.recap.main", "--invalid-option"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
