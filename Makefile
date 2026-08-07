.DEFAULT_GOAL := help

# Thin wrappers around the commands used most often. Run `make` or `make help`.
.PHONY: help sync lock run test test-integration lint format format-check typecheck check build up down logs clean reset reset-hard

# --- Deployment resource tier -------------------------------------------------
# DEPLOY_ENV selects a per-VPS resource profile (environments/<tier>.env), loaded
# into Compose next to .env. Read from .env; override per-invocation, e.g.
# `make up DEPLOY_ENV=small`. Defaults to medium.
DEPLOY_ENV ?= $(shell sed -n 's/^DEPLOY_ENV=//p' .env 2>/dev/null | tail -n1)
DEPLOY_ENV := $(if $(strip $(DEPLOY_ENV)),$(strip $(DEPLOY_ENV)),medium)
# The tier file supplies the per-service CPU/memory vars; .env (loaded last, so
# it wins) supplies app settings/secrets and can override any single tier value.
# Inline $(VAR:-default)s in compose/*.yaml keep a bare `docker compose` working
# (medium defaults) for anyone not using make.
COMPOSE := docker compose --env-file environments/$(DEPLOY_ENV).env $(if $(wildcard .env),--env-file .env)

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
	$(COMPOSE) build

up: ## Start the full stack (Qdrant + app) in the background
	$(COMPOSE) up --build -d

down: ## Stop the stack
	$(COMPOSE) down

logs: ## Follow the app logs
	$(COMPOSE) logs -f app qdrant

clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov dist build

reset: ## Wipe storage/ EXCEPT the Ollama models (keeps storage/ollama to avoid re-downloading); deletes qdrant + opencode data and stops the stack; rebuild with `make up`
	@echo "WARNING: this will delete storage/ (qdrant, opencode data), including all ingested Qdrant data and opencode state (auth/sessions)."; \
	echo "The Ollama models in storage/ollama are PRESERVED (use 'make reset-hard' to also delete them). These will be rebuilt from scratch on the next 'make up'."; \
	read -p "Proceed? [y/N] " reply; \
	if [ "$$reply" = "y" ] || [ "$$reply" = "Y" ]; then \
		$(COMPOSE) down --remove-orphans && \
		mkdir -p storage && \
		find storage -mindepth 1 -maxdepth 1 ! -name ollama ! -name .gitkeep -exec rm -rf {} + && \
		touch storage/.gitkeep && \
		echo "Reset complete."; \
	else \
		echo "Aborted. Nothing was deleted."; \
	fi

reset-hard: ## Like reset, plus remove the built app image and prune dangling images/build cache for a from-scratch rebuild
	@echo "WARNING: unlike 'reset', this will delete storage/ (qdrant, ollama, opencode data) ENTIRELY, including the ~17GB Ollama model, all ingested Qdrant data, and opencode state (auth/sessions)."; \
	echo "AND remove the locally-built app image and prune dangling images and build cache."; \
	echo "These will be rebuilt from scratch on the next 'make up'."; \
	read -p "Proceed? [y/N] " reply; \
	if [ "$$reply" = "y" ] || [ "$$reply" = "Y" ]; then \
		$(COMPOSE) down --rmi local --remove-orphans && \
		rm -rf storage && \
		mkdir -p storage && \
		touch storage/.gitkeep && \
		docker image prune -f && \
		docker builder prune -f && \
		echo "Hard reset complete."; \
	else \
		echo "Aborted. Nothing was deleted."; \
	fi
