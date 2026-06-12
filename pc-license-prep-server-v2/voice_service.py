#!/usr/bin/env python3
"""
voice_service.py — Qwen3-TTS voice backend for WIT
Replaces Kokoro. Runs on port 8001.
Serves:
  GET  /voices          — list available voices
  POST /tts             — generate speech
  GET  /health          — liveness check

Start with:
  .venv-voice/bin/python3 voice_service.py
"""
import io
import logging
import os
import tempfile

import soundfile as sf
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("voice_service")

# ── VOICES ────────────────────────────────────────────────────────────────────

VOICES = [
    {"id": "Vivian",   "name": "Vivian",    "description": "Bright, slightly edgy young female", "language": "Chinese"},
    {"id": "Serena",   "name": "Serena",    "description": "Warm, gentle young female",            "language": "Chinese"},
    {"id": "Uncle_Fu", "name": "Uncle Fu",  "description": "Seasoned male, low mellow timbre",     "language": "Chinese"},
    {"id": "Dylan",    "name": "Dylan",     "description": "Youthful Beijing male, clear",          "language": "Chinese (Beijing)"},
    {"id": "Eric",     "name": "Eric",      "description": "Lively Chengdu male, slightly husky",  "language": "Chinese (Sichuan)"},
    {"id": "Ryan",     "name": "Ryan",      "description": "Dynamic male with strong rhythmic drive","language": "English"},
    {"id": "Aiden",    "name": "Aiden",     "description": "Sunny American male, clear midrange",  "language": "English"},
    {"id": "Ono_Anna", "name": "Ono Anna",  "description": "Playful Japanese female, light nimble","language": "Japanese"},
    {"id": "Sohee",    "name": "Sohee",     "description": "Warm Korean female, rich emotion",     "language": "Korean"},
]

DEFAULT_VOICE = "Ryan"  # Best for English insurance content

# ── MODEL LOADING ─────────────────────────────────────────────────────────────

MODEL_ID = os.environ.get("QWEN_TTS_MODEL", "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice")
# Use 1.7B on GPU VPS: QWEN_TTS_MODEL=Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice

log.info(f"Loading Qwen3-TTS model: {MODEL_ID}")
log.info("First run will download ~1.5-4.5GB from HuggingFace. Subsequent runs use cache.")

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32

try:
    from qwen_tts import Qwen3TTSModel
    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID,
        device_map=device,
        dtype=dtype,
    )
    log.info(f"Qwen3-TTS loaded on {device}")
except Exception as e:
    log.error(f"Failed to load Qwen3-TTS: {e}")
    model = None

# ── APP ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="WIT Voice Service (Qwen3-TTS)", version="3.0.0")


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    voice: str = Field(default=DEFAULT_VOICE)
    instruct: str = Field(default="")   # Optional emotion/style instruction
    language: str = Field(default="English")
    format: str = Field(default="wav")  # wav only for now


@app.get("/health")
def health():
    return {
        "ok": model is not None,
        "model": MODEL_ID,
        "device": device,
        "voices": len(VOICES),
    }


@app.get("/voices")
def list_voices():
    return {"voices": VOICES, "default": DEFAULT_VOICE}


@app.post("/tts")
def synthesize(req: TTSRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="TTS model not loaded")

    # Validate voice
    valid_ids = {v["id"] for v in VOICES}
    voice = req.voice if req.voice in valid_ids else DEFAULT_VOICE

    log.info(f"TTS: voice={voice} lang={req.language} len={len(req.text)}")

    try:
        wavs, sr = model.generate_custom_voice(
            text=req.text,
            language=req.language,
            speaker=voice,
            instruct=req.instruct if req.instruct else None,
        )
    except Exception as e:
        log.error(f"TTS generation error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")

    # Write WAV to memory buffer
    buf = io.BytesIO()
    sf.write(buf, wavs[0], sr, format="WAV")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=speech.wav"},
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("VOICE_PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
