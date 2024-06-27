from dataclasses import dataclass
from enum import Enum, StrEnum
from importlib import resources

import yaml


@dataclass
class Metadata:
    """
    Represents metadata for a specific data type in Apple Health.

    Attributes:
        name (str): The name of the data type
        unit (str): The unit of measurement for the data type
        color (str): The color associated with the data type
        colormap (str): The colormap associated with the data type
    """

    name: str
    unit: str
    color: str
    colormap: str


def get_flag_metadata() -> dict[str, Metadata]:
    """
    Get the metadata for each flag.

    Returns:
        dict[str, Metadata]: Dictionary of flag metadata with flag as key and Metadata as value
    """
    flags_file = resources.files("apple_health_parser.config") / "flags.yaml"
    flags_content = yaml.safe_load(flags_file.read_text())
    return {flag: Metadata(**metadata) for flag, metadata in flags_content.items()}


class AllowedImageFormats(StrEnum):
    HTML = "html"
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"
    SVG = "svg"
    PDF = "pdf"


class Operations(StrEnum):
    COUNT = "count"
    MAX = "max"
    MEAN = "mean"
    MEDIAN = "median"
    MIN = "min"
    SUM = "sum"


class PlotType(StrEnum):
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"
    HEATMAP = "imshow"


class OverviewType(Enum):
    ACTIVITY = [
        "HKQuantityTypeIdentifierActiveEnergyBurned",
        "HKQuantityTypeIdentifierAppleExerciseTime",
        "HKQuantityTypeIdentifierAppleStandTime",
    ]
    BODY = [
        "HKQuantityTypeIdentifierBodyMass",
        "HKQuantityTypeIdentifierBodyFatPercentage",
        "HKQuantityTypeIdentifierBodyMassIndex",
    ]


@dataclass
class PlotSettings:
    """
    Represents the settings for a plot.

    Attributes:
        x (str): The column name to be plotted on the x-axis
        y (str): The column name to be plotted on the y-axis
        color (str | None): The variable to determine the color of the plot (optional)
        colormap (str | None): The colormap to be used for coloring the plot (optional)
        legend (str | None): The title of the legend (optional)
        title (str | None): The title of the plot (optional)
        title_yaxis (str | None): The title of the y-axis (optional)
    """

    x: str
    y: str
    color: str | None
    colormap: str | None
    legend: str | None
    title: str | None
    title_yaxis: str | None
