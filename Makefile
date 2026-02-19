.PHONY: install venv clean format lint test test-fixtures help

SRC = apple_health_parser
VENV = .venv
TESTS = tests
MYPY_CACHE = .mypy_cache

install: ## Run the application
	uv sync

clean: ## Clean up
	pyclean . --debris
	rm -rf $(MYPY_CACHE) $(VENV)

lint: install ## Lint code with ruff
	ruff check $(SRC) $(TESTS)

format: install ## Format and auto-fix code with ruff
	ruff check --fix $(SRC) $(TESTS)
	ruff format $(SRC) $(TESTS)

docs: install ## Generate documentation
	mkdocs serve

test: install ## Run tests
	uv run pytest -sx $(TESTS) --cov=$(SRC) --cov-report=term-missing --cov-report=html

test-fixtures: install ## Show tests fixtures
	uv run pytest --fixtures

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
