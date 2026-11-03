import asyncio
import warnings
import zipfile
from collections.abc import Collection
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import click
import lxml.etree as ET

from apple_health_parser.scripts.recap.metrics.definitions import (
    METRIC_DEFINITIONS,
)
from apple_health_parser.scripts.recap.recap_data import get_recap_data
from apple_health_parser.scripts.recap.recap_html import (
    HtmlSectionData,
    get_recap_report_html,
)
from apple_health_parser.scripts.recap.recap_plot import get_recap_figures
from apple_health_parser.scripts.recap.recap_stats import get_recap_stats
from apple_health_parser.utils.logging import logger
from apple_health_parser.utils.parser import Parser

# Ignore warnings about timezone information dropping when converting to PeriodArray/Index representation
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Converting to PeriodArray/Index representation will drop timezone information.",
)


@dataclass
class RecapResult:
    """
    Result of `generate_recap_report_html()`.

    Attributes:
        html (str): HTML fragment for the year recap report
        flag_counts (dict[str, int]): Number of records per requested flag within the year,
            0 for flags that have no records
        charted_flags (list[str]): Flags that got a section in the report
        stats_text (dict[str, str]): Per-flag stats summary (the same markdown-formatted
            text rendered into the HTML), keyed by flag - lets a caller (e.g. a PDF export)
            read the real value instead of re-deriving it from the rendered HTML
        quantiles (dict[str, tuple[float, float, float, float, float]]): Per-flag five-number
            summary (min, q1, median, q3, max), keyed by flag
    """

    html: str
    flag_counts: dict[str, int] = field(default_factory=dict)
    charted_flags: list[str] = field(default_factory=list)
    stats_text: dict[str, str] = field(default_factory=dict)
    quantiles: dict[str, tuple[float, float, float, float, float]] = field(
        default_factory=dict
    )


def _as_float_quantiles(
    quantiles: tuple[float, float, float, float, float],
) -> tuple[float, float, float, float, float]:
    """
    Cast a five-number summary to plain `float`.

    `get_recap_stats()` returns numpy scalars (`int64`/`float64`) for integer-dtype
    metrics, which aren't JSON-serializable.

    Args:
        quantiles (tuple[float, float, float, float, float]): Min, Q1, median, Q3, max

    Returns:
        tuple[float, float, float, float, float]: Same values, cast to `float`
    """
    q_min, q1, q2, q3, q_max = quantiles
    return float(q_min), float(q1), float(q2), float(q3), float(q_max)


def _find_export_xml_name(namelist: list[str]) -> str:
    """
    Find the `export.xml` (or `Export.xml`) member name inside an export.zip's namelist.

    Args:
        namelist (list[str]): Member names, as returned by `ZipFile.namelist()`

    Raises:
        FileNotFoundError: If no `export.xml` member was found

    Returns:
        str: The matching member name
    """
    for name in namelist:
        if name.startswith("__MACOSX/"):
            continue
        if Path(name).name.lower() == "export.xml":
            return name
    raise FileNotFoundError("No export.xml found in the provided zip file")


