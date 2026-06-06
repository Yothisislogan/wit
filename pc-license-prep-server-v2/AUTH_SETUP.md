# SSO Setup

V2 is built for Google, Microsoft, and Facebook sign-in.

## Local development

Run locally with the development login:

```text
http://127.0.0.1:8000/auth/dev-login
```

For production, set:

```text
ENABLE_DEV_LOGIN=false
```

## Google OAuth

Callback URL:

```text
https://your-domain.com/auth/callback/google
```

Environment variables:

```text
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Microsoft OAuth

Callback URL:

```text
https://your-domain.com/auth/callback/microsoft
```

Environment variables:

```text
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
```

## Facebook OAuth

Callback URL:

```text
https://your-domain.com/auth/callback/facebook
```

Environment variables:

```text
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
```

## Required production variables

```text
APP_BASE_URL=https://your-domain.com
SESSION_SECRET=use-a-long-random-secret
DATABASE_URL=postgresql+psycopg://user:password@host:5432/database
CORS_ORIGINS=https://your-domain.com
ENABLE_DEV_LOGIN=false
```

## Privacy position

Because the platform is free, collect as little data as possible:

- name
- email
- avatar URL if provided
- OAuth provider ID
- course progress
- quiz attempts
- mistake history

Do not collect payment data because this project is not paid.
