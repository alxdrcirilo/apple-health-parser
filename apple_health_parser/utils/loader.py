import re
from pathlib import Path
from shutil import rmtree
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import click

from apple_health_parser.utils.logging import logger


class Loader:
    """
    Loader class to extract and read an XML file from the Apple Health `export.zip` file.
    """

    @staticmethod
    def extract_zip(
        zip_file: str | Path, output_dir: str | Path, overwrite: bool | None = None
    ) -> Path:
        """
        Extracts a zip file to an output directory.

        Args:
            zip_file (str | Path): The zip file to extract
            output_dir (str | Path): The output directory to extract the file to
            overwrite (bool, optional): Flag to overwrite the existing data, defaults to None

        Returns:
            Path: The absolute path to the extracted file
        """
        if isinstance(zip_file, str):
            zip_file = Path(zip_file)

        if isinstance(output_dir, str):
            output_dir = Path(output_dir)

        export_dir = output_dir / "apple_health_export"

        # Check if output directory exists and delete it if it does and "y" or "yes" is entered
        if export_dir.exists():
            Loader.delete_previous_export(export_dir, overwrite)

        # Extract the zip file
        with ZipFile(zip_file, "r") as data:
            logger.info(f"Extracting {zip_file} to {output_dir}...")
            data.extractall(output_dir)

        # Log the compressed and uncompressed file sizes
        file_size = zip_file.stat().st_size
        dir_size = sum(f.stat().st_size for f in output_dir.glob("**/*") if f.is_file())
        logger.info(f"Compressed: {file_size / 1e6:.2f} MB")
        logger.info(f"Uncompressed: {dir_size/ 1e6:.2f} MB")

        return (export_dir / "export.xml").resolve()

    @staticmethod
    def delete_previous_export(output_dir: Path, overwrite: bool | None) -> None:
        """
        Delete the previous export if it exists and the user agrees.

        Args:
            output_dir (Path): The output directory to extract the file to
            overwrite (bool | None): Flag to overwrite the existing data, defaults to None
        """
        match overwrite:
            case None:
                logger.warning(f"Found previous export at {output_dir}...")
                if click.confirm("Do you want to delete it?"):
                    rmtree(output_dir)
                    logger.warning(f"Deleted previous export at {output_dir}...")

            case True:
                rmtree(output_dir)
                logger.warning(f"Deleted previous export at {output_dir}...")

    @staticmethod
    def read_xml(xml_file: Path) -> list[ET.Element]:
        """
        Read an XML file and return the root element.

        Args:
            xml_file (Path): Path to the XML file

        Returns:
            list[ET.Element]: List of records (ET.Element)
        """
        logger.info(f"Processing {xml_file}...")
        with open(xml_file, "r") as file:
            root = ET.parse(file).getroot()
            Loader._log_metadata(root)
            return root.findall("Record")

    @staticmethod
    def _log_metadata(root: ET.Element) -> None:
        """
        Log metadata from the XML file.

        Example:

        ```bash
        2024-05-29 22:28:23,064 - INFO - Locale:                            en_NL
        2024-05-29 22:28:23,065 - INFO - Export date:                       2024-05-30 22:20:25 +0200
        2024-05-29 22:28:23,065 - INFO - Date of birth:                     1990-04-22
        2024-05-29 22:28:23,065 - INFO - Biological sex:                    HKBiologicalSexMale
        2024-05-29 22:28:23,065 - INFO - Blood type:                        HKBloodTypeAPositive
        2024-05-29 22:28:23,065 - INFO - Fitzpatrick skin type:             HKFitzpatrickSkinTypeNotSet
        2024-05-29 22:28:23,065 - INFO - Cardio fitness medications use:    None
        ```

        Args:
            root (ET.Element): Root element of the XML file
        """

        def get_locale() -> None:
            """
            Get the locale from the XML file (e.g. `en_NL`).
            """
            locale = root.attrib.get("locale")
            if locale is not None:
                logger.info(f"{'Locale:':<35}" + click.style(f"{locale}", bg="red"))

        def get_export_date() -> None:
            """
            Get the export date from the XML file (e.g. `2024-05-29 22:20:35 +0200`).
            """
            export_date = root.find("ExportDate")
            if export_date is not None:
                logger.info(
                    f"{'Export date:':<35}"
                    + click.style(f"{export_date.attrib['value']}", fg="green")
                )

        def get_user() -> None:
            """
            Get user metadata from the XML file.
            """
            user = root.find("Me")
            if user is not None:
                user_data: list[tuple[str, str]] = [
                    (flag.removeprefix("HKCharacteristicTypeIdentifier"), value)
                    for (flag, value) in user.items()
                ]
                for flag, value in user_data:
                    # Split flag at uppercase letters
                    flag = " ".join(re.findall(r"[A-Z][^A-Z]*", flag))
                    # Lower case every word except the first
                    flag = flag[0] + flag[1:].lower() + ":"
                    logger.info(f"{flag:<35}" + click.style(f"{value}", fg="cyan"))

        get_locale()
        get_export_date()
        get_user()
