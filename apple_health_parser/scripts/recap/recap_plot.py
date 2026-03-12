import io

import pandas as pd
import plotly.graph_objects as go

from apple_health_parser.config.definitions import PlotType


def get_recap_plots(
    flag: str,
    df_merged: pd.DataFrame,
    df_day: pd.DataFrame,
    week_labels: list[str],
    month_annotations: list[dict],
    axis_label: str,
    plot_type: PlotType,
    metric_color: str,
) -> tuple[io.BytesIO, io.BytesIO]:
    """
    Generate the bar chart and box plot for the year recap.

    Args:
        flag (str): Health data type identifier to determine the appropriate plot settings (e.g. "HKQuantityTypeIdentifierDistanceWalkingRunning")
        df_merged (pd.DataFrame): DataFrame containing the weekly data
        df_day (pd.DataFrame): DataFrame containing the daily data for the box plot
        week_labels (list[str]): List of week labels for the x-axis
        month_annotations (list[dict]): List of annotation dicts for month labels
        axis_label (str): Label for the y-axis (e.g. "Distance (km)")
        plot_type (PlotType): Type of plot to generate (e.g. PlotType.BAR)
        metric_color (str): Hex color code for the metric (e.g. "#fe5841")

        Returns:
            tuple[io.BytesIO, io.BytesIO]: Tuple containing the SVG image data for the bar chart and box plot
                - Bar chart image data
                - Box plot image data
    """

    fig = go.Figure()

    if plot_type == PlotType.BAR:
        bar_kwargs = dict(
            x=week_labels,
            y=df_merged["value"],
            name=axis_label,
        )

        # Time in daylight gets a special color mapping based on the value
        if flag == "HKQuantityTypeIdentifierTimeInDaylight":
            bar_kwargs["marker"] = dict(
                color=df_merged["value"],
                colorscale=[[0, "#1a237e"], [1, "#ffd700"]],
            )
        else:
            # Other metrics use a single color
            bar_kwargs["marker_color"] = metric_color

        fig.add_trace(go.Bar(**bar_kwargs))

    elif plot_type == PlotType.LINE:
        fig.add_trace(
            go.Scatter(
                x=week_labels,
                y=df_merged["value"],
                mode="lines",
                name=axis_label,
                line_color=f"{metric_color}",
                line_shape="spline",
                marker=dict(size=6),
            )
        )

    fig.update_layout(
        width=900,
        height=450,
        xaxis=dict(
            tickangle=-90,
            tickvals=week_labels,
            ticktext=week_labels,
        ),
        yaxis_title=axis_label,
        template="simple_white",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=60),  # Add bottom margin for annotations
        annotations=month_annotations,
    )

    image_data = fig.to_image(format="svg")
    image = io.BytesIO(image_data)

    fig_box = go.Figure()
    fig_box.add_trace(
        go.Box(
            x=df_day,
            marker_color=f"{metric_color}",
            boxpoints="all",
            pointpos=-2,
            notched=True,
            marker=dict(size=3),
        )
    )

    fig_box.update_layout(
        xaxis=dict(title=axis_label),
        yaxis=dict(visible=False),
        width=600,
        height=100,
        template="simple_white",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=20),
    )
    box_image_data = fig_box.to_image(format="svg")
    box_image = io.BytesIO(box_image_data)

    return image, box_image
