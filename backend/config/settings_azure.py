"""Production settings for the single-instance academic Azure deployment."""
import os
from .settings import *  # noqa: F403

DEBUG = False
if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5 or SECRET_KEY.startswith("django-insecure-"):
    raise ValueError("Azure requiere una DJANGO_SECRET_KEY nueva, aleatoria y de al menos 50 caracteres.")
AZURE_HOST = os.environ["AZURE_APP_HOST"]
ALLOWED_HOSTS = [AZURE_HOST]
APP_ORIGIN = f"https://{AZURE_HOST}"
CSRF_TRUSTED_ORIGINS = [APP_ORIGIN]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
MIDDLEWARE = [*MIDDLEWARE, "django.middleware.clickjacking.XFrameOptionsMiddleware"]
DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}
DATABASES["default"]["CONN_MAX_AGE"] = 60
# App Service persists /home; never put private uploads inside the static root.
MEDIA_ROOT = Path("/home/ecogest/media")
ROOT_URLCONF = "config.urls_azure"
AI_ENABLED = False
AI_BUDGET_AUTHORIZED = False
OPENAI_SMOKE_TEST = False
