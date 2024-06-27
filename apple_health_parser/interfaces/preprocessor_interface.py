from abc import ABC, abstractmethod

import pandas as pd

from apple_health_parser.config.definitions import Metadata
from apple_health_parser.consts import FLAG_METADATA, OPERATIONS
from apple_health_parser.exceptions import (
    InvalidHeatmapOperation,
    InvalidOperation,
    InvalidSource,
    MissingFlag,
    MissingYear,
)
from apple_health_parser.models.parsed import ParsedData


class PreprocessorInterface(ABC):
    def __init__(
        self,
        data: ParsedData,
        year: int,
        source: str | None = None,
        operation: str | None = None,
        heatmap: bool = False,
    ) -> None:
        """
        Initialize the Preprocessor object.

        Prepare the DataFrame for the plot.

        Args:
            data (ParsedData): ParsedData object
            year (int, optional): Year, defaults to date.today().year
            source (str | None, optional): Source, defaults to None
            operation (str | None, optional): Operation, defaults to None
            heatmap (bool, optional): Flag to plot a heatmap, defaults to False
        """
        self.src = source
        self.data = data
        self.year = year
        self.oper = operation
        self.hmap = heatmap
        self.flag = data.flag
        self._validate()

    @property
    def meta(self) -> Metadata:
        """
        Metadata for the flag.

        Raises:
            MissingFlag: Missing flag metadata

        Returns:
            Metadata: Metadata for the flag
        """
        metadata = FLAG_METADATA.get(self.flag)
        if metadata is None:
            raise MissingFlag(self.flag)
        return metadata

    def _validate(self) -> None:
        """
        Validate the flag, operation, and year.

        Raises:
            MissingYear: Missing year in the records
            InvalidOperation: Invalid operation
            InvalidHeatmapOperation: Invalid operation for heatmap
            InvalidSource: Invalid source name
        """
        years = self.data.records.start_date.dt.year.unique().tolist()
        if self.year not in years:
            raise MissingYear(self.year, years)

        if self.oper is not None:
            if self.oper not in OPERATIONS:
                raise InvalidOperation(self.oper)
        else:
            if self.hmap:
                raise InvalidHeatmapOperation

        sources = self.data.records.source_name.unique()
        if self.src and self.src not in sources:
            raise InvalidSource(self.src, sources)

    @abstractmethod
    def get_heatmap(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        pass
