import click
import pandas as pd

from apple_health_parser.interfaces.preprocessor_interface import PreprocessorInterface
from apple_health_parser.utils.logging import logger


class Preprocessor(PreprocessorInterface):
    """
    Preprocess the parsed data.

    Additional steps:
    - Validate `flag`, `source`, `operation`, and `year`
    - Filter the records for the given year (e.g. `2024`)
    - Apply the operation to the data if provided (e.g. `"mean"` or `"sum"`)
    """

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the preprocessed data in a DataFrame.

        Filter the records for the given year (e.g. `2024`).
        Apply the operation to the data if provided (e.g. `"mean"` or `"sum"`).

        For example, using the `"sum"` operation:

        ```bash
        date        value
        2024-01-01  10.0
        2024-01-02  15.0
        2024-01-03  7.0
        2024-02-01  14.0
        2024-02-02  15.0
        ...         ...
        ```

        Returns:
            pd.DataFrame: DataFrame with the preprocessed data
        """
        self.records = self.data.records

        # Filter by source (e.g. "Apple Watch" or "iPhone")
        if self.src:
            self.records = self.records[self.records.source_name == self.src]

        # Filter by year (e.g. 2024)
        self.records["date"] = self.records.start_date.dt.date
        self.records = self.records[
            self.records.date.apply(lambda x: x.year == self.year)
        ]

        # TODO: Handle other flags with special cases
        # Special case for HKQuantityTypeIdentifierOxygenSaturation (convert to percentage)
        if self.flag == "HKQuantityTypeIdentifierOxygenSaturation":
            self.records.value *= 100

        # Apply operation (e.g. "mean" or "sum")
        if self.oper:
            self.records = (
                self.records.groupby("date")["value"]
                .apply(getattr(pd.Series, self.oper))
                .round()
                .reset_index()
            )

            logger.info(
                f"Found {len(self.records)} records "
                f"(flag: {click.style(self.flag, fg='magenta')}, "
                f"operation: {click.style(self.oper, fg='blue')}, "
                f"year: {click.style(self.year, fg='green')})"
            )

            # Return heatmap data if requested
            if self.hmap:
                return self.get_heatmap(self.records)

        else:
            logger.info(
                f"Found {len(self.records)} records "
                f"(flag: {click.style(self.flag, fg='magenta')}, "
                f"year: {click.style(self.year, fg='green')})"
            )

        return self.records

    @staticmethod
    def get_heatmap(data: pd.DataFrame) -> pd.DataFrame:
        """
        Get the heatmap data.

        For example:

        ```bash
        day       1          2          3          4          5         ...
        month
        1        84.944151  76.080932  67.496200  88.942571  84.944151  ...
        2        84.944151  76.080932  67.496200  88.942571  84.944151  ...
        3        84.944151  76.080932  67.496200  88.942571  84.944151  ...
        ```

        Returns:
            pd.DataFrame: Heatmap data
        """
        data["month"] = data.date.apply(lambda x: x.month)
        data["day"] = data.date.apply(lambda x: x.day)
        heatmap = data.pivot(index="month", columns="day", values="value")
        return heatmap
