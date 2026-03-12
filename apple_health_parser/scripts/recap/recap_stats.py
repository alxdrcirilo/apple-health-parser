import typing

import pandas as pd

from apple_health_parser.config.definitions import Operations
from apple_health_parser.scripts.recap.metrics.definitions import (
    METRIC_DEFINITIONS,
)


@typing.no_type_check
def get_recap_stats(
    df: pd.DataFrame,
    flag: str,
) -> tuple[pd.DataFrame, str, tuple[float, float, float, float, float]]:
    """
    Compute daily distance statistics and return a daily summary DataFrame, a formatted statistics text, and quantiles.

    Args:
        df (pd.DataFrame): DataFrame containing the original distance records with 'start_date' and 'value' columns
        flag (str): Health data type identifier to determine the appropriate summary template (e.g. "HKQuantityTypeIdentifierDistanceWalkingRunning")

    Returns:
        tuple:
            - df_day (pd.DataFrame): DataFrame with daily data
            - stats_text (str): Formatted string summarizing the distance statistics
            - quantiles (tuple): Tuple containing the min, Q1, median, Q3, and max of daily distances
    """
    df["day"] = df["start_date"].dt.to_period("D")

    operation = METRIC_DEFINITIONS[flag].operation
    if operation == Operations.SUM:
        df_day = df.groupby("day")["value"].sum()
    elif operation == Operations.MEAN:
        df_day = df.groupby("day")["value"].mean()

    dist_count = df_day.count()
    dist_avg = df_day.mean()
    dist_total = df_day.sum()
    q_min = df_day.min()
    q_max = df_day.max()
    q1 = df_day.quantile(0.25)
    q2 = df_day.median()
    q3 = df_day.quantile(0.75)

    stats_text = METRIC_DEFINITIONS[flag].summary_template.format(
        dist_total=dist_total,
        dist_avg=dist_avg,
        dist_median=q2,
        dist_min=q_min,
        dist_max=q_max,
        dist_count=dist_count,
    )

    return df_day, stats_text, (q_min, q1, q2, q3, q_max)
