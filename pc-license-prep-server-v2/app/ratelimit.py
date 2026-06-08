from __future__ import annotations

import time
from collections import defaultdict

from fastapi import HTTPException

_rate_limits: dict[str, list[float]] = defaultdict(list)


def rate_limit(key: str, max_calls: int, window_seconds: int) -> None:
    now = time.time()
    _rate_limits[key] = [t for t in _rate_limits[key] if now - t < window_seconds]
    if len(_rate_limits[key]) >= max_calls:
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a moment.")
    _rate_limits[key].append(now)
