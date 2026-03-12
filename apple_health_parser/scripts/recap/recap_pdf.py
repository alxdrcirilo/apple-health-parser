from dataclasses import dataclass
from importlib.metadata import version
from io import BytesIO

from fpdf import FPDF

from apple_health_parser.scripts.recap.metrics.definitions import (
    METRIC_DEFINITIONS,
)


@dataclass
class PdfSectionData:
    year: int
    image_data: BytesIO
    box_image_data: BytesIO
    stats_text: str
    quantiles: tuple[float, float, float, float, float]


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", style="I", size=7)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")
        self.set_font("Arial", style="", size=7)
        self.set_text_color(100)
        footer_text = (
            f"Generated with **Apple Health Parser** {version('apple-health-parser')}"
        )
        self.cell(0, 10, footer_text, align="R", markdown=True)


def get_recap_report(
    pdf_section_data: dict[str, PdfSectionData],
) -> None:
    """
    Generate a PDF report for the year recap.

    Args:
        pdf_section_data (dict[str, PdfSectionData]): Data for each section of the report, keyed by flag
    """
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.author = "Apple Health Parser"
    pdf.title = f"Apple Health Year Recap - {pdf_section_data[next(iter(pdf_section_data))].year}"

    # Text block width
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    WIDTH = (pdf.w - pdf.l_margin - pdf.r_margin) * 0.8
    TABLE_WIDTH = WIDTH * 0.8

    for page, (flag, section_data) in enumerate(pdf_section_data.items()):
        metric_metadata = METRIC_DEFINITIONS[flag]

        year, image_data, box_image_data, stats_text, quantiles = (
            section_data.year,
            section_data.image_data,
            section_data.box_image_data,
            section_data.stats_text,
            section_data.quantiles,
        )

        pdf.add_page()

        if page == 0:
            pdf.set_font("Arial", "B", 36)
            pdf.ln(10)
            pdf.cell(10, 10, "Year Recap")
            pdf.ln(14)
            pdf.set_font("Arial", "B", 24)
            pdf.cell(10, 10, f"{year}")
            pdf.ln(16)

        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 10, f"{metric_metadata.name}")
        pdf.ln(10)

        metric_desc = metric_metadata.description
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(120)
        pdf.multi_cell(WIDTH, 5, metric_desc, border="T", padding=2)
        pdf.ln(12)

        pdf.image(image_data, w=WIDTH, keep_aspect_ratio=True)
        pdf.ln(10)

        pdf.set_font("Arial", size=9)
        pdf.set_text_color(1)
        pdf.multi_cell(WIDTH, 5, stats_text, markdown=True)
        pdf.ln(6)

        pdf.image(box_image_data, w=WIDTH, keep_aspect_ratio=True)
        pdf.ln(10)

        q_min, q1, q2, q3, q_max = quantiles
        table_data = (
            ("Metric", metric_metadata.unit),
            ("Min", f"{q_min:.2f} {metric_metadata.unit}"),
            ("Q1", f"{q1:.2f} {metric_metadata.unit}"),
            ("Median", f"{q2:.2f} {metric_metadata.unit}"),
            ("Q3", f"{q3:.2f} {metric_metadata.unit}"),
            ("Max", f"{q_max:.2f} {metric_metadata.unit}"),
        )

        pdf.set_font("Arial", size=7)
        pdf.set_text_color(60)
        pdf.set_draw_color(60)
        pdf.multi_cell(
            TABLE_WIDTH,
            5,
            text="__Table__ - Five-number summary",
            border="B",
            align="C",
            padding=2,
            markdown=True,
        )
        pdf.ln(4)
        pdf.set_font("Arial", size=9)
        pdf.set_text_color(1)
        pdf.set_draw_color(1)
        with pdf.table(
            align="LEFT", width=TABLE_WIDTH, borders_layout="SINGLE_TOP_LINE"
        ) as table:
            for data_row in table_data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

        # Reset font color
        pdf.set_text_color(1)

    pdf.output("report.pdf")
