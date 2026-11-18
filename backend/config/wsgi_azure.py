import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_azure")
application = WhiteNoise(get_wsgi_application())
application.add_files(Path(__file__).resolve().parent.parent / "web" / "assets", prefix="assets/")
