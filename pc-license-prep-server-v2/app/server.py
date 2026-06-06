from __future__ import annotations

from .main import app
from .studio import router as studio_router

app.include_router(studio_router)
