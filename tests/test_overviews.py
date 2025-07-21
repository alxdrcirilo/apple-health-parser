from unittest import mock

import pytest
from plotly.graph_objs import Figure

from apple_health_parser.exceptions import (
    InvalidImageFormat,
    InvalidOverviewType,
    MissingFlag,
)
from apple_health_parser.plot.overviews import Overview
from apple_health_parser.utils.parser import Parser


@pytest.fixture
def flags() -> list[str]:
    return [
        "HKQuantityTypeIdentifierActiveEnergyBurned",
        "HKQuantityTypeIdentifierAppleExerciseTime",
        "HKQuantityTypeIdentifierAppleStandTime",
    ]


class TestOverviews:
    def test_validate(self, parser: Parser, flags: list[str]) -> None:
        records = parser.get_flag_records(flag=flags)

        with pytest.raises(InvalidOverviewType):
            Overview(data=records, overview_type="fake-overview", year=2024)

        with pytest.raises(MissingFlag):
            Overview(data=records, overview_type="body", year=2024)

    def test_get_figure(self, parser: Parser, flags: list[str]) -> None:
        records = parser.get_flag_records(flag=flags)

        overview = Overview(data=records, overview_type="activity", year=2024)
        fig = overview._get_figure()
        assert isinstance(fig, Figure)

    def test_plot(self, parser: Parser, flags: list[str]) -> None:
        records = parser.get_flag_records(flag=flags)

        overview = Overview(data=records, overview_type="activity", year=2024)
        fig = overview.plot(show=False, save=False)
        assert isinstance(fig, Figure)

        with mock.patch("plotly.graph_objs.Figure.show") as mock_show, mock.patch(
            "plotly.graph_objs.Figure.write_html"
        ) as mock_write_html, mock.patch(
            "plotly.graph_objs.Figure.write_image"
        ) as mock_write_image:
            overview.plot(show=True, save=False)
            mock_show.assert_called_once()

            overview.plot(show=False, save=True, format="html")
            mock_write_html.assert_called_once()

            overview.plot(show=False, save=True, format="png")
            mock_write_image.assert_called_once()

    def test_plot_invalid_image_format(self, parser: Parser, flags: list[str]) -> None:
        records = parser.get_flag_records(flag=flags)

        overview = Overview(data=records, overview_type="activity", year=2024)
        fmt = "tiff"
        with pytest.raises(InvalidImageFormat):
            overview.plot(show=False, save=True, format=fmt)
