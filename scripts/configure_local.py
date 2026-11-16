"""Create ignored local settings with random secrets, without printing credentials."""

from pathlib import Path
import secrets

path = Path(__file__).resolve().parent.parent / ".env"
if path.exists():
    raise SystemExit(".env already exists; preserved without changes.")
content = (
    f"DJANGO_SECRET_KEY={secrets.token_urlsafe(48)}\nDJANGO_DEBUG=1\n"
    f"DB_NAME=ecogest\nDB_USER=ecogest\nDB_PASSWORD={secrets.token_urlsafe(32)}\n"
    f"DB_HOST=127.0.0.1\nDB_PORT=55436\nDEMO_PASSWORD={secrets.token_urlsafe(24)}\n"
    "APP_ORIGIN=http://127.0.0.1:5178\n"
)
with path.open("x", encoding="utf-8") as file:
    file.write(content)
print("Created .env locally with random secrets. Do not publish this file.")
