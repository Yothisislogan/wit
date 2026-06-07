#!/usr/bin/env bash
# P&C License Prep Academy — VPS installer
# Tested on Ubuntu 22.04/24.04 (systemd, nginx, Python 3.11+)
# Run as root: bash install.sh

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────
APP_NAME="pc-prep"
APP_DIR="/opt/${APP_NAME}"
RUN_AS="${APP_NAME}"
DB_PATH="${APP_DIR}/data/db.sqlite3"
VENV="${APP_DIR}/.venv"
PORT="8000"
PYTHON="python3"

ok()  { echo -e "\033[32m✔\033[0m  $*"; }
err() { echo -e "\033[31m✘\033[0m  $*" >&2; exit 1; }
hdr() { echo -e "\n\033[1m── $* ──\033[0m"; }

[[ $EUID -eq 0 ]] || err "Run as root (sudo bash install.sh)"

# ── Phase 1 — System packages ──────────────────────────────────────
hdr "Phase 1 — System packages"
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip nginx curl git
ok "Packages ready"

# ── Phase 2 — App user ────────────────────────────────────────────
hdr "Phase 2 — App user"
if ! id "${RUN_AS}" &>/dev/null; then
  useradd --system --shell /usr/sbin/nologin --home "${APP_DIR}" "${RUN_AS}"
  ok "User ${RUN_AS} created"
else
  ok "User ${RUN_AS} already exists"
fi

# ── Phase 3 — App directory ───────────────────────────────────────
hdr "Phase 3 — App directory"
mkdir -p "${APP_DIR}" "${APP_DIR}/data"
cp -r . "${APP_DIR}/"
ok "Files copied to ${APP_DIR}"

# ── Phase 4 — Python environment ─────────────────────────────────
hdr "Phase 4 — Python environment"
${PYTHON} -m venv "${VENV}"
"${VENV}/bin/pip" install --quiet --upgrade pip
"${VENV}/bin/pip" install --quiet -r "${APP_DIR}/requirements.txt"
ok "Python environment ready"

# ── Phase 5 — Environment file ───────────────────────────────────
hdr "Phase 5 — Environment file"
ENV_FILE="${APP_DIR}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
  SECRET=$(${PYTHON} -c "import secrets; print(secrets.token_hex(32))")
  cat > "${ENV_FILE}" <<ENVEOF
SESSION_SECRET=${SECRET}
DATABASE_URL=sqlite:///${DB_PATH}
ENABLE_DEV_LOGIN=false
APP_BASE_URL=http://localhost
ENVEOF
  chmod 600 "${ENV_FILE}"
  ok "Created ${ENV_FILE} (edit to add OAuth keys)"
else
  ok "${ENV_FILE} already exists — skipping"
fi

# ── Phase 6 — Database ────────────────────────────────────────────
hdr "Phase 6 — Database"
"${VENV}/bin/python" - <<'PYEOF'
import sys, os
sys.path.insert(0, '/opt/pc-prep')
from dotenv import load_dotenv
load_dotenv('/opt/pc-prep/.env')
from app.database import create_all, SessionLocal
from app.content_loader import seed_course_if_empty
create_all()
db = SessionLocal()
try:
    seed_course_if_empty(db)
finally:
    db.close()
print("Schema and seed complete")
PYEOF
chown "$RUN_AS:$RUN_AS" "$DB_PATH" 2>/dev/null || true
chown "$RUN_AS:$RUN_AS" "$APP_DIR" 2>/dev/null || true
ok "Database ready"

# ── Phase 7 — Ownership ───────────────────────────────────────────
hdr "Phase 7 — File ownership"
chown -R "${RUN_AS}:${RUN_AS}" "${APP_DIR}"
ok "Ownership set to ${RUN_AS}"

# ── Phase 8 — Systemd service ─────────────────────────────────────
hdr "Phase 8 — Systemd service"
cat > "/etc/systemd/system/${APP_NAME}.service" <<SVCEOF
[Unit]
Description=P&C License Prep Academy
After=network.target

[Service]
Type=simple
User=${RUN_AS}
WorkingDirectory=${APP_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${VENV}/bin/uvicorn app.main:app --host 127.0.0.1 --port ${PORT}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
SVCEOF
systemctl daemon-reload
systemctl enable "${APP_NAME}"
systemctl restart "${APP_NAME}"
ok "Service ${APP_NAME} started"

# ── Phase 9 — Nginx ───────────────────────────────────────────────
hdr "Phase 9 — Nginx"
cat > "/etc/nginx/sites-available/${APP_NAME}" <<NGXEOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:${PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGXEOF
ln -sf "/etc/nginx/sites-available/${APP_NAME}" "/etc/nginx/sites-enabled/${APP_NAME}"
nginx -t && systemctl reload nginx
ok "Nginx configured"

echo ""
ok "Install complete. Visit http://your-server-ip"
echo "   Edit ${ENV_FILE} to add OAuth keys, then: sudo systemctl restart ${APP_NAME}"
