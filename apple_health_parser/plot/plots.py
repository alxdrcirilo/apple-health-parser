import plotly.express as px
from plotly.graph_objs import Figure

from apple_health_parser.consts import PlotType
from apple_health_parser.interfaces.plot_interface import PlotInterface


class Plot(PlotInterface):
    """
    Plot the parsed data.
    """

    def _get_figure(self) -> Figure:
        """
        Get the plotly figure:
        - If the operation is not provided, the plot type is `PlotType.SCATTER`
        - If the operation is "count" or "sum", the plot type is `PlotType.BAR`
        - If the operation is "max", "mean", "median", or "min", the plot type is `PlotType.LINE`

        Returns:
            Figure: Figure object
        """
        if self.ptype is PlotType.HEATMAP:
            fig: Figure = px.imshow(
                self.dataframe,
                labels=dict(
                    x="Day of the month",
                    y="Month",
                ),
                text_auto=True,
                color_continuous_scale=self.psets.colormap,
                title=self.psets.title,
                template="simple_white",
            )

            fig.update_layout(
                coloraxis=dict(colorbar=dict(orientation="h", y=-0.15)),
                width=720,
                # This is a workaround to fix the height of the heatmap based on the number of months
                height=150
                + 15 * (self.dataframe.index.max() - self.dataframe.index.min() + 1),
            )

            fig.update_coloraxes(showscale=False)
            fig.update_xaxes(
                title="Day of the Month",
                tickvals=list(range(1, 32)),
                showline=True,
                linewidth=1,
                linecolor="black",
                mirror=True,
            )
            fig.update_yaxes(
                title="Month",
                tickvals=list(
                    range(
                        self.dataframe.index.min(),
                        self.dataframe.index.max() + 1,
                    )
                ),
                showline=True,
                linewidth=1,
                linecolor="black",
                mirror=True,
            )

        else:
            fig: Figure = getattr(px, self.ptype)(
                data_frame=self.dataframe,
                x=self.psets.x,
                y=self.psets.y,
                color=self.psets.color,
                title=self.psets.title,
                template="simple_white",
            )

            if self.ptype is PlotType.SCATTER:
                fig.update_traces(marker=dict(size=4))

            elif self.ptype is PlotType.BAR:
                fig.update_coloraxes(showscale=False)

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title=self.psets.title_yaxis,
                legend_title_text=self.psets.legend,
            )

        return fig
