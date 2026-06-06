from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from .models import OAuthAccount, User
from .settings import settings


oauth = OAuth()

if settings.oauth_configured("google"):
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

if settings.oauth_configured("microsoft"):
    oauth.register(
        name="microsoft",
        client_id=settings.microsoft_client_id,
        client_secret=settings.microsoft_client_secret,
        server_metadata_url="https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile User.Read"},
    )

if settings.oauth_configured("facebook"):
    oauth.register(
        name="facebook",
        client_id=settings.facebook_client_id,
        client_secret=settings.facebook_client_secret,
        access_token_url="https://graph.facebook.com/v19.0/oauth/access_token",
        authorize_url="https://www.facebook.com/v19.0/dialog/oauth",
        api_base_url="https://graph.facebook.com/v19.0/",
        client_kwargs={"scope": "email public_profile"},
    )


def configured_providers() -> list[dict[str, Any]]:
    return [
        {"id": "google", "name": "Google", "configured": settings.oauth_configured("google")},
        {"id": "microsoft", "name": "Microsoft", "configured": settings.oauth_configured("microsoft")},
        {"id": "facebook", "name": "Facebook", "configured": settings.oauth_configured("facebook")},
    ]


def require_user(request: Request, db: Session) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Please sign in first")
    user = db.get(User, int(user_id))
    if not user:
        request.session.clear()
        raise HTTPException(status_code=401, detail="Please sign in first")
    return user


def public_user(user: User) -> dict[str, Any]:
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "avatar_url": user.avatar_url,
        "is_admin": user.is_admin,
    }


def upsert_oauth_user(db: Session, provider: str, profile: dict[str, Any]) -> User:
    provider_user_id = str(profile["provider_user_id"])
    email = profile.get("email")
    name = profile.get("name") or email or "Student"
    avatar_url = profile.get("avatar_url")

    account = db.scalar(
        select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_user_id == provider_user_id,
        )
    )
    if account:
        user = account.user
        user.email = email or user.email
        user.name = name or user.name
        user.avatar_url = avatar_url or user.avatar_url
        user.last_login_at = datetime.now(timezone.utc)
        db.commit()
        return user

    user = None
    if email:
        user = db.scalar(select(User).where(User.email == email))

    if not user:
        user_count = db.scalar(select(User.id).limit(1))
        user = User(
            email=email,
            name=name,
            avatar_url=avatar_url,
            is_admin=False if user_count else True,
            last_login_at=datetime.now(timezone.utc),
        )
        db.add(user)
        db.flush()

    db.add(OAuthAccount(
        user_id=user.id,
        provider=provider,
        provider_user_id=provider_user_id,
        email=email,
    ))
    db.commit()
    db.refresh(user)
    return user


async def login_redirect(request: Request, provider: str):
    if provider not in {"google", "microsoft", "facebook"}:
        raise HTTPException(status_code=404, detail="Unknown provider")
    if not settings.oauth_configured(provider):
        raise HTTPException(status_code=501, detail=f"{provider} OAuth is not configured yet")
    redirect_uri = f"{settings.app_base_url}/auth/callback/{provider}"
    client = oauth.create_client(provider)
    return await client.authorize_redirect(request, redirect_uri)


async def oauth_callback(request: Request, db: Session, provider: str):
    if provider not in {"google", "microsoft", "facebook"}:
        raise HTTPException(status_code=404, detail="Unknown provider")
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)

    if provider in {"google", "microsoft"}:
        info = token.get("userinfo") or await client.userinfo(token=token)
        profile = {
            "provider_user_id": info.get("sub") or info.get("id"),
            "email": info.get("email") or info.get("preferred_username"),
            "name": info.get("name"),
            "avatar_url": info.get("picture"),
        }
    else:
        response = await client.get("me?fields=id,name,email,picture", token=token)
        info = response.json()
        profile = {
            "provider_user_id": info.get("id"),
            "email": info.get("email"),
            "name": info.get("name"),
            "avatar_url": ((info.get("picture") or {}).get("data") or {}).get("url"),
        }

    if not profile.get("provider_user_id"):
        raise HTTPException(status_code=400, detail="Provider did not return a user id")

    user = upsert_oauth_user(db, provider, profile)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/")


def dev_login(request: Request, db: Session):
    if not settings.enable_dev_login:
        raise HTTPException(status_code=404, detail="Development login is disabled")
    profile = {
        "provider_user_id": "dev-user",
        "email": "dev@example.com",
        "name": "Demo Student",
        "avatar_url": None,
    }
    user = upsert_oauth_user(db, "dev", profile)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/")
