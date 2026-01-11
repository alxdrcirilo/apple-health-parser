import click

from apple_health_parser.utils.logging import logger
from apple_health_parser.utils.parser import Parser


@click.command(no_args_is_help=True)
@click.option("--zip_file", help="Path to the Apple Health export.zip file")
@click.option(
    "--dir_name",
    default=None,
    help="Directory to export the CSV files to. If None, uses the current directory",
)
def main(zip_file: str, dir_name: str | None) -> None:
    """
    CLI to export data from the Apple Health export file to CSV files.
    """
    logger.info(click.style("Apple Health Parser", bg="blue", fg="white", bold=True))

    parser = Parser(export_file=zip_file, overwrite=True, verbose=True)

    # Export all data
    parser.export(dir_name=dir_name)


if __name__ == "__main__":
    main()