async def _prefilter_export(
    zip_file: str | Path,
    year: int,
    output_dir: str | Path,
    flags: set[str],
    scan_callback: Callable[[int], None] | None = None,
) -> tuple[Path, dict[str, int]]:
    """
    Stream-filter an export.zip down to one year's `Record` elements using `iterparse`,
    so the whole export never has to fit in memory (a WASM/Pyodide sandbox may not have
    enough) and `Parser`'s full DOM parse only has to handle the filtered subset.

    Also counts every requested flag's `year` records in this same pass.

    Args:
        zip_file (str | Path): Path to the original Apple Health export.zip file
        year (int): Year to keep records for
        output_dir (str | Path): Directory to write the filtered export.xml/export.zip into
        flags (set[str]): Flags to count records for
        scan_callback (Callable[[int], None], optional): Called periodically with the running
            count of `Record` elements scanned so far, defaults to None

    Returns:
        tuple[Path, dict[str, int]]: Path to the filtered export.zip (only `year`'s records for
            flags with a metric definition), and per-flag record counts for `year`
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    flag_counts = {flag: 0 for flag in flags}
    chartable = flags & METRIC_DEFINITIONS.keys()
    year_prefix = str(year)

    filtered_xml = output_dir / "export.filtered.xml"
    with zipfile.ZipFile(zip_file) as zf:
        export_name = _find_export_xml_name(zf.namelist())
        with zf.open(export_name) as xml_stream, open(filtered_xml, "wb") as out:
            out.write(b"<HealthData>")

            context = ET.iterparse(xml_stream, events=("end",), tag="Record")
            for scanned, (_, elem) in enumerate(context, start=1):
                flag = elem.attrib.get("type")
                start_date = elem.attrib.get("startDate", "")
                if flag in flag_counts and start_date.startswith(year_prefix):
                    flag_counts[flag] += 1
                    if flag in chartable:
                        out.write(ET.tostring(elem))

                # Standard iterparse memory-saving idiom: drop the element and any
                # already-processed preceding siblings once we're done with it.
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

                if scanned % 2000 == 0:
                    if scan_callback is not None:
                        scan_callback(scanned)
                    await asyncio.sleep(0)
            del context

            out.write(b"</HealthData>")

    filtered_zip = output_dir / "export.filtered.zip"
    with zipfile.ZipFile(filtered_zip, "w") as zf_out:
        # Loader.extract_zip looks for "<zip stem>.xml", so the archive member must match it
        zf_out.write(
            filtered_xml, arcname=f"apple_health_export/{filtered_zip.stem}.xml"
        )

    return filtered_zip, flag_counts


async def generate_recap_report_html(
    zip_file: str | Path,
    year: int,
    output_dir: str | Path = "data",
    progress_callback: Callable[[int, int], None] | None = None,
    scan_callback: Callable[[int], None] | None = None,
    flags: Collection[str] | None = None,
) -> RecapResult:
    """
    Generate the year recap report as an HTML fragment with interactive Plotly charts.
    This is the browser-safe counterpart to `generate_recap_report()` (no `kaleido`/`fpdf2`).

    Args:
        zip_file (str | Path): Path to the Apple Health export.zip file
        year (int): Year to filter the data for
        output_dir (str | Path, optional): Directory to extract the export file to, defaults to "data"
        progress_callback (Callable[[int, int], None], optional): Called as `(n, total)` after each
            selected metric is processed (e.g. to drive a progress bar), defaults to None
        scan_callback (Callable[[int], None], optional): Called periodically during the pre-filter
            pass with the running count of records scanned, defaults to None
        flags (Collection[str], optional): Flags to include in the report and count records for,
            defaults to None (all metrics with a definition)

    Returns:
        RecapResult: The HTML fragment for the year recap report, the per-flag record counts for
            the year, and the flags that were charted
    """
    logger.info(
        click.style(f"Generating year recap report - {year}...", fg="green", bold=True)
    )

    selected = set(METRIC_DEFINITIONS) if flags is None else set(flags)

    # Stream-filter down to this year's relevant records first, so Parser's full
    # DOM parse only ever has to handle a small, pre-filtered export.xml
    filtered_zip, flag_counts = await _prefilter_export(
        zip_file, year, output_dir, selected, scan_callback
    )

    # Parse data
    parser = Parser(
        export_file=filtered_zip, output_dir=output_dir, overwrite=True, verbose=True
    )

    # Get data and prepare for plotting
    metrics = [
        (flag, metadata)
        for flag, metadata in METRIC_DEFINITIONS.items()
        if flag in selected
    ]
    total = len(metrics)
    html_section_data: dict[str, HtmlSectionData] = {}
    for n, (flag, metadata) in enumerate(metrics):
        try:
            logger.info(
                click.style(
                    f"Processing metric {n + 1}/{total}: {flag}",
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

            df_day, stats_text, quantiles = get_recap_stats(df, flag)

            figure, box_figure = get_recap_figures(
                flag,
                df_merged,
                df_day,
                week_labels,
                month_annotations,
                metadata.axis_label,
                metadata.plot_type,
                metadata.color,
            )

            html_section_data[flag] = HtmlSectionData(
                year=year,
                figure=figure,
                box_figure=box_figure,
                stats_text=stats_text,
                quantiles=quantiles,
            )

        except Exception as e:
            logger.warning(
                click.style(f"Error processing metric {flag}: {e}", fg="yellow")
            )
        finally:
            if progress_callback is not None:
                progress_callback(n + 1, total)
            await asyncio.sleep(0)

    # get_recap_report_html needs at least one section (it takes the year from the first one)
    html = get_recap_report_html(html_section_data) if html_section_data else ""

    return RecapResult(
        html=html,
        flag_counts=flag_counts,
        charted_flags=list(html_section_data),
        stats_text={flag: data.stats_text for flag, data in html_section_data.items()},
        quantiles={
            flag: _as_float_quantiles(data.quantiles)
            for flag, data in html_section_data.items()
        },
    )
