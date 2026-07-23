# CLAUDE.md

## Important instructions

* Use best subagent available for each task.
* Ask the user any question to clarify.
* This project uses [Backlog.md](https://github.com/MrLesk/Backlog.md).

## Python Engineering Standards

This is a Python project. Follow these standards for all work.

### Environment & dependencies

* Pin the Python version (`.python-version` and `requires-python` in `pyproject.toml`).
* Lock every dependency with `uv` (preferred) or `pip-tools`, and install **only** from the lockfile so environments stay reproducible (`uv sync --frozen`).
* Separate runtime dependencies from dev/test dependencies (use dependency groups).
* Commit the lockfile (`uv.lock` / compiled `requirements*.txt`). Never commit virtual environments.

### Lint, format & types

* Lint and format with `ruff` (`ruff check` and `ruff format`).
* Type-check with `mypy` or `pyright`.

### Security

* Scan dependencies for CVEs with `pip-audit`.
* Catch insecure code patterns with `bandit`.
* Block leaked credentials with `gitleaks`.
* Read secrets from the environment — **never** hardcode them in source.
* Keep dependencies patched with Dependabot or Renovate.

### Testing

* Test with `pytest`. Keep a fast unit suite that avoids network and database access.
* Measure coverage with `pytest-cov` and fail the build below a realistic floor (≥ 80%).

### Automation

* Wire all checks above into `pre-commit` hooks locally.
* Enforce the **identical** checks in CI as the merge gate, across every supported Python version.

<!-- BACKLOG.MD GUIDELINES START -->
<!-- backlog.md-instructions-version: 1.48.0 -->
<CRITICAL_INSTRUCTION>

## Backlog.md Workflow

This project uses Backlog.md for task and project management.

**For every user request in this project, run `backlog instructions overview` before answering or taking action.**

Use the overview to decide whether to search, read, create, or update Backlog tasks.

Before task lifecycle actions, read the matching detailed guide:
- `backlog instructions task-creation` before creating or splitting tasks
- `backlog instructions task-execution` before planning, changing status or assignee, adding a plan or implementation notes, or implementing task work
- `backlog instructions task-finalization` before checking acceptance criteria, writing final summaries, or moving tasks to terminal statuses

Use `backlog <command> --help` before running unfamiliar commands. Help shows options, fields, and examples.

Do not edit Backlog task, draft, document, decision, or milestone markdown files directly. Use the `backlog` CLI so metadata, relationships, and history stay consistent.

</CRITICAL_INSTRUCTION>
<!-- BACKLOG.MD GUIDELINES END -->
