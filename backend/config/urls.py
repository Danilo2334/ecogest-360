from django.urls import path, re_path
from core.views import csrf, sign_in, dispatch

urlpatterns = [
    path("api/session/csrf", csrf),
    path("api/session/login", sign_in),
    re_path(r"^api/(?P<path>.+)$", dispatch),
]
