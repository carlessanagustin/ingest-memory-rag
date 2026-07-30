.DEFAULT_GOAL := help

# Thin wrappers around the commands used most often. Run `make` or `make help`.
.PHONY: help sync lock run test test-integration lint format format-check typecheck check build up down logs clean reset reset-hard

help: ## List available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

sync: ## Install runtime + dev dependencies from the lockfile
	uv sync --frozen

lock: ## Update the dependency lockfile
	uv lock

run: ## Run the watcher locally (needs Qdrant at QDRANT_URL)
	uv run ingest-memory-rag

test: ## Run the fast unit suite (no network / no Qdrant)
	uv run pytest -m "not integration"

test-integration: ## Run integration tests against a live Qdrant
	uv run pytest -m integration --no-cov

lint: ## Lint with ruff
	uv run ruff check .

format: ## Auto-format with ruff
	uv run ruff format .

format-check: ## Check formatting without writing (CI mode)
	uv run ruff format --check .

typecheck: ## Type-check with mypy
	uv run mypy

check: lint format-check typecheck test ## Run the full CI gate (lint, format, types, unit tests)

build: ## Build the app image
	docker compose build

up: ## Start the full stack (Qdrant + app) in the background
	docker compose up --build -d

down: ## Stop the stack
	docker compose down

logs: ## Follow the app logs
	docker compose logs -f app qdrant

clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov dist build

reset: ## Wipe storage_qdrant/, storage_ollama/ and storage_openwebui/ (deletes the pulled model + ingested vectors + OpenWebUI state) and stop the stack; rebuild with `make up`
	@echo "WARNING: this will delete storage_qdrant/, storage_ollama/ and storage_openwebui/, including the ~17GB Ollama model, all ingested Qdrant data, and OpenWebUI state."; \
	echo "These will be rebuilt from scratch on the next 'make up'."; \
	read -p "Proceed? [y/N] " reply; \
	if [ "$$reply" = "y" ] || [ "$$reply" = "Y" ]; then \
		docker compose down --remove-orphans && \
		rm -rf storage_qdrant storage_ollama storage_openwebui && \
		mkdir -p storage_qdrant storage_ollama storage_openwebui && \
		touch storage_qdrant/.gitkeep storage_ollama/.gitkeep storage_openwebui/.gitkeep && \
		echo "Reset complete."; \
	else \
		echo "Aborted. Nothing was deleted."; \
	fi

reset-hard: ## Like reset, plus remove the built app image and prune dangling images/build cache for a from-scratch rebuild
	@echo "WARNING: this will delete storage_qdrant/, storage_ollama/ and storage_openwebui/, including the ~17GB Ollama model, all ingested Qdrant data, and OpenWebUI state,"; \
	echo "AND remove the locally-built app image and prune dangling images and build cache."; \
	echo "These will be rebuilt from scratch on the next 'make up'."; \
	read -p "Proceed? [y/N] " reply; \
	if [ "$$reply" = "y" ] || [ "$$reply" = "Y" ]; then \
		docker compose down --rmi local --remove-orphans && \
		rm -rf storage_qdrant storage_ollama storage_openwebui && \
		mkdir -p storage_qdrant storage_ollama storage_openwebui && \
		touch storage_qdrant/.gitkeep storage_ollama/.gitkeep storage_openwebui/.gitkeep && \
		docker image prune -f && \
		docker builder prune -f && \
		echo "Hard reset complete."; \
	else \
		echo "Aborted. Nothing was deleted."; \
	fi
