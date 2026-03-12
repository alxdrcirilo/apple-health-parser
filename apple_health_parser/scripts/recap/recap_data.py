import typing

import pandas as pd

from apple_health_parser.config.definitions import Operations
from apple_health_parser.exceptions import MissingYear
from apple_health_parser.models.parsed import ParsedData
from apple_health_parser.utils.parser import Parser


@typing.no_type_check
def get_recap_data(
    parser: Parser, year: int, flag: str, operation: Operations
) -> tuple[pd.DataFrame, pd.DataFrame, list[str], list[dict]]:
    """
    Parse Apple Health data and prepare weekly summary, labels, and month annotations for plotting.

    Args:
        parser (Parser): Instance of the Parser class
        year (int): Year to filter the data for
        flag (str): Health data type identifier to extract (e.g. "HKQuantityTypeIdentifierDistanceWalkingRunning")
        operation (Operations): Operation type for the data (e.g. "sum")

    Returns:
        tuple:
            - df (pd.DataFrame): Original filtered DataFrame for further statistics
            - df_merged (pd.DataFrame): Weekly summary DataFrame with all weeks for the year
            - week_labels (pd.Series): Series of week labels for plotting
            - month_annotations (list[dict]): List of annotation dicts for month labels
    """
    # Get records for the specified flag
    parsed: ParsedData = parser.get_flag_records(flag)
    df = parsed.records

    years = df.start_date.dt.year.unique().tolist()
    if year not in years:
        raise MissingYear(year, years)

    # Ensure start_date is datetime
    df["start_date"] = pd.to_datetime(df["start_date"])

    # Filter by year
    df = df[df["start_date"].dt.year == year]

    # Compute week start
    df["week_start"] = df["start_date"].dt.to_period("W").dt.start_time

    # Compute week start and aggregate
    if operation == Operations.SUM:
        df_week = df.groupby("week_start", as_index=False)["value"].sum()
    elif operation == Operations.MEAN:
        df_week = df.groupby("week_start", as_index=False)["value"].mean()
    else:
        raise ValueError(f"Unsupported operation: {operation}")

    # Generate all weeks for the year
    weeks = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="W-MON")

    # Merge with all weeks to ensure we have a complete timeline, filling missing weeks with NaN
    df_merged = pd.DataFrame({"week_start": weeks}).merge(
        df_week,
        on="week_start",
        how="left",
    )
    df_merged["value"] = df_merged["value"].fillna(pd.NA)

    # Drop weeks that are outside the specified year (e.g., last week of previous year or first week of next year)
    isocal = df_merged["week_start"].dt.isocalendar()
    df_merged["week"] = isocal.week
    df_merged["month"] = df_merged["week_start"].dt.strftime("%b")
    df_merged = df_merged[isocal.year == year]

    # Labels for plotting
    week_labels = df_merged["week"].astype(str).str.zfill(2)

    # Find first week index for each month for annotation
    month_week_index = list(
        df_merged.drop_duplicates("month")[["month", "week"]]
        .sort_values("week")
        .itertuples(index=False, name=None)
    )
    month_annotations = [
        dict(
            x=week_num,
            y=-0.12,  # y-offset below the x-axis
            xref="x",
            yref="paper",
            text=month,
            showarrow=False,
            font=dict(size=14),
            align="left",
        )
        for month, week_num in month_week_index
    ]

    return df, df_merged, week_labels, month_annotations
