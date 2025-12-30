# Repository Guidelines

See [CLAUDE.md](CLAUDE.md) for build commands and architecture details.

## Coding Style

- Python 3.11+ with 4-space indentation
- Format and lint with `ruff` (`make format`)
- Type hints required; checked with `mypy` (`make type`)
- Naming: `snake_case` for modules/functions, `PascalCase` for classes, `UPPER_SNAKE` for constants

## Commit & PR Guidelines

- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) (e.g., `feat:`, `fix:`, `build(deps):`)
- PRs are squashed into a single conventional commit
- Include related issue link if one exists

## Data Privacy

- Apple Health exports contain sensitive personal data
- Never commit real health exports
- Keep test fixtures small and anonymized in `tests/data/`
