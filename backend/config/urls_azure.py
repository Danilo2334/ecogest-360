from django.conf import settings
from django.http import FileResponse
from django.urls import re_path
from .urls import urlpatterns as api_patterns


def frontend(request):
    response = FileResponse(
        (settings.BASE_DIR / "web" / "index.html").open("rb"),
        content_type="text/html; charset=utf-8",
    )
    response["Cache-Control"] = "no-cache"
    return response


urlpatterns = [*api_patterns, re_path(
    r"^(?:|registros|lotes(?:/[0-9a-fA-F-]+)?|compostaje|incidencias|institucion|simulador|planes|asistente)/?$",
    frontend,
)]
