#!/usr/bin/env bash
set -euo pipefail

CONFIG="${OPENCODE_CONFIG:-/config/opencode.json}"

export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq jq >/dev/null

if [[ ! -f "$CONFIG" ]]; then
  echo "No opencode config found at $CONFIG, skipping model pull."
  exit 0
fi

mapfile -t models < <(jq -r '.provider.ollama.models // {} | keys[]' "$CONFIG")

if [[ ${#models[@]} -eq 0 ]]; then
  echo "No models found under provider.ollama.models in $CONFIG, skipping model pull."
  exit 0
fi

echo "Models to pull: ${models[*]}"

for m in "${models[@]}"; do
  echo "==> ollama pull $m"
  ollama pull "$m"
done

echo "All models pulled successfully."
