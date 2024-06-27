import pandas as pd
import pytest

from apple_health_parser.exceptions import (
    InvalidOperation,
    InvalidSource,
    MissingYear,
)
from apple_health_parser.utils.parser import Parser
from apple_health_parser.utils.preprocessor import Preprocessor


class TestPreprocessor:
    def test_exceptions(self, parser: Parser) -> None:
        data = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        year = 2024
        source = "Alexandre's Apple Watch"
        operation = "sum"
        heatmap = False

        with pytest.raises(MissingYear):
            Preprocessor(
                data, year=2020, source=source, operation=operation, heatmap=heatmap
            )

        with pytest.raises(InvalidOperation):
            Preprocessor(
                data, year=year, source=source, operation="test", heatmap=heatmap
            )

        with pytest.raises(InvalidSource):
            Preprocessor(
                data,
                year=year,
                source="Invalid Source",
                operation=operation,
                heatmap=heatmap,
            )

    def test_get_dataframe(self, parser: Parser) -> None:
        data = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        year = 2024
        source = "Alexandre's Apple Watch"
        operation = "sum"
        heatmap = False
        preprocessor = Preprocessor(data, year, source, operation, heatmap)
        df = preprocessor.get_dataframe()

        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 2)

        heatmap = True
        preprocessor = Preprocessor(data, year, source, operation, heatmap)
        df = preprocessor.get_dataframe()
        assert df.shape == (1, 2)

    def test_get_heatmap(self, parser: Parser) -> None:
        data = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        year = 2024
        source = "Alexandre's Apple Watch"
        operation = "sum"
        heatmap = False
        preprocessor = Preprocessor(data, year, source, operation, heatmap)
        df = preprocessor.get_dataframe()
        heatmap = Preprocessor.get_heatmap(df)

        assert isinstance(heatmap, pd.DataFrame)
        assert heatmap.shape == (1, 2)
        assert heatmap.columns.name == "day"
        assert heatmap.index.name == "month"
