from datetime import date
from pathlib import Path
from unittest import mock
from xml.etree import ElementTree as ET

import pandas as pd
import pytest

from apple_health_parser.exceptions import (
    InvalidFileFormat,
    InvalidFlag,
    MissingRecords,
)
from apple_health_parser.models.parsed import ParsedData
from apple_health_parser.models.records import HealthData, HeartRateData
from apple_health_parser.utils.parser import Parser


class TestParser:
    def test_init(self, xml_file: str, export_file: str, tmp_path: Path) -> None:
        with mock.patch(
            "apple_health_parser.utils.loader.Loader.extract_zip",
            return_value=xml_file,
        ) as mock_extract_zip, mock.patch(
            "apple_health_parser.utils.parser.Parser._get_records", return_value=[]
        ) as mock_get_records:
            parser = Parser(export_file=export_file, output_dir=tmp_path)

            assert parser.xml_file == mock_extract_zip.return_value
            assert parser.records == mock_get_records.return_value

            mock_extract_zip.assert_called_once()
            mock_get_records.assert_called_once()

    def test_get_records(self, parser: Parser) -> None:
        expected_flags = [
            "HKQuantityTypeIdentifierHeartRate",
            "HKQuantityTypeIdentifierActiveEnergyBurned",
        ]
        records = parser._get_records()

        assert isinstance(records, dict)
        assert all(flag in records for flag in expected_flags)
        assert all(
            isinstance(rec, ET.Element)
            for rec_list in records.values()
            for rec in rec_list
        )

    def test_build_models(self, parser: Parser) -> None:
        heart_rate_models = parser._build_models("HKQuantityTypeIdentifierHeartRate")
        active_energy_models = parser._build_models(
            "HKQuantityTypeIdentifierActiveEnergyBurned"
        )
        with pytest.raises(InvalidFlag):
            parser._build_models("HKQuantityTypeIdentifierStepCount")

        assert len(heart_rate_models) == 1
        assert isinstance(heart_rate_models[0], HeartRateData)
        assert heart_rate_models[0].type == "HKQuantityTypeIdentifierHeartRate"
        assert heart_rate_models[0].value == 74
        assert heart_rate_models[0].unit == "count/min"
        assert heart_rate_models[0].motion_context == "Unset"
        assert heart_rate_models[0].source_version == "10.2"

        assert len(active_energy_models) == 2
        assert isinstance(active_energy_models[0], HealthData)
        assert (
            active_energy_models[0].type == "HKQuantityTypeIdentifierActiveEnergyBurned"
        )
        assert active_energy_models[0].value == 0.12
        assert active_energy_models[1].value == 0.08
        assert active_energy_models[0].unit == "kcal"
        assert active_energy_models[0].source_version == "10.2"

    def test_get_dates(self, parser: Parser) -> None:
        active_energy_models = parser._build_models(
            "HKQuantityTypeIdentifierActiveEnergyBurned"
        )
        dates = parser._get_dates(active_energy_models)
        actual_dates = {method() for method in dates}

        assert actual_dates == {date(2024, 1, 1), date(2024, 1, 2)}

    def test_map_record_keys_to_flags(self, parser: Parser) -> None:
        flags = [
            "HKCategoryTypeIdentifierSleepAnalysis",
            "HKQuantityTypeIdentifierActiveEnergyBurned",
            "HKQuantityTypeIdentifierAppleExerciseTime",
            "HKQuantityTypeIdentifierAppleStandTime",
            "HKQuantityTypeIdentifierHeartRate",
        ]
        record_keys = {
            "device",
            "type",
            "startDate",
            "value",
            "sourceName",
            "endDate",
            "creationDate",
            "sourceVersion",
            "unit",
        }
        flag_map = parser._map_record_keys_to_flags()
        # Check if the flags are in the flag_map
        assert sorted(flag_map.keys()) == flags
        # Check if the record keys are as expected
        assert all(record_keys == i for i in flag_map.values())

    def test_get_flag_records(self, parser: Parser) -> None:
        with mock.patch(
            "apple_health_parser.utils.parser.Parser._build_models"
        ) as mock_build_models, mock.patch(
            "apple_health_parser.utils.parser.Parser._get_dates"
        ) as mock_get_dates, mock.patch(
            "apple_health_parser.utils.parser.Parser.get_sources"
        ) as mock_get_sources:
            result = parser.get_flag_records("HKQuantityTypeIdentifierHeartRate")

            mock_get_dates.assert_called_once()
            mock_build_models.assert_called_once()
            mock_get_sources.assert_called_once()
            assert isinstance(result, ParsedData)

            result = parser.get_flag_records(
                [
                    "HKQuantityTypeIdentifierHeartRate",
                    "HKQuantityTypeIdentifierActiveEnergyBurned",
                ]
            )

            assert mock_get_dates.call_count == 3
            assert mock_build_models.call_count == 3
            assert mock_get_sources.call_count == 3
            assert isinstance(result, dict)

    def test_write_csv(self, parser: Parser) -> None:
        with mock.patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
            data = parser.get_flag_records("HKQuantityTypeIdentifierHeartRate")
            parser.write_csv(data=data, filename="test.csv")
            mock_to_csv.assert_called_once()

            with pytest.raises(InvalidFileFormat):
                parser.write_csv(data=data, filename="test.pdf")
                mock_to_csv.assert_not_called()

            data.records = None
            with pytest.raises(MissingRecords):
                parser.write_csv(data=data, filename="test.csv")
                mock_to_csv.assert_not_called()

    def test_export(self, parser: Parser, tmp_path: Path) -> None:
        with mock.patch(
            "apple_health_parser.utils.parser.Parser.get_flag_records"
        ) as mock_get_flag_records, mock.patch(
            "apple_health_parser.utils.parser.Parser.write_csv"
        ) as mock_write_csv:
            parser.export(dir_name=tmp_path)

            assert mock_get_flag_records.call_count == 5
            assert mock_write_csv.call_count == 5

    def test_parsed(self, parser: Parser) -> None:
        flag = "HKQuantityTypeIdentifierHeartRate"
        records = parser.get_flag_records(flag=flag)
        str_records = str(records)

        assert "ParsedData" in str_records
        assert flag in str_records
        assert all(
            item in str_records for item in ["Flag", "Sources", "Dates", "Records"]
        )
