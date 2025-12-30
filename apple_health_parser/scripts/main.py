from datetime import date

import click

from apple_health_parser.config.definitions import OverviewType
from apple_health_parser.plot.overviews import Overview
from apple_health_parser.plot.plots import Plot
from apple_health_parser.utils.logging import logger
from apple_health_parser.utils.parser import Parser


@click.command(no_args_is_help=True)
@click.option(
    "--zip_file", required=True, help="Path to the Apple Health export.zip file"
)
@click.option(
    "--year", default=date.today().year, help="Year to plot (default: current year)"
)
@click.option(
    "--source", default=None, help="Filter by source (default: all sources combined)"
)
def main(zip_file: str, year: int, source: str | None) -> None:
    """
    CLI to parse and plot data from the Apple Health export file.

    Args:
        zip_file (str): Path to the export.zip file
        year (int): Year to plot
        source (str | None): Source to filter by (None for all sources)
    """
    logger.info(click.style("Apple Health Parser", bg="blue", fg="white", bold=True))

    parser = Parser(export_file=zip_file, overwrite=True, verbose=True)

    # Distance walking/running plot
    flag = "HKQuantityTypeIdentifierDistanceWalkingRunning"
    data = parser.get_flag_records(flag=flag)
    plot = Plot(data=data, year=year, source=source, operation="sum", heatmap=False)
    plot.plot(show=True, save=True, format="svg")

    # Activity overview
    flags = [
        "HKQuantityTypeIdentifierActiveEnergyBurned",
        "HKQuantityTypeIdentifierAppleExerciseTime",
        "HKQuantityTypeIdentifierAppleStandTime",
    ]
    data = parser.get_flag_records(flag=flags)
    overview = Overview(
        data=data, year=year, overview_type=OverviewType.ACTIVITY, source=source
    )
    overview.plot(show=True, save=True, format="svg")


if __name__ == "__main__":
    main()
