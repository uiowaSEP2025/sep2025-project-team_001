# django_backend/urls.py

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django_backend import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
]

# Only serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
