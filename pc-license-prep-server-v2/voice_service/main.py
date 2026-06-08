# Voice pipeline: faster-whisper STT → Ollama/DeepSeek LLM → Kokoro TTS
# Runs on port 8001 alongside the main app (port 8000)
from __future__ import annotations

import base64
import io
import json
import logging
import os
import re
import subprocess
import tempfile
import time
from contextlib import asynccontextmanager
from typing import Any

import httpx
import numpy as np
import soundfile as sf
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("voice")

OLLAMA_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1/chat/completions")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-r1:7b")

VOICE_COACH_SYSTEM = (
    "You are Coverage Coach, a friendly P&C insurance licensing exam tutor. "
    "Keep answers concise (2-4 sentences) since they will be spoken aloud. "
    "Avoid bullet points, headers, or markdown. "
    "Speak naturally as if talking to a student. "
    "Focus on helping them understand and remember concepts for the licensing exam."
)

KOKORO_VOICES = [
    "af_heart", "af_bella", "af_nova", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_liam",
    "bf_emma", "bm_george", "bm_lewis",
]

# Global model handles — loaded once at startup
_whisper_model = None
_kokoro_pipeline = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _whisper_model, _kokoro_pipeline

    t0 = time.time()
    log.info("Loading faster-whisper model (base, CPU, int8)…")
    try:
        from faster_whisper import WhisperModel
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        log.info("faster-whisper loaded in %.1fs", time.time() - t0)
    except Exception as e:
        log.error("faster-whisper failed to load: %s", e)

    t1 = time.time()
    log.info("Loading Kokoro TTS pipeline…")
    try:
        from kokoro import KPipeline
        _kokoro_pipeline = KPipeline(lang_code="a")
        log.info("Kokoro loaded in %.1fs", time.time() - t1)
    except Exception as e:
        log.error("Kokoro failed to load: %s", e)

    log.info("Voice service ready (total startup %.1fs)", time.time() - t0)
    yield


app = FastAPI(title="P&C Voice Pipeline", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text or "", flags=re.DOTALL).strip()


def _strip_markdown(text: str) -> str:
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"`[^`]*`", lambda m: m.group(0)[1:-1], text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _convert_to_wav(input_bytes: bytes, suffix: str = ".webm") -> bytes:
    """Convert browser audio (webm/wav/ogg) to 16kHz mono WAV via ffmpeg."""
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as fin:
        fin.write(input_bytes)
        in_path = fin.name
    out_path = in_path + ".wav"
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", in_path, "-ar", "16000", "-ac", "1", "-f", "wav", out_path],
            capture_output=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg error: {result.stderr.decode()[:400]}")
        with open(out_path, "rb") as f:
            return f.read()
    finally:
        os.unlink(in_path)
        if os.path.exists(out_path):
            os.unlink(out_path)


def _transcribe(wav_bytes: bytes) -> dict[str, Any]:
    if _whisper_model is None:
        raise RuntimeError("Whisper model not loaded")
    t0 = time.time()
    audio_buf = io.BytesIO(wav_bytes)
    audio_np, sr = sf.read(audio_buf, dtype="float32")
    if sr != 16000:
        raise RuntimeError(f"Expected 16kHz audio, got {sr}Hz")
    segments, info = _whisper_model.transcribe(audio_np, beam_size=5, language="en")
    text = " ".join(seg.text for seg in segments).strip()
    elapsed = time.time() - t0
    log.info("Transcription (%.1fs): %r", elapsed, text[:120])
    return {
        "text": text,
        "language": info.language,
        "duration_seconds": round(info.duration, 2),
        "transcribe_ms": round(elapsed * 1000),
    }


def _synth_wav(text: str, voice: str = "af_heart") -> bytes:
    if _kokoro_pipeline is None:
        raise RuntimeError("Kokoro pipeline not loaded")
    if voice not in KOKORO_VOICES:
        voice = "af_heart"
    text = _strip_markdown(text)[:1000]
    t0 = time.time()
    audio_chunks = []
    for _, _, audio in _kokoro_pipeline(text, voice=voice, speed=1.0):
        if audio is not None:
            audio_chunks.append(audio)
    if not audio_chunks:
        raise RuntimeError("Kokoro produced no audio")
    audio_np = np.concatenate(audio_chunks)
    buf = io.BytesIO()
    sf.write(buf, audio_np, 24000, format="wav", subtype="PCM_16")
    elapsed = time.time() - t0
    log.info("TTS (%.1fs): %d chars → %d samples", elapsed, len(text), len(audio_np))
    return buf.getvalue()


