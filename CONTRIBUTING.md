# Contributing

## Development setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
# Install dependencies
make install

# Run all checks (lint, format, type, test)
make check

# Verify environment setup
make doctor
```

## Code style

Follow the code style of the project.

The project is linted and formatted using [`ruff`](https://docs.astral.sh/ruff). Simply run `make format` to format the entire project.

## Issues

For any issue and/or feature, please double-check that there isn't already an open ticket for it in the [issues](https://github.com/alxdrcirilo/apple-health-parser/issues) tab.

### Creating a bug report

Fill in the [Bug report](https://github.com/alxdrcirilo/apple-health-parser/issues/new/choose) template. Be sure to add any helpful details.

### Requesting a new feature

Fill in the [Feature request](https://github.com/alxdrcirilo/apple-health-parser/issues/new/choose) template.
Be mindful that new features will not always be considered if they offer little added value to the package.

## Pull requests

Approved pull requests will be squashed into one single commit with a [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) compliant commit message.
Be sure to mention the GitHub issue you're fixing if one was already open.
