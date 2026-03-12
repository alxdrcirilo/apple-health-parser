from dataclasses import dataclass
from importlib import resources

import yaml

from apple_health_parser.config.definitions import Operations, PlotType


@dataclass(frozen=False)
class MetricDefinition:
    """
    Dataclass to hold the metadata for each health metric, including:
        - `axis_label`: The label for the y-axis in plots
        - `color`: The color to use for the metric in plots
        - `description`: A brief description of the metric
        - `flag`: The unique identifier for the metric in the Apple Health data
        - `marker_color`: The color to use for markers in plots
        - `name`: A human-readable name for the metric
        - `operation`: The type of aggregation operation to perform (e.g. sum, mean)
        - `plot_type`: The type of plot to use for the metric (e.g. bar, line)
        - `summary_template`: The template for summarizing the metric
        - `unit`: The unit of measurement for the metric (e.g. "km", "min")
    """

    axis_label: str
    color: str
    description: str
    flag: str
    marker_color: str
    name: str
    operation: Operations
    plot_type: PlotType
    summary_template: str
    unit: str


metrics_file = (
    resources.files("apple_health_parser.scripts.recap.metrics") / "metrics.yaml"
)
metrics_content = yaml.safe_load(metrics_file.read_text())
METRIC_DEFINITIONS: dict[str, MetricDefinition] = {
    flag: MetricDefinition(**metadata) for flag, metadata in metrics_content.items()
}
