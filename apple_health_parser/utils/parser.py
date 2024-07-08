import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import click
import pandas as pd
from pydantic import ValidationError

from apple_health_parser.decorators import timeit
from apple_health_parser.exceptions import (
    InvalidFileFormat,
    InvalidFlag,
    MissingRecords,
)
from apple_health_parser.models.parsed import ParsedData
from apple_health_parser.models.records import HealthData, HeartRateData
from apple_health_parser.utils.loader import Loader
from apple_health_parser.utils.logging import logger

# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
pd.options.mode.copy_on_write = True


class Parser(Loader):
    """
    Parser class to parse the Apple Health export file.

    Subclass of the Loader class which extracts the export.zip file and logs metadata.
    """

    def __init__(
        self,
        export_file: str | Path,
        output_dir: str | Path = "data",
        verbose: bool = False,
        overwrite: bool | None = None,
    ) -> None:
        """
        Initialize the Parser class with the path to the export.zip file.

        Args:
            export_file (str): Path to the export.zip file
            output_dir (str): Directory to export the parsed data to, defaults to "data"
            verbose (bool): Flag to enable verbose logging, defaults to False
            overwrite (bool, optional): Flag to overwrite the existing data, defaults to None
        """
        if verbose is False:
            logger.propagate = False

        self.xml_file = self.extract_zip(
            zip_file=export_file, output_dir=output_dir, overwrite=overwrite
        )
        self.records = self._get_records()
        self.sources = self.get_sources()

    @timeit
    def _get_records(self) -> dict[str, list[ET.Element]]:
        """
        Get records from the Apple Health export file.
        The records are grouped by flags as keys and list of records as values.

        Returns:
            dict[str, list[ET.Element]]: Records from the export.xml file
        """
        data = self.read_xml(self.xml_file)

        self.flags = self._get_flags(data)
        records = {
            flag: [rec for rec in data if rec.attrib["type"] == flag]
            for flag in self.flags
        }

        record_count = sum(len(rec) for rec in records.values())
        logger.info(
            f"Processed {len(records.keys())} flags with {record_count:,} records"
        )

        return records

    def _get_flags(self, data: list[ET.Element]) -> list[str]:
        """
        Get flags from the Apple Health records.

        Args:
            data (list[ET.Element]): List of records from the export.xml file

        Returns:
            list[str]: Sorted list of flags
        """
        return sorted({rec.attrib["type"] for rec in data})

    def _build_models(self, flag: str) -> list:
        """
        Build models from the records based on the flag.

        Args:
            flag (str): Flag to parse the records

        Returns:
            list: List of models based on the flag
        """
        logger.info(f"Parsing records with flag: {click.style(flag, fg='magenta')}")

        if flag not in self.flags:
            raise InvalidFlag(flag, self.flags)

        models: list[HealthData | HeartRateData] = []
        failed: dict[str, int] = {}

        for rec in self.records[flag]:
            try:
                # Heart rate records have additional metadata (motionContext)
                if flag == "HKQuantityTypeIdentifierHeartRate":
                    models.append(
                        HeartRateData(
                            **{
                                **rec.attrib,
                                **{
                                    "motionContext": rec.find("MetadataEntry").attrib[
                                        "value"
                                    ]
                                },
                            }
                        )
                    )
                else:
                    models.append(HealthData(**rec.attrib))

            except ValidationError as exc:
                error_type = exc.errors()[0]["type"]
                loc = exc.errors()[0]["loc"]
                try:
                    failed[f"{error_type}_{loc}"] += 1
                except KeyError:
                    failed[f"{error_type}_{loc}"] = 1
                continue

        if failed:
            logger.warning(
                click.style(f"Failed to parse {len(failed)} records", bold=True)
            )

        return models

    def _get_dates(self, models: list) -> set[date]:
        """
        Get unique month and year combinations from the models.

        Args:
            models (list): List of models

        Returns:
            set[datetime.date]: Set of dates (year, month, day)
        """
        return {rec.start_date.date for rec in models}

    def _map_record_keys_to_flags(self) -> dict[str, set]:
        """
        Map record keys (e.g. `unit`, `value`, `creationDate`) for each flag.

        For example:

        ```python
        HKCategoryTypeIdentifierAppleStandHour         {('type', 'sourceName', 'sourceVersion', 'device', ...)}
        HKCategoryTypeIdentifierAudioExposureEvent     {('type', 'sourceName', 'sourceVersion', 'device', ...)}
        HKDataTypeSleepDurationGoal                    {('type', 'sourceName', 'sourceVersion', 'unit', ...)}
        HKQuantityTypeIdentifierActiveEnergyBurned     {('type', 'sourceName', 'sourceVersion', 'device', ...)}
        ```

        Returns:
            dict[str, set]: Dictionary with flags as keys and set of record keys as values
        """
        return {
            flag: {tuple(rec.attrib.keys()) for rec in self.records[flag]}
            for flag in self.flags
        }

    @timeit
    def get_flag_records(
        self, flag: str | list[str]
    ) -> ParsedData | dict[str, ParsedData]:
        """
        Get parsed data based on the given flag.

        Args:
            flag (str | list[str]): Flag to parse the records (e.g., `"HKQuantityTypeIdentifierHeartRate"`)

        Returns:
            ParsedData | dict[str, ParsedData]: Parsed data based on the flag(s)
        """

        def _get_parsed_data(flag: str) -> ParsedData:
            sources = self.get_sources(flag=flag)
            models = self._build_models(flag=flag)
            dates = self._get_dates(models=models)
            records = pd.DataFrame([model.model_dump() for model in models])
            return ParsedData(flag=flag, sources=sources, dates=dates, records=records)

        if isinstance(flag, str):
            return _get_parsed_data(flag=flag)

        elif isinstance(flag, list):
            return {f: _get_parsed_data(flag=f) for f in flag}

    def get_sources(self, flag: str | None = None) -> list[str] | dict[str, list[str]]:
        """
        Get sources for each flag or for a given flag.

        Args:
            flag (str, optional): Get sources for the given flag, defaults to None

        Returns:
            list[str] | dict[str, list[str]]: Dictionary with flags as keys and list of sources as values
        """
        if flag:
            return sorted({rec.attrib["sourceName"] for rec in self.records[flag]})
        else:
            return {
                flag: sorted({rec.attrib["sourceName"] for rec in self.records[flag]})
                for flag in self.flags
            }

    @staticmethod
    def write_csv(data: ParsedData, filename: str) -> None:
        """
        Write the parsed data to a CSV file.

        Args:
            data (ParsedData): Parsed data to write to CSV file
            filename (str): Filename to write the data

        Raises:
            RecordsMissing: No records to write to CSV file
            FileTypeInvalid: File type is incorrect
        """
        if data.records is None:
            raise MissingRecords

        filepath = Path(filename)
        if filepath.suffix != ".csv":
            raise InvalidFileFormat(filepath.suffix)

        data.records.to_csv(filepath, index=False)
        logger.info(f"Parsed data written to {filepath}")

    @timeit
    def export(self, dir_name: str) -> None:
        """
        Export all parsed data to multiple CSV files.

        Args:
            dir_name (str): Directory name to export the CSV files
        """
        export_dir = Path(dir_name)
        export_dir.mkdir(exist_ok=True)

        logger.info(f"Exporting parsed data to {export_dir}...")

        for n, flag in enumerate(self.flags):
            try:
                parsed = self.get_flag_records(flag=flag)
            except Exception:
                logger.error(f"Error parsing {flag=}")
                continue

            filename = f"{dir_name}/{flag}.csv"
            self.write_csv(data=parsed, filename=filename)

            logger.info(f"Exported {n+1}/{len(self.flags)} flags to {filename}")
