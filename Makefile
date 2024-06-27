.PHONY: format

SRC = apple_health_parser
VENV = .venv
TESTS = tests
MYPY_CACHE = .mypy_cache

install: ## Create virtual environment
	poetry install

venv: install ## Activate virtual environment
	poetry shell

clean: ## Clean up
	pyclean . --debris
	rm -rf $(MYPY_CACHE) $(VENV)

format: venv ## Format code
	ruff check --fix $(SRC) $(TESTS)
	ruff format $(SRC) $(TESTS)

test: venv ## Run tests
	pytest -s $(TESTS) --cov=$(SRC) --cov-report=term-missing --cov-report=html

test-fixtures: venv ## Show tests fixtures
	pytest --fixtures

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
