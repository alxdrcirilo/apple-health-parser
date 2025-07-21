import click

from apple_health_parser.plot.overviews import Overview
from apple_health_parser.plot.plots import Plot
from apple_health_parser.plot.sleep import SleepPlot
from apple_health_parser.utils.logging import logger
from apple_health_parser.utils.parser import Parser


@click.command(no_args_is_help=True)
@click.option("--zip_file", help="Path to the Apple Health export.zip file")
def main(zip_file: str) -> None:
    """
    CLI to parse and plot data from the Apple Health export file.

    Args:
        zip_file (str): Path to the export.zip file
    """
    logger.info(click.style("Apple Health Parser", bg="blue", fg="white", bold=True))

    parser = Parser(export_file=zip_file, overwrite=True, verbose=True)

    # Get the sources from the export file
    flag = "HKQuantityTypeIdentifierDistanceWalkingRunning"
    source = "Alexandre’s Apple\xa0Watch"
    data = parser.get_flag_records(flag=flag)

    plot = Plot(data=data, year=2024, source=source, operation="sum", heatmap=False)
    plot.plot(show=True, save=True, format="svg")

    # Activity overview
    flags = [
        "HKQuantityTypeIdentifierActiveEnergyBurned",
        "HKQuantityTypeIdentifierAppleExerciseTime",
        "HKQuantityTypeIdentifierAppleStandTime",
    ]
    data = parser.get_flag_records(flag=flags)
    overview = Overview(data=data, year=2024, overview_type="activity", source=source)
    overview.plot(show=True, save=True, format="svg")

    # Sleep
    flag = "HKCategoryTypeIdentifierSleepAnalysis"
    data = parser.get_flag_records(flag=flag)
    start_date = "2024-03-01T20:00:00+02:00"
    end_date = "2024-03-02T08:00:00+02:00"
    plot = SleepPlot(data=data, year=2024, timerange=(start_date, end_date))
    plot.plot(show=True, save=True, format="svg")


if __name__ == "__main__":
    main()