async def _ask_ollama(messages: list[dict]) -> str:
    t0 = time.time()
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "max_tokens": 300,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"]
    text = _strip_think(raw)
    elapsed = time.time() - t0
    log.info("LLM (%.1fs): %r", elapsed, text[:120])
    return text


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "whisper": "loaded" if _whisper_model is not None else "unavailable",
        "kokoro": "loaded" if _kokoro_pipeline is not None else "unavailable",
        "voices": KOKORO_VOICES,
    }


@app.get("/voices")
def voices() -> list[str]:
    return KOKORO_VOICES


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)) -> dict[str, Any]:
    if _whisper_model is None:
        raise HTTPException(status_code=503, detail={"error": "whisper_unavailable"})
    try:
        raw = await audio.read()
        suffix = ".webm" if (audio.content_type or "").startswith("audio/webm") else ".wav"
        t0 = time.time()
        wav_bytes = _convert_to_wav(raw, suffix=suffix)
        log.info("ffmpeg conversion: %.1fs", time.time() - t0)
        result = _transcribe(wav_bytes)
    except Exception as e:
        log.error("Transcription error: %s", e)
        raise HTTPException(status_code=500, detail={"error": str(e)})

    if not result["text"].strip():
        return {"text": "", "error": "no_speech"}
    return result


class SpeakRequest(BaseModel):
    text: str
    voice: str = "af_heart"


@app.post("/speak")
def speak(req: SpeakRequest) -> Response:
    if _kokoro_pipeline is None:
        raise HTTPException(status_code=503, detail={"error": "kokoro_unavailable"})
    try:
        wav = _synth_wav(req.text, voice=req.voice)
    except Exception as e:
        log.error("TTS error: %s", e)
        raise HTTPException(status_code=500, detail={"error": str(e)})
    return Response(content=wav, media_type="audio/wav")


@app.post("/chat")
async def chat(
    audio: UploadFile = File(...),
    voice: str = Form(default="af_heart"),
    conversation_history: str = Form(default="[]"),
) -> dict[str, Any]:
    t_start = time.time()

    # 1. Transcribe
    if _whisper_model is None:
        raise HTTPException(status_code=503, detail={"error": "whisper_unavailable"})
    try:
        raw = await audio.read()
        suffix = ".webm" if (audio.content_type or "").startswith("audio/webm") else ".wav"
        wav_bytes = _convert_to_wav(raw, suffix=suffix)
        stt_result = _transcribe(wav_bytes)
    except Exception as e:
        log.error("STT error: %s", e)
        raise HTTPException(status_code=500, detail={"error": f"stt_failed: {e}"})

    transcript = stt_result.get("text", "").strip()
    if not transcript:
        return {"error": "no_speech"}

    # 2. LLM
    try:
        history = json.loads(conversation_history) if conversation_history else []
    except Exception:
        history = []
    messages = [{"role": "system", "content": VOICE_COACH_SYSTEM}]
    messages.extend(history[-6:])  # keep last 3 turns for context
    messages.append({"role": "user", "content": transcript})

    try:
        response_text = await _ask_ollama(messages)
    except Exception as e:
        log.error("LLM error: %s", e)
        raise HTTPException(status_code=500, detail={"error": f"llm_failed: {e}"})

    # 3. TTS
    if _kokoro_pipeline is None:
        raise HTTPException(status_code=503, detail={"error": "kokoro_unavailable"})
    try:
        wav_bytes = _synth_wav(response_text, voice=voice)
    except Exception as e:
        log.error("TTS error: %s", e)
        raise HTTPException(status_code=500, detail={"error": f"tts_failed: {e}"})

    audio_b64 = base64.b64encode(wav_bytes).decode()
    log.info("Full pipeline: %.1fs", time.time() - t_start)

    return {
        "transcript": transcript,
        "response_text": response_text,
        "audio_base64": audio_b64,
    }
