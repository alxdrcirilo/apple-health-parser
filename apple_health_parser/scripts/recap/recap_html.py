import html
import re
from dataclasses import dataclass

import plotly.graph_objects as go

from apple_health_parser.scripts.recap.metrics.definitions import (
    METRIC_DEFINITIONS,
)


@dataclass
class HtmlSectionData:
    year: int
    figure: go.Figure
    box_figure: go.Figure
    stats_text: str
    quantiles: tuple[float, float, float, float, float]


def _render_stats_text(stats_text: str) -> str:
    """
    Escape the stats text as HTML, then turn its `**bold**` markdown (the only
    markdown syntax `summary_template` strings use) into `<strong>` tags.

    Args:
        stats_text (str): Stats text, as produced by `get_recap_stats()`

    Returns:
        str: HTML-safe stats text
    """
    escaped = html.escape(stats_text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def _make_figure_responsive(figure: go.Figure, font_size: int = 9) -> go.Figure:
    """
    Adapt a figure (built with a fixed width tuned for the PDF path) for a fluid web layout.

    Args:
        figure (go.Figure): Figure to adapt (mutated in place)
        font_size (int, optional): Font size for axes/ticks, defaults to 9

    Returns:
        go.Figure: The same figure, for chaining
    """
    # Mid-grey that stays readable on both the light (#ffffff) and dark (#0f1218) page backgrounds
    axis_color = "#8a93a6"
    figure.update_layout(
        autosize=True, width=None, font=dict(size=font_size, color=axis_color)
    )
    figure.update_xaxes(
        showline=True,
        linecolor=axis_color,
        linewidth=1,
        tickfont=dict(color=axis_color),
    )
    figure.update_yaxes(
        showline=True,
        linecolor=axis_color,
        linewidth=1,
        tickfont=dict(color=axis_color),
    )
    for annotation in figure.layout.annotations or ():
        annotation.update(font=dict(size=font_size))
    return figure


def get_recap_report_html(
    html_section_data: dict[str, HtmlSectionData],
) -> str:
    """
    Build the year recap report as a single HTML fragment with interactive Plotly charts.

    Unlike `get_recap_report()` (which produces a PDF with static chart images via
    `fpdf2`/`kaleido`), this returns a plain HTML fragment. The caller's page is
    expected to already have Plotly.js loaded, since the embedded charts are generated
    with `Figure.to_html(include_plotlyjs=False, full_html=False)`.

    Args:
        html_section_data (dict[str, HtmlSectionData]): Data for each section of the report, keyed by flag

    Returns:
        str: HTML fragment for the year recap report
    """
    year = html_section_data[next(iter(html_section_data))].year

    sections = []
    for flag, section_data in html_section_data.items():
        metric_metadata = METRIC_DEFINITIONS[flag]
        unit = html.escape(metric_metadata.unit)
        q_min, q1, q2, q3, q_max = section_data.quantiles

        chart_config = {"responsive": True, "displayModeBar": False}
        chart_html = _make_figure_responsive(section_data.figure).to_html(
            include_plotlyjs=False, full_html=False, config=chart_config
        )
        box_chart_html = _make_figure_responsive(section_data.box_figure).to_html(
            include_plotlyjs=False, full_html=False, config=chart_config
        )

        sections.append(f"""
<section class="metric" data-flag="{html.escape(flag)}">
  <h2>{html.escape(metric_metadata.name)}</h2>
  <p class="description">{html.escape(metric_metadata.description)}</p>
  <div class="chart-frame">{chart_html}</div>
  <p class="stats">{_render_stats_text(section_data.stats_text)}</p>
  <div class="chart-frame">{box_chart_html}</div>
  <table class="summary">
    <caption>Five-number summary</caption>
    <tbody>
      <tr><th scope="row">Metric</th><td>{unit}</td></tr>
      <tr><th scope="row">Min</th><td>{q_min:.2f} {unit}</td></tr>
      <tr><th scope="row">Q1</th><td>{q1:.2f} {unit}</td></tr>
      <tr><th scope="row">Median</th><td>{q2:.2f} {unit}</td></tr>
      <tr><th scope="row">Q3</th><td>{q3:.2f} {unit}</td></tr>
      <tr><th scope="row">Max</th><td>{q_max:.2f} {unit}</td></tr>
    </tbody>
  </table>
</section>""")

    body = "\n".join(sections)
    return f"""<article class="year-recap">
  <header>
    <p class="year">{year}</p>
  </header>
{body}
</article>"""
