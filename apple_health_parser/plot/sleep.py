from datetime import datetime

from plotly.graph_objects import Figure, Scatter

from apple_health_parser.config.definitions import SleepColors
from apple_health_parser.interfaces.plot_interface import PlotInterface
from apple_health_parser.models.parsed import ParsedData
from apple_health_parser.models.records import SleepType


class SleepPlot(PlotInterface):
    """
    Plot the parsed sleep data.
    """

    def __init__(
        self, data: ParsedData, year: int, timerange: tuple[str, str] | None = None
    ):
        """
        Initialize the SleepPlot.

        Args:
            data (ParsedData): Parsed data object containing sleep records.
            year (int): Year for which the data is plotted.
            timerange (tuple, optional): Start and end date for the plot in ISO format.
                If provided, the data will be filtered to include only records within this range.
                Must be a tuple of two strings in ISO format (e.g. `("2024-03-01T20:00:00+00:00", "2024-03-02T08:00:00+00:00")`).
                Defaults to None, which means no filtering is applied.
        """
        super().__init__(data=data, year=year)

        if timerange is not None:
            # Validate timerange
            if not isinstance(timerange, tuple) or len(timerange) != 2:
                raise ValueError("timerange must be a tuple of two date strings.")
            if not all(isinstance(date, str) for date in timerange):
                raise ValueError(
                    "Both elements of timerange must be strings in ISO format."
                )

            # Convert strings to datetime objects
            start_dt, end_dt = (datetime.fromisoformat(date) for date in timerange)
            timerange_iso: tuple[datetime, datetime] = (start_dt, end_dt)

            # Filter the dataframe based on the timerange
            self.dataframe = self.dataframe[
                (self.dataframe["start_date"] >= timerange_iso[0])
                & (self.dataframe["end_date"] <= timerange_iso[1])
            ]

    def _get_figure(self) -> Figure:
        """
        Get the plotly figure for sleep data.

        Returns:
            Figure: Figure object
        """
        colors = {
            SleepType.IN_BED: SleepColors.in_bed,
            SleepType.AWAKE: SleepColors.awake,
            SleepType.CORE: SleepColors.core,
            SleepType.DEEP: SleepColors.deep,
            SleepType.REM: SleepColors.rem,
            SleepType.UNSPECIFIED: SleepColors.unset,
        }

        fig = Figure()
        for row in self.dataframe.itertuples():
            fig.add_trace(
                Scatter(
                    x=[row.start_date, row.end_date],
                    y=[row.value, row.value],
                    name=row.value,
                    showlegend=False,
                    mode="lines",
                    line_shape="hvh",
                    line=dict(
                        color=colors.get(SleepType(row.value), "black"), width=10
                    ),
                    hoverinfo="text",
                    hovertext=f"{row.start_date} - {row.end_date}<br>Sleep stage: {row.value}",
                )
            )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=self.psets.title_yaxis,
            legend_title_text=self.psets.legend,
            template="simple_white",
        )

        return fig
