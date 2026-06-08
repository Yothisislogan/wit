#!/usr/bin/env bash
# Start the voice pipeline service on port 8001
# Uses the .venv-voice virtualenv (Python 3.12 with Kokoro + faster-whisper)
cd "$(dirname "$0")/.."
exec .venv-voice/bin/uvicorn voice_service.main:app \
    --host 0.0.0.0 \
    --port 8001 \
    --workers 1 \
    --log-level info
