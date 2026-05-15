"""
URL configuration for Smart Academic Result Portal.

Includes admin, student accounts, results dashboard, and media files in DEBUG.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Smart Academic Result Portal"
admin.site.site_title = "Result Portal Admin"
admin.site.index_title = "Manage students and result PDFs"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("results.urls")),
]

# Serve uploaded PDFs during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
