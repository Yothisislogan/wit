from __future__ import annotations

import os
from dataclasses import dataclass


def _bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = os.environ.get("APP_NAME", "P&C License Prep Academy")
    app_base_url: str = os.environ.get("APP_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./pc_prep_v2.db")
    session_secret: str = os.environ.get("SESSION_SECRET", "change-me-in-production")
    cors_origins: str = os.environ.get("CORS_ORIGINS", "*")
    enable_dev_login: bool = _bool("ENABLE_DEV_LOGIN", True)

    google_client_id: str = os.environ.get("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    microsoft_client_id: str = os.environ.get("MICROSOFT_CLIENT_ID", "")
    microsoft_client_secret: str = os.environ.get("MICROSOFT_CLIENT_SECRET", "")
    facebook_client_id: str = os.environ.get("FACEBOOK_CLIENT_ID", "")
    facebook_client_secret: str = os.environ.get("FACEBOOK_CLIENT_SECRET", "")

    ollama_base_url: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    ollama_model: str = os.environ.get("OLLAMA_MODEL", "deepseek-r1:7b")
    ollama_max_tokens: int = _int("OLLAMA_MAX_TOKENS", 700)

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()] or ["*"]

    def oauth_configured(self, provider: str) -> bool:
        return bool(getattr(self, f"{provider}_client_id", "") and getattr(self, f"{provider}_client_secret", ""))

    @property
    def tutor_mode(self) -> str:
        return "ollama"

    gemini_api_key: str = os.environ.get("GEMINI_API_KEY", "")
    gemini_model: str = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    coverage_coach_provider: str = os.environ.get("COVERAGE_COACH_PROVIDER", "gemini")

    @property
    def openai_api_key(self) -> str:
        return os.environ.get("OPENAI_API_KEY", "")

    @property
    def openai_model(self) -> str:
        return os.environ.get("OPENAI_MODEL", self.ollama_model)

    @property
    def openai_max_output_tokens(self) -> int:
        return self.ollama_max_tokens


settings = Settings()
