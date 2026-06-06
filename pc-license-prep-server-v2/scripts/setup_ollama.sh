#!/usr/bin/env bash
set -euo pipefail

MODEL="${OLLAMA_MODEL:-deepseek-r1:7b}"
PORT="${OLLAMA_PORT:-11434}"

echo "Installing or updating Ollama..."
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl enable ollama || true
  sudo systemctl start ollama || true
fi

echo "Waiting for Ollama API..."
for i in $(seq 1 20); do
  if curl -sf "http://localhost:${PORT}/api/tags" >/dev/null; then
    break
  fi
  sleep 1
  if [ "$i" = "20" ]; then
    echo "Ollama did not respond on localhost:${PORT}."
    exit 1
  fi
done

echo "Pulling model: ${MODEL}"
ollama pull "${MODEL}"

echo "Done. Use OLLAMA_BASE_URL=http://localhost:${PORT}/v1 and OLLAMA_MODEL=${MODEL}."
