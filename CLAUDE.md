# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
make install      # Create venv and install dependencies (uv venv && uv sync --all-extras --dev)
make check        # Run all checks (lint, format, type, test)
make test         # Run pytest with coverage
make lint         # Check code style (ruff)
make format       # Auto-fix and format (ruff)
make type         # Type check (mypy)
make docs         # Serve docs locally (mkdocs)
make doctor       # Verify environment setup
make clean        # Remove venv, cache, and build artifacts
```

Run a single test:
```bash
uv run pytest tests/test_parser.py::test_function_name -v
```

## Architecture

This package parses Apple HealthKit `export.zip` files, validates records with Pydantic models, and generates Plotly visualizations.

### Data Flow

1. **Loader** (`utils/loader.py`) - Extracts `export.zip` and reads `export.xml`
2. **Parser** (`utils/parser.py`) - Extends Loader, groups XML records by flag types (e.g., `HKQuantityTypeIdentifierHeartRate`), builds Pydantic models
3. **ParsedData** (`models/parsed.py`) - Dataclass holding flag, sources, devices, dates, and pandas DataFrame of records
4. **Preprocessor** (`utils/preprocessor.py`) - Filters/aggregates DataFrame by year, source, and operation (sum, mean, etc.)
5. **Plot classes** (`plot/`) - Generate Plotly figures (scatter, bar, line, heatmap)

### Key Abstractions

- **PlotInterface** (`interfaces/plot_interface.py`) - Abstract base for all plot types; handles preprocessing, plot type selection, and save/show logic
- **PreprocessorInterface** (`interfaces/preprocessor_interface.py`) - Abstract base for data transformation; validates year, operation, and source

### Record Models

- **HealthData** (`models/records.py`) - Base Pydantic model for all health records
- **HeartRateData** - Extends HealthData with `motion_context` field
- **SleepData** - Extends HealthData with `timezone` and computed `range` field

### Flag Metadata

`config/definitions.py` contains YAML-loaded metadata (name, unit, colormap) for each HealthKit flag type. The `FLAG_METADATA` dict in `consts.py` maps flag strings to `Metadata` objects.

## CLI

Entry point: `cli` command (defined in `pyproject.toml` scripts section)
```bash
uv run cli --zip_file path/to/export.zip
```

## Testing

Tests use fixtures from `tests/conftest.py` with sample data in `tests/data/`. The `parser` fixture creates a Parser instance using `tmp_path` for isolated extraction.
