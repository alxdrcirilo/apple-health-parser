from apple_health_parser.consts import ALLOWED_IMAGE_FORMATS, OPERATIONS, OVERVIEW_TYPES


class MissingFlag(Exception):
    """
    Exception to raise when the flag is missing.
    """

    def __init__(self, flag: str) -> None:
        super().__init__(f"Flag '{flag}' is missing in the data.")


class MissingRecords(Exception):
    """
    Exception to raise when records are missing.
    """

    def __init__(self) -> None:
        super().__init__("No records found in the data.")


class MissingYear(Exception):
    """
    Exception to raise when there is no record for the given year.
    """

    def __init__(self, year: int, years: list[int]) -> None:
        super().__init__(f"No record for the year {year}. Available years: {years}.")


class InvalidFileFormat(Exception):
    """
    Exception to raise when the file type is incorrect.
    """

    def __init__(self, format: str) -> None:
        super().__init__(
            f"File type is incorrect. Requires .csv, but provided {format}."
        )


class InvalidFlag(Exception):
    """
    Exception to raise when the flag is incorrect.
    """

    def __init__(self, flag: str, flags: list[str]) -> None:
        super().__init__(f"Flag '{flag}' is not valid. Allowed flags: {flags}.")


class InvalidHeatmapOperation(Exception):
    """
    Exception to raise when the operation is invalid for a heatmap (i.e. when operation is `None`).
    """

    def __init__(self) -> None:
        super().__init__(
            f"Heatmaps require an operation. Allowed operations: {OPERATIONS}."
        )


class InvalidImageFormat(Exception):
    """
    Exception to raise when the image format is incorrect.
    """

    def __init__(self, format: str) -> None:
        super().__init__(
            f"Incorrect image format: '{format}'. Allowed formats: {ALLOWED_IMAGE_FORMATS}."
        )


class InvalidOperation(Exception):
    """
    Exception to raise when the operation is invalid.
    """

    def __init__(self, operation: str | None) -> None:
        super().__init__(
            f"Operation '{operation}' is invalid. Allowed operations: {OPERATIONS}."
        )


class InvalidOverviewType(Exception):
    """
    Exception to raise when the overview type is invalid.
    """

    def __init__(self, overview_type: str) -> None:
        super().__init__(
            f"Flag '{overview_type}' is invalid. Allowed overview types: {OVERVIEW_TYPES}."
        )


class InvalidSource(Exception):
    """
    Exception to raise when the source is missing.
    """

    def __init__(self, source: str, sources: list[str]) -> None:
        super().__init__(
            f"No records found for '{source}'. Available sources: {sources}."
        )
