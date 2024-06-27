from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from apple_health_parser.utils.parser import Parser


@pytest.fixture
def xml_file() -> Path:
    """
    XML file path fixture.
    """
    return Path("tests/data/export.xml")


@pytest.fixture
def export_file() -> str:
    """
    Export zip file path fixture.
    """
    return "tests/data/export.zip"


@pytest.fixture
def root(xml_file: Path) -> ET.Element:
    """
    Root element fixture.
    This is the root element of the XML file.
    """
    with open(xml_file, "r") as file:
        return ET.parse(file).getroot()


@pytest.fixture
def parser(export_file: str, tmp_path: Path) -> Parser:
    """
    Parser fixture.
    This is the parser object that will be used in the tests.
    """
    return Parser(export_file=export_file, output_dir=tmp_path)
