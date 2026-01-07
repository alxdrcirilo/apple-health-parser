from unittest import mock

import pytest
from plotly.graph_objs import Figure

from apple_health_parser.exceptions import InvalidImageFormat
from apple_health_parser.plot.sleep import SleepPlot
from apple_health_parser.utils.parser import Parser


class TestSleepPlot:
    def test_get_figure(self, parser: Parser) -> None:
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        plot = SleepPlot(data=records, year=2024)
        fig = plot._get_figure()
        assert isinstance(fig, Figure)

    def test_plot(self, parser: Parser) -> None:
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        plot = SleepPlot(data=records, year=2024)
        fig = plot.plot(show=False, save=False)
        assert isinstance(fig, Figure)

        with (
            mock.patch("plotly.graph_objs.Figure.show") as mock_show,
            mock.patch("plotly.graph_objs.Figure.write_html") as mock_write_html,
            mock.patch("plotly.graph_objs.Figure.write_image") as mock_write_image,
        ):
            plot.plot(show=True, save=False)
            mock_show.assert_called_once()

            plot.plot(show=False, save=True, format="html")
            mock_write_html.assert_called_once()

            plot.plot(show=False, save=True, format="png")
            mock_write_image.assert_called_once()

    def test_plot_invalid_image_format(self, parser: Parser) -> None:
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        overview = SleepPlot(data=records, year=2024)
        fmt = "tiff"
        with pytest.raises(InvalidImageFormat):
            overview.plot(show=False, save=True, format=fmt)
