FROM ubuntu:26.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://opencode.ai/install | bash
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.opencode/bin:${PATH}"

RUN opencode --version
