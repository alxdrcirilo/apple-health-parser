# CLI

The CLI allows you to parse and visualize your Apple Health data without writing any code. At the moment, the CLI supports exporting data from the Apple Health export file to CSV files.

## Running the CLI

The CLI comes with a help command that lists all available options and commands:

```bash
❯ apple-health-parser-cli --help
Usage: apple-health-parser-cli [OPTIONS]

  CLI to export data from the Apple Health export file to CSV files.

Options:
  --zip_file TEXT  Path to the Apple Health export.zip file
  --dir_name TEXT  Directory to export the CSV files to. If None, uses the
                   current directory
  --help           Show this message and exit.
```

To run the CLI, simply execute the following command in your terminal:

```bash
apple-health-parser-cli --zip_file <export.zip> --dir_name <output_directory>
```

!!! note

    The `--dir_name` argument is optional. If not provided, the current directory will be used.
