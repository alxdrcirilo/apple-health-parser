# Installation

You can install the _Apple Health Parser_ Python package using your favourite package manager.

<!-- termynal -->

```bash
$ pip install apple-health-parser
---> 100%
Installed using pip!

$ poetry add apple-health-parser
---> 100%
Installed using poetry!

$ uv add apple-health-parser
---> 100%
Installed using uv!
```

## Dependencies

_Apple Health Parser_ comes with several dependencies. These are listed in the `pyproject.toml` file at the root of the package.

The following dependencies make the bulk of the work:

- `click`: for the CLI
- `kaleido`: used to export plots in various formats
- `pandas`: used for data processing
- `plotly`: used for plotting
- `pydantic`: used for validation
