import logging
import os
import sys
import warnings
from datetime import date
from pathlib import Path

import click

from apple_health_parser.scripts.recap.metrics.definitions import (
    METRIC_DEFINITIONS,
)
from apple_health_parser.scripts.recap.recap_data import get_recap_data
from apple_health_parser.scripts.recap.recap_pdf import PdfSectionData, get_recap_report
from apple_health_parser.scripts.recap.recap_plot import get_recap_plots
from apple_health_parser.scripts.recap.recap_stats import get_recap_stats
from apple_health_parser.utils.logging import logger
from apple_health_parser.utils.parser import Parser

# Set logging level for fpdf to ERROR to suppress warnings
logging.getLogger("fpdf").setLevel(logging.ERROR)

# Ignore warnings about timezone information dropping when converting to PeriodArray/Index representation
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Converting to PeriodArray/Index representation will drop timezone information.",
)


def open_pdf(filepath: Path) -> None:
    """
    Open the generated PDF report using the default PDF viewer based on the operating system.

    Args:
        filepath (Path): The path to the PDF file to open

    Raises:
        RuntimeError: If the platform is unsupported
    """
    if sys.platform.startswith("darwin"):
        os.system(f'open "{filepath}"')
    elif sys.platform.startswith("win"):
        os.startfile(filepath)
    elif sys.platform.startswith("linux"):
        os.system(f'xdg-open "{filepath}"')
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")


@click.command(no_args_is_help=True)
@click.option("--zip_file", help="Path to the Apple Health export.zip file")
@click.option(
    "--year",
    default=date.today().year,
    help="Year to filter the data for, defaults to current year",
)
def main(zip_file: str, year: int = date.today().year) -> None:
    """
    CLI to export the year recap from the Apple Health export file to a PDF file.

    Args:
        zip_file (str): Path to the Apple Health export.zip file
        year (int, optional): Year to filter the data for, defaults to current year
    """
    logger.info(
        click.style(f"Generating year recap report - {year}...", fg="green", bold=True)
    )

    # Parse data
    parser = Parser(export_file=zip_file, overwrite=True, verbose=True)

    # Get data and prepare for plotting
    pdf_section_data: dict[str, PdfSectionData] = {}
    for n, (flag, metadata) in enumerate(METRIC_DEFINITIONS.items()):
        try:
            logger.info(
                click.style(
                    f"Processing metric {n + 1}/{len(METRIC_DEFINITIONS)}: {flag}",
                    fg="blue",
                )
            )

            if flag not in parser.flags:
                logger.warning(
                    click.style(
                        f"\nFlag not found in data, skipping: {flag}", fg="yellow"
                    )
                )
                continue

            df, df_merged, week_labels, month_annotations = get_recap_data(
                parser, year, flag, metadata.operation
            )

            df_day, stats_text, (q_min, q1, q2, q3, q_max) = get_recap_stats(df, flag)

            image, box_image = get_recap_plots(
                flag,
                df_merged,
                df_day,
                week_labels,
                month_annotations,
                metadata.axis_label,
                metadata.plot_type,
                metadata.color,
            )

            pdf_section_data[flag] = PdfSectionData(
                year=year,
                image_data=image,
                box_image_data=box_image,
                stats_text=stats_text,
                quantiles=(q_min, q1, q2, q3, q_max),
            )

        except Exception as e:
            logger.warning(
                click.style(f"Error processing metric {flag}: {e}", fg="yellow")
            )

    try:
        get_recap_report(pdf_section_data)
        pdf_filepath = Path("report.pdf").resolve()
        logger.info(click.style(f"Report generated: {pdf_filepath}", underline=True))
        open_pdf(pdf_filepath)

    except StopIteration:
        logger.error(
            click.style(
                "No data found to generate the report. Please check your data and/or CLI command, and try again.",
                fg="red",
            )
        )


if __name__ == "__main__":
    main()
