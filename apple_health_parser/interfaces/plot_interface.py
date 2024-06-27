from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path

from plotly.graph_objs import Figure

from apple_health_parser.config.definitions import AllowedImageFormats, PlotSettings
from apple_health_parser.consts import Operations, PlotType
from apple_health_parser.exceptions import InvalidImageFormat
from apple_health_parser.models.parsed import ParsedData
from apple_health_parser.utils.preprocessor import Preprocessor


class PlotInterface(ABC):
    def __init__(
        self,
        data: ParsedData,
        year: int = date.today().year,
        source: str | None = None,
        operation: str | None = None,
        heatmap: bool = False,
        title: bool = False,
    ) -> None:
        """
        Initialize the Plot object.

        Setup the plot after preprocessing the data.

        Args:
            data (ParsedData): ParsedData object
            year (int, optional): Year, defaults to date.today().year
            source (str | None, optional): Source, defaults to None
            operation (str | None, optional): Operation, defaults to None
            heatmap (bool, optional): Flag to plot a heatmap, defaults to False
            title (bool, optional): Flag to include the plot title, defaults to False
        """
        self.src = source
        self.data = data
        self.year = year
        self.oper = operation
        self.hmap = heatmap
        self.title = title
        self.flag = data.flag

        preprocessor = Preprocessor(
            data=data, year=year, source=source, operation=operation, heatmap=heatmap
        )
        self.dataframe = preprocessor.get_dataframe()
        self.meta = preprocessor.meta

        # Plot type after preprocessor due to validity checks in preprocessor
        self.ptype: PlotType = self._get_plot_type()
        self.psets: PlotSettings = self._get_plot_settings()

    def _get_plot_settings(self) -> PlotSettings:
        """
        Get the plot settings.

        For the heart rate flag, the x-axis is "start_date" and the y-axis is "value".
        It also includes the color as "motion_context" and the legend as "Motion Context".

        Returns:
            PlotSettings: Plot settings
        """
        color = None
        colormap = None
        legend = None
        title = None
        title_yaxis = None

        # Special case for the heart rate flag ot include the motion context
        if self.flag == "HKQuantityTypeIdentifierHeartRate" and self.oper is None:
            x = "start_date"
            y = "value"
            color = "motion_context"
            legend = "Motion Context"
        else:
            x = "date"
            y = "value"

        match self.title:
            case True:
                title = (
                    f"{self.meta.name} {self.year}"
                    f"{' (' + self.oper + ')' if self.oper else ''}"
                    f"{': ' + self.src if self.src else ''}"
                )

        match self.ptype:
            case PlotType.HEATMAP:
                colormap = self.meta.colormap
            case _:
                title_yaxis = f"{self.meta.name} {self.meta.unit} ({self.oper})"

        return PlotSettings(x, y, color, colormap, legend, title, title_yaxis)

    def _get_plot_type(self) -> PlotType:
        """
        Get the plot type based on the operation and whether a heatmap is requested.

        Returns:
            PlotType: Plot type
        """
        match self.hmap:
            case True:
                return PlotType.HEATMAP
            case False:
                match self.oper:
                    case Operations.COUNT | Operations.SUM:
                        return PlotType.BAR
                    case (
                        Operations.MAX
                        | Operations.MEAN
                        | Operations.MEDIAN
                        | Operations.MIN
                    ):
                        return PlotType.LINE
                    case _:
                        return PlotType.SCATTER

    @abstractmethod
    def _get_figure(self) -> Figure:
        pass

    def plot(
        self, show: bool = True, save: bool = False, format: str = "png"
    ) -> Figure:
        """
        Plot the figure.

        Args:
            show (bool, optional): Whether to show the figure, defaults to True
            save (bool, optional): Whether to save the figure, defaults to False
            format (str, optional): Format of the file to be saved, defaults to "png"

        Raises:
            InvalidImageFormat: Image format is not allowed

        Returns:
            Figure: Figure object
        """
        figure = self._get_figure()

        if show:
            figure.show()

        if save:
            if format.upper() not in AllowedImageFormats.__members__:
                raise InvalidImageFormat(format)

            output_dir = Path("plots")
            output_dir.mkdir(exist_ok=True)
            lowercase_flag = self.meta.name.replace(" ", "_").lower()
            filename = f"{'heatmap' if self.hmap else 'plot'}_{lowercase_flag}_{self.year}{'_' + self.oper if self.oper else ''}"

            if format == "html":
                figure.write_html(output_dir / f"{filename}.html")
            else:
                figure.write_image(
                    file=output_dir / f"{filename}.{format}", format=format, scale=2
                )

        return figure
