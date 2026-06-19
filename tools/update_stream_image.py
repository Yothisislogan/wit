#!/usr/bin/env python3
"""
update_stream_image.py — WIT-FM stream image generator
Generates a 1280x720 stream thumbnail/overlay centered for YouTube Shorts 9:16 safe zone.
Run continuously to keep the stream image current (polls every 30s).
"""
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

# ── PATHS ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ASSET_DIR = BASE_DIR / "assets"
OUTPUT = BASE_DIR / "stream_image.jpg"

FONT_B = str(ASSET_DIR / "fonts" / "Inter-Bold.ttf")
FONT_R = str(ASSET_DIR / "fonts" / "Inter-Regular.ttf")
BG_IMAGE = str(ASSET_DIR / "stream_bg.jpg")
MONSTER_LOGO = str(ASSET_DIR / "monster_logo.png")
DEFAULT_ART = str(ASSET_DIR / "default_art.jpg")

# ── STATION CONFIG ────────────────────────────────────────────────────────────
ICECAST_URL = os.environ.get("ICECAST_STATUS_URL", "http://localhost:8000/status-json.xsl")
UPDATE_INTERVAL = int(os.environ.get("STREAM_IMAGE_INTERVAL", "30"))

THEMES: dict[str, dict] = {
    "default": {"accent": "0x4FC3F7", "label": "WIT-FM • LIVE STREAM"},
    "evening":  {"accent": "0xFFB74D", "label": "WIT-FM • EVENING VIBES"},
    "weekend":  {"accent": "0x33D17A", "label": "WIT-FM • WEEKEND EDITION"},
}


def get_now_playing() -> dict:
    try:
        with urllib.request.urlopen(ICECAST_URL, timeout=5) as r:
            data = json.loads(r.read())
        source = data.get("icestats", {}).get("source", {})
        if isinstance(source, list):
            source = source[0]
        title = source.get("title", "")
        artist, track = ("Unknown", title) if " - " not in title else title.split(" - ", 1)
        return {"title": track.strip(), "artist": artist.strip(), "host": source.get("server_name", "WIT Radio")}
    except Exception:
        return {"title": "Live Insurance Radio", "artist": "WIT-FM", "host": "WIT Radio"}


def _esc(s: str) -> str:
    return s.replace("'", "\\'").replace(":", "\\:").replace("%", "\\%").replace("\\", "\\\\")


def build_image(title: str, artist: str, host: str, art_path: str | None = None, theme: str = "default") -> bool:
    cfg = THEMES.get(theme, THEMES["default"])
    art = art_path if art_path and Path(art_path).exists() else DEFAULT_ART
    title = _esc(title[:60])
    artist = _esc(artist[:60])
    host = _esc(host[:60])

    filter_complex = (
        f"[0]scale=1280:720[bg];"
        f"[bg]drawbox=x=0:y=0:w=1280:h=4:color={cfg['accent']}:t=fill[bg2];"
        f"[bg2]drawbox=x=0:y=716:w=1280:h=4:color={cfg['accent']}@0.4:t=fill[bg3];"
        f"[1]scale=240:240[art];"
        f"[bg3][art]overlay=x=520:y=80[wa];"
        f"[2]scale=80:-1[monster];"
        f"[wa][monster]overlay=x=1160:y=20[wm];"
        f"[wm]"
        f"drawtext=fontfile={FONT_B}:text='WIT Radio':fontsize=72:fontcolor=white:x=(1280-text_w)/2:y=340,"
        f"drawtext=fontfile={FONT_R}:text='We Insure Things Radio':fontsize=20:fontcolor={cfg['accent']}:x=(1280-text_w)/2:y=425,"
        f"drawtext=fontfile={FONT_B}:text='{cfg['label']}':fontsize=16:fontcolor={cfg['accent']}:x=(1280-text_w)/2:y=458,"
        f"drawtext=fontfile={FONT_B}:text='NOW PLAYING':fontsize=13:fontcolor=white:x=(1280-text_w)/2:y=498:alpha=0.6,"
        f"drawtext=fontfile={FONT_B}:text='{title}':fontsize=32:fontcolor=white:x=(1280-text_w)/2:y=520,"
        f"drawtext=fontfile={FONT_R}:text='{artist}':fontsize=20:fontcolor={cfg['accent']}:x=(1280-text_w)/2:y=562,"
        f"drawtext=fontfile={FONT_B}:text='ON AIR\\: {host}':fontsize=18:fontcolor=white:x=(1280-text_w)/2:y=595,"
        f"drawtext=fontfile={FONT_B}:text='● LIVE':fontsize=18:fontcolor=0x33D17A:x=(1280-text_w)/2:y=630,"
        f"drawtext=fontfile={FONT_R}:text='radio.weinsurethings.com':fontsize=14:fontcolor=gray:x=(1280-text_w)/2:y=695"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", BG_IMAGE,
        "-i", art,
        "-i", MONSTER_LOGO,
        "-filter_complex", filter_complex,
        "-frames:v", "1",
        "-q:v", "2",
        str(OUTPUT),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[stream-image] ffmpeg error:\n{result.stderr[-800:]}")
        return False
    return True


def main() -> None:
    print(f"[stream-image] Starting — updating every {UPDATE_INTERVAL}s → {OUTPUT}")
    last: dict = {}
    while True:
        try:
            np = get_now_playing()
            if np != last:
                ok = build_image(np["title"], np["artist"], np["host"])
                if ok:
                    print(f"[stream-image] Updated: {np['artist']} — {np['title']}")
                last = np
        except Exception as exc:
            print(f"[stream-image] Error: {exc}")
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()
