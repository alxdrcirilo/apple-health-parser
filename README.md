<div align="center">
    <img src="https://github.com/alxdrcirilo/apple-health-parser/blob/main/docs/assets/images/logo.png?raw=true" alt="logo" width=128 />

# Apple Health Parser

<img src="https://raw.githubusercontent.com/alxdrcirilo/apple-health-parser/main/docs/assets/images/header.png" alt="header" width=720 />

*Python package to parse, analyse, and plot Apple HealthKit data*

![pypi - version](https://img.shields.io/pypi/v/apple-health-parser)
[![coverage](https://coveralls.io/repos/github/alxdrcirilo/apple-health-parser/badge.svg?branch=main)](https://coveralls.io/github/alxdrcirilo/apple-health-parser?branch=main)
[![python version](https://img.shields.io/badge/python-3.11|3.12-blue)](https://www.python.org/)
[![poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![pypi - downloads](https://img.shields.io/pypi/dm/apple-health-parser)
[![license](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

----

Source: [https://github.com/alxdrcirilo/apple-health-parser](https://github.com/alxdrcirilo/apple-health-parser) \
Documentation: [https://alxdrcirilo.dev/apple-health-parser](https://alxdrcirilo.dev/apple-health-parser)

----

The *Apple Health Parser* Python package simplifies the extraction and analysis of health data exported from [Apple HealthKit](https://developer.apple.com/documentation/healthkit). Designed for seamless integration into data science workflows and health analytics applications, this package offers robust parsing and plotting capabilities for various health metrics stored in the Apple Health export XML format.

In a nutshell, *Apple Health Parser* is capable of:

- Extraction and processing of health data from the Apple HealthKit (i.e. `export.zip`)
- Parsing and validation of health records
- Plotting (optionally interactive) health records
- Exporting plots and tables from the parsed health records

Additionally, it also comes with a CLI for the terminal geeks.

> :warning: This package is still in **active development** and has not been tested on real data coming from different sources, nor has it been tested with data originating from versions of iOS < 17.
