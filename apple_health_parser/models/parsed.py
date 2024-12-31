from dataclasses import dataclass
from datetime import date

import pandas as pd


@dataclass
class ParsedData:
    """
    Dataclass to store parsed data from the Apple Health export file.
    """

    flag: str
    sources: list[str]
    devices: list[str]
    dates: set[date]
    records: pd.DataFrame

    def __str__(self) -> str:
        """
        String representation of the ParsedData class.
        Includes the flag, sources, devices, dates, and number of records.

        Example:
        ```bash
        =====================ParsedData=====================
        Flag:       HKQuantityTypeIdentifierRestingHeartRate
        Sources:    3 sources
        Devices:    8 devices
        Dates:      144 dates
        Records:    145 records
        ```

        Returns:
            str: String representation of the ParsedData class
        """

        description = [
            f"{'Flag:':<12}{self.flag}",
            f"{'Sources:':<12}{len(self.sources)} sources",
            f"{'Devices:':<12}{len(self.devices)} devices",
            f"{'Dates:':<12}{len(self.dates)} dates",
            f"{'Records:':<12}{len(self.records)} records",
        ]

        max_len = len(max(description, key=len))
        description = [f"{'ParsedData':=^{max_len}}"] + description

        return "\n".join(description)
