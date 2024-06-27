from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from apple_health_parser.utils.loader import Loader


def test_extract_zip() -> None:
    with mock.patch("click.confirm", return_value=True):
        with TemporaryDirectory() as temp_dir:
            # Trigger deletion of previous export warning
            for _ in range(2):
                zip_path = Path(temp_dir) / "test.zip"

                with ZipFile(zip_path, "w") as zip_file:
                    zip_file.writestr("apple_health_export/export.xml", "test data")

                result = Loader.extract_zip(str(zip_path), temp_dir)
                expected = Path(temp_dir) / "apple_health_export/export.xml"

                assert result.resolve() == expected.resolve()
                assert result.exists()


@mock.patch("apple_health_parser.utils.loader.Loader._log_metadata")
def test_read_xml(mock_log_metadata, xml_file: Path) -> None:
    loader = Loader()
    result = loader.read_xml(xml_file=xml_file)
    mock_log_metadata.assert_called_once()

    assert isinstance(result, list)
    assert all(isinstance(item, ET.Element) for item in result)


@mock.patch("apple_health_parser.utils.logging.logger.info")
def test_log_metadata(mock_logger_info, xml_file: Path, root: ET.Element) -> None:
    with open(xml_file, "r") as _:
        Loader._log_metadata(root)
        mock_logger_info.assert_called()
        assert mock_logger_info.call_count == 7
