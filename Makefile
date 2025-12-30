.PHONY: install clean lint format type check test test-fixtures docs doctor help

SRC = apple_health_parser
VENV = .venv
TESTS = tests
MYPY_CACHE = .mypy_cache

install: ## Create virtual environment and install dependencies
	uv venv
	uv sync --all-extras --dev

clean: ## Clean up
	uv run pyclean . --debris
	rm -rf $(MYPY_CACHE) $(VENV) uv.lock

lint: ## Lint code
	uv run ruff check $(SRC) $(TESTS)

format: ## Format code
	uv run ruff check --fix $(SRC) $(TESTS)
	uv run ruff format $(SRC) $(TESTS)

type: ## Type check code
	uv run mypy $(SRC)

check: lint format type test ## Run all checks (lint, format, type, test)

docs: ## Generate documentation
	uv run mkdocs serve

test: ## Run tests
	uv run pytest -sx $(TESTS) --cov=$(SRC) --cov-report=term-missing --cov-report=html

test-fixtures: ## Show tests fixtures
	uv run pytest --fixtures

doctor: ## Check environment setup
	@echo "Checking environment..."
	@printf "  %-8s" "uv:" && uv --version || echo "NOT FOUND"
	@printf "  %-8s" "python:" && uv run python --version || echo "NOT FOUND"
	@printf "  %-8s" "venv:" && (test -d $(VENV) && echo "OK") || echo "NOT FOUND (run 'make install')"
	@printf "  %-8s" "deps:" && (uv sync --all-extras --dev --quiet && echo "OK") || echo "OUT OF SYNC"
	@printf "  %-8s" "lint:" && (uv run ruff check $(SRC) $(TESTS) --quiet && echo "OK") || echo "FAILED"
	@printf "  %-8s" "type:" && (uv run mypy $(SRC) --no-error-summary 2>/dev/null && echo "OK") || echo "FAILED"
	@printf "  %-8s" "test:" && (uv run pytest $(TESTS) -q --tb=no >/dev/null 2>&1 && echo "OK") || echo "FAILED"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
