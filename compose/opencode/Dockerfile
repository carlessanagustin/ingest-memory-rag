FROM ubuntu:26.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN curl -fsSL https://opencode.ai/install | bash
RUN curl -fsSL https://claude.ai/install.sh | bash

ENV PATH="/root/.opencode/bin:/root/.local/bin:${PATH}"

RUN uv python install 3.12 && \
    uv tool install --python 3.12 mcp-server-qdrant@0.8.1 && \
    uv venv /opt/uv-venv --python 3.12 && \
    uv pip install --python /opt/uv-venv/bin/python pydantic_core

RUN opencode --version && \
    claude --version